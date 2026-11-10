"""Print a Markdown table of merge-ready PRs in ballerina-nutcracker/ballerina.

A PR is merge-ready when all of these hold:
- open, not a draft, no don't-merge/dnm/hold/wip label
- GitHub reports it mergeable (no conflicts)
- every CI check on the head passed (skipped/neutral count as passed; pending or failed do not)
- our latest "PR review summary" reviewed the current head and reports 0 findings
- none of our finding threads is unresolved

REST only (works in Claude Code cloud sessions). A PR whose data can't be fetched is listed
under "Could not check".
"""
import re

from ghrest import GhError, ci_state, mergeability, open_prs, pr_detail, review_decision, skipped_by_label, \
    summaries, unresolved_finding_threads


def why_not_ready(p):
    n, sha = p["number"], p["head"]["sha"]
    merge = mergeability(pr_detail(n))
    if merge != "MERGEABLE":
        return "conflicting" if merge == "CONFLICTING" else "mergeability unknown"
    bodies = summaries(n)
    body = bodies[-1] if bodies else ""
    shas = re.findall(r"reviewed `([0-9a-f]{7,40})", body)
    if not shas or not sha.startswith(shas[-1]):
        return "not reviewed at current head"
    status = next((line for line in body.splitlines() if "reviewed `" in line), "")
    if not status.startswith("0 findings"):
        return "open findings"
    if unresolved_finding_threads(n):
        return "unresolved finding threads"
    failed, pending = ci_state(sha)
    if failed:
        return "CI failed: " + ", ".join(failed[:3])
    if pending:
        return f"CI pending ({pending})"
    return None


# Order of the "Not ready" groups: what the PR author can act on first.
GROUPS = ["open findings", "unresolved finding threads", "CI failed", "CI pending", "conflicting",
          "not reviewed at current head", "mergeability unknown", "could not check"]


def group_of(why):
    return next((g for g in GROUPS if why.startswith(g)), why)


def link(p):
    return f"[#{p['number']}]({p['html_url']})"


def main():
    ready, blocked = [], []
    for p in sorted(open_prs(), key=lambda p: p["number"]):
        if p["draft"] or skipped_by_label(p):
            continue
        try:
            why = why_not_ready(p)
            decision = review_decision(p["number"]) if why is None else ""
        except GhError:
            blocked.append((p, "could not check (GitHub didn't answer)"))
            continue
        if why:
            blocked.append((p, why))
        else:
            ready.append((p, decision))

    print(f"## Merge-ready ({len(ready)})\n")
    print("| PR | Title | Author | Approval | Reviewed |")
    print("|---|---|---|---|---|")
    for p, decision in ready:
        print(f"| {link(p)} | {p['title'][:70]} | {p['user']['login']} | "
              f"{decision.replace('_', ' ').lower()} | `{p['head']['sha'][:9]}` |")
    if not ready:
        print("| — | no merge-ready PRs | | | |")

    if blocked:
        counts = {}
        for _, why in blocked:
            counts[group_of(why)] = counts.get(group_of(why), 0) + 1
        order = {g: i for i, g in enumerate(GROUPS)}
        blocked.sort(key=lambda b: (order.get(group_of(b[1]), len(GROUPS)), b[0]["number"]))
        print(f"\n## Not ready ({len(blocked)})\n")
        print(" · ".join(f"{g}: {n}" for g, n in sorted(counts.items(), key=lambda kv: order.get(kv[0], len(GROUPS)))))
        print("\n| PR | Title | Author | Why |")
        print("|---|---|---|---|")
        for p, why in blocked:
            print(f"| {link(p)} | {p['title'][:60]} | {p['user']['login']} | {why} |")


if __name__ == "__main__":
    main()

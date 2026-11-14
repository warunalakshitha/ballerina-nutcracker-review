"""Print Markdown tables of open PRs in ballerina-nutcracker/ballerina: Can merge (merge-queue PRs first,
in queue order), Cannot merge (with why; a queued PR with open findings is flagged there), and Drafts and held
(drafts and don't-merge/dnm/hold/wip labels, which aren't reviewed).

A PR can merge when all of these hold:
- open, not a draft, no don't-merge/dnm/hold/wip label
- GitHub reports it mergeable (no conflicts)
- based on the default branch (a stacked PR waits for the PR below it)
- no CI check on the head failed (skipped/neutral count as passed; pending ones show as "after CI pending")
- our latest "PR review summary" reviewed the current head and reports 0 findings
- none of our finding threads is unresolved

REST only (works in Claude Code cloud sessions). A PR whose data can't be fetched is listed
under "Could not check".
"""
import functools
import re

from ghrest import DONT_MERGE, REPO, GhError, api, ci_state, merge_queue, mergeability, open_prs, pr_detail, review_decision, \
    skipped_by_label, summaries, unresolved_finding_threads, changes_requested_by, unresolved_other_threads

# Stack members share base PRs, so fetch each PR's detail once.
detail = functools.lru_cache(maxsize=None)(pr_detail)


def stack_blocker(p, by_head):
    """Why a stacked PR can't be reviewed yet, walking its base PRs down to the default branch, or None.
    The round reviews a stack only when it merges into main, so a conflicting base PR blocks every
    PR above it even though GitHub reports each one mergeable into its own base."""
    seen, cur = {p["number"]}, p
    while cur["base"]["ref"] != p["base"]["repo"]["default_branch"]:
        base = cur["base"]["ref"]
        q = by_head.get(base)
        if q is None:
            owner = REPO.split("/")[0]
            closed = api(f"repos/{REPO}/pulls?state=closed&head={owner}:{base}&per_page=10") or []
            merged = next((c for c in closed if c.get("merged_at")), None)
            if merged:
                return f"base #{merged['number']} already merged; rebase onto {p['base']['repo']['default_branch']}"
            return f"base branch `{base}` has no open PR"
        if q["number"] in seen:
            return None
        seen.add(q["number"])
        if mergeability(detail(q["number"])) == "CONFLICTING":
            return f"stacked on conflicting #{q['number']}"
        cur = q
    return None


def why_not_ready(p, by_head):
    n, sha = p["number"], p["head"]["sha"]
    merge = mergeability(detail(n))
    if merge != "MERGEABLE":
        return "conflicting" if merge == "CONFLICTING" else "mergeability unknown"
    bodies = summaries(n)
    body = bodies[-1] if bodies else ""
    shas = re.findall(r"reviewed `([0-9a-f]{7,40})", body)
    if not shas or not sha.startswith(shas[-1]):
        blocker = stack_blocker(p, by_head)
        if blocker:
            return blocker
        # scan_prs.py skips PRs a human approved at this head, so say so instead of implying a miss.
        if review_decision(n, sha) == "APPROVED":
            return "approved at head; our review is older"
        if not shas:
            return "awaiting first review"
        return f"awaiting re-review: pushed since our review of `{shas[-1][:9]}`"
    status = next((line for line in body.splitlines() if "reviewed `" in line), "")
    if not status.startswith("0 findings"):
        counts = re.findall(r"\*\*(\d+ [A-Za-z]+)\*\*", status)
        return "open findings" + (": " + ", ".join(counts) if counts else "")
    if unresolved_finding_threads(n):
        return "unresolved finding threads"
    by = changes_requested_by(n)
    if by:
        return "changes requested by " + ", ".join(by)
    other = unresolved_other_threads(n)
    if other:
        return "unresolved review threads: " + ", ".join(f"{k} {w}" for w, k in sorted(other.items()))
    failed, pending = ci_state(sha)
    if failed:
        return "CI failed: " + ", ".join(failed[:3])
    base = p["base"]["ref"]
    if base != p["base"]["repo"]["default_branch"]:
        # Clean, but it lands only after the PR below it in the stack merges.
        q = by_head.get(base)
        return stack_blocker(p, by_head) or (f"stacked: merge #{q['number']} first" if q else f"stacked on `{base}`")
    if pending:
        return f"CI pending ({pending})"
    return None


# Order of the "Not ready" groups: what the PR author can act on first.
GROUPS = ["open findings", "unresolved finding threads", "changes requested", "unresolved review threads", "CI failed", "conflicting", "stacked on conflicting",
          "base #", "base branch", "stacked", "awaiting re-review", "awaiting first review",
          "approved at head; our review is older", "mergeability unknown", "could not check"]
GROUP_NAMES = {"base #": "base already merged", "base branch": "base branch has no open PR"}


def group_of(why):
    return next((g for g in GROUPS if why.startswith(g)), why)


def title(p, width):
    return p["title"][:width].replace("|", "\\|")


def link(p):
    return f"[#{p['number']}]({p['html_url']})"


def auto_merge(p):
    """Auto-merge lands a PR once GitHub's required checks and approvals pass, whatever our findings say."""
    am = p.get("auto_merge")
    if not am:
        return "—"
    return f"on ({am.get('merge_method', '?')}, {(am.get('enabled_by') or {}).get('login', '?')})"


def main():
    mergeable, blocked, parked = [], [], []
    prs = sorted(open_prs(), key=lambda p: p["number"])
    by_head = {p["head"]["ref"]: p for p in prs if (p["head"].get("repo") or {}).get("full_name") == REPO}
    queue_read = merge_queue({p["number"] for p in prs})
    queue = queue_read or {}
    for p in prs:
        if p["draft"]:
            parked.append((p, "draft"))
            continue
        if skipped_by_label(p):
            labels = [l["name"] for l in p.get("labels", []) if any(k in l["name"].lower() for k in DONT_MERGE)]
            parked.append((p, "label: " + ", ".join(labels)))
            continue
        try:
            why = why_not_ready(p, by_head)
            # 0 findings, mergeable, reviewed at head: with only CI left it counts as mergeable once CI passes.
            waits = bool(why) and why.startswith("CI pending")
            decision = review_decision(p["number"], p["head"]["sha"]) if why is None or waits else ""
        except GhError:
            blocked.append((p, "could not check (GitHub didn't answer)"))
            continue
        q = queue.get(p["number"])
        if why and not waits:
            # Queued with our findings still open: it lands anyway, so flag it.
            blocked.append((p, why + (f" · in merge queue (#{q[0]})" if q else "")))
        elif q:
            # The queue runs its own checks, so pending CI on the head doesn't matter here.
            mergeable.append((p, f"in merge queue (#{q[0]}, {q[1]})", decision))
        else:
            mergeable.append((p, f"after {why}" if waits else "ready", decision))
    # Queued PRs first, in queue order; the rest keep PR order.
    mergeable.sort(key=lambda m: queue[m[0]["number"]][0] if m[0]["number"] in queue else len(queue) + 1)

    ready = sum(1 for _, s, _ in mergeable if s == "ready")
    in_queue = sum(1 for _, s, _ in mergeable if s.startswith("in merge queue"))
    print(f"**Open PRs: {len(prs)}** · can merge: {len(mergeable)} ({in_queue if queue_read is not None else '?'} in merge queue, {ready} ready,"
          f" {len(mergeable) - ready - in_queue} after CI)"
          f" · cannot merge: {len(blocked)}"
          f" · drafts: {sum(1 for _, w in parked if w == 'draft')}"
          f" · held by label (don't-merge/dnm/hold/wip): {sum(1 for _, w in parked if w != 'draft')}\n")
    print(f"## Can merge ({len(mergeable)})\n")
    if queue_read is None:
        print("Couldn't read the merge queue; a queued PR shows as `ready` here.\n")
    print("0 findings, no changes requested, no unresolved review threads (ours, humans' or CodeRabbit's), no conflicts, reviewed at the current head, not waiting on another PR.\n")
    print("| PR | Title | Author | Approval | Auto-merge | Status |")
    print("|---|---|---|---|---|---|")
    for p, state, decision in mergeable:
        print(f"| {link(p)} | {title(p, 70)} | {p['user']['login']} | "
              f"{decision.replace('_', ' ').lower()} | {auto_merge(p)} | {state} |")
    if not mergeable:
        print("| — | none | | | | |")

    if blocked:
        counts = {}
        for _, why in blocked:
            counts[group_of(why)] = counts.get(group_of(why), 0) + 1
        order = {g: i for i, g in enumerate(GROUPS)}
        print(f"\n## Cannot merge ({len(blocked)})\n")
        print(" · ".join(f"{GROUP_NAMES.get(g, g)}: {n}" for g, n in sorted(counts.items(), key=lambda kv: order.get(kv[0], len(GROUPS)))))
        print("\nAuto-merge on a PR here merges it once GitHub's requirements pass, open findings or not.\n")
        print("| PR | Title | Author | Auto-merge | Why |")
        print("|---|---|---|---|---|")
        for p, why in blocked:
            print(f"| {link(p)} | {title(p, 60)} | {p['user']['login']} | {auto_merge(p)} | {why} |")


    # Not reviewed at all: drafts and PRs held by a don't-merge/dnm/hold/wip label.
    print(f"\n## Drafts and held ({len(parked)})\n")
    print("Not reviewed until the PR is marked ready or the label is removed.\n")
    print("| PR | Title | Author | Why |")
    print("|---|---|---|---|")
    for p, why in parked:
        print(f"| {link(p)} | {title(p, 60)} | {p['user']['login']} | {why} |")
    if not parked:
        print("| — | none | | |")



if __name__ == "__main__":
    main()

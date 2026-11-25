"""Print Markdown tables of open PRs in ballerina-nutcracker/ballerina: Can merge (merge-queue PRs first,
in queue order), Cannot merge (with why; a queued PR with open findings is flagged there), and Drafts and held
(drafts and don't-merge/dnm/hold/wip labels, which aren't reviewed).

A PR can merge when all of these hold:
- open, not a draft, no don't-merge/dnm/hold/wip label
- GitHub reports it mergeable (no conflicts)
- based on the default branch (a stacked PR waits for the PR below it)
- no CI check on the head failed (skipped/neutral count as passed; pending ones show as "after CI pending")
- our latest "PR review summary" reviewed the current head and reports 0 findings, not counting 📝 Commit/PR ones
  (commit history, PR title or body): those leave the PR under Can merge with a warning to fix them first,
  since a merge-commit or rebase merge lands the commits as they are
- none of our finding threads is unresolved
Findings the summary still lists count as closed when the author has replied to every one; the PR's row in
Can merge or Cannot merge says how many, for a manual check. A "👤 For a human" item in our summary (an author's
answer to one of our findings, linked) doesn't block merging; the For a human table lists every one, whatever the
PR's state, until the reviewer reacts 👍 to the answer and the next round drops it.

REST only (works in Claude Code cloud sessions). A PR whose data can't be fetched is listed
under "Could not check".
"""
import functools
import re

from ghrest import DONT_MERGE, REPO, GhError, api, ci_state, merge_queue, mergeability, open_prs, pr_detail, review_decision, \
    skipped_by_label, summaries, answered_findings, unresolved_finding_threads, changes_requested_by, unresolved_other_threads, \
    COMMIT_LABEL, code_findings, status_counts

# Stack members share base PRs, so fetch each PR's detail once.
detail = functools.lru_cache(maxsize=None)(pr_detail)
summaries = functools.lru_cache(maxsize=None)(summaries)
answered_findings = functools.lru_cache(maxsize=None)(answered_findings)


def queue_removal(n):
    """(time, actor) of the PR's last removal from the merge queue when it hasn't been re-added since, else None."""
    last = None
    for e in api(f"repos/{REPO}/issues/{n}/timeline", paginate=True) or []:
        if e.get("event") == "added_to_merge_queue":
            last = None
        elif e.get("event") == "removed_from_merge_queue":
            last = (e["created_at"][:16].replace("T", " "), (e.get("actor") or {}).get("login", "?"))
    return last


def latest_summary(n):
    bodies = summaries(n)
    return bodies[-1] if bodies else ""


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


def human_checks(p):
    """'👤 For a human' items in our latest summary (authors' answers to check), even if the PR moved since."""
    body = latest_summary(p["number"])
    return [line.split("·", 1)[1].strip() for line in body.splitlines() if line.startswith("- 👤 **For a human** ·")]


def commit_items(p):
    """📝 Commit/PR findings our summary lists at the PR's current head (0 if it reviewed an older head)."""
    body = latest_summary(p["number"])
    shas = re.findall(r"reviewed `([0-9a-f]{7,40})", body)
    if not shas or not p["head"]["sha"].startswith(shas[-1]):
        return 0
    return status_counts(body).get(COMMIT_LABEL, 0)


def commit_warning(k):
    return f" · ⚠️ fix {k} Commit/PR item{'s' if k > 1 else ''} first (squash, reword or rebase)" if k else ""


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
    # Findings the author answered (declined, deferred) count as closed, though the summary still lists them.
    # Commit/PR findings don't block: the Can merge row warns about them instead.
    open_code = code_findings(body)
    answered = open_code and answered_findings(n, body)
    if open_code and not answered:
        counts = [f"{k} {label}{'s' if label == 'Nit' and k > 1 else ''}" for label, k in status_counts(body).items()]
        return "open findings" + (": " + ", ".join(counts) if counts else "")
    if not answered and unresolved_finding_threads(n):
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
    mergeable, blocked, parked, humans, removed = [], [], [], [], []
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
            checks = human_checks(p)
            answered = answered_findings(p["number"], latest_summary(p["number"]))
            commits = commit_items(p)
            q = queue.get(p["number"])
            removal = None if q else queue_removal(p["number"])
        except GhError:
            blocked.append((p, "could not check (GitHub didn't answer)"))
            continue
        if checks:
            humans.append((p, checks))
        note = f" ({answered} answered by the author, check by hand)" if answered else ""
        if not why or waits:
            note += commit_warning(commits)
        if removal:
            # The queue rejected it (or someone took it out): listed only in its own table, not as mergeable.
            # The queue takes only PRs approved at their head; a push since the approval makes GitHub ask again.
            if not why:
                why = "re-queue it" if decision == "APPROVED" else "needs an approval at head before it can be re-queued"
            removed.append((p, removal, why + note))
            continue
        if why and not waits:
            # Queued with our findings still open: it lands anyway, so flag it.
            blocked.append((p, why + note + (f" · in merge queue (#{q[0]})" if q else "")))
        elif q:
            # The queue runs its own checks, so pending CI on the head doesn't matter here.
            mergeable.append((p, f"in merge queue (#{q[0]}, {q[1]})" + note, decision))
        else:
            mergeable.append((p, (f"after {why}" if waits else "ready") + note, decision))
    # Queued PRs first, in queue order; the rest keep PR order.
    mergeable.sort(key=lambda m: queue[m[0]["number"]][0] if m[0]["number"] in queue else len(queue) + 1)

    ready = sum(1 for _, s, _ in mergeable if s.startswith("ready"))
    in_queue = sum(1 for _, s, _ in mergeable if s.startswith("in merge queue"))
    print("## Summary\n")
    print("| Open PRs | Count |")
    print("|---|---|")
    print(f"| **All open** | **{len(prs)}** |")
    print(f"| Can merge | {len(mergeable)} |")
    print(f"| ↳ in merge queue | {in_queue if queue_read is not None else '?'} |")
    print(f"| ↳ ready | {ready} |")
    print(f"| ↳ after CI | {len(mergeable) - ready - in_queue} |")
    print(f"| Cannot merge | {len(blocked)} |")
    print(f"| Removed from merge queue | {len(removed)} |")
    print(f"| For a human (answers to check) | {sum(len(h) for _, h in humans)} |")
    print(f"| Drafts | {sum(1 for _, w in parked if w == 'draft')} |")
    print(f"| Held by label (don't-merge/dnm/hold/wip) | {sum(1 for _, w in parked if w != 'draft')} |\n")
    print(f"## Can merge ({len(mergeable)})\n")
    if queue_read is None:
        print("Couldn't read the merge queue; a queued PR shows as `ready` here.\n")
    print("0 findings (📝 Commit/PR items aside: the Status column warns to fix them before merging, as a merge-commit or rebase merge lands commits as they are), no changes requested, no unresolved review threads (ours, humans' or CodeRabbit's), no conflicts, reviewed at the current head, not waiting on another PR.\n")
    print("| PR | Title | Author | Approval | Auto-merge | Status |")
    print("|---|---|---|---|---|---|")
    for p, state, decision in mergeable:
        print(f"| {link(p)} | {title(p, 70)} | {p['user']['login']} | "
              f"{decision.replace('_', ' ').lower()} | {auto_merge(p)} | {state} |")
    if not mergeable:
        print("| — | none | | | | |")

    if removed:
        print(f"\n## Removed from merge queue ({len(removed)})\n")
        print("Taken out of the merge queue (usually by the queue, when its checks failed) and not re-added. "
              "Listed only here, not under Can merge or Cannot merge; Now says what still blocks each one.\n")
        print("| PR | Title | Author | Removed (UTC) | By | Now |")
        print("|---|---|---|---|---|---|")
        for p, (at, by), why in removed:
            print(f"| {link(p)} | {title(p, 60)} | {p['user']['login']} | {at} | {by} | {why} |")

    if humans:
        print(f"\n## For a human ({len(humans)})\n")
        print("Authors' answers to our findings (declined, explained, or resolved without a change). They don't block merging. "
              "Check each one and react 👍 to the linked answer; the next review round drops it.\n")
        print("| PR | Title | Author | Check |")
        print("|---|---|---|---|")
        for p, items in humans:
            for h in items:
                cell = h.replace("|", "\\|")
                print(f"| {link(p)} | {title(p, 60)} | {p['user']['login']} | {cell} |")

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

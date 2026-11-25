"""List open PRs a sweep still has to re-review: our latest summary was written by skills older than
the sweep's target commit (or there is no summary yet).

Usage: python3 sweep_candidates.py <target-skills-commit> [--include-approved]
  Run with $TOOLS as the current repo or set TOOLS; the summary marker's `tools=<sha>` is compared with
  the target in that checkout (`git merge-base --is-ancestor`), so it must not be shallow.

Prints one line per candidate: first every PR whose head moved since our last summary
(`<N> MOVED <reviewed sha> -> <head> <merge>`, as scan_prs.py reports it: hourly rounds are paused during a
sweep, so an author who pushed is reviewed first), then the stale ones, oldest PR first
(`<N> STALE <tools sha or none> <MERGEABLE|UNKNOWN>`).
Skips what scan_prs.py skips (drafts, don't-merge/dnm/hold/wip labels, PRs approved at their head, unless
--include-approved is given),
conflicting PRs, which a review would only report as conflicting, and PRs in the merge queue, which are
about to land. Fetch failures print ERR.
A swept PR whose author answered our findings since its summary is listed with the moved ones
(`<N> REPLIED <head> <k> new <merge>`, as scan_prs.py reports it), and so is one with a 👤 For a human line
we've checked off with 👍 (`<N> CHECKED <head> <k> checked <merge>`), and one whose author edited the PR title or body
since a summary that lists a 📝 Commit/PR item (`<N> EDITED <head> <merge>`); a stale PR's full re-review reads replies anyway.
Exit status 0 with no output means the sweep is done.
"""
import os
import re
import subprocess
import sys

from ghrest import (GhError, merge_queue, mergeability, open_prs, pr_detail, replies_since_summary, review_decision,
                    skipped_by_label, summaries, checked_human, text_edited)

TOOLS = os.environ.get("TOOLS", ".")
TOOLS_RE = re.compile(r"<!-- pre-pr-review:summary [^>]*\btools=([0-9a-f]{7,40})")


def swept(tools_sha, target):
    """True when the summary's tools commit already includes the target skills commit."""
    if not tools_sha:
        return False
    r = subprocess.run(["git", "-C", TOOLS, "merge-base", "--is-ancestor", target, tools_sha],
                       capture_output=True, text=True)
    return r.returncode == 0


def main():
    args = sys.argv[1:]
    include_approved = "--include-approved" in args
    if include_approved:
        args.remove("--include-approved")
    if len(args) != 1:
        sys.exit("usage: sweep_candidates.py <target-skills-commit> [--include-approved]")
    target = args[0]
    if subprocess.run(["git", "-C", TOOLS, "cat-file", "-e", f"{target}^{{commit}}"]).returncode != 0:
        sys.exit(f"sweep_candidates: target {target} is not a commit in {TOOLS}")
    moved, stale = [], []
    prs = open_prs()
    queued = merge_queue({p["number"] for p in prs})
    if queued is None:
        print("sweep_candidates: merge queue unreadable, not skipping queued PRs", file=sys.stderr)
        queued = {}
    for p in sorted(prs, key=lambda p: p["number"]):
        if p["draft"] or skipped_by_label(p) or p["number"] in queued:
            continue
        n, sha = p["number"], p["head"]["sha"]
        try:
            if not include_approved and review_decision(n, sha) == "APPROVED":
                continue
            bodies = summaries(n)
            merge = mergeability(pr_detail(n))
        except GhError as e:
            print(n, "ERR", sha[:9], e)
            continue
        if merge == "CONFLICTING":
            continue
        reviewed = re.findall(r"reviewed `([0-9a-f]{7,40})", bodies[-1]) if bodies else []
        if reviewed and not sha.startswith(reviewed[-1]):
            moved.append(f"{n} MOVED {reviewed[-1]} -> {sha[:9]} {merge}")
            continue
        tools = TOOLS_RE.findall(bodies[-1]) if bodies else []
        tools_sha = tools[-1] if tools else None
        if not swept(tools_sha, target):
            stale.append(f"{n} STALE {tools_sha or 'none'} {merge}")
            continue
        try:
            replies = replies_since_summary(n, p["user"]["login"])
        except GhError as e:
            print(n, "ERR", sha[:9], e)
            continue
        if replies:
            moved.append(f"{n} REPLIED {sha[:9]} {replies} new {merge}")
        elif checked := checked_human(bodies[-1]):
            moved.append(f"{n} CHECKED {sha[:9]} {checked} checked {merge}")
        elif text_edited(bodies[-1], p):
            moved.append(f"{n} EDITED {sha[:9]} {merge}")
    for line in moved + stale:
        print(line)


if __name__ == "__main__":
    main()

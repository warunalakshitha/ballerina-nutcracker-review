"""List open PRs a sweep still has to re-review: our latest summary was written by skills older than
the sweep's target commit (or there is no summary yet).

Usage: python3 sweep_candidates.py <target-skills-commit>
  Run with $TOOLS as the current repo or set TOOLS; the summary marker's `tools=<sha>` is compared with
  the target in that checkout (`git merge-base --is-ancestor`), so it must not be shallow.

Prints one line per candidate: first every PR whose head moved since our last summary
(`<N> MOVED <reviewed sha> -> <head> <merge>`, as scan_prs.py reports it: hourly rounds are paused during a
sweep, so an author who pushed is reviewed first), then the stale ones, oldest PR first
(`<N> STALE <tools sha or none> <MERGEABLE|UNKNOWN>`).
Skips what scan_prs.py skips (drafts, don't-merge/dnm/hold/wip labels, PRs approved at their head) and
conflicting PRs, which a review would only report as conflicting. Fetch failures print ERR.
Exit status 0 with no output means the sweep is done.
"""
import os
import re
import subprocess
import sys

from ghrest import GhError, mergeability, open_prs, pr_detail, review_decision, skipped_by_label, summaries

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
    if len(sys.argv) != 2:
        sys.exit("usage: sweep_candidates.py <target-skills-commit>")
    target = sys.argv[1]
    if subprocess.run(["git", "-C", TOOLS, "cat-file", "-e", f"{target}^{{commit}}"]).returncode != 0:
        sys.exit(f"sweep_candidates: target {target} is not a commit in {TOOLS}")
    moved, stale = [], []
    for p in sorted(open_prs(), key=lambda p: p["number"]):
        if p["draft"] or skipped_by_label(p):
            continue
        n, sha = p["number"], p["head"]["sha"]
        try:
            if review_decision(n, sha) == "APPROVED":
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
    for line in moved + stale:
        print(line)


if __name__ == "__main__":
    main()

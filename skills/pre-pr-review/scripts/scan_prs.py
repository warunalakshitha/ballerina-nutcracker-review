"""List open PRs needing review: NEW (no summary of ours yet) or MOVED (head differs from the
commit our last summary reviewed). Skips drafts, PRs approved at their current head and don't-merge/dnm/hold/wip labels.
Fetch failures print ERR, never NEW. REST only (works in Claude Code cloud sessions).

A PR whose head was pushed less than SETTLE_MINUTES ago (default 30) is left out, so a burst of pushes is
reviewed once, at its final commit; it's named on stderr as SETTLING and shows up in a later scan."""
import os
import re
import sys
from datetime import datetime, timedelta, timezone

from ghrest import GhError, mergeability, open_prs, pr_detail, pushed_at, review_decision, skipped_by_label, summaries

SETTLE = timedelta(minutes=float(os.environ.get("SETTLE_MINUTES", "30")))


def main():
    for p in sorted(open_prs(), key=lambda p: p["number"], reverse=True):
        if p["draft"] or skipped_by_label(p):
            continue
        n, sha = p["number"], p["head"]["sha"]
        try:
            if review_decision(n, p["head"]["sha"]) == "APPROVED":
                continue
            bodies = summaries(n)
            merge = mergeability(pr_detail(n))
        except GhError as e:
            print(n, "ERR", sha[:9], e)
            continue
        shas = re.findall(r"reviewed `([0-9a-f]{7,40})", bodies[-1]) if bodies else []
        if shas and sha.startswith(shas[-1]):
            continue
        try:
            age = datetime.now(timezone.utc) - pushed_at(sha)
        except GhError as e:
            print(n, "ERR", sha[:9], e)
            continue
        if age < SETTLE:
            print(n, "SETTLING", sha[:9], f"pushed {int(age.total_seconds() // 60)} min ago", file=sys.stderr)
            continue
        if not shas:
            print(n, "NEW", sha[:9], merge)
        elif not sha.startswith(shas[-1]):
            print(n, "MOVED", shas[-1], "->", sha[:9], merge)


if __name__ == "__main__":
    main()

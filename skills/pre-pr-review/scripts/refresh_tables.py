#!/usr/bin/env python3
"""Replace the open-PR tables in reports/latest.md with fresh ones from ready_table.py.

Run by .github/workflows/refresh-tables.yml after each round's report and hourly, with the reviewer's token, where
GraphQL (and so the merge queue) works, unlike in cloud sessions. Only the block from the `**Open PRs:` line up
to `## This round` changes; the round's own sections stay as written. A first line saying when the tables were
refreshed is kept just above them. Exits 1 without touching the report if ready_table.py fails.
"""
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
REPORT = os.path.join(ROOT, "reports/latest.md")
STAMP = "_Open-PR tables refreshed "


def main():
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "ready_table.py")],
                       capture_output=True, text=True, timeout=1800)
    if r.returncode != 0 or "**Open PRs:" not in r.stdout:
        print(f"ready_table.py failed:\n{r.stderr[-1000:]}")
        return 1
    text = open(REPORT).read()
    start = text.find("**Open PRs:")
    end = text.find("## This round")
    if start < 0 or end < start:
        print("reports/latest.md has no tables block to replace")
        return 1
    head = text[:start]
    if STAMP in head:
        head = head[:head.rindex(STAMP)]
    colombo = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M")
    tables = r.stdout.rstrip("\n") + "\n\n"
    open(REPORT, "w").write(head + f"{STAMP}{colombo} (Asia/Colombo)._\n\n" + tables + text[end:])
    print(f"tables refreshed at {colombo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

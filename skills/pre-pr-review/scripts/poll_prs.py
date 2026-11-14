#!/usr/bin/env python3
"""Start a cloud review round when there's new work (run hourly by .github/workflows/poll-prs.yml).

No Claude runs unless all of these hold:
  - no round holds reports/round.lock (updated hourly while a round runs; stale after 2 hours)
  - scan_prs.py ran cleanly (no ERR) and lists a mergeable PR that isn't in reports/last-scan.txt
    (scan_prs.py already leaves out PRs pushed less than 30 minutes ago, so bursts of pushes settle first)
  - this poller didn't already start a round for the same scan in the last 6 hours
    (reports/poller-fired.txt), so a round that keeps failing early isn't restarted every hour

Then it POSTs to the routine's API trigger (ROUTINE_FIRE_URL, ROUTINE_FIRE_TOKEN) and records the scan in
reports/poller-fired.txt; the workflow commits that file. Prints what it decided; exit 0 either way.
"""
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.environ.get("REVIEW_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
LOCK = os.path.join(ROOT, "reports/round.lock")
LAST = os.path.join(ROOT, "reports/last-scan.txt")
FIRED = os.path.join(ROOT, "reports/poller-fired.txt")
STALE = timedelta(hours=2)
REFIRE = timedelta(hours=6)


def now():
    return datetime.now(timezone.utc)


def lines(path):
    return sorted(l.strip() for l in open(path) if l.strip()) if os.path.exists(path) else None


def round_running():
    if not os.path.exists(LOCK):
        return None
    lock = dict(l.strip().split("=", 1) for l in open(LOCK) if "=" in l)
    try:
        if now() - datetime.fromisoformat(lock.get("heartbeat_utc") or lock["started_utc"]) <= STALE:
            return lock.get("started", "?")
    except (KeyError, ValueError):
        pass
    return None


def fire(scan):
    url, token = os.environ.get("ROUTINE_FIRE_URL"), os.environ.get("ROUTINE_FIRE_TOKEN")
    if not url or not token:
        print("ROUTINE_FIRE_URL or ROUTINE_FIRE_TOKEN not set: not starting a round")
        return False
    body = json.dumps({"text": "Started by poll_prs.py; the scan found:\n" + "\n".join(scan)}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {token}", "anthropic-beta": "experimental-cc-routine-2026-04-01",
        "anthropic-version": "2023-06-01", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            print("started a round:", json.loads(r.read()).get("claude_code_session_url", "?"))
            return True
    except urllib.error.HTTPError as e:
        print(f"starting the round failed: HTTP {e.code} {e.read().decode()[:300]}")
        return False


def main():
    running = round_running()
    if running:
        print(f"round {running} is running; nothing to do")
        return 0
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "scan_prs.py")],
                       capture_output=True, text=True, timeout=1800)
    if r.stderr.strip():
        print(r.stderr.strip())
    scan = sorted(l.strip() for l in r.stdout.splitlines() if l.strip())
    if r.returncode != 0 or any(" ERR " in f" {l} " for l in scan):
        print("scan failed or had ERR lines; trying again next time")
        return 0
    last = set(lines(LAST) or [])
    new = [l for l in scan if l not in last and l.endswith("MERGEABLE")]
    if not new:
        print("no new mergeable PR changes since the last round")
        return 0
    if os.path.exists(FIRED):
        fired = open(FIRED).read().split("\n", 1)
        try:
            when = datetime.fromisoformat(fired[0].strip())
        except ValueError:
            when = None
        if when and sorted(l for l in fired[1].splitlines() if l.strip()) == scan and now() - when < REFIRE:
            print(f"already started a round for this scan at {fired[0].strip()}; waiting")
            return 0
    print("new work:\n  " + "\n  ".join(new))
    if fire(scan):
        with open(FIRED, "w") as f:
            f.write(now().replace(microsecond=0).isoformat() + "\n" + "\n".join(scan) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

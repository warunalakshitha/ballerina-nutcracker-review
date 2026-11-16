#!/usr/bin/env python3
"""Helpers for cloud review rounds. Nothing here commits anything: the round keeps its lock, last scan and report
in the Ballerina Nutcracker Pull Request Review Board artifact (via ArtifactData), and GitHub writes go to the post-outbox Action as
repository_dispatch events.

  round_state.py unchanged <scan file> <saved scan file>
                                  exit 0 if the scan matches the saved one (nothing to do), 1 if it changed
                                  (a missing or empty saved scan, or an ERR line, counts as changed)
  round_state.py saved-scan <end scan> <start scan>
                                  print the lines to save: end-scan lines that were also in the start scan, so a
                                  PR pushed during the round looks new to the next run
  round_state.py send <STARTED> <file> <name>
                                  hand a GitHub write to the post-outbox Action (repository_dispatch). Check the
                                  lock is still ours on the board right before calling this.
  round_state.py wait-posted <findings.json> [minutes]
                                  wait (default 15 min) until the PR's summary shows the reviewed head
  round_state.py refresh-tables <report.md> <tables.md> <when>
                                  print the report with its open-PR tables (from the **Open PRs** line through the
                                  Drafts and held table) replaced by a fresh ready_table.py output, under a
                                  "Tables refreshed <when>" line; exit 0 if the tables changed, 1 if they didn't,
                                  2 if the report or the tables file has no tables block
"""
import os
import subprocess
import sys
import time

TOOLS = os.environ.get("TOOLS") or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))


def _lines(path):
    return sorted(l.strip() for l in open(path) if l.strip()) if path and os.path.exists(path) else []


def unchanged(scan_file, saved_file):
    new, old = _lines(scan_file), _lines(saved_file)
    if not old or any(" ERR" in l for l in new) or new != old:
        print("changed")
        return 1
    print("unchanged since the last round")
    return 0


def saved_scan(end_file, start_file):
    start = set(_lines(start_file))
    for l in _lines(end_file):
        if l in start:
            print(l)
    return 0


def _tools_repo():
    url = subprocess.run(["git", "-C", TOOLS, "remote", "get-url", "origin"], capture_output=True, text=True,
                         check=True).stdout.strip()
    return url.rstrip("/").removesuffix(".git").split("github.com/")[-1].split("github.com:")[-1]


def send(started, path, name):
    """Hand one item to the post-outbox Action as a repository_dispatch: gzip+base64 of the file, split over
    client_payload fields (GitHub allows 10 top-level fields and about 64 KB each). Nothing is committed."""
    import base64
    import gzip
    import json
    if "/" in name or not name.endswith(".json") or not name.startswith(("review-", "issue-", "ping-")):
        print("name must be review-<N>.json, issue-<slug>.json, issue-comment-<slug>.json or ping-<x>.json")
        return 2
    blob = base64.b64encode(gzip.compress(open(path, "rb").read())).decode()
    size = 60000
    parts = [blob[i:i + size] for i in range(0, len(blob), size)] or [""]
    if len(parts) > 7:
        print(f"{name} is too large to send ({len(blob)} bytes compressed)")
        return 1
    payload = {"name": name, "started": started, "parts": len(parts)}
    payload.update({f"p{i}": p for i, p in enumerate(parts)})
    body = json.dumps({"event_type": "post-item", "client_payload": payload})
    r = subprocess.run(["gh", "api", "-X", "POST", f"repos/{_tools_repo()}/dispatches", "--input", "-"],
                       input=body, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"dispatch failed: {(r.stderr or r.stdout).strip()[:300]}")
        return 1
    print(f"sent {name} to the post-outbox Action")
    return 0


def wait_posted(findings, minutes="15"):
    """Wait until the PR's latest "PR review summary" comment names the head this review covered."""
    import json
    import re
    data = json.load(open(findings))
    n, head = data["pr"], data["head_sha"]
    repo = data.get("repo", "ballerina-nutcracker/ballerina")
    deadline = time.time() + 60 * float(minutes)
    while True:
        r = subprocess.run(["gh", "api", f"repos/{repo}/issues/{n}/comments?per_page=100&sort=updated&direction=desc"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            bodies = [c["body"] for c in json.loads(r.stdout) if "PR review summary" in c.get("body", "")]
            shas = re.findall(r"reviewed `([0-9a-f]{7,40})", bodies[-1]) if bodies else []
            if any(head.startswith(s) for s in shas):
                print(f"#{n}: summary shows {head[:9]}: posted")
                return 0
        if time.time() > deadline:
            print(f"#{n}: summary doesn't show {head[:9]} yet: not posted (see the post-outbox Action runs)")
            return 1
        time.sleep(30)


TABLE_HEADINGS = ("## Can merge", "## For a human", "## Cannot merge", "## Drafts and held", "## Findings all answered")
REFRESHED = "_Tables refreshed "


def refresh_tables(report_file, tables_file, when):
    """Swap the report's open-PR tables for fresh ones, so merge-queue, approval and CI changes show between
    rounds even when no PR head moved."""
    lines = open(report_file).read().split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith("**Open PRs:")), None)
    if start is None:
        print("no **Open PRs** line in the report", file=sys.stderr)
        return 2
    while start > 0 and (lines[start - 1].startswith(REFRESHED) or not lines[start - 1].strip()):
        start -= 1
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("## ") and not lines[i].startswith(TABLE_HEADINGS)), len(lines))
    old = "\n".join(l for l in lines[start:end] if not l.startswith(REFRESHED)).strip()
    new = open(tables_file).read().strip()
    if not new.startswith("**Open PRs:"):
        print("the tables file doesn't start with an **Open PRs** line (did ready_table.py fail?)", file=sys.stderr)
        return 2
    if old == new:
        return 1
    head = lines[:start] + ([""] if start else [])
    block = [f"{REFRESHED}{when}; filed issues below are from the last round._", ""] + new.split("\n") + [""]
    print("\n".join(head + block + lines[end:]))
    return 0


def main():
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    commands = {"unchanged": (unchanged, 2), "saved-scan": (saved_scan, 2), "send": (send, 3), "wait-posted": (wait_posted, 2),
                "refresh-tables": (refresh_tables, 3)}
    if cmd == "wait-posted" and len(args) == 1:
        return wait_posted(args[0])
    if cmd not in commands or len(args) != commands[cmd][1]:
        print(__doc__)
        return 2
    return commands[cmd][0](*args)


if __name__ == "__main__":
    sys.exit(main())

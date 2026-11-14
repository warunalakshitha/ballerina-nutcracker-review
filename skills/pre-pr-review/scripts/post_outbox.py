#!/usr/bin/env python3
"""Post the GitHub writes a cloud round queued in outbox/ (run by .github/workflows/post-outbox.yml).

Cloud rounds can't write to ballerina-nutcracker/ballerina, so they commit each write to outbox/ on main
and this script posts it with the reviewer's token (GH_TOKEN, an Actions secret). Items:
  review-<N>.json         a findings.json: post_review.py --post
  issue-<slug>.json       {"title", "body", "labels": [...]}: a new issue
  issue-comment-<slug>.json  {"issue": N, "body"}: a comment on an issue or PR

A posted item is deleted. A review whose PR moved since it was reviewed is dropped (the next round
re-reviews). Anything else that fails stays for the next run, and the script exits 1 so the job fails.
Each line of outbox/posted.log records what happened; only the newest 100 lines are kept (the rest are in git history). Issues and comments carry a hidden marker so a
retry after a partly finished run doesn't post them twice.
"""
import datetime
import glob
import json
import os
import subprocess
import sys

from ghrest import ME, REPO, GhError, api

OUTBOX = "outbox"
LOG = os.path.join(OUTBOX, "posted.log")
LOG_KEEP = 100  # newest lines kept; older ones stay in git history
POST_REVIEW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "post_review.py")
MOVED = ("PR head is ", "moved to ")  # post_review.py's refusals when the PR changed since the review


def log(line):
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(line)
    old = open(LOG).read().splitlines() if os.path.exists(LOG) else []
    with open(LOG, "w") as f:
        f.write("\n".join((old + [f"{stamp} {line}"])[-LOG_KEEP:]) + "\n")


def write(path, payload):
    r = subprocess.run(["gh", "api", "-X", "POST", path, "--input", "-"], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise GhError((r.stderr or r.stdout).strip()[:300])
    return json.loads(r.stdout)


def marker(name):
    return f"<!-- pre-pr-review:outbox {name} -->"


def already_posted(items, name):
    return next((i for i in items or [] if i["user"]["login"] == ME and marker(name) in (i.get("body") or "")), None)


def post_review(path, name):
    r = subprocess.run([sys.executable, POST_REVIEW, path, "--post", "--ignore-warnings", "--out", "/tmp/preview.md"],
                       capture_output=True, text=True, timeout=1800)
    out = (r.stdout + r.stderr).strip()
    if r.returncode == 0:
        return "posted", f"review #{json.load(open(path)).get('pr', '?')}"
    if any(m in out for m in MOVED):
        return "dropped", f"review {name}: PR moved since the review ({out.splitlines()[-1][:160]})"
    return "failed", f"review {name}: {out[-300:]}"


def post_issue(path, name):
    item = json.load(open(path))
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    done = already_posted(api(f"repos/{REPO}/issues?creator={ME}&state=all&since={since}&per_page=100"), name)
    if done:
        return "posted", f"issue {name}: already filed as {done['html_url']}"
    made = write(f"repos/{REPO}/issues", {"title": item["title"], "body": item["body"] + "\n\n" + marker(name),
                                          "labels": item.get("labels", [])})
    return "posted", f"issue {name}: {made['html_url']}"


def post_comment(path, name):
    item = json.load(open(path))
    n = int(item["issue"])
    done = already_posted(api(f"repos/{REPO}/issues/{n}/comments?per_page=100", paginate=True), name)
    if done:
        return "posted", f"comment {name}: already posted as {done['html_url']}"
    made = write(f"repos/{REPO}/issues/{n}/comments", {"body": item["body"] + "\n\n" + marker(name)})
    return "posted", f"comment {name}: {made['html_url']}"


def main():
    login = api("user")["login"]
    if login != ME:
        print(f"GH_TOKEN belongs to {login}, not {ME}: nothing posted")
        return 1
    failed = 0
    for path in sorted(glob.glob(os.path.join(OUTBOX, "*.json"))):
        name = os.path.basename(path)
        kind = (post_review if name.startswith("review-") else post_comment if name.startswith("issue-comment-")
                else post_issue if name.startswith("issue-") else None)
        if kind is None:
            log(f"skipped {name}: unknown item type")
            continue
        try:
            state, what = kind(path, name)
        except (GhError, KeyError, ValueError, subprocess.TimeoutExpired) as e:
            state, what = "failed", f"{name}: {e}"
        log(f"{state} {what}")
        if state == "failed":
            failed += 1
        else:
            os.remove(path)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""List links the PR adds to ballerina-nutcracker/ballerina issues that are already closed.

Usage: $TOOLS/skills/pr-review/scripts/check_closed_issue_links.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it inside the PR worktree.

SKILL.md (Links to closed issues): a PR that adds a link to an already-closed ballerina-nutcracker/ballerina
issue (in a TODO, skip list, workaround, README or test comment) is a Nit. This script finds the added lines
that reference such an issue and asks GitHub for its state. A reference is an issue URL, `ballerina-nutcracker/ballerina#N`, or a bare `#N`
on a line that doesn't cite another repository (`ballerina-library`, `ballerina-lang`, `jBallerina`,
`ballerina-platform`). A URL with an `#issuecomment-` anchor is fine and is skipped; numbers that resolve to
pull requests are skipped.

  CLOSED   <path>:<line>: #<issue> (<state reason>, <title>)   the issue is closed at the time of the check

Read each hit: a link kept on purpose (e.g. "fixed in #N" history) is fine; report the rest as one Nit listing
the locations. Exit status 1 when anything is reported.
"""
import json
import re
import subprocess
import sys

REPO = "ballerina-nutcracker/ballerina"
URL = re.compile(r"ballerina-nutcracker/ballerina(?:/(?:issues|pull)/|#)(\d+)(#[\w-]+)?")
BARE = re.compile(r"(?<![\w/#])#(\d{2,6})\b")
OTHER_REPO = re.compile(r"ballerina-library|ballerina-lang\b|ballerina-platform|jballerina|module-ballerina", re.I)
SKIP_PATHS = re.compile(r"(^|/)(CHANGELOG|\.github/)")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def added_lines(base):
    """Yield (path, line number, text) for every line the PR adds."""
    diff = git("diff", "--no-color", "-U0", f"{base}...HEAD")
    path, line = None, 0
    for raw in diff.splitlines():
        if raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else None
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            line = int(m.group(1)) if m else 0
        elif raw.startswith("+") and path:
            yield path, line, raw[1:]
            line += 1


def refs_in(text):
    """Issue numbers the line references, URLs first; None entries mean the line is skipped."""
    out = []
    for m in URL.finditer(text):
        if m.group(2) and m.group(2).startswith("#issuecomment"):
            continue
        out.append(int(m.group(1)))
    if not out and not OTHER_REPO.search(text):
        out.extend(int(n) for n in BARE.findall(text))
    return out


def issue_state(n, cache):
    if n not in cache:
        r = subprocess.run(["gh", "api", f"repos/{REPO}/issues/{n}"], capture_output=True, text=True)
        if r.returncode != 0:
            cache[n] = None
        else:
            d = json.loads(r.stdout)
            cache[n] = None if d.get("pull_request") else (d["state"], d.get("state_reason") or "", d["title"])
    return cache[n]


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    base = git("merge-base", base_ref, "HEAD").strip()
    cache, hits = {}, []
    for path, line, text in added_lines(base):
        if SKIP_PATHS.search(path):
            continue
        for n in refs_in(text):
            st = issue_state(n, cache)
            if st and st[0] == "closed":
                hits.append(f"CLOSED   {path}:{line}: #{n} ({st[1] or 'closed'}, {st[2]})")
    for h in hits:
        print(h)
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()

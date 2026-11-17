#!/usr/bin/env python3
"""List CI checks that passed at the last reviewed head and fail at the current one.

Usage: $TOOLS/skills/pr-review/scripts/check_ci_regression.py <PR number> <last reviewed sha> [base-ref] [owner/repo]
  base-ref defaults to origin/main, owner/repo to ballerina-nutcracker/ballerina. Run it inside the PR worktree at
  the current head, with the last reviewed sha fetched. REST only (works in cloud sessions).

A check that fails now but passed at the head we last reviewed is not flaky by default. When the PR's own non-test
changes are the same at both heads, the failure comes from nondeterminism the PR already had (a race, an ordering
or clock-resolution assumption, a map iteration order) that CI happened to miss last time (#985: a Windows trace
test failed on a coarse-clock tie one round after passing on identical code).

  REGRESSED <check>: passed at <old>, fails at <head>; PR's production code unchanged since then
  REGRESSED <check>: passed at <old>, fails at <head>; production files changed since then: <files>

The PR's own changes are compared file by file (each head against its merge-base with base-ref, ignoring index
and hunk-offset lines), so a rebase onto main doesn't count as a change. Test files, corpus/, testdata/ and
Markdown aren't production code. Treat an "unchanged" hit as a finding of the PR until a repro shows otherwise:
rerun the test in a loop under the failing job's conditions (OS, -race, -count) and find the assumption it breaks.
Exit status 1 when anything is reported.
"""
import json
import re
import subprocess
import sys

NOT_PRODUCTION = re.compile(r"(_test\.go$|^corpus/|/testdata/|\.md$)")
FAILED = {"failure", "timed_out", "cancelled", "startup_failure"}


def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"gh api {path} failed: {(r.stderr or r.stdout).strip()[:200]}")
    return json.loads(r.stdout)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def runs(repo, sha):
    """{check name: [conclusions]} for every attempt on sha."""
    out, page = {}, 1
    while True:
        batch = gh(f"repos/{repo}/commits/{sha}/check-runs?filter=all&per_page=100&page={page}")["check_runs"]
        for c in batch:
            out.setdefault(c["name"], []).append(c.get("conclusion"))
        if len(batch) < 100:
            return out
        page += 1


def own_diff(base_ref, sha):
    """{file: normalised patch} of the PR's own changes at sha."""
    mb = git("merge-base", base_ref, sha).strip()
    files = git("diff", "--name-only", mb, sha).split()
    return {f: "\n".join(l for l in git("diff", mb, sha, "--", f).splitlines()
                         if not l.startswith(("index ", "@@"))) for f in files if not NOT_PRODUCTION.search(f)}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    n, old = sys.argv[1], sys.argv[2]
    base_ref = sys.argv[3] if len(sys.argv) > 3 else "origin/main"
    repo = sys.argv[4] if len(sys.argv) > 4 else "ballerina-nutcracker/ballerina"
    head = gh(f"repos/{repo}/pulls/{n}")["head"]["sha"]
    old = git("rev-parse", old).strip()
    if old == head:
        return 0
    before, now = runs(repo, old), runs(repo, head)
    regressed = sorted(name for name, results in now.items()
                       if FAILED & set(results) and "success" in before.get(name, []))
    if not regressed:
        return 0
    a, b = own_diff(base_ref, old), own_diff(base_ref, head)
    changed = sorted(f for f in a.keys() | b.keys() if a.get(f) != b.get(f))
    where = f"production files changed since then: {', '.join(changed)}" if changed else \
        "PR's production code unchanged since then"
    for name in regressed:
        print(f"REGRESSED {name}: passed at {old[:9]}, fails at {head[:9]}; {where}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

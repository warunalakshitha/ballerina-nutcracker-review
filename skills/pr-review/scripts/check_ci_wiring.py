#!/usr/bin/env python3
"""List test files a PR adds under .github/scripts/ that nothing runs.

Usage: $TOOLS/skills/pr-review/scripts/check_ci_wiring.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it inside the PR worktree.

Tests for CI scripts (.github/scripts/test_*) only run when a workflow, a Makefile target or a git hook names
them; on main each one is named in a workflow. A file the PR adds (or renames) whose name (with or without its
extension) appears in none of .github/workflows/, Makefile, *.mk or .githooks/ at HEAD is reported:

  NOT RUN   <file>

Each is a Nit: the test never runs in CI, so it can rot unnoticed. Ask for a workflow step or Makefile target
that runs it. Exit status 1 when anything is reported.
"""
import os
import subprocess
import sys

WHERE = [".github/workflows", "Makefile", "*.mk", ".githooks"]


def git(*args, check=True):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check)


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    base = git("merge-base", base_ref, "HEAD").stdout.strip()
    changed = git("diff", "--name-status", "--diff-filter=AR", f"{base}...HEAD", "--", ".github/scripts").stdout
    found = 0
    for line in changed.splitlines():
        path = line.split("\t")[-1]
        name = os.path.basename(path)
        if not name.startswith("test_"):
            continue
        stem = os.path.splitext(name)[0]
        if git("grep", "-q", "-F", stem, "HEAD", "--", *WHERE, check=False).returncode != 0:
            print(f"NOT RUN   {path}")
            found += 1
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

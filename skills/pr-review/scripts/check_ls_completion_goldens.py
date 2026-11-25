#!/usr/bin/env python3
"""List new stdlib packages that the LS completion goldens don't offer yet.

Usage: $TOOLS/skills/pr-review/scripts/check_ls_completion_goldens.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it inside the PR worktree.

Some LS completion goldens under ls/corpus/completion/testdata/ list every bundled module as an import completion
(`"label": "ballerina/<pkg>"`), so a PR that adds a package under lib/stdlibs/ballerina/ must add it to each of them,
or the LS corpus test fails once the package is bundled. CI shows that only after the tests run, and a rebase onto a
main that bundled another package breaks the same goldens again (stdlib-review.md, "Wire-up"):

  MISSING  <golden>: ballerina/<pkg>

A golden counts as listing bundled modules when, at HEAD, it offers at least three `ballerina/<pkg>` labels of
packages that already exist at the base. A golden whose own source already imports the package is skipped, since
completion doesn't offer an import that is already there. Exit status 1 when anything is reported.
"""
import re
import subprocess
import sys

STDLIBS = "lib/stdlibs/ballerina/"
GOLDENS = "ls/corpus/completion/testdata/"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def packages(ref):
    return {p.rsplit("/", 1)[-1] for p in git("ls-tree", "--name-only", ref, STDLIBS).split() if not p.endswith(".gitkeep")}


def main():
    base = git("merge-base", sys.argv[1] if len(sys.argv) > 1 else "origin/main", "HEAD").strip()
    old, new = packages(base), packages("HEAD")
    added = sorted(new - old)
    if not added:
        return 0
    problems = []
    for path in git("ls-tree", "--name-only", "HEAD", GOLDENS).split():
        if not path.endswith(".json"):
            continue
        text = git("show", f"HEAD:{path}")
        labels = set(re.findall(r'"label":\s*"ballerina/([\w.]+)"', text))
        if len(labels & old) < 3:
            continue
        for pkg in added:
            if pkg in labels or re.search(rf"import(\s|\\n)+ballerina/{re.escape(pkg)}\b", text):
                continue
            problems.append(f"MISSING  {path}: ballerina/{pkg}")
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

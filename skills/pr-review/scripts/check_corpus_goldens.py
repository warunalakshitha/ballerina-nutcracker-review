#!/usr/bin/env python3
"""List corpus fixtures a PR adds or renames without the golden files the corpus tests need.

Usage: $TOOLS/skills/pr-review/scripts/check_corpus_goldens.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it inside the PR worktree.

The goldens each fixture needs (as on main, where every fixture follows this except skip-listed ones):

  corpus/bal/<path>-v.bal, -p.bal   corpus/{ast,cfg,desugared,bir}/<path>.txt and corpus/integration/<path>.txtar
  corpus/bal/<path>-e.bal           corpus/integration/<path>.txtar
  corpus/lib/<path>.bal             corpus/integration/lib/<path>.txtar

A fixture named in test_util/skip.go is exempt (skipped tests have no goldens). Without its goldens the corpus
tests (TestIntegration, TestASTGeneration, TestCFGGeneration, TestDesugar, TestBIRGeneration) fail at the PR
head, which CI only shows hours later.

  MISSING   <fixture>: <golden>, ...   one line per fixture with every golden it lacks

Each MISSING fixture is an Important finding (the PR's own tests fail); report them together. Exit status 1 when
anything is reported.
"""
import os
import re
import subprocess
import sys

STAGES = ("ast", "cfg", "desugared", "bir")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def needed(path):
    m = re.fullmatch(r"corpus/bal/(.+-([vep]))\.bal", path)
    if m:
        rel, kind = m.group(1), m.group(2)
        out = [f"corpus/integration/{rel}.txtar"]
        if kind in "vp":
            out = [f"corpus/{s}/{rel}.txt" for s in STAGES] + out
        return out
    m = re.fullmatch(r"corpus/lib/(.+)\.bal", path)
    if m:
        return [f"corpus/integration/lib/{m.group(1)}.txtar"]
    return []


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    base = git("merge-base", base_ref, "HEAD").strip()
    changed = git("diff", "--name-status", "--diff-filter=AR", f"{base}...HEAD", "--", "corpus/bal", "corpus/lib")
    added = [line.split("\t")[-1] for line in changed.splitlines() if line.strip()]
    skip = open("test_util/skip.go").read() if os.path.exists("test_util/skip.go") else ""
    found = 0
    for path in sorted(added):
        if not path.endswith(".bal"):
            continue
        rel = re.sub(r"^corpus/(bal|lib)/", "", path)
        if rel in skip or path in skip:
            continue
        missing = [g for g in needed(path) if not os.path.exists(g)]
        if missing:
            found += 1
            print(f"MISSING   {path}: {', '.join(missing)}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

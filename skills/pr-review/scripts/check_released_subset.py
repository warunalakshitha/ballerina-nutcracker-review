#!/usr/bin/env python3
"""List corpus test cases a PR adds to a released language subset instead of the open one.

Usage: $TOOLS/skills/pr-review/scripts/check_released_subset.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it inside the PR worktree.

The open subset is the highest-numbered corpus/bal/subset<N>/; every lower one is released. New test cases belong in
the open subset, whether they arrive as a new file or as new cases appended to an existing released file:

  NEW       <file>                     a .bal file added (or renamed into) a released subset
  APPENDED  <file>: +<n> case(s)       an existing released-subset file that gains `// @output`, `// @error` or
                                       `// @panic` markers on lines of code it didn't have before, i.e. new cases
                                       (a line that only gains or changes its marker is re-marked, not new)

Each line is a Nit: move the cases to corpus/bal/subset<open>/<open>-<same area>/ with their goldens. Editing,
renaming or re-marking an existing case (marker count unchanged) is fine and is not reported. Exit status 1 when
anything is reported.
"""
import re
import subprocess
import sys

MARKER = re.compile(r"//\s*@(output|error|panic)\b")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def code(line):
    """The line without its marker comment and surrounding space: how a re-marked line is matched to its old self."""
    return line[1:].split("//", 1)[0].strip()


def new_cases(diff):
    """How many cases the change adds to an existing file: it must add code the old file didn't have, and end with
    more markers than it started with; the count is the smaller of the marker growth and the markers on new code.

    Not counted: a line that only gains or changes its marker (recovery now reports one more error there), a marker
    comment added without new code, and an error case turned into a valid one (marker count unchanged)."""
    lines = [d for d in diff.splitlines() if d[:1] in "+-" and d[:3] not in ("+++", "---")]
    old = [code(d) for d in lines if d[0] == "-"]
    on_new_code = 0
    new_code = False
    for d in lines:
        if d[0] != "+":
            continue
        c = code(d)
        if c in old:
            old.remove(c)
            continue
        if c:
            new_code = True
            on_new_code += bool(MARKER.search(d))
    growth = sum(1 for d in lines if d[0] == "+" and MARKER.search(d)) - sum(1 for d in lines if d[0] == "-" and MARKER.search(d))
    return min(growth, on_new_code) if new_code and growth > 0 else 0


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    base = git("merge-base", base_ref, "HEAD").strip()
    subsets = [int(n) for n in re.findall(r"^corpus/bal/subset(\d+)$", git("ls-tree", "-d", "--name-only", "HEAD", "corpus/bal/"), re.M)]
    if not subsets:
        print("check_released_subset: no corpus/bal/subset<N>/ directories at HEAD", file=sys.stderr)
        return 2
    open_n = max(subsets)
    released = re.compile(r"^corpus/bal/subset(\d+)/.+\.bal$")

    def is_released(path):
        m = released.match(path)
        return bool(m) and int(m.group(1)) < open_n

    found = 0
    for line in git("diff", "--name-status", "--diff-filter=AMR", f"{base}...HEAD", "--", "corpus/bal").splitlines():
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        if not is_released(path):
            continue
        if status == "A" or (status.startswith("R") and not is_released(parts[1])):
            print(f"NEW       {path}")
            found += 1
            continue
        new = new_cases(git("diff", "-U0", "-M", f"{base}...HEAD", "--", *parts[1:]))
        if new:
            print(f"APPENDED  {path}: +{new} case(s)")
            found += 1
    if found:
        print(f"open subset: corpus/bal/subset{open_n}/")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

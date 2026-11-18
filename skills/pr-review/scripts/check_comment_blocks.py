#!/usr/bin/env python3
"""List long or narrating comment blocks a PR adds to production code.

Usage: $TOOLS/skills/pr-review/scripts/check_comment_blocks.py [base-ref] [--min N]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it
  inside the PR worktree. --min sets the length threshold (default 6 added
  lines).

Scans `//` comment blocks in the .go and .bal files the PR touches, outside
tests (`_test.go`, `testdata/`, `corpus/`, a package's `tests/`). A block is
a run of consecutive comment lines in the head file; only the lines the PR
adds count toward its length, so a one-line edit to an old comment isn't
reported. License headers are skipped.

  LONG     the block adds at least --min lines
  PKGDOC   a LONG block that is the package doc (followed by `package`);
           allowed, but still check it for the narration below
  REFS     the block names jBallerina internals or claims parity
           (`execute.bal#startSuite`, `RunTestsTask#…`, "byte for byte",
           "ported from", "mirrors jballerina"); flagged at any length
  HISTORY  the block narrates review or PR history ("review", "previously",
           "moved from", "confirmed against", a P<N> plan); any length

Output is grouped by file, largest blocks first, with each block's head line
range and first comment line. Run it over the whole PR diff on every review,
re-reviews included: a block an earlier round skipped is still a finding.
Exit status 1 when anything is reported.
"""
import collections
import re
import subprocess
import sys

TEST_PARTS = ("_test.go", "/testdata/", "corpus/", "/tests/")
REFS_RE = re.compile(
    r"jballerina|\b\w+\.bal#\w+|\b[A-Z]\w+#\w+|byte[- ]for[- ]byte|ported (?:exactly )?from|\bmirror(?:s|ing)\b",
    re.I)
HISTORY_RE = re.compile(
    r"\breview(?:er|ed)?\b|\bpreviously\b|\bmoved from\b|\bconfirmed against\b|\bno longer\b|\bP\d+\b plan|\bused to\b",
    re.I)
LICENSE_RE = re.compile(r"Copyright \(c\)|licenses this file|www\.apache\.org/licenses")


def sh(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def added_lines(merge_base):
    """Map path -> set of head line numbers the PR adds, for non-test .go/.bal files."""
    diff = sh("git", "diff", "-U0", "--no-color", f"{merge_base}...HEAD", "--", ":(top)*.go", ":(top)*.bal")
    added, path, line = collections.defaultdict(set), None, 0
    for text in diff.split("\n"):
        if text.startswith("+++ "):
            path = text[6:] if text.startswith("+++ b/") else None
            if path and any(part in "/" + path for part in TEST_PARTS):
                path = None
            continue
        hunk = re.match(r"@@ -\S+ \+(\d+)", text)
        if hunk:
            line = int(hunk.group(1))
            continue
        if path and text.startswith("+"):
            added[path].add(line)
            line += 1
    return added


def blocks(path, added):
    """Yield (start, end, added_count, lines, next_code_line) for comment runs touching added lines."""
    lines = sh("git", "show", f"HEAD:{path}").split("\n")
    i = 0
    while i < len(lines):
        if not lines[i].lstrip().startswith("//"):
            i += 1
            continue
        start = i
        while i < len(lines) and lines[i].lstrip().startswith("//"):
            i += 1
        run = range(start + 1, i + 1)
        count = sum(1 for n in run if n in added)
        if count:
            following = next((t for t in lines[i:] if t.strip()), "")
            yield start + 1, i, count, lines[start:i], following


def main():
    args = sys.argv[1:]
    minimum = 6
    if "--min" in args:
        at = args.index("--min")
        minimum = int(args[at + 1])
        del args[at:at + 2]
    base = args[0] if args else "origin/main"
    try:
        merge_base = sh("git", "merge-base", base, "HEAD").strip()
    except subprocess.CalledProcessError:
        sys.exit(f"check_comment_blocks: no merge-base with {base}; run it inside the PR worktree")

    report = collections.defaultdict(list)
    for path, added in sorted(added_lines(merge_base).items()):
        for start, end, count, text, following in blocks(path, added):
            joined = " ".join(t.strip().lstrip("/").strip() for t in text)
            if LICENSE_RE.search(joined):
                continue
            tags = []
            if count >= minimum:
                tags.append("PKGDOC" if following.startswith("package ") else "LONG")
            if REFS_RE.search(joined):
                tags.append("REFS")
            if HISTORY_RE.search(joined):
                tags.append("HISTORY")
            if tags:
                first = text[0].strip().lstrip("/").strip()
                report[path].append((count, start, end, tags, first[:70]))

    if not report:
        return 0
    total = sum(len(v) for v in report.values())
    long_count = sum(1 for v in report.values() for b in v if "LONG" in b[3] or "PKGDOC" in b[3])
    print(f"{total} comment blocks in {len(report)} files ({long_count} of {minimum}+ added lines)")
    for path, hits in sorted(report.items(), key=lambda kv: -sum(b[0] for b in kv[1])):
        print(f"\n{path}")
        for count, start, end, tags, first in sorted(hits, key=lambda b: (-b[0], b[1])):
            print(f"  {start}-{end}  {count:>3} lines  {','.join(tags):<18} {first}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

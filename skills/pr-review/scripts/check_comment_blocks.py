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
           (`execute.bal#startSuite`, `RunTestsTask#…`, `CsvUtils.getSkipDataRows`,
           "byte for byte", "ported from", "mirrors jballerina"); flagged at
           any length. A `Class.method` name only counts when Class is not a
           Go type in the repo, a common JDK class (`String.valueOf` is fine)
           or attributed to a library ("JavaMail's InternetAddress.toString")
  HISTORY  the block narrates review or PR history ("review", "previously",
           "moved from", "confirmed against", a P<N> plan); any length
  TESTREF  production code points at a test or fixture (`corpus/`,
           `testdata/`, a `_test.go` file, or the name of a Go test function); any length. The test documents the
           behaviour itself, and the pointer goes stale when the test moves

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
    r"jballerina|\b\w+\.bal#\w+|byte[- ]for[- ]byte|ported (?:exactly )?from|\bmirror(?:s|ing)\b",
    re.I)
# A Java `Class#member` reference; case-sensitive so an issue reference such as
# `ballerina#1383` or `owner/repo#12` (lower-case name, numeric member) doesn't match.
CLASSREF_RE = re.compile(r"\b[A-Z]\w*#[A-Za-z_]\w*")
# A Java `Class.method` reference: a CamelCase class of two or more words and a lower-case method,
# e.g. `CsvUtils.getSkipDataRows`; not a file name such as `Foo.java`. Go types and common JDK classes
# are excluded in java_refs().
JAVA_METHOD_RE = re.compile(r"\b([A-Z][a-z0-9]+[A-Z]\w*)\.(?!(?:java|toml|bal|go|md|json|ya?ml|xml)\b)[a-z]\w*")
JDK_CLASSES = {"BigDecimal", "BigInteger", "NumberFormat", "DecimalFormat", "DecimalFormatSymbols",
               "StringBuilder", "DateTimeFormatter", "LocalDate", "LocalDateTime", "ZonedDateTime",
               "OffsetDateTime", "ZoneId", "ZoneOffset", "TimeUnit", "ConcurrentHashMap", "MessageDigest", "ByteBuffer", "CharBuffer", "InputStream",
               "OutputStream", "HashMap", "LinkedHashMap", "ArrayList", "CompletableFuture"}
HISTORY_RE = re.compile(
    r"\breview(?:er|ed)?\b|\bpreviously\b|\bmoved from\b|\bconfirmed against\b|\bno longer\b|\bP\d+\b plan|\bused to be\b|\bwe used to\b|\bpreviously used\b",
    re.I)
TESTREF_RE = re.compile(r"\bcorpus/|\btestdata/|\w+_test\.go\b")
TEST_NAME_RE = re.compile(r"\bTest[A-Z]\w*")
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


def test_function_names():
    """Names of Go test functions defined in _test.go files at HEAD."""
    out = subprocess.run(["git", "grep", "-h", "-o", "-E", r"^func Test[A-Z][A-Za-z0-9_]*", "HEAD", "--", ":(top)*_test.go"],
                         capture_output=True, text=True).stdout
    return {line.split()[-1] for line in out.split("\n") if line.strip()}


def go_type_names():
    """Names of exported Go types declared at HEAD, so a `Type.method` comment on Go code isn't a Java reference."""
    out = subprocess.run(["git", "grep", "-h", "-E", r"^(type[[:space:]]+|[[:space:]]+)[A-Z][A-Za-z0-9_]*[[:space:]]+(struct|interface)",
                          "HEAD", "--", ":(top)*.go"], capture_output=True, text=True).stdout
    out += subprocess.run(["git", "grep", "-h", "-E", r"^type[[:space:]]+[A-Z][A-Za-z0-9_]*", "HEAD", "--", ":(top)*.go"],
                          capture_output=True, text=True).stdout
    return {m.group(1) for m in re.finditer(r"^(?:HEAD:)?(?:type\s+|\s+)([A-Z]\w*)", out, re.M)}


def java_refs(text, go_types):
    """Class.method names of unattributed Java code. One introduced with a possessive ("JavaMail's
    InternetAddress.toString", "Netty's …") names the library the port matches; a jBallerina one is
    already caught by REFS_RE."""
    return [m.group(1) for m in JAVA_METHOD_RE.finditer(text)
            if m.group(1) not in go_types and m.group(1) not in JDK_CLASSES
            and not re.search(r"\w's\s+$", text[:m.start()])]


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

    test_funcs = test_function_names()
    go_types = go_type_names()
    report = collections.defaultdict(list)
    for path, added in sorted(added_lines(merge_base).items()):
        for start, end, count, text, following in blocks(path, added):
            joined = " ".join(t.strip().lstrip("/").strip() for t in text)
            if LICENSE_RE.search(joined):
                continue
            tags = []
            if count >= minimum:
                tags.append("PKGDOC" if following.startswith("package ") else "LONG")
            if REFS_RE.search(joined) or CLASSREF_RE.search(joined) or java_refs(joined, go_types):
                tags.append("REFS")
            if HISTORY_RE.search(joined):
                tags.append("HISTORY")
            if TESTREF_RE.search(joined) or any(n in test_funcs for n in TEST_NAME_RE.findall(joined)):
                tags.append("TESTREF")
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

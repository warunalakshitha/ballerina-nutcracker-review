#!/usr/bin/env python3
"""List files a PR adds whose license header differs from the commit hook's.

Usage: $TOOLS/skills/pr-review/scripts/check_license_headers.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it
  inside the PR worktree.

`.githooks/commit-msg` compares the first lines of every `.go` / `.bal` file a
commit adds with its `license_header` text, exactly. CI doesn't run the hook,
so a header variant (`WSO2 LLC licenses` without the period, wider wrapping,
one space before `See`) passes CI and is only rejected on a contributor's
machine. The header is read from the hook at the base, so this follows the
hook when it changes. The copyright year may be any year, since the hook uses
the year of the commit.

  MISMATCH   an added .go/.bal file whose header differs; the first differing
             line is shown
  GENERATOR  an added non-.go/.bal file (a generator or template) that embeds a
             license header but not the hook's text, so regenerated files will
             mismatch again

Files under cli/templates/ are exempt. Report all hits as one PR-level Nit
listing the files, not one finding per file. Exit status 1 when anything is
reported.
"""
import re
import subprocess
import sys

EXEMPT_PREFIXES = ("cli/templates/",)
YEAR_RE = re.compile(r"^// Copyright \(c\) (?:\d{4}|\$current_year), ", re.M)
# Generators and templates that write Go or Ballerina sources. Test transcripts
# (testdata, .json) embed sources as escaped strings and are skipped.
GENERATOR_SUFFIXES = (".py", ".sh", ".tmpl", ".tpl", ".gotmpl")


def sh(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def hook_header(base):
    hook = sh("git", "show", f"{base}:.githooks/commit-msg")
    match = re.search(r"^license_header=\$\(cat <<EOF\n(.*?)\nEOF\n\)", hook, re.S | re.M)
    if not match:
        sys.exit("check_license_headers: no license_header block in .githooks/commit-msg at " + base)
    return match.group(1).split("\n")


def normalize_year(line):
    return YEAR_RE.sub("// Copyright (c) YEAR, ", line)


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    try:
        merge_base = sh("git", "merge-base", base, "HEAD").strip()
    except subprocess.CalledProcessError:
        sys.exit(f"check_license_headers: no merge-base with {base}; run it inside the PR worktree")
    header = [normalize_year(line) for line in hook_header(merge_base)]
    added = sh("git", "diff", "--name-only", "--diff-filter=A", f"{merge_base}...HEAD").splitlines()
    mismatches, generators = [], []
    for path in added:
        if path.startswith(EXEMPT_PREFIXES):
            continue
        try:
            text = sh("git", "show", f"HEAD:{path}")
        except subprocess.CalledProcessError:
            continue
        if path.endswith((".go", ".bal")):
            lines = [normalize_year(line) for line in text.split("\n")[: len(header)]]
            if lines != header:
                index = next((i for i, (a, b) in enumerate(zip(lines, header)) if a != b), len(lines))
                got = lines[index] if index < len(lines) else "<missing>"
                mismatches.append((path, index + 1, got, header[index]))
        elif path.endswith(GENERATOR_SUFFIXES) and "/testdata/" not in path and "licenses this file to you" in text:
            body = "\n".join(header[1:])
            if body not in normalize_year(text):
                generators.append(path)
    for path, line, got, want in mismatches:
        print(f"MISMATCH   {path}:{line}\n    got:  {got}\n    want: {want}")
    for path in generators:
        print(f"GENERATOR  {path}: embeds a license header that is not the hook's text")
    if mismatches or generators:
        print(f"\n{len(mismatches)} mismatched file(s), {len(generators)} generator(s). Report as one PR-level Nit.")
        sys.exit(1)


if __name__ == "__main__":
    main()

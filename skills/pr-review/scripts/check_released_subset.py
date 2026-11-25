#!/usr/bin/env python3
# Copyright (c) 2026, WSO2 LLC. (http://www.wso2.com).
#
# WSO2 LLC. licenses this file to you under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
#
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Fails when a change adds tests to, or edits the docs of, a subset that has already been released.

Usage: check_released_subset.py [base-ref [head-ref]]
  base-ref defaults to origin/main and head-ref to HEAD; the change is base-ref...head-ref (from the merge-base).

A subset is released when it exists at the latest release tag (v<N>.<N>.<N>) reachable from base-ref: every
corpus/bal/subset<N>/ or doc/lang/subset<N>.md there is a released language subset, and every corpus/lib/subset<N>/
or doc/library/subset<N>.md a released library subset. The open subsets are the next numbers up. Nothing needs
updating at release time: tagging the release closes its subsets.

Reported, each as an error:

  NEW       <file>                 a .bal test added to (or renamed into) a released corpus/bal or corpus/lib subset
  APPENDED  <file>: +<n> case(s)   an existing released test that gains `// @output`, `// @error` or `// @panic`
                                   markers on new code, i.e. new cases (a line that only gains or changes its
                                   marker is re-marked, not new)
  DOC       <file>                 an edit to a released subset doc

Editing, re-marking or deleting existing cases, and regenerating goldens, is fine and is not reported. Exit status 1
when anything is reported, 2 when no release tag is found.
"""
import os
import re
import subprocess
import sys

MARKER = re.compile(r"//\s*@(output|error|panic)\b")
TAG = "v[0-9]*.[0-9]*.[0-9]*"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def code(line):
    """The diff line without its marker comment and surrounding space: how a re-marked line is matched to its old self."""
    return line[1:].split("//", 1)[0].strip()


def new_cases(diff):
    """How many cases the change adds to an existing file: it must add code the old file didn't have, and end with
    more markers than it started with; the count is the smaller of the marker growth and the markers on new code."""
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


def highest(tag, *patterns):
    """The highest subset number any of the path patterns (with one (\\d+) group) matches at tag, or 0."""
    paths = git("ls-tree", "-r", "-d", "--name-only", tag, "corpus", "doc").splitlines()
    paths += git("ls-tree", "-r", "--name-only", tag, "doc").splitlines()
    return max([int(m.group(1)) for p in paths for pat in patterns if (m := re.fullmatch(pat, p))], default=0)


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    head_ref = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    try:
        tag = git("describe", "--tags", "--abbrev=0", "--match", TAG, base_ref).strip()
    except subprocess.CalledProcessError:
        print(f"check_released_subset: no release tag reachable from {base_ref} (fetch tags first)", file=sys.stderr)
        return 2
    lang = highest(tag, r"corpus/bal/subset(\d+)", r"doc/lang/subset(\d+)\.md")
    lib = highest(tag, r"corpus/lib/subset(\d+)", r"doc/library/subset(\d+)\.md")
    print(f"{tag} released language subsets 1-{lang} and library subsets 1-{lib}; "
          f"open: corpus/bal/subset{lang + 1}/, corpus/lib/subset{lib + 1}/, "
          f"doc/lang/subset{lang + 1}.md, doc/library/subset{lib + 1}.md")

    tests = {r"corpus/bal/subset(\d+)/.+\.bal": lang, r"corpus/lib/subset(\d+)/.+\.bal": lib}
    docs = {r"doc/lang/subset(\d+)\.md": lang, r"doc/library/subset(\d+)\.md": lib}

    def released(path, kinds):
        return any((m := re.fullmatch(pat, path)) and int(m.group(1)) <= n for pat, n in kinds.items())

    annotate = os.environ.get("GITHUB_ACTIONS") == "true"
    found = []

    def report(kind, path, why, detail=""):
        found.append(path)
        print(f"{kind:<9} {path}{detail}")
        if annotate:
            print(f"::error file={path}::{why}")

    base = git("merge-base", base_ref, head_ref).strip()
    changes = git("diff", "--name-status", "-M", "--diff-filter=AMR", f"{base}...{head_ref}", "--", "corpus", "doc")
    for line in changes.splitlines():
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        if released(path, docs):
            report("DOC", path, f"{path} documents a subset released in {tag}; document the change in the open subset's doc")
        elif released(path, tests):
            if status == "A" or (status.startswith("R") and not released(parts[1], tests)):
                report("NEW", path, f"This test is in a subset released in {tag}; move it to the open subset")
                continue
            n = new_cases(git("diff", "-U0", "-M", f"{base}...{head_ref}", "--", *parts[1:]))
            if n:
                report("APPENDED", path, f"{n} new case(s) in a subset released in {tag}; move them to the open subset",
                       f": +{n} case(s)")
    if found:
        print(f"\n{len(found)} file(s) target subsets released in {tag}. Move new tests, with their goldens, to the "
              f"open subset (corpus/bal/subset{lang + 1}/{lang + 1}-<area>/ or corpus/lib/subset{lib + 1}/), and "
              f"document changes in doc/lang/subset{lang + 1}.md or doc/library/subset{lib + 1}.md.")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

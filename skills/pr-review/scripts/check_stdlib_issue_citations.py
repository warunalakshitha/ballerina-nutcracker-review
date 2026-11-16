#!/usr/bin/env python3
"""List ballerina-library issues a stdlib README links that no corpus test of that module cites.

Usage: $TOOLS/skills/pr-review/scripts/check_stdlib_issue_citations.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it inside the PR worktree.

For each package README under lib/stdlibs/ballerina/ that the PR adds or changes, every
`ballerina-platform/ballerina-library` issue linked under `Notable Behavioural Changes` marks a jBallerina bug the
port fixes. stdlib-review.md asks that the corpus `@output` showing the fixed behaviour cite that issue in a
comment. The corpus tests of a module are the `.bal` files under corpus/ that import it and the `_test.go` files
under corpus/ whose name contains the module name (e.g. corpus/extern/tcp_client_test.go).

  UNCITED   <README>: #<issue> (<bullet title>)   no corpus test importing the module mentions the issue

Read each hit: the fix may have no test at all (a different finding), or its test may cite the issue in a Go test
outside corpus/. Report the rest as one Nit listing the issues. Exit status 1 when anything is reported.
"""
import re
import subprocess
import sys

README = re.compile(r"lib/stdlibs/ballerina/([^/]+)/.*README\.md$")
ISSUE = re.compile(r"ballerina-library(?:#|/issues/)(\d+)")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def notable_bullets(text):
    m = re.search(r"^#+\s*Notable Behavioural Changes\s*$(.*?)(?=^#+\s|\Z)", text, re.M | re.S)
    return re.findall(r"^\s*[-*]\s+(.*)$", m.group(1), re.M) if m else []


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    base = git("merge-base", base_ref, "HEAD").strip()
    changed = git("diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD", "--", "lib/stdlibs/ballerina").split()
    found = 0
    for readme in sorted(f for f in changed if README.match(f)):
        module = README.match(readme).group(1)
        importers = git("grep", "-l", "-E", rf"^import ballerina/{re.escape(module)}( |;|\.)", "HEAD", "--", "corpus/*.bal")
        tests = [line.split(":", 1)[1] for line in importers.splitlines()]
        name = module.split(".")[-1]
        tests += [f for f in git("ls-tree", "-r", "--name-only", "HEAD", "corpus").split()
                  if f.endswith("_test.go") and name in f.rsplit("/", 1)[-1]]
        text = "\n".join(git("show", f"HEAD:{t}") for t in tests)
        for bullet in notable_bullets(git("show", f"HEAD:{readme}")):
            title = re.match(r"\*\*(.+?)\*\*", bullet)
            for issue in dict.fromkeys(ISSUE.findall(bullet)):
                if not re.search(rf"ballerina-library(?:#|/issues/){issue}\b", text):
                    found += 1
                    print(f"UNCITED   {readme}: #{issue} ({title.group(1) if title else bullet[:60]})")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

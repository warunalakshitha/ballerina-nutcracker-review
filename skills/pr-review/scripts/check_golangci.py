#!/usr/bin/env python3
"""Check a PR's golangci-lint config changes and the linter directives it adds.

Usage: $TOOLS/skills/pr-review/scripts/check_golangci.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it inside the PR worktree.

Modules use `<module>/.golangci.yml`, usually a symlink to a tier in `.golangci/` but sometimes a hand-made copy
(a regular file); `make lint-module/<m>` falls back to the root `.golangci.yml`. Reported, one line each:

  DUPLICATE  <config>: <linter>          a linter listed twice in an `enable`/`disable` list the PR changes
  NOT COPIED <module config>: <linters>   linters the PR adds to a tier that a hand-made copy of that tier lacks
                                          (the copy has every other linter of the tier, so it was meant to follow it)
  NOT ON     <file>:<line>: <directive>   a directive the PR adds whose linter the module's config doesn't enable,
                                          so it is never checked (`//sumtype:decl` needs gochecksumtype)

Each is a Nit; NOT ON is Important when the PR relies on that linter for a guarantee it claims. Exit status 1
when anything is reported.
"""
import os
import re
import subprocess
import sys

DIRECTIVES = {"//sumtype:decl": "gochecksumtype"}


def git(*args, check=True):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check).stdout


def lists(text):
    """{'enable': [...], 'disable': [...]} of the top-level `linters:` block, from indentation (no YAML module)."""
    out, in_linters, key, key_indent = {"enable": [], "disable": []}, False, None, 0
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            in_linters, key = line.startswith("linters:"), None
            continue
        if not in_linters:
            continue
        m = re.match(r"\s*(enable|disable):\s*$", line)
        if m:
            key, key_indent = m.group(1), indent
            continue
        if key and indent > key_indent and line.strip().startswith("- "):
            out[key].append(line.strip()[2:].strip().strip("'\""))
        elif indent <= key_indent:
            key = None
    return out


def show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True).stdout


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    base = git("merge-base", base_ref, "HEAD").strip()
    changed = git("diff", "--name-only", f"{base}...HEAD").split()
    found = []

    configs = [p for p in changed if re.search(r"(^|/)\.golangci(\.ya?ml$|/[^/]+\.ya?ml$)", p) and os.path.isfile(p)]
    for p in configs:
        for key, names in lists(open(p).read()).items():
            for n in sorted({n for n in names if names.count(n) > 1}):
                found.append(f"DUPLICATE  {p}: {n} (in {key})")

    copies = [p for p in git("ls-files", "*/.golangci.yml").split()
              if p.count("/") == 1 and os.path.isfile(p) and not os.path.islink(p)]
    for tier in (p for p in configs if p.startswith(".golangci/")):
        now, before = set(lists(open(tier).read())["enable"]), set(lists(show(base, tier))["enable"])
        added = now - before
        if not before:
            continue  # a new tier: no copy follows it yet
        for copy in copies:
            have = set(lists(open(copy).read())["enable"])
            missing = sorted(added - have)
            if missing and before <= have:
                found.append(f"NOT COPIED {copy}: {', '.join(missing)} (added to {tier})")

    for p in (p for p in changed if p.endswith(".go") and os.path.isfile(p)):
        new = git("diff", "-U0", f"{base}...HEAD", "--", p)
        line_no = 0
        for row in new.splitlines():
            m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", row)
            if m:
                line_no = int(m.group(1))
                continue
            if not row.startswith("+") or row.startswith("+++"):
                continue
            for directive, linter in DIRECTIVES.items():
                if directive in row:
                    module = p.split("/", 1)[0] if "/" in p else "."
                    cfg = f"{module}/.golangci.yml" if os.path.exists(f"{module}/.golangci.yml") else ".golangci.yml"
                    if linter not in lists(open(cfg).read())["enable"]:
                        found.append(f"NOT ON     {p}:{line_no}: {directive} ({cfg} doesn't enable {linter})")
            line_no += 1

    print("\n".join(found)) if found else None
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

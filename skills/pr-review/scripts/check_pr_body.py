#!/usr/bin/env python3
"""Check a PR's description against the repo's PR template (SKILL.md step 3.6).

Usage: $TOOLS/skills/pr-review/scripts/check_pr_body.py <PR number> [owner/repo]
  owner/repo defaults to ballerina-nutcracker/ballerina. REST only (works in cloud sessions).

The template is read from `.github/pull_request_template.md` on the PR's base branch, so this follows the
template when it changes. Reported, one line each:

  MISSING     a `## ` section of the template that the body doesn't have (e.g. a Goals/Design layout instead)
  EMPTY       a required section (Purpose, Approach) with nothing but the template's hint in it
  PLACEHOLDER the `Fixes #<Issue Number>` line left as is
  NO-ISSUE    no closing keyword (Fixes/Closes/Resolves #N) and no line saying why there's no issue
  CHECKBOX    a ticked checklist item the diff doesn't match: corpus tests ticked but no corpus file added or
              changed; the subset doc ticked but no doc/lang/subset<N>.md change

Report everything as one PR-level Nit listing the problems, not one finding each. Exit status 1 when anything is
reported, 0 when the body matches the template.
"""
import base64
import json
import re
import subprocess
import sys

REQUIRED = ("Purpose", "Approach")
CLOSING = re.compile(r"\b(fix(e[sd])?|close[sd]?|resolve[sd]?)\s+(#\d+|https://github\.com/\S+/issues/\d+)", re.I)
NO_ISSUE = re.compile(r"\bno (related |linked |tracking )?issue\b|\bwithout an issue\b|\bissue: none\b", re.I)


def api(path):
    out, page, items = None, 1, []
    while True:
        sep = "&" if "?" in path else "?"
        r = subprocess.run(["gh", "api", f"{path}{sep}per_page=100&page={page}"], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"gh api {path} failed: {(r.stderr or r.stdout).strip()[:200]}")
        out = json.loads(r.stdout)
        if not isinstance(out, list):
            return out
        items += out
        if len(out) < 100:
            return items
        page += 1


def sections(text):
    """{heading: body} for `## heading` blocks, with HTML comments removed."""
    text = re.sub(r"<!--.*?-->", "", text or "", flags=re.S)
    parts = re.split(r"^##\s+(.+?)\s*$", text, flags=re.M)
    return {h.strip(): b for h, b in zip(parts[1::2], parts[2::2])}


def meaningful(body, hint):
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    return [l for l in lines if l != hint and l != "Fixes #<Issue Number>"]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    n, repo = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "ballerina-nutcracker/ballerina"
    pr = api(f"repos/{repo}/pulls/{n}")
    body = pr.get("body") or ""
    tpl = api(f"repos/{repo}/contents/.github/pull_request_template.md?ref={pr['base']['repo']['default_branch']}")
    template = base64.b64decode(tpl["content"]).decode()
    want, got = sections(template), sections(body)
    got_lower = {h.lower(): b for h, b in got.items()}
    problems = []
    for heading, tbody in want.items():
        if heading.lower() not in got_lower:
            problems.append(f"MISSING     section '## {heading}'")
        elif heading in REQUIRED:
            hint = next((l.strip() for l in tbody.splitlines() if l.strip().startswith(">")), None)
            if not meaningful(got_lower[heading.lower()], hint):
                problems.append(f"EMPTY       section '## {heading}' has only the template hint")
    if "Fixes #<Issue Number>" in body:
        problems.append("PLACEHOLDER 'Fixes #<Issue Number>' left unchanged")
    elif not CLOSING.search(body) and not NO_ISSUE.search(body):
        problems.append("NO-ISSUE    no 'Fixes #N' (or Closes/Resolves) and no line saying why there's no issue")
    ticked = [l for l in body.splitlines() if re.match(r"\s*[-*]\s*\[[xX]\]", l)]
    if ticked:
        files = [f["filename"] for f in api(f"repos/{repo}/pulls/{n}/files")]
        if any("corpus test" in l.lower() for l in ticked) and not any(f.startswith("corpus/") for f in files):
            problems.append("CHECKBOX    corpus tests ticked, but the PR adds or changes no file under corpus/")
        if any("subset" in l.lower() for l in ticked) and not any(re.match(r"doc/lang/subset\d+\.md$", f) for f in files):
            problems.append("CHECKBOX    subset doc ticked, but the PR doesn't change doc/lang/subset<N>.md")
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Check a PR's description against the repo's PR template (SKILL.md step 3.6).

Usage: $TOOLS/skills/pr-review/scripts/check_pr_body.py <PR number> [owner/repo]
  owner/repo defaults to ballerina-nutcracker/ballerina. REST only (works in cloud sessions).

The template is read from `.github/pull_request_template.md` on the PR's base branch, so this follows the
template when it changes. Reported, one line each:

  MISSING     a `## ` section of the template that the body doesn't have (e.g. a Goals/Design layout instead)
  EMPTY       a required section (Purpose, Approach) with nothing but the template's hint in it
  PLACEHOLDER the `Fixes #<Issue Number>` line left as is
  NO-ISSUE    no closing keyword (Fixes/Closes/Resolves #N), no non-closing link (Part of/Related to/Refs #N) and no
              line saying why there's no issue
  CHECKBOX    a ticked checklist item the diff doesn't match: corpus tests ticked but no corpus file added or
              changed; the subset doc ticked but no doc/lang/subset<N>.md or doc/library/subset<N>.md change
  CLOSED      a closing keyword (Fixes/Closes/Resolves, with or without a colon) names an issue of this repo that
              is already closed, so the PR fixes nothing it claims to
  PATH        a backticked path in the body that the PR doesn't add or change (a stale description after a
              commit was dropped, or a file the PR renamed away); read each hit, since a body may also point at
              an unchanged file on purpose

Report everything as one PR-level Nit listing the problems, not one finding each. Exit status 1 when anything is
reported, 0 when the body matches the template.
"""
import base64
import json
import re
import subprocess
import sys

REQUIRED = ("Purpose", "Approach")
CLOSING = re.compile(r"\b(fix(e[sd])?|close[sd]?|resolve[sd]?):?\s+(#\d+|https://github\.com/\S+/issues/\d+)", re.I)
# A backticked token that may be a repo path; kept when it ends in a file extension, or has a slash and starts at
# a top-level directory or a corpus subset (so module names like `ballerina/tcp` are skipped).
PATH_TOKEN = re.compile(r"`([A-Za-z0-9_.{},*…/-]+)`")
FILE_EXT = re.compile(r"\.(go|bal|md|txt|txtar|toml|ya?ml|py|sh|json|mod)$")
NO_ISSUE = re.compile(r"\bno (related |linked |tracking )?issue\b|\bwithout an issue\b|\bissue: none\b"
                      r"|\b(part of|related to|relates to|refs?|see|follow-up (to|of))\s+(#\d+|https://github\.com/\S+/issues/\d+)", re.I)


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
        problems.append("NO-ISSUE    no 'Fixes #N' (or Closes/Resolves), no 'Part of #N' and no line saying why there's no issue")
    for m in CLOSING.finditer(body):
        ref = m.group(3)
        num = re.search(r"(\d+)$", ref).group(1)
        if ref.startswith("http") and f"github.com/{repo}/issues/" not in ref:
            continue
        issue = api(f"repos/{repo}/issues/{num}")
        if issue.get("state") == "closed":
            problems.append(f"CLOSED      '{m.group(0)}' names #{num}, which is already closed ({issue.get('state_reason')})")
    pr_files = api(f"repos/{repo}/pulls/{n}/files")
    files = [f["filename"] for f in pr_files if f["status"] != "removed"]
    gone = {f["filename"]: "deletes it" for f in pr_files if f["status"] == "removed"}
    gone.update({f["previous_filename"]: f"renames it to {f['filename']}" for f in pr_files if f.get("previous_filename")})
    top = {e["name"] for e in api(f"repos/{repo}/contents?ref={pr['head']['sha']}") if e["type"] == "dir"}
    for token in dict.fromkeys(PATH_TOKEN.findall(body)):
        first = token.split("/")[0]
        if not FILE_EXT.search(token) and ("/" not in token or first not in top and not re.match(r"subset\d+$", first)):
            continue
        prefix = re.split(r"[{*…]|\.\.\.", token)[0]
        if prefix != token:
            hit = lambda f: prefix in f
        else:
            path = token.rstrip("/")
            hit = lambda f: f == path or f.endswith("/" + path) or f.startswith(path + "/") or f"/{path}/" in f
        if any(hit(f) for f in files):
            continue
        what = next((f"; the PR {v}" for k, v in gone.items() if hit(k)), "")
        problems.append(f"PATH        `{token}` is named in the body but the PR doesn't add or change it{what}")
    ticked = [l for l in body.splitlines() if re.match(r"\s*[-*]\s*\[[xX]\]", l)]
    if ticked:
        if any("corpus test" in l.lower() for l in ticked) and not any(f.startswith("corpus/") for f in files):
            problems.append("CHECKBOX    corpus tests ticked, but the PR adds or changes no file under corpus/")
        if any("subset" in l.lower() for l in ticked) and not any(re.match(r"doc/(lang|library)/subset\d+\.md$", f) for f in files):
            problems.append("CHECKBOX    subset doc ticked, but the PR doesn't change doc/lang/subset<N>.md or doc/library/subset<N>.md")
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

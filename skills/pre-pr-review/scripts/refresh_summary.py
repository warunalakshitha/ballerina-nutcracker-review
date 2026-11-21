#!/usr/bin/env python3
"""Rebuild a PR's findings.json from its posted review, for a summary-only refresh in the current layout.

Usage: refresh_summary.py <PR number> [<out findings.json>]   (default: stdout)

For a PR scan_prs.py lists as REFORMAT: our summary reviewed the current head but was written in an older layout
(no fmt=2 in its marker). No code is reviewed. The output is a findings.json with "summary_only": true, which
post_review.py turns into an in-place edit of the summary; inline comments are left exactly as they are.
- Inline findings whose thread is still open are listed as `keep_posted` (counted, not touched).
- PR-level findings come from the summary. A PR-level Nit with no file is a commit, PR title or PR body item
  (agent-instructions.md), so it becomes a 📝 Commit/PR finding; other PR-level findings keep their severity.
- Every answered finding with a thread gets a linked For-a-human line (the author's last reply, or our comment
  when the thread was resolved without one), unless the thread points to an issue that tracks it. An earlier
  unlinked line about the same finding keeps its text and gains the link.
- The marker's skill= and tools= are kept, so a later sweep still sees the code as reviewed with older skills.
Exits 1 with a message when the PR can't be refreshed this way (no summary, moved head, counts that don't add up).
REST only (works in Claude Code cloud sessions).
"""
import json
import re
import sys

from ghrest import ME, REPO, api, review_threads

FINDING_RE = re.compile(r"<!-- pre-pr-review:finding id=(\S+) -->")
MARKER_RE = re.compile(r"<!-- pre-pr-review:summary pr=\d+ diff=(\w+) skill=(\w+)(?: tools=(\w+))?(?: fmt=(\d+))? -->")
ANSWERED_RE = re.compile(r"<!-- pre-pr-review:answered ids=(\S+) -->")
BADGE = {"🔴": "important", "🟡": "verify", "🔵": "nit", "📝": "commit"}
PR_ITEM_RE = re.compile(r"^- (🔴|🟡|🔵|📝) \*\*[\w/]+\*\* · (.*?)\.(?: \*\*Fix:\*\* (.*?))?(?: · `([^`]+):(\d+)`)? "
                        r"<!-- pre-pr-review:finding id=(\S+) -->$")
INLINE_HEAD_RE = re.compile(r"🤖 (🔴|🟡|🔵|📝) \*\*[\w/]+\*\* · (.+?) — \*\*(.+?)\*\*")
TRACKED_RE = re.compile(r"(?i)(issues/\d+|\b(tracked|tracking|filed|follow[- ]?up|issue)\b[^\n]{0,40}#\d+|#\d+[^\n]{0,20}\btracks?\b)")
LINK_RE = re.compile(r"https://github\.com/[^\s)]+/pull/\d+#(discussion_r|issuecomment-)\d+")


def fail(msg):
    sys.exit(f"refresh_summary: {msg}")


def latest_summary(n):
    ours = [c for c in api(f"repos/{REPO}/issues/{n}/comments?per_page=100", paginate=True)
            if c["user"]["login"] == ME and c["body"].startswith("<!-- pre-pr-review:summary")]
    return max(ours, key=lambda c: c["updated_at"])["body"] if ours else None


def parse_summary(body):
    """(status tail, stack, checked, items, fixed_later, human lines, PR-level findings) from the summary text."""
    lines = body.splitlines()
    status = next((l for l in lines if "reviewed `" in l), "")
    tail = status.split("`.", 1)[1].strip() if "`." in status else ""
    stack = next((l for l in lines if l.startswith("Stack: ")), "")
    checked = next((l for l in lines if l.startswith("Checked: ")), "")
    checked = [c.replace("✔", "").strip() for c in checked[len("Checked: "):].split(" · ")] if checked else []
    items, fixed_later, human, findings = [], [], [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.startswith("- "):
            continue
        if line.startswith("- 👤 **For a human** · "):
            human.append(line[len("- 👤 **For a human** · "):].strip())
        elif m := re.match(r"- ✅ Fixed later in the stack by #(\d+): (.*)$", line):
            fixed_later.append({"pr": int(m.group(1)), "text": m.group(2)})
        elif m := PR_ITEM_RE.match(line):
            details = []
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                if lines[i].startswith("- "):
                    break
                details.append(lines[i][2:] if lines[i].startswith("  ") else "")
                i += 1
            text = "\n".join(details)
            body_text = re.sub(r"^\s*<details><summary>Details</summary>\s*", "", text)
            body_text = re.sub(r"\s*</details>\s*$", "", body_text).strip()
            sev = BADGE[m.group(1)]
            f = {"id": m.group(6), "severity": sev, "kind": "PR", "anchor": "pr", "title": m.group(2),
                 "body": body_text, "code": None, "outputs": None, "suggestion": None}
            if m.group(3):
                f["fix"] = m.group(3).strip()
            if m.group(4):
                f.update(path=m.group(4), line=int(m.group(5)))
            elif sev == "nit":
                f["severity"] = "commit"  # a PR-level Nit with no file is a commit, PR title or body item
            findings.append(f)
        else:
            items.append(line[2:])
    return tail, stack, checked, items, fixed_later, human, findings


def human_text(c):
    text = re.sub(r"^\s*\[AI RESPONSE\]\s*", "", c["body"]).strip()
    text = " ".join(text.split())
    first = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
    return first if len(first) <= 120 else first[:117] + "…"


def answered_lines(n, answered, old_human):
    """Linked For-a-human lines for answered findings that have a thread of ours."""
    comments = api(f"repos/{REPO}/pulls/{n}/comments?per_page=100", paginate=True)
    roots = {FINDING_RE.search(c["body"]).group(1): c for c in comments
             if not c.get("in_reply_to_id") and c["user"]["login"] == ME and FINDING_RE.search(c["body"])}
    replies = {}
    for c in sorted(comments, key=lambda c: c["created_at"]):
        if c.get("in_reply_to_id"):
            replies.setdefault(c["in_reply_to_id"], []).append(c)
    out, used = [], set()
    for fid in answered:
        root = roots.get(fid)
        if not root:
            print(f"refresh_summary: answered {fid} has no thread of ours (PR-level); no human line", file=sys.stderr)
            continue
        thread = replies.get(root["id"], [])
        if any(TRACKED_RE.search(c["body"]) for c in thread if c["user"].get("type") == "User"):
            continue  # deferred to an issue: settled, nothing for a human to check
        answer = next((c for c in reversed(thread) if c["user"].get("type") == "User" and c["user"]["login"] != ME), None)
        url = (answer or root)["html_url"]
        head = INLINE_HEAD_RE.search(root["body"])
        title = head.group(3) if head else fid
        same_link = next((h for h in old_human if url in h), None)
        if same_link:
            used.add(same_link)
            out.append(same_link)  # already linked to this answer: keep the reviewer's words
            continue
        # Earlier unlinked lines start with the finding's id or its title.
        old = next((h for h in old_human if not LINK_RE.search(h) and
                    (h.startswith((fid + ":", f"`{fid}`")) or h.startswith(title))), None)
        if old:
            used.add(old)
            text = old.rstrip(" ·")
        else:
            text = f"{title}: " + (f"author: “{human_text(answer)}”" if answer else "resolved by the author without a reply")
        out.append(f"{text} · [answer]({url})")
    return out, used


def main():
    if len(sys.argv) not in (2, 3):
        fail("usage: refresh_summary.py <PR number> [<out findings.json>]")
    n = int(sys.argv[1])
    pr = api(f"repos/{REPO}/pulls/{n}")
    head = pr["head"]["sha"]
    body = latest_summary(n)
    if not body:
        fail(f"#{n} has no summary of ours")
    marker = MARKER_RE.search(body)
    if not marker:
        fail(f"#{n}: summary marker not recognised")
    reviewed = re.findall(r"reviewed `([0-9a-f]{7,40})", body)
    if not reviewed or not head.startswith(reviewed[-1]):
        fail(f"#{n}: head moved since the summary; it needs a re-review, not a refresh")
    diff, skill, tools, _ = marker.groups()
    tail, stack_line, checked, items, fixed_later, old_human, pr_findings = parse_summary(body)
    answered = ANSWERED_RE.search(body)
    answered = answered.group(1).split(",") if answered else []

    # Inline findings still open: our finding threads that aren't resolved.
    open_roots = {cid for cid, resolved in review_threads(n) if not resolved}
    kept = []
    for c in api(f"repos/{REPO}/pulls/{n}/comments?per_page=100", paginate=True):
        m = FINDING_RE.search(c["body"])
        if c.get("in_reply_to_id") or c["user"]["login"] != ME or not m or c["id"] not in open_roots:
            continue
        h = INLINE_HEAD_RE.search(c["body"])
        if not h:
            fail(f"#{n}: can't read the severity of inline finding {m.group(1)}")
        kept.append({"id": m.group(1), "severity": BADGE[h.group(1)], "kind": h.group(2), "title": h.group(3),
                     "body": "", "path": c["path"], "line": c.get("line"), "keep_posted": True})

    status = next((l for l in body.splitlines() if "reviewed `" in l), "")
    counted = sum(int(k) for k in re.findall(r"\*\*(\d+) [A-Za-z/]+\*\*", status))
    if counted != len(kept) + len(pr_findings):
        fail(f"#{n}: summary counts {counted} findings but {len(kept)} open inline + {len(pr_findings)} PR-level "
             "were found; re-review it instead")

    human, used = answered_lines(n, answered, old_human)
    # Earlier lines not about an answered thread: linked ones carry over; unlinked ones stay for the reviewer.
    human += [h for h in old_human if h not in used and h not in human]

    data = {"repo": REPO, "pr": n, "head_sha": head, "reviewed_diff": diff, "skill_version": skill,
            "skill_commit": tools or "none", "summary_only": True, "answered": answered, "human": human,
            "summary": {"line": tail, "checked": checked, "items": items}, "findings": pr_findings + kept}
    if stack_line:
        prs = [int(x) for x in re.findall(r"#(\d+)", stack_line.split(" · ")[0])]
        tip = re.search(r"at `([0-9a-f]+)`", stack_line)
        data["stack"] = {"prs": prs, "heads": {str(p): (head if p == n else api(f"repos/{REPO}/pulls/{p}")["head"]["sha"])
                                               for p in prs},
                         "tip_sha": tip.group(1) if tip else head, "fixed_later": fixed_later}
    text = json.dumps(data, indent=1, ensure_ascii=False)
    if len(sys.argv) == 3:
        open(sys.argv[2], "w").write(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()

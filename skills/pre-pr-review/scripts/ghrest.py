"""REST-only GitHub helpers for the review scripts.

Claude Code cloud sessions block GraphQL (and so `gh pr list/view/checks --json`), so everything
here uses `gh api` REST routes, plus the `ccr/review_threads` route those sessions provide for
review threads. Every call is retried; a call that still fails raises GhError.
"""
import json
import os
import subprocess
import time

REPO = os.environ.get("REVIEW_REPO", "ballerina-nutcracker/ballerina")
ME = os.environ.get("REVIEWER", "warunalakshitha")
DONT_MERGE = ("merge", "dnm", "hold", "wip")


class GhError(RuntimeError):
    pass


def _get(path, tries):
    err = ""
    for i in range(tries):
        try:
            r = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            err = f"timed out: gh api {path}"
            time.sleep(3 * (i + 1))
            continue
        if r.returncode == 0:
            return json.loads(r.stdout) if r.stdout.strip() else None
        err = (r.stderr or r.stdout).strip()
        if i + 1 < tries:
            time.sleep(3 * (i + 1))
    raise GhError(err[:300])


def api(path, paginate=False, tries=4):
    """GET a REST path (relative to api.github.com). With paginate, returns the concatenated list.

    Pages are requested explicitly with `page=N`: `gh api --paginate` follows GitHub's Link
    headers, which use numeric `repositories/{id}` URLs that the cloud proxy rejects."""
    if not paginate:
        return _get(path, tries)
    items, page = [], 1
    sep = "&" if "?" in path else "?"
    if "per_page=" not in path:
        path += f"{sep}per_page=100"
        sep = "&"
    while True:
        batch = _get(f"{path}{sep}page={page}", tries) or []
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def open_prs():
    return api(f"repos/{REPO}/pulls?state=open&per_page=100", paginate=True)


def skipped_by_label(pr):
    return any(any(k in label["name"].lower() for k in DONT_MERGE) for label in pr.get("labels", []))


def pr_detail(n):
    """Single-PR REST payload; `mergeable` is computed lazily by GitHub, so retry while it's null."""
    for _ in range(4):
        d = api(f"repos/{REPO}/pulls/{n}")
        if d.get("mergeable") is not None:
            return d
        time.sleep(3)
    return d


def mergeability(detail):
    m = detail.get("mergeable")
    return "MERGEABLE" if m is True else "CONFLICTING" if m is False else "UNKNOWN"


def review_decision(n, head):
    """APPROVED / CHANGES_REQUESTED / REVIEW_REQUIRED from each reviewer's latest decisive review.
    An approval counts only if it was given on `head`: after a push GitHub asks for review again,
    so an approval of an older commit means the PR still needs review (#701, #1422, #1465)."""
    latest = {}
    for r in api(f"repos/{REPO}/pulls/{n}/reviews?per_page=100", paginate=True):
        if r["state"] == "APPROVED" and r.get("commit_id") != head:
            latest[r["user"]["login"]] = "STALE"
        elif r["state"] in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
            latest[r["user"]["login"]] = r["state"]
    states = set(latest.values())
    if "CHANGES_REQUESTED" in states:
        return "CHANGES_REQUESTED"
    return "APPROVED" if "APPROVED" in states else "REVIEW_REQUIRED"


def summaries(n):
    """Bodies of our "PR review summary" comments, least recently updated first, so [-1] is the one
    post_review.py edits (it updates the most recently updated summary)."""
    ours = [c for c in api(f"repos/{REPO}/issues/{n}/comments?per_page=100", paginate=True)
            if c["user"]["login"] == ME and "PR review summary" in c["body"]]
    return [c["body"] for c in sorted(ours, key=lambda c: c["updated_at"])]


def graphql(q, args=()):
    """Parsed `gh api graphql` output, or None if it fails after retries (cloud sessions may lack GraphQL)."""
    for i in range(4):
        try:
            r = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}", *args],
                               capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            time.sleep(3 * (i + 1))
            continue
        if r.returncode == 0:
            return json.loads(r.stdout)
        time.sleep(3 * (i + 1))
    return None


def merge_queue(branch="main"):
    """{PR number: (position, state)} for the branch's merge queue, or None if it can't be read."""
    owner, name = REPO.split("/")
    out = graphql('{repository(owner:"%s",name:"%s"){mergeQueue(branch:"%s"){entries(first:100)'
                  '{nodes{position state pullRequest{number}}}}}}' % (owner, name, branch))
    if out is None:
        return None
    mq = (out.get("data") or {}).get("repository", {}).get("mergeQueue") or {}
    return {e["pullRequest"]["number"]: (e["position"], e["state"].replace("_", " ").lower())
            for e in (mq.get("entries") or {}).get("nodes", []) if e.get("pullRequest")}


def review_threads(n):
    """[(first comment id, resolved)] per review thread. Cloud sessions serve the `ccr` route;
    elsewhere (a local gh login) that route doesn't exist, so fall back to GraphQL."""
    try:
        return [(t["comment_ids"][0], bool(t.get("resolved")))
                for t in api(f"repos/{REPO}/pulls/{n}/ccr/review_threads", tries=1) or [] if t.get("comment_ids")]
    except GhError:
        owner, name = REPO.split("/")
        q = ('query($n:Int!,$after:String){repository(owner:"%s",name:"%s"){pullRequest(number:$n)'
             '{reviewThreads(first:100,after:$after){pageInfo{hasNextPage endCursor}'
             'nodes{isResolved comments(first:1){nodes{databaseId}}}}}}}' % (owner, name))
        threads, after = [], None
        while True:
            args = ["-F", f"n={n}"] + (["-f", f"after={after}"] if after else [])
            out = graphql(q, args)
            if out is None:
                raise GhError(f"review threads for #{n}: neither ccr route nor GraphQL worked")
            rt = out["data"]["repository"]["pullRequest"]["reviewThreads"]
            threads += [(t["comments"]["nodes"][0]["databaseId"], t["isResolved"])
                        for t in rt["nodes"] if t["comments"]["nodes"]]
            if not rt["pageInfo"]["hasNextPage"]:
                return threads
            after = rt["pageInfo"]["endCursor"]


def unresolved_finding_threads(n):
    """Number of our finding threads (first comment ours with a finding marker) that aren't resolved."""
    comments = {c["id"]: c for c in api(f"repos/{REPO}/pulls/{n}/comments?per_page=100", paginate=True)}
    count = 0
    for first_id, resolved in review_threads(n):
        first = comments.get(first_id)
        if first and not resolved and first["user"]["login"] == ME and "pre-pr-review:finding" in first["body"]:
            count += 1
    return count


def ci_state(sha):
    """(failed check names, pending count) for a commit, from check runs and legacy statuses."""
    runs = []
    page = 1
    while True:
        d = api(f"repos/{REPO}/commits/{sha}/check-runs?per_page=100&page={page}")
        runs += d.get("check_runs", [])
        if len(runs) >= d.get("total_count", 0) or not d.get("check_runs"):
            break
        page += 1
    # A re-run or a newer workflow run (e.g. after a title edit) adds runs and leaves the old ones, often
    # cancelled, on the commit; only the latest run of each check counts. Run ids grow over time.
    latest = {}
    for c in runs:
        key = ((c.get("app") or {}).get("id"), c["name"])
        if key not in latest or c["id"] > latest[key]["id"]:
            latest[key] = c
    failed, pending = [], 0
    for c in latest.values():
        if c["status"] != "completed":
            pending += 1
        elif c["conclusion"] not in ("success", "skipped", "neutral"):
            failed.append(c["name"])
    statuses = (api(f"repos/{REPO}/commits/{sha}/status?per_page=100") or {}).get("statuses", [])
    if not runs and not statuses:
        return [], 1  # no CI has started yet (just pushed, or a fork PR awaiting workflow approval)
    for s in statuses:
        if s["state"] == "pending":
            pending += 1
        elif s["state"] != "success":
            failed.append(s["context"])
    return failed, pending

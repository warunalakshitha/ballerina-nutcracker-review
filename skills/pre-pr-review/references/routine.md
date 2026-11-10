# Scheduled review round (cloud routine)

You coordinate one review round for ballerina-nutcracker/ballerina, unattended, in a Claude Code cloud session. Nothing from earlier runs survives except what is on GitHub.

## 0. Setup
1. Sources are checked out side by side:
   - `REPO=/home/user/ballerina`: ballerina-nutcracker/ballerina (`origin`). Its `main` carries the current AGENTS.md, docs and the repo's own `.agents/skills`; always review against `origin/main`.
   - `TOOLS=/home/user/ballerina-nutcracker-review`: this tooling (review skill `skills/pr-review`, posting/agent rules `skills/pre-pr-review`).
   Confirm both paths exist (`ls /home/user`); adjust if the checkout dirs differ. `SP=/tmp/review-sp`; `mkdir -p $SP/review-out`. `UPSTREAM=origin`. Agents get `$REPO`, `$TOOLS`, `$UPSTREAM` and `$SP` in their prompts.
2. `git -C $REPO fetch origin main` (and PR heads as needed: `git -C $REPO fetch origin +refs/pull/<N>/head:refs/review/pr<N>`).
3. GitHub access: GraphQL is blocked in cloud sessions. Use `gh api` REST only (`gh pr list/view/checks --json` fail). Review threads: `GET repos/<repo>/pulls/<n>/ccr/review_threads` (list of `{resolved, outdated, path, line, comment_ids}`); resolve with `POST repos/<repo>/pulls/<n>/ccr/comments/<comment_ids[0]>/resolve`. The scripts already do this. `gh api user` shows the identity comments post as; if a write fails with 403, run report-only and say so first.
4. Tooling: Go comes from the repo's toolchain line (auto-downloaded). jBallerina `bal` is not installed: agents skip parity runs and write "jBallerina not available" instead of claiming parity.

## 1. Scan
`cd $TOOLS/skills/pre-pr-review/scripts && python3 scan_prs.py` lists PRs needing review: `NEW` (no summary of ours) or `MOVED` (head differs from the commit our last summary reviewed). It skips drafts, approved PRs and don't-merge/dnm/hold/wip labels. `ERR`: retry once, then list as "not checked". A PR whose head equals the commit in our latest summary is already reviewed: skip it.

## 2. Review
- Drop PRs that conflict with `origin/main` (`git -C $REPO merge-tree --write-tree origin/main refs/review/pr<N>`): no review, no comment; list as skipped.
- Stacks (base branch isn't `main`): `python3 $TOOLS/skills/pre-pr-review/scripts/stack.py <tip> --json` run inside `$REPO`; review the stack as one unit at the highest non-conflicting PR.
- MOVED PRs: interdiff of the PR's own changes (old reviewed head vs new head, each against its merge-base). Only merges of main, no PR-file change: refresh the summary (rebuild findings.json from GitHub with the new `head_sha`/`reviewed_diff`, post) instead of re-reviewing.
- One review subagent per PR (stack = one agent), at most 3 at a time, smallest PRs first. Each prompt: follow `$TOOLS/skills/pre-pr-review/references/agent-instructions.md` exactly; gives `$REPO`, `$TOOLS`, `$SP`, the PR number, the last reviewed sha (MOVED) and PR-specific focus. Rules belong in agent-instructions.md, never only in a prompt.
- No local findings files exist: agents rebuild every still-open finding of ours from GitHub before re-reviewing.

## 3. Post
Per finished review: dry-run `python3 $TOOLS/skills/pre-pr-review/scripts/post_review.py $SP/review-out/<N>/findings.json`; fix brevity warnings (shorten; complete repro programs; avoid "e.g." which counts as a sentence break); check overlap warnings against the other reviewer's comment (drop only true duplicates); then `--post`. If the head moved since the review, re-queue instead of posting.

## 4. Bugs found on main
`$TOOLS/skills/pre-pr-review/references/retrospective.md`, "Bugs found on main": one repro on current main, duplicate search (`gh api 'search/issues?q=repo:ballerina-nutcracker/ballerina+<words>'`), then file via `gh api repos/ballerina-nutcracker/ballerina/issues -f title=... -f body=... -f 'labels[]=triage' -f 'labels[]=Type/Bug'`. No bug hunting beyond what reviews found.

## 5. Report
Your final message is the report; it is what the user reads in the session, so make it complete and easy to scan (Markdown headings and tables, no doc or file needed):
1. A one-line header: run time (Asia/Colombo), `origin/main` sha, tooling gaps.
2. The output of `cd $TOOLS/skills/pre-pr-review/scripts && python3 ready_table.py`, pasted as is: the **Merge-ready** table and the **Not ready** table grouped by reason.
3. **This round** table: PR | verdict | new Important/Verify findings (one line each) | summary link. Write "Nothing reviewed" if no PR needed review, and say why (e.g. all conflicting).
4. **Skipped** (conflicting, not checked) and **Filed issues** as short lists.
5. **Review-skill updates** proposed by agents (PRs that change AGENTS.md, skills, lint config, hooks or CI validators): list them for the user; don't apply them.

## Limits
- If a usage limit stops you, stop cleanly: post nothing half-finished; report which PRs weren't reached. Never enable or rely on paid overage.
- Never commit or push anything. Never approve, merge, label or close PRs.
- Only kill processes you started; services and listeners need process groups (agent-instructions.md).

# Review round (local)

You coordinate one review round for ballerina-nutcracker/ballerina, unattended, on the user's Mac, started by `scripts/run-round.sh`. Nothing from earlier runs survives except what is on GitHub.

## 0. Setup
1. Paths (exported by the runner; these are the defaults):
   - `REPO=/Users/waruna/Dev/Git/ballerina-lang-go`: the local clone. Its `origin` is the user's fork; `UPSTREAM=pr730remote` is ballerina-nutcracker/ballerina. Always review against `$UPSTREAM/main`. Only `git fetch` and `git worktree add` there; never touch its working tree or current branch.
   - `TOOLS=/Users/waruna/Dev/Git/ballerina-nutcracker-review`: this tooling (review skill `skills/pr-review`, posting/agent rules `skills/pre-pr-review`).
   - `SP=/private/tmp/review-sp`; `mkdir -p $SP/review-out`. Review worktrees go under `$SP/wt/pr<N>`; remove the ones this round created when it ends (`git -C $REPO worktree remove --force <path>`).
   - `JBALLERINA_SRC=/Users/waruna/Dev/Git/ballerina-lang`.
   Agents get `$REPO`, `$TOOLS`, `$UPSTREAM`, `$SP` and `$JBALLERINA_SRC` in their prompts.
2. `git -C $REPO fetch $UPSTREAM main` (and PR heads as needed: `git -C $REPO fetch $UPSTREAM +refs/pull/<N>/head:refs/review/pr<N>`).
3. GitHub: `gh` uses the user's own login, which can post. GraphQL works; the scripts use it. Check `gh auth status` first; if it fails, stop and report that.
4. Tooling: `bal` (jBallerina) is on PATH, so run parity checks as the review skill says. Go comes from the repo's toolchain line. If `golangci-lint` is missing, say so in the report header and skip lint.

## 1. Scan
`cd $TOOLS/skills/pre-pr-review/scripts && python3 scan_prs.py` lists PRs needing review: `NEW` (no summary of ours) or `MOVED` (head differs from the commit our last summary reviewed). It skips drafts, PRs approved at their current head (an approval of an older commit still needs review) and don't-merge/dnm/hold/wip labels. `ERR`: retry once, then list as "not checked". A PR whose head equals the commit in our latest summary is already reviewed: skip it.

## 2. Review
- Drop PRs that conflict with `$UPSTREAM/main` (`git -C $REPO merge-tree --write-tree $UPSTREAM/main refs/review/pr<N>`): no review, no comment; list as skipped.
- Stacks (base branch isn't `main`): `python3 $TOOLS/skills/pre-pr-review/scripts/stack.py <tip> --json` run inside `$REPO`; review the stack as one unit at the highest non-conflicting PR.
- MOVED PRs: interdiff of the PR's own changes (old reviewed head vs new head, each against its merge-base). Only merges of main, no PR-file change: refresh the summary (rebuild findings.json from GitHub with the new `head_sha`/`reviewed_diff`, post) instead of re-reviewing.
- One review subagent per PR (stack = one agent), at most 3 at a time, smallest PRs first. Each prompt: follow `$TOOLS/skills/pre-pr-review/references/agent-instructions.md` exactly; gives `$REPO`, `$TOOLS`, `$UPSTREAM`, `$SP`, `$JBALLERINA_SRC`, the PR number, the last reviewed sha (MOVED) and PR-specific focus. Rules belong in agent-instructions.md, never only in a prompt.
- No local findings files exist: agents rebuild every still-open finding of ours from GitHub before re-reviewing.

## 3. Post
Per finished review: dry-run `python3 $TOOLS/skills/pre-pr-review/scripts/post_review.py $SP/review-out/<N>/findings.json`; fix brevity warnings (shorten; complete repro programs; avoid "e.g." which counts as a sentence break); check overlap warnings against the other reviewer's comment (drop only true duplicates); then `--post`. If the head moved since the review, re-queue instead of posting.

## 4. Bugs found on main
`$TOOLS/skills/pre-pr-review/references/retrospective.md`, "Bugs found on main": one repro on current main, duplicate search (`gh api 'search/issues?q=repo:ballerina-nutcracker/ballerina+<words>'`), then file via `gh api repos/ballerina-nutcracker/ballerina/issues -f title=... -f body=... -f 'labels[]=triage' -f 'labels[]=Type/Bug'`. No bug hunting beyond what reviews found.

## 5. Report
Your final message is the report; it is what the user reads in the session, so make it complete and easy to scan (Markdown headings and tables, no doc or file needed):
1. Title `# Review round · <STARTED>` using the `STARTED` date and time from the prompt (when the review started; if missing, the time you started), then one line: `$UPSTREAM/main` sha, end time, tooling gaps.
2. The output of `cd $TOOLS/skills/pre-pr-review/scripts && python3 ready_table.py`, pasted as is: the **Open PRs** totals line (total, merge-ready, waiting for CI, not ready, drafts, held by label), the **Merge-ready** table, the **Waiting for CI** table (0 findings, only CI pending), and the **Not ready** table with the reason each PR isn't mergeable (both tables oldest PR first). Run it after posting so it reflects this round. If it fails, say so and list each open PR with its reason by hand.
3. **This round** table, oldest PR first: PR | verdict | new Important/Verify findings (one line each) | summary link. Write "Nothing reviewed" if no PR needed review, and say why (e.g. all conflicting).
4. **Skipped** (conflicting, not checked) and **Filed issues** as short lists, PR numbers in ascending order.
5. **Review-skill updates** proposed by agents (PRs that change AGENTS.md, skills, lint config, hooks or CI validators): list them for the user; don't apply them.

## Limits
- If posting a PR's review fails, put its findings (title, path:line, body) in the report so the user can post them by hand.
- If a usage limit stops you, stop cleanly: post nothing half-finished; report which PRs weren't reached. Never enable or rely on paid overage.
- Never commit or push anything. Never approve, merge, label or close PRs.
- Only kill processes you started; services and listeners need process groups (agent-instructions.md).

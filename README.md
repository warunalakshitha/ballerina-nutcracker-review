# ballerina-nutcracker-review

PR review tooling for [ballerina-nutcracker/ballerina](https://github.com/ballerina-nutcracker/ballerina). Review rounds run in Claude Code cloud sessions on a schedule; skill fixes are made locally and pushed here.

- `skills/pr-review/`: the review checklist (`SKILL.md`) and companion checklists (stdlib, LS, workflow).
- `skills/pre-pr-review/`: agent rules (`references/agent-instructions.md`), the round procedure (`references/routine.md`), the cloud setup (`references/cloud-round.md`), the posting format (`references/github-posting.md`), the retrospective (`references/retrospective.md`) and scripts.

## How rounds run

- **Schedule:** a claude.ai routine at 06:00, 12:00, 18:00 and 00:00 Asia/Colombo (it starts a few minutes late). It resets its checkout of this repo to `main`, then follows `references/cloud-round.md`.
- **Environment** (`ballerina-nutcracker-review` at claude.ai/code): network access Limited plus `dist.ballerina.io`; the setup script installs Ballerina 2201.14.1, wrk, hyperfine and shellcheck. Go 1.27.1 comes through the module proxy (`GOTOOLCHAIN`), golangci-lint and actionlint are built with it.
- **One round at a time:** `reports/round.lock` on `main`, updated hourly while a round runs. A run skips when the PR scan matches `reports/last-scan.txt` from the last round.
- **Posting:** cloud sessions can read ballerina-nutcracker/ballerina but not write to it. Rounds queue reviews, issues and comments in `outbox/`; the `post-outbox` Action posts them as the reviewer with the `REVIEW_POST_TOKEN` secret (a classic token with `public_repo`) and logs each in `outbox/posted.log`.
- **GitHub access for the routine:** the Claude GitHub App, installed on this repo only.
- **Mac fallback:** `skills/pre-pr-review/scripts/run-round.sh [extra instructions]` runs a round locally if the cloud can't (needs `claude`, `gh`, `go`, `bal`, `wrk`, `hyperfine` on `PATH`, `~/Dev/Git/ballerina-lang-go` with a `pr730remote` remote and `~/Dev/Git/ballerina-lang`; keep the Mac on power). It posts directly with your `gh` login and copies the report to `reports/latest.md` for you to commit. It respects the cloud lock: it stops if a round is running and holds the lock while it runs.
- **Reports:** each round pushes `reports/latest.md`. Its **Retrospective inputs** section feeds `references/retrospective.md`, which you run interactively.

## Scripts (`skills/pre-pr-review/scripts/`)

- `scan_prs.py`: PRs needing review, `NEW` (no summary of ours) or `MOVED` (head changed since our last summary). Skips drafts, PRs approved at their current head, and don't-merge/dnm/hold/wip labels.
- `ready_table.py`: open-PR totals, then Can merge (in merge queue, ready or after CI) and Cannot merge (with reason) tables, oldest PR first.
- `post_review.py`: posts or updates a review from `findings.json` (dry run by default, `--post` to post).
- `stack.py`: the stack a PR belongs to.
- `post_outbox.py`: posts the reviews, issues and comments a cloud round queued in `outbox/`; run by `.github/workflows/post-outbox.yml` with the `REVIEW_POST_TOKEN` secret, because cloud sessions can't write to ballerina-nutcracker/ballerina.
- `round_lock.py`: the cloud round lock (`reports/round.lock`), hourly heartbeat, skip-if-unchanged check and report push. See `references/cloud-round.md`.

Repo rules (AGENTS.md, docs, the repo's own skills) are read from ballerina-nutcracker/ballerina `main` at review time; only the review skill lives here.

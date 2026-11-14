# ballerina-nutcracker-review

PR review tooling for [ballerina-nutcracker/ballerina](https://github.com/ballerina-nutcracker/ballerina), used for local review rounds.

- `skills/pr-review/`: the review checklist (`SKILL.md`) and companion checklists (stdlib, LS, workflow).
- `skills/pre-pr-review/`: agent rules (`references/agent-instructions.md`), the round procedure (`references/routine.md`), the posting format (`references/github-posting.md`), the retrospective (`references/retrospective.md`) and scripts.

## Prerequisites

macOS with [Homebrew](https://brew.sh). Install:

```bash
brew install gh go golangci-lint wrk hyperfine actionlint shellcheck
gh auth login            # the account the reviews are posted from
```

| Tool | Used for | Required |
|---|---|---|
| `claude` ([Claude Code](https://claude.com/claude-code), at `~/.local/bin/claude`) | runs the round | yes |
| `gh`, logged in | reading PRs and posting reviews | yes |
| `git`, `python3` (macOS system ones are fine) | worktrees, scripts | yes |
| `go` (version from the repo's `go.mod` toolchain line) | building and testing PRs | yes |
| `bal` ([Ballerina](https://ballerina.io/downloads/), jBallerina) | parity checks (`bal run`) | yes |
| `wrk`, `hyperfine` | `compiler-tools` benchmark tests, which fail without them (CI installs both) | yes |
| `golangci-lint` (same version as CI, see `.github/workflows/golangci-lint.yml`) | `make lint` / `make lint-module/<m>` | recommended |
| `actionlint`, `shellcheck` | PRs that change `.github/workflows/*.yml` | recommended |

`run-round.sh` checks the required ones and stops with `missing: <tool>` if one isn't on `PATH`.

Local clones:

- `~/Dev/Git/ballerina-lang-go`: a clone of the repo with a remote (default `pr730remote`) pointing at `ballerina-nutcracker/ballerina`.
- `~/Dev/Git/ballerina-lang`: a clone of `ballerina-platform/ballerina-lang` (jBallerina source) for parity questions.

## Running a round

`skills/pre-pr-review/scripts/run-round.sh [extra instructions]` starts a headless Claude session that follows `routine.md`.

- Override `REPO`, `UPSTREAM`, `SP` and `JBALLERINA_SRC` via the environment.
- Keep the Mac on power: `caffeinate -is` blocks system sleep only on AC, and a closed lid still sleeps without an external display.

The runner clears `$SP` (except `reports/`), `$SP/wt` worktrees and `refs/review/*` before and after each round. It saves `$SP/reports/<timestamp>.md` and copies it to `reports/latest.md`, which is tracked: commit it after each round. The report's **Retrospective inputs** section feeds `references/retrospective.md`, which you run interactively.

## Scripts (`skills/pre-pr-review/scripts/`)

- `scan_prs.py`: PRs needing review, `NEW` (no summary of ours) or `MOVED` (head changed since our last summary). Skips drafts, PRs approved at their current head, and don't-merge/dnm/hold/wip labels.
- `ready_table.py`: open-PR totals, then Can merge (in merge queue, ready or after CI) and Cannot merge (with reason) tables, oldest PR first.
- `post_review.py`: posts or updates a review from `findings.json` (dry run by default, `--post` to post).
- `stack.py`: the stack a PR belongs to.
- `post_outbox.py`: posts the reviews, issues and comments a cloud round queued in `outbox/`; run by `.github/workflows/post-outbox.yml` with the `REVIEW_POST_TOKEN` secret, because cloud sessions can't write to ballerina-nutcracker/ballerina.
- `round_lock.py`: the cloud round lock (`reports/round.lock`), hourly heartbeat, skip-if-unchanged check and report push. See `references/cloud-round.md`.

Repo rules (AGENTS.md, docs, the repo's own skills) are read from ballerina-nutcracker/ballerina `main` at review time; only the review skill lives here.

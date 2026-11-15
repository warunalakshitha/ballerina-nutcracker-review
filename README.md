# ballerina-nutcracker-review

PR review tooling for [ballerina-nutcracker/ballerina](https://github.com/ballerina-nutcracker/ballerina): the review skills and scripts. Review rounds run in Claude Code cloud sessions and never commit here; skill fixes are made locally and pushed here.

- `skills/pr-review/`: the review checklist (`SKILL.md`) and companion checklists (stdlib, LS, workflow).
- `skills/pre-pr-review/`: agent rules (`references/agent-instructions.md`), the round procedure (`references/routine.md`), the cloud setup (`references/cloud-round.md`), the posting format (`references/github-posting.md`), the retrospective (`references/retrospective.md`) and scripts.

## How rounds run

- **Routine:** a claude.ai routine runs hourly. It resets its checkout of this repo to `main`, then follows `references/cloud-round.md`, and stops within a minute when no PR changed since the last round.
- **Review board:** the [Ballerina Nutcracker Pull Request Review Board](https://claude.ai/artifact/PDgHUQcCGn5gx84bQ2Ssh1) artifact holds the latest report (open-PR tables, what each round reviewed), earlier reports, and the round's lock and last scan. Rounds write it with `ArtifactData`; nothing is committed to this repo.
- **Environment** (`ballerina-nutcracker-review` at claude.ai/code): network access Limited plus `dist.ballerina.io`, and this setup script (cached between runs):

  ```bash
  #!/bin/bash
  set -e
  export PATH="/usr/local/go/bin:/root/go/bin:$PATH"
  curl -fsSL -o /tmp/bal.deb https://dist.ballerina.io/downloads/2201.14.1/ballerina-2201.14.1-swan-lake-linux-x64.deb
  apt-get install -y /tmp/bal.deb && rm -f /tmp/bal.deb
  apt-get update && apt-get install -y wrk hyperfine shellcheck
  # go.dev is blocked; the module proxy serves the toolchain the repo pins.
  go env -w GOTOOLCHAIN=go1.27.1
  go version
  # Lint tools must be built with that Go, or golangci-lint refuses the module.
  # One go install per tool: Go refuses packages from different modules or versions in one command.
  GOBIN=/usr/local/bin go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@v2.15.0
  GOBIN=/usr/local/bin go install github.com/rhysd/actionlint/cmd/actionlint@latest
  bal version && golangci-lint --version && actionlint --version
  ```
- **One round at a time:** the lock is `state/lock` on the board, created with a version check so only one session gets it, and refreshed at least hourly while a round runs. A run skips when the PR scan matches `state/scan` from the last round.
- **Posting:** cloud sessions can read ballerina-nutcracker/ballerina but not write to it. Rounds send each review, issue and comment as a `repository_dispatch` (`round_state.py send`); the `post-outbox` Action posts it as the reviewer with the `REVIEW_POST_TOKEN` secret (a classic token with `public_repo`). Nothing is committed; failed runs email the repo owner.
- **GitHub access for the routine:** the Claude GitHub App, installed on this repo only.
- **Mac fallback:** `skills/pre-pr-review/scripts/run-round.sh [extra instructions]` runs a round locally if the cloud can't (needs `claude`, `gh`, `go`, `bal`, `wrk`, `hyperfine` on `PATH`, `~/Dev/Git/ballerina-lang-go` with a `pr730remote` remote and `~/Dev/Git/ballerina-lang`; keep the Mac on power). It shares the board's lock, scan and report and posts directly with your `gh` login.
- **Reports:** each report's **Retrospective inputs** section feeds `references/retrospective.md`, which you run interactively.

## Scripts (`skills/pre-pr-review/scripts/`)

- `scan_prs.py`: PRs needing review, `NEW` (no summary of ours) or `MOVED` (head changed since our last summary). Skips drafts, PRs approved at their current head, don't-merge/dnm/hold/wip labels, and PRs pushed less than 30 minutes ago (`SETTLING` on stderr; `SETTLE_MINUTES` overrides), so a burst of pushes is reviewed once, at its final commit.
- `ready_table.py`: open-PR totals, then Can merge (in merge queue, ready or after CI), Cannot merge (with reason), then Drafts and held tables, oldest PR first.
- `post_review.py`: posts or updates a review from `findings.json` (dry run by default, `--post` to post).
- `stack.py`: the stack a PR belongs to.
- `post_outbox.py`: posts a review, issue or comment a round sent; run by `.github/workflows/post-outbox.yml` with the `REVIEW_POST_TOKEN` secret.
- `round_state.py`: scan comparison (`unchanged`, `saved-scan`), `send` (dispatch to the post-outbox Action) and `wait-posted`. See `references/cloud-round.md`.

Repo rules (AGENTS.md, docs, the repo's own skills) are read from ballerina-nutcracker/ballerina `main` at review time; only the review skill lives here.

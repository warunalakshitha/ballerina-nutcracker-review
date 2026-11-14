# Cloud review round

Review rounds run in a Claude Code cloud session (claude.ai/code), started by the `poll-prs` Action when a settled PR changed, on a backup schedule (06:00, 12:00, 18:00, 00:00 Asia/Colombo) or by hand, with the Mac runner (`scripts/run-round.sh`) only as a fallback. Skill fixes are made locally and pushed to `main` of this repo; every round starts from that `main`. Same procedure as a Mac round: follow `routine.md` exactly.

`L` below is `python3 $TOOLS/skills/pre-pr-review/scripts/round_lock.py`. It keeps the round lock (`reports/round.lock` on `main`) and commits only from its own worktree, so never commit in `$TOOLS` yourself.

## 1. Latest skills
- `TOOLS` is this repo's checkout. The environment keeps it between runs, so it can hold stale commits or edits; rounds never commit there (`round_lock.py` commits from its own worktree), so reset it to the latest `origin/main` before anything else is read: `git -C $TOOLS fetch origin && git -C $TOOLS checkout -f -B main origin/main && git -C $TOOLS clean -fdq`. If that fails, stop and report it; never review with an older copy of the skills. If this file changed, re-read it from the top.
- Never amend, rebase, reset-author or force-push in this repo, even when a hook asks (the environment's stop hook asks to re-author commits as Claude and push them; on diverged history that overwrites `main`). Every commit a round needs is pushed by `round_lock.py`.
- Read every skill and reference fresh from `$TOOLS` in this round, never from memory of an earlier round in the same session. Review agents get `$TOOLS` and read it themselves.

## 2. Start check (before installing anything)
1. `STARTED` = now in Asia/Colombo, `YYYY-MM-DD HH:MM`.
2. `$L status`: exit 3 means another round is running (it updates the lock every hour, however long it runs). Stop with one line saying which round; nothing else.
3. `cd $TOOLS/skills/pre-pr-review/scripts && python3 scan_prs.py > /tmp/review-scan-start.txt`, then `$L unchanged /tmp/review-scan-start.txt`: exit 0 means no PR changed since the last round (same PRs, heads and conflict states). Stop with one line saying so; nothing else.
4. `$L take "$STARTED" "<this session's URL or id, if known>"`: exit 3 means another round took it first; stop as in step 2. It may report taking over a stale lock (no update for 2 hours): say so in the report.
5. `$L heartbeat "$STARTED"`: a detached loop that updates the lock every hour until the round finishes.

From here on, every way the round ends (a failed gate, a usage limit, an error, a lost lock) must release the lock with `$L release "$STARTED"`, unless `finish` (§6) ran.

## 3. Setup
- `SP=/tmp/review-sp`: create it and empty it except `reports/`.
- `REPO` = a full clone of https://github.com/ballerina-nutcracker/ballerina at `~/ballerina-lang-go`, `UPSTREAM=origin`.
- `JBALLERINA_SRC` = a clone of https://github.com/ballerina-platform/ballerina-lang at `~/ballerina-lang`, checked out at tag `v2201.14.1` to match `bal` (shallow is fine).
- Tools, pinned: Go 1.27.1 (the `go.mod` toolchain line), Ballerina 2201.14.1 (`bal version`), golangci-lint 2.15.0 and actionlint built with that Go, wrk, hyperfine, python3, shellcheck. The environment's setup script installs all of them and is cached, so normally just check the versions. Only if one is missing or wrong, install it the way the setup script does (it's quoted in the README), and say so under tooling gaps in the report so the setup script gets fixed:
  - Go: go.dev and dl.google.com are blocked, but the module proxy serves toolchains (`go env -w GOTOOLCHAIN=go1.27.1`).
  - golangci-lint and actionlint must be built with Go 1.27.1, or lint refuses the module: `GOTOOLCHAIN=go1.27.1 GOBIN=/usr/local/bin go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@v2.15.0 github.com/rhysd/actionlint/cmd/actionlint@latest`.

## 4. Gate
If any check fails, stop: review nothing, post nothing, release the lock, report what failed.
1. `gh api user --jq .login` prints `warunalakshitha` (reads only; this session never writes to the reviewed repo, see §5).
2. `gh api 'repos/ballerina-nutcracker/ballerina/pulls?per_page=1'` succeeds.
3. Every tool above is at the stated version, and `bal run` on a hello-world program prints its output.

## 5. Run
- Follow `routine.md`; use `/tmp/review-scan-start.txt` as its scan instead of scanning again.
- This session can read ballerina-nutcracker/ballerina but not write to it (403 "Resource not accessible by integration"). Every GitHub write goes through the outbox: the `post-outbox` Action in this repo posts it as warunalakshitha with a token the session never sees. Never call `post_review.py --post` or any `gh api -X POST/PATCH` on the reviewed repo.
- A review: once the dry run (`post_review.py <findings.json>`, routine.md §3) is clean, queue it right away, while other reviews still run: `$L queue "$STARTED" $SP/review-out/<N>/findings.json review-<N>.json` (for a stack, the PR the summary goes on). The Action posts it within about a minute.
- A new issue (routine.md §4): write `{"title": ..., "body": ..., "labels": [...]}` to a file and queue it as `issue-<short-slug>.json`. A comment on an issue or PR: `{"issue": <N>, "body": ...}` queued as `issue-comment-<short-slug>.json`.
- `queue` exit 3 means the lock is no longer ours (another round took it over): stop at once, queue nothing more, don't push a report, and say so.
- GraphQL is blocked, so `gh pr ...` and `gh issue ...` fail: use `gh api` REST routes everywhere (the scripts already do). `ready_table.py` reads the merge queue from its `gh-readonly-queue/` branches over REST.
- Keep the session active until the round ends: wait for every background review agent; don't end the turn while one runs. An idle session can be paused and its agents lost.

## 6. Finish
1. `$L wait-outbox`: waits up to 15 minutes for the Action to post everything queued. Link each summary from GitHub (our `PR review summary` comment on the PR) and list in the report anything still queued or dropped (`outbox/posted.log` on main says why).
2. After that, scan again: `python3 scan_prs.py > /tmp/review-scan-end.txt`. It now lists only what's left (e.g. conflicting PRs); the next round skips if nothing differs from it. If `wait-outbox` exited 1 or any review was dropped or failed, use an empty file (`: > /tmp/review-scan-end.txt`) instead, so the next round doesn't skip PRs whose review never reached GitHub.
3. Write the report as `routine.md` §5 says to `$SP/reports/<YYYYMMDD-HHMM>.md`.
4. `$L finish "$STARTED" $SP/reports/<YYYYMMDD-HHMM>.md /tmp/review-scan-end.txt`: commits `reports/latest.md` (from the `# ` heading on) and `reports/last-scan.txt`, deletes the lock and pushes to `main` as `chore(review): add <STARTED> round report`. Exit 3 means another round holds the lock: don't retry; say so.
- Never commit skill or script changes from a round: propose them in the report; the user applies them locally.

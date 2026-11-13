# Cloud review round

Review rounds run in a Claude Code cloud session (claude.ai/code), never on the user's Mac. Skill fixes are made locally and pushed to `main` of this repo; every round starts from that `main`. Same procedure as a local `run-round.sh` round: follow `routine.md` exactly.

## 1. Setup (before reviewing anything)
- `TOOLS` is this repo's checkout. It must be at the latest `origin/main` before anything else is read: `git -C $TOOLS fetch origin && git -C $TOOLS checkout main && git -C $TOOLS merge --ff-only origin/main`. If that fails (local commits or edits), stop and report it; never review with an older copy of the skills. If this file changed in the pull, re-read it from the top.
- Read every skill and reference fresh from `$TOOLS` in this round, never from memory of an earlier round in the same session. Review agents get `$TOOLS` and read it themselves.
- `SP=/tmp/review-sp`: create it and empty it except `reports/`. `STARTED` = now in Asia/Colombo, `YYYY-MM-DD HH:MM`.
- `REPO` = a full clone of https://github.com/ballerina-nutcracker/ballerina at `~/ballerina-lang-go`, `UPSTREAM=origin`.
- `JBALLERINA_SRC` = a clone of https://github.com/ballerina-platform/ballerina-lang at `~/ballerina-lang`, checked out at tag `v2201.14.1` to match `bal` (shallow is fine).
- Tools, pinned: Go from the `go.mod` toolchain line (1.27.1), Ballerina 2201.14.1 (`bal version`), golangci-lint at the version in `.github/workflows/golangci-lint.yml` (2.15.0), wrk, hyperfine, python3, actionlint, shellcheck. Install what's missing: apt as root, `https://dist.ballerina.io/downloads/2201.14.1/ballerina-2201.14.1-swan-lake-linux-x64.deb`, or the official release downloads.

## 2. Gate
If any check fails, stop: review nothing, post nothing, report what failed.
1. `gh api user --jq .login` prints `warunalakshitha`. Comments must come from that account, or the next scan treats every PR as unreviewed and posts duplicates.
2. `gh api 'repos/ballerina-nutcracker/ballerina/pulls?per_page=1'` succeeds.
3. Every tool above is at the stated version, and `bal run` on a hello-world program prints its output.

## 3. Run
- GraphQL is blocked, so `gh pr ...` and `gh issue ...` fail: use `gh api` REST routes everywhere (the scripts already do). `ready_table.py` reads the merge queue from its `gh-readonly-queue/` branches over REST.
- Keep the session active until the round ends: wait for every background review agent; don't end the turn while one runs. An idle session can be paused and its agents lost.
- Run one round at a time across all sessions: two rounds review the same PRs and post twice.

## 4. Finish
- Write the report as `routine.md` §5 says and save it to `reports/latest.md` (from the `# ` heading on).
- Commit only that file, subject `chore(review): add <STARTED> round report`, no body, no trailers; push to `main`. If the push to `main` is refused, push a branch and say which.
- Never commit skill or script changes from a round: propose them in the report; the user applies them locally.

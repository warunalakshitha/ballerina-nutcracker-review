# Cloud review round

Review rounds run in a Claude Code cloud session (claude.ai/code), on a schedule (06:00, 12:00, 18:00, 00:00 Asia/Colombo) or by hand, never on the user's Mac. Skill fixes are made locally and pushed to `main` of this repo; every round starts from that `main`. Same procedure as a local `run-round.sh` round: follow `routine.md` exactly.

`L` below is `python3 $TOOLS/skills/pre-pr-review/scripts/round_lock.py`. It keeps the round lock (`reports/round.lock` on `main`) and commits only from its own worktree, so never commit in `$TOOLS` yourself.

## 1. Latest skills
- `TOOLS` is this repo's checkout. It must be at the latest `origin/main` before anything else is read: `git -C $TOOLS fetch origin && git -C $TOOLS checkout main && git -C $TOOLS merge --ff-only origin/main`. If that fails (local commits or edits), stop and report it; never review with an older copy of the skills. If this file changed in the pull, re-read it from the top.
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
- Tools, pinned: Go from the `go.mod` toolchain line (1.27.1), Ballerina 2201.14.1 (`bal version`), golangci-lint at the version in `.github/workflows/golangci-lint.yml` (2.15.0), wrk, hyperfine, python3, actionlint, shellcheck. Install what's missing: apt as root, `https://dist.ballerina.io/downloads/2201.14.1/ballerina-2201.14.1-swan-lake-linux-x64.deb`, or the official release downloads.

## 4. Gate
If any check fails, stop: review nothing, post nothing, release the lock, report what failed.
1. `gh api user --jq .login` prints `warunalakshitha`. Comments must come from that account, or the next scan treats every PR as unreviewed and posts duplicates.
2. `gh api 'repos/ballerina-nutcracker/ballerina/pulls?per_page=1'` succeeds.
3. Every tool above is at the stated version, and `bal run` on a hello-world program prints its output.

## 5. Run
- Follow `routine.md`; use `/tmp/review-scan-start.txt` as its scan instead of scanning again.
- Post each PR as soon as its review finishes (routine.md §3), not all together at the end. Right before each post run `$L beat "$STARTED"`: exit 3 means the lock is no longer ours (another round took it over), so stop at once: post nothing more, don't push a report, and say so.
- GraphQL is blocked, so `gh pr ...` and `gh issue ...` fail: use `gh api` REST routes everywhere (the scripts already do). `ready_table.py` reads the merge queue from its `gh-readonly-queue/` branches over REST.
- Keep the session active until the round ends: wait for every background review agent; don't end the turn while one runs. An idle session can be paused and its agents lost.

## 6. Finish
1. After the last post, scan again: `python3 scan_prs.py > /tmp/review-scan-end.txt`. It now lists only what's left (e.g. conflicting PRs); the next round skips if nothing differs from it.
2. Write the report as `routine.md` §5 says to `$SP/reports/<YYYYMMDD-HHMM>.md`.
3. `$L finish "$STARTED" $SP/reports/<YYYYMMDD-HHMM>.md /tmp/review-scan-end.txt`: commits `reports/latest.md` (from the `# ` heading on) and `reports/last-scan.txt`, deletes the lock and pushes to `main` as `chore(review): add <STARTED> round report`. Exit 3 means another round holds the lock: don't retry; say so.
- Never commit skill or script changes from a round: propose them in the report; the user applies them locally.

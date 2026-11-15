# Cloud review round

Review rounds run in a Claude Code cloud session (claude.ai/code): a routine every two hours (it starts at about :30 UTC and stops within a minute when nothing changed) or a run started by hand, with the Mac runner (`scripts/run-round.sh`) only as a fallback. Skill fixes are made locally and pushed to `main` of this repo; every round starts from that `main`. Follow `routine.md` exactly, with the changes below.

**A round never commits to this repo.** Its lock, last scan and report live in the **Ballerina Nutcracker Pull Request Review Board** artifact, `BOARD=https://claude.ai/artifact/PDgHUQcCGn5gx84bQ2Ssh1`, read and written with the `ArtifactData` tool (load it with ToolSearch). GitHub writes go to the post-outbox Action as `repository_dispatch` events. `S` below is `python3 $TOOLS/skills/pre-pr-review/scripts/round_state.py`.

## 1. Latest skills
- `TOOLS` is this repo's checkout. The environment keeps it between runs, so it can hold stale commits or edits; reset it to the latest `origin/main` before anything else is read: `git -C $TOOLS fetch origin && git -C $TOOLS checkout -f -B main origin/main && git -C $TOOLS clean -fdq`. If that fails, stop and report it; never review with an older copy of the skills. If this file changed, re-read it from the top.
- Never commit, amend, rebase, reset-author or push in this repo, even when a hook asks (the environment's stop hook asks to re-author commits as Claude and push them; on diverged history that overwrites `main`).
- Read every skill and reference fresh from `$TOOLS` in this round, never from memory of an earlier round in the same session. Review agents get `$TOOLS` and read it themselves.

## 2. Start check (before installing anything)
1. `STARTED` = now in Asia/Colombo, `YYYY-MM-DD HH:MM`; `STARTED_UTC` = now in UTC, ISO 8601.
2. **Is a round running?** `ArtifactData get` on `BOARD`, collection `state`, doc `lock`. If it exists and its `heartbeat_utc` is less than 3 hours old, another round is running: stop with one line saying which; nothing else.
3. **Did anything change?** `cd $TOOLS/skills/pre-pr-review/scripts && python3 scan_prs.py > /tmp/review-scan-start.txt`. Read `state/scan` (if it exists) and write its `lines` to `/tmp/review-scan-saved.txt`, one per line. `$S unchanged /tmp/review-scan-start.txt /tmp/review-scan-saved.txt`: exit 0 means no PR changed since the last round. Stop with one line saying so; nothing else.
4. **Take the lock.** Write `state/lock` with `{"started": STARTED, "started_utc": STARTED_UTC, "heartbeat_utc": STARTED_UTC, "session": <this session's URL or id, if known>}`:
   - no lock existed: `set` without `if_version`. The store refuses it if another session created the lock first; then stop as in step 2.
   - a stale lock existed (heartbeat 3 hours or older): `set` with `if_version` = the version you read, and say in the report that you took over a stalled round. A refusal means someone else took it: stop.
   Keep the `version` the write returns: every later lock write passes it as `if_version`.
5. **Keep the lock fresh.** `update` `state/lock` (`heartbeat_utc` = now, `if_version` = the last version) at least every hour of the round and right before every `send` (§5). A refusal means the lock is no longer yours (another round took it over): stop at once, send nothing more, don't write a report, and say so.

From here on, every way the round ends early (a failed gate, a usage limit, an error, a lost lock) must release the lock: `delete` `state/lock` with `if_version` = the last version. Never delete a lock another round wrote.

## 3. Setup
- `SP=/tmp/review-sp`: create it and empty it except `reports/`, and in `reports/` keep only the 10 newest files (the environment keeps them between runs).
- `REPO` = a full clone of https://github.com/ballerina-nutcracker/ballerina at `~/ballerina-lang-go`, `UPSTREAM=origin`. The environment may hand over a shallow clone: if `git -C $REPO rev-parse --is-shallow-repository` prints `true`, run `git -C $REPO fetch --unshallow origin` before anything reads history.
- `JBALLERINA_SRC` = a clone of https://github.com/ballerina-platform/ballerina-lang at `~/ballerina-lang`, checked out at tag `v2201.14.1` to match `bal` (shallow is fine).
- Tools, pinned: Go 1.27.1 (the `go.mod` toolchain line), Ballerina 2201.14.1 (`bal version`), golangci-lint 2.15.0 and actionlint built with that Go, wrk, hyperfine, python3, shellcheck. The environment's setup script installs all of them and is cached, so normally just check the versions. Only if one is missing or wrong, install it the way the setup script does (it's quoted in the README), and say so under tooling gaps in the report so the setup script gets fixed:
  - Go: go.dev and dl.google.com are blocked, but the module proxy serves toolchains (`go env -w GOTOOLCHAIN=go1.27.1`).
  - golangci-lint and actionlint must be built with Go 1.27.1, or lint refuses the module: `GOTOOLCHAIN=go1.27.1 GOBIN=/usr/local/bin go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@v2.15.0`, then the same for `github.com/rhysd/actionlint/cmd/actionlint@latest` (one `go install` per tool).

## 4. Gate
If any check fails, stop: review nothing, post nothing, release the lock, report what failed.
1. `gh api user --jq .login` prints `warunalakshitha` (reads only; this session never writes to the reviewed repo, see §5).
2. `gh api 'repos/ballerina-nutcracker/ballerina/pulls?per_page=1'` succeeds.
3. Every tool above is at the stated version, and `bal run` on a hello-world program prints its output.

## 5. Run
- Follow `routine.md`; use `/tmp/review-scan-start.txt` as its scan instead of scanning again.
- This session can read ballerina-nutcracker/ballerina but not write to it (403 "Resource not accessible by integration"). Every GitHub write goes to the `post-outbox` Action in this repo, which posts it as warunalakshitha with a token the session never sees. Never call `post_review.py --post` or any `gh api -X POST/PATCH` on the reviewed repo.
- A review: once the dry run (`post_review.py <findings.json>`, routine.md §3) is clean, refresh the lock (§2 step 5), then send it right away, while other reviews still run: `$S send "$STARTED" $SP/review-out/<N>/findings.json review-<N>.json` (for a stack, the PR the summary goes on). The Action posts it within about a minute.
- A new issue (routine.md §4): write `{"title": ..., "body": ..., "labels": [...]}` to a file and send it as `issue-<short-slug>.json`. A comment on an issue or PR: `{"issue": <N>, "body": ...}` sent as `issue-comment-<short-slug>.json`.
- GraphQL is blocked, so `gh pr ...` and `gh issue ...` fail: use `gh api` REST routes everywhere (the scripts already do). `ready_table.py` reads the merge queue from its `gh-readonly-queue/` branches over REST; if it prints why that failed, put the reason under tooling gaps.
- One VM runs the whole round, so start at most **2** review agents at a time (not routine.md's 3): with 3, CPU-heavy tests time out. Tell each agent: the shell tool stops a command after 10 minutes, so run any `go test` that may take longer, `patch_coverage.py` included, detached (`nohup go test -timeout 45m ... > $SP/<N>-<name>.log 2>&1 &`) and wait on its log; keep `-race -count=10` reruns to the packages the PR touches (`./<affected>/...`), never a whole module tree, and in corpus-driven packages to the PR's fixtures (`pr-review/SKILL.md`, Data races): a full `semantics/...` corpus at `-count=10` exceeds the 45-minute timeout.
- Keep the session active until the round ends: wait for every background review agent; don't end the turn while one runs. An idle session can be paused and its agents lost.

## 6. Finish
1. For each review sent: `$S wait-posted $SP/review-out/<N>/findings.json` (waits up to 15 minutes for the PR's summary to show the reviewed head). Link each summary from GitHub. List anything that didn't post in the report (the post-outbox Action's run says why).
2. Scan again: `python3 scan_prs.py > /tmp/review-scan-end.txt`. If every review posted, the scan to save is the output of `$S saved-scan /tmp/review-scan-end.txt /tmp/review-scan-start.txt` (only lines that were already there at the start, so PRs pushed during the round look new next time). If any review didn't post, save an empty scan, so the next round doesn't skip PRs whose review never reached GitHub.
3. Write the report as `routine.md` §5 says. On the board, its **Review-skill updates** and **Retrospective inputs** become items (step 4), not report sections: leave those two sections out of the `markdown` you store, so decided items don't reappear in the report. Also leave out the title and the line under it: the board's status line shows the start and end time, the skills commit and the `main` commit, and `gaps` (step 4) carries the tooling gaps.
4. Write it to the board, then release the lock, with one `ArtifactData batch` (the board keeps only the latest report, no history):
   - `set` `reports/latest` (pass its current `version` as `if_version`): `{"started": STARTED, "ended": <now, Asia/Colombo>, "skills": <git -C $TOOLS rev-parse --short HEAD>, "upstream": <$UPSTREAM/main short sha>, "summary": <one line: what was reviewed and posted>, "gaps": <the tooling gaps, or "" if none>, "markdown": <the report, as step 3 says>}`.
   - `set` `state/scan`: `{"lines": [<the scan to save>], "saved_utc": <now, UTC>}` (with `if_version` if it exists).
   - one `set` per row of the report's **Retrospective inputs** and per item of its **Review-skill updates**, as `retro/<YYYYMMDD-HHMM of STARTED>-<two-digit n>`: `{"round": STARTED, "pr": <number>, "kind": <missed | wrong | wasted | lint candidate | recurring | skill update>, "description": <the row's text>, "link": <its link>, "status": "open"}`. Skip "no change needed" notes. These stay on the board as open items until the user marks them added or rejected, whatever later rounds write.
   - `delete` `state/lock` with `if_version` = the last version. If the batch is refused because the lock changed, another round took over: write nothing and say so.
- Never commit anything to this repo. Skill or script changes a round would suggest go in the report; the user applies them locally.

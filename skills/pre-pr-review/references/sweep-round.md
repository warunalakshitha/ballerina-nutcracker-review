# Sweep round

A sweep re-reviews every open PR whose review was written by skills older than a target commit, so each author gets one complete, current list of findings to fix in a single push. It runs in a Claude Code cloud session, started by its own routine every three hours; each run re-reviews as many stale PRs as fit in about three hours and the next run continues. While a sweep is running, the hourly review rounds stop (cloud-round.md §2), and they resume by themselves once the sweep marks itself done.

Follow `cloud-round.md` exactly, with the changes below. `BOARD`, `S`, `TOOLS`, `REPO`, `UPSTREAM`, `SP` and the "never commit to this repo" rule are as there.

## Sweep state
The board's `state/sweep` document drives the sweep:
`{"target": <skills commit>, "status": "running" | "done", "requested": <Asia/Colombo time>, "total": <stale PRs when it started>, "done_count": <PRs re-reviewed so far>, "left": <stale PRs still to do>, "updated": <Asia/Colombo time>, "done_at": <time, once done>}`.
The user starts a sweep by setting `target` to a skills commit and `status` to `running` (`total`, `done_count`, `left` absent). Only sweep runs change it after that.

## Changes to cloud-round.md
1. **Latest skills (§1):** unchanged. The target must resolve in `$TOOLS` after the reset; if it doesn't, stop and say so.
2. **Start check (§2):**
   - Step 2: the lock check as written, but skip its `state/sweep` check (that pauses hourly rounds, not this one).
   - Replace step 3 ("Did anything change?") with: `ArtifactData get` `state/sweep`. If it is missing or its `status` isn't `running`, stop with one line ("No sweep requested"). Otherwise keep its `version`.
   - Steps 4–5 (take the lock, keep it fresh) as written. The lock's heartbeat must stay fresh for the whole run: refresh it at least every 45 minutes, not only before each send.
3. **Setup and gate (§3, §4):** unchanged, plus a disk check before any review: the environment keeps its disk between runs and a sweep builds many PRs. If `df -Pk "$HOME"` shows less than 20 GB free, run `go clean -cache` and remove `$SP/wt` worktrees left from an earlier run (`git -C $REPO worktree prune` afterwards); say in the report how much it freed. If still under 10 GB free, stop and report it.
4. **Pick the PRs:** `cd $TOOLS/skills/pre-pr-review/scripts && TOOLS=$TOOLS python3 sweep_candidates.py <target>` lists PRs whose head moved since their last review first (`<N> MOVED …`: hourly rounds are paused, so an author who pushed must not wait for the sweep to end), then the stale PRs, oldest first (`<N> STALE <tools> <merge>`). Take them in that order; re-run the script before starting each new review so a push made during the run moves to the front. An `ERR` line is a fetch failure: retry that PR once, then leave it for the next run.
   - If `total` is absent, set `total` = the number of STALE candidates now (first run of this sweep). MOVED PRs don't count toward `total`, `done_count` or `left`; they are reviewed on top of the sweep.
   - No candidates: the sweep is done. Set `status` = `done`, `done_at` = now, `left` = 0, write the report (step 7) and release the lock.
   - Then hand back to the hourly rounds: load `RemoteTrigger` with ToolSearch (`select:RemoteTrigger`) and `update` the hourly routine `trig_013aGBK9j4GW4xb38FrVL3Yn` to `{"enabled": true}` and this sweep routine `trig_017tqeKSsVeXbyVYrJ8ex4qU` to `{"enabled": false}`. If the tool isn't available, say in the report that the user should disable the sweep routine and check the hourly one is enabled.
   - Stacks: review a stack as one unit, as routine.md says, and count each of its PRs.
5. **Review (§5 and routine.md):** treat every candidate as MOVED: a full re-review at its current head, with the re-review steps of agent-instructions.md (rebuild our open findings from GitHub first, so the posting script resolves only findings that are really gone). At most 2 review agents at a time, as in cloud-round.md.
   - Our own comments without a `pre-pr-review:finding` marker were posted by hand: treat them like another reviewer's threads. Don't repeat them as new findings (check the dry run's overlap warnings), and don't resolve or edit them.
   - Time budget: start no new review once 2 h 15 min have passed since `STARTED`; let running reviews finish and post. If a review is still running at 2 h 50 min, stop it, post nothing for that PR (it stays stale for the next run) and say so in the report.
6. **Progress:** after each posted review, `update` `state/sweep` (with `if_version`) to `done_count` += the PRs it covered, `left` = `total` − `done_count` (never below 0), `updated` = now. Then show it on the board: `ArtifactData get` `reports/latest`, put the progress line `**Sweep to <target short sha>:** <done_count> of <total> PRs re-reviewed, <left> left · updated <now>` as the report's first line (replacing an earlier `**Sweep to` line, keeping everything else), and `update` it with that `if_version`; on a refusal re-read and retry once. Write the same line once right after taking the lock, so the board shows the sweep has started. Before ending, run `sweep_candidates.py <target>` again and set `left` to the number of `STALE` lines it prints; if it prints no lines at all, mark the sweep done as in step 4.
7. **Finish (§6):** as written, except:
   - The report title is `# Sweep round · <STARTED>`, and its second line is the progress: `Sweep to <target short sha>: <done_count> of <total> PRs re-reviewed, <left> left` (or `Sweep complete` when done).
   - Leave `state/scan` as it is: a sweep doesn't change PR heads, and the hourly round needs its own last scan when it resumes.
   - Retrospective inputs and review-skill updates go to the board as cloud-round.md says, with the same filter.

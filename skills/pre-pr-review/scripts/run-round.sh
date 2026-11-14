#!/usr/bin/env bash
# Runs one unattended PR review round on this Mac (routine.md) and saves the report.
#
# Usage: skills/pre-pr-review/scripts/run-round.sh [extra instructions]
#   e.g. run-round.sh "only PR 1422"
# Report: $SP/reports/<timestamp>.md (also printed). Override any path below via the environment.
set -euo pipefail

# Keep the Mac from idle-sleeping for the whole round (the display may still turn off).
if [[ -z "${RUN_ROUND_AWAKE:-}" ]]; then
  export RUN_ROUND_AWAKE=1
  # -i blocks idle sleep; -s also blocks system sleep while on AC power (no effect on battery).
  exec caffeinate -is "$0" "$@"
fi

TOOLS="${TOOLS:-$(cd "$(dirname "$0")/../../.." && pwd)}"
REPO="${REPO:-$HOME/Dev/Git/ballerina-lang-go}"
UPSTREAM="${UPSTREAM:-pr730remote}"
SP="${SP:-/private/tmp/review-sp}"
JBALLERINA_SRC="${JBALLERINA_SRC:-$HOME/Dev/Git/ballerina-lang}"
CLAUDE="${CLAUDE:-$HOME/.local/bin/claude}"
export TOOLS REPO UPSTREAM SP JBALLERINA_SRC

# wrk and hyperfine: compiler-tools benchmark tests fail without them (CI installs both).
for cmd in "$CLAUDE" gh git go bal python3 wrk hyperfine; do
  command -v "$cmd" >/dev/null || { echo "missing: $cmd" >&2; exit 1; }
done
git -C "$REPO" remote get-url "$UPSTREAM" | grep -q 'ballerina-nutcracker/ballerina' \
  || { echo "$REPO remote $UPSTREAM is not ballerina-nutcracker/ballerina" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh is not logged in (gh auth login)" >&2; exit 1; }

# Per-round state lives in $SP (except reports/) and in refs/review/* and refs/pr-stack/* of the clone; findings are
# rebuilt from GitHub each round, so clear both before (a crashed round) and after every round.
# Resolve $SP (symlinks, ..) before trusting it with rm -rf: it must be a real dir under /private/tmp.
case "$SP" in *..*) echo "SP must not contain '..': $SP" >&2; exit 1 ;; esac
mkdir -p "$SP"
SP="$(cd "$SP" && pwd -P)"
case "$SP" in /private/tmp/?*) ;; *) echo "SP must be under /private/tmp: $SP" >&2; exit 1 ;; esac
export SP
cleanup() {
  git -C "$REPO" worktree list --porcelain | awk '/^worktree /{print $2}' | while read -r w; do
    case "$w" in "$SP"/wt/*|"${SP#/private}"/wt/*) git -C "$REPO" worktree remove --force "$w" || true ;; esac
  done
  git -C "$REPO" worktree prune
  git -C "$REPO" for-each-ref --format='delete %(refname)' refs/review/ refs/pr-stack/ | git -C "$REPO" update-ref --stdin
  [[ -d "$SP" ]] || return 0
  find "$SP" -mindepth 1 -maxdepth 1 ! -name reports -exec rm -rf {} +
  # Keep only the 10 newest saved reports (reports/latest.md in the repo has the last one, git the rest).
  if [[ -d "$SP/reports" ]]; then
    find "$SP/reports" -maxdepth 1 -type f -name '*.md' | sort -r | tail -n +11 | while read -r f; do rm -f "$f"; done
  fi
}
cleanup
trap cleanup EXIT

START="$(TZ=Asia/Colombo date '+%Y-%m-%d %H:%M')"

# Rounds normally run in the cloud (cloud-round.md); share their lock so the two never run at once.
LOCK=(python3 "$TOOLS/skills/pre-pr-review/scripts/round_lock.py")
"${LOCK[@]}" take "$START" "mac:$(hostname -s)" || { echo "another round holds reports/round.lock; not starting" >&2; exit 1; }
"${LOCK[@]}" heartbeat "$START"
on_exit() { "${LOCK[@]}" release "$START" >/dev/null 2>&1 || true; cleanup; }
trap on_exit EXIT

mkdir -p "$SP/review-out" "$SP/reports"
report="$SP/reports/$(TZ=Asia/Colombo date +%Y%m%d-%H%M).md"

prompt="Run one PR review round. Follow $TOOLS/skills/pre-pr-review/references/routine.md exactly.
REPO=$REPO TOOLS=$TOOLS UPSTREAM=$UPSTREAM SP=$SP JBALLERINA_SRC=$JBALLERINA_SRC
STARTED=$START Asia/Colombo
${1:+Extra instructions for this round: $1}"

cd "$TOOLS"
# In -p mode Claude Code kills background tasks 10 min after the last turn; the scan and
# review agents can take longer, so wait for them indefinitely.
export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0
"$CLAUDE" -p "$prompt" \
  --permission-mode auto \
  --add-dir "$REPO" "$SP" "$JBALLERINA_SRC" \
  --output-format text | tee "$report"

echo
echo "Report saved: $report"

# Keep a copy of the latest report in this repo (from the report heading on, without progress chatter).
# reports/latest.md is tracked; the user commits it after each round.
mkdir -p "$TOOLS/reports"
if grep -q '^# ' "$report"; then
  sed -n '/^# /,$p' "$report" > "$TOOLS/reports/latest.md"
  echo "Report copied: $TOOLS/reports/latest.md"
else
  echo "No report heading in $report (round ended early); reports/latest.md left unchanged." >&2
fi

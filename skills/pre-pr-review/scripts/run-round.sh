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

for cmd in "$CLAUDE" gh git go bal python3; do
  command -v "$cmd" >/dev/null || { echo "missing: $cmd" >&2; exit 1; }
done
git -C "$REPO" remote get-url "$UPSTREAM" | grep -q 'ballerina-nutcracker/ballerina' \
  || { echo "$REPO remote $UPSTREAM is not ballerina-nutcracker/ballerina" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh is not logged in (gh auth login)" >&2; exit 1; }

mkdir -p "$SP/review-out" "$SP/reports"
START="$(TZ=Asia/Colombo date '+%Y-%m-%d %H:%M')"
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

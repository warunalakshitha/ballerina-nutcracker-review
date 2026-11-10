# ballerina-nutcracker-review

PR review tooling for [ballerina-nutcracker/ballerina](https://github.com/ballerina-nutcracker/ballerina), used by the scheduled Claude Code cloud routine and by local review rounds.

- `skills/pr-review/`: the review checklist (`SKILL.md`) and companion checklists.
- `skills/pre-pr-review/`: agent rules (`references/agent-instructions.md`), the round procedure (`references/routine.md`), the posting format and scripts.
- `skills/pre-pr-review/scripts/ready_table.py`: merge-ready PR table (REST only; needs `gh` logged in).
- `skills/pre-pr-review/scripts/scan_prs.py`: PRs with commits since our last review.

Repo rules (AGENTS.md, docs, the repo's own skills) are read from ballerina-nutcracker/ballerina `main` at review time; only the review skill lives here.

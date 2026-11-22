---
name: playground-review
description: >-
  Reviews Ballerina Playground PRs (ballerina-nutcracker/playground): fit with
  the current architecture, the design system (tokens, colours, icons, shadcn
  primitives), user experience in the running app (mobile, loading and failure
  states, accessibility), WASM runtime parity with native `bal`, examples and
  their golden output, and tests (bun, Go WASM, Playwright). Run by hand, one
  PR or all open non-draft PRs. Use when the user pastes a
  github.com/ballerina-nutcracker/playground PR URL or asks to review
  playground PRs.
---

# Ballerina Playground PR review

Manual only: no routine, no board. Few playground PRs come in, so the user starts a review when one is ready. Findings are shown in chat; post to GitHub only when the user asks.

The rules below come from the human and agent reviews on playground PRs #1–#148 ([references/past-reviews.md](references/past-reviews.md) lists them with their PRs, and the decisions authors already defended). The look and feel rules are in [references/design-system.md](references/design-system.md).

## Setup

| Role | Path |
|------|------|
| Playground clone | `$PG`, a clone of `ballerina-nutcracker/playground` (ask for the path if unset; otherwise clone into a temp dir) |
| Review tooling | `$TOOLS`, this repo |
| Native Ballerina | `bal` on PATH, for parity checks |

Read `AGENTS.md` in the playground at the PR's base before judging: it holds the package table, the Bun-only rule, the `components/ui/` rule and the example workflow. Prerequisites: Bun 1.3.10, the Go version in `packages/wasm/go.mod`.

## Picking PRs

```bash
gh pr list -R ballerina-nutcracker/playground --state open --draft=false \
  --json number,title,author,headRefOid,updatedAt
```

Skip drafts and PRs whose latest 🤖 summary already reviewed the current head (`🤖 PR review summary` comment naming that SHA). For a stack (one PR's base is another's branch), use `$TOOLS/skills/pre-pr-review/scripts/stack.py <N> --repo ballerina-nutcracker/playground --json` and review it as a unit at the tip, as #137–#140 were.

## Workflow

```
Playground review progress:
- [ ] 0. Mergeability gate
- [ ] 1. Metadata, checkout, prior reviews
- [ ] 2. What changes for the user
- [ ] 3. Commits and PR description
- [ ] 4. Architecture fit and scope
- [ ] 5. Design system (check_playground_ui.py)
- [ ] 6. UX in the running app
- [ ] 7. WASM runtime parity (packages/wasm)
- [ ] 8. Examples and golden output
- [ ] 9. Tests
- [ ] 10. Security and privacy
- [ ] 11. Validate (lint, tests, build, e2e, wasm size)
- [ ] 12. Report, then post if asked
```

### 0. Mergeability gate

Same as `skills/pr-review/SKILL.md` step 0: if the PR conflicts with its base, report only the conflicting files and stop.

### 1. Metadata, checkout, prior reviews

```bash
R=ballerina-nutcracker/playground
gh pr view "$PR" -R $R --json title,body,author,baseRefName,headRefOid,commits,files,isDraft
gh pr diff "$PR" -R $R
gh api "repos/$R/pulls/$PR/comments" --paginate
gh api "repos/$R/issues/$PR/comments" --paginate
gh api "repos/$R/pulls/$PR/reviews" --paginate
cd "$PG" && git fetch origin "pull/$PR/head:pr$PR" && git worktree add "/tmp/pg-$PR" "pr$PR"
cd "/tmp/pg-$PR" && bun install
```

CodeRabbit reviews every playground PR. Read its threads and the humans' before hunting: don't repeat a raised point. Note it in the summary only when it is still open and you confirmed it (as #140 did: "Still open (raised by coderabbitai): …").

### 2. What changes for the user

Write this first, 2–4 sentences: what the user sees or can do now, where in the UI, and for runtime PRs a short `.bal` program that shows it. Then point-form: which layers changed (see step 4), tests added.

A PR that changes the UI needs a screenshot or GIF in its description (asked on #69, #131). If the description describes UI that the code no longer matches, say so (#131: body said `Loading N%`, the button showed a ring).

### 3. Commits and PR description

Same commit review as `skills/pr-review/SKILL.md` step 3 (rules 1–5), with one difference: the playground has no commit-lint CI (`ci.yml` runs only Biome), so we validate Conventional Commits ourselves. In the worktree run:

```bash
python3 $TOOLS/skills/pr-review/scripts/check_commit_trailers.py origin/<base> \
  --pr "$PR" --repo ballerina-nutcracker/playground --conventional --ai-only
```

It runs nutcracker's `validate_commits.py` (fetched from `ballerina-nutcracker/ballerina` main) on the PR title and every non-merge commit subject, and also checks commit bodies, author/committer, GitHub author and the PR description. Every commit finding is PR-level (`"anchor": "pr"`), reported with SHA + subject. AI authorship is 🔴 **Important** and blocks merge; the rest are 📝 **Commit/PR** (`"severity": "commit"`), as in `github-posting.md`:

- **Conventional Commits** on every commit subject and the PR title (agreed on #87): `<type>(<scope>): <description>`, lowercase, ≤ 72 chars (`SUBJECT`, `PR-TITLE`). Leftover `fixup!` / `squash!` commits fail too (#136).
- **No AI authorship anywhere** (#105): no co-author trailer naming an AI tool, no `Generated-by:` / `Assisted-by:` / "Generated with Claude Code" line in a commit message, no AI tool or bot as git author, committer or GitHub author (`COAUTHOR`, `AI-TRAIL`, `AI-AUTHOR`, `AI-LOGIN`), and no AI attribution line in the PR description (`PR-BODY`; #105's body ended with "🤖 Generated with [Claude Code]").
- **Human authors other than the PR opener are fine** (`--ai-only`): a sync PR like #151 carries teammates' commits, and a teammate may push to or co-author a PR. Only AI tools (Claude, Cursor, Copilot, Codex, …) are rejected.
- **Atomic commits, no unsquashed corrections** (pr-review rule 2): a commit that fixes, narrows or rewords an earlier commit on the same PR (e.g. `fix: address review comments`) should be squashed into it; name the target SHA. No `go build` rebase check here: run `bun run lint && bun run build` per commit with `git rebase -x` only when the PR has several commits touching code.
- **Type matches behaviour** (pr-review rule 5): a `refactor` / `style` / `chore` that changes what the user sees or what the runtime does is `fix` / `feat`.
- The repo's `pull_request_template.md` is the generic WSO2 one; don't raise missing template sections or run `check_pr_body.py`. Do ask for the issue link when the PR fixes a reported problem.

### 4. Architecture fit and scope

Map each changed file to its layer and check it sits where the rest of that kind of code sits:

| Layer | Where | Fits when |
|-------|-------|-----------|
| UI | `apps/web/src/components/`, routes in `routes/` | composes `components/ui/` primitives; feature folders like `bal-bot/` for a large view |
| State | `apps/web/src/stores/` (zustand + immer) | one store per concern; derived values computed, not stored twice |
| Runtime bridge | `providers/ballerina-provider.tsx`, `workers/` (Comlink) | the WASM runs in the worker; the UI never calls `window.run` directly |
| Files | `apps/web/src/lib/fs/` (`LayeredFS`, `SnapshotFS`, `LocalStorageFS`, `EphemeralFS`) | goes through `fs-provider` / `file-tree-store`, not raw `localStorage` |
| WASM | `packages/wasm/*_wasm.go` (PAL, bridge FS, HTTP, listeners, signals) | implements the nutcracker PAL; pinned in `go.mod` |
| Agent view | `packages/compiler`, `packages/workspace`, `packages/browser-workspace` | only reached from the agent view |
| Examples | `examples/NN-name/` + `e2e/fixtures/examples/` | see step 8 |

Raise:

- a hand-rolled version of something the repo or a dependency already gives (#101: `useDefaultLayout` instead of manual `localStorage` layout code; #136: hand-rolled popover instead of `ui/dropdown-menu`).
- edits under `apps/web/src/components/ui/` (AGENTS.md). A **Verify**, not a defect: the authors keep shadcn's own patterns there (#83, #86, #87, #101, #108) — ask only when the edit changes behaviour for every user of the primitive (#105 restyled `ui/button`).
- generated files edited by hand: `apps/web/src/assets/examples.json`, `routeTree.gen.ts`, `packages/browser-workspace/src/generated/`.
- a non-Bun lockfile or command.
- a new package or top-level folder not added to the `AGENTS.md` structure table (#136).
- unrelated work bundled in: an interpreter bump inside a feature PR (#131), CI/hook changes inside a feature (#136). Ask for a separate PR.
- `ballerina.wasm` size growth: build base and head and report the MB and gzipped delta in the summary (#131, #137). A new wasm or large asset fetched at startup is a **Verify**.
- dead files: unreferenced assets, testdata nothing reads, duplicated fixtures, `.gitkeep` beside real files (#136).

### 5. Design system

```bash
python3 $TOOLS/skills/playground-review/scripts/check_playground_ui.py origin/<base>
```

It lists raw colours, Tailwind palette colours, native controls, glyph icons, other icon libraries, font overrides, `console.log`, `ui/` edits, generated-file edits and non-Bun lockfiles on the PR's added lines. Each line is a lead: read it, then raise one finding per kind (e.g. "`bal-bot.css` has 71 hard-coded colours", not 71 comments). Then check by eye what the script can't, per [references/design-system.md](references/design-system.md): spacing and sizes match the neighbouring components, UI wording matches existing names (Local Space, Try It, agent view — #64, #136), and any change to the brand or primary colour is a maintainer call (#105).

### 6. UX in the running app

Run it: `bun run dev` (or `bun run build && bun run preview`) and drive it with Playwright or by hand. Check, for the parts the PR touches:

- **Phone width.** 390×844: nothing wider than `main` (`scrollWidth`), toolbar buttons don't overflow (#110, #136). `useIsMobile` switches at 768px.
- **Loading and failure states.** Every async action shows progress and a failure that stays until the user can read it; a failed load never leaves a spinner forever or blanks the app (#131 run button, #136 chunk load). Errors reach the user through a toast or the output pane, not only the console; silent no-ops are findings.
- **Stale async.** After each `await`, the code rechecks that the file, request or component is still current before writing state (#131 diagnostics generation; CodeRabbit on #39, #42, #86).
- **Editor and files.** A program's writes to the open file reach the editor, and unsaved edits aren't overwritten silently (#140). Renames/moves keep the active file and expanded folders right.
- **Accessibility.** Icon-only buttons have `aria-label`; dialogs trap focus and close on Escape; inputs have labels, not only placeholders; text contrast ≥ 4.5:1, including disabled labels that carry information (#131).
- **URLs.** Navigation keeps existing search params (`?sidebar=collapsed`, #107); shared links made before the PR still open (#73).
- **Output pane.** Long output scrolls without moving the header (#116); auto-scroll doesn't fight the user (#62, #63).
- **Dark mode** isn't reachable from the UI: don't test it, but new styles must use tokens so it keeps working (#136).

Put the viewport, steps and what you saw in the finding. Attach nothing you didn't observe.

### 7. WASM runtime parity (`packages/wasm`)

For a PAL, HTTP, file or listener change, write a short Ballerina program, run it with native `bal run` and in the playground, and put both outputs in the finding as `native bal:` / `Playground:` (#139, #140). Check:

- error messages match native wording where the PAL builds them (#139 "directory not empty").
- it works in a Local Space project, not only in an example run under `/tmp` (#139).
- bounded queues and buffers don't drop events native delivers (#140 watch queue).
- unsupported operations panic with `<Op> is not supported in Playground` (agreed on #75); don't ask for an error return instead.
- Go: `gofmt -l packages/wasm` clean (#131); new tests call `t.Parallel()` when they share no state (#127, #140); tests run with `GOOS=js GOARCH=wasm` (`bun run --filter @playground/wasm test`).

### 8. Examples and golden output

For changes in `examples/`:

- golden output refreshed with `bun test:e2e:update-examples`; service requests in `e2e/tests/examples.spec.ts` updated (AGENTS.md).
- volatile output (timestamps, versions, counts from live services) goes through the placeholders in `e2e/helpers/example-output.ts`, and regeneration doesn't bake it back in (#122).
- client calls set a timeout below the e2e wait (#122).
- `io:println` in `main` examples, `log` in service examples (connector team convention, #126); follow the Swan Lake BBE style (#92); a POST returns the created resource (#92).
- only features Nutcracker supports today; if an idiomatic form isn't supported, that's not a finding (#122).
- a new default example updates `DEFAULT_FILE` in `file-route-sync.tsx`.

### 9. Tests

| Change | Expected test |
|--------|---------------|
| store, lib, worker client logic | `bun test` in `apps/web/tests` (happy-dom) |
| WASM / PAL behaviour | Go test in `packages/wasm` or a `.bal` fixture in `apps/web/tests/fixtures/` run by `ballerina.test.ts` |
| visible behaviour, flows across components | Playwright spec in `e2e/tests/`, using `e2e/helpers/playground.ts` |
| mobile layout | a spec at 390px that opens the view and checks overflow, not just the toolbar (#136) |
| example change | golden in `e2e/fixtures/examples/` |

Ask for the missing test on the changed line it belongs to. A test that asserts a state users can't reach (dark mode, #136) or duplicates another case byte for byte is a Nit. Fixture tests should cover the variants of the API they claim (#75 asked for every `io:file*` pair).

### 10. Security and privacy

- Model or user-supplied Markdown never fetches remote images or runs HTML (#136).
- Text about where data goes is accurate: code and chat sent to a provider must say so (#136).
- API keys stay in memory; not in `localStorage`, logs, URLs or test snapshots.
- Share payloads and persisted `localStorage` data are validated before use (names, paths, schema).
- No secrets, tokens or personal data in fixtures.

### 11. Validate

```bash
bun run lint            # Biome; CI fails on it
bun run test            # all workspaces (Go WASM tests included)
bun run build
bunx playwright install chromium && bun run test:e2e
```

Report failures as findings only after checking they also fail for a reason in this PR (run the same on the base when unsure). For wasm size: `ls -l packages/wasm/dist/ballerina.wasm` and `gzip -c … | wc -c` on base and head.

### 12. Report, then post if asked

In chat: the "what changes" block, then findings by severity — 🔴 **Important** (confirmed defect), 🟡 **Verify** (a question or unconfirmed suspicion), 🔵 **Nit** — each with file:line, ≤ 3 sentences, and a repro (`.bal` program, viewport and steps, or a test) or a `suggestion`. Then PR-level notes (wasm size, scope, screenshots) and what you checked.

To post, write `findings.json` (in a temp dir) per `skills/pre-pr-review/references/github-posting.md` with `"repo": "ballerina-nutcracker/playground"`, label outputs `native bal` / `Playground`, set `summary.checked` to what you ran (e.g. `mobile 390px`, `native bal parity`, `e2e 29/29`), then:

```bash
python3 $TOOLS/skills/pre-pr-review/scripts/post_review.py findings.json          # dry run
python3 $TOOLS/skills/pre-pr-review/scripts/post_review.py findings.json --post   # only when the user says so
```

Reruns and withdrawals follow `github-posting.md` (edit in place, "✅ No longer reported", "🤖 Withdrawn: <reason>").

## Proportion

Findings must be worth a developer's time. Don't raise:

- anything in the "decided" list of [references/past-reviews.md](references/past-reviews.md) unless the code changed what made it acceptable.
- style Biome already enforces.
- refactors of code the PR didn't touch; file an issue instead if it matters.

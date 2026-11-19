# Lessons from past playground reviews

Mined from human, CodeRabbit and 🤖 reviews on ballerina-nutcracker/playground #1–#148 (2026-11-19). Each line is a check that found something real, with the PR where it did. Add to this when a review misses something a human or CodeRabbit catches, after proving the new rule (retrospective proof runs plus a clean-PR control).

## Checks that found real problems

| Area | Check | PRs |
|------|-------|-----|
| Design | hard-coded colours instead of tokens | #136 |
| Design | native `<select>`, hand-rolled popover, Unicode glyph icons | #136 |
| Design | brand colour on one button clashes with black primary | #105 |
| Design | UI text still uses an old name after a rename | #136, #64 |
| UX | view wider than a 390px screen | #136, #110 |
| UX | failed wasm/chunk load: spinner forever or blank app | #131, #136 |
| UX | failure reason only in a toast that auto-dismisses | #131 |
| UX | icon-only button with no accessible name | #34, #80, #87 |
| UX | header scrolls away with output | #116 |
| UX | navigation drops existing search params | #107 |
| UX | program writes to the open file never reach the editor | #140 |
| Async | stale result published after a newer request | #131 |
| Async | cancellation not rechecked after each await | #39, #42, #86 |
| Async | worker setup failure never rejects `whenReady()` | #131 |
| Errors | failure turned into a silent no-op (share, fork, stop) | #16, #17, #80 |
| Runtime | `createTemp()` fails outside `/tmp` example runs | #139 |
| Runtime | PAL error text differs from native | #139 |
| Runtime | bounded watch queue drops events native delivers | #140 |
| Runtime | literal `\\n` in a template string | #140 |
| Runtime | two dispatch paths resolve hosts differently | #86 |
| Deps | interpreter pinned to an untagged commit via `replace` | #131, #80 |
| Deps | Go version bumped in `go.mod` but not in CI/deploy | #140 |
| Scope | interpreter bump hidden in a feature PR; wasm +32% | #131 |
| Scope | 92% of a PR is copied testdata; dead fixtures | #136 |
| Examples | regenerating goldens bakes volatile values back in | #122 |
| Examples | header says "Top 5" but list can be shorter | #122 |
| Examples | no client timeout below the e2e wait | #122 |
| Tests | mobile test never opens the view it guards | #136 |
| Tests | test asserts dark mode users can't reach | #136 |
| Tests | Go tests not parallel | #127, #140 |
| Tests | fixture covers one API of a family | #75 |
| Security | model Markdown images fetched without a click | #136 |
| Privacy | disclaimer says data stays in the browser when it goes to a provider | #136 |
| Commits | non-conventional subject, AI co-author, leftover `fixup!` | #87, #105, #136 |
| Docs | AGENTS.md package table not updated | #136 |
| Docs | scripts without a header saying what they do | #21, #30 |

## Decided: don't raise again

Authors answered these with a reason the reviewers accepted. Raise again only if the code changed what made it acceptable.

- `components/ui/` files keep shadcn's own patterns (orientation classes, tabs props) (#83, #86, #87, #101, #108).
- Streaming file writes are buffered in WASM memory and flushed on `Close()` (#124).
- Unsupported OS/process PAL calls panic with "… is not supported in Playground" rather than returning errors (#75).
- Copying a directory into an existing one merges, as native PAL does (#139).
- Runtime file-sync failures are a stderr diagnostic only (#139); concurrent-change merging is deferred (#139).
- `https://localhost` is served by the in-memory handler without TLS, with a comment (#86).
- `dispatchHttpRequest` (Try It) can't apply `http:Client` response limits (#86).
- The playground offers graceful stop only; the WASM API keeps both (#80).
- The share e2e test uses a fixed encoded URL so old links keep working (#73).
- `routeTree.gen.ts` and `bun.lock` are committed (#13).
- Two hotkey registrations (editor scope and global) are intentional (#35).
- `main` examples print with `io`, service examples log with `log` (#126).
- Example code uses only what Nutcracker supports, even when a more idiomatic form exists (#122).
- The `aws` query in the HTTP client example always returns ≥ 5 packages over 100 pulls (#122).

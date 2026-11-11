# Review round 2026-11-11 13:58 +0530 (Asia/Colombo)

`pr730remote/main` is at `b46b10336`. `gh`, `bal`, `go` and `golangci-lint` were all available, so nothing was skipped for missing tools.

## Merge-ready (0)

| PR | Title | Author | Approval | Reviewed |
|---|---|---|---|---|
| — | no merge-ready PRs | | | |

## Not ready (62)

open findings: 23 · CI failed: 6 · CI pending: 1 · conflicting: 23 · not reviewed at current head: 5 · mergeability unknown: 4

| PR | Title | Author | Why |
|---|---|---|---|
| [#925](https://github.com/ballerina-nutcracker/ballerina/pull/925) | feat(semantics): use record defaults in constant mappings | heshanpadmasiri | open findings |
| [#926](https://github.com/ballerina-nutcracker/ballerina/pull/926) | fix(semantics): analyze constant type descriptors separately | heshanpadmasiri | open findings |
| [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) | perf(projects): fix parallelization issue | azinneera | open findings |
| [#1188](https://github.com/ballerina-nutcracker/ballerina/pull/1188) | fix(nodebuilder): report '_' used as identifier as syntax er | heshanpadmasiri | open findings |
| [#1193](https://github.com/ballerina-nutcracker/ballerina/pull/1193) | fix(semantics): evaluate computed mapping keys as expression | heshanpadmasiri | open findings |
| [#1201](https://github.com/ballerina-nutcracker/ballerina/pull/1201) | refactor: align conditional type narrowing with the spec | heshanpadmasiri | open findings |
| [#1208](https://github.com/ballerina-nutcracker/ballerina/pull/1208) | fix(semantics): reject out-of-range int literals | heshanpadmasiri | open findings |
| [#1213](https://github.com/ballerina-nutcracker/ballerina/pull/1213) | fix(semantics): apply detail record defaults in error constr | heshanpadmasiri | open findings |
| [#1377](https://github.com/ballerina-nutcracker/ballerina/pull/1377) | fix(projects): parse module documents into a slice indexed b | azinneera | open findings |
| [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) | feat(runtime): expose annotations of nested field types | warunalakshitha | open findings |
| [#1480](https://github.com/ballerina-nutcracker/ballerina/pull/1480) | feat(workflow): bundle ballerina/workflow with an in-memory  | hasithaa | open findings |
| [#1517](https://github.com/ballerina-nutcracker/ballerina/pull/1517) | fix: reject non-private non-isolated fields in isolated obje | heshanpadmasiri | open findings |
| [#1536](https://github.com/ballerina-nutcracker/ballerina/pull/1536) | feat(ls): add signature help support | nipunayf | open findings |
| [#1544](https://github.com/ballerina-nutcracker/ballerina/pull/1544) | ci(perf): replace PR benchmark gates with nightly comparison | heshanpadmasiri | open findings |
| [#1567](https://github.com/ballerina-nutcracker/ballerina/pull/1567) | feat(ls): add initial completion support | nipunayf | open findings |
| [#1601](https://github.com/ballerina-nutcracker/ballerina/pull/1601) | feat(cli): add --dump-desugared-ast flag | heshanpadmasiri | open findings |
| [#1606](https://github.com/ballerina-nutcracker/ballerina/pull/1606) | docs(agents): limit subset doc updates to support and restri | heshanpadmasiri | open findings |
| [#1608](https://github.com/ballerina-nutcracker/ballerina/pull/1608) | refactor(diagnostics): remove unused diagnostic severities | heshanpadmasiri | open findings |
| [#1609](https://github.com/ballerina-nutcracker/ballerina/pull/1609) | chore(lint): make enum switches exhaustive | heshanpadmasiri | open findings |
| [#1612](https://github.com/ballerina-nutcracker/ballerina/pull/1612) | chore(lint): enforce module lint tiers | heshanpadmasiri | open findings |
| [#1623](https://github.com/ballerina-nutcracker/ballerina/pull/1623) | ci(nightly): add nightly flake sniffer and actionlint | heshanpadmasiri | open findings |
| [#1624](https://github.com/ballerina-nutcracker/ballerina/pull/1624) | ci(release): publish an automatic patch release every night | heshanpadmasiri | open findings |
| [#1630](https://github.com/ballerina-nutcracker/ballerina/pull/1630) | ci: report references to closed issues nightly | heshanpadmasiri | open findings |
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title |
| [#1254](https://github.com/ballerina-nutcracker/ballerina/pull/1254) | test(corpus): cover error-typed wildcards in query clauses | heshanpadmasiri | CI failed: Validate PR Title, Validate Commit Messages |
| [#1255](https://github.com/ballerina-nutcracker/ballerina/pull/1255) | fix(nodebuilder): allow start actions in type casts and quer | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title, Validate PR Title |
| [#1495](https://github.com/ballerina-nutcracker/ballerina/pull/1495) | test: clean up constant folding skip list | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title, Validate PR Title |
| [#1610](https://github.com/ballerina-nutcracker/ballerina/pull/1610) | chore(lint): make expression switches exhaustive | heshanpadmasiri | CI failed: Windows Native Build, Validate PR Title, Validate Commit Messages |
| [#1611](https://github.com/ballerina-nutcracker/ballerina/pull/1611) | refactor(nodes): keep shared base types private | heshanpadmasiri | CI failed: Ubuntu WASM Build, Windows Native Build, Ubuntu Native Build |
| [#1607](https://github.com/ballerina-nutcracker/ballerina/pull/1607) | chore(lint): enable modernize and modernize Go code | heshanpadmasiri | CI pending (5) |
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | conflicting |
| [#701](https://github.com/ballerina-nutcracker/ballerina/pull/701) | feat(tcp): port ballerina/tcp standard library | TharmiganK | conflicting |
| [#921](https://github.com/ballerina-nutcracker/ballerina/pull/921) | feat: support compiler plugins | heshanpadmasiri | conflicting |
| [#1053](https://github.com/ballerina-nutcracker/ballerina/pull/1053) | fix(types): treat readonly class values as readonly | heshanpadmasiri | conflicting |
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | conflicting |
| [#1189](https://github.com/ballerina-nutcracker/ballerina/pull/1189) | feat(worker): support worker message passing | heshanpadmasiri | conflicting |
| [#1233](https://github.com/ballerina-nutcracker/ballerina/pull/1233) | fix(semantics): enforce visibility of object member access | heshanpadmasiri | conflicting |
| [#1263](https://github.com/ballerina-nutcracker/ballerina/pull/1263) | feat(compiler): add warnings and report unused variables as  | heshanpadmasiri | conflicting |
| [#1390](https://github.com/ballerina-nutcracker/ballerina/pull/1390) | feat(stdlib): add `ballerina/data.csv` standard library | TharmiganK | conflicting |
| [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) | feat(stdlib): add `ballerina/data.jsondata` standard library | TharmiganK | conflicting |
| [#1411](https://github.com/ballerina-nutcracker/ballerina/pull/1411) | feat(stdlib): add byte-stream and Server-Sent Event support  | TharmiganK | conflicting |
| [#1415](https://github.com/ballerina-nutcracker/ballerina/pull/1415) | feat(data.xmldata): add `ballerina/data.xmldata` standard li | TharmiganK | conflicting |
| [#1422](https://github.com/ballerina-nutcracker/ballerina/pull/1422) | feat(stdlib): add `ballerina/data.yaml` standard library | TharmiganK | conflicting |
| [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) | fix(semantics): carry annotations on inferred typedesc args | warunalakshitha | conflicting |
| [#1437](https://github.com/ballerina-nutcracker/ballerina/pull/1437) | feat(stdlib): add `ballerina/cache` standard library | TharmiganK | conflicting |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sor | warunalakshitha | conflicting |
| [#1446](https://github.com/ballerina-nutcracker/ballerina/pull/1446) | feat(stdlib): add `ballerina/ftp` standard library | TharmiganK | conflicting |
| [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) | fix(http): send http:Request message headers and type client | TharmiganK | conflicting |
| [#1476](https://github.com/ballerina-nutcracker/ballerina/pull/1476) | fix(parser): normalize source newlines and BOM | snelusha | conflicting |
| [#1481](https://github.com/ballerina-nutcracker/ballerina/pull/1481) | fix(semantics): reject writes to final object fields outside | heshanpadmasiri | conflicting |
| [#1508](https://github.com/ballerina-nutcracker/ballerina/pull/1508) | feat: introduce the test framework | azinneera | conflicting |
| [#1600](https://github.com/ballerina-nutcracker/ballerina/pull/1600) | fix(desugar): register each module listener object once | heshanpadmasiri | conflicting |
| [#1613](https://github.com/ballerina-nutcracker/ballerina/pull/1613) | chore(lint): require production use of functions in strict m | heshanpadmasiri | conflicting |
| [#1221](https://github.com/ballerina-nutcracker/ballerina/pull/1221) | fix(semantics): check named worker captures in isolated func | heshanpadmasiri | not reviewed at current head |
| [#1238](https://github.com/ballerina-nutcracker/ballerina/pull/1238) | feat(worker): support fork statements | heshanpadmasiri | not reviewed at current head |
| [#1625](https://github.com/ballerina-nutcracker/ballerina/pull/1625) | ci: check stdlib coverage docs before push | TharmiganK | not reviewed at current head |
| [#1626](https://github.com/ballerina-nutcracker/ballerina/pull/1626) | fix(desugar): check service on-clause variables for errors | heshanpadmasiri | not reviewed at current head |
| [#1631](https://github.com/ballerina-nutcracker/ballerina/pull/1631) | fix(analysis): require isolated values in isolated object fi | heshanpadmasiri | not reviewed at current head |
| [#1237](https://github.com/ballerina-nutcracker/ballerina/pull/1237) | perf(cfg): bitset-backed state for uninit analysis | heshanpadmasiri | mergeability unknown |
| [#1584](https://github.com/ballerina-nutcracker/ballerina/pull/1584) | ci: check lang library coverage docs before push | heshanpadmasiri | mergeability unknown |
| [#1597](https://github.com/ballerina-nutcracker/ballerina/pull/1597) | fix(semantics): reject undeclared detail args in error const | heshanpadmasiri | mergeability unknown |
| [#1614](https://github.com/ballerina-nutcracker/ballerina/pull/1614) | chore(lint): enforce shallow declaration checks and fix find | heshanpadmasiri | mergeability unknown |

## This round

I reviewed four PRs and posted all four reviews; none failed to post.

| PR | Verdict | New Important/Verify findings | Summary |
|---|---|---|---|
| #1630 (new) | Ready except approval (3 Nits) | — | [comment](https://github.com/ballerina-nutcracker/ballerina/pull/1630#issuecomment-6791256159) |
| #985 (moved) | Not ready: 3 PR-level Nits (unsquashed review-fix commits, PR body describes reverted changes, `perf` title on a PR that changes diagnostics). The 3 earlier threads are fixed and were resolved. | — | [comment](https://github.com/ballerina-nutcracker/ballerina/pull/985#issuecomment-5874531843) |
| #925 (moved, stack base) | Not ready | **Verify** `constant_evaluator.go:410`: a const that leaves out a field whose default is an XML template or a computed-key mapping now reports "not a constant expression" instead of "unimplemented". The spec says both defaults are constant expressions. A second check reproduced it. | [comment](https://github.com/ballerina-nutcracker/ballerina/pull/925#issuecomment-5882334998) |
| #926 (moved, stack tip) | Not ready: the `fix` title on a tests-only PR is still open. This push was only a rebase, so I refreshed the summary and didn't re-review it. | — | [comment](https://github.com/ballerina-nutcracker/ballerina/pull/926#issuecomment-5874489239) |

The earlier Important finding on #925 (a spread may supply a runtime default) is now fixed.

## Skipped
- **Conflict with main** (no review, no comment): #1481, #1438, #1263, #1233, #1165, #921.
- **Stack 1607→1614 plus #1626 and #1631:** #1612 is the highest PR in the stack that still merges cleanly, and it was already reviewed at its current head. #1613 conflicts, so #1613, #1614, #1626 and #1631 were skipped.
- **Stack 1584→1625:** #1625 conflicts.
- **Stack 1189→1221→1238:** the base #1189 conflicts.
- **Not checked:** none.

## Filed issues
None. The #985 agent saw a possible stage-stop masking case, where `int a = "x"; string s = 1;` reports only an unused variable. It was not checked against the spec, so I didn't file it. It happens on main as well as on the PR.

## Review-skill updates (proposed, not applied)
- **From #1630 (adds a nightly job that reports links to closed issues):** in pr-review SKILL.md, flag a PR that adds a link to a ballerina-nutcracker issue that is already closed (TODO, skip list, workaround or test comment). The new nightly job would report it as stale after merge. The exception is a link to an `#issuecomment-` anchor.
- **From #985 (AGENTS.md now says stages 1–2 also run concurrently and BIR generation is pipelined per module):** in the "Data races" section of SKILL.md, change "stages 5–9 running concurrently across modules" to "stages 1–2 and 5–10 running concurrently across modules (BIR pipelined per module; `AGENTS.md`)".

## Notes
- **Flaky test:** `TestLibIntegration/lib/subset3/task-listener2-v.bal` failed once on #925 and passed when rerun alone.
- **Stale threads on #985:** three unresolved threads from heshanpadmasiri look stale, because the author dropped those changes and moved them to #1363.

All review worktrees were removed.

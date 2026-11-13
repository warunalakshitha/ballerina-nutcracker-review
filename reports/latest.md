# Review round · 2026-11-13 12:08 Asia/Colombo

`pr730remote/main` is at `d69c341a5`. The round ended at 12:31. No tooling was missing: `gh`, `bal` and `golangci-lint` were all available.

**Open PRs: 68** · merge-ready: 4 · waiting for CI: 0 · not ready: 61 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 0

## Merge-ready (4)

| PR | Title | Author | Approval | Reviewed |
|---|---|---|---|---|
| [#701](https://github.com/ballerina-nutcracker/ballerina/pull/701) | feat(tcp): port ballerina/tcp standard library | TharmiganK | review required | `c1b5afb31` |
| [#1415](https://github.com/ballerina-nutcracker/ballerina/pull/1415) | feat(data.xmldata): add `ballerina/data.xmldata` standard library | TharmiganK | review required | `530706e70` |
| [#1437](https://github.com/ballerina-nutcracker/ballerina/pull/1437) | feat(stdlib): add `ballerina/cache` standard library | TharmiganK | review required | `b2d2ea24e` |
| [#1446](https://github.com/ballerina-nutcracker/ballerina/pull/1446) | feat(stdlib): add `ballerina/ftp` standard library | TharmiganK | review required | `a5fab9f5c` |

## Waiting for CI (0)

0 findings, no conflicts, reviewed at the current head; merge-ready once CI passes.

| PR | Title | Author | Approval | CI |
|---|---|---|---|---|
| — | none | | | |

## Not ready (61)

open findings: 36 · CI failed: 13 · conflicting: 9 · stacked on conflicting: 2 · base already merged: 1

| PR | Title | Author | Why |
|---|---|---|---|
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | conflicting |
| [#925](https://github.com/ballerina-nutcracker/ballerina/pull/925) | feat(semantics): use record defaults in constant mappings | heshanpadmasiri | open findings: 1 Verify, 2 Nits |
| [#926](https://github.com/ballerina-nutcracker/ballerina/pull/926) | fix(semantics): analyze constant type descriptors separately | heshanpadmasiri | open findings: 1 Nit |
| [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) | perf(projects): fix parallelization issue | azinneera | open findings: 1 Important, 7 Nits |
| [#1053](https://github.com/ballerina-nutcracker/ballerina/pull/1053) | fix(types): treat readonly class values as readonly | heshanpadmasiri | conflicting |
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title |
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | CI failed: Validate PR Title |
| [#1188](https://github.com/ballerina-nutcracker/ballerina/pull/1188) | fix(nodebuilder): report '_' used as identifier as syntax er | heshanpadmasiri | open findings: 1 Important, 1 Nit |
| [#1189](https://github.com/ballerina-nutcracker/ballerina/pull/1189) | feat(worker): support worker message passing | heshanpadmasiri | conflicting |
| [#1193](https://github.com/ballerina-nutcracker/ballerina/pull/1193) | fix(semantics): evaluate computed mapping keys as expression | heshanpadmasiri | open findings: 6 Nits |
| [#1201](https://github.com/ballerina-nutcracker/ballerina/pull/1201) | refactor: align conditional type narrowing with the spec | heshanpadmasiri | open findings: 1 Nit |
| [#1208](https://github.com/ballerina-nutcracker/ballerina/pull/1208) | fix(semantics): reject out-of-range int literals | heshanpadmasiri | open findings: 2 Nits |
| [#1213](https://github.com/ballerina-nutcracker/ballerina/pull/1213) | fix(semantics): apply detail record defaults in error constr | heshanpadmasiri | open findings: 1 Verify |
| [#1221](https://github.com/ballerina-nutcracker/ballerina/pull/1221) | fix(semantics): check named worker captures in isolated func | heshanpadmasiri | stacked on conflicting #1189 |
| [#1233](https://github.com/ballerina-nutcracker/ballerina/pull/1233) | fix(semantics): enforce visibility of object member access | heshanpadmasiri | conflicting |
| [#1238](https://github.com/ballerina-nutcracker/ballerina/pull/1238) | feat(worker): support fork statements | heshanpadmasiri | stacked on conflicting #1189 |
| [#1254](https://github.com/ballerina-nutcracker/ballerina/pull/1254) | test(corpus): cover error-typed wildcards in query clauses | heshanpadmasiri | CI failed: Validate PR Title, Validate Commit Messages |
| [#1255](https://github.com/ballerina-nutcracker/ballerina/pull/1255) | fix(nodebuilder): allow start actions in type casts and quer | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title, Validate PR Title |
| [#1263](https://github.com/ballerina-nutcracker/ballerina/pull/1263) | feat(compiler): add warnings and report unused variables as  | heshanpadmasiri | conflicting |
| [#1377](https://github.com/ballerina-nutcracker/ballerina/pull/1377) | fix(projects): parse module documents into a slice indexed b | azinneera | open findings: 2 Nits |
| [#1390](https://github.com/ballerina-nutcracker/ballerina/pull/1390) | feat(stdlib): add `ballerina/data.csv` standard library | TharmiganK | open findings: 2 Nits |
| [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) | feat(stdlib): add `ballerina/data.jsondata` standard library | TharmiganK | open findings: 4 Nits |
| [#1411](https://github.com/ballerina-nutcracker/ballerina/pull/1411) | feat(stdlib): add byte-stream and Server-Sent Event support  | TharmiganK | open findings: 1 Nit |
| [#1422](https://github.com/ballerina-nutcracker/ballerina/pull/1422) | feat(stdlib): add `ballerina/data.yaml` standard library | TharmiganK | open findings: 1 Important, 1 Nit |
| [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) | feat(runtime): expose annotations of nested field types | warunalakshitha | open findings: 1 Important, 2 Nits |
| [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) | fix(semantics): carry annotations on inferred typedesc args | warunalakshitha | open findings: 1 Important, 1 Nit |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sor | warunalakshitha | open findings: 1 Nit |
| [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) | fix(http): send http:Request message headers and type client | TharmiganK | open findings: 2 Nits |
| [#1476](https://github.com/ballerina-nutcracker/ballerina/pull/1476) | fix(parser): normalize source newlines and BOM | snelusha | conflicting |
| [#1480](https://github.com/ballerina-nutcracker/ballerina/pull/1480) | feat(workflow): bundle ballerina/workflow with an in-memory  | hasithaa | open findings: 8 Nits |
| [#1481](https://github.com/ballerina-nutcracker/ballerina/pull/1481) | fix(semantics): reject writes to final object fields outside | heshanpadmasiri | conflicting |
| [#1495](https://github.com/ballerina-nutcracker/ballerina/pull/1495) | test: clean up constant folding skip list | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title, Validate PR Title |
| [#1508](https://github.com/ballerina-nutcracker/ballerina/pull/1508) | feat: introduce the test framework | azinneera | conflicting |
| [#1517](https://github.com/ballerina-nutcracker/ballerina/pull/1517) | fix: reject non-private non-isolated fields in isolated obje | heshanpadmasiri | open findings: 3 Nits |
| [#1536](https://github.com/ballerina-nutcracker/ballerina/pull/1536) | feat(ls): add signature help support | nipunayf | open findings: 4 Important, 8 Verify, 10 Nits |
| [#1544](https://github.com/ballerina-nutcracker/ballerina/pull/1544) | ci(perf): replace PR benchmark gates with nightly comparison | heshanpadmasiri | open findings: 4 Verify, 6 Nits |
| [#1567](https://github.com/ballerina-nutcracker/ballerina/pull/1567) | feat(ls): add initial completion support | nipunayf | open findings: 6 Important, 3 Verify, 39 Nits |
| [#1598](https://github.com/ballerina-nutcracker/ballerina/pull/1598) | fix(semantics): reject self in object field initializers | heshanpadmasiri | open findings: 3 Nits |
| [#1600](https://github.com/ballerina-nutcracker/ballerina/pull/1600) | fix(desugar): register each module listener object once | heshanpadmasiri | conflicting |
| [#1601](https://github.com/ballerina-nutcracker/ballerina/pull/1601) | feat(cli): add --dump-desugared-ast flag | heshanpadmasiri | open findings: 2 Nits |
| [#1606](https://github.com/ballerina-nutcracker/ballerina/pull/1606) | docs(agents): limit subset doc updates to support and restri | heshanpadmasiri | open findings: 1 Nit |
| [#1607](https://github.com/ballerina-nutcracker/ballerina/pull/1607) | chore(lint): enable modernize and modernize Go code | heshanpadmasiri | CI failed: Ubuntu WASM Build |
| [#1608](https://github.com/ballerina-nutcracker/ballerina/pull/1608) | refactor(diagnostics): remove unused diagnostic severities | heshanpadmasiri | CI failed: codecov/patch |
| [#1609](https://github.com/ballerina-nutcracker/ballerina/pull/1609) | chore(lint): make enum switches exhaustive | heshanpadmasiri | CI failed: Validate PR Title, Validate Commit Messages |
| [#1610](https://github.com/ballerina-nutcracker/ballerina/pull/1610) | chore(lint): make expression switches exhaustive | heshanpadmasiri | CI failed: Benchmark memory main vs PR head, Benchmark time main vs PR head, Benchmark HTTP base vs PR head |
| [#1611](https://github.com/ballerina-nutcracker/ballerina/pull/1611) | refactor(nodes): keep shared base types private | heshanpadmasiri | CI failed: Benchmark time main vs PR head, Benchmark memory main vs PR head, Benchmark HTTP base vs PR head |
| [#1612](https://github.com/ballerina-nutcracker/ballerina/pull/1612) | chore(lint): enforce module lint tiers | heshanpadmasiri | open findings: 1 Nit |
| [#1613](https://github.com/ballerina-nutcracker/ballerina/pull/1613) | chore(lint): require production use of functions in strict m | heshanpadmasiri | open findings: 1 Verify, 1 Nit |
| [#1614](https://github.com/ballerina-nutcracker/ballerina/pull/1614) | chore(lint): enforce shallow declaration checks and fix find | heshanpadmasiri | CI failed: Benchmark memory main vs PR head, Benchmark HTTP base vs PR head, Ubuntu WASM Build |
| [#1623](https://github.com/ballerina-nutcracker/ballerina/pull/1623) | ci(nightly): add nightly flake sniffer and actionlint | heshanpadmasiri | open findings: 5 Nits |
| [#1624](https://github.com/ballerina-nutcracker/ballerina/pull/1624) | ci(release): publish an automatic patch release every night | heshanpadmasiri | open findings: 1 Important, 3 Nits |
| [#1625](https://github.com/ballerina-nutcracker/ballerina/pull/1625) | ci: check stdlib coverage docs before push | TharmiganK | base #1584 already merged; rebase onto main |
| [#1626](https://github.com/ballerina-nutcracker/ballerina/pull/1626) | fix(desugar): check service on-clause variables for errors | heshanpadmasiri | CI failed: Validate PR Title, Validate Commit Messages |
| [#1630](https://github.com/ballerina-nutcracker/ballerina/pull/1630) | ci: report references to closed issues nightly | heshanpadmasiri | open findings: 3 Nits |
| [#1631](https://github.com/ballerina-nutcracker/ballerina/pull/1631) | fix(analysis): require isolated values in isolated object fi | heshanpadmasiri | CI failed: Benchmark HTTP base vs PR head, Benchmark memory main vs PR head, Benchmark time main vs PR head |
| [#1638](https://github.com/ballerina-nutcracker/ballerina/pull/1638) | fix(cfg): reject reads of module variables in init before as | heshanpadmasiri | open findings: 2 Nits |
| [#1639](https://github.com/ballerina-nutcracker/ballerina/pull/1639) | fix(semantics): reject non-type symbols in type references | heshanpadmasiri | open findings: 1 Important, 1 Nit |
| [#1640](https://github.com/ballerina-nutcracker/ballerina/pull/1640) | fix(types): defer recursive subtype checks until types are d | heshanpadmasiri | open findings: 1 Important, 3 Nits |
| [#1641](https://github.com/ballerina-nutcracker/ballerina/pull/1641) | fix(symbols): stop transitive field walk on object inclusion | heshanpadmasiri | open findings: 1 Nit |
| [#1642](https://github.com/ballerina-nutcracker/ballerina/pull/1642) | fix(types): resolve annotations on local variables and neste | heshanpadmasiri | open findings: 2 Important, 1 Nit |
| [#1647](https://github.com/ballerina-nutcracker/ballerina/pull/1647) | fix(desugar): capture enclosing variables in anonymous funct | heshanpadmasiri | open findings: 1 Verify, 2 Nits |

## This round

| PR | Verdict | New Important/Verify findings | Summary |
|---|---|---|---|
| #985 (re-review: `fae6e4a04` → `3c2ea5b7b`) | Not ready | **Important:** 4bb33a14a and 98c37765c don't build. `ls/core/compile/stage.go:177,181` still passes 2 arguments, and c32cdae04 fixes that. 3 earlier Nits are still open (unsquashed fix-up commits, stale PR body, `perf` title on a diagnostics change). There are 4 new Nits, including a sibling-drop test that the barriers from the compiler-plugin merge made vacuous. | [comment](https://github.com/ballerina-nutcracker/ballerina/pull/985#issuecomment-5874531843) |
| #1598 (new) | Ready except approval | None. There are 3 Nits: two subset10.md bullets only restate spec behaviour, and the PR body doesn't use the template. Rejections match jBallerina, measured on all 7 tests and 5 extra probes. | [comment](https://github.com/ballerina-nutcracker/ballerina/pull/1598#issuecomment-6846416487) |

## Skipped
- **Conflicting with main, not reviewed:**
  - #1189 is the base of the #1221 and #1238 stack, so the whole stack was skipped.
  - #1233, #1263 and #1481 conflict.
  - #1625 is based on `ci/langlib-coverage-pre-push`, which was already merged as #1584. It needs a rebase onto main.
- **Not checked:** none.

## Filed issues
- [#1659](https://github.com/ballerina-nutcracker/ballerina/issues/1659): `self` in a method or `init` parameter default compiles, then crashes at runtime with `interface conversion: values.BalValue is nil`. I re-ran it on main `d69c341a5` and it still crashes. jBallerina rejects it with `undefined symbol 'self'`. It came up during the #1598 review. The closest existing issue, #1151, has a different trigger.

## Review-skill updates (proposed by the #985 agent, not applied)
- **SKILL.md, "Data races" section:** the stage description is out of date. It should say:
  - stages 1–2 run concurrently across modules;
  - stages 3–4 run in sequence, in dependency order;
  - stages 5–8 run concurrently;
  - stage 9 (compiler plugins) is a barrier;
  - stages 10–11 are pipelined per module.
- **SKILL.md, "Stage boundaries" section:** change `analyzeAndDesugar` / "stages 5–9" to `analyzeAndCreateCFG` / `desugarModule` in `module_context.go`, plus the barriers in `package_compilation.go`, covering stages 5–10.
- **New rule:** when re-reviewing a rebased PR, check that tests added for an earlier finding still reach their code path. Barriers added on main can make them vacuous.
- **Per-commit build check:** it must build every module in go.work. A root `go build ./...` misses `ls` and the other submodules.

## Retrospective inputs

| PR | Kind | Description | Link |
|---|---|---|---|
| #985 | missed | The last round didn't flag the license-header mismatch on `projects/testdata/single-file-birgen-fails/main.bal`, which was already in the `fae6e4a04` diff. | [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) |
| #985 | wasted | The first full `go test` run passed module patterns as one zsh word and tested nothing. Run it under `sh`. | [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) |
| #985 | lint candidate | A per-commit build check across all go.work modules, plus a license-header check in CI. | [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) |
| #985 | recurring | "address review suggestions" fix-up commits are left unsquashed; this is the third round on this PR. | [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) |
| #1598 | wasted | Relative paths broke the jBallerina probe runner. A base run of the service `-e` tests ran without a timeout and had to be stopped by hand. Existing rules already cover both (absolute paths, Popen + killpg). | [#1598](https://github.com/ballerina-nutcracker/ballerina/pull/1598) |
| #1598 | lint candidate | Flag subset-doc bullets that only restate spec behaviour. Low value. | [#1598](https://github.com/ballerina-nutcracker/ballerina/pull/1598) |
| #1598 | recurring | The PR body uses Goals/Non goals/Design instead of the template's sections, the same pattern as #1638–#1647. | [#1598](https://github.com/ballerina-nutcracker/ballerina/pull/1598) |

**Housekeeping:**
- A safety check blocked deleting `/private/tmp/review-sp/selfbug`, the folder I used to write the bug repro, because it was my working directory at the time. It's under `$SP`, so the runner's cleanup will remove it.
- Older worktrees not created by this round are still registered: `/private/tmp/pr1053-merged`, `/private/tmp/pr1053-merged-current`, `/private/tmp/pr1536-head`, `/private/tmp/pr921-merged`, and a bal-bench worktree. I left them alone.

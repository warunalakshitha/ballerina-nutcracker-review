# Review round · 2026-11-12 23:13

`pr730remote/main` `d69c341a5` · ended 23:42 · no tooling gaps (`bal`, `go` and `golangci-lint` are all available)

**Open PRs: 69** · merge-ready: 5 · waiting for CI: 1 · not ready: 57 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 3

## Merge-ready (5)

| PR | Title | Author | Approval | Reviewed |
|---|---|---|---|---|
| [#701](https://github.com/ballerina-nutcracker/ballerina/pull/701) | feat(tcp): port ballerina/tcp standard library | TharmiganK | review required | `c1b5afb31` |
| [#1415](https://github.com/ballerina-nutcracker/ballerina/pull/1415) | feat(data.xmldata): add `ballerina/data.xmldata` standard library | TharmiganK | review required | `530706e70` |
| [#1437](https://github.com/ballerina-nutcracker/ballerina/pull/1437) | feat(stdlib): add `ballerina/cache` standard library | TharmiganK | review required | `b2d2ea24e` |
| [#1607](https://github.com/ballerina-nutcracker/ballerina/pull/1607) | chore(lint): enable modernize and modernize Go code | heshanpadmasiri | review required | `c53f03fb4` |
| [#1611](https://github.com/ballerina-nutcracker/ballerina/pull/1611) | refactor(nodes): keep shared base types private | heshanpadmasiri | review required | `bd8ea77c3` |

## Waiting for CI (1)

0 findings, no conflicts, reviewed at the current head; merge-ready once CI passes.

| PR | Title | Author | Approval | CI |
|---|---|---|---|---|
| [#1446](https://github.com/ballerina-nutcracker/ballerina/pull/1446) | feat(stdlib): add `ballerina/ftp` standard library | TharmiganK | review required | CI pending (1) |

## Not ready (57)

open findings: 33 · CI failed: 6 · conflicting: 10 · not reviewed at current head: 8

| PR | Title | Author | Why |
|---|---|---|---|
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | conflicting |
| [#925](https://github.com/ballerina-nutcracker/ballerina/pull/925) | feat(semantics): use record defaults in constant mappings | heshanpadmasiri | open findings: 1 Verify, 2 Nits |
| [#926](https://github.com/ballerina-nutcracker/ballerina/pull/926) | fix(semantics): analyze constant type descriptors separately | heshanpadmasiri | open findings: 1 Nit |
| [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) | perf(projects): fix parallelization issue | azinneera | conflicting |
| [#1053](https://github.com/ballerina-nutcracker/ballerina/pull/1053) | fix(types): treat readonly class values as readonly | heshanpadmasiri | conflicting |
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title |
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | CI failed: Validate PR Title |
| [#1188](https://github.com/ballerina-nutcracker/ballerina/pull/1188) | fix(nodebuilder): report '_' used as identifier as syntax er | heshanpadmasiri | open findings: 1 Important, 1 Nit |
| [#1189](https://github.com/ballerina-nutcracker/ballerina/pull/1189) | feat(worker): support worker message passing | heshanpadmasiri | conflicting |
| [#1193](https://github.com/ballerina-nutcracker/ballerina/pull/1193) | fix(semantics): evaluate computed mapping keys as expression | heshanpadmasiri | open findings: 6 Nits |
| [#1201](https://github.com/ballerina-nutcracker/ballerina/pull/1201) | refactor: align conditional type narrowing with the spec | heshanpadmasiri | open findings: 1 Nit |
| [#1208](https://github.com/ballerina-nutcracker/ballerina/pull/1208) | fix(semantics): reject out-of-range int literals | heshanpadmasiri | open findings: 2 Nits |
| [#1213](https://github.com/ballerina-nutcracker/ballerina/pull/1213) | fix(semantics): apply detail record defaults in error constr | heshanpadmasiri | open findings: 1 Verify |
| [#1221](https://github.com/ballerina-nutcracker/ballerina/pull/1221) | fix(semantics): check named worker captures in isolated func | heshanpadmasiri | not reviewed at current head |
| [#1233](https://github.com/ballerina-nutcracker/ballerina/pull/1233) | fix(semantics): enforce visibility of object member access | heshanpadmasiri | conflicting |
| [#1238](https://github.com/ballerina-nutcracker/ballerina/pull/1238) | feat(worker): support fork statements | heshanpadmasiri | not reviewed at current head |
| [#1254](https://github.com/ballerina-nutcracker/ballerina/pull/1254) | test(corpus): cover error-typed wildcards in query clauses | heshanpadmasiri | CI failed: Validate PR Title, Validate Commit Messages |
| [#1255](https://github.com/ballerina-nutcracker/ballerina/pull/1255) | fix(nodebuilder): allow start actions in type casts and quer | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title, Validate PR Title |
| [#1263](https://github.com/ballerina-nutcracker/ballerina/pull/1263) | feat(compiler): add warnings and report unused variables as  | heshanpadmasiri | conflicting |
| [#1377](https://github.com/ballerina-nutcracker/ballerina/pull/1377) | fix(projects): parse module documents into a slice indexed b | azinneera | open findings: 2 Nits |
| [#1390](https://github.com/ballerina-nutcracker/ballerina/pull/1390) | feat(stdlib): add `ballerina/data.csv` standard library | TharmiganK | open findings: 2 Nits |
| [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) | feat(stdlib): add `ballerina/data.jsondata` standard library | TharmiganK | open findings: 1 Important, 2 Nits |
| [#1411](https://github.com/ballerina-nutcracker/ballerina/pull/1411) | feat(stdlib): add byte-stream and Server-Sent Event support  | TharmiganK | open findings: 1 Nit |
| [#1422](https://github.com/ballerina-nutcracker/ballerina/pull/1422) | feat(stdlib): add `ballerina/data.yaml` standard library | TharmiganK | open findings: 1 Important, 12 Nits |
| [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) | feat(runtime): expose annotations of nested field types | warunalakshitha | open findings: 2 Important, 3 Nits |
| [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) | fix(semantics): carry annotations on inferred typedesc args | warunalakshitha | open findings: 1 Important, 2 Nits |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sor | warunalakshitha | open findings: 1 Verify, 1 Nit |
| [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) | fix(http): send http:Request message headers and type client | TharmiganK | open findings: 2 Nits |
| [#1476](https://github.com/ballerina-nutcracker/ballerina/pull/1476) | fix(parser): normalize source newlines and BOM | snelusha | conflicting |
| [#1480](https://github.com/ballerina-nutcracker/ballerina/pull/1480) | feat(workflow): bundle ballerina/workflow with an in-memory  | hasithaa | open findings: 8 Nits |
| [#1481](https://github.com/ballerina-nutcracker/ballerina/pull/1481) | fix(semantics): reject writes to final object fields outside | heshanpadmasiri | conflicting |
| [#1495](https://github.com/ballerina-nutcracker/ballerina/pull/1495) | test: clean up constant folding skip list | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title, Ubuntu Native Build |
| [#1508](https://github.com/ballerina-nutcracker/ballerina/pull/1508) | feat: introduce the test framework | azinneera | conflicting |
| [#1517](https://github.com/ballerina-nutcracker/ballerina/pull/1517) | fix: reject non-private non-isolated fields in isolated obje | heshanpadmasiri | open findings: 3 Nits |
| [#1536](https://github.com/ballerina-nutcracker/ballerina/pull/1536) | feat(ls): add signature help support | nipunayf | open findings: 4 Important, 8 Verify, 10 Nits |
| [#1544](https://github.com/ballerina-nutcracker/ballerina/pull/1544) | ci(perf): replace PR benchmark gates with nightly comparison | heshanpadmasiri | open findings: 4 Verify, 6 Nits |
| [#1567](https://github.com/ballerina-nutcracker/ballerina/pull/1567) | feat(ls): add initial completion support | nipunayf | open findings: 6 Important, 3 Verify, 39 Nits |
| [#1600](https://github.com/ballerina-nutcracker/ballerina/pull/1600) | fix(desugar): register each module listener object once | heshanpadmasiri | conflicting |
| [#1601](https://github.com/ballerina-nutcracker/ballerina/pull/1601) | feat(cli): add --dump-desugared-ast flag | heshanpadmasiri | open findings: 2 Nits |
| [#1606](https://github.com/ballerina-nutcracker/ballerina/pull/1606) | docs(agents): limit subset doc updates to support and restri | heshanpadmasiri | open findings: 1 Nit |
| [#1608](https://github.com/ballerina-nutcracker/ballerina/pull/1608) | refactor(diagnostics): remove unused diagnostic severities | heshanpadmasiri | open findings: 1 Nit |
| [#1609](https://github.com/ballerina-nutcracker/ballerina/pull/1609) | chore(lint): make enum switches exhaustive | heshanpadmasiri | open findings: 1 Nit |
| [#1610](https://github.com/ballerina-nutcracker/ballerina/pull/1610) | chore(lint): make expression switches exhaustive | heshanpadmasiri | CI failed: codecov/patch, Benchmark time main vs PR head, Benchmark memory main vs PR head |
| [#1612](https://github.com/ballerina-nutcracker/ballerina/pull/1612) | chore(lint): enforce module lint tiers | heshanpadmasiri | open findings: 3 Nits |
| [#1613](https://github.com/ballerina-nutcracker/ballerina/pull/1613) | chore(lint): require production use of functions in strict m | heshanpadmasiri | open findings: 8 Nits |
| [#1614](https://github.com/ballerina-nutcracker/ballerina/pull/1614) | chore(lint): enforce shallow declaration checks and fix find | heshanpadmasiri | open findings: 9 Nits |
| [#1623](https://github.com/ballerina-nutcracker/ballerina/pull/1623) | ci(nightly): add nightly flake sniffer and actionlint | heshanpadmasiri | open findings: 5 Nits |
| [#1624](https://github.com/ballerina-nutcracker/ballerina/pull/1624) | ci(release): publish an automatic patch release every night | heshanpadmasiri | open findings: 1 Important, 3 Nits |
| [#1625](https://github.com/ballerina-nutcracker/ballerina/pull/1625) | ci: check stdlib coverage docs before push | TharmiganK | not reviewed at current head |
| [#1626](https://github.com/ballerina-nutcracker/ballerina/pull/1626) | fix(desugar): check service on-clause variables for errors | heshanpadmasiri | open findings: 1 Nit |
| [#1630](https://github.com/ballerina-nutcracker/ballerina/pull/1630) | ci: report references to closed issues nightly | heshanpadmasiri | open findings: 3 Nits |
| [#1631](https://github.com/ballerina-nutcracker/ballerina/pull/1631) | fix(analysis): require isolated values in isolated object fi | heshanpadmasiri | open findings: 3 Nits |
| [#1638](https://github.com/ballerina-nutcracker/ballerina/pull/1638) | fix(cfg): reject reads of module variables in init before as | heshanpadmasiri | not reviewed at current head |
| [#1639](https://github.com/ballerina-nutcracker/ballerina/pull/1639) | fix(semantics): reject non-type symbols in type references | heshanpadmasiri | not reviewed at current head |
| [#1640](https://github.com/ballerina-nutcracker/ballerina/pull/1640) | fix(types): defer recursive subtype checks until types are d | heshanpadmasiri | not reviewed at current head |
| [#1641](https://github.com/ballerina-nutcracker/ballerina/pull/1641) | fix(symbols): stop transitive field walk on object inclusion | heshanpadmasiri | not reviewed at current head |
| [#1642](https://github.com/ballerina-nutcracker/ballerina/pull/1642) | fix(types): resolve annotations on local variables and neste | heshanpadmasiri | not reviewed at current head |

The table lists #1165 as "CI failed: Validate PR Title", but that check now passes. All its checks are green, so the table is reading an old failed run. With 0 findings, #1165 is in practice merge-ready.

## This round

| PR | Verdict | New Important/Verify | Summary |
|---|---|---|---|
| #1165 | READY except approval | None. The rebase left the tree unchanged, and all earlier items are fixed. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1165#issuecomment-6022408692) |
| #1434 | NOT READY | **Important:** since 1be0a790f, an alias whose target is still being resolved copies no members. With `type Alias Node;` declared after a recursive `Node`, `f(*Alias)` rejects `v`. main and jBallerina print 3 and 7.<br>**Important:** commit 19b7df2b0 doesn't build; squash 0fc0e1d0e into it. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1434#issuecomment-6506053463) |
| #1435 | NOT READY | **Important:** commit 5ec80fd34 doesn't build; squash 1078f0ea5 into it. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1435#issuecomment-6720717565) |
| #1438 | NOT READY | **Verify:** `pop`, `shift` and `unshift` on a union of fixed-length lists (`int[1]\|int[2]`) compile and then always panic. jBallerina rejects them at compile time. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1438#issuecomment-6817254010) |

Nits posted this round:
- **#1434:** add `Fixes #1527`, add a test case for #1527, and use the body template.
- **#1435:** test cases for two of the fix's paths are missing, and use the body template.
- **#1438:** an empty list is reported as readonly.

## Skipped
- **Conflicting with main (not reviewed):**
  - #1189, #1221 and #1238: the whole worker stack; #1189 conflicts at its base.
  - #1233, #1263, #1481.
  - #1625: its base branch has no open PR.
  - #1638, #1639, #1640, #1641 and #1642: the top of the #1607–#1642 stack. Every PR in that stack that needed review conflicts.
- **Not checked:** none.

## Filed issues
- [#1646](https://github.com/ballerina-nutcracker/ballerina/issues/1646) `[Bug]: record type inclusion of a type alias reports "included type is not a record type"`.
  - Reproduced on main d69c341a5; jBallerina prints `5 true`.
  - A clean-context spec check prefers the reading that makes it valid.
  - No duplicates found. Related: #1289, #1295.

## Review-skill updates
None. No reviewed PR changes process files.

## Retrospective inputs

| PR | Kind | Description | Link |
|---|---|---|---|
| #1434 | missed | CodeRabbit's stale stub-fingerprint thread (already noted in an earlier retrospective). | [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) |
| #1434 | lint candidate | A commit that doesn't build has recurred on this stack. A per-commit `go build` check (`git rebase -x`) would catch it every time. | [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) |
| #1435 | missed | CodeRabbit's outside-diff items "constructor args lose named types" and "deferred param defaults"; both are now fixed in 5ec80fd34. | [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) |
| #1435 | recurring | A commit that doesn't build: follow-up refactor commits that later commits rely on are left unsquashed. | [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) |
| #1438 | missed | heshanpadmasiri: the sort key must stay isolated when the caller is not isolated. Probe declared isolated callback parameters from a non-isolated caller. | [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) |
| #1438 | missed | CodeRabbit: a stray "parameter" in the `sort` doc text. | [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) |
| #1438 | lint candidate | Flag `ToListAtomicType(...) != nil && IsNever(atomic.Rest())` used as an "is fixed-length" test, because it misses unions. `push` at `registry.go:127` on main has the same pattern. | [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) |

**Other notes:**
- **Flaky test:** `corpus/lib/subset3/task-misfire1-v.bal` failed once during the #1438 review and passed when rerun alone.
- **Unfiled bug on main:** the #1438 agent found the same union gap in `push` on main (`int[1]|int[2]` compiles, then panics at runtime). It ran no duplicate search, so I haven't filed it.

All worktrees, binaries and probes from this round are removed.

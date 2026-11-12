# Review round · 2026-11-12 15:28 Asia/Colombo

`pr730remote/main` `d69c341a5` · ended 2026-11-12 15:57 · no tooling gaps (`bal`, `golangci-lint` and `gh` all available)

**Open PRs: 68** · merge-ready: 6 · waiting for CI: 1 · not ready: 55 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 3

## Merge-ready (6)

| PR | Title | Author | Approval | Reviewed |
|---|---|---|---|---|
| [#701](https://github.com/ballerina-nutcracker/ballerina/pull/701) | feat(tcp): port ballerina/tcp standard library | TharmiganK | review required | `c1b5afb31` |
| [#1415](https://github.com/ballerina-nutcracker/ballerina/pull/1415) | feat(data.xmldata): add `ballerina/data.xmldata` standard library | TharmiganK | review required | `530706e70` |
| [#1437](https://github.com/ballerina-nutcracker/ballerina/pull/1437) | feat(stdlib): add `ballerina/cache` standard library | TharmiganK | review required | `b2d2ea24e` |
| [#1567](https://github.com/ballerina-nutcracker/ballerina/pull/1567) | feat(ls): add initial completion support | nipunayf | review required | `b66eda4f1` |
| [#1607](https://github.com/ballerina-nutcracker/ballerina/pull/1607) | chore(lint): enable modernize and modernize Go code | heshanpadmasiri | review required | `c53f03fb4` |
| [#1611](https://github.com/ballerina-nutcracker/ballerina/pull/1611) | refactor(nodes): keep shared base types private | heshanpadmasiri | review required | `bd8ea77c3` |

## Waiting for CI (1)

0 findings, no conflicts, reviewed at the current head; merge-ready once CI passes.

| PR | Title | Author | Approval | CI |
|---|---|---|---|---|
| [#1446](https://github.com/ballerina-nutcracker/ballerina/pull/1446) | feat(stdlib): add `ballerina/ftp` standard library | TharmiganK | review required | CI pending (1) |

## Not ready (55)

open findings: 33 · CI failed: 5 · conflicting: 10 · not reviewed at current head: 7

| PR | Title | Author | Why |
|---|---|---|---|
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | conflicting |
| [#925](https://github.com/ballerina-nutcracker/ballerina/pull/925) | feat(semantics): use record defaults in constant mappings | heshanpadmasiri | open findings: 1 Verify, 2 Nits |
| [#926](https://github.com/ballerina-nutcracker/ballerina/pull/926) | fix(semantics): analyze constant type descriptors separately | heshanpadmasiri | open findings: 1 Nit |
| [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) | perf(projects): fix parallelization issue | azinneera | conflicting |
| [#1053](https://github.com/ballerina-nutcracker/ballerina/pull/1053) | fix(types): treat readonly class values as readonly | heshanpadmasiri | conflicting |
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title |
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | open findings: 1 Important, 3 Nits |
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
| [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) | feat(runtime): expose annotations of nested field types | warunalakshitha | open findings: 1 Important, 1 Verify, 1 Nit |
| [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) | fix(semantics): carry annotations on inferred typedesc args | warunalakshitha | open findings: 1 Important |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sor | warunalakshitha | open findings: 1 Verify, 1 Nit |
| [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) | fix(http): send http:Request message headers and type client | TharmiganK | open findings: 2 Nits |
| [#1476](https://github.com/ballerina-nutcracker/ballerina/pull/1476) | fix(parser): normalize source newlines and BOM | snelusha | conflicting |
| [#1480](https://github.com/ballerina-nutcracker/ballerina/pull/1480) | feat(workflow): bundle ballerina/workflow with an in-memory  | hasithaa | open findings: 8 Nits |
| [#1481](https://github.com/ballerina-nutcracker/ballerina/pull/1481) | fix(semantics): reject writes to final object fields outside | heshanpadmasiri | conflicting |
| [#1495](https://github.com/ballerina-nutcracker/ballerina/pull/1495) | test: clean up constant folding skip list | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title, Ubuntu Native Build |
| [#1508](https://github.com/ballerina-nutcracker/ballerina/pull/1508) | feat: introduce the test framework | azinneera | conflicting |
| [#1517](https://github.com/ballerina-nutcracker/ballerina/pull/1517) | fix: reject non-private non-isolated fields in isolated obje | heshanpadmasiri | open findings: 3 Nits |
| [#1536](https://github.com/ballerina-nutcracker/ballerina/pull/1536) | feat(ls): add signature help support | nipunayf | open findings: 1 Nit |
| [#1544](https://github.com/ballerina-nutcracker/ballerina/pull/1544) | ci(perf): replace PR benchmark gates with nightly comparison | heshanpadmasiri | open findings: 4 Verify, 6 Nits |
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

## This round

| PR | Verdict | New Important / Verify findings | Summary |
|---|---|---|---|
| #1165 | NOT READY | 🔴 Seven of nine commits don't build: ldap still calls the 3-argument `CloneWithType` until `f876d11f0`; fold it into `1a53a4dd6`. I re-ran this build myself before posting. Also 3 Nits: unsquashed review fixes, body lacks `Fixes #1026`, body doesn't use the PR template. All 4 earlier code findings are fixed. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1165#issuecomment-6022408692) |
| #1434 | NOT READY | 🔴 `fbdaf706b` doesn't build: `common.NamedTypeRef` only exists from `b35691ae8`.<br>🟡 Typedesc `===` now depends on which module built the typedesc. Is per-module identity intended? | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1434#issuecomment-6506053463) |
| #1435 | NOT READY | 🔴 `ad72d6876` doesn't build: `resolveWithNamedTypes` only exists from `9169d0d99`; squash that commit into `ad72d6876`. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1435#issuecomment-6720717565) |
| #1438 | NOT READY | 🟡 `pop`, `shift` and `unshift` on a list known to be fixed-length now compile and panic at runtime. The spec's lang/lib/array.bal says this is a compile-time error, and jBallerina rejects it. Should it stay a compile error? Plus 1 Nit on the sort error message. All 5 earlier findings are fixed. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1438#issuecomment-6817254010) |
| #1536 | 1 Nit (refreshed only) | None. The code diff is unchanged after the rebase; the diff hash matches the last round. The commits went from 19 to 5, and the nit about unsquashed commits still holds, so I updated it to the current SHAs. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1536#issuecomment-6624746231) |

## Skipped
- **#1189, #1221, #1238**: worker stack. #1189 conflicts with main, so the whole stack does.
- **#1233, #1263, #1481**: conflicting.
- **#1625**: its base PR #1584 was merged, and its own two commits conflict when applied to main.
- **#1638, #1639, #1640, #1641**: they sit in the #1607 stack above #1613, the first PR in it that conflicts with main. #1607–#1612 merge cleanly but didn't need review this round.
- Not checked: none.

## Filed issues
None. The only bug found on main was a false "invalid cycle" when a record that refers through a field to the record that includes it is declared first. It is already tracked as #1289.

## Review-skill updates
None. No reviewed PR changes process files.

## Retrospective inputs

| PR | Kind | Description | Link |
|---|---|---|---|
| #1165 | lint candidate | Build every commit including the `lib` workspace module (`git rebase -x 'go build ./... ./lib/...'`). A plain `go build ./...` misses the ldap break. | [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) |
| #1434 | lint candidate | The same per-commit build check would have caught the Important findings on #1434 and #1435. | [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) |
| #1434 | missed | CodeRabbit: stale stub fingerprint in the serializer (the author declined it). | [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) |
| #1435 | missed | CodeRabbit: named types for the rest parameter (fixed). | [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) |
| #1435 | missed | CodeRabbit: named types for nil-conditional expressions (fixed). | [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) |
| #1438 | missed | heshanpadmasiri: the sort key function must be isolated (fixed). | [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) |
| #1438 | wrong | Last round's spec subagent wasn't given lang/lib/array.bal, so it missed the "compile-time error if known to be fixed-length" comment. Our own question then pushed the author to runtime-only checks. Langlib spec questions should always include that file. | [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) |
| #1438 | lint candidate | Check that a langlib function's mutation rules match the `//` comments in the spec's lang/lib/*.bal files. | [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) |

Flaky test seen: `corpus/lib/subset3/task-misfire1-v.bal` failed once and passed when rerun alone.

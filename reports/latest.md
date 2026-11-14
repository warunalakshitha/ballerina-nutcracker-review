# Review round · 2026-11-14 12:07

`origin/main` cbe12629d · skills ded7d34 · ended 2026-11-14 12:31 · tooling gaps: none (go 1.27.1, bal 2201.14.1, golangci-lint 2.15.0, actionlint 1.7.12, shellcheck 0.9.0, wrk, hyperfine)

_Open-PR tables refreshed 2026-11-14 20:40 (Asia/Colombo)._

**Open PRs: 67** · can merge: 3 (0 in merge queue, 3 ready, 0 after CI) · cannot merge: 61 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 0

## Can merge (3)

0 findings, no conflicts, reviewed at the current head, not waiting on another PR.

| PR | Title | Author | Approval | Auto-merge | Status |
|---|---|---|---|---|---|
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | review required | — | ready |
| [#1255](https://github.com/ballerina-nutcracker/ballerina/pull/1255) | fix(nodebuilder): allow start actions in type casts and query selects | heshanpadmasiri | review required | — | ready |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sort | warunalakshitha | review required | — | ready |

## Cannot merge (61)

open findings: 39 · CI failed: 9 · conflicting: 9 · stacked on conflicting: 2 · base already merged: 1 · stacked: 1

Auto-merge on a PR here merges it once GitHub's requirements pass, open findings or not.

| PR | Title | Author | Auto-merge | Why |
|---|---|---|---|---|
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | — | conflicting |
| [#701](https://github.com/ballerina-nutcracker/ballerina/pull/701) | feat(tcp): port ballerina/tcp standard library | TharmiganK | — | open findings: 2 Verify, 4 Nits |
| [#925](https://github.com/ballerina-nutcracker/ballerina/pull/925) | feat(semantics): use record defaults in constant mappings | heshanpadmasiri | — | open findings: 1 Verify, 2 Nits |
| [#926](https://github.com/ballerina-nutcracker/ballerina/pull/926) | fix(semantics): analyze constant type descriptors separately | heshanpadmasiri | on (rebase, heshanpadmasiri) | open findings: 1 Nit |
| [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) | perf(projects): fix parallelization issue | azinneera | — | open findings: 1 Important, 7 Nits |
| [#1053](https://github.com/ballerina-nutcracker/ballerina/pull/1053) | fix(types): treat readonly class values as readonly | heshanpadmasiri | — | conflicting |
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | — | CI failed: Windows Native Build, Ubuntu WASM Build, Ubuntu Native Build |
| [#1188](https://github.com/ballerina-nutcracker/ballerina/pull/1188) | fix(nodebuilder): report '_' used as identifier as syntax er | heshanpadmasiri | on (rebase, heshanpadmasiri) | open findings: 1 Important, 1 Nit |
| [#1189](https://github.com/ballerina-nutcracker/ballerina/pull/1189) | feat(worker): support worker message passing | heshanpadmasiri | — | conflicting |
| [#1193](https://github.com/ballerina-nutcracker/ballerina/pull/1193) | fix(semantics): evaluate computed mapping keys as expression | heshanpadmasiri | — | open findings: 6 Nits |
| [#1201](https://github.com/ballerina-nutcracker/ballerina/pull/1201) | refactor: align conditional type narrowing with the spec | heshanpadmasiri | — | open findings: 1 Nit |
| [#1208](https://github.com/ballerina-nutcracker/ballerina/pull/1208) | fix(semantics): reject out-of-range int literals | heshanpadmasiri | on (rebase, heshanpadmasiri) | open findings: 2 Nits |
| [#1213](https://github.com/ballerina-nutcracker/ballerina/pull/1213) | fix(semantics): apply detail record defaults in error constr | heshanpadmasiri | — | open findings: 1 Verify |
| [#1221](https://github.com/ballerina-nutcracker/ballerina/pull/1221) | fix(semantics): check named worker captures in isolated func | heshanpadmasiri | — | stacked on conflicting #1189 |
| [#1233](https://github.com/ballerina-nutcracker/ballerina/pull/1233) | fix(semantics): enforce visibility of object member access | heshanpadmasiri | — | conflicting |
| [#1238](https://github.com/ballerina-nutcracker/ballerina/pull/1238) | feat(worker): support fork statements | heshanpadmasiri | — | stacked on conflicting #1189 |
| [#1263](https://github.com/ballerina-nutcracker/ballerina/pull/1263) | feat(compiler): add warnings and report unused variables as  | heshanpadmasiri | — | conflicting |
| [#1390](https://github.com/ballerina-nutcracker/ballerina/pull/1390) | feat(stdlib): add `ballerina/data.csv` standard library | TharmiganK | — | open findings: 2 Nits |
| [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) | feat(stdlib): add `ballerina/data.jsondata` standard library | TharmiganK | — | open findings: 3 Nits |
| [#1411](https://github.com/ballerina-nutcracker/ballerina/pull/1411) | feat(stdlib): add byte-stream and Server-Sent Event support  | TharmiganK | — | open findings: 1 Nit |
| [#1415](https://github.com/ballerina-nutcracker/ballerina/pull/1415) | feat(data.xmldata): add `ballerina/data.xmldata` standard li | TharmiganK | — | open findings: 1 Important, 1 Verify, 7 Nits |
| [#1422](https://github.com/ballerina-nutcracker/ballerina/pull/1422) | feat(stdlib): add `ballerina/data.yaml` standard library | TharmiganK | — | open findings: 1 Important, 1 Nit |
| [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) | feat(runtime): expose annotations of nested field types | warunalakshitha | — | open findings: 2 Nits |
| [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) | fix(semantics): carry annotations on inferred typedesc args | warunalakshitha | — | open findings: 1 Verify, 4 Nits |
| [#1437](https://github.com/ballerina-nutcracker/ballerina/pull/1437) | feat(stdlib): add `ballerina/cache` standard library | TharmiganK | — | open findings: 3 Nits |
| [#1446](https://github.com/ballerina-nutcracker/ballerina/pull/1446) | feat(stdlib): add `ballerina/ftp` standard library | TharmiganK | — | open findings: 4 Nits |
| [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) | fix(http): send http:Request message headers and type client | TharmiganK | — | open findings: 2 Nits |
| [#1476](https://github.com/ballerina-nutcracker/ballerina/pull/1476) | fix(parser): normalize source newlines and BOM | snelusha | — | conflicting |
| [#1480](https://github.com/ballerina-nutcracker/ballerina/pull/1480) | feat(workflow): bundle ballerina/workflow with an in-memory  | hasithaa | — | open findings: 8 Nits |
| [#1481](https://github.com/ballerina-nutcracker/ballerina/pull/1481) | fix(semantics): reject writes to final object fields outside | heshanpadmasiri | — | conflicting |
| [#1508](https://github.com/ballerina-nutcracker/ballerina/pull/1508) | feat: introduce the test framework | azinneera | — | conflicting |
| [#1517](https://github.com/ballerina-nutcracker/ballerina/pull/1517) | fix: reject non-private non-isolated fields in isolated obje | heshanpadmasiri | — | open findings: 3 Nits |
| [#1536](https://github.com/ballerina-nutcracker/ballerina/pull/1536) | feat(ls): add signature help support | nipunayf | — | open findings: 4 Important, 8 Verify, 10 Nits |
| [#1544](https://github.com/ballerina-nutcracker/ballerina/pull/1544) | ci(perf): replace PR benchmark gates with nightly comparison | heshanpadmasiri | — | open findings: 4 Verify, 6 Nits |
| [#1567](https://github.com/ballerina-nutcracker/ballerina/pull/1567) | feat(ls): add initial completion support | nipunayf | — | open findings: 6 Important, 3 Verify, 39 Nits |
| [#1598](https://github.com/ballerina-nutcracker/ballerina/pull/1598) | fix(semantics): reject self in object field initializers | heshanpadmasiri | — | open findings: 3 Nits |
| [#1600](https://github.com/ballerina-nutcracker/ballerina/pull/1600) | fix(desugar): register each module listener object once | heshanpadmasiri | — | conflicting |
| [#1601](https://github.com/ballerina-nutcracker/ballerina/pull/1601) | feat(cli): add --dump-desugared-ast flag | heshanpadmasiri | — | open findings: 2 Nits |
| [#1606](https://github.com/ballerina-nutcracker/ballerina/pull/1606) | docs(agents): limit subset doc updates to support and restri | heshanpadmasiri | — | open findings: 1 Nit |
| [#1607](https://github.com/ballerina-nutcracker/ballerina/pull/1607) | chore(lint): enable modernize and modernize Go code | heshanpadmasiri | — | CI failed: Ubuntu WASM Build |
| [#1608](https://github.com/ballerina-nutcracker/ballerina/pull/1608) | refactor(diagnostics): remove unused diagnostic severities | heshanpadmasiri | — | CI failed: codecov/patch |
| [#1609](https://github.com/ballerina-nutcracker/ballerina/pull/1609) | chore(lint): make enum switches exhaustive | heshanpadmasiri | — | CI failed: codecov/patch |
| [#1610](https://github.com/ballerina-nutcracker/ballerina/pull/1610) | chore(lint): make expression switches exhaustive | heshanpadmasiri | — | CI failed: codecov/patch |
| [#1611](https://github.com/ballerina-nutcracker/ballerina/pull/1611) | refactor(nodes): keep shared base types private | heshanpadmasiri | — | stacked: merge #1610 first |
| [#1612](https://github.com/ballerina-nutcracker/ballerina/pull/1612) | chore(lint): enforce module lint tiers | heshanpadmasiri | — | open findings: 1 Nit |
| [#1613](https://github.com/ballerina-nutcracker/ballerina/pull/1613) | chore(lint): require production use of functions in strict m | heshanpadmasiri | — | open findings: 1 Verify, 1 Nit |
| [#1614](https://github.com/ballerina-nutcracker/ballerina/pull/1614) | chore(lint): enforce shallow declaration checks and fix find | heshanpadmasiri | — | CI failed: codecov/patch, Ubuntu WASM Build |
| [#1623](https://github.com/ballerina-nutcracker/ballerina/pull/1623) | ci(nightly): add nightly flake sniffer and actionlint | heshanpadmasiri | — | open findings: 2 Nits |
| [#1624](https://github.com/ballerina-nutcracker/ballerina/pull/1624) | ci(release): publish an automatic patch release every night | heshanpadmasiri | — | open findings: 1 Important, 3 Nits |
| [#1625](https://github.com/ballerina-nutcracker/ballerina/pull/1625) | ci: check stdlib coverage docs before push | TharmiganK | — | base #1584 already merged; rebase onto main |
| [#1626](https://github.com/ballerina-nutcracker/ballerina/pull/1626) | fix(desugar): check service on-clause variables for errors | heshanpadmasiri | — | CI failed: Ubuntu WASM Build |
| [#1630](https://github.com/ballerina-nutcracker/ballerina/pull/1630) | ci: report references to closed issues nightly | heshanpadmasiri | — | open findings: 3 Nits |
| [#1631](https://github.com/ballerina-nutcracker/ballerina/pull/1631) | fix(analysis): require isolated values in isolated object fi | heshanpadmasiri | — | CI failed: Ubuntu WASM Build |
| [#1638](https://github.com/ballerina-nutcracker/ballerina/pull/1638) | fix(cfg): reject reads of module variables in init before as | heshanpadmasiri | — | open findings: 2 Nits |
| [#1639](https://github.com/ballerina-nutcracker/ballerina/pull/1639) | fix(semantics): reject non-type symbols in type references | heshanpadmasiri | — | open findings: 1 Important, 1 Nit |
| [#1640](https://github.com/ballerina-nutcracker/ballerina/pull/1640) | fix(types): defer recursive subtype checks until types are d | heshanpadmasiri | — | open findings: 1 Important, 3 Nits |
| [#1641](https://github.com/ballerina-nutcracker/ballerina/pull/1641) | fix(symbols): stop transitive field walk on object inclusion | heshanpadmasiri | — | open findings: 1 Nit |
| [#1642](https://github.com/ballerina-nutcracker/ballerina/pull/1642) | fix(types): resolve annotations on local variables and neste | heshanpadmasiri | — | open findings: 2 Important, 1 Nit |
| [#1647](https://github.com/ballerina-nutcracker/ballerina/pull/1647) | fix(desugar): capture enclosing variables in anonymous funct | heshanpadmasiri | — | open findings: 1 Verify, 2 Nits |
| [#1661](https://github.com/ballerina-nutcracker/ballerina/pull/1661) | fix(types): accept actions as query let clause initializers | heshanpadmasiri | — | CI failed: Ubuntu WASM Build |
| [#1662](https://github.com/ballerina-nutcracker/ballerina/pull/1662) | fix(nodebuilder): lower resource signatures in object types | heshanpadmasiri | — | open findings: 2 Verify, 3 Nits |

## Drafts and held (3)

Not reviewed until the PR is marked ready or the label is removed.

| PR | Title | Author | Why |
|---|---|---|---|
| [#1137](https://github.com/ballerina-nutcracker/ballerina/pull/1137) | feat(stdlib): add `ballerina/constraint` standard library | TharmiganK | draft |
| [#1357](https://github.com/ballerina-nutcracker/ballerina/pull/1357) | feat(http): bind query, header and payload resource paramete | TharmiganK | draft |
| [#1430](https://github.com/ballerina-nutcracker/ballerina/pull/1430) | feat(stdlib): add `ballerina/zip` standard library | TharmiganK | draft |

## This round

| PR | Verdict | New Important/Verify | Summary |
|---|---|---|---|
| #1623 | READY except approval (2 new Nits; all 5 earlier items fixed) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1623#issuecomment-6789513854) |

## Skipped
- #1189: conflicts with main (bottom of stack #1189 → #1221 → #1238)
- #1221, #1238: stacked on conflicting #1189
- #1233, #1263, #1481: conflict with main
- #1625: base branch `ci/langlib-coverage-pre-push` (#1584) is already merged and the PR conflicts with main; needs a rebase onto main

## Filed issues
None.

## Review-skill updates (from #1623, not applied)
- SKILL.md "CI workflow PRs": once #1623 is on main, rely on the `Lint workflows` check at head (path-filtered, not required; note if missing) and run actionlint locally only for mutation proofs.
- New rule next to "Release scripts": for PRs touching `.github/scripts/{cpu_load,collect_failures}.py`, rely on CI's `test_cpu_load.py`/`test_collect_failures.py` run (nightly-flake-sniffer.yml path filter) except for mutations.
- agent-instructions.md known-flaky line already names `nightly-flake-sniffer-failure`: no change.

## Retrospective inputs

| PR | Kind | Description | Link |
|---|---|---|---|
| #1623 | missed | CodeRabbit: interleaved output from 3 concurrent `go test` processes can misattribute tests/seeds in `collect_failures.py` | https://github.com/ballerina-nutcracker/ballerina/pull/1623 |
| #1623 | missed | CodeRabbit: `cpu_load.py` opens the log after `Popen`; a failed open leaks the child | https://github.com/ballerina-nutcracker/ballerina/pull/1623 |
| #1623 | missed | Our earlier round missed that package-level repro commands drop the runner's `-skip`/`-timeout` (raised now as a new Nit) | https://github.com/ballerina-nutcracker/ballerina/pull/1623 |
| #1623 | wasted | 4-minute corpus timing run to support a 10m-timeout claim that didn't hold | https://github.com/ballerina-nutcracker/ballerina/pull/1623 |
| #1623 | lint candidate | Test that `collect_failures` repro commands include `run_native_tests.SKIP_PATTERN` and `TIMEOUT` | https://github.com/ballerina-nutcracker/ballerina/pull/1623 |
| #1623 | recurring | PR body not in template format (Goals/Design), same as #1638, #1640 | https://github.com/ballerina-nutcracker/ballerina/pull/1623 |

Note: the #1623 summary marker's `skill=f9513c71` matched no committed SKILL.md in the tools repo (likely hashed from a local uncommitted copy); the agent did a full re-review with the current skill.

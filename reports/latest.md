# Review round · 2026-11-12 12:20 Asia/Colombo

`pr730remote/main` `008256345` · ended 2026-11-12 13:02 · tooling gaps: none (`bal`, `go`, `golangci-lint` all present).

**Open PRs: 65** · merge-ready: 5 · waiting for CI: 2 · not ready: 52 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 3

## Merge-ready (5)

| PR | Title | Author | Approval | Reviewed |
|---|---|---|---|---|
| [#701](https://github.com/ballerina-nutcracker/ballerina/pull/701) | feat(tcp): port ballerina/tcp standard library | TharmiganK | review required | `c1b5afb31` |
| [#1415](https://github.com/ballerina-nutcracker/ballerina/pull/1415) | feat(data.xmldata): add `ballerina/data.xmldata` standard library | TharmiganK | review required | `530706e70` |
| [#1437](https://github.com/ballerina-nutcracker/ballerina/pull/1437) | feat(stdlib): add `ballerina/cache` standard library | TharmiganK | review required | `b2d2ea24e` |
| [#1607](https://github.com/ballerina-nutcracker/ballerina/pull/1607) | chore(lint): enable modernize and modernize Go code | heshanpadmasiri | review required | `c53f03fb4` |
| [#1611](https://github.com/ballerina-nutcracker/ballerina/pull/1611) | refactor(nodes): keep shared base types private | heshanpadmasiri | review required | `bd8ea77c3` |

## Waiting for CI (2)

0 findings, no conflicts, reviewed at the current head; merge-ready once CI passes.

| PR | Title | Author | Approval | CI |
|---|---|---|---|---|
| [#1446](https://github.com/ballerina-nutcracker/ballerina/pull/1446) | feat(stdlib): add `ballerina/ftp` standard library | TharmiganK | review required | CI pending (1) |
| [#1567](https://github.com/ballerina-nutcracker/ballerina/pull/1567) | feat(ls): add initial completion support | nipunayf | review required | CI pending (2) |

## Not ready (52)

open findings: 30 · CI failed: 5 · conflicting: 10 · not reviewed at current head: 6 · approved at head; our review is older: 1

| PR | Title | Author | Why |
|---|---|---|---|
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | conflicting |
| [#921](https://github.com/ballerina-nutcracker/ballerina/pull/921) | feat: support compiler plugins | heshanpadmasiri | approved at head; our review is older |
| [#925](https://github.com/ballerina-nutcracker/ballerina/pull/925) | feat(semantics): use record defaults in constant mappings | heshanpadmasiri | open findings: 1 Verify, 2 Nits |
| [#926](https://github.com/ballerina-nutcracker/ballerina/pull/926) | fix(semantics): analyze constant type descriptors separately | heshanpadmasiri | open findings: 1 Nit |
| [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) | perf(projects): fix parallelization issue | azinneera | open findings: 3 Nits |
| [#1053](https://github.com/ballerina-nutcracker/ballerina/pull/1053) | fix(types): treat readonly class values as readonly | heshanpadmasiri | conflicting |
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title |
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | conflicting |
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
| [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) | feat(runtime): expose annotations of nested field types | warunalakshitha | not reviewed at current head |
| [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) | fix(semantics): carry annotations on inferred typedesc args | warunalakshitha | not reviewed at current head |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sor | warunalakshitha | open findings: 1 Important, 2 Verify, 3 Nits |
| [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) | fix(http): send http:Request message headers and type client | TharmiganK | open findings: 2 Nits |
| [#1476](https://github.com/ballerina-nutcracker/ballerina/pull/1476) | fix(parser): normalize source newlines and BOM | snelusha | conflicting |
| [#1480](https://github.com/ballerina-nutcracker/ballerina/pull/1480) | feat(workflow): bundle ballerina/workflow with an in-memory  | hasithaa | open findings: 8 Nits |
| [#1481](https://github.com/ballerina-nutcracker/ballerina/pull/1481) | fix(semantics): reject writes to final object fields outside | heshanpadmasiri | conflicting |
| [#1495](https://github.com/ballerina-nutcracker/ballerina/pull/1495) | test: clean up constant folding skip list | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title, Ubuntu Native Build |
| [#1508](https://github.com/ballerina-nutcracker/ballerina/pull/1508) | feat: introduce the test framework | azinneera | conflicting |
| [#1517](https://github.com/ballerina-nutcracker/ballerina/pull/1517) | fix: reject non-private non-isolated fields in isolated obje | heshanpadmasiri | open findings: 3 Nits |
| [#1536](https://github.com/ballerina-nutcracker/ballerina/pull/1536) | feat(ls): add signature help support | nipunayf | not reviewed at current head |
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

**#1536 shows "not reviewed at current head" because its author pushed `1db3706a9` at 12:45, after this round refreshed it at `be5a65917`.** The next round will pick it up.

## This round

| PR | Verdict | New Important/Verify findings | Summary |
|---|---|---|---|
| #701 | READY except approval. Rebase only: no PR code changed, and the rebased BIR goldens pass. | — | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/701#issuecomment-6161724644) |
| #1390 | READY except approval (2 PR-level Nits: unsquashed corrections, stale body). The earlier Important (row-index presize) is fixed: 10.1 s → 0.045 s. | — | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1390#issuecomment-6385533098) |
| #1391 | NOT READY | 🔴 A union target with a scalar-subtype member (`R\|"none"`, enum, `byte`) is classified again for every value, so cost is quadratic: a 20k-element array takes 13.7–21 s, jBallerina 0.03 s. An independent check reproduced it. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1391#issuecomment-6385685350) |
| #1422 | NOT READY | 🔴 Still open from last round: correction commits aren't fixups, and the 3 new commits add more. The 11 new Nits cover: a wrong README empty-value note (2 places), a stale body, a stale `!!str` comment, and 7 corpus files that don't cite their upstream issue. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1422#issuecomment-6385842883) |
| #1438 | NOT READY (new) | 🔴 The subset10.md Import declarations list omits `pop`/`shift`/`unshift`/`reduce`/`sort`/`SortDirection`.<br>🟡 `shift()` on `[int, int\|string...]` is a compile error, but the spec says it completes. Question to the author: document it or relax the check?<br>🟡 `unshift()` with no values on a fixed-length list is a compile error, but the spec says it completes. Same question. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1438#issuecomment-6817254010) |
| #1465 | READY except approval (2 PR-level Nits: unsquashed corrections, stale body on #830 resource methods). All 10 earlier findings are fixed. | — | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1465#issuecomment-6447242358) |
| #1536 | Summary refreshed, no re-review: rebased with the same diff. The body nit is fixed, and the commit-squash nit was restated with the current SHAs. 1 Nit open. The head has since moved again. | — | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1536#issuecomment-6624746231) |
| #1567 | Summary refreshed, no re-review: rebased and squashed into 8 clean commits with the same diff, and the body updated. 0 findings (20 fixed, 7 answered). | — | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1567#issuecomment-6652025430) |

## Skipped
- **Conflicting with main:** #1165, #1233, #1263, #1481.
- **Worker stack #1189 → #1221 → #1238:** every PR in the stack conflicts.
- **#1625:** conflicts. Its base `ci/langlib-coverage-pre-push` has no open PR.
- **Not checked:** none.

## Filed issues
None. The #1391 agent noted that an unused `foreach int i` variable is a compile error. It didn't check this against the spec or jBallerina, and #1263 (open) is the PR that turns unused variables into warnings, so I didn't file it.

## Review-skill updates
None. No PR reviewed this round changes AGENTS.md, skills, lint config, hooks or CI validators.

## Retrospective inputs

| PR | Kind | Description | Link |
|---|---|---|---|
| #1390 | missed | CodeRabbit: the union fail-safe `OVERWRITE` log was lost. | [#1390](https://github.com/ballerina-nutcracker/ballerina/pull/1390) |
| #1390 | missed | CodeRabbit: the skipLines range expansion blew up memory. | [#1390](https://github.com/ballerina-nutcracker/ballerina/pull/1390) |
| #1390 | recurring | Unsquashed correction commits and the stale PR body existed in earlier rounds but were raised only now. | [#1390](https://github.com/ballerina-nutcracker/ballerina/pull/1390) |
| #1390 | lint candidate | Flag a PR body that still says "Depends on #N" after #N has merged. Also flagged on #1391. | [#1390](https://github.com/ballerina-nutcracker/ballerina/pull/1390) |
| #1391 | wrong | Earlier rounds counted `classify-quadratic-ephemeral-atoms` fixed (author: "Fixed in 38120d9ea"). It is still quadratic and is re-raised under a new id. | [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) |
| #1391 | missed | CodeRabbit: the `@jsondata:Name` annotation key issue. | [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) |
| #1391 | recurring | Unsquashed review-fix commits were missed in earlier rounds. | [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) |
| #1391 | lint candidate | A scaling check: run union-with-scalar-singleton targets at 2× input size. | [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) |
| #1422 | missed | CodeRabbit: quoting of flow indicators and `...`, the `%TAG` reset, and the duplicate-key template message. | [#1422](https://github.com/ballerina-nutcracker/ballerina/pull/1422) |
| #1422 | lint candidate | Flag `corpus/lib` `-v.bal` files whose package README links upstream fixes but which cite no `ballerina-library#` issue. | [#1422](https://github.com/ballerina-nutcracker/ballerina/pull/1422) |
| #1422 | lint candidate | Check that the test files a PR body lists exist and that the list is complete. | [#1422](https://github.com/ballerina-nutcracker/ballerina/pull/1422) |
| #1438 | missed | heshanpadmasiri: a `reduce` callback that shrinks the array caused a raw Go panic. We reasoned about the case but didn't run it. | [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) |
| #1438 | lint candidate | Check that the subset doc's lang.array/map method-call list and its Import declarations list match. | [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) |
| #1465 | missed | TharmiganK self-review: server-side `http:Request` typing (root cause of #1464 for inbound requests). Earlier rounds missed it. | [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) |
| #1465 | missed | Small efficiency items: the `rawRequestHeaders` copy and the second pass for `Server`. | [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) |
| #1465 | lint candidate | Detect unsquashed correction commits (fix/revert subjects touching the same files as an earlier commit on the PR). Also flagged on #1390, #1391 and #1422. | [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) |
| #1536 / #1567 | wrong | My first refresh reposted commit-squash nits naming SHAs that rebases had removed, and body nits the authors had already fixed. I corrected both summaries within minutes, after the routine's new re-check rule. | [#1536](https://github.com/ballerina-nutcracker/ballerina/pull/1536#issuecomment-6624746231), [#1567](https://github.com/ballerina-nutcracker/ballerina/pull/1567#issuecomment-6652025430) |

Flaky test: one `TestLibIntegration -race` failure outside data-yaml during the #1422 review passed on rerun; its name wasn't captured. Every post succeeded, and nothing was committed or pushed.

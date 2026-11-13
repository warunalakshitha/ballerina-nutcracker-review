# Review round · 2026-11-13 16:03 Asia/Colombo

`pr730remote/main` at `d69c341a5` · ended 2026-11-13 16:31 · no tooling gaps (`bal` and `golangci-lint` both present)

**Open PRs: 70** · can merge: 7 (2 in merge queue, 3 ready, 2 after CI) · cannot merge: 60 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 0

## Can merge (7)

0 findings, no conflicts, reviewed at the current head, not waiting on another PR.

| PR | Title | Author | Approval | Auto-merge | Status |
|---|---|---|---|---|---|
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | approved | — | in merge queue (#1, awaiting checks) |
| [#1495](https://github.com/ballerina-nutcracker/ballerina/pull/1495) | test: clean up constant folding skip list | heshanpadmasiri | approved | — | in merge queue (#2, awaiting checks) |
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | review required | — | ready |
| [#1254](https://github.com/ballerina-nutcracker/ballerina/pull/1254) | test(corpus): cover error-typed wildcards in query clauses | heshanpadmasiri | review required | on (rebase, heshanpadmasiri) | ready |
| [#1255](https://github.com/ballerina-nutcracker/ballerina/pull/1255) | fix(nodebuilder): allow start actions in type casts and query selects | heshanpadmasiri | review required | — | ready |
| [#1377](https://github.com/ballerina-nutcracker/ballerina/pull/1377) | fix(projects): parse module documents into a slice indexed by position | azinneera | approved | on (rebase, warunalakshitha) | after CI pending (9) |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sort | warunalakshitha | review required | — | after CI pending (8) |

## Cannot merge (60)

open findings: 40 · CI failed: 8 · conflicting: 8 · stacked on conflicting: 2 · base already merged: 1 · stacked: 1

Auto-merge on a PR here merges it once GitHub's requirements pass, open findings or not.

| PR | Title | Author | Auto-merge | Why |
|---|---|---|---|---|
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | — | conflicting |
| [#701](https://github.com/ballerina-nutcracker/ballerina/pull/701) | feat(tcp): port ballerina/tcp standard library | TharmiganK | — | open findings: 2 Verify, 4 Nits |
| [#925](https://github.com/ballerina-nutcracker/ballerina/pull/925) | feat(semantics): use record defaults in constant mappings | heshanpadmasiri | — | open findings: 1 Verify, 2 Nits |
| [#926](https://github.com/ballerina-nutcracker/ballerina/pull/926) | fix(semantics): analyze constant type descriptors separately | heshanpadmasiri | on (rebase, heshanpadmasiri) | open findings: 1 Nit |
| [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) | perf(projects): fix parallelization issue | azinneera | — | open findings: 1 Important, 7 Nits |
| [#1053](https://github.com/ballerina-nutcracker/ballerina/pull/1053) | fix(types): treat readonly class values as readonly | heshanpadmasiri | — | conflicting |
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
| [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) | feat(runtime): expose annotations of nested field types | warunalakshitha | — | open findings: 1 Important, 2 Nits |
| [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) | fix(semantics): carry annotations on inferred typedesc args | warunalakshitha | — | open findings: 1 Important, 1 Nit |
| [#1437](https://github.com/ballerina-nutcracker/ballerina/pull/1437) | feat(stdlib): add `ballerina/cache` standard library | TharmiganK | — | open findings: 3 Nits |
| [#1446](https://github.com/ballerina-nutcracker/ballerina/pull/1446) | feat(stdlib): add `ballerina/ftp` standard library | TharmiganK | — | open findings: 4 Nits |
| [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) | fix(http): send http:Request message headers and type client | TharmiganK | — | open findings: 2 Nits |
| [#1476](https://github.com/ballerina-nutcracker/ballerina/pull/1476) | fix(parser): normalize source newlines and BOM | snelusha | — | conflicting |
| [#1480](https://github.com/ballerina-nutcracker/ballerina/pull/1480) | feat(workflow): bundle ballerina/workflow with an in-memory  | hasithaa | — | open findings: 8 Nits |
| [#1481](https://github.com/ballerina-nutcracker/ballerina/pull/1481) | fix(semantics): reject writes to final object fields outside | heshanpadmasiri | — | conflicting |
| [#1508](https://github.com/ballerina-nutcracker/ballerina/pull/1508) | feat: introduce the test framework | azinneera | — | open findings: 2 Important, 3 Verify, 15 Nits |
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
| [#1623](https://github.com/ballerina-nutcracker/ballerina/pull/1623) | ci(nightly): add nightly flake sniffer and actionlint | heshanpadmasiri | — | open findings: 5 Nits |
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

## This round

All five PRs below had new commits and were re-reviewed; none is ready to merge.

| PR | Verdict | New Important/Verify findings | Summary |
|---|---|---|---|
| #701 | NOT READY (2 Verify, 4 Nits) | **Verify** `tcp-client-ciphers-fallback` (tls.go:126-128): a client given only unknown `ciphers` names falls back to Go's default suites and connects, and a TLS 1.3 suite restriction is ignored; jBallerina fails both handshakes. Return `tcp:Error`, or document?<br>**Verify** `tcp-listener-ciphers-fallback` (tls.go:169-171): the same question for the listener, which falls back silently. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/701#issuecomment-6161724644) |
| #1415 | NOT READY (1 Important, 1 Verify, 7 Nits) | **Important** `xml-wellformedness-remaining-sites` (stax.go:225): the StAX reader still accepts malformed XML: a DOCTYPE inside the root or in the epilog, CDATA in the prolog, and `version = 'abc'`. jBallerina and XML 1.0 reject all four.<br>**Verify** `xml-declaration-version-1-1-rejected` (stax.go:216): `version='1.1'` is rejected, but jBallerina accepts it and XML 1.0 §2.8 says to process it as 1.0. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1415#issuecomment-6489172644) |
| #1437 | NOT READY (3 PR-level Nits) | None. The new commit is comment-only and fixes our 3 earlier findings. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1437#issuecomment-6489017303) |
| #1446 | NOT READY (4 PR-level Nits) | None. The README row fix closes our earlier `readme-closed-issue-1360` finding. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1446#issuecomment-6489164987) |
| #1508 | NOT READY (2 Important, 3 Verify, 15 Nits) | **Important** `merge-commits-dont-build`: merge commits f2b880223 and 423588be6 don't build on their own (an empty `compilation_stats.go`; `GetDeterminedType` undefined).<br>**Important** `stdlib-readme-missing`: ballerina/test has no README support table and no `doc/library` row or subset3 section, so the missing mocking API (`mock`, `when`, `MockObject`, …) isn't declared.<br>**Verify** `running-tests-header`: the `Running Tests` header jBallerina prints is missing.<br>The `testerror-name-match-*` Verify questions are still open from last round. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1508#issuecomment-6525640999) |

Posting notes:
- **#701:** the dry run flagged two overlaps with resolved threads. Neither is a duplicate: TharmiganK's thread is about `handshakeTimeout` and daneshk's is about a signature note. I shortened one body to fit the length limit.
- **#1415:** I shortened one body to fit the length limit.
- **#1508:** I posted with `--ignore-warnings`. The only warnings were "no `main`" on two repros, which are `bal test` programs and can't have a `main`.

## Skipped
- **Conflicting with main:**
  - #1189, #1221, #1238: one stack whose bottom PR, #1189, conflicts
  - #1233
  - #1263
  - #1481
  - #1625: its base #1584 is already merged and it conflicts with main
- **Not checked:** none.

## Filed issues
None.
- **#701:** the agent checked the suspected cipher-fallback bug on main. For http, main behaves the same as jBallerina, so it only matters for tcp, which the #701 findings already cover.
- **#1508:** the agent saw that `runCompilerPlugins` stops after the first plugin that reports errors. That is main's design from #921, not a bug, so I didn't file it.

## Review-skill updates
None. No reviewed PR changes AGENTS.md, skills, lint config, hooks or CI validators.

## Retrospective inputs

| PR | Kind | Description | Link |
|---|---|---|---|
| #701 | missed | Four README NBC bullets for jBallerina defects have no ballerina-library issue link. Earlier rounds of ours missed this, and it was raised only now. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/701#issuecomment-6161724644) |
| #701 | lint candidate | A check that fails when a package README NBC bullet says "bug in the reference implementation" without a `ballerina-library/issues/` link. | — |
| #701 | wasted | The agent handed back before its independent verifier finished, so the cipher findings needed a second pass. | — |
| #1415 | recurring | XML well-formedness gaps in the StAX reader keep surfacing one review at a time; this is the third round of the same class. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1415#issuecomment-6489172644) |
| #1415 | lint candidate | A table-driven or differential test of the StAX reader against `values/xml_parse.go` or Woodstox for XML 1.0 well-formedness cases. | — |
| #1508 | lint candidate | A CI step that builds each commit, which would have caught both broken merges, and running the license-header check in CI, not only in the commit hook. | — |
| #1508 | wasted | `post_review.py`'s "no `main`" check fires on `bal test` repros, which forced `--ignore-warnings`. It should exempt programs marked `run bal test`. | — |
| #1508 | wasted | The last summary's `skill=472e025e` matches no commit in the tools repo, so the agent couldn't find which rules were new and checked every rule added since `0b88f9f`. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1508#issuecomment-6525640999) |

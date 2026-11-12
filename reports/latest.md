# Review round · 2026-11-12 20:53 Asia/Colombo

`pr730remote/main` is at `d69c341a5`. The round ended at 2026-11-12 21:33. No tooling gaps: `gh` auth, `bal` and `golangci-lint` were all available.

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

open findings: 30 · CI failed: 5 · conflicting: 10 · not reviewed at current head: 12

| PR | Title | Author | Why |
|---|---|---|---|
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | conflicting |
| [#925](https://github.com/ballerina-nutcracker/ballerina/pull/925) | feat(semantics): use record defaults in constant mappings | heshanpadmasiri | open findings: 1 Verify, 2 Nits |
| [#926](https://github.com/ballerina-nutcracker/ballerina/pull/926) | fix(semantics): analyze constant type descriptors separately | heshanpadmasiri | open findings: 1 Nit |
| [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) | perf(projects): fix parallelization issue | azinneera | conflicting |
| [#1053](https://github.com/ballerina-nutcracker/ballerina/pull/1053) | fix(types): treat readonly class values as readonly | heshanpadmasiri | conflicting |
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title |
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | not reviewed at current head |
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
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sor | warunalakshitha | not reviewed at current head |
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
| [#1642](https://github.com/ballerina-nutcracker/ballerina/pull/1642) | fix(types): resolve annotations on live variables and neste | heshanpadmasiri | not reviewed at current head |

## This round

| PR | Verdict | New Important / Verify findings | Summary |
|---|---|---|---|
| #1536 | **NOT READY**: 4 Important, 8 Verify, 10 Nits | 🔴 `sig-unclosed-call-absorbs-next-statement`: `add(1, ` followed by an assignment line gives activeParameter 3 instead of 1; lang-lib calls get `null`<br>🔴 `sig-union-receiver-arg-types`: a method call on an `A\|B` receiver shows the arguments as the label, e.g. `m(1, "q")`<br>🔴 `sig-monomorphic-langlib-docs`: `arr.indexOf(` has no docs because the lookup uses the monomorphized ref<br>🔴 `sig-sibling-module-docs`: no docs for callees in a sibling module of the same package<br>🟡 `sig-out-of-range-active-parameter`: LSP 3.18 treats an out-of-range `activeParameter` as 0<br>🟡 `sig-callee-name-of-nested-call`: `add(1, ‸g(2))` returns `null`<br>🟡 `sig-names-only-drops-methods`: one undefined name in the module makes method, `new` and lang-lib help return `null`<br>🟡 `sig-new-paren-text-scan`: `new Box // c` then `(` on the next line gives no help<br>🟡 `sig-object-type-method-docs`: no docs when the receiver is typed as an object type<br>🟡 `sig-unused-context-drops-help`: an invalid `context`, which the handler never reads, makes the result `null`<br>🟡 `sig-stale-on-callee-file-edit`: an edit to the callee's file right after the request returned the old signature in 7 of 16 rounds<br>🟡 `sig-errored-dependency-kills-help`: an unused variable in an imported module makes help return `null` in every module that imports it | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1536#issuecomment-6624746231) |

- **What was posted:** the summary comment was updated, plus 21 new inline threads. Nothing was resolved, and no replies or issues were posted.
- **Earlier findings:** all 21 earlier code findings are fixed or resolved. The PR-level Nit "Later commits rewrite fixtures the first commit adds" is still open.
- **Coverage of the new `ls-review.md` sections:**
  - The new section 3 checks gave `sig-out-of-range-active-parameter` and `sig-malformed-params-null`.
  - Section 6 (callee location, receiver shape, cursor boundaries, compile stage, rendered output) was probed on the real server.
  - Section 7 fixtures and harness were checked. The PR adds no dev tools to run.
  - Section 9 got one subagent per package, plus the section 5 end-to-end trace.
- **Verification:** an independent fresh subagent re-ran all 12 Important/Verify findings at head, and all reproduced.
- **Checks:** `go vet ./ls/...`, `go test ./ls/...` and `go test -race -count=5 ./ls/...` pass, each of the 5 commits builds on its own, and CI is green.
- **reviewed_diff:** `gh pr diff` returned HTTP 406 because the PR has 316 files, so `reviewed_diff` is the sha256 of `git diff <merge-base> <head>`.
- **Overlap kept:** `sig-markdown-first-config-name` was flagged as overlapping hasithaa's resolved thread. I kept it because that thread named 4 fixtures, all of which were fixed, and this config wasn't one of them. The body says so.

## Skipped
- None. Only PR 1536 was in scope, and it merges cleanly.

## Filed issues
- None. The out-of-scope items can't be reproduced through features on main, because main's LS has no hover or other position-based requests:
  - A `# # Deprecated` section drops the last parameter's doc (`nodebuilder/node_builder.go:739`).
  - A line past EOF gets -32602 or a clamp depending on whether the file ends with a newline.
  - A wrongly typed capability makes `initialize` fail.

  They will surface once features that use them land.

## Review-skill updates
- None from the PR: it changes no process files.
- Agent suggestion for `ls-review.md` section 3 ("spec defaults"): when no spec-conforming value exists, as with an out-of-range `activeParameter`, post the finding as Verify.

## Retrospective inputs

| PR | Kind | Description | Link |
|---|---|---|---|
| #1536 | missed | Earlier rounds missed hasithaa's expanded type labels and fenced-code doc rendering. The new section 6 "read the rendered output" check would catch both. | [PR](https://github.com/ballerina-nutcracker/ballerina/pull/1536) |
| #1536 | missed | Earlier rounds missed 4 Important bugs: unclosed call before an assignment, union receiver, generic lang-lib docs, sibling-module docs. They were found only with the new section 6 probes. | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1536#issuecomment-6624746231) |
| #1536 | wasted | The review agent handed back twice before its own package subagents finished. It blamed the handback check, not the coordinator. I re-ran s4, s5 and the verifiers from the coordinator. agent-instructions.md could tell agents to run package subagents in the foreground. | n/a |
| #1536 | lint candidate | None. | n/a |

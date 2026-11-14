# Review round · 2026-11-14 06:07

`origin/main` cbe12629d · skills 7ec5b15 · ended 2026-11-14 06:37 · tooling: all pinned versions present (golangci-lint 2.15.0 built with go1.26 refused go1.27.1; the agent built a per-PR copy with GOTOOLCHAIN=go1.27.1) · **POSTING FAILED: HTTP 403 "Resource not accessible by integration" on ballerina-nutcracker/ballerina; nothing was posted.** The Gate checks only read access, so this was not caught earlier. Fix: install the Claude GitHub App on the repo or reconnect GitHub in claude.ai settings.

**Open PRs: 68** · can merge: 5 (? in merge queue, 5 ready, 0 after CI) · cannot merge: 60 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 0

## Can merge (5)

Couldn't read the merge queue; a queued PR shows as `ready` here.

0 findings, no conflicts, reviewed at the current head, not waiting on another PR.

| PR | Title | Author | Approval | Auto-merge | Status |
|---|---|---|---|---|---|
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | approved | — | ready |
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | review required | — | ready |
| [#1254](https://github.com/ballerina-nutcracker/ballerina/pull/1254) | test(corpus): cover error-typed wildcards in query clauses | heshanpadmasiri | review required | on (rebase, heshanpadmasiri) | ready |
| [#1255](https://github.com/ballerina-nutcracker/ballerina/pull/1255) | fix(nodebuilder): allow start actions in type casts and query selects | heshanpadmasiri | review required | — | ready |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sort | warunalakshitha | review required | — | ready |

## Cannot merge (60)

open findings: 37 · CI failed: 8 · conflicting: 9 · stacked on conflicting: 2 · base already merged: 1 · stacked: 1 · awaiting re-review: 2

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
| [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) | feat(runtime): expose annotations of nested field types | warunalakshitha | — | awaiting re-review: pushed since our review of `edf01a7bf` |
| [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) | fix(semantics): carry annotations on inferred typedesc args | warunalakshitha | — | awaiting re-review: pushed since our review of `4a0cafb3c` |
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

| PR | verdict | new Important/Verify | summary link |
|---|---|---|---|
| #1434 | READY except approval (3 Nits: PR/commit level) | none | not posted (403); previewed below |
| #1435 | READY except approval (5 Nits) | none | not posted (403); previewed below |

Both reviewed as a stack at the tip, bfe316b40. #1434's own diff is unchanged (only re-split commits), so its summary was refreshed. #1435 got a full re-review. Earlier Important findings ("commit doesn't build") are FIXED on both. Every commit now builds.

### Unposted findings (post by hand or let the next round post them)
**#1434** (summary comment 6506053463):
- 🔵 pr: 77084a87b only moves `namedTypeRef` + helpers added by f17c7c1d1 into `common/named_types.go`; squash with `--fixup=f17c7c1d1`.
- 🔵 pr: 709a8640e fixes #1527 (head `{"s":"a","left":null,"n":5}`, main `{"s":"a"}`) but the body doesn't close it; add `Fixes #1527`.
- 🔵 pr: body skips the template's Purpose/Approach/Checklist sections.

**#1435** (summary comment 6720717565):
- 🔵 `semantics/internal/types/type_resolver.go:9106-9107`: the named types for function-type parameter defaults are untested. A mutation to `nil` passes every test. Add `function (Person|error value = annotatedFieldsInferred()) returns string fnWithDefault = fieldsOf; io:println(fnWithDefault()); //@output active,age,dynamic,name` to `record-field-annotations-v`.
- 🔵 pr: 2f7ac76f4 reworks what 6ae4744c6 adds; squash with `--fixup=6ae4744c6`.
- 🔵 pr: the head fixes #1496, #1497 and #1498, but the body doesn't close them.
- 🔵 pr: the body doesn't describe bfe316b40's fix (a later-declared dependently-typed callee caused INTERNAL_ERROR on the base) or the record-field/function-type defaults.
- 🔵 pr: body skips the template's Purpose/Approach/Checklist sections.

Full previews: `$SP/review-out/{1434,1435}/pr-comment.md` (cleared with the session). Because nothing was posted, the next round will re-review both PRs.

## Skipped
- #1189: conflicting with main.
- #1221 and #1238: stacked on conflicting #1189.
- #1233: conflicting.
- #1263: conflicting.
- #1481: conflicting.
- #1625: conflicting; its base #1584 is already merged, so it needs a rebase onto main.

## Filed issues
None. The out-of-scope bug the agent found (a compiler stack overflow when a parameter default calls its own function) is already #1648. Suggest adding to #1648: with #1435's bfe316b40, a dependently-typed self-calling default (`function inferred(int val = inferred(0), typedesc retTy = <>)`) now overflows the stack too. On the base it gave INTERNAL_ERROR.

## Review-skill updates
None. Neither PR touches AGENTS.md, skills, lint config, hooks or CI.

Proposed round-procedure fix (not applied):
- Add a write-access check to cloud-round.md §4 Gate, for example a dry PATCH probe or `check_repo_access`. That way a round with read-only GitHub access stops before it reviews.
- Note that the shared golangci-lint needs `GOTOOLCHAIN=go1.27.1` at install time.

## Retrospective inputs

| PR | kind | description | link |
|---|---|---|---|
| #1434 | missed | heshanpadmasiri's design objection to side tables and per-stage caches for annotation data (`declaredNamedTypes`, `TypeRef`, `typeDescCache`). Our "Data smuggled past accessors" check covers it, but we didn't raise it. | https://github.com/ballerina-nutcracker/ballerina/pull/1434 |
| #1435 | missed | CodeRabbit: default providers passed `nil` named types. The last round missed it; it is fixed at the tip. | https://github.com/ballerina-nutcracker/ballerina/pull/1435 |
| #1434 | lint candidate | Flag a later commit that only moves or renames symbols an earlier commit on the same PR added. | https://github.com/ballerina-nutcracker/ballerina/pull/1434 |
| #1435 | lint candidate | Mutation check: flip each new `namedTypes` argument to `nil` and require a test to fail. | https://github.com/ballerina-nutcracker/ballerina/pull/1435 |

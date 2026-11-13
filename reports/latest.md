# Review round · 2026-11-13 18:02
`origin/main` d69c341a5 · skills 73abf22 · ended 2026-11-13 18:48 · gaps: **posting failed (no write access, see below)**; lint not run by the agent (its golangci-lint 2.15.0 was built with go1.26, older than the repo's go 1.27.1); go.dev download blocked (Go 1.27.1 fetched through the module proxy instead).

> ⚠️ **Nothing was posted this round.** Every write to ballerina-nutcracker/ballerina failed with 403 "Resource not accessible by integration", after repeated 502/503 "credential service unavailable" errors. `check_repo_access` reports `repo_not_connected`: Claude doesn't have GitHub access to ballerina-nutcracker/ballerina for this org. Reads still work. To fix it, reconnect GitHub at claude.ai/customize/connectors, or have an org admin install the Claude GitHub App. The comments below are ready to post by hand. The recorded last scan leaves out #1434 and #1435, so the next round won't skip as unchanged and will retry them.

**Open PRs: 70** · can merge: 7 (? in merge queue, 5 ready, 2 after CI) · cannot merge: 60 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 0

## Can merge (7)

Couldn't read the merge queue; a queued PR shows as `ready` here.

0 findings, no conflicts, reviewed at the current head, not waiting on another PR.

| PR | Title | Author | Approval | Auto-merge | Status |
|---|---|---|---|---|---|
| [#1098](https://github.com/ballerina-nutcracker/ballerina/pull/1098) | fix(semantics): widen unary - and ~ result to the basic type | heshanpadmasiri | approved | — | ready |
| [#1165](https://github.com/ballerina-nutcracker/ballerina/pull/1165) | fix(runtime): fill record field defaults in cloneWithType | warunalakshitha | review required | — | ready |
| [#1254](https://github.com/ballerina-nutcracker/ballerina/pull/1254) | test(corpus): cover error-typed wildcards in query clauses | heshanpadmasiri | review required | on (rebase, heshanpadmasiri) | ready |
| [#1255](https://github.com/ballerina-nutcracker/ballerina/pull/1255) | fix(nodebuilder): allow start actions in type casts and query selects | heshanpadmasiri | review required | — | ready |
| [#1377](https://github.com/ballerina-nutcracker/ballerina/pull/1377) | fix(projects): parse module documents into a slice indexed by position | azinneera | approved | — | after CI pending (2) |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sort | warunalakshitha | review required | — | after CI pending (2) |
| [#1495](https://github.com/ballerina-nutcracker/ballerina/pull/1495) | test: clean up constant folding skip list | heshanpadmasiri | approved | — | ready |

## Cannot merge (60)

open findings: 38 · CI failed: 8 · conflicting: 8 · stacked on conflicting: 2 · base already merged: 1 · stacked: 1 · awaiting re-review: 2

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

| PR | Verdict | New Important/Verify | Summary |
|---|---|---|---|
| #1434 | Nits only: 3 Nits (8 fixed, 1 answered). Refresh: own diff unchanged since `edf01a7bf`. | none | not posted (403) |
| #1435 | Not ready: 1 Verify, 4 Nits (3 fixed) | 🟡 `dependent-default-cycle-crash` (type_resolver.go:7966): cyclic defaults through a dependently typed callee now overflow the Go stack. Main gives INTERNAL_ERROR; jBallerina compiles it. The author decides whether to guard here or leave it to #1648. | not posted (403) |

## Skipped
- Conflicting with main: #1189, #1233, #1263, #1481.
- Stacked on conflicting #1189: #1221, #1238.
- #1625: its base was already merged and it conflicts with main.
- Not checked: none.

## Filed issues
None. #1648 (cyclic plain defaults overflow the stack) is already open. #1326 is fixed by #1435's bfe316b40.

## Review-skill updates
None. Neither PR changes AGENTS.md, skills, lint config, hooks or CI.

## Retrospective inputs

| PR | Kind | Item | Link |
|---|---|---|---|
| #1435 | missed | Record-field and function-type parameter defaults passed `nil` named types; CodeRabbit raised it and we didn't. After a "carry X through all contexts" change, a review should list every call site of `resolveDefaultExpression` and similar functions. | https://github.com/ballerina-nutcracker/ballerina/pull/1435 |
| #1434 | recurring | A refactor commit kept separate from the feature commit it reworks. The author fixed only the build break, so the squash advice was re-raised as a nit. | https://github.com/ballerina-nutcracker/ballerina/pull/1434 |
| #1435 | recurring | Same as #1434. | https://github.com/ballerina-nutcracker/ballerina/pull/1435 |
| #1435 | lint candidate | A grep check for `resolveDefaultExpression(..., nil)` and `resolveWithNamedTypes(..., nil)`. | https://github.com/ballerina-nutcracker/ballerina/pull/1435 |

## Unposted comments (post by hand)
For each PR: the summary comment edits our existing summary comment (id shown), and each line comment goes on a review.

### #1434

## Summary comment (update 6506053463)

<!-- pre-pr-review:summary pr=1434 diff=6ecf04ac skill=b19e979f -->
## 🤖 PR review summary · #1434
🔵 **3 Nits** (8 fixed, 1 answered) · reviewed `77084a87b`.
Stack: **#1434** → #1435 · reviewed as a unit at `bfe316b40`.
Checked: each commit built ✔ · tip go test ✔ · race -count=10 on touched tests ✔
CodeRabbit: 0 of 5 threads unresolved ✅.

- Read line by line: semantics/internal/{common/named_types.go, types/type_resolver.go}
- Subset doc: Updated: record-type-inclusion restriction (R declared first + back-reference); matches head and main
- Optional: TestRecordFieldAnnotationsCrossModule and TestRecordFieldAnnotationsSymbolPoolRoundtrip (bodies edited) lack t.Parallel()
- 🔵 **Nit** · 77084a87b only moves the `namedTypeRef` helper that f17c7c1d1 adds — Read: 77084a87b moves `namedTypeRef`, added by f17c7c1d1 in `type_resolver.go`, into `common` as `NamedTypeRef`; every commit now builds. Squash it into f17c7c1d1 (`git commit --fixup`, autosquash) so the helper lands in `common` directly.
- 🔵 **Nit** · 709a8640e fixes #1527 but the body doesn't close it — Measured: #1527's program prints `{"s":"a","left":null,"n":5}` at head (main: `{"s":"a"}`), and the new test covers it; #1527 is still open. Add `Fixes #1527`.
- 🔵 **Nit** · PR body skips the template's Purpose, Approach and Checklist sections — Read: the body uses Summary/Problem/How it's fixed/Changes headings instead of `.github/pull_request_template.md`'s `## Purpose` (with `Fixes #N` or a reason), `## Approach` and the checklist. Map the existing text onto those sections.

### #1435

## Summary comment (update 6720717565)

<!-- pre-pr-review:summary pr=1435 diff=f6c9355b skill=b19e979f -->
## 🤖 PR review summary · #1435
🟡 **1 Verify** · 🔵 **4 Nits** (3 fixed) · reviewed `bfe316b40`.
Stack: #1434 → **#1435** · reviewed as a unit at `bfe316b40`.
Checked: fails on main ✔ · jBallerina parity ✔ · each commit built ✔ · race -count=10 on touched tests ✔
CodeRabbit: 1 of 3 threads unresolved.

- Read line by line: semantics/internal/{common/named_types.go, symbols/symbol_resolver.go, types/type_resolver{,_loop,_state}.go}
- Subset doc: Not needed: entry for dependently-typed functions already accurate; fixes are crashes and typedesc metadata
- Optional: TestRecordFieldAnnotations{,CrossModule,SymbolPoolRoundtrip} (bodies edited) lack t.Parallel()
- 🔵 **Nit** · 2f7ac76f4 reworks the named-type plumbing 6ae4744c6 adds — Read: 2f7ac76f4 renames and moves what 6ae4744c6 adds (`resolveActionOrExpressionWithNamedTypes`, `common.NamedTypes`, signature named types) after review; every commit now builds. Squash it into 6ae4744c6 (`git commit --fixup`, autosquash).
- 🔵 **Nit** · bfe316b40 fixes #1326 but the body doesn't close it — Measured: #1326's program (a parameter default calling `conv`, declared later) compiles at head; main and the previous head report INTERNAL_ERROR `function parameter type not found`. #1326 is still open. Add `Fixes #1326`.
- 🔵 **Nit** · PR body skips the template's Purpose, Approach and Checklist sections — Read: the body uses Summary/Problem/How it's fixed/Changes headings instead of `.github/pull_request_template.md`'s `## Purpose` (with `Fixes #N` or a reason), `## Approach` and the checklist. Map the existing text onto those sections.

## line comment · semantics/internal/types/type_resolver.go:7966-7968 · new

<!-- pre-pr-review:finding id=dependent-default-cycle-crash -->

🤖 🟡 **Verify** · Correctness — **Cyclic defaults through a dependently typed callee now overflow the stack**

Measured: jBallerina compiles this; main reports INTERNAL_ERROR, head crashes with a Go stack overflow, because this `ensureResolved` re-enters `f`'s signature with no in-progress check. Plain functions already crash this way on main (#1648). Should this guard detect the re-entry, or is it left to #1648?

```ballerina
import ballerina/io;

function f(int n, int a = n > 0 ? g(n - 1) : 0) returns int => n + a;

// compile-only repro: g has no native
function g(int v, int w = f(v), typedesc<int> t = <>) returns t = external;

public function main() {
    io:println(f(2));
}
```

<details><summary>Output</summary>

```text
jBallerina: bal build: compiles
Nutcracker: head: fatal error: stack overflow (main: fatal[INTERNAL_ERROR]: function parameter type not found)
```
</details>

## line comment · semantics/internal/types/type_resolver.go:9106-9107 · new

<!-- pre-pr-review:finding id=fn-type-default-named-types-untested -->

🤖 🔵 **Nit** · Test — **Named types for function-type parameter defaults are untested**

Measured: passing `nil` here still passes `TestRecordFieldAnnotations`. With the case below added, head prints `active,age,dynamic,name` and the `nil` mutant fails. Add it so this default can't regress.

```ballerina
// record-field-annotations-v.bal, module level
type FieldsFn function (Person|error value = annotatedFieldsInferred()) returns string;

// in main
FieldsFn fn = function(Person|error value) returns string => fieldsOf(value);
io:println(fn()); //@output active,age,dynamic,name
```

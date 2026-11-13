# Review round · 2026-11-13 09:49

`pr730remote/main` `d69c341a5` · ended 2026-11-13 11:53 · tooling: no gaps (`bal`, `golangci-lint` present)

**Open PRs: 68** · merge-ready: 3 · waiting for CI: 1 · not ready: 61 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 0

## Merge-ready (3)

| PR | Title | Author | Approval | Reviewed |
|---|---|---|---|---|
| [#701](https://github.com/ballerina-nutcracker/ballerina/pull/701) | feat(tcp): port ballerina/tcp standard library | TharmiganK | review required | `c1b5afb31` |
| [#1415](https://github.com/ballerina-nutcracker/ballerina/pull/1415) | feat(data.xmldata): add `ballerina/data.xmldata` standard library | TharmiganK | review required | `530706e70` |
| [#1437](https://github.com/ballerina-nutcracker/ballerina/pull/1437) | feat(stdlib): add `ballerina/cache` standard library | TharmiganK | review required | `b2d2ea24e` |

## Waiting for CI (1)

0 findings, no conflicts, reviewed at the current head; merge-ready once CI passes.

| PR | Title | Author | Approval | CI |
|---|---|---|---|---|
| [#1446](https://github.com/ballerina-nutcracker/ballerina/pull/1446) | feat(stdlib): add `ballerina/ftp` standard library | TharmiganK | review required | CI pending (2) |

## Not ready (61)

open findings: 34 · CI failed: 13 · conflicting: 9 · stacked on conflicting: 2 · base already merged: 1 · awaiting re-review: 1 · awaiting first review: 1

| PR | Title | Author | Why |
|---|---|---|---|
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | conflicting |
| [#925](https://github.com/ballerina-nutcracker/ballerina/pull/925) | feat(semantics): use record defaults in constant mappings | heshanpadmasiri | open findings: 1 Verify, 2 Nits |
| [#926](https://github.com/ballerina-nutcracker/ballerina/pull/926) | fix(semantics): analyze constant type descriptors separately | heshanpadmasiri | open findings: 1 Nit |
| [#985](https://github.com/ballerina-nutcracker/ballerina/pull/985) | perf(projects): fix parallelization issue | azinneera | awaiting re-review: pushed since our review of `fae6e4a04` |
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
| [#1598](https://github.com/ballerina-nutcracker/ballerina/pull/1598) | fix(semantics): reject self in object field initializers | heshanpadmasiri | awaiting first review |
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
| [#1614](https://github.com/ballerina-nutcracker/ballerina/pull/1614) | chore(lint): enforce shallow declaration checks and fix find | heshanpadmasiri | CI failed: Benchmark memory main vs PR head, Benchmark HTTP base vs PR head, Benchmark time main vs PR head |
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

| PR | Verdict | New Important / Verify | Summary |
|---|---|---|---|
| #1391 | Ready except approval (4 Nits; last Important fixed) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1391#issuecomment-6385685350) |
| #1422 | Not ready: unsquashed correction commits (Important, open) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1422#issuecomment-6385842883) |
| #1434 | Not ready: commit 157b88a27 doesn't build (open) | none (both code findings fixed) | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1434#issuecomment-6506053463) |
| #1435 | Not ready: commit f9e9efa1c doesn't build (open) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1435#issuecomment-6720717565) |
| #1438 | Ready except approval (1 Nit) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1438#issuecomment-6817254010) |
| #1607 | 0 findings (refresh) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1607#issuecomment-6772773678) |
| #1608 | 0 findings (body Nit fixed) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1608#issuecomment-6772803394) |
| #1609 | 0 findings (commit-type Nit fixed) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1609#issuecomment-6772837482) |
| #1610 | 0 findings (refresh) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1610#issuecomment-6772861524) |
| #1611 | 0 findings (refresh) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1611#issuecomment-6772871406) |
| #1612 | 1 Nit | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1612#issuecomment-6772901261) |
| #1613 | Not ready | Verify `funcusage-exported-hook-deadlock`: an exported function used in production only in its own package and by other packages' tests can't pass funcusage with or without `//funcusage:test-hook` | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1613#issuecomment-6814601067) |
| #1614 | 0 findings (7 fixed, 2 answered) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1614#issuecomment-6814606413) |
| #1626 | 0 findings (body Nit fixed) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1626#issuecomment-6814614107) |
| #1631 | 0 findings (2 fixed, 1 answered) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1631#issuecomment-6814610640) |
| #1638 | 2 Nits (new PR) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1638#issuecomment-6845755385) |
| #1639 | Not ready (new PR) | Important `class-field-hides-type`: a class field named like a module type hides that type (`Unknown type: Name`; jBallerina prints `yx`) | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1639#issuecomment-6845761269) |
| #1640 | Not ready (new PR) | Important `xml-deferred-constraint-empty-type`: deferred `xml<R>` check loses or duplicates its error; debug build asserts | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1640#issuecomment-6845767294) |
| #1641 | 1 Nit (new PR) | none | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1641#issuecomment-6845773170) |
| #1642 | Not ready (new PR) | Important `field-annotation-value-ignores-narrowing` (record/object field annotations ignore `is` narrowing); Important `lambda-param-annotation-value-ignores-narrowing` (same for anonymous function params) | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1642#issuecomment-6845779334) |
| #1647 | Not ready (new PR) | Verify `lambda-record-default-wrong-frame`: a record-field default inside a lambda signature runs in the wrong frame (panic or empty line; expected 41). Base was already wrong, so the question is fix here or in a follow-up | [summary](https://github.com/ballerina-nutcracker/ballerina/pull/1647#issuecomment-6845785081) |

The stack #1609–#1647 was pushed again mid-review (about 05:35 UTC). It was re-queued and updated at the new heads before posting, so nothing was posted against a stale head.

## Skipped

- #1189: conflicting
- #1221: stacked on conflicting #1189
- #1233: conflicting
- #1238: stacked on conflicting #1189
- #1263: conflicting
- #1481: conflicting
- #1625: conflicting (its base #1584 is already merged; needs a rebase onto main)

## Filed issues

- #1656: module `init` that returns an error on one path reports a module variable as not initialized (from #1638)
- #1657: object field initializer can read a mutable module variable when the class has no `init` (from #1638)
- #1658: object field override errors report one member, chosen by map iteration order (from #1640)
- Comment on #1321: a `typedesc` parameter used as a local variable type is accepted (from #1639)

Not filed: these were found without a spec check or a duplicate search.
- After an "Unknown annotation" error, later annotation-value errors in the same function are dropped.
- `c.f()` on a function-typed class field fails at runtime with `function not found: f`; jBallerina prints 2.

## Review-skill updates (proposed by the #1612 / #1613 / #1614 review; not applied)

1. **SKILL.md:239, lint tiers:** change it to "A module moved to a looser tier, or a linter removed from a tier's config, is a finding." Our "unless the PR explains it" contradicts lint-setup, which allows no exception.
2. **SKILL.md:235:** "`make lint` (including walkpurity)" becomes "(including walkpurity, nodebase, funcusage, shallow)".
3. **funcusage (#1613)** contradicts SKILL.md:235 ("`unused` is disabled… nothing but `check_unused_symbols.py`") and :313 ("No linter reports either"). Reword both:
   - `make lint-func-usage` rejects functions in Strict-and-above modules that are unused, used only by tests, or exported but used only inside their own package. `test_util` uses don't count as production use, and the check runs on each build-specific declaration.
   - `check_unused_symbols.py` remains the only check for methods, types, consts, vars, fields and Basic-tier modules.
   - Step 6: don't raise UNUSED or TEST-ONLY hits on package-level functions in those modules.
   - New Nit: a `//funcusage:test-hook` on a function no test references.
4. **shallow (#1614):** in Strict-and-above modules `make lint-shallow` rejects single-call functions and one-embed wrappers, so don't raise those. Do check each `//shallow:allow` reason and look for leftover single-use temporaries. Don't make "keep forwarders" a finding class; the author inlines them on purpose (answered).
5. **lint-setup/SKILL.md:** in lint-config PRs, check that the tier table, the module lists (against go.work) and the Make targets stay consistent. Cite Make targets, not `Makefile:N` lines.
6. **CI now runs** check_lint_configs and its test, the nodebase, funcusage and shallow tests, and `make -j4 lint`. Re-run them only when a PR changes lint config or the checkers.

## Retrospective inputs

| PR | Kind | Description | Link |
|---|---|---|---|
| #1391 | missed | License headers with an extra `//` line in errors.bal and json_api.bal, caught only now because `check_license_headers.py` is new | [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) |
| #1391 | lint candidate | Run the license-header check in CI; the hook is local only | [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) |
| #1422 | lint candidate | Unsquashed corrections (same files + fix/correct subjects) | [#1422](https://github.com/ballerina-nutcracker/ballerina/pull/1422) |
| #1434/#1435 | lint candidate | CI `go build ./...` per commit (two commits don't build on their own) | [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) |
| #1435 | missed | CodeRabbit (type_resolver.go:9030): named types dropped for record-field and function-type parameter defaults | [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) |
| #1438 | missed | CodeRabbit: `reduce` accumulator type inference | [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) |
| #1612 | missed | `Makefile:N` citations in lint-setup/SKILL.md pointed at wrong lines; raised a round late by us | [#1612](https://github.com/ballerina-nutcracker/ballerina/pull/1612) |
| #1612 | lint candidate | Check that `path:N` citations in `.agents/skills/**` resolve; compare lint-setup's Basic row with go.work | [#1612](https://github.com/ballerina-nutcracker/ballerina/pull/1612) |
| #1613 | missed | 5 CodeRabbit threads: `Toml.Validate` Schema unbuildable, spaces in module paths, `test_util` counted as production, debug-variant directive unchecked, exported hook with in-package use | [#1613](https://github.com/ballerina-nutcracker/ballerina/pull/1613) |
| #1613 | lint candidate | `paralleltest`/`tparallel` for compiler-tools tests; reject a `//funcusage:test-hook` on a function no test references | [#1613](https://github.com/ballerina-nutcracker/ballerina/pull/1613) |
| #1631 | missed | CodeRabbit: unwrapping grouped receivers | [#1631](https://github.com/ballerina-nutcracker/ballerina/pull/1631) |
| #1638–#1647 | recurring | PR-body template Nit raised by only 2 of 6 per-PR reviewers; the stack agent added it to the other 4 after the fact | [#1638](https://github.com/ballerina-nutcracker/ballerina/pull/1638) |
| #1640 | lint candidate | Corpus check for duplicate diagnostics in `-e` goldens; corpus CI run with `-tags debug` | [#1640](https://github.com/ballerina-nutcracker/ballerina/pull/1640) |
| #1642 | missed | CodeRabbit (type_resolver.go:3721): local annotations in a lambda inside a record-field default hit INTERNAL_ERROR (fixed in the new push) | [#1642](https://github.com/ballerina-nutcracker/ballerina/pull/1642) |
| #1609–#1647 | wasted | Stack pushed mid-review; the 16-PR review ran twice (about 77 min + 17 min) | [#1647](https://github.com/ballerina-nutcracker/ballerina/pull/1647) |

Flaky tests seen: `corpus/lib/subset3/task-policy1-v`, `task-listener2-v`, `task-misfire1-v` and `task-onetime1-v`. Each passed when rerun alone.

# PR review round: 2026-11-12, started 09:31 (Asia/Colombo)

`pr730remote/main` is at `008256345`. One tooling gap: `wrk` isn't installed, so the two `compiler-tools/benchmark-http` tests failed in the lint stack's `make test`. That comes from the machine, not the PRs; everything else in `make test` passed. `golangci-lint` v2.15 and `bal` were available.

**Open PRs: 65** · merge-ready: 4 · waiting for CI: 1 · not ready: 54 · drafts: 3 · held by label (don't-merge/dnm/hold/wip): 3

## Merge-ready (4)

| PR | Title | Author | Approval | Reviewed |
|---|---|---|---|---|
| [#1415](https://github.com/ballerina-nutcracker/ballerina/pull/1415) | feat(data.xmldata): add `ballerina/data.xmldata` standard library | TharmiganK | review required | `530706e70` |
| [#1437](https://github.com/ballerina-nutcracker/ballerina/pull/1437) | feat(stdlib): add `ballerina/cache` standard library | TharmiganK | review required | `b2d2ea24e` |
| [#1607](https://github.com/ballerina-nutcracker/ballerina/pull/1607) | chore(lint): enable modernize and modernize Go code | heshanpadmasiri | review required | `c53f03fb4` |
| [#1611](https://github.com/ballerina-nutcracker/ballerina/pull/1611) | refactor(nodes): keep shared base types private | heshanpadmasiri | review required | `bd8ea77c3` |

## Waiting for CI (1)

0 findings, no conflicts, reviewed at the current head; merge-ready once CI passes.

| PR | Title | Author | Approval | CI |
|---|---|---|---|---|
| [#1446](https://github.com/ballerina-nutcracker/ballerina/pull/1446) | feat(stdlib): add `ballerina/ftp` standard library | TharmiganK | review required | CI pending (1) |

## Not ready (54)

open findings: 28 · CI failed: 5 · conflicting: 12 · not reviewed at current head: 9

| PR | Title | Author | Why |
|---|---|---|---|
| [#684](https://github.com/ballerina-nutcracker/ballerina/pull/684) | feat(query): implement query actions | gimantha | conflicting |
| [#701](https://github.com/ballerina-nutcracker/ballerina/pull/701) | feat(tcp): port ballerina/tcp standard library | TharmiganK | not reviewed at current head |
| [#921](https://github.com/ballerina-nutcracker/ballerina/pull/921) | feat: support compiler plugins | heshanpadmasiri | not reviewed at current head |
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
| [#1390](https://github.com/ballerina-nutcracker/ballerina/pull/1390) | feat(stdlib): add `ballerina/data.csv` standard library | TharmiganK | not reviewed at current head |
| [#1391](https://github.com/ballerina-nutcracker/ballerina/pull/1391) | feat(stdlib): add `ballerina/data.jsondata` standard library | TharmiganK | not reviewed at current head |
| [#1411](https://github.com/ballerina-nutcracker/ballerina/pull/1411) | feat(stdlib): add byte-stream and Server-Sent Event support  | TharmiganK | open findings: 1 Nit |
| [#1422](https://github.com/ballerina-nutcracker/ballerina/pull/1422) | feat(stdlib): add `ballerina/data.yaml` standard library | TharmiganK | not reviewed at current head |
| [#1434](https://github.com/ballerina-nutcracker/ballerina/pull/1434) | feat(runtime): expose annotations of nested field types | warunalakshitha | open findings: 2 Important, 3 Nits |
| [#1435](https://github.com/ballerina-nutcracker/ballerina/pull/1435) | fix(semantics): carry annotations on inferred typedesc args | warunalakshitha | conflicting |
| [#1438](https://github.com/ballerina-nutcracker/ballerina/pull/1438) | feat(langlib): add array pop, shift, unshift, reduce and sor | warunalakshitha | conflicting |
| [#1465](https://github.com/ballerina-nutcracker/ballerina/pull/1465) | fix(http): send http:Request message headers and type client | TharmiganK | not reviewed at current head |
| [#1476](https://github.com/ballerina-nutcracker/ballerina/pull/1476) | fix(parser): normalize source newlines and BOM | snelusha | conflicting |
| [#1480](https://github.com/ballerina-nutcracker/ballerina/pull/1480) | feat(workflow): bundle ballerina/workflow with an in-memory  | hasithaa | open findings: 8 Nits |
| [#1481](https://github.com/ballerina-nutcracker/ballerina/pull/1481) | fix(semantics): reject writes to final object fields outside | heshanpadmasiri | conflicting |
| [#1495](https://github.com/ballerina-nutcracker/ballerina/pull/1495) | test: clean up constant folding skip list | heshanpadmasiri | CI failed: Validate Commit Messages, Validate PR Title, Ubuntu Native Build |
| [#1508](https://github.com/ballerina-nutcracker/ballerina/pull/1508) | feat: introduce the test framework | azinneera | conflicting |
| [#1517](https://github.com/ballerina-nutcracker/ballerina/pull/1517) | fix: reject non-private non-isolated fields in isolated obje | heshanpadmasiri | open findings: 3 Nits |
| [#1536](https://github.com/ballerina-nutcracker/ballerina/pull/1536) | feat(ls): add signature help support | nipunayf | open findings: 2 Nits |
| [#1544](https://github.com/ballerina-nutcracker/ballerina/pull/1544) | ci(perf): replace PR benchmark gates with nightly comparison | heshanpadmasiri | open findings: 4 Verify, 6 Nits |
| [#1567](https://github.com/ballerina-nutcracker/ballerina/pull/1567) | feat(ls): add initial completion support | nipunayf | open findings: 2 Nits |
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

## This round

No PR got a new Important or Verify finding. All reviews posted without errors.

| PR | Verdict | New findings (all Nits) | Summary |
|---|---|---|---|
| #1377 | Not ready: 2 Nits | None new. Still open: the "address review suggestions" commit isn't squashed, and the corpus-test checkbox isn't ticked. The 2 comment-trim threads were fixed and resolved. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1377#issuecomment-6311243425) |
| #1411 | Not ready: 1 Nit | None. The code is identical to the last review (history-only rebase). Still open: 22 review-fix commits to squash. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1411#issuecomment-6624722382) |
| #1607 | Ready except approval | None. The rewrite only adapts to main. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1607#issuecomment-6772773678) |
| #1608 | Ready + 1 Nit | Still open: the PR body says Warning keeps its numeric value, but it is now 0. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1608#issuecomment-6772803394) |
| #1609 | Ready + 1 Nit | Still open: the commit type, since 249 BIR goldens change. The golden-refresh finding was fixed and resolved. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1609#issuecomment-6772837482) |
| #1610 | Ready except approval | None. Rebase only. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1610#issuecomment-6772861524) |
| #1611 | Ready except approval | None. Rebase only. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1611#issuecomment-6772871406) |
| #1612 | Ready + 3 Nits | Still open: lint skill intro wording, `decimal` config copy, and a stale PR body about the Concurrent-safe tier. One earlier finding was fixed. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1612#issuecomment-6772901261) |
| #1613 | Ready + 8 Nits | 4 tests missing `t.Parallel()`; 3 `//funcusage:test-hook` markers on table helpers that no test calls; trailing spaces and wording in SKILL.md. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1613#issuecomment-6814601067) |
| #1614 | Ready + 9 Nits | Inlining `NewErrorWithMessage` spread a 5-argument call to 168 sites (suggest keeping it with `//shallow:allow`); leftovers from the inlining; 2 statement splits the lint never asked for; duplicate closures; a `FunctionScope` alias; stale Makefile line references. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1614#issuecomment-6814606413) |
| #1626 | Ready + 1 Nit | The PR body says "Stacked on #1614", but its base is #1631. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1626#issuecomment-6814614107) |
| #1631 | Ready + 3 Nits | The subset-doc bullet doesn't say `clone()` calls are always isolated; `lock { self.a = v; }` gets two errors at one position (measured); the PR body leaves out the nodebuilder change and test 5. | [link](https://github.com/ballerina-nutcracker/ballerina/pull/1631#issuecomment-6814610640) |

The ten PRs from #1607 to #1626 form one stack and were reviewed together at its tip, `a2a9bb54b`.

**#1631 needs a human decision (not raised as a finding).** The spec's "Initialization" section is ambiguous. It says a field can only be assigned an isolated expression, but doesn't clearly say whether that applies only in `init` or in every method. The PR applies it to every method, so `lock { int[] t = [a]; self.arr = t; }` is now rejected; jBallerina accepts it. The PR's claim that this is "as the spec requires" holds only under the every-method reading.

## Skipped
- **Conflicting with main:** #1625, #1481, #1438, #1263, #1233, #1165, and the #1189 → #1221 → #1238 stack (#1189 conflicts).
- **Not checked:** none.

## Filed issues
None. The one main bug the reviews came across (a lock that reads two `self` fields is wrongly rejected) is already open as #1433.

## Review-skill updates (proposed, not applied)
These come from the new lints in #1612–#1614:
1. **#1613 adds `make lint-func-usage`.**
   - Stop raising functions in Strict-or-higher modules that have no production caller, or that are exported but only used in their own package.
   - Keep `check_unused_symbols.py` for what the lint misses: methods, types, fields, consts and vars; Basic-tier modules; callers only in `test_util`; dead call cycles.
   - Treat a `//funcusage:test-hook` with no test reference as a Nit.
2. **#1614 adds `make lint-shallow`.**
   - Stop raising "pointless wrapper" Nits in Strict-or-higher modules; the lint enforces them there, and exemptions need `//shallow:allow <reason>`.
   - Keep raising them in Basic modules (lib, cli, ls, projects, tools).
3. **#1612 tiers and `lint-configs`:** the skill already matches; nothing needed.

**Lint ideas from the stack agent:**
- funcusage: require each `test-hook` to have a test reference, and treat `test_util/**` as test code.
- shallow: skip functions that are only used as values.
- A check for a blank line right after `case:` / `default:`.

**Retrospective input:** CodeRabbit raised three points on #1613 that our review missed:
- `FieldsSeq` splits module paths that contain spaces.
- The directive on the debug-build duplicate is never validated.
- An exported hook used only in its own package isn't reported by anything.

All review worktrees are removed.

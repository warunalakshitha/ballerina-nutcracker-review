# Language server PR review

Use this in addition to the main checklist when a PR adds or changes code under `ls/` or the `start-language-server` CLI host (`cli/cmd/langserver.go`). The LSP 3.18 specification is the source of truth for wire behaviour. The jBallerina language server (`$JBALLERINA_SRC/language-server/`) is the reference for Ballerina-specific feature behaviour, and gopls is the reference for framing and dispatch patterns. The rules in `ls/AGENTS.md` apply on top of the root `AGENTS.md`; read both before judging.

## 1. Main-checklist adjustments

| Main step | For an LS PR |
|-----------|--------------|
| 2. Example Ballerina code | Show an LSP exchange instead: the fixture `.bal` (trimmed), the request or notification, and the expected response or `publishDiagnostics`. Take it from an `ls/corpus` fixture when one exists |
| 4. Challenge every unit test | The target is an `ls/corpus/<feature>/testdata/` fixture driven through the real-framing session, not `corpus/bal`. A Go test is justified only when no LSP request sequence can reach the case (e.g. a UTF-16 conversion table, an event-bus ordering primitive) |
| 6. Duplicate tests | `check_duplicate_tests.py` does not scan `ls/corpus`. Compare new fixture JSON by hand: two scenarios with the same request sequence and the same expected output are one scenario |
| 7. Subset doc | Not needed for `ls/`-only changes; state `Not needed: language server only` |
| 8. Codecov | Suggested tests are fixture scenarios (`ls/corpus/<feature>/testdata/<scenario>.json`), with the request sequence in the Snippet column |
| 10. Parity | Compare against the LSP spec and the jBallerina language server (see section 6), not `bal run` output |

Compiler files the PR also touches (`projects/`, `semantics/`, `context/`, …) get the full main checklist, including a check that `go run ./cli/cmd run` behaviour is unchanged on the corpus.

### Rules from the other checklists that apply to LS PRs

Only the main checklist's `bal run` parity step is replaced. Everything else in `SKILL.md` applies as written, including commit and PR-body checks, the representation-change and design-finding rules, Go-test challenges, unused symbols, comment size and license headers. These rules from [stdlib-review.md](stdlib-review.md) and [workflow-review.md](workflow-review.md) also apply, adapted:

| Source rule | LS form |
|---|---|
| stdlib §2 spec walk (Implemented / Partial / Not supported, verified with a program) | Walk the PR body's claims (provider or context table, "supports X") the same way, each verified with a fixture or harness run (section 6). |
| workflow §1 scope against the task list | When the PR names a parent issue (e.g. #1535), compare the diff with the issue's task list: each ticked task is implemented, and unticked ones aren't claimed in the PR body. |
| stdlib §6 / workflow §2 panic isolation | A panic in a feature provider, AST walk or handler must not kill the server. Find where requests are dispatched and check each runs under a `recover` that turns a panic into `InternalError` (-32603) for that request only. Probe with an input that reaches a nil node (a recovered or empty AST). |
| stdlib §6 blocking externs yield / workflow no bare waits | Every wait in a request handler (for a compile, a generation, a lock) selects on the request's `ctx`, so `$/cancelRequest` and `shutdown` end it. |
| workflow §2 no `time.Sleep`/`time.Now`, time via PAL | Debounce and timeouts go through an injectable clock or option, so tests don't sleep. A test that sleeps to wait for a compile is a finding. |
| workflow §4 negative inputs must not cause unbounded waits | Negative, huge (`4294967295`) and missing positions, versions and ids: a protocol error or a clamp, never a stall or panic (#1543). |
| stdlib §6 typed errors | Each failure path returns the LSP error code the spec names (`InvalidParams`, `RequestCancelled`, `ContentModified`, `ServerNotInitialized`), not a successful `null`. |
| stdlib §6 deferrals | When the PR body or parent issue defers something to a named later PR or issue, that's a one-line summary note, not a finding (section 6 scope rule). |
| stdlib §6 sibling ports | LS features share helpers and habits (cursor scanning, comment and trivia skipping, import lookup, request decoding). A bug class found in one feature package is checked in the PR's other feature packages and in the ones already on main. Mention a hit in another open LS PR in the final message, not as a finding here. |

## 2. Layering (`ls/AGENTS.md`)

- `ls/protocol` imports no compiler package and no other `ls/` package.
- Handlers take typed params and return typed results; they never write to the transport or frame messages.
- No direct filesystem, `os`, stdio or network use inside `ls/`. The host injects streams, the filesystem and the log writer. Production code reading `os.ReadFile`, `os.Stat`, `filepath.Walk` on the real disk, etc. is a blocking finding (the offline protocol generator is exempt).
- Logs never reach protocol output (stdout). Any `fmt.Print*`, `log.Print*` or default-logger use is blocking: it corrupts the JSON-RPC stream. The server must not close the host's log writer.
- Project keys, filesystem roots and compiler module names stay distinct; two single files in one folder get separate project keys.
- The compiler is reached through its public APIs (`projects`, `context`, `ast`, `model`, `semantics`). Reaching into compiler internals, or mutating compiler state shared with another compile, is a finding.

## 3. Protocol conformance

Check each against the LSP 3.18 spec and probe it with a fixture or the nvim harness (`compiler-tools/ls-nvim-harness/`):

- **Lifecycle:** requests before `initialize` return `ServerNotInitialized` (-32002); a second `initialize` is rejected; after `shutdown`, requests return `InvalidRequest`; `exit` exits 0 after `shutdown` and 1 without it.
- **JSON-RPC:** ids work as both numbers and strings; notifications never get a response; unknown requests return `MethodNotFound`, unknown notifications (and any `$/` notification) are ignored; malformed JSON returns `ParseError`; a duplicate in-flight id is rejected; params that don't decode or miss a required field (a negative position, no `textDocument`) return `InvalidParams` (-32602), not a successful `null`.
- **Spec defaults:** when the PR invents a fallback for a client that lacks a capability (a sentinel value, an omitted field), check the spec's default rule for that field. Raise it only with a measured client-visible difference (a wrong highlight, a dropped field, an error in the nvim harness); a fallback that merely restates the spec default (e.g. an out-of-range `activeParameter`, which the spec also treats as 0) with no demonstrated failure is not a finding, not even a Nit.
- **Cancellation:** `$/cancelRequest` produces exactly one response (`RequestCancelled`, -32800) or the normal result if it already finished; cancelling an unknown or finished id is a no-op.
- **Framing:** `Content-Length` counts bytes, not runes; a missing or bad header is handled without a panic; partial reads across buffer boundaries.
- **Capabilities:** the server only advertises what it implements, and honours client capabilities it depends on (position encoding, `didChangeWatchedFiles` dynamic registration, pull vs push diagnostics).
- **Document sync:** full and incremental `didChange`; versions only go forward; `didClose` drops the overlay and falls back to disk; non-`file:` URI schemes are handled as the PR documents.

## 4. Positions and text

Positions on the wire are UTF-16 code units unless `positionEncoding` negotiated otherwise; core and services use byte offsets. Conversion happens only at the server edge.

- Any UTF-16 ⇄ byte arithmetic in `ls/core`, a service or compiler code is a finding.
- Probe with: a surrogate pair (emoji) before the position, a multi-byte non-BMP identifier or string literal, CRLF and lone CR line endings, a position past the end of a line (clamp per spec), an edit at the very end of the file, and an empty document.
- Diagnostic ranges round-trip: a diagnostic on a line containing an emoji highlights the right columns.

## 5. Concurrency and incremental compile

This is the highest-risk area of an LS PR. Apply the main skill's data-race section, plus:

- **Generations:** a result computed for an older generation is never published (diagnostics) or returned (features). Find every place a result is stored or sent and check it compares generations under the same lock that reads the latest one (check-then-act).
- **Trace each result end to end.** For diagnostics, and for each feature result, follow one value from the compile that produces it to the byte written on the wire, across package boundaries: workspace generation → compile cycle → snapshot store → bus event → server claim / dedup → publish goroutine → transport. At each hop write down what is checked (generation, version, closed flag), what is read separately from that check, and what happens when the check fails (dropped, retried, or the generation is marked done anyway). Common misses: two reads of state under different locks that can come from different generations (a stable snapshot plus a separately read module map), a dedup claim taken before the fetch that can fail, and a check done before a store without holding the lock. Do this as its own pass, not inside the per-package split (section 9), because the interleavings cross packages.
- **Event bus:** delivery order within a subscriber, behaviour when a subscriber is slow or blocks, unsubscribe during delivery, and publish after shutdown. A blocking subscriber must not stall `didChange` handling.
- **Shutdown:** every goroutine the PR starts (compile workers, bus dispatchers, watchers, timers, per-document publish goroutines) stops on `shutdown`/`exit`, and nothing writes to the transport after the `shutdown` response; no send on a closed channel. List each `go` statement and each `WaitGroup.Add` the PR adds and name what waits for it on shutdown; one that only `Flush` waits for is a finding. Check with `-race` and, when the package has one, a goroutine-leak check.
- **Shared compiler state:** two concurrent compiles (two projects, or a new generation while the old one runs) must not share mutable compiler context, type env or module caches.
- **Invalidation:** an edit to a dependency's public API invalidates its dependents; an edit that keeps the API unchanged doesn't. Adding or removing a file, an import, a module directory, or a `Ballerina.toml` change reloads correctly. Each claim in the PR body ("dependents keep their work", "unchanged recompile is skipped") needs a fixture that fails when the claim is broken. Mutation-test it: disable the optimisation or the invalidation and check that the fixture fails.

Run:

```bash
go test -race -count=10 ./ls/...
go vet ./ls/...
go build ./...
```

## 6. Feature parity (when the PR adds an LSP feature)

For completion, hover, signature help, diagnostics, go-to-definition and similar features, read the matching provider in `$JBALLERINA_SRC/language-server/modules/langserver-core/` and its test configs (`src/test/resources/<feature>/`). Pick a handful of the jBallerina test cases that fall inside Nutcracker's supported subset and run them as fixtures. A divergence is a finding only if the PR doesn't document it as a non-goal; apply the spec-over-jBallerina rule for wire behaviour.

**Probe what the PR claims, nothing more.** Turn each supported context the PR body lists (e.g. a provider table row: "after `mod:` in a type descriptor", "auto-import edit") into a few fixtures that vary the input the claim covers: import forms (plain, `as alias`, dotted module names, two imports), nesting (top level vs inside `record {| |}`, `object {}`, a union, parentheses), and a comment or line break in the middle. Also vary:

- **Where the callee or symbol lives:** same file, another file of the same module, a sibling module of the same package, an external dependency, and a langlib or stdlib module (`io:println`, `arr.push`). Docs and labels often work only for the first.
- **Receiver and callee shape:** a class, an object union (`A|B` with the same method), a function-typed variable, a remote method, `new` with an inferred type.
- **Cursor boundaries:** for each argument form (positional, named, rest), put the cursor at the start of the name, before and after `=`, at the start and end of the value, and just before and after each comma.
- **Compile stage:** run each case on a module that type-checks and on one with an unrelated error elsewhere, since syntax-only and typed paths often give different answers.

Report a failure only when it falls inside a claimed context:

- In scope: the PR claims the context and the feature returns wrong results there (missing items, items for the wrong context, a duplicate or wrong edit). A handler that takes the cursor and answers wrongly counts, even when the PR never names that exact variant (e.g. a record field type is part of "in a type descriptor").
- Out of scope, not reported: contexts the PR lists as not yet supported or a later PR, and contexts no provider claims where the feature correctly returns nothing. Don't post these, not even as `verify`. Mention them only in the final message if they look like a trap for the follow-up PR.
- If a variant can't be placed in or out of a claim from the PR body, post one `verify` question asking whether it is meant to be supported.

**Read the output as a user sees it.** Goldens pass by definition, so read them. Render each Markdown string the PR produces (labels, parameter docs, descriptions) and check spacing between parts (`` `int` a``, not `` `int`a``), that fenced code blocks and line breaks in doc comments survive, and that type names are readable: a type the compiler expands in full (`nil|boolean|int|…`) where jBallerina prints the source form (`any|error`) is a finding. Do this for at least one stdlib callee with real docs, not only fixtures written for the PR.

**Drive the real server.** Run the PR's claims table through the built `bal start-language-server` over stdio (or the nvim harness), not only the in-process corpus client, including a request sent right after `didChange` as trigger characters would send it.

**Text heuristics in place of parsed data.** When feature code re-derives something the compiler already holds (matching `import` lines as strings, counting `{` depth, scanning tokens with regexes rather than reading the AST or the file's parsed imports), probe that code with aliases, comments, nesting and unusual formatting inside the claimed contexts. If the PR body says it works from the AST but the code scans text, raise that as a design finding backed by one of these repros.

Diagnostics must match the compiler: the set of errors published for a file equals what `go run ./cli/cmd run` reports for it (same lines, same count), and a file with no errors gets an empty `publishDiagnostics`, not none.

## 7. Tests and fixtures

- Fixtures follow `ls/AGENTS.md` and the `manage-ls-fixtures` skill: `ls/corpus/<feature>/testdata/<scenario>.json` (transcript `messages` + golden `expected`), with an optional `.bal` named by the transcript's `source` field; one behaviour per scenario, named for the behaviour (not numbered).
- Golden updates are scoped (`go test ./ls/corpus -run 'TestCorpus/<feature>/testdata/<scenario>.json' -update`); changed goldens for scenarios the PR didn't touch are drift to revert.
- The PR passes the three gates: `go test ./ls/...`, `go build ./...`, `go vet ./ls/...`.
- A fixture tests what its name says: for each fixture named after a capability, client setting or format (`docs-format-plaintext-first`, `capability`), check that the harness actually sends that setting. A harness that runs every config through one client with fixed capabilities makes those fixtures duplicates of each other.
- Dev tools the PR adds (`compiler-tools/ls-nvim-harness/`, probe scripts, README setup steps) are run, not only read: a path with a space and a `'`, an empty argument where the tool accepts one (empty replacement text), a falsy result (`false`, `0`, `""`) passing through, and the README steps followed from a clean build (every binary it needs is listed).
- Goldens must not be hand-edited to pass; a golden that encodes wrong behaviour (e.g. a stale diagnostic, a wrong range) is a finding on the server code.
- Tests use the injected filesystem and temp directories; a test reading the real repo tree outside its `testdata/` is a finding.
- Platform-specific tests (`*_windows_test.go`) are built with a matching build tag and run in CI on that platform.
- CI: new LS packages are covered by the existing test and race jobs (check `.github/workflows/`), not only by a new workflow step.
- Production timing is tested: at least one fixture or test runs with the default debounce, not only with `WithDebounce(0)` (main step 4, production defaults).
- Each rule `ls/AGENTS.md` states as behaviour (e.g. two single files in one folder get separate project keys) has a fixture that fails when the rule is broken.
- Each race the end-to-end trace (section 5) names has a test that drives that interleaving (a test hook, a blocked request, or `-race -count=N` on a scenario that hits it), or the finding says why it can't be driven.

## 8. Agent docs and skills the PR adds

`ls/AGENTS.md` and `.agents/skills/**` the PR adds are process docs (main step 4 rule). In addition, check that they:

- name only skills, files and paths that exist in the repo at the PR head (no references to skills from another repo, no absolute paths from the author's machine);
- describe the package layout the PR actually ships: run `git ls-tree -d -r --name-only HEAD ls/` and check that every package (including nested ones such as `ls/core/*`) is listed, that no listed package is gone, and that each stated role (e.g. which package owns workspace state) matches the code and the PR's architecture diagram;
- don't contradict the code ("the driver may not exist yet" when the PR adds it).

## 9. Large PRs

When the LS diff is over ~5k lines, review it in one subagent per package (`ls/protocol`, `ls/server`, `ls/core/compile`, `ls/core/event`, `ls/core/observability`, `ls/core/workspace`, `ls/cmd`, each feature package such as `ls/core/completion`, the host + harness + docs; list the packages from `git diff --name-only` rather than from this list, so a new package always gets its own subagent), run from a queue with at most ~3 concurrent, each given this file (including the borrowed rules in section 1) and the main checklist. Alongside them, run the section 5 end-to-end trace as its own subagent over all packages. Give the mechanical checks (`t.Parallel()`, `check_license_headers.py`, `check_unused_symbols.py`, duplicate fixtures) to one more subagent, and tell the package subagents to skip them so they spend their time on behaviour. Merge their findings into one report and dedupe across packages before the prior-review overlap step.

## 10. Report additions

In the report, replace **Example Ballerina code** with **Example LSP exchange**, replace **jBallerina parity** with **LSP / jBallerina LS parity**, and add a **Protocol conformance** table (check → result → evidence: fixture name or harness transcript). Findings follow the main template.

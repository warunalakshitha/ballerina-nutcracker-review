# Standard library PR review

Use this in addition to the main checklist when a PR adds or changes a module under `lib/stdlibs/ballerina/<name>/`. A Nutcracker stdlib is a port of jBallerina's `ballerina/<name>`. The source of truth is the module's spec. jBallerina's Ballerina and Java sources are the reference implementation.

## 1. Fetch the references

For `ballerina/<name>`, the upstream repo is `ballerina-platform/module-ballerina-<name>` (default branch usually `main`; check with `gh api repos/ballerina-platform/module-ballerina-<name> --jq .default_branch`). Pin the version that matches the jBallerina distribution used for parity: the version a fresh project resolves (`bal build` in a new package that imports the module, then read its Dependencies.toml), not the copy bundled with the distribution, which can be an older patch. Say which one you used. When the PR or its README names a newer patch, use the newer of the two, and recheck every Notable Behavioural Changes bullet against that release's changelog: a jBallerina bug that release already fixes is parity, not a defect the port fixes.

```bash
M=module-ballerina-<name>
REF=<pinned tag, or the default branch>
gh api "repos/ballerina-platform/$M/git/trees/$REF?recursive=1" --jq '.tree[].path' \
  | grep -E '^docs/spec/spec.md$|^ballerina/.*\.bal$|^native/src/main/java/.*\.java$|^compiler-plugin/src/main/java/.*\.java$' | grep -vi test
gh api "repos/ballerina-platform/$M/contents/docs/spec/spec.md?ref=$REF" --jq .content | base64 -d > "$SP/<name>-spec.md"   # $SP: your scratch dir
```

Fetch only the files a check needs. The spec, the public `.bal` files, and the Java class behind a native method are enough for most findings.

## 2. Spec walk (section by section)

Go through every section of `docs/spec/spec.md` and give each one a status:
- **Implemented:** the behaviour matches. Verify with a program, not by reading code.
- **Partial:** some parts are missing or behave differently. Name what.
- **Not supported:** absent.

Then cross-check the PR's package README coverage table and `doc/library/README.md`. Every Partial or Not-supported item must appear as Partially Supported, Not Yet Supported or Cannot Support, or under Notable Behavioural Changes. A row marked Supported that the spec walk found Partial is a finding (doc fact). Leave counts and percentages to the checker (main skill, **Stdlib coverage docs**).

## 3. Public API parity (`ballerina/*.bal`)

Compare the PR's `.bal` with upstream:
- types, records and their fields, open vs closed (`{| |}`), defaults;
- `distinct` error and service types;
- function and method signatures (parameter names matter for named arguments), return types, `isolated`, `remote` and `resource` qualifiers;
- enums, constants and annotations.

Run the contract extractor on both sides and diff them (`validate-stdlib-contract`): `go run ./.agents/skills/validate-stdlib-contract/cmd/extract-surface <dir>` on upstream `ballerina/` and on the port, then `diff -u`. Only a Not Yet Supported symbol may be absent. A missing Supported, Partially Supported or Cannot Support symbol (Cannot Support must still be declared and fail at runtime), a changed signature (parameter names count), or a new `public` symbol jBallerina lacks is blocking; a README note doesn't excuse it.

## 4. Behaviour vs the native implementation (`native/.../*.java`)

For each native method, read the Java class it maps to, e.g. `UdpClient.java` or `Listener.java`, for:
- error types and messages, and which error is returned versus panicked;
- default values and timeouts (`0` or negative meaning "no timeout");
- lifecycle: `start`, `gracefulStop`, `immediateStop`, restart after stop, double `close()`, attach and detach, and `start()` with no service;
- resource limits (buffer sizes, truncation), encodings and charsets, IPv6, and name resolution;
- config mapping: for each config record field the natives read (e.g. `secureSocket.protocol.versions`, `ciphers`, `cert`), check the Go translation is exact: no list collapsed to a range, no unknown enum or string value skipped silently, no empty result falling back to a default. A lossy mapping that isn't documented is a finding.
- multiple input paths: when a native picks between two or more parsers, readers or decoders for the same input (by target type, size, an option or a mode), list the paths and run every well-formedness, limit and boundary probe that the PR's tests or README claim on each path, not only on the default one. A check enforced on one path and missing on another is a finding.

Confirm each difference with `bal run` (see the main skill's step 10) before raising it. Apply the main skill's Base check and spec-over-jBallerina rules.

**jBallerina bugs are fixed, not copied** (`add-stdlib-support` step 5). Where jBallerina contradicts its spec or API docs, or is clearly defective (data loss, races, silent overflow or truncation, unenforced limits, ignored inputs), the port implementing the correct behaviour is right, not a parity finding. Check instead that each such fix:

- is listed under the package README's **Notable Behavioural Changes** (the checker keeps `doc/library/README.md` in sync) with a real link to an existing or filed issue in `ballerina-platform/ballerina-library` — a missing or placeholder link is a finding;
- has its corpus `@output` that differs from jBallerina cite that issue in a comment (`$TOOLS/skills/pr-review/scripts/check_stdlib_issue_citations.py <base>` lists linked issues no test of the module cites). For each issue it lists, find the case that shows the bullet's behaviour, one jBallerina handles differently. When no fixture has one (the nearby cases fail on jBallerina too), the gap is a missing test, not a missing cite: raise a Nit on the fixture where the case belongs, asking for the bullet's own example with the cite;
  compare each fixture with jBallerina call by call: when jBallerina panics or hangs partway through, trap or comment out that line and rerun until every line has run, then check every `@output` that differs, not one cite per issue. A cite comment directly above consecutive lines for the same issue covers all of them. Report gaps as one Nit per fixture file listing its lines and the issue each needs (name the ones that need filing);
- isn't contradicted by a corpus test that still asserts the buggy jBallerina behaviour.

Check the README side on its own as well, not only for the fixes you found: go through **every** bullet under the package README's Notable Behavioural Changes that the PR adds or edits (all of them for a new package). Each bullet that describes a jBallerina defect the port fixes, as opposed to an architectural Go constraint, needs a `ballerina-platform/ballerina-library` issue link (`stdlib-readme-format` checklist). List the unlinked bullets by title in one finding on the README.

Conversely, a port that copies a jBallerina bug to keep outputs identical is a finding.

## 5. Compiler plugin (`compiler-plugin/.../*.java`)

Upstream compile-time rules, for example service validators for allowed remote methods, parameter types and return types, are part of the module contract. For each rule, check whether the port enforces it, at compile time or at attach or runtime, or documents that it doesn't. An invalid service that jBallerina rejects at compile time and the port accepts silently is a finding unless the README lists it.

## 6. Port-specific checks

- **PAL:** no direct `os`, `net`, `time` or `fmt.Fprint*(os.Stderr)` use. DNS resolution, dialing, listening, clocks and stderr go through `rt.Platform()`. Randomness via `crypto/rand` is fine, since PAL has no randomness interface.
- **Ballerina code on a native goroutine:** a panic must not crash the interpreter. This covers every `go func()` that calls `InvokeFunctionValue` / `InvokeFunction`: listener and service dispatch, engines that run user functions on their own strand, and callbacks. Recover around the invocation. Dispatch logs `error: <msg>` through PAL stderr and keeps serving, as http's `startHTTPServer`, udp's `dispatch.go` and file's listener do. An engine records the panic as the run's failure.
- **Blocking externs yield:** an extern that waits (a channel receive, `time.After`, `time.Sleep`, `sync.WaitGroup.Wait`, a socket read without a deadline loop) must not hold the strand's thread. Loop with `<-ctx.Yield()` between checks, as `lang.runtime` `sleep` does with `Platform.Time.MonotonicNow`. A bare wait can starve another strand that would unblock it (e.g. the strand that sends the data being waited on): **Important**. A read or write deadline doesn't count as yielding. Run `$TOOLS/skills/pr-review/scripts/check_blocking_externs.py <base>` and probe every extern it lists with a program where a started strand must run before the call can return; the rule existing is not a substitute for that probe.
- **Connections:** for every connection or session an extern opens (including in `init`), check that it is closed on every path out, success included, and that `close()` after a protocol-level goodbye (`QUIT`, `LOGOUT`) still releases the socket. An error from that goodbye or from a commit it triggers (e.g. POP3 deletions) is returned, not dropped, unless the data was already retrieved: then a failed commit, whether refused (an error reply) or unanswered, still returns the data, since an error could lose data the server already removed while a kept item is just received again (at-least-once). The README must say so. After `close()`, a receive or poll in progress stops and later calls return an error instead of reconnecting or polling on.
- **Typed errors:** for each `error` subtype a public function documents (`distinct` or not), find the native path that produces it and check it builds that type. A test like `r is mod:NotFoundError` must hold. A plain `NewErrorWithMessage` where a subtype is documented is a finding per error type.
- **Caller headers vs defaults:** when the port (`.bal` or native) puts both caller-supplied headers and a default it sets itself (a body's `Content-Type`, a `Content-Length`, a default `Accept`) on the same message, send one whose caller headers name that same header and compare the message on the wire with jBallerina: which value wins, and whether both are sent. A default that overrides or sits beside the caller's value is a finding. Example (#1756): an error detail's `Content-Type: application/problem+json` was appended after the payload's `application/json`, so clients reading the first value got `application/json`.
- **Externs:** named functions only. Types are built once in module init, not per call.
- **Tests:** anything that needs no network or OS fixture goes in the open library subset `corpus/lib/subset<N>` (the open one `check_released_subset.py` prints; golden in `corpus/integration/lib/subset<N>`). Real sockets, servers, chmod or links go in `corpus/extern` with `.bal` fixtures and `t.Parallel()`. Challenge each Go test case (main skill). A new package with no test at all is a finding unless the PR defers it to a tracked task (see deferrals below).
- **Fake servers:** a test against an in-process fake server proves only what the fake models. For each error path a test claims (a missing entry or base, a bad credential, a refused operation), check that the fake gives the same result code as a real server and jBallerina. A fake that succeeds where the real server fails lets wrong code pass.
- **Timing-sensitive tests:** for each new test that `@output`s an order of events, or a count taken after `stop`, `detach`, a retry or a sleep, run it at least 20 times with `-race` and under CPU load (e.g. `GOMAXPROCS=1`, or while a parallel `go test ./...` runs). Read how it waits and what orders its events: a fixed `sleep` before asserting, one wait that drains setup and processing events together, or an order produced by callbacks that can run concurrently (each poll or dispatch on its own goroutine) is a race even when no run varies. Each is an Important flaky-test finding naming the line.
- **Docs:** a **new** package ships `lib/stdlibs/ballerina/<name>/0.0.1/go1.27/README.md` (support table + behavioural notes) and the `check_readmes.py --write` output for `doc/library/README.md` and the root `README.md` committed. For any package, rely on `check_readmes.py` as described under **Stdlib coverage docs** in the main skill instead of cross-checking totals by hand. Newly supported surface is documented in `doc/library/subset<N>.md` for the lib subset the tests use; a new lib subset adds `subset<N+1>.md`.
- **Deferrals:** when the PR body or its parent issue's task list defers README, tests or compiler checks to a named later task or PR, that's a one-line summary note ("deferred to <task/issue>"), not a finding. Check the task exists. A deferral with no issue or task behind it is a finding.
- **Wire-up (new package):** when `builtinStdlibs` changes, run `go test ./birgen -run TestBIRGeneration` too: global type ids in BIR goldens (`$service.<id>`) shift for unrelated fixtures, and only that test shows the churn. `lib/rt/libs.go` has the blank import when there is a `native/` directory; `test_util/testphases/phases.go` has a `builtinStdlibs` entry after the package's dependencies (root module before its sub-modules); `Dependencies.toml` declares every `import ballerina/<dep>`; a langlib import is in the `isLangImport` switch in `semantics/symbol_resolver.go` (`add-stdlib-support`). A gap-fill PR (`fill-stdlib-gap`) must not change `libs.go` or `phases.go`.
- **Natives:** `*-v.bal` lib tests have empty stderr; no wrong-type extern argument guards (`x, _ := args[i].(T)`); never add fields to `values.Map` for native state; use `values.BalToGoJSON`/`GoToBalValue` instead of a per-module conversion; a new `go.mod` dependency states its license (GPL/AGPL/LGPL is a finding) and footprint (`add-stdlib-support`).
- **Copies of compiler or runtime data:** native code sometimes hand-writes what the compiler or runtime already derives from the module's `.bal` source, for want of an API: a `bir.BIRClassDef`, a VTable or method-key list, `"<org>/<module>:<Class>.<method>"` lookup keys, an object's field list or a `values.NewObject` field map; or it reaches into runtime or compiler internals. When the PR adds or edits such code, or adds or changes a `.bal` method, field or class such code copies:
  1. **Completeness.** At the PR head, compare each copy with the `.bal` declarations it mirrors. Every method or field the `.bal` declares appears in every copy (e.g. the class def's VTable and the list an inbound-object builder uses). A missing entry is **Important**: natively built objects lack it while `new` ones have it. Prove it with a program that calls the method on a natively built object (#729: `setPayload`/`getFormParams` missing from http's `requestMethodKeyCache`, so an inbound `Request` panicked with `function not found`).
  2. **The missing API.** Unless a comment at the workaround already links an issue, raise one Nit asking the author to link the issue for the API it stands in for in a comment there. A hand-kept method-key map, VTable or field map for an object built natively (`values.NewObject`, `RegisterExternClassDef`) links #1797, native creation of module class instances; for any other missing API, ask the author to file a runtime or compiler issue first. Once #1797 is closed, ask for its API instead. Don't ask the PR to build the API.
- **XML on encoding/xml:** `encoding/xml` leaves parts of XML 1.0 unchecked. For each input path (record target, union target, xml target, stream), probe: a PI in the internal subset whose data holds `>` and quotes; a C0 control and U+FFFE in a PI, a comment, CDATA, an attribute value and text; an `ATTLIST` default; an internal parameter entity that declares a general entity; nested entities that expand exponentially; an entity reference in a start tag right after a self-closing element (`<a/><b x="&e;">`), placed exactly at the entity-count limit, so a pre-scan that counts it twice rejects a valid document. Compare each with jBallerina.
- **Sibling ports:** when several ports land together (tcp, udp, ldap), a bug class found in one is worth checking in the others.

Module-specific companions: [workflow-review.md](workflow-review.md) for `ballerina/workflow`.

## 7. Report additions

In the report, add a **Spec walk** table (section → status → evidence) and a **Compiler plugin rules** table (rule → enforced / documented / missing). Findings follow the main template. A spec gap that the README documents is a summary note, not a finding.

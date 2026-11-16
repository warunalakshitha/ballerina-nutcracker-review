#!/usr/bin/env python3
"""List stdlib extern functions that make a blocking call without ever yielding the strand's thread.

Usage: $TOOLS/skills/pr-review/scripts/check_blocking_externs.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it inside the PR worktree.

An extern runs on its strand's thread. One that waits on a socket, a channel, a WaitGroup or a sleep without
looping on `<-ctx.Yield()` holds that thread, so another strand on it (often the one that would unblock the wait)
can't run (stdlib-review.md, "Blocking externs yield"). For each Go file under lib/stdlibs/ the PR adds or changes,
this finds the extern bodies (functions taking `*extern.Context`, including the closures a `func(...) extern.NativeFunc`
returns) that reach a blocking call outside a `go func` literal, directly or through helper functions and methods of
the same package, with no `Yield(` call on the way:

  BLOCKING  <file>:<line> <function>: <call>              the call is in the extern body
  BLOCKING  <file>:<line> <function> via <helper>: <call>  the call is in a helper the extern calls

Each blocking line is listed once, under the first extern that reaches it. Calls started with `go` aren't followed.

A deadline doesn't make the call yield: a read with a 30 s timeout still holds the thread for 30 s. Each hit is a
candidate, not a finding: probe it with a program where a second strand on the same thread must run for the call to
return (e.g. a started strand that writes the bytes the extern reads), and raise it only if the probe hangs or
waits out the deadline. Helpers are matched by name within the package, so calls into other packages (a client
library's own methods other than those listed) aren't followed. Exit status 1 when anything is reported.
"""
import re
import subprocess
import sys

BLOCKING = re.compile(
    r"\.(Read|ReadFrom|ReadFromUDP|ReadMsgUDP|Accept|AcceptTCP|Dial|DialContext|DialTimeout|DialURL|Wait|Recv|Receive"
    r"|Bind|SimpleBind|Search|SearchWithPaging|Query|QueryContext|Exec|ExecContext|Do|RoundTrip)\("
    r"|\btime\.Sleep\(|\bconn\w*\.Write\(|^\s*(\w+(,\s*\w+)?\s*:?=\s*)?<-\s*[\w.]+\s*$"
)
EXTERN_SIG = re.compile(r"func\s*(\(\w+ \*?\w+\)\s*)?(\w*)\s*\([^)]*\*extern\.Context[^)]*\)")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def strip(line):
    """The line without string, rune and comment text, so braces in them don't count."""
    line = re.sub(r'"(\\.|[^"\\])*"|`[^`]*`|\'(\\.|[^\'\\])*\'', '""', line)
    return line.split("//", 1)[0]


def func_bodies(lines):
    """Yield (name, body) for every top-level function or method declaration."""
    for i, line in enumerate(lines):
        m = re.match(r"func\s*(\(\w+ \*?\w+\)\s*)?(\w+)", line)
        if m:
            yield m.group(2), block(lines, i)


def block(lines, i):
    depth, body = 0, []
    for j in range(i, len(lines)):
        code = strip(lines[j])
        body.append((j, lines[j], code))
        depth += code.count("{") - code.count("}")
        if depth <= 0 and "{" in "".join(c for _, _, c in body):
            break
    return body


def extern_bodies(lines):
    """Yield (name, body) for each function literal or declaration taking *extern.Context."""
    outer = None
    for i, line in enumerate(lines):
        m = re.match(r"func\s*(\(\w+ \*?\w+\)\s*)?(\w+)", line)
        if m:
            outer = m.group(2)
        sig = EXTERN_SIG.search(strip(line))
        if sig:
            yield sig.group(2) or outer or "?", block(lines, i)


def outside_go(body):
    """Body lines that aren't inside a `go func` literal."""
    depth, go_depth = 0, None
    for j, raw, code in body:
        if go_depth is None and re.search(r"\bgo\s+func\b", code):
            go_depth = depth
        depth += code.count("{") - code.count("}")
        if go_depth is not None:
            if depth <= go_depth:
                go_depth = None
            continue
        yield j, raw, code


def main():
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    base = git("merge-base", base_ref, "HEAD").strip()
    changed = git("diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD", "--", "lib/stdlibs").split()
    changed = [f for f in changed if f.endswith(".go") and not f.endswith("_test.go")]
    found, reported = 0, set()
    for pkg in sorted({f.rsplit("/", 1)[0] for f in changed}):
        files = [f for f in git("ls-tree", "--name-only", "HEAD", pkg + "/").split()
                 if f.endswith(".go") and not f.endswith("_test.go")]
        sources = {f: git("show", f"HEAD:{f}").split("\n") for f in files}
        helpers = {}
        for path, lines in sources.items():
            for name, body in func_bodies(lines):
                helpers.setdefault(name, (path, body))
        for path in sorted(f for f in changed if f in sources):
            for name, body in extern_bodies(sources[path]):
                seen, queue, hits, yields = set(), [(None, path, body)], [], False
                while queue:
                    via, where, part = queue.pop()
                    for j, raw, code in outside_go(part):
                        if "Yield(" in code:
                            yields = True
                        if BLOCKING.search(code):
                            hits.append((where, j, via, raw.strip()))
                        if re.match(r"\s*go\s", code):
                            continue
                        for callee in re.findall(r"\b(\w+)\(", code):
                            if callee in helpers and callee not in seen and callee != name:
                                seen.add(callee)
                                queue.append((via or callee, *helpers[callee]))
                if yields:
                    continue
                for where, j, via, raw in hits:
                    if (where, j) in reported:
                        continue
                    reported.add((where, j))
                    found += 1
                    label = f"{name} via {via}" if via else name
                    print(f"BLOCKING  {where}:{j + 1} {label}: {raw}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

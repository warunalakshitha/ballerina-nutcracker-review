#!/usr/bin/env python3
"""Flag added lines that drift from the playground's design system and repo rules.

Usage: $TOOLS/skills/playground-review/scripts/check_playground_ui.py [base-ref]
  base-ref defaults to origin/main (merge-base with HEAD is used). Run it
  inside the playground PR worktree.

Only lines the PR adds are checked. Each hit is a lead, not a finding: read
the line before raising it, and group hits of one kind into one finding.

  COLOR      raw hex/rgb/hsl/oklch colour, or a Tailwind palette / arbitrary
             colour class, in apps/web/src outside styles.css. Use the tokens
             in styles.css (bg-background, text-muted-foreground, border-border,
             --foreground, ...). The editor theme (shiki-editor.ts) is exempt.
  UI-EDIT    a change under apps/web/src/components/ui/ (shadcn primitives;
             AGENTS.md: don't edit unless clearly necessary).
  NATIVE     a native <select>, <dialog>, checkbox, or window.alert/confirm/
             prompt where a ui/ primitive exists (ui/select, ui/dialog,
             ui/alert-dialog, ui/checkbox).
  GLYPH      a Unicode glyph used as an icon in .tsx; use HugeiconsIcon.
  ICONLIB    an icon import that isn't @hugeicons.
  TOASTER    <Toaster> imported straight from "sonner" instead of ui/sonner.
  FONT       a font-family / font-[...] override; the app is JetBrains Mono.
  CONSOLE    console.log/debug added in apps/web/src.
  PKGMGR     an npm/pnpm/yarn lockfile; the repo uses Bun only.
  GENERATED  a hand edit to a generated file (examples.json, routeTree.gen.ts,
             browser-workspace/src/generated/).

Exit status 1 when anything is reported.
"""
import re
import subprocess
import sys

WEB = "apps/web/src/"
UI_DIR = WEB + "components/ui/"
COLOR_EXEMPT = (WEB + "styles.css", WEB + "components/shiki-editor.ts", WEB + "wasm_exec.js")

RAW_COLOR = re.compile(r"(?<![\w&/-])#[0-9a-fA-F]{3,8}\b(?![\w-])|\b(?:rgba?|hsla?|oklch|oklab|lab|lch)\(")
TW_PALETTE = re.compile(
    r"\b(?:bg|text|border|ring|fill|stroke|from|to|via|outline|decoration|divide|shadow|accent|caret)-"
    r"(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|"
    r"indigo|violet|purple|fuchsia|pink|rose|black|white)(?:-\d{2,3})?(?:/\d+)?\b"
)
TW_ARBITRARY = re.compile(r"\b(?:bg|text|border|ring|fill|stroke|from|to|via|outline)-\[(?:#|rgb|hsl|oklch)")
NATIVE = re.compile(r"<select\b|<dialog\b|<input[^>]*type=[\"']checkbox|\bwindow\.(?:alert|confirm|prompt)\(|(?<![\w.])(?:alert|confirm|prompt)\(")
GLYPHS = "☰×⌄›‹✓✔✕✖↑↓←→■□▶▸▾▼▲◀✦⇄⚙⋯⋮＋✎⟳↻"
GLYPH = re.compile(f"[{GLYPHS}]")
ICONLIB = re.compile(r"from\s+[\"'](?:lucide-react|react-icons[^\"']*|@radix-ui/react-icons|@heroicons/[^\"']*|@tabler/icons-react|@phosphor-icons/[^\"']*)[\"']")
TOASTER = re.compile(r"import\s*\{[^}]*\bToaster\b[^}]*\}\s*from\s*[\"']sonner[\"']")
FONT = re.compile(r"font-family\s*:(?!\s*inherit)|\bfont-\[(?!inherit\])|fontFamily\s*:(?!\s*[\"']inherit)")
CONSOLE = re.compile(r"\bconsole\.(?:log|debug)\(")
LOCKFILES = ("package-lock.json", "pnpm-lock.yaml", "yarn.lock")
GENERATED = ("apps/web/src/assets/examples.json", "apps/web/src/routeTree.gen.ts", "packages/browser-workspace/src/generated/")


def sh(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def added_lines(base):
    """Yield (path, line_no, text) for every line the PR adds."""
    diff = sh("git", "diff", "--unified=0", "--no-color", f"{base}...HEAD")
    path, line_no = None, 0
    for raw in diff.split("\n"):
        if raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else None
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            line_no = int(m.group(1)) if m else 0
        elif path and raw.startswith("+"):
            yield path, line_no, raw[1:]
            line_no += 1


def is_comment(text):
    s = text.strip()
    return s.startswith(("//", "/*", "*", "{/*"))


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    base = sh("git", "merge-base", base, "HEAD").strip()
    changed = [p for p in sh("git", "diff", "--name-only", "--diff-filter=d", f"{base}...HEAD").split("\n") if p]
    hits = []

    for p in changed:
        if p.startswith(UI_DIR):
            hits.append(("UI-EDIT", p, 0, "shadcn primitive changed"))
        if p.endswith(LOCKFILES):
            hits.append(("PKGMGR", p, 0, "non-Bun lockfile"))
        if p.startswith(GENERATED):
            hits.append(("GENERATED", p, 0, "generated file edited"))

    for path, n, text in added_lines(base):
        if not path.startswith(WEB) or path.startswith(UI_DIR) or is_comment(text):
            continue
        code = path.endswith((".ts", ".tsx", ".css"))
        if not code:
            continue
        if path not in COLOR_EXEMPT and (RAW_COLOR.search(text) or TW_PALETTE.search(text) or TW_ARBITRARY.search(text)):
            hits.append(("COLOR", path, n, text.strip()))
        if path.endswith(".tsx") and NATIVE.search(text):
            hits.append(("NATIVE", path, n, text.strip()))
        if path.endswith(".tsx") and GLYPH.search(text):
            hits.append(("GLYPH", path, n, text.strip()))
        if ICONLIB.search(text):
            hits.append(("ICONLIB", path, n, text.strip()))
        if TOASTER.search(text):
            hits.append(("TOASTER", path, n, text.strip()))
        if path != WEB + "styles.css" and FONT.search(text):
            hits.append(("FONT", path, n, text.strip()))
        if CONSOLE.search(text):
            hits.append(("CONSOLE", path, n, text.strip()))

    for kind, path, n, text in hits:
        loc = f"{path}:{n}" if n else path
        print(f"{kind:9} {loc}  {text[:140]}")
    if hits:
        counts = {}
        for h in hits:
            counts[h[0]] = counts.get(h[0], 0) + 1
        print("\n" + " · ".join(f"{k} {v}" for k, v in sorted(counts.items())), file=sys.stderr)
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()

# Playground design system

What the playground UI is built from, so a PR can be checked against it. Read the files at the PR's base when in doubt; they win over this page.

## Stack

- shadcn/ui, style `base-lyra`, on Base UI (`@base-ui/react`), base colour `neutral` (`apps/web/components.json`). Primitives live in `apps/web/src/components/ui/`: alert-dialog, button, button-group, checkbox, collapsible, dialog, dropdown-menu, field, hover-card, input, label, resizable, select, separator, sheet, sidebar, skeleton, sonner, tabs, textarea, toggle, toggle-group, tooltip.
- Tailwind CSS v4 with tokens in `apps/web/src/styles.css`; `cn()` from `@/lib/utils` to merge classes.
- Icons: Hugeicons only (`HugeiconsIcon` + `@hugeicons/core-free-icons`), mostly `strokeWidth={1.5}` (some `2`; match the neighbours), `aria-hidden` when a label is next to it.
- Toasts: `sonner` through `ui/sonner.tsx` (`<Toaster>` from the wrapper; `toast()` may be imported from `sonner`).
- Font: JetBrains Mono Variable for everything (`--font-sans`). No other font families.
- Editor: CodeMirror 6 with a Shiki theme (`components/shiki-editor.ts`, which may hold its own colours).

## Colour

The palette is greyscale: `--primary` is near-black in light mode, so primary buttons are black. Colour carries meaning only (destructive red, ANSI output colours, chart tokens).

| Use | Token / class |
|-----|---------------|
| page, text | `bg-background`, `text-foreground` |
| secondary text | `text-muted-foreground` |
| panels, cards, popovers | `bg-card`, `bg-popover`, `bg-muted` |
| hover / selected | `bg-accent`, `text-accent-foreground` |
| borders, inputs, focus | `border-border`, `border-input`, `ring-ring` |
| errors | `text-destructive`, `bg-destructive/10` |
| sidebar | `bg-sidebar`, `text-sidebar-foreground`, … |
| program output colours | `--ansi-fg-*` |

Findings:

- raw hex/rgb/oklch, Tailwind palette classes (`text-red-500`, `bg-teal-600`) or arbitrary colours (`bg-[#20b6b0]`) in components: use a token. A view-scoped CSS variable derived from tokens is fine (#136 kept a few).
- a new brand or accent colour, or a different primary: a maintainer decision, not a reviewer nit. #105 (teal Run button) was closed because one teal button didn't fit a black-primary theme and making teal the primary would recolour every primary button. Raise it as **Verify** and tag the maintainers.
- contrast below 4.5:1 for text (3:1 for large text and icons), including text on a disabled button that is the only place a message shows.

## Components

| Need | Use | Not |
|------|-----|-----|
| choose one of many | `ui/select` | `<select>` |
| menu / picker | `ui/dropdown-menu` | a hand-rolled popover with document click/Escape listeners |
| modal | `ui/dialog`, `ui/alert-dialog` | `<dialog>`, `window.confirm` |
| side panel on mobile | `ui/sheet` | custom fixed div |
| tooltip | `ui/tooltip` | `title` alone on icon buttons |
| on/off | `ui/checkbox`, `ui/toggle` | raw `<input type="checkbox">` |
| resizable panes | `ui/resizable` with `useDefaultLayout` | manual `localStorage` layout parsing |
| loading placeholder | `ui/skeleton` | custom shimmer |
| icon | `HugeiconsIcon` | Unicode glyphs (☰ × ⌄ › ✓ ↑ ■), other icon packs |

Logos are not icons: a glyph standing in for a provider logo with no asset is acceptable (#136, withdrawn).

## Layout and behaviour

- Breakpoint: `useIsMobile()` is `< 768px`; `useIsDesktop()` for the large layout. Test at 390×844.
- The sidebar collapses (`?sidebar=collapsed`) and panes resize; new panels must fit both.
- Buttons in the editor toolbar are compact (`size="sm"`/icon); labels may hide below `sm`, so the button then needs `aria-label`.
- Long-running actions keep the Run button in place and show progress on it; failures stay visible until read.

## Wording

Use the names the UI already uses: **Local Space**, **Try It**, **agent view**, **Run** / **Stop**. Renames must cover every string, toast and label (#136 left "bal-bot" in three places). UI text changes are reviewed by the documentation team per the PR template.

# Caruca Design System (Caruca v2)

Design system for **Caruca** — the research project "Caruca v2": *LLM-based specification mining for opaque shell commands*. Caruca v2 rigorously compares an LLM-based approach against the hand-written Caruca v1 pipeline (correctness, cost, coverage, consistency), producing evidence for a white-paper resubmission — and an application (CLI `caruca-v2` plus a planned web evaluation console) behind it.

## Sources
- GitHub repo: https://github.com/tirandagan/caruca_v2 (branch `main`) — the primary and only source. Visual identity extracted from `scripts/md-to-pdf/` (the project's branded PDF pipeline: `styles.ts`, `cover.ts`, fonts, logo) and product context from `ai_docs/prep/*.md`, `memory/*.md`, and `ai_docs/refs/caruca_white_paper.md`. Explore the repo to design better against this product.
- No Figma, decks, or app UI code exist yet; the planned Web GUI (side-by-side v1/v2 terminal comparison + metrics panel) is specified in `ai_docs/prep/component_functionality.md` and recreated here as the Eval Console UI kit.

## Brand in one line
A rigorous, academic instrument: ink-navy text, one electric blue, a teal accent, flat white pages, and mono type wherever a command, spec, or number appears. Feels like a beautifully typeset systems paper, not a SaaS product.

## CONTENT FUNDAMENTALS
- **Voice:** first-person researcher ("I want to determine…", "we want the evaluation harness's results…"). Precise, hedged where honest ("not yet decided", "deliberately qualitative at this stage"). Claims are always qualified by methodology.
- **Casing:** sentence case everywhere — headings, buttons, labels. Uppercase is reserved for micro-labels (table headers, callout titles, code-language tags) with 0.05em tracking.
- **Terminology is exact and versioned:** "v1" vs "v2", "naive-LLM baseline", "v1-faithful" vs "v2-extended" profiles, "Q2-style comparison", "ground truth". Never blend conditions ("plain docs" and "augmented docs" are separately labeled, always).
- **Commands, flags, files are always mono:** `caruca-v2 compare rm --variance 5`, `cmp_specs.py`, `--backend firecracker`.
- **Numbers carry their basis:** "52/52", "+/-N% on Q2 exact-match", "Nx cost". Percent-change roll-ups are the headline format.
- **No emoji. No exclamation marks. No marketing superlatives.** Enthusiasm is expressed through precision.
- Example microcopy: button "Run comparison", empty state "No runs yet — telemetry records appear here after the first `caruca-v2` run.", callout title "OPEN QUESTION".

## VISUAL FOUNDATIONS
- **Color:** ink `#0B1F33` for text and the mark; one blue `#2563EB` for actions, links, and section heads; teal `#0E7490` strictly as a secondary accent (gradient bars, decorative concentric rings at very low opacity). Semantic green/amber/red only for status. Backgrounds are white; gray surfaces (`#F6F8FA`, `#F1F5F9`) mark code and table heads only.
- **Type:** Lexend Deca (400/600/700) for everything; JetBrains Mono for code, commands, telemetry numbers. Body 15px/1.5 with +0.01em tracking; headings tighten to −0.01em; micro-labels uppercase 11px +0.05em. H2s are blue — a distinctive tic from the paper styling.
- **Spacing:** generous document rhythm; 4px base scale; content blocks padded 16px.
- **Backgrounds:** flat white. The only decoration is the teal→ink gradient accent bar (80×4px, 2px radius) and faint concentric teal rings (rgba(14,116,144,.01–.04)) bleeding off a corner on covers/heroes. No photos, no textures, no illustrations.
- **Borders & shadows:** hairline borders do the separating (`#D0D7DE` strong, `#E2E8F0` default); zebra striping on tables. The system is flat — the single shadow token is for overlays/dialogs only.
- **Radii:** small and precise — 6px blocks/cards/callouts, 4px chips/inline code, 3px checkboxes. Nothing pill-shaped except status badges.
- **Callouts:** 4px colored left border, tinted background, rounded right corners only (0 6px 6px 0), uppercase colored title. Info/warning/tip/danger.
- **Tables:** uppercase 12px gray-600 headers on `#F1F5F9`, 2px `#334155` header underline, 1px row rules, even-row zebra `#F8FAFC`.
- **Motion:** essentially none in source. Use restrained 120–160ms ease-out color/opacity transitions; no bounces, no slides.
- **States:** hover = darker blue (`#1D4ED8`) or surface tint; focus = 2px blue outline offset 2px; press = same color, no shrink; disabled = 45% opacity.
- **Imagery:** cool, technical, monochrome-plus-blue. Diagrams over photos.

## ICONOGRAPHY
- The repo ships **no icon set** — the only mark is the logo (`assets/logo.png`, 400×267 PNG: a pickaxe mining an ink-navy cube that cracks open into blue circuit traces). Unicode/text stand-ins appear in source (✓ checkmark, → arrows in diagrams); no emoji anywhere.
- **Substitution (flagged):** components and UI kits use [Lucide](https://lucide.dev) via CDN — 1.5–2px stroke icons match the brand's precise, technical line quality. Swap in a real icon set if one is adopted.
- Logo clear space ≈ the cube's height/4; never recolor; on dark, place on white/light chip. Where a mark is unavailable, set "Caruca" / "Caruca v2" in Lexend Deca 700 ink.

## Intentional additions
- Standard component set (no app UI exists yet to copy): Button, Input, Select, Checkbox, Radio, Switch, Tabs, Card, Badge, Callout, CodeBlock, MetricStat, DataTable — styled strictly from the PDF-pipeline foundations.
- `MetricStat`, `CodeBlock`, `DataTable` added because telemetry numbers, commands, and comparison tables are the product's core content.
- Spacing scale and interaction states are inferred (source is print-only); flagged here for review.

## Index
- `styles.css` — global entry (imports everything below)
- `tokens/` — `colors.css`, `typography.css`, `spacing.css`
- `assets/` — `logo.png`, `fonts.css`, `fonts/` (Lexend Deca ×3, JetBrains Mono)
- `guidelines/` — foundation specimen cards (colors, type, spacing, brand)
- `components/forms/` — Button, Input, Select, Checkbox, Radio, Switch
- `components/display/` — Card, Badge, Callout, CodeBlock, MetricStat, DataTable
- `components/navigation/` — Tabs
- `ui_kits/eval-console/` — the planned Web GUI recreated: runs list, side-by-side v1/v2 terminal comparison, comparison report
- `SKILL.md` — agent-skill entry point

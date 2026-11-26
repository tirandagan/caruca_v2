---
name: Caruca v2
description: A rigorous, academic instrument on flat white paper. Recorded from the built PaSh benchmark report (2026-11-24) against the caruca-design skill and the PDF pipeline's tokens.
colors:
  ink: "#0B1F33"
  blue: "#2563EB"
  teal: "#0E7490"
  gray-700: "#374151"
  gray-600: "#475569"
  gray-500: "#616B73"
  surface-page: "#FFFFFF"
  surface-code: "#F6F8FA"
  surface-thead: "#F1F5F9"
  surface-info: "#EFF6FF"
  border-strong: "#D0D7DE"
  border-subtle: "#E5E7EB"
  src-pash: "#4a4a4a"
  src-naive: "#2563EB"
  src-cpash: "#e8622b"
  src-cmain: "#f0b060"
typography:
  display:
    fontFamily: "Lexend Deca, -apple-system, Segoe UI, sans-serif"
    fontSize: "22pt"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.015em"
  headline:
    fontFamily: "Lexend Deca, -apple-system, Segoe UI, sans-serif"
    fontSize: "15pt"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Lexend Deca, -apple-system, Segoe UI, sans-serif"
    fontSize: "11pt"
    fontWeight: 600
    letterSpacing: "-0.005em"
  body:
    fontFamily: "Lexend Deca, -apple-system, Segoe UI, sans-serif"
    fontSize: "10.5pt"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0.005em"
  stat:
    fontFamily: "Lexend Deca, -apple-system, Segoe UI, sans-serif"
    fontSize: "13pt"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  table:
    fontFamily: "Lexend Deca, -apple-system, Segoe UI, sans-serif"
    fontSize: "9.3pt"
    fontWeight: 400
  label:
    fontFamily: "Lexend Deca, -apple-system, Segoe UI, sans-serif"
    fontSize: "8.6pt"
    fontWeight: 600
    lineHeight: 1.3
  caption:
    fontFamily: "Lexend Deca, -apple-system, Segoe UI, sans-serif"
    fontSize: "8.6pt"
    fontWeight: 400
    lineHeight: 1.4
  mono:
    fontFamily: "JetBrains Mono, Consolas, monospace"
    fontSize: "8.3pt"
    fontWeight: 400
    lineHeight: 1.45
  chrome:
    fontFamily: "Lexend Deca, -apple-system, Segoe UI, sans-serif"
    fontSize: "8pt"
    fontWeight: 400
rounded:
  xs: "3px"
  sm: "4px"
  md: "6px"
  swatch: "2px"
spacing:
  space-1: "4pt"
  space-2: "8pt"
  space-3: "12pt"
  space-4: "16pt"
  section: "18pt"
  page-top: "0.95in"
  page-side: "0.8in"
  page-bottom: "0.8in"
components:
  source-column-head:
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    padding: "6pt 7pt 4pt 7pt"
  board-cell:
    typography: "{typography.stat}"
    padding: "4pt 7pt"
  board-cell-reference:
    backgroundColor: "{colors.surface-thead}"
    typography: "{typography.stat}"
    padding: "4pt 7pt"
  diff-cell-changed:
    backgroundColor: "{colors.surface-thead}"
    textColor: "{colors.ink}"
    typography: "{typography.table}"
    padding: "4pt 7pt"
  script-box:
    backgroundColor: "{colors.surface-code}"
    textColor: "{colors.ink}"
    typography: "{typography.mono}"
    rounded: "{rounded.md}"
    padding: "6pt 8pt"
  caption:
    textColor: "{colors.gray-600}"
    typography: "{typography.caption}"
  running-head:
    textColor: "{colors.gray-500}"
    typography: "{typography.chrome}"
---

# Design System: Caruca v2

## Overview

**Creative North Star: "The Typeset Systems Paper"**

Caruca's documents look like a well-set systems paper, not a product. One sans face (Lexend Deca) at three weights does every job from the page title to the running foot; one mono face (JetBrains Mono) marks every command, file name and script. The page is flat white; hairline rules separate, nothing is shadowed, and colour is spent only where it carries a meaning the reader needs: blue on section heads, teal on list markers, and, in a comparison report, one colour per source of data.

The identity was established in the PDF pipeline (`scripts/md-to-pdf/`) and codified in the `caruca-design` skill; this file records how it landed in the first hand-authored report surface, the PaSh benchmark comparison of 24 November 2026. Where the report departs from the skill's stated values, the departure is recorded as what was built and the skill's value is named beside it. The skill remains the authority for new screen surfaces; the report's values are the authority for the *report* surface.

Density is editorial: body copy is capped at 72 characters, tables run the full measure, and a page carries one idea with its evidence. Numbers are set with tabular figures document-wide and always carry their basis beneath them.

**Key Characteristics:**
- Flat white paper; hairline rules do all the separating.
- Lexend Deca 400/600/700 only (no italic cut is shipped); JetBrains Mono for anything a shell would read.
- Blue section heads; teal appears only as the list marker.
- A comparison board whose columns are colour-capped by source and whose reference column is tinted.
- Figures are lettered in the same faces and filled with the same four source colours as the tables.

## Colors

Ink on white, one working blue, a reserved teal, and a four-colour family that exists only to tell data sources apart.

### Primary
- **Ink navy** (`ink`): all running text, the page title, table row heads, the wordmark in the running head, and the fill of the logo. Nothing is set in pure black.
- **Electric blue** (`blue`): section heads (h2), the command words in a script listing, and, in a comparison report, the naive LLM's source colour. This blue carries two meanings in the report (heading and source) and no surface may add a third.

### Secondary
- **Teal** (`teal`): in body documents it is spent only on list markers. The pipeline's cover and the Markdown pipeline's page title also use it in the 80×4 teal-to-ink accent bar; this report does not draw that bar.

### Source family (report surface addition)
One colour per source of annotation files, shared by the stylesheet and the figure scripts. A source's colour caps its column (a 3px top border on the column head) in every table and fills its bars and boxes in every figure.
- **PaSh's own files** (`src-pash`, dark grey): the reference. Its column is always the first data column and its cells are tinted `surface-thead`.
- **Naive LLM's files** (`src-naive`): the identity blue, reused deliberately.
- **Caruca's files, PaSh grammar** (`src-cpash`, orange).
- **Caruca's files, main grammar** (`src-cmain`, light orange).
- A column that is not a source of files in the run (the paper's published numbers in Table 3) has no cap and no colour.

### Neutral
- **Gray 700** (`gray-700`): table row heads in the board, the source-key legend.
- **Gray 600** (`gray-600`): captions, version lines, column-head sub-lines, the "whole" state in the differences table, muted cells.
- **Gray 500** (`gray-500`): script comments, and the running head and foot text.
- **Paper** (`surface-page`): the page.
- **Code surface** (`surface-code`): the script listing's body.
- **Head surface** (`surface-thead`): the script box's title bar, the reference column's cells, and the "changed" cells in a differences table. It is the only tint in the report.
- **Info surface** (`surface-info`): text selection only.
- **Strong rule** (`border-strong`): the box border, the line under a table head, the line that closes a table.
- **Subtle rule** (`border-subtle`): row rules, the box's inner dividers, and (at 0.5pt) the running head and foot rules.

### Named Rules
**The One Colour Per Source Rule.** Each source of data owns exactly one colour, and that colour appears everywhere the source does: column cap, figure fill, legend swatch. PaSh's own files are always the tinted reference column. Figures read the same four values as the stylesheet.

**The One Tint Rule.** A body document has one tint, `surface-thead`. It marks the reference column and the cells that differ from it; it never marks emphasis. A cell whose meaning rests on the tint also carries weight 600, so a greyscale print still reads.

**The Spent Teal Rule.** Teal is a mark, not a colour family: list markers in the body, the accent bar on covers and Markdown titles. It is never a fill, a head colour or a border.

## Typography

**Display Font:** Lexend Deca (with -apple-system, Segoe UI, sans-serif)
**Body Font:** Lexend Deca
**Label/Mono Font:** JetBrains Mono (with Consolas, monospace)

**Character:** one humanist sans at three weights, doing display and body alike, so the page reads as a single voice; mono is reserved for anything a shell would read, so a command never passes as prose. Lexend Deca ships in 400, 600 and 700 only and in no italic cut; `em` in body copy renders a synthesized oblique, which is tolerated for author intent in prose and never used on a designed element.

### Hierarchy (report surface, as built)
- **Display** (700, 22pt, 1.15, −0.015em): the document title, once, balanced across two lines. *The skill's print scale sets the page title at 28pt.*
- **Headline** (600, 15pt, 1.2, −0.01em, blue): section heads. *The skill sets h2 at 20pt, weight 700.*
- **Title** (600, 11pt, −0.005em, ink): sub-sections and addendum entries. *The skill sets h3 at 15pt.*
- **Minor head** (600, 9.6pt): group heads inside the addendum's script list.
- **Body** (400, 10.5pt, 1.5, +0.005em): paragraphs, capped at 72ch. *The skill's print body is 11pt with +0.01em tracking.*
- **Lead** (400, 10.3pt, 1.4, uncapped): the opener's four labelled summary paragraphs; the label is a 600 run-in, never a kicker.
- **Stat** (600, 13pt, 1.15, −0.01em): the leading figure in a board cell, with a **basis line** (400, 8.3pt, 1.3, gray-600) beneath it.
- **Table** (400, 9.3pt): cell text; column heads 600, 8.6pt, ink, sentence case; column-head sub-lines 400, 8pt, gray-600. *The skill's Markdown-pipeline tables use uppercase 9pt gray-600 heads with +0.03em tracking on a tinted head row; the report's board does not.*
- **Caption** (400, 8.6pt, 1.4, gray-600): below tables and figures; the "Table n." / "Figure n." label is 600 ink. A table's caption above it (`tcap`) is 9pt ink.
- **Mono** (400, 8.3pt, 1.45): the script listing and the script list table; inline code is 0.95em of its context, and 1em inside captions and sub-lines.
- **Chrome** (400 and 600, 8pt): the running head ("Caruca v2" at 600 ink; running title at 400 gray-500) and foot ("CARUCA V2" and "Page n of N" at 400 gray-500).

### Named Rules
**The Basis Line Rule.** A number set large is never alone: a 13pt figure sits over an 8.3pt grey line stating what it is out of or compared against ("3 of 3", "1.67× faster than bash").

**The Mono Means Shell Rule.** Command names, flags, file paths, script text and commit hashes are mono; nothing else is. Numbers in tables are the sans with tabular figures, not mono.

**The Run-in Label Rule.** A paragraph that needs a label gets a 600-weight run-in on its first words ("What we ran."), in sentence case, in the text colour. No eyebrow, no kicker, no uppercase label above a heading.

## Layout

Letter portrait. Margins: 0.95in top, 0.8in sides and bottom; the running head sits in the top margin and the foot in the bottom one, both stamped after render in the real brand font. Text measures the full 6.9in width for tables and figures, and is capped at 72ch for paragraphs, lists and definition lists.

The opener is a two-column grid (1.45fr : 1fr, 16pt gutter): the summary on the left, the artefact under study (a boxed script listing) on the right, and the comparison board full-width beneath them, so the first page carries title, summary, evidence and the board without a turn.

Vertical rhythm is in points: 4pt between list items and under table captions, 6–8pt under paragraphs and under a title, 12pt under a caption, 14pt above a sub-section, 18pt above a section head, 16pt between grid columns. Figures are generated at the text width (6.5in, 300dpi) and placed at 100%, or 84% centred for a narrow figure.

Page breaks are declared, not left to flow: a section that must open a page carries `break-before: page`; every heading and table caption refuses a break after itself; a table and a figure refuse to break inside; the caption under a board refuses to break before. Only the long script list may split across pages, with its head row repeated and each row kept whole.

### Named Rules
**The Board Whole Rule.** A comparison board, its caption above and its note below are one unit; they never straddle a page.

**The 72ch Rule.** Prose is capped at 72 characters; evidence (tables, figures, the script box) runs the full measure.

## Elevation & Depth

No shadows. The system is flat: hairline rules (1px `border-strong` and `border-subtle`, 0.5pt in the page chrome) and the single `surface-thead` tint convey all structure. The one shadow token the skill defines is for screen overlays and dialogs only and has no place in a document.

**The Flat Paper Rule.** A document never casts a shadow. Depth, where needed, is a 1px rule or the one tint.

## Shapes

Corners are small and precise. Boxed listings and code blocks take 6px; inline chips 4px and checkboxes 3px in the Markdown pipeline; the legend swatch is 8×8pt at 2px. Tables have no outer frame: the head is underlined with `border-strong`, rows with `border-subtle`, and the last row closed with `border-strong`. A source column is capped with a 3px top border in the source's colour, the only coloured border in the system. Figures are drawn with top and right spines removed, the same openness as the tables.

## Components

### Comparison board
The report's signature. A table whose first column is the row head (17% of the width, 600, gray-700) and whose remaining columns each belong to one source.
- **Column head:** 600, 8.6pt, ink, sentence case, bottom-aligned, capped with a 3px bar in the source's colour; beneath the name a 400, 8pt, gray-600 sub-line says what the source is ("the files that ship with PaSh, hand-written").
- **Cell:** a 13pt 600 stat over an 8.3pt gray-600 basis line; 4pt 7pt padding; rows ruled with `border-subtle`.
- **Reference column:** PaSh's own files, first data column, every cell tinted `surface-thead`.
- **Four-column variant:** row head 28%, data columns 24%, used when a column is a published figure with no source colour.
- **Caption above** (9pt ink, "Table n." at 600) states what the table shows; the **note below** (8.6pt gray-600) carries the control or baseline value.

### Differences table
Same head treatment; cells hold a one-word state. "split" is 600 ink; "whole" is 400 gray-600; a cell that differs from the reference is tinted `surface-thead` and set 600 ink, so the tint and the weight both carry the meaning.

### Script box
A 1px `border-strong` frame at 6px radius: a title bar on `surface-thead` (script name at 600, its provenance at gray-600, 8.5pt), the listing in mono 8.3pt on `surface-code` with command words in blue 600 and comments in gray-500, and an optional note strip below the listing at 8.3pt gray-600 above a `border-subtle` rule.

### Figures
Generated by script at 6.5in × 300dpi, lettered in Lexend Deca with mono command names, filled with the four source colours, spines top and right removed, grid lines `#e4e3df`. A figure sits at 100% width with 6pt above and 12pt below and its caption ("Figure n." at 600 ink, the rest gray-600 8.6pt) directly beneath.

### Source key
A wrapped row of legend entries, 8.6pt gray-700, each an 8pt swatch at 2px radius in the source's colour followed by the source's name; 14pt between entries.

### Running head and foot
Stamped on every page with pdf-lib in the embedded Lexend Deca files. Head: the logo at 12pt tall, "Caruca v2" at 600 8pt ink, the running title right-aligned at 400 8pt gray-500, a 0.5pt `border-subtle` rule beneath. Foot: a matching rule, "CARUCA V2" left and "Page n of N" right, 400 8pt gray-500. Chromium's own header and footer templates are not used; they cannot load the brand font.

### Lists and definitions
Bulleted lists indent 1.1em with teal markers and 4pt between items. A glossary is a definition list with the term at 600 run in to its definition, 3pt between entries. Addendum entries are paragraphs with a 600 run-in label, 9pt apart.

## Do's and Don'ts

### Do:
- **Do** give every source of data one colour and use it for its column cap, its figure fills and its legend swatch, in both the stylesheet and the figure scripts.
- **Do** put PaSh's own files (or whatever the reference is) in the first data column and tint its cells `surface-thead`.
- **Do** set a large number over its basis line; "0.64 s" over "1.67× faster than bash".
- **Do** cap prose at 72ch and let tables, figures and listings run the full measure.
- **Do** declare page breaks: `break-before: page` on a section that opens a page, `break-after: avoid` on every heading and table caption, `break-inside: avoid` on tables and figures.
- **Do** stamp the running head and foot after render with the embedded Lexend Deca files, at 8pt, with a 0.5pt rule.
- **Do** letter figures in Lexend Deca and JetBrains Mono at 300dpi and the text width, with the top and right spines removed.
- **Do** carry a tinted cell's meaning in weight as well, so greyscale print reads.

### Don't:
- **Don't** add a second tint; `surface-thead` is the only one in a document, and it marks reference and difference, never emphasis.
- **Don't** use teal as a fill, head colour or border; it is a list marker in body documents and the accent bar on covers.
- **Don't** set numbers in mono inside a sans table; tabular figures in the sans line up already.
- **Don't** add kickers, eyebrows or uppercase labels above headings; a labelled paragraph gets a 600 run-in on its first words.
- **Don't** cast a shadow on anything in a document.
- **Don't** italicise a designed element; Lexend Deca has no italic cut and the browser will fake one.
- **Don't** use Chromium's header and footer templates for the running head and foot; they fall back to Times.
- **Don't** give a column that is not a source of files a colour cap.


## Conference variant (2026-11-26)

Reports that may become part of a paper, or go to the advisors as paper-grade documents, switch the type to the
ACM `acmart` look (Tiran's call, ISSTA 2027 target): Libertinus Serif 10/12 pt justified text, Libertinus Sans bold
headings in ink (no blue), Inconsolata code, numbered sections with appendix A.1..A.n, booktabs tables (1.2 pt top
and bottom rules, 0.6 pt under the head, no vertical rules), captions in 8.8 pt sans with a bold "Figure n:" label.
The source-colour family, the comparison board, the tinted reference column and the page-break rules above are kept.
First instance: `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/report/` (the academic block at the
end of its `report.css`; fonts in `scripts/md-to-pdf/fonts/academic/`).

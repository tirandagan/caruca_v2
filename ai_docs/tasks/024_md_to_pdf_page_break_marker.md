# Task 024: a page-break marker for the Markdown-to-PDF converter

**Requested by:** Tiran, 2026-11-24. **Status:** in progress (Antigravity agent, pane "Converter: page-break marker").

## Goal

Reports written in Markdown and converted with `npm run convert -- <file.md>` (`scripts/md-to-pdf.ts`,
`scripts/md-to-pdf/*.ts`) need a way to say "start a new page here". Today the only way is raw HTML
(`<div style="page-break-before: always"></div>`), which is ugly in the source and easy to get wrong. Add a
simple Markdown marker the converter turns into a page break.

## What to build

- A marker that reads well in Markdown and is harmless elsewhere (e.g. GitHub). Preferred:
  `<!-- pagebreak -->` on its own line; also accept `\pagebreak` and `\newpage` on their own line.
- The converter turns it into an element that forces a page break in the PDF (`break-before: page` /
  `page-break-before: always`), with no visible output and no empty paragraph left behind.
- It must work in both places people will use it: between sections of the body, and right before a
  heading (the heading must land at the top of the new page, with the converter's existing
  "keep heading with next paragraph" rules still working).
- Add it to the converter's help/README text (`scripts/md-to-pdf/README.md` if there is one, else the
  header comment of `scripts/md-to-pdf.ts`) with a two-line example.
- A test: a small Markdown file under `scripts/md-to-pdf/` (or the repo's existing test location) with
  three markers; the converted PDF has the expected page count and each marked heading starts a page
  (check with `pdftotext -layout` or `pdfinfo`). Keep the test file tiny.

## Where to look

- `scripts/md-to-pdf/converter.ts` (markdown-it is configured with `html: true`; see how it renders and
  where custom handling such as diagrams is hooked in, `diagrams.ts`).
- `scripts/md-to-pdf/styles.ts` (print CSS; headings have `break-before: avoid` rules that must not
  cancel the explicit break).
- `scripts/md-to-pdf/toc.ts` uses `page-break-after: always` already, so the print engine honours it.

## Rules

- Change only the converter files and their docs/tests. Do not touch report content.
- Verify by converting `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/report_draft.md` after
  inserting the marker before `## What we ran`, `## What we saw` and `## Addendum` **in a scratch copy** (not the
  original), and checking those headings start new pages.
- Do not commit or push. Report: the marker syntax, the files changed, and the test result.

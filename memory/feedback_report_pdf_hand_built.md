---
name: feedback-report-pdf-hand-built
description: 2026-11-24 Tiran: reports for Michael are no longer made with `npm run convert`; they are hand-authored HTML+CSS rendered by a per-report build.ts (puppeteer, repo fonts/tokens), laid out with the impeccable skill; structure = "comparison board"
metadata:
  type: feedback
---
**Rule (Tiran, 2026-11-24):** the Markdown-to-PDF converter (`npm run convert`) is not good enough for
reports Michael reads; "tables, graphs, charts and text layout must be much more professional". Reports are
now **hand-authored HTML + CSS**, rendered by a build script that reuses the repo's brand fonts, colour
tokens and running head/foot (`scripts/md-to-pdf/tokens.ts`, `templates.ts`) via puppeteer. First
instance: `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/report/` (`report.html`,
`report.css`, `build.ts`, `README.md` with the update procedure). Build:
`npx tsx <that folder>/build.ts` from the repo root; pages: `pdftoppm -r 70 -png report.pdf /tmp/p`.

**Why:** the converter drops alt text, keeps tables whole (pushing them to new pages), inserts a
contents page, and can't do side-by-side layouts; Tiran had to ask for fixes four times in one session.

**How to apply:** design with the `impeccable` skill (Read mode; the Caruca identity is the established
world; surface structure chosen on its decision page — Tiran locked **"Comparison board"**: the four
annotation sources as four colour-topped columns through every table, PaSh's own files as the tinted
reference column). Keep: numbered tables/figures with captions, rates as "a of b", no kicker labels, forced
page breaks only before the paper comparison and the addendum, everything else flows. Finish with the
skill's reviewer on the page renders. The Markdown draft stays only as a record.
Related: [[feedback-greenberg-report-style]], [[reference-md-to-pdf-wide-diagrams]].

**Build facts (2026-11-24, verified by `pdffonts` and page renders):** Chromium's puppeteer header/footer
templates cannot load the brand font even as an inline data-URI `@font-face` (they rendered Times), so
`build.ts` renders the body with `displayHeaderFooter: false` and stamps the running head/foot afterwards
with pdf-lib + `@pdf-lib/fontkit` (added as a devDependency) using `scripts/md-to-pdf/fonts/LexendDeca-*.ttf`
and the logo PNG. puppeteer margins must be given in `in`/`px`, not `pt`. For matplotlib figures, register
the TTFs with `font_manager.fontManager.addfont` (JetBrains Mono ships as woff2; a TTF converted with
fonttools lives in `figures_interim/fonts/`). `scripts/md-to-pdf/templates.ts` also got the inline font
embed, a 75-character title limit and gray-500 running text; harmless for the Markdown converter.
Layout rules that survived the finish review: the board (Table 1) must sit whole on page 1 with its one-line
caption; only the addendum forces a page break; tables and figures don't break inside; put a figure after the
paragraph that cites it, never right under a heading at a page end. Finish review + critique snapshots:
`.impeccable/critique/2026-11-24T18-04-31Z__…report-html.md`.


## Update 2026-11-26: conference typography for paper-bound reports

Tiran: "when generating the pdf - use font, text size, etc - which are congruent with an academic conference. they
use latex" (ISSTA as the example). ISSTA requires ACM `acmart` with `acmsmall` (single column); no font size is
stated there, so the report uses acmart's look: Libertinus Serif 10/12 pt text, Libertinus Sans bold black
headings, Inconsolata code, numbered sections, appendix A.1..A.n, booktabs tables, "Figure n:" captions.
Fonts are in `scripts/md-to-pdf/fonts/academic/` with TrueType conversions in `ttf/` (Chromium embeds CFF OTF as
Type 3; pdf-lib garbles subsetted conversions, so stamp unsubsetted; avoid "fi" in the stamped running title).
**How to apply:** any report that may become part of the paper or go to the advisors uses this academic block
(see the report folder's README); the Lexend Deca house style stays for internal documents.

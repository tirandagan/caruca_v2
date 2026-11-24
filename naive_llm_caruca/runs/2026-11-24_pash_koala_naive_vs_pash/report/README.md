# The report for Michael: how it is built and how to update it

The report is hand-authored HTML, not converted Markdown, so its layout can be exact: `report.html`
(content) and `report.css` (layout), rendered to `report.pdf` by `build.ts` with the repo's own brand
fonts and colour tokens (`scripts/md-to-pdf/tokens.ts`); the running head and foot are stamped on afterwards with pdf-lib in the brand face (Chromium's own header templates cannot load it), so it stays
one system with the other Caruca documents. The earlier Markdown draft (`../report_draft.md`) is kept
for the record and is no longer the source.

## Build

```sh
cd <repo root>
npx tsx naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/report/build.ts
# optional second argument: the running-head title
```

It prints the page count. To look at the pages: `pdftoppm -r 70 -png report/report.pdf /tmp/p`.

## Structure (the "comparison board", chosen by Tiran on 2026-11-24)

The four annotation sources are four columns that run through every table: PaSh's own files (the
reference, dark grey, tinted cells), the naive LLM's (blue), Caruca's PaSh grammar (orange), Caruca's main
grammar (light orange). The same four colours are used in the figures. Pages: opener (title, one version
line, the summary in four short labelled paragraphs beside the script in a box, then Table 1, the board);
where the sources differ (Table 2, Figure 1, the faults list); time (Figures 2 and 3, then Figure 4);
next to the paper (Table 3) and what this does not show; addendum (A1 script path, A2 words used, A3 the
setup for a reader new to PaSh with Figure 3, A5 every script with its folder, A6 records).

## Rules the layout follows

- Every table and figure is numbered and referred to by number in the text.
- Every rate is written "a of b". No kicker/eyebrow labels, no coloured side stripes, no section numbers.
- Page breaks: only `class="page-break"` sections force a new page (the paper comparison, the addendum);
  everything else flows. Tables and figures do not break inside.
- Figures are referenced relative to this folder (`../figures_interim/*.png`); regenerate them with the
  scripts in `../figures_interim/` and rebuild. The figure scripts check their counts against
  `../numbers_pilot.json`.

## Updating for the full run

1. Rebuild the records with `../count_report.py` and the figures with `../make_charts.py` /
   `../figures_interim/make_figures_interim.py`.
2. Replace the numbers in `report.html` from `numbers.md` (every number in the report comes from that
   file). Keep the four-column structure; add rows, never columns.
3. Bump the version line, rebuild, look at every page once, run the finish review (the impeccable skill's
   reviewer) on the page renders.

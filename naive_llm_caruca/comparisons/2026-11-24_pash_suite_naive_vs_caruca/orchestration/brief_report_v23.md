# Brief: Draft 2.3, fix every critique finding (2026-11-27)

Read the two critique files first: `orchestration/critique_2026-11-27_design.md` (design review, 23/40) and
`orchestration/critique_2026-11-27_detector.md` (detector, page fill, links). Tiran: "fix all the issues from the
critique, including the cross-referencing suggestions" and "make sure that links are visually standing out. It's not
clear to me where I can click to follow a link, for instance, in your footnotes under tables." Work in
`naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`; edit `report/` (html, css, build.ts, README),
figure scripts if needed, and the repo root `DESIGN.md`. Records read-only. Do not commit. Keep every rule in
`report/README.md` (single set of results, every finding answers its next question, ACM look, a-of-b rates).

## Links must look clickable (Tiran's explicit ask, do first)
- One link colour for every internal link and footnote mark, distinct from the four source colours (not the naive
  LLM's blue): use ACM's dark link blue-violet, e.g. #3B3F99 (check it differs clearly from #2563EB), plus a thin
  dotted underline (`text-decoration: underline dotted; text-underline-offset: 1.5pt; text-decoration-thickness:
  0.5pt`) so links show in black-and-white print too. Footnote marks in tables in the same colour, slightly bold.
- Every link target lands with its heading visible (ids on headings and captions).

## Design-review priority issues (all of them)
1. Finding line (P0): name all comparators, e.g. "PaSh printed bash's output in 86 of 86 scripts with the naive LLM's
   files and in 77 and 76 of 86 with Caruca's; it split 43 of 177 parts (PaSh's own files 41, Caruca 29 and 40) and
   took 1.15 times PaSh's own time (Caruca 1.09 and 1.10)." Remove "about 5 %".
2. Table 1 verdict cue (P0): cells worse than PaSh's own files get a small ▼ in the source colour and weight 600;
   better ones ▲; ties plain. Row labels carry "↑ better" or "↓ better". Add a closing "Reading" row: one short line
   per column (e.g. "always right; splits slightly more; 15 % slower"). No winner crown.
3. Time on page 1 (P1): the start-up-removed row shows all scripts (from `overhead_adjusted.md`: pooled PaSh's own
   about 0.97, naive 1.26, Caruca small 1.05, full 1.09; compute the pooled own value as the geometric mean of the
   two runs' 1.03 and 0.92) labelled "all 72 scripts over 0.05 s"; the one-pass subset moves to section 5's table.
4. One source column order everywhere (P1): PaSh's own, the naive LLM, Caruca small, Caruca full, then notes/cause.
   Apply to every table and every figure legend/row order.
5. Merge Table 2 into Table 1 (P1) as a lower block headed "Behind the result" with a thin rule; renumber all tables
   and every reference; section 1 opens with Figure 2 and "How it fared".
6. Table notes (P1): ACM-style lettered notes (a, b, c) restarting per table, one note per line with hanging indent,
   each linking to its target and with a ↩ back-link to its row. Body notes stay numbered at the foot of the page.
7. Naming (P2): column header "Caruca, full where traced" with a note mark explaining 22 full grammars + small rest.
8. Legibility and fill (P2): Figure 1 to full column width (or drop it if the text already says it; your call,
   say which); the per-script figure (A.8) split across two pages at legible size (smallest text 7 pt printed);
   fix pages 10 and 14 (31 % and 49 % empty) and keep A.7's heading with its content.

## Cross-referencing improvements (do 1 to 8; skip the ones listed as clutter)
1. PDF outline/bookmarks from h2/h3 and table/figure captions (puppeteer `outline: true` if supported, else build it
   with pdf-lib after rendering).
2. Visible link style (above).
3. Page numbers in references ("Table A.6, p. 13"): two-pass build in build.ts (render, read each anchor's page from
   the PDF's named destinations, inject "p. N", render again).
4. Back-links: ↩ on table notes; each appendix part opens with one line "Supports: …" linking to the body places
   that cite it.
5. Lettered table notes numbered by the build script (above).
6. One contents line on page 1 under the finding line, linked section numbers, 8 pt sans.
7. Running head shows the current section name (CSS string-set if Chromium supports it in print, otherwise set it in
   the pdf-lib stamping pass from the outline); drop the duplicated "CARUCA V2" in the footer, keep "Page n of N".
8. PDF metadata title = the visible title (`<title>` in report.html and pdf-lib `setTitle`).

## Minor observations (all)
- Drop page-1 cells that add nothing (PaSh's own 1.00 time cell may stay as the reference marker, "Parts split …
  the reference" sub-line goes); fold "without cat" sub-lines into one note; "A Addendum" → "A Appendix"; move any
  remaining per-session numbers in captions (Table 6, note 7, A.4) to A.3; Figure 2's 2.7× point: clip with an arrow
  or widen the axis; Table 4's "8 raised" → a note mark.

## Detector findings
- DESIGN.md: add the Libertinus Serif/Sans and Inconsolata fonts to its font tokens for the conference variant (and
  `.impeccable/design.json` if it lists fonts); update the THESIS comment at the top of report.html (it still says
  Lexend Deca). The other detector findings were false positives (unit parsing, hyphenation): no change.

## Build and verify
Version "Draft 2.3, 27 November 2026". Build, render every page, then verify: links count and that every link
destination exists (pypdf), outline entries exist, page numbers in references match the real pages, no page before
the last over a third empty, no split tables, Table 1 on page 1. Update `report/README.md` with the new conventions
(link colour, lettered notes, two-pass page numbers, outline). Reply in at most 10 lines: page count, link and
outline counts, what you chose for Figure 1, and anything not done and why.

# Brief: one set of results, no session split in the body (2026-11-27)

Tiran: the report must present a single set of results across the board. The runs were made in two sessions
(first: bash, PaSh's own, the naive LLM's sets; second: bash, PaSh's own, Caruca's expanded sets), but each source's
time is already normalised to bash and to PaSh's own files of its own run, so the body shows one number per source.
The two sessions are described only in the method appendix (A.3) and in the records table (A.9).

Work in `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`. Edit `report/report.html`, and
`figures_interim/make_figures_interim.py` for Figure 4 only. Do not change any count or record. Do not commit.

1. Table 1, Time row: PaSh's own `2.3 × bash`, sub "the reference" (pooled: 2.38 first run, 2.27 second;
   geometric mean 2.33). Naive `2.7 × bash`, sub `1.15 × PaSh's own`. Caruca small `2.5 × bash`, sub
   `1.09 × PaSh's own`. Caruca full `2.5 × bash`, sub `1.10 × PaSh's own`. No "first/second session" text in
   the table. Same for the naive sed-v2 row: drop any session wording.
2. Remove "first session" / "second session" / "of the same session" / "in two sessions" wording from the body
   (pages 1 to 7: version line, How it was run, Table 2 and its caption, Figure 2 caption, section 3 and 4
   text, Time section, Figure 4 caption, Table 5, threats). Where a sentence needs the idea, say "against PaSh's
   own files run alongside it" once, in the Time section, and point to A.3. Keep the A.3 method paragraph and
   the A.9 records rows that name the two sets of records.
3. Figure 4: one panel, one row per source, top to bottom: the naive LLM, the naive LLM with its second sed
   file (52 scripts), Caruca's small grammar, Caruca's full grammar, PaSh's own files run twice. Each dot is a
   script's time divided by PaSh's own files' time in the same run (the data are unchanged; only the drawing
   merges). For "PaSh's own files run twice", plot both runs' second-copy ratios as one row (172 dots) and draw
   one noise band from their range (0.83 to 1.46) with a lighter inner band for the middle 90 % if it fits;
   right-hand labels per row: geometric mean and "slower than bash: n of 86". Same fonts, colours, size rules.
   Regenerate with `uv run --offline --with matplotlib --with numpy python figures_interim/make_figures_interim.py`
   using the same arguments the report README gives, and check the figure script's self-checks still pass.
4. Glossary "Noise band": one sentence with the pooled range and how many of the 172 runs strayed by more than
   10 %; the 1.46 is one file-encryption script.
5. Build (`npx tsx report/build.ts` from the repo root path given in report/README.md), render every page, keep
   Table 1 on page 1 and no page before the last more than a third empty. Version line "Draft 2.1, 27 November
   2026". Update report/README.md's framing section with the rule: one set of results in the body.
Reply in at most 6 lines: page count, the Table 1 time row as built, and anything you could not do.

# Brief: Draft 2.5, add the larger-input run and what it means (2026-11-27)

Read `report/README.md` (all conventions: single results, every finding answers its next question, live links in the
link colour, lettered table notes, ACM look, page numbers in references, outline) and the current `report/report.html`
(Draft 2.4). Then `full_run_large/README.md` and `full_run_large/numbers.md` (the larger-input run, finished
2026-11-27) and `orchestration/plan_large_inputs.md` (its pre-registered plan). Work in
`naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`; edit `report/` only (and a figure script if you
add a figure). Records read-only. Do not commit.

## Add a section "Larger inputs" (after Time, renumber the rest)

1. **What was run** (3 sentences, link A.x for detail): the plan was written before running; 43 scripts chosen by a
   source-blind rule (group A: 29 where split decisions differ beyond `cat`; group B: 14 that differ only by a `cat`
   split); each script's own input copied 10 or 30 times (up to about 1 GB; COVID's own 3.6 GB input unscaled) as set
   by a bash-only pilot; one session; the naive LLM's files with the second sed file.
2. **One table** (from `full_run_large/README.md` "What was found"): output right, compiler stops, files that raised,
   time against bash, time against PaSh's own, time against Caruca, groups A and B, three source columns in the
   report's order. One number per cell where possible.
3. **What it shows**, four short paragraphs:
   - With work to divide, PaSh's own files make PaSh faster than bash (1.30 times as fast in group A); the naive LLM's
     files about break even (0.97) and Caruca's are slower (0.85). The naive LLM's files are never wrong (43 of 43);
     Caruca's are wrong in 10, one of them new at this size (uniq-ips: a split `uniq` goes wrong only when a repeated
     line falls where two pieces meet, so it depends on the data; the plan had assumed size could not change
     correctness, and that assumption was wrong for this case).
   - Against Caruca the naive LLM's files are faster where Caruca cannot split `sort` (0.37 to 0.81 of its time in
     14 scripts); Caruca is faster only where its splits are wrong (Unix50 26, 28-33) or where its compiler stops and
     plain bash runs.
   - Against PaSh's own files the naive LLM's extra splits pay in three scripts (Unix50 12, 14, 16: 0.59 to 0.71 of
     PaSh's own time) and cost elsewhere (group A 1.33, group B 1.57).
   - Expectations against results: a compact version of the README's table (held 3 of 10 for "faster than PaSh's
     own"; held for Caruca; group B as expected), or a link to it in the appendix if it does not fit.
4. **Why PaSh's own files win on speed** (Tiran asked for this insight explicitly; a titled paragraph, plain words):
   PaSh's own files were written by hand by PaSh's authors for this very benchmark suite. They carry two kinds of
   knowledge: whether a split is safe, and whether a split is worth it in PaSh's runtime. The naive LLM was asked only
   the first; it answers it as well as PaSh's own files do (its output was always right) but says yes to every safe
   split, including ones that cost more than they save in PaSh. Two such decisions explain most of its time: it splits
   a plain `cat` (group B: 1.57 times PaSh's own), and its `tr` file allows only consecutive pieces, never round robin,
   which kept one script correct but makes PaSh run many `tr` uses in a slower way (every script where it took more than
   1.4 times Caruca's time has such a `tr` use; observed, not isolated). Caruca is slower for the opposite reason: it
   splits too little (no `sort` without its options; compiler stops fall back to bash) and sometimes wrongly. So PaSh's
   own 1.30 times bash's speed comes from splitting the right commands; the naive LLM splits the right ones plus
   wasteful ones; Caruca splits too few.
   Two caveats in the same paragraph: group A was chosen because decisions differ, so it shows the differences at
   their largest; and PaSh's own files are not better everywhere (the naive LLM beats them on Unix50 12, 14, 16, its
   `col` refusal is the safer answer, and PaSh's own `tail` file stops the compiler).
   Close with what it means: a naive LLM given only the goal and four examples matched PaSh's hand-written files on
   correctness and beat Caruca on both correctness and speed; it loses to the hand-written files on speed because it
   lacks PaSh-specific cost knowledge (chiefly "do not split a plain `cat`"), a nameable gap rather than poor judgment
   about the commands. Giving it that knowledge would change the prompt, which the naive baseline rules out; it could
   be a separate, labelled variant.

## Update elsewhere
- Page-1 "What we saw": one sentence: with larger inputs PaSh's own files make PaSh faster than bash and the naive
  LLM's files break even, ahead of Caruca's, still never wrong (section n). Keep the subtitle as is.
- Section 5's paragraph "No large script gains from the naive LLM's extra splits" now has a larger-input answer:
  replace its last sentences with a pointer to the new section and its result.
- Threats: remove "larger inputs not tested"; add: the larger inputs are concatenated copies of the small ones; COVID
  unscaled; `tr` recipe cause observed not isolated; group selection shows differences at their largest.
- Table A.x records: add `full_run_large/` and `orchestration/plan_large_inputs.md`.
- Version "Draft 2.5, 27 November 2026". Build, verify links/outline/page numbers as before, render every page, no page
  over a third empty before the last, Table 1 on page 1. Reply in at most 8 lines.

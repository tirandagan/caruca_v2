# Brief: independent check of the pilot run (naive LLM's PaSh files vs PaSh's own)

You are a checker. Another worker built and ran an experiment in this folder:
`naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/`. Its brief is
`orchestration/brief_builder.md`; read it for what was asked. Your job is to find out, **from the raw
records and by re-running things yourself**, whether the results can be trusted. Do not take the
worker's README at its word. Read it last, and only to compare its claims with what you found.

## Check these

1. **The right files were loaded.** For every command in the `naive` set, the three files in the set's
   folder (inside the Lima VM `pash`) are byte-identical to the naive LLM's files in the run folder given
   by the `"repeat": 1` row for that command in `naive_llm_caruca/fig7_campaign/ledger.jsonl`. The
   command is in the set's name table. Every other file in the set equals PaSh's installed package. The
   `pash-own` set equals the installed package exactly
   (`~/pash/python_pkgs/lib/python3.12/site-packages/pash_annotations`). For the `caruca-pash` and
   `caruca-main` sets (see Amendment 1 in the builder's brief): the files for `cat cp cut grep rm sort
   split wc` are byte-identical to the paths in the `v1-pash` / `v1-main` rows of
   `naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/sides.jsonl`, and every other
   command's files equal PaSh's installed package.
2. **PaSh really used the folder it was given.** Re-run one PaSh run yourself with each set and one
   control of your own design: a change to the set's files that should change what splits. Confirm that
   it does.
3. **The splitting claims hold.** For the script's runs, confirm from PaSh's logs and from the record of
   which commands started, and how many copies of each, which commands were split under each set.
   Remember that PaSh falls back to plain bash quietly, so a correct output proves nothing about splitting.
4. **The output claims hold.** Recompute the output hashes, the comparison with bash, and the comparison
   with Koala's stored hash, from the saved files or by re-running.
5. **The annotation answers are real.** Load each set's generator for each command invocation in the
   script yourself, and compare your answers (including any exceptions) with the worker's records.
6. **Timings are honest.** Check the Mac's power log for sleeps during the timed window
   (`pmset -g log`, from the Mac side), and that runs were repeated as the README says.
7. **The README says only what the records support**, in plain words, with every rate given with its
   denominator.

## Rules

- Don't edit the worker's files. Write your findings to `orchestration/review_checker.md`: for each
  check, pass or fail, the evidence (command and output, briefly), and what is wrong if it failed.
- Use your own scratch folder in the VM (e.g. `~/t024-check/`). Never edit PaSh's installed package,
  its source, the Koala checkout, or the worker's VM folder.
- Don't run anything heavy while another job is timing runs in the VM. Ask the orchestrator first, if
  needed, by finishing with a question.
- Do not commit or push.

## When done

Reply with three lines: the path of your review; how many of the 7 checks passed; the most important
problem, if any.

## Amendment 4 (2026-11-25, full run): check the full records, not the pilot

The batch is complete: 86 scripts, six sources (PaSh's own, naive, naive with sed file v2, Caruca PaSh
grammar, Caruca main grammar, a second copy of PaSh's own files as a timing control), three timed repeats.
Records are in `full_run/` (`results.jsonl.gz`, `regions.jsonl.gz`, `occurrences.jsonl.gz`,
`run_windows.jsonl`, `sleep_events.jsonl`), the counts in `full_run/numbers.md` (built by
`full_run/summarise.py`), the builder's account in `full_run/README.md`. Run the same seven checks as before
against these files, plus:

8. The two recorder fix-ups described in numbers.md (same-repeat bash reference; the seven node-less
   web-search rows left out and the redone rows used instead): confirm from the raw rows that the fix-up
   is applied exactly as described and nothing else was dropped. Report counts before and after.
9. The Mac sleeps in `sleep_events.jsonl`: confirm every timed row that overlaps a sleep window was either
   redone or excluded; list any that was not.
10. Recompute the headline numbers of numbers.md sections 1, 3, 5 and 6 independently from the raw rows
    (your own short script, not summarise.py) and report any cell that differs.
11. Spot-check five parallel-split claims by opening the PaSh logs in the VM (`~/t024/runs/<group>_<script>/`).

Write `orchestration/review_checker_full.md` (same shape as `review_checker.md`), then reply with pass/fail
per check in at most twelve lines. Do not change any record or any file under `full_run/`.

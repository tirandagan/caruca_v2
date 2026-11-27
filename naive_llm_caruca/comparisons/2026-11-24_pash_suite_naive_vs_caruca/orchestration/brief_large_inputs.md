# Brief: run the larger-input plan (2026-11-27)

You are the builder. Tiran said go. Read `orchestration/plan_large_inputs.md` (the plan; follow it exactly, its rules
are fixed), then `full_run_caruca_all/README.md` and `run_koala_caruca_all.py` (the last runner, which you will copy).
Work in `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`. Do not edit any existing record or the
report. Do not commit. Never touch `~/dev/stevens/caruca`. The Lima VM `pash` is running (the repo mount is read-only
inside it; write in `~/t024/...` and copy out, as the last run did).

## Steps

1. **Runner copy** `run_koala_large.py` from `run_koala_caruca_all.py`, writing to `~/t024/out_large/`. Add input
   scaling: for a script, build its scaled input under `~/t024/big/` (concatenate the small input k times; COVID:
   keep the header once, then k copies of the data rows), point the invocation's input argument at it, run all sources,
   then delete it. Sets: `bash`, `pash-own`, `naive-sed2` (the naive LLM's files with the second sed file; check the
   first run's set folder `~/t024/sets/naive-sed2` exists and holds every naive file, otherwise build it as the first
   run did), `caruca-pash-all`, `pash-own-copy`; optional `caruca-main-all` (see step 3). Keep bash first in every
   repeat; keep the stand-in (instrumented) pass once per script and set; outputs may be deleted after hashing, but
   keep each script's bash output hash so wrong outputs can be re-made later.
2. **Pilot (bash only)**: for every script in groups A and B (lists in the plan), time bash at k=10, and at k=30 if
   k=10 is under 3 s; record k per script in `full_run_large/scale.jsonl` (script, k, input bytes, bash seconds at each
   k). This is the only basis for k. Report the list and the projected total time to the orchestrator before step 3.
3. **Batch**: group A first, then group B. Include `caruca-main-all` only if the projected total with it stays under
   two hours. Watch Mac sleep and power (`pmset -g log`, `pmset -g batt`) as before; redo any timed run that overlaps a
   sleep or ran on battery. Copy records to `full_run_large/` after each group.
4. **Count**: adapt `full_run_caruca_all/summarise.py` to `full_run_large/summarise.py` (one session, five or six
   sets; add time against Caruca and against PaSh's own per script and per group, and group-level geometric means), and
   run `overhead_adjusted.py`'s model on the new records (copy it, change paths). Write `full_run_large/numbers.md` and
   `full_run_large/README.md` (what ran, k per script, faults, redos, and the plan's expectations side by side with the
   result: held or not, per expectation).
5. Report to the orchestrator in at most 8 lines after the pilot, after group A, and at the end.

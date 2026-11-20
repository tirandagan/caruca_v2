---
name: reference-pash-comparison-scorer
description: Where task 021's v1-vs-naive PaSh-annotation comparison lives, how its scorer and blind assessments work, and gotchas found building it (2026-11-11)
metadata:
  type: reference
---
Built 2026-11-11 for task 021. Folder: `naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/`
(Tiran: comparisons go in `naive_llm_caruca/comparisons/`). Start at its `report.md`.

- `score_pash.py all` runs on the **Mac** in about 30 s: it copies `pash-annotations` 0.2.4 from the uv cache
  (`~/.cache/uv/archive-v0/QbrdQstfYG3j7LuuIEFCo/pash_annotations`, override `PASH_ANNOTATIONS`) once per
  side into `SCORER_SCRATCH`, and calls each side's classes directly (catches exceptions PaSh hides). No VM needed
  for checks 1-2.
- Steps: `sides`, `lines`, `answers`, `iosets`, `tables`, `packets`, `packets-swap`, `unblind`.
- Blind assessment = fresh general-purpose subagents given only `rubric.md` + `packets/<cmd>/` (comments and
  docstrings stripped by `ast`); keys in `assessments/keys/`. A working-session self-assessment can't be blind
  (it wrote v1's generator). Leaks that remain: v1's per-situation code shape, `relpath_1` placeholders,
  `PATH_UNTRACED` in v1 tables.
- Result (rubric v1): reassessment under redrawn letters kept 111/114 rating fields. Rubric v1 gaps: says
  `assessment.md` (conflicts with given path), and has no "no answer" rule (assessors invented a type).
- Gotchas: `answers.jsonl.gz` differs between runs only in the `seconds` field; plain jsonl was 43 MB/69 MB, so
  records are gzipped (mtime 0).
**Real PaSh runs (task 022, run 2026-11-19): `pash_runs/` in the same folder; start at `observations.md`.**
- `run_pash.py` runs **inside the pash VM** from the read-only Mac mount, writes to `~/t022/out`; steps `build`,
  `controls`, `answers`, `select`, `run`, `causes`, `timing`, `heavy`, `scripts`. Copy results out with
  `limactl shell pash -- cat` or `limactl copy`, then `count_runs.py` on the Mac builds `numbers_pash.md` and
  `controls.md`. Line-by-line pass: about 6 minutes for 2,377 PaSh runs (about 0.15 s each on a 4 MB input).
- A side = private copy of the installed package with one command's three files, chosen with
  `pa.sh --local-annotations-dir`; `cp` and `split` must be added to the name table in the copy.
- State needs two signals (split steps in the log + stand-in count). Five states, incl. "split set up, workers
  got no input".
- Headline (2,377 runs, 382 lines): v1 139/139 allowed splits carried out, 0 wrong with PaSh-grammar files,
  **7 wrong `sort` lines with main-grammar files**; agent 423 of 655 allowed splits carried out, 19 empty
  `grep` outputs (folder with `-r`, `--color`), no unsafe split; PaSh's own 16 wrong; PaSh's compiler failed in
  329 runs. Whole scripts (46): all outputs right; split 35 (agent) / 35 (PaSh's own) / 35 (v1 main) / 27 (v1 PaSh
  grammar); v1 never splits `sort`. Heavy grep: 6.4x with v1's files, 6.1-6.3x agent/own.
- Not done: other worker counts; more than 8 commands; the suites' own inputs.
Related: [[feedback-qualitative-by-claude-in-session]], [[reference-pash-annotations-runtime]], [[feedback-pash-bugs-annotate-first]].

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
Related: [[feedback-qualitative-by-claude-in-session]], [[reference-pash-annotations-runtime]].

# Brief: answer Tiran's questions about the PaSh suite comparison and its interim report

You are a question-answering session for Tiran Dagan. He will type questions into this pane about the
experiment below and about the interim report draft. Answer from the records and documents, in plain
language (see `memory/feedback_plain_language.md` and `memory/feedback_be_brief.md`), with the file and
line a fact comes from. If something is not in the records, say so; do not guess. Do not run anything
in the Lima VM `pash` (a batch is timing runs there) and do not edit any file unless he asks.

## What the experiment is

PaSh is a tool that runs parts of a shell script in parallel. It decides what it may split from three
small *annotation files* per command. We run PaSh's published benchmark suite (in its current form,
Koala) with four sources of those files and compare each with plain bash: PaSh's own files; the naive
LLM's files (written by an off-the-shelf coding agent, 79 commands + `tr`, `xargs`, `awk` added
2026-11-24); Caruca's files for its 8 commands, in two variants (PaSh grammar, main grammar). Where a
source has no files for a command, PaSh's own are used. Measured per script: output same as bash, which
commands PaSh split and why not, share of regions parallelized, wall-clock time (3 timed repeats
planned; 1 so far for the quick groups). All decisions were Tiran's; they are listed in
`orchestration/metrics_spec.md` and `memory/project_pash_suite_comparison.md`.

Status on 2026-11-24 afternoon: one script (`spell`) measured, independently checked and written up;
the full batch (73 scripts) is running in the VM and will take about 10 hours; the interim report is
built from the one script.

## Where everything is (all under `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/`)

| What | File |
|---|---|
| The interim report (Markdown and PDF) | `report_draft.md`, `report_draft.pdf` |
| The pilot write-up by the builder | `README.md` |
| Every number in the report, written by the counting script | `numbers_pilot.md`, `numbers_pilot.json` |
| The records: per run, per part, per command use, direct answers of the files | `results.jsonl`, `regions.jsonl`, `occurrences.jsonl`, `answers.jsonl`, `commands.jsonl`, `controls.jsonl`, `manifest.json`, `run_windows.jsonl`, `timing_check_pilot.jsonl` |
| The independent check of the pilot | `orchestration/review_checker.md` |
| The suite map: 12 published sets → Koala groups, commands per script, who has files | `orchestration/coverage.md`, `coverage.jsonl` |
| Setup of the extra groups (downloads, installs, what runs) | `orchestration/inputs_setup.md` |
| The report design (tables, charts, what to leave out) | `orchestration/report_plan.md` |
| The metrics Tiran asked for and his decisions | `orchestration/metrics_spec.md` |
| The briefs each worker got | `orchestration/brief_*.md` |
| The runner, counting, chart and timing-check scripts | `run_koala.py`, `count_report.py`, `make_charts.py`, `timing_check.py`, `count_report.md` |
| Charts | `figures_pilot/`, `figures_interim/` (being drawn now) |

Background in `memory/`: `project_pash_suite_comparison.md`, `reference_pash_annotations_runtime.md`
(PaSh's behaviour, the OSDI'22 suite, Koala, the quoting fact), `feedback_pash_runs_test_our_annotations.md`,
`feedback_greenberg_report_style.md`, `project_key_people.md`, `project_requesty_llm_billing.md`.
Earlier related work: task 022 (`naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/pash_runs/`),
and the Caruca paper's own PaSh check (`ai_docs/refs/caruca_white_paper.md`, section 7.1, Table 1).

Start by reading `report_draft.md`, `README.md`, `review_checker.md`, `coverage.md` and `metrics_spec.md`,
then say in two lines that you are ready and what you have read.

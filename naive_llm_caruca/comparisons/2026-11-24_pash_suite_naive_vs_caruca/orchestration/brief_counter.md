# Brief: the counting script and the charts for the report

You are a worker. An orchestrating Claude session gave you this brief. Work only on it.

## What this is

The PaSh benchmark suite is being run right now in the Lima VM `pash` by another worker (the
"builder"); it takes hours. The report for Michael Greenberg will be built **only from numbers a
counting script writes**, never by hand. Your job is to write that script and the chart script now,
against the pilot's records, so they are ready and tested when the full records arrive.

Read, in this order, in `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`:
`orchestration/report_plan.md` (sections 2, 5.4 and 5.5 define exactly what to count and draw; section
6 is the report skeleton), `orchestration/metrics_spec.md`, `orchestration/brief_builder.md` (all
amendments), `README.md` (the pilot), the pilot's records (`results.jsonl`, `regions.jsonl`,
`commands.jsonl`, `answers.jsonl`, `controls.jsonl`, `invocations.jsonl`, `manifest.json`, and
`occurrences.jsonl` / `sets.json` once the builder has written them; the shapes are described in the
plan), `orchestration/coverage.jsonl`, and the house-style memory files `memory/feedback_plain_language.md`,
`memory/feedback_greenberg_report_style.md`.

## Produce, in this folder

1. `count_report.py`: count-only (no judgement, no prose beyond labels). Reads the records, writes
   `numbers.md` (every number for tables 1–4 and charts A–C, plus the appendix tables A1, A3, A4, A5)
   and `numbers.json` (the same, for the chart script). It must do the pairing in plan section 5.4
   (parts by `id` + region text hash; uses by `id` + hash + position; reasons split into shared /
   only-this-source; agreement with PaSh's own files counted as the plan says; repeated launches pooled).
   Every rate is written "a of b". Use the display-name map (`sets.json`) for all labels. It must run
   with `python3 -I` and only the standard library. Make it fail loudly, naming the field, when a record
   lacks something it needs.
2. `make_charts.py`: reads `numbers.json`, writes `figures/chartA.png`, `chartB.png`, `chartC.png`
   as the plan specifies (portrait width 6.5 in, ≥ 8 pt text, 300 dpi, one colour per source, PaSh's
   own files always the reference). Load the `dataviz` skill before drawing. Matplotlib is fine.
3. `count_report.md`: one page on how to run both scripts, what each number means, and the checks the
   script performs on itself (e.g. the distinct-part count is the same for every source).

Test both on the pilot's records (one script: most tables will have one row). Where a record the plan
names does not exist yet (`occurrences.jsonl`), write the code against the plan's field list and mark
the test as pending in `count_report.md`.

## Rules

- Do not run anything in the Lima VM `pash`; the builder is timing runs there.
- Do not edit the builder's records or scripts; read them only.
- Plain language in `count_report.md` and in every label; no bare field names in labels.
- Do not commit or push.

## When done

Reply with: the two script paths; which tables and charts were produced from the pilot; what is
pending on the full records.

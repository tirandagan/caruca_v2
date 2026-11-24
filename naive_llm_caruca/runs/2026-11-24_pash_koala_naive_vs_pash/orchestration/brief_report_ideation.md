# Brief: plan how the PaSh suite experiment is reported to Michael Greenberg

You are an ideation and planning agent. You run nothing and change nothing except the one file you
produce. Think hard: other agents will build what you plan, and the orchestrator will change their
work based on what you say.

## The reader

Michael Greenberg: principal investigator of Caruca, co-author of the Caruca paper, Tiran's PhD advisor.
He does **not** like long, AI-sounding reports: too confusing, too many details. He likes very simple,
human-like reporting: *what did we observe*, with clean, clear tables and charts. When shown a
comparison he asks whether and how the results differ, so lead with the observation. Because he
co-authored the original system, write about the naive LLM's and Caruca's results as what each adds,
never as fixing the other's flaws; technical facts are still stated plainly.

## The experiment you are planning the report for

Read, in this order, under `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/orchestration/`:
`brief_builder.md` (including Amendment 1 at the end), `metrics_spec.md` (Tiran's metrics and his
four decisions), `brief_inventory.md`, `brief_checker.md`. In short: PaSh's published benchmark suite
(its newer form, Koala) is run under plain bash and under PaSh with four annotation sources: PaSh's
own files; the naive LLM's files for the 79 commands it covers (PaSh's own elsewhere); Caruca's files
for its 8 commands, in two variants (PaSh's own elsewhere). Measured: output correctness, which
commands PaSh split and why not, the share of regions parallelized, wall-clock time with 3 repeats.

## House style, from memory (read these files under `memory/`)

`feedback_plain_language.md`, `feedback_be_brief.md`, `feedback_addendum_style.md`,
`feedback_handout_workflow.md`, `feedback_v1_v2_framing.md`, `feedback_qualitative_by_claude_in_session.md`,
`project_key_people.md`, `project_pash_suite_comparison.md`, `feedback_pash_runs_test_our_annotations.md`.

## Earlier reports, and how they were received

- `naive_llm_caruca/white_paper_addendum_naive_llm.md`: version 0.6 is the style Tiran settled on after
  rejecting earlier versions as too complex (per insight: what we found / what it shows / how Caruca
  does it / what the agent adds; no file names or command lines in the body; sources at the end).
- `naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/pash_runs/observations.md` and
  `results_page.html` (a results page published for this kind of run), and `../report.md`: the most
  recent PaSh comparison write-ups. Judge what in them Michael would find too much.
- `naive_llm_caruca/latest_findings.md`: the running findings log.
- The paper's own reporting of its PaSh check: `ai_docs/refs/caruca_white_paper.md`, section 7.1 and
  its Table 1. The new report should let Michael put our numbers next to those.

## Produce one file: `orchestration/report_plan.md`

1. **Shape.** The report's sections in order, one line each on what the reader learns there, and a
   target length. Short.
2. **Every table and chart, specified.** For each: title; rows and columns (or chart type, axes, series);
   the one sentence it exists to support; the exact records and fields it needs (map them to
   `results.jsonl`, `regions.jsonl`, `commands.jsonl`, `coverage.jsonl` in the briefs); and what it
   should look like at a glance. Prefer few, dense, clean tables. Charts only where a picture says it
   faster than a table (e.g. time per script under each source; parallelized-region share per source;
   which commands each source covers).
3. **The headline.** How to present the three-way comparison (naive LLM vs Caruca vs PaSh's own) and
   Tiran's case split (commands only PaSh covers vs commands we cover) in plain words, with every rate
   given with its denominator.
4. **What to leave out** of the body, and what goes to an appendix or linked records.
5. **Changes needed in the running agents' records or runs** so the report can be built: a concrete
   list for the orchestrator (fields to add, controls to run, repeats, naming), each with why. This is
   the most important part; put it first in your reply.
6. **A skeleton** of the report with placeholder tables and draft wording in the style described.
7. **Delivery.** Markdown to PDF (the handout workflow) and/or a published results page: recommend.

Rules for the plan and the report it describes: plain language; one word, one meaning; define every
rate with its denominator; no bare option names, field names or file names in the report body; explain
every term the first time. Do not commit or push.

## When done

Reply with: the path of the plan; the three most important changes for the running agents; one open
question for Tiran, if any.

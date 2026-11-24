---
name: project-pash-suite-comparison
description: 2026-11-24 goal set by Tiran: run PaSh's whole published benchmark suite (Koala stand-ins) three ways, naive LLM's files vs Caruca's vs PaSh's own, with PaSh's own files filling in for commands a set lacks; pilot = one script, then all
metadata:
  type: project
---
**Goal (Tiran, 2026-11-24).** Run the benchmark scripts PaSh itself ships ("not one-liners, 7 or 13 of
them": the OSDI'22 paper's Table 1 rows 2–13, which the Caruca paper names as its PaSh check) under PaSh
with three annotation sources, and compare: the **naive LLM's** PaSh files, **Caruca's** (v1's) PaSh files,
and **PaSh's own** ("organic") annotations. For commands a source has no files for, PaSh's own files are
used, so the comparison is "ours where we have them, PaSh's elsewhere". Start with one script; the goal is
all of them. Koala (`kbensh/koala`) stands in for the published suite because its inputs are gone.

**Setup.** Work folder `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/` (briefs in
`orchestration/`). Sets per script: `bash`, `pash-own`, `naive` (first Fig. 7 run per command, 79
commands), `caruca-pash` and `caruca-main` (v1's 8 commands `cat cp cut grep rm sort split wc`, paths from
task 021's `sides.jsonl`). Pilot script: Koala `oneliners/scripts/spell.sh` (naive covers 6 of its 7
commands, Caruca 2: `cat`, `sort`). Run by Claude Code worker panes under Herdr (Opus, medium effort):
`pash-builder`, `pash-inventory` (maps the 12 published sets to Koala groups and command coverage), then an
independent `pash-checker`. Orchestrator = the main session.

**Metrics (Tiran's note + answers, 2026-11-24; spec in `orchestration/metrics_spec.md`):** per command
occurrence, where its annotation came from (ours / PaSh's own / none: his "case 1 vs case 2"); per region
(PaSh's compile requests, plus distinct-region counts), the outcome (parallelized, refused by annotation,
missing annotation, annotation raised, unsupported construct, PaSh crash, other); **rate = parallelized /
all regions, and every unparallelized region counts against the source whatever the cause** (causes
listed alongside); wall-clock with **3 timed repeats** (median, min–max); **all of a source's commands
swapped in at once**, no one-command-at-a-time runs, and the report must say so; naive files = **first
run per command**. Scripts with no "ours" command are the noise control for that set.

**Inventory (pash-inventory worker, 2026-11-24, read from the VM's Koala `ccf25a57`; details in
`orchestration/coverage.md` + `coverage.jsonl`).** The 12 published sets map to 10 Koala groups
(Classics→`oneliners`, Unix50→`unixfun`, COVID-mts→`covid`, NLP→`nlp`, AvgTemp→`weather`,
WebIndex→`web-search`, MediaConv+FileEnc→`file-mod`, ProgInf+AurPkg→`pkg`, LogAnalysis→`analytics`,
Genomics→`bio`), which run 92 scripts; 82 have a published original, mostly near-identical. The naive
LLM fully covers only 17 of 92 because it has **no `tr` (54 scripts), `xargs` (24), `awk` (18)**: not in
the 79 Fig. 7 commands. Naive + PaSh's own together cover 52 of 92. **The VM is aarch64:** Koala's
installers fetch Intel-only Go (analytics `zannotate`), `STAR`, `seqkit` and `liftOver` (bio). bio's
TERA-Seq scripts can't run there (fetch.sh pulls ~15 GB at every non-min size, `STAR` index ~33 GB RAM);
`bio.sh` at min only. `pkg` has nothing any source lets PaSh split. Command lists came from parsing
with PaSh's bundled libdash + shasta (`~/pash/python_pkgs/bin/python3`), then hand checks.

**Why Koala groups, not PaSh's `evaluation/benchmarks`:** those scripts exist in the VM but their
inputs can't be fetched ([[reference-pash-annotations-runtime]]).
Related: [[feedback-pash-runs-test-our-annotations]], [[reference-pash-comparison-scorer]].

**Progress 2026-11-24 (afternoon).** Pilot `spell.sh` done and accepted (see
[[reference-pash-annotations-runtime]] for the numbers). Report design by an Opus-xhigh agent:
`orchestration/report_plan.md` (3-page body: 4 tables, 3 charts; section 5 = record changes, given to the
builder as Amendment 2; section 5.4 = a count-only `count_report.py` → `numbers.md`, every report number
copied from it; delivery = Markdown → PDF, no results page). Tiran's decisions: naive LLM run on
`tr`/`xargs`/`awk` (worker `naive-runs`, new tab); scope = six ready groups + `analytics` (no port-scan)
+ `file-mod`, `bio.sh` at min, `pkg` once at min (worker `pash-inventory` setting up inputs). Checker
(`pash-checker`) verifying the pilot. Full-suite batch waits for the three naive files.

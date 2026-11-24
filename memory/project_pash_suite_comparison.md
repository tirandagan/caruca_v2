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

**Inputs set up 2026-11-24 (pash-inventory; `orchestration/inputs_setup.md`).** analytics small
(nginx, pcaps, ray-tracing), file-mod small (all 5), bio.sh min are installed and fetched in the VM and
run under bash. pkg skipped (installer needs proget.makedeb.org + npm; pacaur fetches keys/sources at
run time). Koala-hash mismatches, each stable across two runs, so use VM bash output as the reference:
pcaps 35/69 (tcpdump 4.99.4 vs Koala's Debian 12; untested), img_convert 1/508, thumbnail 460/508,
to_mp3 40/40. to_mp3's check also can't work as shipped: validate.sh uses `ffmpeg` from PATH, and only
execute.sh adds `/usr/local/legacy-bin`. minimap2 fails to build on ARM (Koala uses `-msse` flags);
bio.sh doesn't need it. Free disk afterwards: 9.3 GB.

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

**Report tooling ready (counter worker, 2026-11-24, in the run folder):** `count_report.py` (count-only,
standard library, writes `numbers.md` + `numbers.json`; fails loudly on missing fields or a bad timing
window), `make_charts.py` (`figures/chart{A,B,C}.png`, dataviz-skill palette), `timing_check.py` (Mac side:
reads `run_windows.jsonl` + `pmset -g log`, writes `timing_check.jsonl` per window with sleep events, power
source, VM clock offset; run it soon after the batch, the Mac keeps only a few days of power log; a snapshot
is in `orchestration/pmset_log_snapshot_*.txt`), `count_report.md` (how to run). Pilot outputs carry a
`_pilot` suffix. **Full batch launched 12:05 on 2026-11-24** (73 scripts × bash/pash-own/pash-own-copy/
naive/caruca-pash/caruca-main × 3 timed repeats, plus instrumented passes; ~9 h). Then: fresh checker →
count → charts → `report.md` from the plan's skeleton → PDF.

**Vetted pilot differences (worker, 2026-11-24, `orchestration/judgment_errors.md`):** naive `sed` =
instrument gap (repaired, re-run, PaSh rerun pending); naive `col` = safe refusal, **naive file right in
general, PaSh's own `col` unsafe** (`\v` at a piece boundary changes `col -bx` output; safe in spell.sh only
because `sed` strips it first) — the report's "col: wrong judgment" needs correcting; `cat` (naive + Caruca)
= correct but useless split (task 022: 0.27 s split vs 0.10 s whole on 64 MB; inside spell.sh not measurable,
one control run 0.877 vs 0.89 s); Caruca `sort` = method limit (only end-to-end joins). PaSh's own `sed` also
wrongly splits `N;s/\n/ /`. No source's file is wrong about a command on spell.sh.

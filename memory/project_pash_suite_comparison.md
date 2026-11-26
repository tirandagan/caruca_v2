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

**First full-run numbers, the 46 quick scripts (oneliners 12 + unixfun 34), 2026-11-24 15:00, one timed
repeat, `full_run/numbers.md` (builder's `summarise.py`):** every PaSh run's output = bash = Koala's hash
for all five sources (46 of 46). Scripts with any part parallelized: PaSh's own 37 of 46, naive 39, Caruca
PaSh-grammar 29, Caruca main-grammar 37, PaSh's own second copy 37. Distinct parts (51): naive 39 (gained 2,
lost 0 vs PaSh's own), Caruca main = PaSh's own exactly (37, 0/0), Caruca PaSh-grammar 29 (lost 8; PaSh
compiler crashes 11 vs 3: the `sort -rn` read as a file). Naive's gains: `cat` split in 39 scripts, `awk`
2; loss: `col` 1. Method check: in 747 of 748 uses PaSh split exactly when the files (asked with PaSh's
words) allowed a split PaSh can carry out. One naive file raised: `wc` (AssertionError).

**Checker's review of the full run (86 scripts), 2026-11-25, `orchestration/review_checker_full.md`:** 10 of
11 checks pass. Every number in `numbers.md` sections 1, 3, 5, 6 and the per-script table was recomputed from
the raw rows with independent code: 0 cells differ. PaSh's logs agree with the recorded splits in 396 of 396
instrumented runs. The README fails on these points:
- **"same as bash" covers printed output only.** Of 588 timed rows from the 32 scripts that write files, 211
  checked the files as the same as bash's, 352 were not checked and 25 differ. **web-search's written files
  differ between two plain-bash runs** (redo-r1 vs redo-r3 file hashes), so file comparison cannot judge it.
- The power statement misses short battery stretches in 13:10–17:31 and at 10:15 on 11-25. There was also an
  unlogged 61 s lid-closed dark wake at 10:43 on 11-25 (on mains power, caffeinate held, not a sleep).
- The naive LLM's 2 gained parts (unixfun/12, /16) are parts where PaSh's own files crash PaSh's compiler.
- `numbers.md`'s "sed2 run only on scripts that use sed" is false: 27 of 52 have no sed.

Facts about where things are and how they were built:
- Full PaSh logs are in the VM at `~/t024/out/logs/`, not `~/t024/runs/`.
- The runner rebuilds the set folders at each start. The first 46 scripts' main runs (13:10–13:50) used a build
  with no record; the current build dates from 13:54.
- The checker's scripts are in the VM at `~/t024-check/full/`.

## Report refresh to the full run (2026-11-26, worker under `orchestration/brief_report_refresh.md`)

Established by counting the records in `full_run/`:
- **The naive LLM's second sed file DID recover the sed splits**: it splits `sed` in 5 of the 5 scripts where the
  first file lost it (covid/1-4, oneliners/spell); against PaSh's own it gains and loses nothing on `sed`. The
  brief's "did not recover (0 gained of 5 lost)" was wrong; the report follows the records.
- Independent recount (`count_report.py` + new `prep_full_records.py`, output `numbers_full.md/.json`): 0 headline
  cells differ from `full_run/numbers.md` sections 1, 3, 5, 6.
- Written-file check after both fix-ups: 211 same / 347 not checked / 18 different, of 576 timed rows (32 scripts).
  The checker's 211/352/25 of 588 counts before fix-up 2 (12 web-search rows: 7 different, 5 not checked).
- The naive LLM's 2 gained parts (unixfun/12, /16) are both PaSh-own compiler crashes; all 29 of Caruca PaSh
  grammar's filled-in differences sit in parts its own files broke (23 crash, 6 "other").
- Full-run figures: `make_figures_interim.py --records full_run --numbers numbers_full.json --out figures_full`.

## Full run complete (2026-11-25 12:53; report Draft 1.0 built 2026-11-26)

Established by running (records in `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/full_run/`,
checked independently in `orchestration/review_checker_full.md`, 10 of 11 checks pass):

- 86 Koala scripts, six annotation sets (PaSh's own; naive; naive with sed file v2 on the 52 scripts that
  were rerun; Caruca PaSh grammar; Caruca main grammar; a second copy of PaSh's own files as timing control),
  three timed repeats, medians. Printed output identical to bash in 86 of 86 under every source; Koala's
  stored answer matched in 46 of 46. Written files were compared in only 211 of 576 timed runs (347 no
  reference, 18 differ: web-search 12, whose files differ even between two bash runs, bio 6).
- Scripts with a parallel part: PaSh own 41, naive 43, Caruca main 41, Caruca PaSh grammar 29 (of 86).
  Naive gained cat 43, awk 6, tr 3, cut 2, sort 2, grep 1 scripts; lost sed 5, col 1. Caruca main lost sort 17;
  Caruca PaSh grammar lost sort 17, cut 9, tr 5, sed 5, grep 4 and gained cat 29. The sed v2 file did not
  recover the sed splits. The naive LLM's two gained parts are parts where PaSh's own files crash PaSh's compiler.
- Time: PaSh slower than bash under every source on small inputs (0.37x to 0.43x geometric mean). Naive files
  1.15 times PaSh's own (34 of 86 scripts slower by >10%); noise band of the identical second copy 0.83 to 1.13.
- Instrument faults, records untouched, fixed in the counting: repeats recorder compared sources run before
  bash (rotated order) against a missing reference (482 rows); web-search's timed runs lacked `node` (7 rows
  redone); Mac slept four times (two NLP scripts rerun, web-search repeat 3 redone on mains).
- Report: `report/report.pdf` Draft 1.0, 12 pages, built from `numbers_full.json` (`count_report.py --tag full`
  on records expanded by `prep_full_records.py`), figures in `figures_full/`. Not committed as of the build.
- Parallel panes cannot speed up the timed repeats: PaSh uses all 8 VM cores per script, so concurrent scripts
  distort each other's times (Tiran asked 2026-11-25; answer: wait or cut repeats, he chose to wait).
- **PaSh compiler crashes in the suite (read from PaSh logs 2026-11-26):** two exceptions only. `NameError: name 'Arg'
  is not defined` (PaSh's Jan 2026 refactor, issue #794) in one part of `oneliners/bi-grams` under every source;
  and an `AssertionError` at `src/pash/compiler/ir.py` ~line 596 (`assert not other_in is None`, when PaSh pipes one
  command into the next and the next command's annotation says it reads a file named by one of its own words,
  not stdin): `tail -n 1`, `awk` with PaSh's own files (unixfun/12, 16, covid/5); `fmt -w1`, `sed` with the naive
  files (unixfun/34, 36, covid/5); `sort -r/-n/-rn` with Caruca's PaSh-grammar files (10 more parts than PaSh's
  own). Parts crashed per source: PaSh own 4, naive 4, Caruca PaSh grammar 14, Caruca main 4, of 177. PaSh falls
  back to bash, so output stays right.
- **Report Draft 1.0 final shape (2026-11-26):** 23 pages; body 6 pages (Table 1 incl. crash row, Table 2, Fig 1,
  causes, "When PaSh itself failed", Fig 2, Table 3, limits); addendum A1 script, A2 words, A3 setup + Fig 3,
  A4 reasons per part, A5 per-script parts/crashes/times with min–max, A6 every differing use (135), A7 all 86
  scripts, A8 records. Tiran's rule: the metrics he specified (crashes with reasons, per-script rates and times)
  must appear in the PDF's addendum, not only in numbers.md (he flagged their absence 2026-11-26).

**Report round 3 (2026-11-26, brief `orchestration/brief_report_round3.md`): Draft 1.1, 10 pages (was 23).**
Body 4½ pp, addendum A1–A8 (A5 = one-page chart, A6/A7 one page). Facts established from the records that day:
- The naive LLM's 31 parts in Table A4's "other, not classified / only here" are **30 single-`mkdir` parts and 1
  single-`mogrify` part**: PaSh's own has no file for them ("missing annotation"); the naive file declares a
  non-stream output and PaSh logs "Command X has outputs other than streaming". Correct answer, nothing lost.
  (Read from `full_run/regions.jsonl.gz`, `reason` field.)
- **Scripts with a split command other than `cat`**: PaSh's own 41, naive 43, Caruca small grammar 27, full
  grammar 39 of 86; second sed file 14 of 52 — so the naive LLM's +2 gain does **not** come from `cat`.
- **Time ÷ bash time** (geometric mean = 1 / `speedup_gmean`): 2.35, 2.70, 2.47, 2.49; second sed file 1.96.
- Excalidraw renderer cannot use Lexend Deca (built-in Excalidraw fonts only); Figure 3 is now drawn by
  `figures_interim/make_figures_interim.py` (`full_setup`), which also draws A5's chart (`full_a5`).
- **Report Draft 1.1 (2026-11-26, after /impeccable critique 22/36):** 10 pages. Body 4 pages: question + one-line
  finding, "How it was run" with Figure 1 (setup) before Table 1, Table 1 with crash row, "without cat" counts and
  time as "n × bash (lower is better)"; Figure 2 splits by command with PaSh's own counts as grey labels; five vetted
  causes; three-sentence crash note; Figure 3 time with per-source "slower than bash: n of 86"; Table 3 paper
  comparison; threats to validity. Addendum: A1 script, A2 words, A3 setup, A4 reasons per part (merged table; the
  naive LLM's 31 "other" parts = mkdir in 30 scripts and mogrify in 1, whose naive files say they write something
  other than a stream, so PaSh runs them as bash), A5 scripts (one page, run-in lists), A6 by command (old Table 2 +
  command-line counts), A7 every-script chart (Figure A7: time ÷ bash, parts split, hollow = crash) + crash list, A8
  records table. Rules learned: figures numbered in reading order; the Excalidraw renderer cannot use Lexend Deca, so
  Figure 1 is drawn by the figure script; Chromium multicol blocks must be `break-inside: avoid` or they straddle pages.

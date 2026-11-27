---
name: project-pash-suite-comparison
description: 2026-11-24 goal set by Tiran: run PaSh's whole published benchmark suite (Koala stand-ins) three ways, naive LLM's files vs Caruca's vs PaSh's own, with PaSh's own files filling in for commands a set lacks; pilot = one script, then all
metadata:
  type: project
---
**LARGER-INPUT RUN DONE 2026-11-27 (`full_run_large/`, runner `run_koala_large.py`, plan
`orchestration/plan_large_inputs.md`).** 43 scripts (group A 29, B 14), inputs = small input x k (k=10/30 from a
bash-only pilot; COVID k=1 because its own input is already 3.6 GB, VM disk 6.6 GB free), sets bash / pash-own /
naive-sed2 / caruca-pash-all / pash-own-copy (caruca-main-all left out: projected 127 min > 2 h). Observed: naive
right 43/43, Caruca wrong 10 (its 9 + uniq-ips, which was right at small size: split `uniq` errors are
data-dependent); time vs PaSh's own: naive 1.33 (A) / 1.57 (B), Caruca 1.52 / 1.23; naive faster than PaSh's own
only on Unix50 12, 14, 16; vs Caruca naive 0.88 (A) / 1.28 (B). Every script where naive > 1.4x Caruca has a naive
`tr` split whose file offers only CONSEC_CHUNKS (PaSh's own/Caruca's also offer round robin) - association, not
tested. Gotchas: a `limactl shell` that starts a nohup job stays open until the job ends (use setsid + </dev/null);
regions/occurrences files are flushed only when each script finishes.

**Goal (Tiran, 2026-11-24).** Run the benchmark scripts PaSh itself ships ("not one-liners, 7 or 13 of
them": the OSDI'22 paper's Table 1 rows 2–13, which the Caruca paper names as its PaSh check) under PaSh
with three annotation sources, and compare: the **naive LLM's** PaSh files, **Caruca's** (v1's) PaSh files,
and **PaSh's own** ("organic") annotations. For commands a source has no files for, PaSh's own files are
used, so the comparison is "ours where we have them, PaSh's elsewhere". Start with one script; the goal is
all of them. Koala (`kbensh/koala`) stands in for the published suite because its inputs are gone.

**Setup.** Work folder `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/` (briefs in
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

Established by running (records in `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/full_run/`,
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
- **Framing rule (Tiran, 2026-11-26):** the one thing the report must show is how the naive LLM fared against
  Caruca (correctness, reach, splits, crashes it caused, files that failed, wrong decisions, wall-clock), with
  PaSh's own files as the yardstick for both. Draft 1.1 was retitled "How a naive LLM's annotation files fare
  against Caruca's on PaSh's benchmark suite", opens with that question and a finding line in those terms, and
  section 1 is a head-to-head Table 2 (naive | Caruca full | Caruca small): 82 vs 8 commands with own files;
  523 vs 304 of 609 uses decided by own files; output equal; splits 43/41/29 of 86; compiler stops beyond PaSh's
  own 2/0/10; files that fail to load 2/0/0; time vs PaSh's own 1.15 (1.07 with fixed sed)/1.06/1.05, i.e. naive
  8 % slower than Caruca, 1 % once sed is fixed. Every figure caption must say why its items were chosen (Figure 2's
  eight commands = every command that differed under any source).
- **Per-command test vs PaSh's own (2026-11-26, per_command.py):** naive 82 files, PaSh's own 30, overlap 20; 18 of
  the 20 met a part; on those 484 uses PaSh split 126 with its own files, 192 with the naive files (mostly `cat`;
  also more tr/sort/awk/cut; fewer sed (quoting gap) and col (safer refusal)). 5 naive-only commands met a part
  (mkdir 31, join 3, fmt 2, rev 2, mogrify 1), none split; 53 naive files never called. **Time correction:** naive is
  9 % slower than Caruca full over 86 scripts; ~40 % of the log-gap from splitting a plain `cat` (25 cat-only scripts,
  1.21×), ~26 % from COVID 1-4 (sed whole); the fixed sed file must be compared on its 52 scripts (8 % -> 3 %), not
  against the 86-script mean. An earlier draft wrongly said "almost all in COVID" and "1 % with the fixed sed".
- **Why Caruca has only 8 commands in this run (checked 2026-11-26):** current PaSh reads only Python annotation
  classes; Caruca's 54 PaSh annotations in `caruca/save/*.json` (2024, old JSON) cannot be loaded. The task-020
  converter (`run_pash_py.sh`, branch `pash-python-annotations`, `caruca/save_pash_py/`) was run for 8 commands only
  (cat cp cut grep rm sort split wc, small grammar) and 3 with the full grammar (cut rm sort); tracing the rest was
  deferred (task 022: "Default: the eight v1 has finished"). Caruca's repo has 54 small grammars
  (`pash_syntax_specs/`) and ~120 full grammars (`syntax_specs/`). The paper's PaSh figure is 52 of 52 commands
  (Tab. 1; 88 ground truths incl. 52 PaSh). **The report's "Caruca's full grammar" set is mixed:** full-grammar files
  for cut, rm, sort only; small-grammar files for cat, cp, grep, split, wc (manifest.json source_per_command).
  Tiran (2026-11-26) questioned the 8 ("there were 72 in the white paper"); 72 does not appear in the paper.
- **Caruca conversion, 2026-11-26:** 45 more small grammars converted (53 of 54 now; `gzip` grammar broken:
  defines gunzip_syntax_spec), 18 more full grammars at max-count 2 (21 total). Full-grammar `grep` (154K runs) and
  `ls` were OOM-killed at 8 GB VM memory (tracer holds all traces in RAM, 7.7 GB at kill); grep retried alone at 16 GB.
  Timeouts (2 s limit) inherent for rev/pandoc/grep (rev retraced idle: same 67 of 1,364, identical files). Record:
  comparisons/2026-11-24_pash_suite_naive_vs_caruca/caruca_conversion/README.md. caruca VM now 16 GB (was 8).
- **Converter fault found and repaired (2026-11-26 14:30):** our task-020 converter (`annotator/pash_py.py`
  `_comment()`, branch pash-python-annotations, uncommitted edit) copied a traced example with a literal newline/tab
  into a comment, so 3 of 106 new files (paste small+full, awk full) raised TabError and made PaSh's compiler server
  die at start-up. Instrument fault (ours, not Caruca's method): escaped \n \t \r, regenerated the 3 files from
  existing traces (logic lines identical, 14 converter tests pass). Rerun sets: caruca-pash-all 53 commands
  (all small grammars but gzip), caruca-main-all full grammar for 22 commands, small for the rest.
- **Rerun in progress (started ~15:15 2026-11-26, records in full_run_caruca_all/, runner copy run_koala_caruca_all.py).**
  Not yet verified, reported by the builder at 54 of 86 scripts: with Caruca's expanded files PaSh's printed output is
  wrong in 9 (caruca-pash-all) and 10 (caruca-main-all) of 54 scripts, identical across repeats; causes named: `sed`
  with a line address (1d, 4d, 100q) split per chunk, `uniq` split with plain concatenation, unixfun/23 undiagnosed.
  Consistent with v1's class-combining rule (keeps the most parallelizable label). Verify from the records before use.
- **Pushed 2026-11-26 (Tiran's request):** binpash/caruca branch pash-python-annotations commit be33389a5 (522 files):
  53 PaSh-grammar + 22 main-grammar conversions, save_pash_py/README.md table of all 75, and the `_comment()` escape fix.
- **Caruca expanded rerun DONE 2026-11-27 04:37** (builder session; records in
  `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/full_run_caruca_all/`, start at its README):
  86/86 scripts, mains power, no sleep. Printed output wrong in 9/86 (caruca-pash-all) and 10/86 (caruca-main-all),
  11 distinct; PaSh's own 86/86. unixfun/23 diagnosed from the records: Caruca allows splitting `tr -d '\n'`
  (PaSh's own allows only an unimplemented split, which ends the parallel chain), so 8 `tr` copies feed 8
  `cut -c 1-4` copies directly, each printing its own first 4 chars. Parallel distinct parts 41 / 29 / 40 of 177;
  time vs pash-own 1.09 / 1.10 (noise copy 1.00, range 0.83-1.46). Same-session pash-own reproduces the first run
  (41 parallel parts, 126 split uses, 4 compiler stops). Counting: `full_run_caruca_all/summarise.py`,
  `../per_command_caruca.py <set>`.
- **Gotchas found in that rerun:** (1) PaSh's AnnotationGeneration exec-imports every name-table generator at
  start-up and catches only ModuleNotFoundError, so ONE file with a SyntaxError stops PaSh's compiler server and no
  script runs (rc 1); always compile-check swapped-in files. (2) `limactl shell pash -- bash -lc 'pgrep -f "X"'` /
  `pkill -f "X"` match the wrapping shell's own command line (pgrep loops never end; pkill kills the session) —
  kill by PID or anchor the pattern (`^python3 ...`). (3) run_koala.py's `run` repeats the instrumented pass
  `--repeats` times; the first run used one instrumented pass (fixed in run_koala_caruca_all.py only).
- **Caruca rerun finished 2026-11-27 04:37 (full_run_caruca_all/, builder-counted, verification pending):** output
  same as bash: PaSh's own 86/86, Caruca small (53 cmds) 77/86, Caruca full where traced (22) 76/86; 11 distinct
  scripts wrong, same in every repeat; causes per builder: sed with a line address split (8), uniq split (2),
  tr -d '\n' split before cut -c (unixfun/23). Scripts with a part split: own 41, Caruca small 29, full 40; parts
  41/29/40 of 177, Caruca gains none. Time vs own, same session: 1.09 / 1.10 (second copy 1.00). Rerun's pash-own
  reproduced the first run exactly (41 parts, 126 uses). Report Draft 2.0 being written (report-v2-opus pane).
- **Verified 2026-11-27 (independent check, full_run_caruca_all/wrong_outputs_verified.md):** all 11 wrong-output
  scripts confirmed (19 script-set pairs, identical wrong output in all 4 runs). Causes: 8 sed scripts (1d..5d, 100q):
  sed grammar `choices=("s/a/b/g")` is a string so Caruca traced one-char scripts; `sed b` stateless + `sed g` non-pure
  merged under the same (flags, n) with max -> stateless. 1 tr -d script: stateless in 1 of 3 split-capable inputs
  (MATH, a no-op), non-pure in 2, max won. 2 uniq scripts: all 3 split inputs agreed stateless because none has a
  repeated line at the split point. So 9 of 11 = Caruca's max-wins combining rule; 2 of 11 = test-input coverage.
  Note: Parallelizability generator comments always show `# v1: stateless` (filtered before _comment).

**Report Draft 2.0 (2026-11-27), Caruca at full reach.** Caruca's columns come from the second session
(`full_run_caruca_all/`, counted into `numbers_caruca_all.md/.json` via `prep_full_records.py` + `count_report.py
--sleep-events <empty>`); times are ratios to PaSh's own of the same session. Verified 2026-11-27 by per-use
comparison: PaSh's own split the identical 126 of 609 uses in both sessions. Headlines: output naive 86/86, Caruca
small 77, full 76; scripts split 43 / 29 / 40; parts lost: small 12 (10 compiler stops on sort options + 2 where its
sort file gave no answer), full 1 (spell, its tr file gave no answer); compiler stops 4 / 11 / 3 (Caruca full's 2 own
= fmt -w1 in unixfun/34, 36, same as the naive LLM's); time vs own 1.15 / 1.09 / 1.10. Caruca's tr files say
"no split" only for tr -c (33 uses); its 24 "refused" parts = 23 single echo + 1 comm. **unixfun/23 explained (2026-11-27, orchestrator's log check + both tr files re-read):** both
sources allow `tr -d '\n'` to split, but the naive LLM's tr file offers only consecutive chunks when newlines may be
touched (round robin regroups by line), so PaSh rejoined before `cut` and output stayed right; Caruca's converted
files offer round robin for every splittable case, so PaSh ran tr and cut per 1 MB block (155 bytes instead of 5).
- **unixfun/23 explained (checked 2026-11-27 in PaSh logs + both tr files):** naive and Caruca both allow `tr -d '\n'`
  and `cut -c 1-4` to split, but the naive LLM's tr file offers only consecutive chunks (comment: round robin regroups by
  line, unsafe when newlines are deleted/created), so PaSh rejoined before cut -> right output; Caruca's converter emits
  cc+rr for every stateless case, so PaSh r_wrap-ed all 7 commands per 1 MB block -> cut printed 4 chars per block.
  A careful judgment by the naive LLM, not luck.
- **Report Draft 2.0 built 2026-11-27 ~05:15 (14 pages):** Caruca at full reach (53 small / 22 full grammars, rerun
  session), new section 2 "Where Caruca's files give wrong output" (Table 3, 11 scripts), Table 4 command by command for
  all three sources vs PaSh's own, two-session timing (ratios to same-session PaSh's own), footnote 1 restored on page 1.
  Headline: naive 86/86 correct, Caruca 77 and 76 of 86; splits naive 43, Caruca full 40, small 29 scripts; time vs
  own 1.15 (naive), 1.09/1.10 (Caruca). Not committed.

**2026-11-27, Draft 2.2 (15 pages):** the naive LLM's 2 compiler stops beyond PaSh's own (Unix50 34 and 36) are both
`fmt -w1` — PaSh's log for `unixfun_36__naive__instrumented` shows `filedes name: -w1` before the `pipe_append`
assertion, and the second sed file stops there too — not its quoted `sed` script (earlier drafts said so). Same 2 parts as
Caruca's full grammar. Stop overlap (both runs' regions, instrumented/main/repeat 1): bi-grams all 4 sources; covid/5
PaSh own + naive; unixfun/12,16 PaSh own only; 34,36 naive + Caruca full; 10 parts Caruca small only.
**2026-11-27, Draft 2.2 second pass (16 pp):** PaSh overhead model (`overhead_adjusted.py`): 0.11 s/script + 6 ms/part
compiled; with it removed PaSh's own ≈ ties bash over 72 scripts (0.97 pooled) and is ≈1.6× faster on one-pass
scripts (0.63). Web search sends 7,003 parts (`regions_sent` in `full_run/results.jsonl.gz`) → ≈42 s overhead by that
model, not the 36 s the orchestrator first quoted. Report cross-references are live PDF links (116 `/Link` with `/Dest`).
**2026-11-27, Draft 2.3 (17 pp):** critique fixes done; the report build (`report/build.ts`) now does lettered table
notes, two-pass ", p. N" page numbers, a pdf-lib outline, a per-section running head and the PDF title (conventions in
`report/README.md`, "Draft 2.3"). Title line (Tiran): "The naive LLM's files never changed PaSh's output; Caruca's
changed it in 11 of 86 scripts." Caruca's wrong-output scripts: 11 different, 9 of 86 small grammar, 10 of 86 full,
8 under both. Old Table 2 merged into Table 1; setup figure moved to A.3 (Figure A.3).
- **Decision 2026-11-27 (Tiran):** the report body shows ONE Caruca column = small (PaSh) grammars, as Caruca's paper
  ran it for PaSh; the full-grammar variant goes to one appendix part. Both grammar sets are hand-written (syntax_specs =
  human ground truth; pash_syntax_specs = hand-trimmed for PaSh), not Caruca's LLM output; the paper never mentions the
  reduced set. So the comparison is naive-LLM files vs Caruca traces of hand-written grammars (favours Caruca).
  Caruca (small): wrong in 9 of 86 scripts, splits 29, compiler stops 11, time 1.09 of PaSh's own.
**2026-11-27, Draft 2.4 (17 pp), Tiran's decision:** the body shows ONE Caruca column = the small (PaSh, hand-trimmed)
grammars, as Caruca's paper ran it for PaSh (wrong in 9 of 86); the full-grammar run is appendix A.8 only (wrong in 10,
8 shared). Both grammar sets are hand-written. Caruca small `cat`-only time = 1.14 on 13 scripts (full 1.13); earlier
drafts had them swapped. Figure scripts: `--no-caruca-full`.
- **Time explanation, checked 2026-11-27:** naive 1.15 vs Caruca(small) 1.09 of PaSh's own; the naive LLM's extra time
  vs Caruca comes almost entirely from the 34 tiny Unix50 scripts (bash 0.03-0.3 s, every split costs more than it
  saves; naive splits more), COVID ~1/4 (first sed file), Classics go the other way; Caruca sometimes faster because its
  sort file stops PaSh's compiler and the part runs as plain bash (unixfun/10, 11 at 0.5x own). One-pass real-work
  scripts with start-up removed: naive 0.88, Caruca 0.85 of bash. **No large script (bash >= 1 s) gains from the naive
  LLM's extra splits:** only 6 of 41 differ from PaSh's own (covid/1-4: slower, sed whole; spell, nfa-regex: cat split
  adds nothing). Lower naive times elsewhere have identical splits = noise. Larger Koala inputs not tested (proposed).
- **Large-input plan written 2026-11-27 (orchestration/plan_large_inputs.md), not run yet:** pre-registered: 29 scripts
  whose split decisions differ beyond cat (group A) + 14 cat-only (group B); inputs = each small input concatenated k
  times, k from a bash-only pilot (smallest of 10/30 reaching 3 s, cap 30 ~1 GB), built and deleted per script (pash VM
  has 6.6 GB free); sources bash, PaSh own, naive with second sed file, Caruca small, own copy; ~1-1.5 h. Only time can
  move with size; correctness/splits/stops are per command line. Unix50/10 under bash: 0.16 s at 30 MB, 0.76 s at 300 MB.
- **Larger-input run done 2026-11-27 ~10:05 (full_run_large/, plan pre-registered):** 43 scripts (A 29 differing
  beyond cat, B 14 cat-only), inputs x10/x30 (~1 GB), COVID own 3.6 GB. Speed vs bash A/B: PaSh own 1.30x/0.47x, naive
  0.97x/0.30x, Caruca 0.85x/0.38x. Output right: naive 43/43, own 43/43, Caruca 33/43 (new: uniq-ips wrong at 30x, right
  at small: data-dependent uniq split). Naive vs own: faster only Unix50 12/14/16 (0.59-0.71); A 1.33, B 1.57. Naive vs
  Caruca A 0.88 (faster where Caruca can't split sort), B 1.28. Naive's tr file offers consecutive chunks only (no rr):
  every script >1.4x Caruca has such a tr use (observed, not isolated). Tiran's insight (to report, Draft 2.5): PaSh's own
  files are hand-written by PaSh's authors for this suite and carry cost knowledge (split worth it), the naive LLM only
  safety knowledge; it says yes to every safe split (cat, tr cc-only), Caruca splits too little.

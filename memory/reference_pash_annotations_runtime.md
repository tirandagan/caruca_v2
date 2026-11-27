---
name: reference-pash-annotations-runtime
description: How PaSh's annotation code (pash_annotations 0.2.4, pash VM) treats a command's three files at run time — exceptions swallowed to None, round robin only with conc/adj-lines aggregators, name allowlist, attached values left as operands; and how to test outside files without touching the install
metadata:
  type: reference
---

Established 2026-10-20 while analysing naive runs 7 (cut) and 9 (sort), by reading and running
`pash_annotations` 0.2.4 in the Lima VM `pash`. Related: [[project-naive-claude-code-arm]],
[[reference-naive-run-playbook]], [[pash-grep-annotation-current-vs-json]].

**Location.** `/home/tirandagan.guest/pash/python_pkgs/lib/python3.12/site-packages/pash_annotations`
(parser tables in `parser/command_flag_option_info/data/<cmd>.json`, classes in
`annotation_generation/annotation_generators/`). PaSh ships `cut` and `sort` annotations (and
`custom_sort`); its `cut.json` lists a `-M` flag that GNU cut 9.4 rejects.

**Run-time rules (read in the source, confirmed by running):**
- `annotation_generation/AnnotationGeneration.py`: `get_input_output_info_from_cmd_invocation` and
  `get_parallelizability_info_from_cmd_invocation` wrap the class in `try/except Exception` and return
  `None`. **A broken class fails silently**, as if no annotation existed. Call the class directly to see
  the traceback.
- Only commands named in `DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES` (30 names incl. cut, sort, grep,
  uniq, tee, rm; not convert) are looked up.
- `annotation_generation/datatypes/parallelizability/Parallelizer.py` `__init__` **asserts that a round-robin
  splitter is paired only with a concatenate, adj_lines_merge, adj_lines_seq or adj_lines_func aggregator.**
  Run 9's sort class paired round robin with a custom 2-ary `sort -m …` aggregator, so for every
  ordinary sort PaSh returned no parallelizability info (only `-s`/`-u`, where it skipped round robin,
  worked). PaSh's own grep class builds the same pairing, but only in a branch guarded by
  `is_implemented`, which its custom aggregators fail, so it never runs. The naive arm's
  `formats/pash_annotation.md` (renamed `formats/annotation.md` on 2026-10-27, task 019) does not state the rule (as of 2026-10-20).
- The parser does not split attached values: `cut -d: -f2` parses with no options and operands `-d:`,
  `-f2`; `--fields=2`, `--sort=numeric`, `-k2` likewise stay operands. Listing an optional-argument option
  (`--check`) as an option makes it take the next word (`sort --check a b` → value `a`, operand `b`).
- `Option.get_name()` / `get_arg()` and `Flag.get_name()` exist (`datatypes/BasicDatatypes.py`).

**Testing outside files without touching the install:** copy the package to `/tmp/<x>/pash_annotations`
(drop `__pycache__`), lay the agent's `<cmd>.json` and two classes into it, then
`python3 -I -c 'import sys; sys.path.insert(0,"/tmp/<x>"); from pash_annotations.parser.parser import parse; …'`.
Run the same invocations with `sys.path` pointing at the install for PaSh's own answers.

**Setting one operand at a time (read from pash-annotations 0.2.4 source, 2026-11-10, uv cache copy on the Mac):**
the input/output interface's helpers only mark operands in bulk (`all_operands_are_…`, `all_but_last_…`,
`only_last_operand_…`). Inside `generate_info`, `self.input_output_info.operand_list_typer` is a plain list,
one entry per operand, default `(WhichClassForArg.FILESTD, make_stream_input())`
(`annotation_generation/datatypes/InputOutputInfo.py`); a class may assign entries by index, e.g.
`make_other_output()` from `pash_annotations.datatypes.AccessKind`. Class names are looked up from a fixed
name table in `annotation_generation/AnnotationGeneration.py` (cut → `Cut`, sort → `Sort` …).

**Stock classes shipped with pash-annotations 0.2.4 (listed 2026-11-10):** name table entries for awk, cat, col,
comm, cut, diff, grep, head, mkfifo, mv, rm, sed, seq, sort, tail, tee, tr, uniq, wc, xargs (+ helper names such as
custom_sort). `cut` and `sort` have both IO and parallelizability classes, while `rm` has only an IO class (so
not parallelizable). These are PaSh's own hand-written answers, so they can serve as a third reference side. The
naive agent was shown the stock files for tee, uniq, grep and rm, but not cut or sort.

**Run-time facts established 2026-11-19 (task 022; pash VM, PaSh `42a8b87`, pash-annotations 0.2.4, width 8).**
Read in source and confirmed by running unless marked.
- **`--r_split` does nothing** (`compiler/arg_parser.py`: obsolete). The splitting style is picked per command
  from its annotation: an implemented round-robin recipe first, then round-robin-with-unwrap, then consecutive
  chunks (`compiler/compilation.py`, `choose_parallelizing_transformation`). A recipe with an unimplemented
  mapper or merge step is skipped silently (the agent's `cat -n` recipe: never split, no error).
- **Ways PaSh falls back to bash with exit 0 and the right output** (traceback only in the `-d 2` log):
  input redirection `< file` (`NotImplementedError`, `ir_defs/dfg_node.py:210`); the command after a pipe
  believed to read a named file (`AssertionError`, `ir.py:596 pipe_append`) — caused by the parser not
  separating attached values (`-f1`, `-k2`, `head -5`: the word and everything after it become operands,
  `parser/parser.py`), by `tail.json` listing `-n`/`-c`/`-s` as flags (so `tail -n 1` anywhere kills the
  pipeline), or by a side's table missing the option; a splittable command with two input files
  (`AssertionError`, `dfg_node.py:270`); an option value typed as a file (`NameError: OptionWithIOVar`,
  `ir.py:215`, never imported); `NameError: Arg` at `ir.py:1454` (PaSh's own `bi-grams.sh`).
- **Wrong output from PaSh's own files, exit 0:** `grep -m`/`-A`/`-B`/`-C` are split (the recipe-adding
  block sits outside the test for those options); `cut -z` split; `grep -r pat dir` and `grep --color pat
  file` return nothing; `--help` lines printed once per worker; a double-quoted regex reaches workers with
  doubled backslashes (re-confirmed).
- **Workers start only when data arrives:** `r_wrap bash -c 'CMD'` runs CMD once per 1 MB piece. If PaSh
  splits a stream that carries nothing, the generated script has 8 workers and no copy of CMD ever runs.
- **Stand-in counting:** PaSh's own calls are `cat /tmp/pash_X//pash_N` (once) and `rm -f .../#fifoN`; worker
  copies of `sort`/`grep` given a file argument carry a `.../#fifoN` path instead of the file.
- **A stand-in changes `argv[0]`**, so `--help` output differs unless the bash reference uses it too.
- **GNU grep exits at the first match when stdout is `/dev/null`**: never time grep with output discarded.
- **The small benchmark inputs' server (`pac-n4.csail.mit.edu:81`) did not answer** that day; `oneliners`
  and `unix50` scripts accept `IN`, `dict`, `IN_PRE` to read other inputs.
- The Mac home is mounted read-only in the pash VM (`mount`), and only `/Users/tirandagan`, so pipe scripts
  in with care: **a script fed on stdin can be eaten by a PaSh-split command that reads stdin**.
Full list with reproducers: `naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/pash_runs/pash_bugs_for_review.md`
(for Tiran's review, nothing sent upstream: [[feedback-pash-bugs-annotate-first]]).
Related: [[project-pash-downstream-study]], [[reference-pash-comparison-scorer]].

**Facts established 2026-11-20 (PaSh `main` at `42a8b87c`, same VM), while preparing binpash/pash#795.**
- **The fallback is not fully silent.** `compiler/compilation_server.py` prints, at the default debug
  level, "[PaSh] Warning: No region was parallelized successfully" plus "Hint: Check if there are
  annotations..." when **no** region of the script compiled and neither assertion flag is set. If any
  other region compiled, nothing is printed. `--assert_compiler_success` exits 1 with "(N/M compiled)";
  `--assert_all_regions_parallelizable` likewise. The traceback needs `-d 2`. Earlier write-ups said
  "no sign outside the debug log"; corrected that day.
- **`Arg` in `compiler/ir.py`:** lost when commit `833b05ca` ("Refactor compiler", #771, 2026-01-19)
  replaced wildcard imports in `ir_defs/file_id.py` and `ir_defs/resource.py` with explicit lists.
  Four uses; only `create_reduce_tree` (line 1454) is reachable, when a merge step has extra outputs
  (stock case: `bigrams_aux`). One-line fix verified: `oneliners/bi-grams.sh` 0/2 regions compiled
  before, 1/2 after, 2.0 s vs 4.8 s on 79 MB. Sent as issue #794 / pull request #795.
- **`OptionWithIOVar` (`ir.py:215`) is four faults, not one:** missing import; `flagoption.name` should
  be `get_name()`; `to_ast_flagoption` and `to_arg_flagoption` in
  `annotations_utils/util_cmd_invocations.py` do not handle the class. With all four repaired `grep -f`
  splits correctly, **but `xargs -a file` returns nothing** (PaSh splits standard input, which it does
  not read). Not sent upstream. Stock options typed as files: `awk -f`, `grep -f`/`--exclude-from`,
  `diff -S`/`--from-file`/`--to-file`, `sort --random-source`/`--files0-from`, `xargs -a`.
- **`ir.py` hides undefined names from `pyflakes`** behind two wildcard imports. To check it, replace
  them with the names the two modules export (import them with `PYTHONPATH=compiler`), then run
  `uvx pyflakes`.
- **PaSh's compiler tests:** `evaluation/tests/test_evaluation_scripts.sh`, about 50 s here, 100 results
  (27 scripts, widths 2 and 8, with and without `--bash`). It sets `PASH_TOP` from its own location, so
  it tests whichever copy it is run from, even though the `pash` command on the search path belongs to
  the install. It compares outputs only, so a fallback to `bash` passes. Results land in
  `evaluation/tests/results/result_status`.
- **Contributing to PaSh:** pull requests target `main` (`future` is stale); commits need `-s`
  (sign-off, checked by a bot); pull requests are squashed. No push access, so a fork is needed. As of
  2026-11-20 most automatic checks fail at checkout for any fork pull request (their open #793).
  `black --check` already fails on `ir.py` at `main`.
- **Where things are:** Mac clone `~/dev/stevens/pash` (`origin` = fork `tirandagan/pash`, `upstream` =
  `binpash/pash`, partial clone); VM copies `~/pash-base` (pristine) and `~/pash-pr` (with the fix),
  test scripts and results in `~/prtest`.

**What PaSh does with a missing answer (read 2026-11-10, pash VM, `~/pash/src/pash/compiler/ir.py:255-282`):**
if the input/output lookup returns `None` (no class, or the class raised: AnnotationGeneration swallows it),
PaSh raises `UnparallelizableError("InputOutputInformation for … not provided so considered side-effectful")`
and leaves the command unparallelized. Any operand marked other output also makes it unparallelizable. A
`None` parallelizability answer is replaced by an empty one, i.e. no splitting.

**Which PaSh script runs the paper's benchmark suite (read 2026-11-20 from `binpash/pash` main, Mac clone).**
The Caruca paper's PaSh hash check (§7.1) cites [26] = the **OSDI'22 PaSh-JIT paper**, not EuroSys'21.
Its Table 1 lists 14 rows; rows 2-13 (12 benchmark sets) are the performance suite, and the one script
that runs them all is **`evaluation/osdi22-eval/run_all.sh`** (not in `evaluation/benchmarks/`). It `cd`s
into `evaluation/benchmarks`, sources `run.seq.sh` / `run.par.sh`, and runs seven groups: `oneliners`
(row 2, 10 scripts), `unix50` (3, 36), `analytics-mts` (4), `nlp` (5), `max-temp` (6), `web-index` (7),
`dependency_untangling` (rows 8-13: MediaConv, ProgInf, LogAnalysis, Genomics, AurPkg, FileEnc). Needs
`$PASH_TOP`; `--small` (4-5 h) or `--full` (paper inputs, >20 h); results in `$PWD/eval_results/run`,
then `gen_data.sh` + `generate_charts.R`. It runs bash once plus several PaSh flag sets (AOT, JIT, and
the Figure 6/7 variants). Row 1 (POSIX test suite) is not public; row 14 (microbenchmarks) is not in it.
`evaluation/benchmarks/run_all_benchmarks.sh` is older (EuroSys era, last changed 2022): only five groups
(oneliners, unix50, nlp, web-index, analytics-mts) and it checks outputs with `diff -q`.
`evaluation/benchmarks/README.md` is stale: it points to an `evaluation/eurosys/` folder that no longer exists.
More from reading the code at `42a8b87c` (2026-11-20, nothing run yet): the eval scripts need
`PASH_TOP` = **repo root** (they source `$PASH_TOP/scripts/utils.sh`), unlike the VM doc's `src/pash`;
the `pash` command (`src/pash/cli.py`) overwrites `PASH_TOP` with its own folder, so both can coexist.
`run_all.sh` **never checks correctness**: it deletes `<group>/outputs/` after every PaSh run (bash
outputs included). Width is hard-coded to 16 in `run.par.sh`. It ends with `pkill -f cat` (kills any
process whose command line contains "cat"). Results go to `$PWD/eval_results/run`; `gen_data.sh` works
relative to the current folder and zeroes the AOT numbers of the for-loop scripts on purpose.
**The OSDI'22 suite cannot fetch its inputs (tested 2026-11-22 from the pash VM and the Mac):** every
`--small` input comes from `http://pac-n4.csail.mit.edu:81/pash_data/...`, which resolves but times out;
`ndr.md` (unix50 full inputs) no longer resolves; the COVID data link on `balab.aueb.gr` returns 404;
`max-temp` fetches nothing (its setup just prints "use an FTP client"). Only `https://atlas.cs.brown.edu/data/`
answers (used by the oneliners `--full` path, which also builds 3G/10G/100G files the 40 GiB VM can't hold).
No PaSh issue mentions the outage. **`binpash/benchmarks` now redirects to `kbensh/koala` (Koala suite,
active)**: inputs on atlas with `--small`/`--min` sizes, per-suite `validate.sh` + reference `hashes`;
`unixfun` = the 36 Unix50 scripts, `oneliners` = 9 of PaSh's 10 (no shortest-scripts; adds comm,
opt-parallel, uniq-ips), `covid` = analytics-mts's 5, `nlp` renamed, `weather`/`web-search` rewritten.
Same family, not the same files. The VM's `~/pash` was clean at `42a8b87c` on 2026-11-22; R is not installed.
**Decision 2026-11-22 (Tiran):** with the OSDI'22 inputs unreachable, run PaSh on **Koala's** versions of
the same groups (oneliners, unixfun, covid, nlp, weather, web-search) at `--small`, checked against Koala's
stored hashes. That first driver and its results were **deleted 2026-11-24 at Tiran's request** (it ran only
PaSh's stock annotations, see [[feedback-pash-runs-test-our-annotations]]). Koala stays checked out at `~/koala`
(`ccf25a57`) with its small inputs downloaded (15 GB). Koala's `validate.sh` prints `<output> 0` when the hash
matches. Each group runs scripts as `$KOALA_SHELL script args…`, so a wrapper set as `KOALA_SHELL` can run PaSh.
**How to tell PaSh really parallelized a script (observed 2026-11-22, `-d 2` logs):** count
`Received data: Compile` (regions sent) vs `Optimized script saved in` (regions run in parallel). The
`Got response from compilation-server: ERROR` line is **not** reliable: Koala's bi-grams (the `Arg`
NameError), diff, set-diff and opt-parallel all fell back with zero ERROR lines; the reason appears as
`Daemon:  WARNING: Exception caught …`. `(4) Will execute script in` is printed for fallbacks too. At
`-d 1` a fully parallelized script logs nothing at all. Pilot at `--min`: all 12 one-liners matched
Koala's hashes under bash and PaSh; 8 of 12 parallelized.
**Stock-annotation Koala run (2026-11-22/23; results deleted 2026-11-24, figures kept here as PaSh-stock facts):** 77 scripts across oneliners, unixfun,
covid, nlp, weather, web-search (web-search at `--min`: `--small` = 65,424 pages, each step slower as the
index grows, well over half a day per pass). PaSh output = bash output byte for byte everywhere it can be
compared; Koala's check passed for every group under both. PaSh parallelized 42 of 77 (oneliners 8/12, unixfun
30/34, covid 4/5; nlp, weather, web-search 0). Group speed-ups (bash/PaSh time, `-w 8`): oneliners 1.9×,
covid 1.6×, weather 1.0×, web-search 0.94×, nlp 0.62×, unixfun 0.5× (sub-second scripts). NLP falls back on
"not implemented" (54k regions), its own shell function `pure_func` (24k), `rev` (3k). **Koala's web-search
index (`global-index.txt`) differs run to run even under bash** (39 of ~138k lines, pages with `€`/`~`
names), so it can't be used for a bash-vs-PaSh hash check. Koala's unixfun omits scripts 22 and 27 on purpose.
**Pilot of the suite comparison, `spell.sh` (2026-11-24, builder worker; records in
`naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`):** one region; every set's output = bash
= Koala's hash; PaSh's own files 0.61 s (sed, col, tr, sort split), naive 0.89 s (cat, tr, sort), both
Caruca sets 1.07 s (cat, sed, col, tr; **Caruca's `sort` file allows no split for a bare `sort`**, only
`sort -m`), bash 1.03 s. **The naive `sed` file allows a split when called directly but `sed` stays one
copy inside PaSh; swapping in PaSh's own `sed` files makes it split; cause not established** (the file
reads the sed script and checks it char by char). So direct-call answers are a check, not proof. Deleting
`sort`'s files made PaSh run the whole script as bash ("InputOutputInformation for sort not provided").
At `-d 2` PaSh keeps `/tmp/pash_*` with the region syntax trees. `PASH_ANNOTATIONS` is set in the VM's
profile but PaSh never reads it. Noise control: in the six Koala groups only 1 of 77 scripts has no
command with naive files and 3 of 77 none with Caruca files, so the plan adds a `pash-own-copy` set.

**Why direct calls differ from PaSh (established 2026-11-24 by the checker, debug-print copies of sets in
`~/t024-check/sets/` in the pash VM):** inside PaSh an annotation class receives a quoted shell word *with
double quotes kept*: `sed 's/[^[:print:]]//g'` arrives as `"s/[^[:print:]]//g"`, `tr -cs A-Za-z '\n'` as
`"\n"`, `tr -d '[:punct:]'` as `"[:punct:]"`. Calling the class directly via `pash_annotations.parser.parse`
gives the unquoted word. Effects on Koala `spell.sh`: the naive sed file rejects the leading `"` (no split in
PaSh, split when called directly); PaSh's own tr file sees `"\n"` as a newline set, so `tr -cs` gets the
not-implemented squeeze recipe and is not split (all sets), though a direct call allows a split. Any direct-call
check must pass operands as PaSh does (keep the quotes) to predict PaSh.
**PaSh hands annotation files quoted operands with the quotes still on (checker, 2026-11-24, shown by
instrumented copies of the sets in the pash VM, `~/t024-check/sets/{naive-sed-debug,tr-debug}`).** For
`sed "s/[^[:print:]]//g"` the file receives the script with its double quotes, so the naive `sed` checker
reads `"` as an unknown sed command and allows no split (that was the "not established" pilot puzzle); for
`tr -cs A-Za-z '\n'` PaSh's own `tr` file receives `"\n"` and treats it as squeezing newlines, which has no
split, so only 2 of spell's 3 `tr` lines split under every set. **Calling the generators directly with
unquoted operands therefore does not reproduce PaSh's answers**; pass operands as PaSh does or record what the
file is given from inside PaSh. Also: the name table additions are the only non-stock lines in each set
(62 names for naive, 2 for Caruca).
**Code path for the kept quotes, and two general faults in PaSh's own files (worker, 2026-11-24, read in the
pash VM at PaSh `42a8b87`; files called on the Mac from a copy of the uv-cache package with a stand-in `Arg`
whose `str()` is the word):** `compiler/annotations_utils/util_parsing.py:121` wraps each operand as
`Operand(Arg(...))`; `Generator_Interface.get_first_operand_name_as_string` returns `str(arg)`;
`ir_defs/arg.py:15` `__repr__` = `format_arg_chars`; `shasta QArgChar.format` returns `'"{}"'` (double quotes
whatever the script used). PaSh's own `sed` file is quote-sensitive too (`"s/d/x/"` → no split, `s/d/x/` →
split) and lets `N;s/\n/ /` split (wrong: pieces pair the wrong lines, checked with GNU sed 4.9). PaSh's own
`col` file splits always; util-linux 2.39.3 `col -bx` gives a different output when a `\v` reverse line feed
follows a piece boundary (checked); that `col` ignored `ESC 7` in the same test. On a split `cat FILE` PaSh
runs `r_split` (1 MB blocks to 8 pipes) → 8 × `r_wrap bash -c 'cat'` → `r_merge`. Write-up:
`naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/orchestration/judgment_errors.md`.

**Koala's other groups on the ARM VM (inputs worker, 2026-11-24, `orchestration/inputs_setup.md`):**
`analytics` small (2.0 GB on disk), `file-mod` small (2.3 GB; ImageMagick 6.9.11 + FFmpeg 5.1.9 built from
source in 2 min), `bio` min all run under bash. **Outputs that don't match Koala's shipped hashes but are
stable run to run:** `pcaps` (35 of 69 files; tcpdump 4.99.4 vs Koala's Debian 12), `img_convert` (1 of
508), `to_mp3` (40 of 40), `thumbnail_generation` (460 of 508): ARM builds, not tested. So for those
scripts the reference is this VM's bash output, not Koala's hash. Koala's `to_mp3` check script looks for
`ffmpeg` on the system path and can't work as shipped. `minimap2` fails to build on ARM (`-msse2`,
`-msse4.1`); `bio.sh` doesn't need it. `pkg` skipped. Free disk after setup: 9.3 GB.
**Vetted causes of the pilot's six Table-2 differences (naive-fix worker, 2026-11-24,
`orchestration/judgment_errors.md`):** none is a wrong statement about a command. `sed` (naive) = instrument
gap: PaSh formats a quoted operand as `"…"` (`QArgChar.format`) before the file sees it, and
`formats/annotation.md` never said so; one sentence added, `sed` re-run → `runs/2026-11-24_125757_naive-run-sed-r2_sed_PROMPT_v1`
(ledger `"repeat": 2`, requesty), new file reads the quoted script correctly (not yet run under PaSh).
`col` (naive says never split) is **right in general**: a reverse line feed near a piece boundary changes
the output (tested); PaSh's own file is the permissive one; in `spell` it is safe only because `sed` removed
those characters first. `cat` split (naive + Caruca) = correct, not useful. `sort` (Caruca) = method limit
(only joins it observed; `sort -m` only). Table 2 of the report said "col: a wrong judgment"; corrected 0.9.

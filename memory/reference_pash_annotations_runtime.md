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

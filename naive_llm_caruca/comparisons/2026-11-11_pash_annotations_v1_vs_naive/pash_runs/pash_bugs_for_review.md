# PaSh problems found while running it, for review before anything goes upstream

**Status, 2026-11-20: one entry has gone upstream, at Tiran's request. B5 (the missing `Arg` import) is
issue [binpash/pash#794](https://github.com/binpash/pash/issues/794) with a one-line fix in pull request
[binpash/pash#795](https://github.com/binpash/pash/pull/795). Nothing else here has been sent, and the
installed PaSh has not been changed.** Started 2026-11-19 during task 022. New findings get added to this
list. Section E records the 2026-11-20 work.

Every entry below was reproduced on PaSh **exactly as installed**, with none of our annotation files:
PaSh commit `42a8b87` (2026-09-29), `pash-annotations` 0.2.4, GNU coreutils 9.4, Ubuntu 24.04 on
aarch64, 8 workers. The reproducers are in [pash_bug_repros.sh](pash_bug_repros.sh) and their output in
[pash_bug_repros.out](pash_bug_repros.out). Run them with `bash -l pash_bug_repros.sh < /dev/null`
inside the virtual machine `pash`.

PaSh's code is in two repositories: **pash** (`binpash/pash`, the compiler and runtime) and
**annotations** (`binpash/annotations`, published as `pash-annotations`, which holds the per-command
files and the parser for command lines).

## Summary

| # | What happens | Repository | Kind | Fix looks like |
|---|---|---|---|---|
| A1 | `grep -m 5` returns nothing; `grep -A 1` returns different lines | annotations | **wrong output, exit code 0** | a few lines |
| A2 | `cut -z` returns different bytes | annotations | **wrong output, exit code 0** | a few lines |
| A3 | `grep -r pattern folder` returns nothing | annotations | **wrong output, exit code 0** | a few lines |
| A4 | `grep --color pattern file` returns nothing | annotations | **wrong output, exit code 0** | one data file |
| A5 | a line with `--help` prints the help once per worker | annotations | wrong output, low priority | a few lines per command |
| A6 | a regular expression in double quotes is passed to the workers with doubled backslashes; the count comes back 0 | pash | **wrong output, exit code 0** | not located yet |
| B1 | `NameError: OptionWithIOVar` whenever an option's value is a file (`grep -f file`) | pash | exception, falls back to `bash` | **not** one line: three more faults sit behind the import, and completing the path makes `xargs -a` return nothing (section E) |
| B2 | a value attached to its option (`cut -d, -f1`, `sort -k2`, `head -5`) is read as a file name | annotations, then pash | exception, falls back to `bash` | a parser change; needs discussion |
| B3 | a splittable command given two input files | pash | exception, falls back to `bash` | small |
| B4 | `tail -n 1` anywhere in a pipeline stops the whole pipeline from being split | annotations | exception, falls back to `bash` | one data file |
| B5 | `NameError: Arg` on PaSh's own benchmark script `bi-grams.sh` | pash | exception, falls back to `bash` | one import line. **Sent: issue #794, pull request #795** |
| D1 | `pa.sh` given a script that does not exist exits with a segmentation fault | pash | crash | small |

"Falls back to `bash`" means the output is right and the exit code is 0, but nothing runs in parallel.
The Python traceback is only in PaSh's debug log. At default settings PaSh prints one general warning,
"No region was parallelized successfully" with a hint to check the annotations, and only when no region
of the whole script compiled (`compiler/compilation_server.py`, the block after the two assertion
flags). That is the same warning a script with nothing to parallelize gets, so the author cannot tell a
compiler fault from an ordinary refusal. With `--assert_compiler_success` PaSh exits 1 and says how many
regions compiled. *(Corrected 2026-11-20: this paragraph first said the debug log was the only trace.)*

## A. Wrong output with exit code 0

### A1. `grep -m`, `-A`, `-B`, `-C` are split

- **Reproduce:** `cat in.txt | grep -m 5 ab`: `bash` prints 5 lines, PaSh prints 0.
  `cat in.txt | grep -A 1 ':96'`: `bash` prints 6,182 lines, PaSh 6,175.
- **Where:** annotations,
  `annotation_generation/annotation_generators/ParallelizabilityInfoGeneratorGrep.py`, `generate_info`.
- **Cause (read in the source):** the file's own comments say `-A`, `-B`, `-C` need context and `-m` is
  only safe file by file. The code tests `if not ...["-A", "-B", "-C", "-m"]` and chooses a mapper and a
  merge step inside that test. But the lines that then add the split-and-join recipes sit *outside* the
  test, guarded only by "mapper is None and merge step is None". When one of the four options is present,
  the test is skipped, both stay `None`, and the plain split-and-join recipe is added.
- **Fix sketch:** return without adding a recipe when any of the four options is present.
- **Why `-m 5` prints nothing rather than too much:** not established.

### A2. `cut -z` is split on newlines

- **Reproduce:** `cat in.txt | cut -z -c 1-3`: `bash` writes 4 bytes, PaSh 32.
- **Where:** annotations, `ParallelizabilityInfoGeneratorCut.py`. `generate_info` adds both recipes for
  every line; `-z` appears only in a comment.
- **Cause:** with `-z` the records end in a NUL byte, not a newline. PaSh cuts its pieces at newlines,
  so each piece starts a new "record".
- **Fix sketch:** add no recipe when `-z` is present.

### A3. Recursive `grep` on a folder returns nothing

- **Reproduce:** `grep -r 'line7 ' d`: `bash` prints 1 line, PaSh prints 0, exit code 0.
- **Where:** annotations, `InputOutputInfoGeneratorGrep.py`. Its comment reads "-r actually does not
  really affect both since files and directories are both identified by their name".
- **Cause:** the folder is typed as an input stream like any file. PaSh feeds it to its splitter, which
  gets no data, so the 8 worker copies in the generated script never start.
- **Fix sketch:** with `-r`, `-R` or `-d recurse`, add no recipe.

### A4. `grep --color pattern file` returns nothing

- **Reproduce:** `grep --color 'line7 ' in.txt`: `bash` prints 1 line, PaSh prints 0.
- **Where:** annotations, `parser/command_flag_option_info/data/grep.json`, entries
  `["--color", "WHEN"]` and `["--colour", "WHEN"]` under `option`.
- **Cause:** GNU grep takes `--color`'s value only when attached (`--color=always`). The table says it
  takes the next word, so the pattern is swallowed, the file name becomes the pattern, and PaSh believes
  grep reads standard input. It splits standard input and the workers get nothing. (When I first piped
  the reproducer script into the shell, PaSh's `grep` read the rest of the script instead.)
- **Fix sketch:** list `--color` and `--colour` as flags. The same check is worth making for every
  option whose value is optional.

### A5. A line containing `--help` is split

- **Reproduce:** `cat in.txt | sort -k 1 --help`: `bash` prints the 73-line help text once, PaSh prints
  584 lines (once per worker, merged).
- **Where:** annotations, the parallelizability classes for sort and cut (grep's input/output class
  says "we assume no help/version").
- **Fix sketch:** add no recipe when `--help` or `--version` is present. Low priority: nobody pipes
  data into `--help` on purpose. Caruca's traces caught it because Caruca runs every option.

### A6. A regular expression in double quotes reaches the workers with doubled backslashes

- **Reproduce:** `cat in.txt | grep "\(.\).*\1\(.\).*\2\(.\).*\3" | wc -l`: `bash` prints 13052, PaSh
  prints 0 and several `grep: Invalid back reference` messages on standard error. With single quotes
  around the same pattern PaSh is right.
- **Where:** pash. The debug log shows the worker command as
  `r_wrap bash -c ' grep "\\\(.\\\).*\\1..." '`. Which function rebuilds that text is **not located**.
- **History:** first seen 2026-10-05; reproduced again 2026-11-19.

## B. PaSh's compiler raises an exception and the script runs as plain `bash`

### B1. `OptionWithIOVar` is used and never imported

- **Reproduce:** `grep -f pats in.txt`. Log: `NameError: name 'OptionWithIOVar' is not defined`, at
  `compiler/ir.py:215` in `add_file_id_vars`.
- **Cause (read in the source):** line 215 is the only place the name appears in `ir.py`. It is defined
  in `pash_annotations.datatypes.BasicDatatypesWithIOVar`.
- **Fix sketch:** `from pash_annotations.datatypes.BasicDatatypesWithIOVar import OptionWithIOVar`.
  **Not tested:** whether the code after that line then works.
- **Reach:** any command line where an annotation types an option's value as a file. In task 022's
  runs: 34 of 2,377 PaSh runs (grep `-f`, sort `--random-source`), with PaSh's own files, the naive
  LLM's and Caruca's.

### B2. A value attached to its option is read as a file name

- **Reproduce:** `cat in.txt | cut -d, -f1` and `cat in.txt | sort -n | head -5`. Log:
  `AssertionError` at `compiler/ir.py:596` in `pipe_append` (`assert not other_in is None`). The same
  lines written `cut -d , -f 1` and `head -n 5` split normally.
- **Where:** the cause is in annotations, `parser/parser.py`, `parse`. A word is matched against the
  option table as a whole. `-f1`, `-k2`, `-d,` and `-5` match nothing, so the loop stops and that word
  and every word after it become file operands. PaSh then believes the command reads files, finds no
  standard input for the pipe, and hits a bare `assert`.
- **Reach:** this is how shell scripts are usually written. With PaSh's own files, 14 of the 46 `cut`
  benchmark lines and 5 of the 17 `sort` benchmark lines stopped here.
- **Fix sketch:** two levels. In PaSh, raise its own "cannot parallelize" error with a message in place
  of the bare `assert`. In the parser, split `-Xvalue` when `-X` is a known value-taking option, and
  `--name=value`. The parser change alters what every annotation sees, so it needs the authors' view.

### B3. A splittable command with more than one input file

- **Reproduce:** `grep 'line7 ' in.txt in2.txt`. Log: `AssertionError` at
  `compiler/ir_defs/dfg_node.py:270` (`assert len(streaming_inputs) == 1`).
- **Cause:** PaSh splits one stream. A recipe offered for a line with two input files reaches a bare
  `assert`.
- **Fix sketch:** decline cleanly with a message, or join the inputs first.

### B4. `tail -n 1` in a pipeline

- **Reproduce:** `cat in.txt | sort -r | tail -n 1`. Log: `AssertionError` at `compiler/ir.py:596`
  (the same assertion as B2). Without `| tail -n 1` the pipeline splits.
- **Where:** annotations, `parser/command_flag_option_info/data/tail.json`. It lists `-n`, `-c` and `-s`
  under `flag`. The comment in tail's own input/output class lists them as options that take a value,
  and `head.json` has `-n` and `-c` under `option`.
- **Cause:** `-n` is parsed as a flag, so `1` becomes a file operand. PaSh believes `tail` reads a file
  named `1` and has no standard input.
- **Reach:** every pipeline that contains `tail -n N` or `tail -c N` runs as plain `bash`. In the
  whole-script part, 2 of PaSh's 46 benchmark scripts stopped here with PaSh's own files
  (`unix50/12.sh`, `unix50/16.sh`).
- **Fix sketch:** move the three entries to `option` in `tail.json`.

### B5. `Arg` is used and never imported

- **Reproduce:** PaSh's own benchmark `evaluation/benchmarks/oneliners/bi-grams.sh`, unchanged. Log:
  `NameError: name 'Arg' is not defined`, at `compiler/ir.py:1454` in `create_reduce_tree`
  (`FileResource(Arg.string_to_arg("/dev/null"))`).
- **Cause (read in the source):** `ir.py` has no import that brings in `Arg`.
- **Fix sketch:** import `Arg` in `ir.py`. Which module to import it from was **not checked**, and
  whether the code after that line then works was **not tested**.

## C. Things PaSh declines that are limits, not bugs

- **Input redirection** (`cut -d , -f 1 < in.txt`): `NotImplementedError` at
  `ir_defs/dfg_node.py:210`. Falls back to `bash`.
- **A merge command with a value-taking option:** `assert isinstance(x, Flag)` at
  `AggregatorSpec.py:275` in the annotations library. Reached only with the naive LLM's sort files
  (9 runs); PaSh's own sort file avoids it.
- **`--r_split`:** accepted and ignored. `compiler/arg_parser.py` lists it as obsolete.

## D. Other

- **D1. Missing script file.** `pa.sh -w 8 does_not_exist.sh` exits with code 139 (segmentation fault)
  and writes no log.
- **D2. Installer on Ubuntu 24.04.** `scripts/distro-deps.sh` does not install `python3-venv`, which
  `setup-pash.sh` needs. Seen 2026-10-05; not re-run today.
- **D3. `cut.json` lists a flag `-M`** that GNU cut 9.4 rejects. Read 2026-10-20.
- **D4. Small benchmark inputs.** `evaluation/benchmarks/*/input/setup.sh --small` downloads from
  `pac-n4.csail.mit.edu:81`, which did not answer on 2026-11-19. The script does not report the failure.

## E. Work done on 2026-11-20, after Tiran asked for a pull request and an issue

All of it on private copies inside the virtual machine `pash` (`~/pash-base` untouched, `~/pash-pr` with the
fix; test scripts and results in `~/prtest`). The installed PaSh at `~/pash` was not changed. The pull
request's branch lives in a clone on the Mac, `~/dev/stevens/pash` (remote `origin` = the fork
`tirandagan/pash`, remote `upstream` = `binpash/pash`), branch `fix-ir-arg-import`.

### B5, sent upstream

- **Cause, read in PaSh's history.** Until the refactoring commit `833b05ca` ("Refactor compiler", #771,
  2026-01-19), `ir.py` got `Arg` through three wildcard imports in a row (`ir.py` from `file_id`,
  `file_id` from `resource`, `resource` from `arg`). That commit replaced the wildcards in `file_id.py`
  and `resource.py` with explicit lists, so `Arg` stopped reaching `ir.py`.
- **Reach.** `ir.py` uses `Arg` in four places. Three are in functions nothing calls
  (`get_option_or_fd`, `get_option`, `make_tee`). The live one is `create_reduce_tree`, reached when a
  command is split with a merge step that has extra outputs. In PaSh's stock files that is `bigrams_aux`.
- **Fix.** One line, `from ir_defs.arg import Arg`.
- **Tested, before and after.** `oneliners/bi-grams.sh` with 8 workers: 0 of 2 regions compiled before,
  1 of 2 after (the other is the line that loads the helper file), output identical to `bash` both
  times. PaSh's own test `evaluation/tests/bigrams.sh`: 0 of 4 before, 1 of 4 after (the other three are
  `export -f` lines). PaSh's compiler test suite (`evaluation/tests/test_evaluation_scripts.sh`): 100 of
  100 passed before and 100 of 100 after, the same result for every test. On a 79 MB text: `bash` 4.7 to
  4.8 s, PaSh before 4.7 to 4.9 s, PaSh after 2.0 to 2.1 s (3 runs each, laptop on battery).
- **Why PaSh's tests did not catch it.** They compare outputs, and the fallback gives the right output.
- **State of the pull request's automatic checks.** The sign-off check passes. Several others stop within
  seconds at the checkout step: PaSh's workflows refuse to check out code from a fork, which another open
  pull request there (#793) addresses. They did not run our change.

### B1, looked at and deliberately not sent

Adding the missing import is not enough. Three more faults sit behind it on the same path:

1. `ir.py:215` reads `flagoption.name`; the class has `get_name()` and no `name`.
2. `annotations_utils/util_cmd_invocations.py`, `to_ast_flagoption`, handles a plain flag and
   `OptionWithIO` but not `OptionWithIOVar`, so it returns nothing.
3. The same file, `to_arg_flagoption`, has the same gap.

With all four repaired in the private copy, `grep -f patterns` was split and right in 6 of 8 forms tried
(piped input, a file argument, with `-v`, `--file`, two `-f` options, in a longer pipeline); `grep -c -f`
and `awk -f` ran unsplit and right; `grep -f -` hit a different exception (`KeyError: None`,
`ir.py:605`) and fell back. **But `xargs -a file -n 1 echo` returned nothing**: PaSh split standard
input, which `xargs -a` does not read. Before the repair that line fell back to `bash` and was right. So
completing this path trades a safe fallback for a wrong answer in at least one stock annotation. It
needs the authors' view, and belongs in an issue of its own, not in a drive-by fix.

Stock files that type an option's value as a file (`pash-annotations` 0.2.4), which is what reaches this
path: `awk -f`, `grep -f` and `--exclude-from`, `diff -S`, `--from-file`, `--to-file`, `sort
--random-source` and `--files0-from`, `xargs -a`. (`sort -T` and `mv -t` are typed as outputs and are
refused earlier, cleanly.)

### Also seen, not run

A static check of PaSh's Python (`pyflakes`) names three more places that use a name without importing
it: `subprocess` in `compiler/dspash/hdfs_utils.py`, `redir_defs` in
`compiler/ir_defs/aggregator_node.py:30`, and `AstNode` in `compiler/ir_to_ast.py` and `ir.py:480`
(inside type hints only, so harmless when run). None was reproduced by a run.

### D1, cause located

`pa.sh missing.sh` dies in the preprocessor (`preprocessor/pash_preprocessor.py`), which the shell
reports as a segmentation fault, exit 139. `bash missing.sh` exits 127 with a message. A check in
`pa.sh` before the preprocessor starts would fix it. Not written, not sent.

## How these were established

- A1-A6, B1-B5, C (input redirection) and D1: run on 2026-11-19 with the reproducer script.
- The causes in A1-A5 and B1-B5: read in the installed source on the same day.
- Section E: run and read on 2026-11-20, on the private copies named there.
- A1-A5 and B1-B3 also appear in task 022's line-by-line records on the "PaSh's own" side, and B2, B4,
  B5 and input redirection in its whole-script records: [numbers_pash.md](numbers_pash.md).

## Questions for the discussion

1. Which of these go upstream, and as issues or as pull requests?
2. B2 (attached values) changes the parser every annotation depends on. Raise it as a question first?
3. A1-A4 are wrong answers in PaSh's hand-written files, which the paper uses as its reference for
   Caruca. Does that belong in the paper's discussion as well as in a bug report?

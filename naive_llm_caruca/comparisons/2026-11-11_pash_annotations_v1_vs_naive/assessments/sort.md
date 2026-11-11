---
command: sort
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[A], [B], [C], [D], [E], [F], [R]]
ratings:
  A:
    io_correct: high
    io_complete: high
    split_safe: broken
    split_coverage: low
    parser_table: gaps
    confidence: high
  B:
    io_correct: low
    io_complete: low
    split_safe: unsafe
    split_coverage: low
    parser_table: wrong
    confidence: high
  C:
    io_correct: high
    io_complete: high
    split_safe: broken
    split_coverage: low
    parser_table: gaps
    confidence: high
  D:
    io_correct: high
    io_complete: high
    split_safe: broken
    split_coverage: low
    parser_table: wrong
    confidence: high
  E:
    io_correct: medium
    io_complete: low
    split_safe: unsafe
    split_coverage: low
    parser_table: wrong
    confidence: high
  F:
    io_correct: high
    io_complete: high
    split_safe: safe
    split_coverage: high
    parser_table: good
    confidence: medium
  R:
    io_correct: high
    io_complete: high
    split_safe: unsafe
    split_coverage: medium
    parser_table: gaps
    confidence: medium
io_difference_types: [standard output differs, standard input differs, operand used by one side only, option value typed differently, kind only]
needs_running: 13
---

# sort: assessment (rubric v1)

No two sides give the same answers on every group, so each side is its own group.

## 1. How each side is built

- **A**: general rules that cover any command line. It writes standard output unless `-o`, `-c` or `-C` is
  given, reads the operands, and reads standard input when there are none. Its splitting class always adds a
  round-robin split with a custom merge (`sort -m …`) unless `-s` or `-u` is given. PaSh refuses that, so the
  class raises an exception on plain lines such as `sort`, `sort -n` and `sort file` (groups "`sort`", "`sort -rn`",
  and the 348-line group). It splits only when `-s` or `-u` is present.
- **B**: a short list of situations: only `-m` or no flags, with 0 or 1 operands. Everything else gets no answer
  (`self.input_output_info = None`). Its parser table holds only `-m`, so every other flag is read as a file
  name. There is no catch-all.
- **C**: general rules like A, plus special handling for `--files0-from -`, which makes it read standard input
  (`_files0_from_argument() == '-'`). Its splitting has the same round-robin plus custom merge pattern as A, so
  it fails in the same way. It refuses `--random-source` entirely, but it does not refuse `-z`.
- **D**: general rules like A. It refuses to split when `-o`, `-z`, `--help` or `--version` is given. It has the
  same round-robin exception on plain lines.
- **E**: an enumeration of the exact flag sets it saw (mostly pairs), with 0 or 1 operands. It gives no answer
  outside those sets. For example, there is no answer for any line with 2 or more operands (the 348-line and
  226-line groups), or for any line with `-S` or `--files0-from`. Its splitting list is also enumerated.
- **F**: general rules. It splits only by consecutive chunks and merges with the original options, minus
  `-S/-T/--parallel/--batch-size/--compress-program`, plus `-m`. It never adds round robin, so it never trips
  PaSh's rule. It raises an exception when `--files0-from` is combined with operands, which GNU sort itself
  rejects.
- **R**: general rules. It is conservative about splitting: it refuses `-s -u -R -z -m -c -C --files0-from
  --random-source`, and for every other line it splits by consecutive chunks with a merge that keeps only the
  ordering options.

For lines they were never tested on, A, C, D, F and R still give an answer. B and E mostly give none.

## 2. Input/output sets

The command lines below are the decision table's (`relpath_1`, `in1`, `s1` and so on are file names).

**Shared misreading, not a difference between sides.** On every side, the parser treats attached values
(`-k1n`, `-t,`, `-oout4`, `-S1M`), `--opt=value` and bundled flags (`-nrk 1`) as file operands. Examples:
`sort -k1n` reads operand 1, and `sort -k2 -n -t, -r` reads 4 operands. Real sort reads standard input in both
cases, so every side is wrong on these lines. This includes benchmark lines such as `sort -k1n` and
`sort -nrk 1`. The behaviour comes from the parser that all sides share, not from any side's choices.

- **Flags read as files (B).** B's table has only `-m`, so `sort -n` reads "operand 1" (the word `-n`), and so
  do `sort -c`, `sort --version` and `sort -z` (groups "`sort -rn`", "`sort -c`", "`sort --version`", "`sort -z`").
  Every other side reads standard input. B is wrong on all of these. Type: operand used by one side only,
  standard input differs.
- **`-c` / `-C` output** (groups "`sort -f -c`", "`sort -c relpath_1`", "`sort -c in1 in2`"). A, C, D, E and F
  say nothing is written. R says it writes standard output. GNU `sort -c` writes its diagnostic to standard error
  and nothing to standard output, so A, C, D, E and F are right. R's answer is wider than needed but harmless.
  Type: standard output differs.
- **`-o` with standard output (E).** For `sort -o relpath_1`, `sort -o in1 in1` and the other `-o` lines, E says
  it writes standard output *and* the `-o` file. All other sides say it writes only the `-o` file. Real sort
  writes nothing to standard output when given `-o`, so E is wrong. Type: standard output differs.
- **`--help` / `--version`** (groups "`sort --version`", "`sort -f --version`", "`sort --version relpath_1`").
  E reads nothing. A, C, D, F and R read standard input (or the operand). E matches the real command: it prints
  and exits without reading. The others are wider than needed but harmless. Type: standard input differs,
  operand used by one side only.
- **`-T` directory** (groups "`sort -T relpath_1`", "`sort -T /tmp -T /var/tmp in1`"). A, C, D, F and R mark the
  value of `-T` as written (`OTHER_OUTPUT`). E's table types it `PATH_UNTRACED`, so it is not listed. Sort does
  create temporary files in that directory when input is large, so the other sides are more faithful. Type:
  option value typed differently.
- **`--files0-from`** (groups "`sort --files0-from relpath_1`", "`sort --files0-from relpath_1 relpath_2`").
  A, C, D, F and R read the list file (`CONTAINER_FOR_INPUT`). E has no answer, and its table types the option
  `PATH_UNTRACED`, which would lose the read. Only C reads standard input for `--files0-from -`, which is what
  sort does. With operands as well, sort exits with "file operands cannot be combined with --files0-from".
  F raises an exception, so it gives no answer, which is accurate. A, C, D and R still list the operand as
  read, which is harmless. Types: option value typed differently, operand used by one side only.
- **`--random-source`** (groups "`sort --random-source relpath_1`" …). All sides read it. E types it
  `STREAM_INPUT` and the rest type it `CONFIG_INPUT`. Type: kind only. `CONFIG_INPUT` is the better fit,
  because sort reads only a seed from it.
- **`--check` with a separate word** (groups "`sort --check s1`", "`sort --debug --check /dev/null`",
  "`sort --check quiet in1`"). D's table makes `--check` an option that takes a value (`WHEN`), so
  `sort --check s1` reads standard input and swallows `s1`. The other sides read `s1`. In GNU sort the
  `--check` argument is optional and must be attached with `=`, so `s1` is a file and D is wrong. Type: option
  value typed differently.
- **`--check=quiet|silent|diagnose-first`** (groups "`sort --check=silent in1`", "`sort --check=diagnose-first
  in1`"). E and F list these words as flag aliases and read only `in1`, with nothing written. F also covers
  `diagnose-first`, which E does not. A, C, D and R read the word `--check=silent` as a second input file and
  write standard output. F matches the real command (E does for quiet/silent). Type: operand used by one side
  only, standard output differs.
- **`-y`** (groups "`sort -y in1`", "`sort -m -y ma mb`", "`sort -y 5 f1`"). C, D and F know `-y` as a flag. A and
  R read the word `-y` as a file. GNU sort accepts `-y` and ignores it for compatibility, and as far as I know it
  also ignores a following all-digit word. On `sort -y 5 f1`, C, D and F read `5` as a file and A and R read
  both `-y` and `5`. If my memory is right, nobody is fully right there, but C, D and F are closer. This is a
  check to run. Type: operand used by one side only.
- **`-c` with `-o`** (groups "`sort -c -o relpath_1`", "`sort -c -o out2 s1`"). Every side that answers lists
  the `-o` file as written. GNU sort rejects `-c` together with `-o` ("options '-co' are incompatible"), so this
  answer is wider than needed but harmless, and it is the same on every side that answers.

## 3. Splitting

- **A, C, D: broken on ordinary lines.** On `sort`, `sort -n`, `sort file`, `sort -k 2n`, `sort -S 1M in1` and
  the big groups, they add round robin with a custom merge, and PaSh raises an exception. They split only when
  `-s` or `-u` is present (groups "`sort -s relpath_1`", "`sort -nru in1`", "`sort -s -k1,1 big`"). There it is
  consecutive chunks merged with `sort -m` plus the ordering flags, including `-s` / `-u`, which should be
  safe (check 6). C also splits `sort -s -z` and `sort -u -z` (group "`sort -s -z`"). Cutting NUL-terminated
  records at newlines is unsafe. A and D refuse `-z`. A also raises an exception on `--help`, `--version` and
  `-o` lines, and C on `-o` lines.
- **B and E: unsafe.** Both split by concatenating outputs. They do this for `sort -m` lines (group "`sort -m`"),
  and E also does it for lines without `-m`: `sort -n -u`, `sort -M -s` and `sort -k 1 -s` (group
  "`sort -M -s`"), and `sort --random-source X -T Y` (group "`sort --random-source relpath_1 -T relpath_2`").
  Joining separately sorted chunks one after another is not sorted output, so this is plainly unsafe. For `-m`
  with a single input, joining consecutive chunks only copies the input through, which is fine. But
  `sort -m -u` (B and E) can leave a duplicate on each side of a chunk boundary, and round robin plus
  concatenation can reorder lines (check 8). B also splits `sort -m -z` and `sort -m -u`, because it believes
  `-z` and `-u` are files.
- **F: safe on realistic lines, and the widest coverage.** It splits every plain sort by consecutive chunks
  with `sort -m <same options>`, including `-s`, `-u`, `-T` and `-o`-free lines, and `-R` with
  `--random-source`. It refuses `-c -C -m -z --debug -o --files0-from`, and `-R` without a fixed source. Its
  remaining risks: it splits `sort --help` and `sort --version` (each copy prints the text and the merge mixes
  them, which is trivial); `--random-source=/dev/urandom` would give each copy a different hash (check 10); and
  `--sort random` detection relies on `get_arg() == 'random'` comparing a parsed argument with a string
  (check 11).
- **R: mostly safe, conservative, with one real hole.** It splits plain sort, `-k`, `-t`, `-S` and `-T` by
  consecutive chunks. It leaves safe speed unused on `-s`, `-u` and `-R --random-source` (groups
  "`sort -s relpath_1`", "`sort -nru in1`"). It splits `--debug` lines (groups "`sort --debug relpath_1`",
  "`sort -f --debug`", "`sort --debug`"). `--debug` adds underline lines to standard output, and the merge
  (which drops `--debug`) would sort those as data, so the output differs. That is unsafe. It also splits `-o`
  lines (group "`sort -o relpath_1`"), which the other splitting sides refuse. Whether PaSh copes with each copy
  carrying `-o` is check 12. It splits `--help` and `--version` too, which is trivial.
- **Shared parser problem, made worse by splitting.** F and R split `sort -k1n`, `sort -k2 -n -t, -r` and
  `sort -nrk 1`, believing the option words are files. A rewritten pipeline would try to read files named
  `-k1n`, and so on (check 13). The sides that do not split are not affected.

## 4. Parser table

- **B**: lists only `-m`. Every other flag becomes a file name. For example, `sort -n` is read as "sort the
  file `-n`", and `sort -f relpath_1` gets no answer because B counts 2 operands.
- **D**: `--check` is typed as taking a value (`WHEN`), so `sort --check s1` loses its input file. `-c` has no
  long alias.
- **E**: `-T` and `--files0-from` are typed `PATH_UNTRACED`, so the temporary directory and the list of
  inputs are not tracked. It lacks `--check=diagnose-first` and `-y`.
- **A, R**: no `-y`, so `sort -y in1` reads a file named `-y`. No `--check=…` forms, so
  `sort --check=silent in1` reads a file named `--check=silent` (and R splits it).
- **C**: has `-y`, but no `--check=…` forms (same misreading as A and R).
- **F**: has `-y` and all three `--check=` forms. I found no gap that changes how a line is read beyond the
  shared attached-value issue.

## 5. Completeness

- **B**: answers only for no flags or `-m`, with at most one operand. Everything else gets no answer, including
  two-file sorts and any key or numeric option. This looks like a limit of its method: it answers only for
  situations it saw.
- **E**: no answer for 2 or more operands, for `-S`, `--debug` and `--files0-from`, and for any flag pair it
  did not see (for example `sort -M -V` and `sort -f -c` get none). It also never reads the `--files0-from` list.
  This is also a limit of its method.
- **A, C, D**: input/output is complete. The split gap is a design mistake (round robin with a custom merge),
  not missing coverage.
- **F, R**: complete input/output. R's split refusals for `-s`, `-u` and `-R --random-source` are a choice. F
  refuses only lines where splitting is genuinely risky.

## 6. Checks to run

1. `sort -y 5 f1`: does GNU sort ignore `5`? If so, every side is wrong. A and R predict that it reads `-y`,
   `5` and `f1`. C, D and F predict that it reads `5` and `f1`.
2. `sort -c in1 > o; wc -c < o`: A, C, D, E and F predict 0 bytes. R predicts that something is written to
   standard output.
3. `sort --check s1` (with `s1` unsorted): A, C, E, F and R predict that it checks `s1`. D predicts that it
   checks standard input.
4. `sort --check quiet in1`: expect an "extra operand" error (`quiet` read as a file). D predicts that it
   checks `in1` quietly.
5. `sort --help < /dev/null`, and the same with an unreadable standard input: E predicts that it reads
   nothing. The others predict that it reads standard input.
6. `sort -s -k1,1 big` against `sort -m -s -k1,1 <(sort -s -k1,1 part0) <(sort -s -k1,1 part1)`, where
   part0 and part1 are consecutive halves of big. Repeat with `-u -k1,1`. A, C, D and F predict identical
   output. R makes no claim.
7. `printf '2\n1\n' | split -l1` and then concatenate `sort -n -u` of each part: E predicts identical output to
   `printf '2\n1\n' | sort -n -u`. I expect "2 1" against "1 2".
8. `printf 'a\na\n'` split into two one-line chunks, then `sort -m -u` on each and concatenate: B and E predict
   the same as `sort -m -u` on the whole. I expect "a a" against "a". Also run PaSh's round-robin plain plus
   concatenation on `sort -m` to see whether it reorders lines.
9. `printf 'b\0a\nc\0' | sort -s -z` against the chunked version cut at the newline: C predicts identical
   output. I expect different output.
10. `sort -R --random-source=f big` against the merge of chunk sorts with the same option, then again with
    `--random-source=/dev/urandom`: F predicts identical output for a regular file. The `/dev/urandom` case
    should break the grouping of equal keys.
11. Run A's, D's and F's classes on `sort --sort random big`: does the `'random'` comparison match the parsed
    argument? If not, A, D and F would split a random sort.
12. Run PaSh on `sort -o out in1` and `sort --debug in1` with R's annotation: R predicts identical output.
    I expect `--debug` to differ, and `-o` is uncertain.
13. Check whether PaSh's real parser reads `-k1n` and `-t,` as operands, as the decision table does. If it does,
    F's and R's splits on `sort -k1n` break.

## 7. Summary

F is the strongest side: its input/output answers are the most faithful (it gets `--check=` forms, `-y`,
`-c` and `-o` right), and it offers the widest splitting without breaking PaSh's rule. The one exception is the
attached-value misreading that every side shares. R is close behind but over-reports standard output for
`-c`, leaves `-s`, `-u` and seeded `-R` unsplit, and unsafely splits `--debug`. A, C and D have sound
input/output but raise PaSh's round-robin exception on nearly every ordinary line, while B and E answer only
the situations they listed, and their concatenation splits (for example E on `sort -n -u`) would produce wrong
output.

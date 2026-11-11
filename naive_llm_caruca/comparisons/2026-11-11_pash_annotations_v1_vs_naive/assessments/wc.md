---
command: wc
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[A], [B], [R]]
ratings:
  A:
    io_correct: high
    io_complete: high
    split_safe: broken
    split_coverage: none
    parser_table: good
    confidence: high
  B:
    io_correct: high
    io_complete: low
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
  R:
    io_correct: medium
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
io_difference_types: [no answer from one side, operand used by one side only, option value typed differently]
needs_running: 5
---

# wc: assessment

## 1. How each side is built

- **A.** General rules. Operands are files that are read, and stdin is read when there are no operands. The
  output goes to stdout. `--files0-from` gets its own branch: the value is a file that is read, and stdin is
  read when the value is `-`. Its splitting class asks for a consecutive-chunk split and a round-robin split,
  both merged with a custom "sum the counts" step that is only a placeholder (`is_implemented=False`). The
  class only does this when there is at most one operand and no `--files0-from`. It answers every line.
- **B.** A list of four exact situations: no operands, with the option set exactly `{-c,-l}`, `{-c}`, `{-l}` or
  none. It answers "stdin to stdout" for those and gives no answer for anything else. Its splitting class is
  empty.
- **R.** General rules: with no operands it reads stdin, otherwise all operands are read files, and the output
  goes to stdout. It raises an exception on purpose for `--files0-from` ("considered side-effectful"). It has
  no splitting class at all. It answers every line except `--files0-from`.

## 2. Input/output sets

All three sides agree on plain lines: group "5 lines" (`wc -l`, `wc -lc`, `wc`; 3 benchmark lines) is "reads
stdin, writes stdout" everywhere, which is correct.

**Difference 1: no answer from B (every other group).** For example `wc f1 f2` (group "13 lines"), or `wc -lwcL`
(group "2 lines (-lwcL)"). A and R give the right answer: the operands are read, or stdin when there are none.
B's gap comes from its method (it lists only `-c`/`-l` with no operands), not from a wrong rule.

**Difference 2: options R's table does not know (`operand used by one side only`).**
- `wc --debug f1` (group "1 line"). A: reads operand 1 (`f1`). R: reads operands 1 and 2, so it treats
  `--debug` as an input file.
- `wc --total only f1` (group "1 line"). A: reads `f1`. R: reads three operands, so `--total` and `only` become
  input files.

A matches recent GNU wc, which has `--debug` and `--total=WHEN` (check 1). R's table predates these options.

**Difference 3: `--files0-from names` (group "1 line"; `option value typed differently`).** A: "reads value of
`--files0-from`, writes stdout", no split. R: exception, which PaSh treats as side-effectful. Real wc reads
`names`, then opens and reads every file listed in it, and those names are not known until it runs (check 3).
A's answer is a true but incomplete list of what is read: it leaves out the listed files. If another stage of
the script wrote one of them at the same time, PaSh could get the order wrong. R's refusal is safe but gives
up any answer. Neither is fully right. R is the safer one; A is the more informative one.

**Shared by A and R (PaSh's parser).** `--opt=value` forms come back as operands: `wc --files0-from=names` and
`wc --files0-from=-` (group "15 lines"), `wc --total=always f1` (group "13 lines"), and `wc --total=only f1 f2`
(group "2 lines (--total=only)"). Both sides then say a file named `--files0-from=names` is read, and A's
`--files0-from` branch never fires for these lines. This is wrong against real wc (which reads `names`, or
stdin for `=-`) for both sides alike (check 5). Only A's test lines use these forms. The benchmark lines are
not affected.

## 3. Splitting

- **A is broken.** On every line with zero or one operand and no `--files0-from`, its class adds a round-robin
  split merged by a custom step. PaSh only allows round robin when outputs are simply joined in order, so the
  class raises an `AssertionError`. The decision table shows "exception" for the 3 benchmark lines (`wc -l`,
  `wc -c`, `wc`), for `wc -c f1` and for `wc -lwmcL`. Even without the round-robin entry, the merge step is
  marked not implemented (`is_implemented=False`), so PaSh could not run it. With two or more operands, or with
  `--files0-from`, it returns no split (groups "13 lines", "2 lines (--total=only)", "1 line (--files0-from
  names)"). So in practice A never gives a usable split. The idea is sound: sum the counts, and take the
  maximum for `-L`. But it is not a working annotation.
- **B** offers no split (empty class).
- **R** offers no split (no class file).
- **Safe speed left unused by all three.** Splitting into consecutive chunks at line boundaries and adding up
  the counts gives the same totals for `-l`, `-w`, `-c` and `-m`, and taking the maximum gives the same `-L`
  (check 4). Nobody delivers that split in a form PaSh accepts.

## 4. Parser table

- **A**: complete for current GNU wc: `-c -m -l -L -w`, `--debug`, `--help`, `--version`, `--files0-from` typed as
  an input file (a container of input names), and `--total` taking a value. Good.
- **R**: has no `--total` and no `--debug`, so `wc --total only f1` is read as three input files and
  `wc --debug f1` as two (section 2). `--files0-from` is typed `GLOB`, which does not matter because its class
  raises an exception first. Gaps.
- **B**: only `-c` and `-l`. `-w`, `-m`, `-L`, `--files0-from`, `--total`, `--help` and `--version` are missing.
  So `wc -w` can never match its option sets, and the gap shows up as no answer. Gaps.

## 5. Completeness

- **B** answers only four option sets with no operands. That is a limit of its method: it answers only
  situations it saw.
- **R** leaves out `--files0-from` on purpose (it raises an exception) and leaves out splitting altogether.
  Both are choices, and its table lags behind newer wc options.
- **A** answers everything for input/output. It tried to give a split but did not produce one PaSh will accept.
  Its incomplete `--files0-from` answer looks like a modelling choice: the format cannot name files that are
  only known when the command runs.

## 6. Checks to run

1. `wc --debug /etc/hostname; wc --total only /etc/hostname /etc/hostname; echo $?`. Confirms that the GNU
   version used accepts `--debug` and `--total WHEN` with the value in a separate word (A's reading). R
   predicts both are file names.
2. `wc --total=foo /etc/hostname; echo $?`. I expect an invalid-argument error. A and R both say a file
   `--total=foo` is read.
3. `printf '/etc/hostname\0/etc/passwd\0' > names; strace -f -e trace=openat wc --files0-from names`. I expect
   `names`, `/etc/hostname` and `/etc/passwd` all opened. A predicts only `names`. R refuses to answer.
4. `seq 1 100000 > x; wc -lwcmL x; for p in 'head -n 50000' 'tail -n +50001'; do $p x | wc -lwcmL; done`.
   Adding the per-chunk `-l -w -c -m` and taking the maximum `-L` should give the whole-file numbers. This
   supports the idea behind A's merge step, but not A's current class.
5. In PaSh, the operand list for `wc --files0-from=names` and `wc --total=always f1`. Confirms that
   `--opt=value` comes back as an operand for both A and R.

## 7. Summary

A has the best input/output answers and the most complete table, but its splitting class is broken: round robin
with a custom merge raises an exception, and the merge itself is not implemented. In practice it gives no split,
the same as the others. R is correct on plain lines but misreads newer options (`--total`, `--debug`) as input
files, and refuses `--files0-from`. B answers only `wc`, `wc -l`, `wc -c` and `wc -lc` read from stdin.

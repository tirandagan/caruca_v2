---
command: rm
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[B, R], [A], [C], [D]]
ratings:
  A:
    io_correct: high
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
  B:
    io_correct: medium
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
  C:
    io_correct: high
    io_complete: low
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
  D:
    io_correct: medium
    io_complete: low
    split_safe: none_offered
    split_coverage: none
    parser_table: wrong
    confidence: high
  R:
    io_correct: medium
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
io_difference_types: [standard output differs, operand used by one side only, no answer from one side]
needs_running: 6
---

# rm: assessment (rubric 1)

## 1. How each side is built

- **B, R** (same answer on every group). One general rule: every operand is a file written. No standard
  output, no standard input. It answers every line. R has no splitting class; B's is empty. Both mean
  "never split".
- **A**. The same general rule, plus standard output when `-v`, `--help` or `--version` is present.
  Answers every line.
- **C**. A list of situations, all with **exactly one operand**: `--help`/`--version` combinations (the
  operand is a plain word, output to stdout), listed flag sets (the operand is written), and `-v` sets
  (the operand is written, plus stdout). Everything else, including every line with two or more files,
  gets no answer.
- **D**. One situation: no flags and exactly one operand, which is written. Its parser table is empty, so
  every flag word becomes an operand. Almost every line gets no answer, and `rm -f` gets a wrong one.

## 2. Input/output sets

1. **`-v` writes to standard output.** Groups "18 lines" (`rm -v relpath_1`, `rm -r -v relpath_1`),
   "3 lines" (`rm -v a b`, `rm -rfv d a`), "2 lines" (`rm -i -v relpath_1`). A and C (where C answers)
   say stdout is written; B and R do not. GNU `rm -v` prints `removed 'x'` on standard output, so
   **A and C are right**. Type: *standard output differs*.
2. **`--help` with an operand.** Group "38 lines" (`rm --help relpath_1`, `rm -i --help relpath_1`).
   C: the operand is a plain word, output goes to stdout. A: the operand is written, plus stdout. B, R:
   the operand is written, no stdout. D: no answer. Real `rm --help` prints usage to stdout and exits
   without removing anything, so **C is right**, A is half right (stdout, but claims a file is written),
   and B and R are wrong on both counts. Types: *operand used by one side only*,
   *standard output differs*.
3. **Several files.** Groups "80", "72", "5", "3", "2", "2" (`rm -f OUT/input.words OUT/input.nextwords
   OUT/input.nextwords2`, `rm -rf genesis exodus pg`, `rm s2 s3`, …), 24 benchmark lines in all. A, B
   and R: every file is written, which is correct. C and D: no answer. Type: *no answer from one side*.
4. **One file with flags.** Group "96" (`rm -f input.txt`, 32 benchmark lines): A, B, C and R say
   operand 1 is written (correct). D gives no answer, because without a table `-f` is an operand, which
   makes two operands. Group "18" (`rm -i relpath_1`): A, B and R answer; C gives no answer (C lists
   `{-I, -i}` but not `{-i}` alone), and so does D.
5. **`rm -f` alone.** Group "1 line". A, B and R: nothing written (correct; GNU `rm -f` with no operands
   does nothing and exits 0). C: no answer. **D says operand 1 (`-f`) is written**, which is wrong: it
   treats the flag as a file name. Type: *operand used by one side only*.
6. **`--interactive` / `--preserve-root` followed by a file.** Group "5 lines" (`rm --interactive a`,
   `rm --preserve-root a`). A, B and R say nothing is written. That is **wrong**: GNU `--interactive`
   and `--preserve-root` take their value only after `=` (`--interactive[=WHEN]`,
   `--preserve-root[=all]`), so `a` is a file and is removed. The tables of A, B, R and C type both as
   options that take the next word as their value, which swallows the file name (section 4). C and D
   give no answer, which is safer here. Reporting fewer writes than really happen is the dangerous
   direction for PaSh's ordering of commands.
7. **Option words after the first file.** Group "3 lines" (`rm -I a b c d -r`,
   `rm --interactive=once a b c d`). A, B and R count `-r` and `--interactive=once` as written files, so
   PaSh's shared command-line reader stops reading options at the first file and does not handle `=`.
   GNU rm reads `-r` as a flag there. The answer claims extra writes, which is harmless for safety.
   All sides share this; it is not a difference between them.
8. **Standard input for `-i`/`-I`/`--interactive`: every side leaves it out.** `rm -i f` reads its
   yes/no answer from standard input. None of the sides marks stdin as read (groups "18 `rm -i`",
   "2 `rm -i -v`"). They are all equally incomplete here, so this is not a difference between them.

## 3. Splitting

No side allows splitting: A, B, C and D have empty classes, and R has no class file. The table shows
"no split" or "no split (no class)", never "exception". That is correct for rm: removing files is a side
effect, and nothing is gained by splitting it. No safe speed is left unused, and no class breaks PaSh's
rule.

## 4. Parser table

- **A, B, R** (identical tables) list every GNU rm flag. The fault is `--interactive WHEN` and
  `--preserve-root all` typed as options that always take a value. In GNU the value is optional and only
  attached with `=`. Example read wrongly: `rm --interactive a` gives `a` as the value, so no file is
  written (group "5 lines").
- **C**: the same flags and the same two mistyped options (`SELECTION`), so the same wrong reading. C
  only gives no answer on those lines because it has no zero-operand case for them.
- **D**: empty table. Every flag becomes an operand: `rm -f a` has two operands and gets no answer, and
  `rm -f` writes a "file" named `-f` (group "1 line").

## 5. Completeness

- **A, B, R**: answer every line. All three miss stdin for interactive prompts; B and R also miss stdout
  for `-v`/`--help`/`--version`. These look like choices or oversights in a general rule, not limits of
  method.
- **C**: answers only one-operand lines in listed flag sets, so it says nothing on 24 multi-file
  benchmark lines and on `rm -i x`. This is a limit of its method (only situations it saw). Inside that
  range it handles `--help` and `-v` most accurately of all sides.
- **D**: answers only `rm X`. Limited by both its method and its empty table.

## 6. Checks to run

1. `touch f; rm -v f 2>/dev/null`. A and C predict `removed 'f'` on stdout; B and R predict no stdout.
2. `touch f; rm --help f > /dev/null; ls f`. C predicts `f` still exists (it is a plain word). A, B and R
   predict `f` is written (removed).
3. `touch a; yes | rm --interactive a; ls a` and `touch a; rm --preserve-root a; ls a`. A, B and R
   predict nothing is written (the file name is taken as the option's value). Expected: `a` is removed
   both times.
4. `touch f; printf 'n\n' | rm -i f; ls f`. Expected: `f` survives, which shows rm reads stdin. No side
   predicts a stdin read.
5. `touch ./-f; rm -f; echo $?; ls ./-f`. D predicts the file `-f` is written. A, B and R predict nothing
   is written. Expected: exit 0 and `-f` still there.
6. `mkdir d; touch a b c ./-r; yes | rm -I a b c d -r; ls`. A, B and R predict a file `-r` is written.
   Expected under GNU option reordering: `-r` is a flag, `d` is removed, and the file `-r` survives.

## 7. Summary

A, B and R apply one general rule (every operand is written) and answer every line. A also models
`-v`/`--help` output to stdout, which B and R miss. C is the most accurate where it answers, and it is
the only side to read `rm --help f` as removing nothing, but it answers only single-file lines. D, with
an empty parser table, answers almost nothing and misreads `rm -f`. No side splits (correct), and every
side's table mistypes `--interactive`/`--preserve-root` and leaves out the stdin read of interactive
prompts.

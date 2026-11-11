---
command: cp
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[A], [B], [C], [D]]
ratings:
  A:
    io_correct: medium
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
  B:
    io_correct: high
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
  C:
    io_correct: high
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
  D:
    io_correct: low
    io_complete: low
    split_safe: none_offered
    split_coverage: none
    parser_table: wrong
    confidence: high
io_difference_types: [operand direction differs, standard input differs, standard output differs, option value typed differently]
needs_running: 7
---

# cp — assessment

There is no side R for `cp`. A, B and C have the same parser table, word for word.

## 1. How each side is built

- **A**: general rules for any line. With `-t`/`--target-directory`, every operand is read and the `-t`
  value is written; otherwise every operand but the last is read and the last is written. No standard
  input or output, ever.
- **C**: A's rules plus two more: standard output is written with `-v`/`--debug`, standard input is read
  with `-i`. (Checking only `-t` instead of A's `-t`/`--target-directory` makes no difference: the
  decision table shows `cp --target-directory d a` handled the same by all three.)
- **B**: C's rules, plus it raises an exception when there is no `-t` and fewer than two operands (`cp`
  needs a source and a destination). It covers any line; the exception only fires on lines that cannot
  be a working copy.
- **D**: one situation: no flags and exactly two operands, and then "both operands written". Its parser
  table is empty, so any flag becomes an operand. Everything else gets no answer.

## 2. Input/output sets

Real GNU `cp`: reads the sources, writes the destination (or the `-t` directory), prints one line per
file to standard output with `-v`, reads standard input with `-i` when it has to ask before overwriting.

1. **Plain copies** (17 lines, incl. all 4 benchmark lines, e.g. `cp R1.fastq Sample1.R1.fq`).
   A, B, C: reads operand 1, writes operand 2. D: writes operands 1 and 2, reads nothing. Real: the
   source is only read. **A, B, C match**; D gets the direction of the source wrong. Type: *operand
   direction differs*.
2. **`-v` / `--debug`** (16 lines, e.g. `cp -v /tmp/.../a out`, `cp --verbose ... a out`; plus
   `cp -abfHilLnPpRrsuvx a d`). B, C: also write standard output. A: does not. Real `cp -v` prints
   `'a' -> 'out'` on standard output, so **B, C match**. Whether `--debug` writes to standard output too
   is a check to run. Type: *standard output differs*.
3. **`-i` / `--interactive`** (10 lines, e.g. `cp -i a b`; plus the clustered line). B, C: also read
   standard input. A: does not. Real `cp -i` asks and reads the answer from standard input when the
   destination exists; **B, C match** (they say so even when no question will be asked, which is a safe
   over-claim). In `cp -H -L -P -l -s -x -p -d -a -f -i -n a d` the later `-n` may cancel `-i`; check to
   run. Type: *standard input differs*.
4. **`cp -t d` with no source** (1 line). A, B, C: writes the value of `-t`. D: writes operands 1 and 2,
   because its empty table reads `-t` as a file. Real: error, nothing copied; A/B/C over-claim harmlessly,
   D names a file called `-t`. Type: *option value typed differently*.
5. **Optional values taking the next word, shared by A, B, C** (28-line group, e.g. `cp --backup a d`,
   `cp --preserve a d`, `cp --reflink a d`). The shared table makes `--backup`, `--preserve`, `--reflink`
   (and `--update`, `--context`) take the next word as their value, so `a` vanishes as a file. A, C:
   reads nothing, writes operand 1 (`d`). B: exception (one operand left), which PaSh sees as no answer.
   In GNU `cp` these options take an *optional* value that must be attached with `=`, so the real command
   reads `a` and writes `d`. **No side is right; B's no-answer is the safer failure**, A and C miss a read.
   The same misreading sits inside the 141-line group: `cp --backup numbered a d` is read as "reads `a`,
   writes `d`", but real `cp` treats `numbered` as a second source. In the same group,
   `cp --sparse always a d`, `cp --no-preserve mode a d` and `cp -S .bak a d` are read correctly, because
   those options really do require a value.
6. **Words the reader does not split, shared by A, B, C** (187-line group, e.g. `cp --backup=numbered a d`;
   4-line group, e.g. `cp --suffix=.bak -b a d/`, `cp -S.bak -b a dir/`; `cp -t d -- a b`). The value
   attached with `=`, an attached short value (`-S.bak`), any flag after it, and `--` all come out as
   extra operands that are *read*. Real `cp` reads only `a`. All three over-claim the same way, so this
   does not separate them; it comes from how PaSh reads the line, not from the classes.
7. **Not modelled by anyone.** `cp -b a d` (and `--backup`) also writes a backup file `d~` that is not on
   the command line; no side records it. `cp --help a d` prints help and copies nothing, but A, B, C
   would say "reads `a`, writes `d`" (none of their classes checks `--help`; no decision-table line
   tests it).

## 3. Splitting

All four sides return an empty list: never split. That is right: `cp` has no stream input to divide.
No safe speed left unused, no rule broken.

## 4. Parser table

- **A, B, C** (identical): list GNU `cp`'s flags thoroughly (`-a -b -d -f -i -H -l -L -n -P -p -R -s -T
  -u -v -x -Z`, `--parents`, `--attributes-only`, `--copy-contents`, `--debug`,
  `--remove-destination`, `--strip-trailing-slashes`, `--help`, `--version`) and type `-t` as a written
  directory, which is right. The one real error is typing the optional-value options `--backup`,
  `--preserve`, `--reflink`, `--update` and `--context` as taking the next word: `cp --backup a d` is read
  as having one operand (28-line group).
- **D**: empty table. Every flag is read as a file, so `cp -t d` is two operands and any flagged line is
  outside its one case.

## 5. Completeness

- **A, C**: answer every line except bare `cp` (exception, 1 line). A's missing standard input/output
  is a choice or oversight in its general rule.
- **B**: also fails on the 28 lines where the shared table leaves one operand. That is a deliberate check,
  and here it avoids a wrong answer.
- **D**: answers 18 of 418 lines (the 17 plain copies, wrongly, and `cp -t d`, wrongly); no answer on
  anything with a flag. A limit of its method: it answers only the one situation it saw.

## 6. Checks to run

1. `touch d; echo y | cp -i a d` — expected: a question, and the answer read from standard input. B, C:
   standard input read. A: not.
2. `cp -v a d` — expected `'a' -> 'd'` on standard output. B, C: standard output written. A: not.
3. `cp --debug a d > out; cat out` — does the debug text go to standard output? B, C say yes.
4. `cp -i -n a d` with `d` existing — does `-n` cancel the question (no standard input read)? B, C say
   standard input is read.
5. `cp --backup a d; ls` — expected: `a` read, `d` written, `d~` created. A, C: `a` not read. B: no
   answer. No side: `d~`.
6. `mkdir d; cp --backup numbered a d` — expected: `numbered` treated as a source (error "cannot stat
   'numbered'"), `a` copied into `d`. A, B, C: reads `a` only.
7. `cp --help a d; ls d` — expected: help on standard output, `d` not created. A, B, C: reads `a`, writes
   `d`, no standard output.

## 7. Summary

B and C give the most accurate answers: correct file directions plus standard output for `-v` and standard
input for `-i`; they differ only in that B refuses (raises) when a line leaves fewer than two operands,
which here avoids a wrong answer. A has the same file rules but never marks standard input or output, and D
answers almost nothing and gets the source's direction wrong when it does. A, B and C share one table error
(optional-value options like `--backup` swallow the next word), and the reader turns attached `=` values
and `--` into extra read files on every side.

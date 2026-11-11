---
command: rm
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[C, R], [A], [B], [D]]
ratings:
  A:
    io_correct: high
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
  B:
    io_correct: high
    io_complete: medium
    split_safe: none_offered
    split_coverage: none
    parser_table: gaps
    confidence: high
  C:
    io_correct: medium
    io_complete: high
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
io_difference_types: [standard output differs, operand used by one side only]
needs_running: 7
---

# rm — assessment

## 1. How each side is built

- **C and R** (same code, same parser table): one general rule, "every operand is a file that is
  written" (`self.all_operands_are_other_outputs()`), applied to any command line. There is no special
  case, so a line it was never tested on still gets an answer, built from the same rule.
- **A**: the same general rule as C/R, plus one more: standard output is written when `-v`, `--help` or
  `--version` appears. It covers every line too.
- **B**: a list of specific situations. It answers only when there is exactly one operand **and** the set
  of flags is one of about 70 listed combinations; everything else, including every line with two or
  more files, falls through to `self.input_output_info = None` (no answer). Lines outside what it saw get
  no answer.
- **D**: one situation only: no flags and exactly one operand. Its parser table is empty
  (`"flag": [], "option": []`), so any flag word is read as a file name. Everything else gets no answer.

## 2. Input/output sets

Real GNU `rm`: reads no file contents, removes (writes) each operand, prints to standard output only with
`-v` (one "removed ..." line per file) or `--help`/`--version` (and then removes nothing), reads standard
input with `-i`, `-I` or `--interactive` to get the yes/no answers.

1. **`--help` with an operand** (38 lines, e.g. `rm --help relpath_1`, `rm -i --help abspath_1`).
   - B: operand is a plain word, writes standard output only.
   - A: writes operand 1 **and** standard output.
   - C, R: writes operand 1, no standard output.
   - Real: `--help` prints help to standard output and exits before removing anything. **B matches.** A is
     right about standard output and over-claims the write (harmless, but wrong). C/R are wrong twice:
     they miss standard output and claim a write that never happens. Types: *standard output differs*,
     *operand used by one side only*.
2. **`-v`** (18 + 3 + 2 lines, e.g. `rm -v relpath_1`, `rm -rfv d a`, `rm -i -v relpath_1`).
   - A and B (B only for its listed one-operand cases): operands written plus standard output.
   - C, R: operands written, no standard output.
   - Real: `-v` prints one line per removed file to standard output. **A and B match**; C/R miss
     standard output. For `rm -i -v relpath_1` B gives no answer (`{'-i', '-v'}` is not in its list).
     Type: *standard output differs*.
3. **`rm -f` with no operand** (1 line).
   - A, C, R: writes nothing. D: writes operand 1.
   - Real: nothing happens. D is wrong because its empty table reads `-f` as a file name, so it claims
     `rm` deletes a file called `-f`. **A, C, R match.** Type: *operand used by one side only*.
4. **Answer versus no answer** (not an input/output difference, but the largest gap). On the 80-line
   group (`rm -rf genesis exodus pg`), the 72-line group (`rm -f a b`) and every larger group, A, C and R
   answer "writes every operand", which is correct; B and D give no answer. On the 96-line group
   (`rm -f input.txt`) D gives no answer because `-f` becomes a second operand.
5. **Shared by every side: standard input under `-i`.** No side marks standard input for `-i`, `-I` or
   `--interactive` (e.g. `rm -i relpath_1`: A, C, R say "writes operand 1" only; B, D no answer). Real
   `rm -i` reads its answers from standard input. Not a difference between sides, but all are incomplete
   here.
6. **Shared by A, B, C, R: `--interactive` and `--preserve-root` swallow the next word** (5-line group,
   `rm --interactive a`, `rm --preserve-root a`): A, C, R say "writes nothing"; B no answer. In GNU `rm`
   both take an *optional* value that must be attached with `=` (`--interactive=once`), so `a` is a file
   and is removed. A/C/R under-report a real deletion here. See section 4.
7. **Shared by A, C, R: words the PaSh reader does not recognise become files.** `rm -I a b c d -r`,
   `rm -rf a b c d -` and `rm --interactive=once a b c d` all come out as five written operands, and
   `rm -v -- -` as two. So a file named `-r`, `--interactive=once` or `--` is claimed as written. GNU `rm`
   treats a trailing `-r` as a flag, `--interactive=once` as an option and `--` as the end of options.
   These are over-claims, not misses, and come from how the command line is read, not from the classes.

## 3. Splitting

Every side has an empty list (A, B, C, D) or no class at all (R): never split. That is right for `rm`,
which has no stream input to divide. No safe speed is left unused, and no class breaks PaSh's rule.

## 4. Parser table

- **A, B, C, R** list all of GNU `rm`'s flags (`-f -i -I -r/-R -d -v --one-file-system
  --no-preserve-root --help --version`). Their tables are the same in effect (B only renames the value
  placeholder to `SELECTION`). All four type `--interactive` and `--preserve-root` as options that take
  the next word. Effect: `rm --preserve-root a` is read as having no file, so A/C/R say it writes nothing
  (5-line group).
- **D**: empty table. Every flag becomes an operand: `rm -f` is read as deleting a file `-f`, and
  `rm -f input.txt` as two operands (so no answer).

## 5. Completeness

- **A, C, R**: answer every line. What they leave out (standard input under `-i`, standard output under
  `-v` for C/R) looks like a choice or an oversight in a general rule, not a method limit.
- **B**: answers only one-operand lines in its listed flag sets: 172 of 368 lines (all of the 96, 38, 20
  and 18-line `-v` groups), and only 47 of the 71 benchmark lines. Nothing with two or more files. This is
  a limit of its method: it only answers situations it saw. Odd holes inside that method: `{'-i'}`
  alone and `{'-i', '-r'}` are missing from its list, so `rm -i relpath_1` gets no answer.
- **D**: answers 21 of 368 lines (the 20-line `rm aux1` group, correctly, and `rm -f`, wrongly). Method
  limit: one situation seen.

## 6. Checks to run

1. `touch f; rm --help f > out; ls f; wc -l out` — B: `f` survives, help on standard output. A: `f`
   written, standard output. C, R: `f` written, no standard output.
2. `touch f; rm -v f` — A, B: prints `removed 'f'` on standard output. C, R: nothing on standard output.
3. `touch f; rm --preserve-root f; ls f` — expected: `f` removed. A, C, R: nothing written. B, D: no
   answer.
4. `touch f; echo y | rm -i f; ls f` — expected: `f` removed after reading `y` from standard input. No
   side marks standard input.
5. `mkdir d; rm d -r; ls d` — expected: `d` removed (GNU moves options found after files). A, C, R would
   read `-r` as a file, as in `rm -I a b c d -r`.
6. `touch -- -; rm -v -- -` — expected: only `-` removed, nothing called `--` touched. A, C, R list `--`
   as a written file.
7. `rm --interactive=once a b c d` through PaSh's parser — confirm it yields five operands (A, C, R mark a
   file `--interactive=once` as written); real `rm` removes four files.

## 7. Summary

C and R are identical and A extends them correctly with standard output for `-v`/`--help`; all three
answer every line and are right on every file `rm` actually deletes in the benchmark lines. B is the most
precise when it answers (it alone gets `--help` right) but gives no answer on any line with two or more
files, and D answers almost nothing and misreads every flag as a file. All sides miss standard input under
`-i`, and A, B, C, R wrongly let `--interactive` and `--preserve-root` take the next word.

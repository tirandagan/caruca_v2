---
command: grep
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[A], [B], [C], [D], [R]]
ratings:
  A:
    io_correct: medium
    io_complete: high
    split_safe: unsafe
    split_coverage: high
    parser_table: gaps
    confidence: medium
  B:
    io_correct: medium
    io_complete: high
    split_safe: unsafe
    split_coverage: high
    parser_table: gaps
    confidence: medium
  C:
    io_correct: high
    io_complete: medium
    split_safe: safe
    split_coverage: high
    parser_table: good
    confidence: medium
  D:
    io_correct: low
    io_complete: low
    split_safe: safe
    split_coverage: low
    parser_table: wrong
    confidence: high
  R:
    io_correct: medium
    io_complete: high
    split_safe: unsafe
    split_coverage: high
    parser_table: gaps
    confidence: high
io_difference_types: [operand direction differs, operand used by one side only, standard input differs, standard output differs, kind only]
needs_running: 11
---

# grep: assessment

No two sides give the same answers on every group of the decision table, so each side is its own group.
Operand numbers below follow the decision table (operand 1 = the first word that is not an option).

## 1. How each side is built

- **A, B, R** use general rules. If `-e`/`-f` is present, every operand is a file read; otherwise
  operand 1 is the pattern and the rest are files read. With no file, grep reads standard input; `-q`
  turns off standard output. These rules give an answer for almost any line, including lines no one
  tested. Differences: A also counts `-d recurse` as recursive and adds standard input for `-f -`. B
  turns off standard input for `-r`/`-R` only. R has no recursion rule at all.
- **C** uses the same general rules and adds two things. (a) A catch-all refusal: if any operand starts
  with `-` (other than `-` itself), its input/output class raises an exception on purpose
  (`has_unrecognised_option`). A word like that means PaSh's parser misread an option. (b) Recursion
  handling: under `-r`/`-R`/`-d recurse`, operands are marked as non-stream ("other") input, and with no
  operand it declares the current directory `.` as the input. On new lines it either answers by rule or
  refuses. It never guesses.
- **D** is a list of exact situations: 1 or 2 operands, with flags drawn only from `-R -c -r -v`. Every
  other line gets "no answer" (`self.input_output_info = None`). Its parser table knows only those four
  flags, so any other flag is read as an operand and changes the operand count. When that count lands
  on 2, D answers, and it answers wrongly (see section 2). So outside the lines it was tested on, its
  answers cannot be trusted.

## 2. Input/output sets

Every difference, grouped by cause:

1. **D reads the pattern as a file** whenever an unknown flag takes the operand count to 2. Lines:
   `grep -n foo`, `-b foo`, `-in foo` (group "-in foo…"), `grep -vE '^_[^_]'`, `grep -e foo`,
   `grep -i foo`, `grep -o 'fo*'`, `grep -z foo`, `grep -R -e foo`, `grep -q foo`. On all of these D
   says it "reads operand 2" (the pattern, for example the file `foo`) and does not read standard input.
   A, B, C, R say it reads standard input. **A, B, C, R are right**: on every one of these lines grep
   reads standard input. On `grep -q foo`, D also says the command writes to standard output, but `-q`
   writes nothing (standard output differs). On `grep -f pats`, D reads `pats`, which is correct by
   accident, but it misses standard input.
2. **Values attached with `=` or glued to a short option** (`--binary-files=x o a.txt`, `--color=x`,
   `--no-group-separator=x`, `-H --label=x foo`, `-A0 --group-separator XX o a.txt`,
   `-r '--include=*.txt' '--include=*.c' foo .`). PaSh's parser keeps the whole word as an operand, so
   A, B, R take it as the pattern and treat the real pattern as a file. For example, on
   `--binary-files=x o a.txt` they say grep reads `o` and `a.txt`. In fact `o` is the pattern and only
   `a.txt` is read. On the `--include` line they say grep reads files named `--include=*.c`, `foo` and
   `.`. C raises its exception (no answer). D gives no answer. **No side gets these right; C and D are
   safe, A, B, R are wrong** (an operand is read by one side only, or its direction differs).
   On `-efoo a.txt` and `--regexp=foo a.txt`, A, B, R are right by luck (the glued word is the pattern
   either way). On `--file=a.txt a.txt` and `-fa.txt a.txt` they are right only because the pattern file
   and the input are the same file.
3. **`-NUM` context** (`grep -2 bar a.txt`). A, B, R: `-2` becomes the pattern and they read `bar` and
   `a.txt`. C lists `-0`…`-9` as flags and reads only `a.txt`. **C is right**: in GNU grep, `-2` means
   `-C 2` (check 9).
4. **`--color` with no `=`**. A and C type `--color`/`--colour` as a flag. B and R type it as an option
   that takes a separate value (`WHEN`).
   - On `grep --color foo a.txt`, A and C read `a.txt`. B and R take `foo` as the colour, `a.txt` as the
     pattern, and read standard input.
   - On `grep --color always foo a.txt`, A and C read `foo` and `a.txt`. B and R read only `a.txt`.
   - **A and C are right**: in GNU grep the value of `--color` is optional and must be attached with
     `=`, so `--color foo a.txt` searches `a.txt` for `foo` (check 3). This is a common real-world form.
   - On `--color=always foo a.txt` (and `=never`, `=auto`), only C lists those exact words. It reads
     `a.txt` and is right. A, B, R read `foo` as a file.
5. **Recursive search with no file operand** (`grep -r a`, `grep -R a`, `grep -c -r a`,
   `grep -R -e foo`, `grep -d recurse foo`). GNU grep then searches the current directory and does
   not read standard input (check 4).
   - A says it reads nothing, which misses the directory but is not wrong in direction. B says the same
     for `-r`/`-R` but says standard input for `-d recurse foo`.
   - R says standard input on all of them. **R is wrong**.
   - C's code declares `.` as the implicit input (`get_from_original_filename_with_ioinfo(FileName('.'),
     make_other_input())`). That is the right answer, but the table prints it as "reads stdin",
     probably because it fills the slot normally used for standard input. How PaSh reads that slot is
     check 5.
   - D gives no answer.
6. **`grep -f - a.txt`**: only A adds standard input. **A is right**: `-f -` reads the patterns from
   standard input. B, C, R treat `-` as a plain file named by the value of `-f`.
7. **`grep --regexp foo a.txt`**: A, B, C read `a.txt`. R reads standard input, because its parser table
   lists `--regexp` apart from `-e` and its code tests only `-e`. **A, B, C are right.**
8. **Kind only.** For recursive lines with a path (`grep -R a relpath_1`), C marks the operand as
   "other" input, because it may be a directory and cannot be read as one stream. A, B, D, R mark it as
   a stream input. C's choice matches what grep does. The decision table does not show kinds; this
   comes from the code.
9. **`grep` with no arguments.** B and R raise an exception (they set operand 1 as the pattern when
   there are no operands). A says standard input. C says nothing is read. grep only prints a usage
   error here, so this does not matter.

All five sides agree on everything else: single-file and standard-input lines, `-q`, `-c`, `-l`, `-L`,
`-f FILE`, `--exclude-from`.

## 3. Splitting

- **R splits where it must not.** When `-A`, `-B`, `-C` or `-m` is present, R's code leaves the mapper
  and aggregator empty and still falls through to `append_to_parallelizer_list(...)`. So it offers
  consecutive-chunk and round-robin splitting with plain concatenation on `grep -m 1 foo`,
  `grep -C 1 foo`, `grep -m -1 o a.txt` and the 36-line group. **Unsafe**: `-m 1` on two chunks can print
  two matches, and context lines and `--` separators break at chunk edges (check 1). R also splits
  `grep -z foo`, where records end in NUL, not newline, and a line-based split can cut a record in two
  (check 2). A, B, C refuse all of these.
- **A, B, R split multi-file and recursive lines** (`grep foo a.txt b.txt`, `grep -e foo a.txt b.txt`,
  `grep -R a relpath_1`, `-d recurse foo a.txt`, `-r --include '*.txt' foo .`). With two or more files,
  grep puts the file name at the start of each line. Recursive search may be over a directory, which
  cannot be cut into chunks. Both look unsafe (checks 6, 7). C allows splitting only with at most one
  file and no recursion, which is the safe choice.
- **A, B, R split `grep -R a`** (no operand). A and B say it reads nothing, so there is nothing to split.
  For R, each copy would search the whole current directory, which repeats the output.
- **D** splits only `grep PAT` and `grep -v PAT` reading standard input. This is safe, but it leaves
  unused the safe splitting of `grep PAT file` (the `grep a relpath_1` group) and of every other flag.
- `-c`, `-l`, `-L`, `-n`, `-b`: A, B, R name the right custom merge steps but mark them not implemented,
  so no split. C and D refuse. Same result for every side.
- No side breaks PaSh's round-robin rule: every round-robin split uses concatenation.
- **`grep -f - a.txt`**: A, B, C, R all split. If PaSh splits `a.txt` and gives standard input to only
  one copy, the other copies get no patterns (check 8).

## 4. Parser table

- **D:** only `-R -c -r -v`. Every other flag (`-n`, `-i`, `-e`, `-q`, `-o`, `-z`, …) becomes an operand.
  Example: `grep -n foo` is read as pattern `-n` and file `foo`.
- **A:** no `-0`…`-9`, so `grep -2 bar a.txt` is read wrongly. `--color` is a flag only, so
  `--color=always` is not recognised.
- **B, R:** `--color`/`--colour` take a separate value (`WHEN`), so `grep --color foo a.txt` is read
  wrongly (section 2, item 4). No `-NUM` either. R also lists `-e` and `--regexp` as separate entries,
  and `-m`/`--max-count` and `-A`/`--after-context` the same way. Its code tests only the short names,
  so `--regexp foo a.txt` is read wrongly, and the long forms of `-m`/`-A`/`-B`/`-C` are not seen. This
  has no extra effect on splitting, since R splits anyway (section 3).
- **C:** has `-NUM` and every documented `--color=WHEN` word. Glued values (`-A0`, `--include=…`) are
  a limit of PaSh's parser, which no table can fix. C detects them and refuses.

## 5. Completeness

- **D** answers only for its tested flag sets and operand counts. That is a limit of its method, and
  its parser table makes it worse: its answers on untested lines are wrong rather than missing.
- **C** gives no answer on about 50 lines with `=` or glued values. That is a choice (refuse when the
  parse is suspect), and it trades completeness for correctness. It also never splits with two or
  more files or with recursion, which is a deliberate safety choice.
- **A, B, R** answer almost everything, including lines they cannot have parsed correctly. None of them
  represents the current directory as the input of `grep -r PAT`. That is a modelling gap, not a limit
  of method.

## 6. Checks to run

1. `seq 1 200000 | grep -m 1 1` against the same line under PaSh, width 2. R predicts the same output.
   A, B, C, D predict that splitting is unsafe, which is why they refuse it. Repeat with
   `grep -C 1 5000`.
2. A NUL-separated input with newlines inside records, `grep -z foo`, under PaSh, width 2. R predicts
   the same output. The others refuse to split.
3. `printf 'foo\n' > a.txt; grep --color foo a.txt < /dev/null`. A and C predict `foo` (reads
   `a.txt`). B and R predict that it reads standard input with pattern `a.txt` (no output).
4. In a folder with `x.txt` containing `a`: `echo a | grep -r a`. A predicts `x.txt:a` with standard
   input ignored. R predicts `a` read from standard input. Also try `echo a | grep -d recurse a`, where
   B predicts standard input.
5. Run PaSh's input/output step with side C on `grep -r a`, and look at what it records as input: the
   current directory or standard input.
6. `grep foo a.txt b.txt` under PaSh, width 2. A, B, R predict the same output, file-name prefixes
   included. C refuses to split.
7. `grep -R a somedir` under PaSh, width 2 (A, B, R split it). Separately, `grep -r a file.txt` on one
   regular file: is there a file-name prefix? That decides whether the split is ever safe.
8. `printf 'foo\n' | grep -f - a.txt` alone and under PaSh, width 2. A predicts that standard input is
   read for the patterns. B, C, R predict a file named `-`. Compare the outputs.
9. `printf 'x\nbar\ny\n' > a.txt; grep -2 bar a.txt`. C predicts the 3 lines of context output from
   `a.txt`. A, B, R predict `-2` used as the pattern and `bar` opened as a file.
10. Run PaSh with C on `grep --binary-files=x o a.txt`. Confirm that the deliberate exception becomes
    "no answer" (treated as having side effects) and does not crash the compile.
11. `grep -- -foo a.txt` with side C. Does PaSh's parser leave `-foo` as an operand, so that C refuses a
    valid line? A, B, R predict that it reads `a.txt`.

## 7. Summary

C is the most correct side. It types `-NUM` and `--color=WHEN` correctly, models recursion, refuses
lines its parser has misread, and splits only single-file, non-recursive lines without context or
`-m`. A, B and R share a broad rule that answers almost everything but trusts misparsed lines, splits
multi-file and recursive searches, and (B, R) mistypes `--color`; R also splits
`-m`/`-A`/`-B`/`-C`/`-z`, which is plainly unsafe. D is a short list of tested cases with a four-flag parser table, so on most
untested lines it gives no answer, and where an unknown flag shifts the operands it confidently names
the pattern as the file read.

---
command: cut
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[A, C, D, F], [B], [E], [R]]
ratings:
  A:
    io_correct: medium
    io_complete: high
    split_safe: safe
    split_coverage: high
    parser_table: good
    confidence: high
  B:
    io_correct: high
    io_complete: low
    split_safe: safe
    split_coverage: low
    parser_table: gaps
    confidence: high
  C:
    io_correct: medium
    io_complete: high
    split_safe: safe
    split_coverage: high
    parser_table: good
    confidence: high
  D:
    io_correct: medium
    io_complete: high
    split_safe: safe
    split_coverage: high
    parser_table: good
    confidence: high
  E:
    io_correct: high
    io_complete: low
    split_safe: safe
    split_coverage: low
    parser_table: good
    confidence: high
  F:
    io_correct: medium
    io_complete: high
    split_safe: safe
    split_coverage: high
    parser_table: good
    confidence: high
  R:
    io_correct: medium
    io_complete: high
    split_safe: unsafe
    split_coverage: high
    parser_table: good
    confidence: high
io_difference_types: [no answer from one side, standard input differs, operand used by one side only]
needs_running: 8
---

# cut: assessment

## 1. How each side is built

- **A, C, D, F (same answers everywhere).** They use general rules: every operand is a file that is read,
  standard input is read when there are no operands, and output goes to standard output. Splitting is
  allowed (in consecutive chunks or round robin, outputs joined in order) unless `-z` is present. They answer
  every line, including lines they were never tested on. D only calls the same three rules in a different
  order. A checks only `-z` and not `--zero-terminated` in its splitting class, while C, D and F check both.
  That difference does not show up in any decision-table group (see check 7).
- **R.** Uses the same general input/output rules as A, C, D and F, and allows splitting on every line,
  with no exception for `-z`.
- **B.** A list of four exact situations: no operands, with the option set exactly `{-d,-f}`, `{-b}`, `{-c}` or
  `{-f}`. For those it answers "reads standard input, writes standard output" and allows splitting.
  Everything else falls through to `self.input_output_info = None` (no answer). Any line it was not tested
  on that does not match one of the four sets gets no answer.
- **E.** A longer list of exact situations (no operands or one operand, specific option pairs), with
  `--help`/`--version` handled separately. It also falls through to no answer for anything else. Splitting
  is allowed for a smaller list of option sets, and only when there are no operands.

## 2. Input/output sets

**Difference 1: no answer (B, E) versus an answer (A, C, D, F, R).** This covers almost every group.

- On normal lines with a file, E is right and B gives nothing. In group "102 lines" (`cut -f 2
  IN/bio/Gene_locs.txt`), A, C, D, E, F and R all say "reads operand 1, writes stdout", which is what cut does.
  B gives no answer.
- On lines with a value written straight after its option (group "996 lines": `cut -d ' ' -f1`, `cut -b-32`;
  group "725 lines": `cut -d= -f1`), A, C, D, F and R say "reads operand 1" (and operand 2). The only words
  there are `-f1`, `-b-32` and `-d=`. So these sides are saying cut reads a *file* named `-f1`, and that it
  does not read standard input. Real cut reads standard input on these lines. All five sides that answer
  agree here, and their own rule ("operands are read") is right. The wrong answer comes from PaSh's parser
  leaving attached values as operands (section 4). B and E give no answer, which is safe but useless. 17 of
  the 46 benchmark lines fall in these two groups. That is why A, C, D, F and R are rated `medium` rather
  than `high` for correctness.
- On lines that make cut stop with an error (group "997 lines": `cut`, `cut -s`, `cut -c 1 -s`), real cut
  reads nothing, prints an error and exits with status 1 (no byte/character/field list given, or `-s` used
  without `-f`). A, C, D, F and R say "reads stdin, writes stdout". B and E give no answer. Neither answer
  matches exactly, but no answer is the closer one (checks 5 and 6).

**Difference 2: `--help` / `--version` (groups "47 lines", "4 lines", "2 lines").** E says "reads nothing,
writes stdout" for `cut --help`, `cut -c 1 --help` and `cut --help relpath_1`. A, C, D, F and R say "reads
stdin" or "reads operand 1". E matches the real command: GNU cut prints help or version text and exits
before it opens any input (check 2). These are of type `standard input differs` (no operand) and `operand used
by one side only` (`relpath_1` is a file to A, C, D, F and R, and a plain word to E). B gives no answer.

Apart from these, all sides that give an answer give the same one, for example group "77 lines" (`cut -c 1-12`):
everyone says stdin to stdout.

## 3. Splitting

- **R splits under `-z` (groups "962", "485", "458", "33 (-z)", "4", "2").** This is unsafe. PaSh splits the
  input at newlines, but with `-z` a record ends at a NUL byte and can contain newlines. When the input is cut
  at a newline inside a record, that record becomes two records. Each half gets its own field numbering, and
  the first half gets an extra NUL added. Example: the input `a:b\nc:d\0` with `cut -z -d: -f2` gives `b\nc\0`
  when run whole, and `b\n\0d\0` when run as two chunks (check 1). A, C, D, E and F all refuse to split under `-z`.
  That is the right call.
- **A, C, D, F allow splitting everywhere else.** cut works on each line separately, so this is safe for
  `-b/-c/-f`, `-s`, `-n`, `--complement` and `--output-delimiter`. One small exception, which R shares: on
  `cut --help` (group "47 lines") they treat stdin as an input that may be split. Running `--help` once per
  chunk would print the help text several times. Nobody pipes data into `cut --help`, so it hardly matters.
- **B** splits only on its four exact option sets with no operands. That is safe, but covers very little.
- **E** splits only with no operands, and only for its listed sets. It leaves safe speed unused:
  - With a file operand (group "102 lines", `cut -f 2 IN/bio/Gene_locs.txt`, 2 benchmark lines) it answers
    "no split".
  - It allows `{--complement,-f}` but not `{--complement,-b}` or `{--complement,-c}` (group "33 lines
    (--complement)", `cut -c 1 --complement`, no split).
  - It does not allow `{-f,-s}`, although `-s` is safe to split.
- No side's class breaks PaSh's round-robin rule: everyone pairs round robin with joining outputs in order.

## 4. Parser table

- **A, C, D, F** have the same table, and it covers GNU cut's options as I know them. The value types (LIST,
  DELIM, STRING) are all non-file, so they do not change any input/output answer.
- **R** is the same plus a `-M` flag. I don't know a `-M` in GNU cut. It does no harm, but it should be checked
  (check 4).
- **E** lists the same options plus a `-w` flag. `-w` is a BSD cut option (split on whitespace). I am not sure
  whether the GNU version tested has it (check 3). Line `cut -w --output-delimiter ,` (group "450 lines") shows
  the sides without `-w` reading `-w`, `--output-delimiter` and `,` as three input files.
- **B** has no flags at all (`-s`, `-z`, `-n`, `--complement`, `--help`, `--version` are missing) and no
  `--output-delimiter`. So a line like `cut -s -d: -f1 file` can never match one of its option sets, and the gap
  shows up as no answer rather than a wrong one.
- **Shared by every side (PaSh's parser, not the tables).** Attached values (`-f1`, `-d:`, `-b-32`) and
  `--opt=value` forms (`--delimiter=: --fields=1-2`, group "450 lines") come back as operands. Option words
  after the first operand are also counted as operands (group "682 lines", `cut -d: -s -f1 c1.txt` → 4
  operands; group "740 lines", where `-n` and `--output-delimiter` are counted as files). Every side that uses
  "operands are read" therefore reports option words as input files. PaSh would try to open or split a "file"
  called `-d:` (check 8). The format has no way to express attached values, so no side could have fixed this
  in its table.

## 5. Completeness

- **B and E** give no answer outside the exact option sets they listed. This is a limit of their method: they
  only answer situations they saw. E answers more than B: `-n`, `-z`, `--complement` and `--output-delimiter`
  pairs, one-operand lines, and help/version. Both miss all benchmark lines except groups "77" and (E only) "102".
- **A, C, D, F, R** answer every line. What they leave out is a choice: there is no special case for
  `--help`/`--version`, and lines that end in an error are not treated as reading nothing.
- **R** leaves out any rule for `-z` in splitting. That looks like an oversight, not a limit of its method.

## 6. Checks to run

1. `printf 'a:b\nc:d\0' | cut -z -d: -f2 | od -c` versus
   `{ printf 'a:b\n' | cut -z -d: -f2; printf 'c:d\0' | cut -z -d: -f2; } | od -c`.
   R predicts the two are the same (splitting is safe). A, C, D, E and F refuse to split. I expect the outputs
   to differ.
2. `strace -f -e trace=openat,read cut --help relpath_1 < /dev/null`. E predicts nothing is opened or read.
   A, C, D, F and R predict `relpath_1` is read.
3. `cut -w -f1 </dev/null; echo $?`. Tells whether E's `-w` flag exists in the GNU version used.
4. `cut -M -f1 </dev/null; echo $?`. Tells whether R's `-M` flag exists.
5. `echo x | cut -c 1 -s; echo $?`. I expect an error and status 1, so the command reads nothing. A, C, D, F
   and R predict a normal read of stdin. B and E give no answer.
6. `echo x | cut; echo $?`. Same as check 5, for a line with no list at all.
7. In PaSh, the parallelizability decision for `cut --zero-terminated -f1` under A. If PaSh's parser maps
   `--zero-terminated` to `-z`, A refuses to split (same as C, D, F). If not, A allows an unsafe split.
8. In PaSh, the operand list for `cut -d: -f2` and for `cut -b1 -n --output-delimiter -- f -`. This confirms
   that attached values and later option words come back as operands, for every side.

## 7. Summary

A, C, D and F are one general annotation with the same answers everywhere. It answers every line, uses the
right input/output rules, and refuses splitting under `-z`. Its main faults are inherited from PaSh's parser:
attached values such as `-f1` are counted as files. R is the same except that it splits under `-z`, which can
change the output. B and E are lists of tested situations that give no answer on most lines, including 17 of
the 46 benchmark lines. E is the only side that gets `--help`/`--version` right.

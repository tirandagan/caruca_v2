---
command: cut
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[B, C, D, F], [R], [A], [E]]
ratings:
  A:
    io_correct: high
    io_complete: low
    split_safe: safe
    split_coverage: low
    parser_table: good
    confidence: high
  B:
    io_correct: medium
    io_complete: high
    split_safe: safe
    split_coverage: high
    parser_table: good
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
    confidence: medium
  E:
    io_correct: high
    io_complete: low
    split_safe: safe
    split_coverage: low
    parser_table: gaps
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
io_difference_types: [operand used by one side only, standard input differs, no answer from one side]
needs_running: 6
---

# cut: assessment (rubric 1)

## 1. How each side is built

- **B, C, D, F** (one group; same answer on every decision-table group). General rules: every operand is
  a file read as a stream, standard input is read when there are no operands, standard output is always
  written. Splitting is allowed on every line except those with `-z` (B, C, F test `-z` and
  `--zero-terminated`; D tests only `-z`). There is no list of cases, so every line gets an answer,
  including lines nobody tested.
- **R**. The same input/output rules as B–F. Splitting is allowed on every line, `-z` included.
- **A**. A list of specific situations: an answer only for given operand counts (0 or 1) combined with
  given flag sets, such as `{-d, -f}` or `{-c, -n}`. Anything else gets `self.input_output_info = None`.
  It is the only side that treats `--help`/`--version` as reading nothing. It allows splitting only for
  a smaller list of flag sets, and only with no operands. Lines it never saw get no answer.
- **E**. A list of four situations: no operands and flags exactly `{-d, -f}`, `{-b}`, `{-c}` or `{-f}`.
  Everything else gets no answer. There is no catch-all, so almost every untested line is unanswered.

## 2. Input/output sets

1. **Words joined to their option (`-d:`, `-f1`, `-b-32`, `-d=`) are read as files by B–F and R; A and E
   give no answer.** Groups "996 lines" (`cut -b-32`, `cut -d ' ' -f1`, `cut -d '"' -f3`), "725 lines"
   (`cut -d= -f1`, `cut '-d ' -f1`), "450 lines" (`cut -d: -f-1 c1.txt`), "785 lines"
   (`cut -d: -f2 c1.txt - c2.txt`). On `cut -d ' ' -f1` the only word left over after `-d ' '` is
   `-f1`, and B–F and R say "reads operand 1", so they claim cut reads a file named `-f1`. Real cut reads
   standard input there: `-f1` is the field list. These forms are common in practice: 17 of the 46
   benchmark lines fall in the 996 and 725 groups. The word is left as an operand by PaSh's command-line
   reader, which all sides share, but B–F and R then mark *every* operand as a file. A and E only answer
   for shapes they recognise, so they decline. Declining is the safer answer; neither side gives the
   true one (reads stdin, writes stdout). Types: *operand used by one side only*,
   *no answer from one side*.
2. **`--help` and `--version`.** Groups "47 lines" (`cut --help`, `cut -c 1 --help`), "4 lines"
   (`cut --help relpath_1`), "2 lines" (`cut -z --help`). A: reads nothing, operand is a plain word,
   writes stdout. B–F and R: read stdin, or read operand 1. Real cut prints usage and exits without
   reading any input or file, so **A is right**. Types: *standard input differs*,
   *operand used by one side only*.
3. **Ordinary lines that A or E do not list.** Group "997 lines" (`cut -c 1 -s`), group "104 lines"
   (`cut -c 1 -n`, E only), group "102 lines" (`cut -f 2 IN/bio/Gene_locs.txt`, E only), and from A's
   code `cut -d ' ' -f 2 file` (one operand with flags `{-d, -f}` is not in A's list). B–F and R give
   the right answer (reads stdin or the file, writes stdout); A and/or E give none. Type:
   *no answer from one side*.
4. **Lines that are errors in real cut**, such as `cut`, `cut -s` and `cut -z relpath_1` (no list
   given). B–F and R answer "reads stdin" or "reads operand 1"; A and E decline. Real cut exits with an
   error, so neither answer matters much.
5. **Agreement.** Group "77 lines" (`cut -c 1-12`, 27 benchmark lines): every side reads stdin and
   writes stdout. B–F and R are the same everywhere; the only difference among B, C, D, F is the
   `--zero-terminated` spelling in D's splitting check (section 3).

## 3. Splitting

- **R splits `-z` lines** (groups "962", "485", "458", "33 `cut -c 1 -z`", "4", "2"). This is unsafe.
  PaSh cuts its input at newlines, but with `-z` cut's records end at NUL bytes and may contain
  newlines. Splitting `ab\ncd\0` at the newline gives two records, so `cut -z -c1` prints `a\0c\0`
  instead of `a\0`. Cut also adds a NUL after a last record that has none, so each chunk boundary can
  add an extra NUL. B–F refuse to split on `-z`, which is correct.
- **B–F and R** otherwise split everywhere with consecutive chunks or round robin, both merged by joining
  outputs in order. Cut works one line at a time (`-s`, `--complement`, `-n` and `--output-delimiter`
  included), so this is safe. One edge case: they also split `cut --help` reading stdin (group 47), which
  would print the usage once per chunk. Nobody pipes data into `cut --help`, so this is a side effect of
  item 2 above, not a real-world risk.
- **A** splits only with no operands and a short list of flag sets. It leaves safe speed unused on
  `cut -f 2 IN/bio/Gene_locs.txt` (group 102, a benchmark line), on `cut -c 1 --complement` (group
  "33 --complement"), and on everything with `-s`. It refuses `-z`, which is correct.
- **E** splits only on its four listed shapes; everything else gets no split. Safe, very little coverage.
- No class breaks PaSh's round-robin rule: all use the joining merge, and no group shows "exception".

## 4. Parser table

- **B, C, D, F**: every GNU cut flag and option, typed correctly. **R**: the same plus `-M`, which as far
  as I know is not a GNU cut option. It does no harm unless a line actually contains `-M` (check 6).
- **A**: the same set, and also `-w` as a flag. `-w` (split fields on whitespace) is a BSD cut option; I
  am not sure whether the GNU version under test has it (check 5). If it does, the other sides read
  `cut -w -f2` with `-w` as an operand, which B–F and R would then mark as a file read. The 450-line
  group (`cut -w --output-delimiter ,`) shows A giving no answer anyway.
- **E**: options `-b -c -d -f` only. No flags at all (`-s`, `-z`, `-n`, `--complement`, `--help`,
  `--version`) and no `--output-delimiter`. So `cut -c 1 -n` has `-n` as an operand (group 104: E gives no
  answer where every other side answers). Because E's input/output class declines on anything it doesn't
  recognise, the gaps cost answers but do not produce wrong ones.
- No table can fix item 2.1: words joined to their option (`-d:`) are left as operands by the shared
  command-line reader, whatever the table says.

## 5. Completeness

- **A**: answers only the operand counts and flag sets it saw (0 or 1 operands). Lines with two or more
  files, `-d … -f … file`, or `-s` with a list get nothing. This is a limit of its method. Its declines
  on joined-value words happen to be the prudent result.
- **E**: answers only four shapes. Also a limit of its method, and narrower than A. It covers 27 of the
  46 benchmark lines, against A's 29.
- **B–F, R**: nothing left unanswered. The cost is wrong answers where the reader gives them bad
  operands (joined values, `--help`). That is a choice: general rules with no exceptions.
- **R** leaves out the `-z` exception, which looks like an oversight, not a method limit.

## 6. Checks to run

1. `printf 'ab\ncd\0' | cut -z -c1 | od -c` against
   `{ printf 'ab\n' | cut -z -c1; printf 'cd\0' | cut -z -c1; } | od -c`.
   R predicts the same output (splitting is safe). B–F predict different output. Expected: `a \0`
   against `a \0 c \0`.
2. `strace -f -e trace=openat,read cut --help < /etc/passwd > /dev/null` and
   `strace -e trace=openat cut --help relpath_1`. A predicts no read of stdin and no open of `relpath_1`.
   B–F and R predict both are read.
3. `echo 'a b' | cut -d ' ' -f1`, and run PaSh's command-line reader on the same line to confirm operand 1
   is `-f1`. B–F and R predict cut reads a file `-f1`; real cut should print `a` from stdin and open no
   such file.
4. Run D's and B's splitting classes on `cut --zero-terminated -c1 f` through PaSh. If PaSh turns long
   flag names into their short form, D and B agree (no split). Otherwise D allows an unsafe split.
5. `printf 'a  b\n' | cut -w -f2` on the target GNU coreutils version. A predicts `-w` is a flag; the
   other sides read it as an operand (a file).
6. `cut -M -c1 < /dev/null`. R lists `-M` as a flag; GNU cut is expected to reject it as an invalid
   option.

## 7. Summary

B, C, D, F and R share broad, general input/output rules that answer every line but read option words
joined to their value (`-d:`, `-f1`, used in 17 of 46 benchmark lines) and `--help` as files read. A and
E answer only the shapes they saw: right when they answer, but often silent. R alone splits `-z` lines,
which is unsafe because records can contain newlines. B–F avoid that, and A gives up safe splits on files
and on `--complement`.

---
command: cat
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[A], [B], [R]]
ratings:
  A:
    io_correct: medium
    io_complete: low
    split_safe: safe
    split_coverage: medium
    parser_table: wrong
    confidence: high
  B:
    io_correct: high
    io_complete: high
    split_safe: unsafe
    split_coverage: high
    parser_table: good
    confidence: medium
  R:
    io_correct: high
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: good
    confidence: high
io_difference_types: [operand used by one side only, standard input differs]
needs_running: 5
---

# cat: assessment

B and R give the same input/output answer on every line. Their input/output classes are identical code:
standard output always, standard input when there are no operands, every operand a file read. They
differ only in splitting, because R has no splitting class. So no two sides match on every group.

## 1. How each side is built

- **A** is a list of exact situations: no operand or one operand, with no flag or `-n` only. Everything
  else gets "no answer" (`self.input_output_info = None`). Its parser table knows only `-n`/`--number`,
  so any other flag is read as an operand. On untested lines, it gives no answer in most cases, and a
  wrong answer when a lone unknown flag becomes the single operand (see section 2).
- **B** uses one general rule for input/output with no exceptions, so it answers any line. For
  splitting it has rules by flag: no split with `-b`; a line-number mapper with `-n`; a merge of
  adjacent lines with `-s`; plain concatenation (including per-file splitting) otherwise.
- **R** has the same general input/output rule as B and no splitting class, so PaSh never splits `cat`
  under R.

## 2. Input/output sets

- **`cat -s`** (no file). A reads "operand 1": the word `-s` is taken as a file name, because A's parser
  table lacks `-s`. B and R read standard input. **B and R are right**: GNU `cat -s` squeezes blank lines
  read from standard input (check 5). The same error hits any lone flag A does not know (`cat -A`,
  `cat -v`, `cat -E`), which are common at the end of a pipeline. Types: operand used by one side only,
  standard input differs.
- **Lines A refuses but B and R answer** (`cat -A f`, `-e`, `-E`, `-s f`, `-b f`, `cat IN1 temp IN2`,
  `cat a1 b1 c1 d1 e1 f1`, `cat -n f g`, `cat f - g`). A gives no answer. B and R read every operand
  and write standard output. **B and R are right.** These are completeness gaps in A, not
  disagreements about direction.
- **Lines all sides read wrongly or refuse** (group `cat -- -n`, `cat -x f`, `cat f -n`, `cat --num f`).
  B and R say it reads two files.
  - In GNU cat, `cat f -n` numbers `f`, because options may come after operands.
  - `cat --num f` is an accepted short form of `--number`.
  - `cat -x f` is an invalid-option error.
  - `cat -- -n` reads only the file `-n`. B and R count two operands, which suggests the parser kept
    `--` as an operand.

  So B and R are wrong on these four lines, a limit of PaSh's parser shared by both (checks 3, 4). A's
  "no answer" is safe here.
- Everywhere else (one file, standard input, `cat -n f`, `cat -n`) all three agree and are right.

## 3. Splitting

- **R:** never splits. Safe, but it leaves unused the easy safe case: plain `cat f` (83 lines, most of
  them benchmark lines) and every per-line flag.
- **A:** splits only plain `cat` and `cat f` with consecutive chunks and round robin, both followed by
  concatenation. This is safe. The one bad case, `cat -s`, comes from the misread operand (section 2),
  not from the split rule.
- **B, plain and per-line flags** (`-A -e -E -T -t -v -u`, and many files): consecutive chunks, per-file
  splitting and round robin, all concatenated. This is safe, since these flags change each line on its
  own.
- **B with `-n`** (`cat -n f`, `cat -n`, `cat -n f g`): it adds splits with a mapper that it itself marks
  not implemented (`cat_add_line_number_offset`, `is_implemented=False`). Unlike other classes of its
  kind, it does not test `is_implemented` before appending, and the table lists the split. If PaSh then
  runs plain `cat -n` on each chunk, the numbers restart in every chunk. **Unsafe**, unless PaSh throws
  away splits whose mapper is not implemented (check 1).
- **B with `-s`**: concatenation is replaced by `ADJ_LINES_SEQ`. This is right only if that merge step
  squeezes just a pair of blank lines at a chunk edge and leaves repeated non-blank lines alone. I do not
  know its exact behaviour (check 2).
- No side breaks PaSh's round-robin rule: B's `-s` round robin uses an `adj_lines_*` step, which is
  allowed.

## 4. Parser table

- **A:** only `-n`/`--number`. It misses `-A -b -e -E -s -t -T -u -v`, `--help`, `--version` and the
  long forms. Example: `cat -s` is read as a file named `-s`.
- **B:** every GNU cat flag. It does not list R's aliases `-vE` and `-vT`, but those are just combined
  short flags (`-v` plus `-E`), so this changes nothing if the parser splits combined flags. The table
  does not distinguish the two.
- **R:** the same as B, plus `-vE` → `-e` and `-vT` → `-t`.
- Neither B nor R can handle options placed after operands, or shortened long options (`cat f -n`,
  `--num`). That is the parser's limit, not the tables'.

## 5. Completeness

- **A** answers only the situations it saw: up to one file, with no flag or `-n` only. Multi-file
  `cat`, a very common benchmark form, gets no answer. This is a limit of its method.
- **R** gives no splitting at all. That is a choice, or an unfinished annotation, since its
  input/output class and parser table are complete.
- **B** is complete on both. Its only gaps are the shared parser limits in section 2.

## 6. Checks to run

1. `seq 1 100000 > f; cat -n f` alone and under PaSh with side B, width 2. B predicts the same output.
   The risk is that the numbers restart in the second chunk, or that PaSh rejects the unimplemented
   mapper and does not split.
2. A file with a blank line on each side of a chunk edge, and with a repeated non-blank line on the
   edge: `cat -s f` alone and under PaSh with B, width 2. B predicts the same output.
3. `printf 'x\n' > f; cat f -n`. B and R predict a read of a file named `-n`. GNU behaviour should be
   `     1	x`.
4. `cat --num f` and `cat -- -n` (with a file named `-n` present). B and R predict two files read. GNU
   should number `f`, and in the second case read only `-n`.
5. `printf 'a\n\n\nb\n' | cat -s`. B and R predict standard input is read, giving `a`, one blank line,
   `b`. A predicts a file named `-s` is read.

## 7. Summary

B and R share a correct, general input/output rule and a complete parser table. They differ only in
that R never splits, while B splits widely, safely for plain and per-line flags but questionably for
`-n` (an unimplemented mapper used without a check) and `-s`. A is a short list of tested cases with a
one-flag parser table: it gives no answer for multi-file `cat` and any flag but `-n`, and it misreads a
lone unknown flag such as `cat -s` as a file, though where it does split, it splits safely.

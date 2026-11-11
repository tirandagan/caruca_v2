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
    io_correct: high
    io_complete: high
    split_safe: broken
    split_coverage: low
    parser_table: wrong
    confidence: high
  C:
    io_correct: low
    io_complete: low
    split_safe: unsafe
    split_coverage: low
    parser_table: wrong
    confidence: high
  D:
    io_correct: medium
    io_complete: low
    split_safe: unsafe
    split_coverage: low
    parser_table: gaps
    confidence: high
  E:
    io_correct: high
    io_complete: high
    split_safe: broken
    split_coverage: low
    parser_table: gaps
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
io_difference_types:
  - no answer from one side
  - standard input differs
  - standard output differs
  - operand used by one side only
  - option value typed differently
  - kind only
needs_running: 14
---

# sort: assessment

No two sides give the same answers on every group, so every side stands alone. On read/written answers,
A, B, E, F and R agree on nearly every line. They differ mainly on how splitting is handled.

## 1. How each side is built

- **A, B, E, F, R** use general rules that cover any command line. Operands are read as input, standard input
  is read when there are no operands, standard output is written unless `-o` (or `-c`/`-C`) is given, and
  `--files0-from` is a special case. They have no catch-all "no answer" branch, so untested lines still get a
  reasonable answer. Their parallelizability classes are also rules: a list of flags that block splitting,
  then consecutive chunks recombined by a `sort -m` built from the line's own ordering flags.
  - A, B and E also add a **round-robin** split with that custom merge whenever `-s`/`-u` is absent
    (A lines 60-61, B lines 287-290, E lines 722-724). That breaks PaSh's rule.
  - F (line 939) and R add consecutive chunks only.
- **C** lists specific situations: no flags or only `-m`, with 0 or 1 operands. Everything else is
  `self.input_output_info = None`. Its parser table knows only `-m`, so any other flag word is read as a
  file name. It has no useful answer outside the handful of shapes it saw.
- **D** also lists specific situations: about 300 hard-coded flag sets for 0 or 1 operands. Everything else
  gets `None`, including any line with 2 or more operands. Its split list is another enumeration of flag
  sets, recombined with `concatenate`. Lines it was not tested on mostly get no answer.

## 2. Input/output sets

1. **No answer at all (C, D).** C gives no answer on almost every group. D gives no answer on any line with
   two or more operands, which includes benchmark lines (group "348 lines":
   `sort OUT/input1.types OUT/input2.types OUT/input2.types`). D also gives none on:
   - plain `sort -c` / `sort -C` (group "3 lines": `sort -c`)
   - `-f -c` (group "51 lines")
   - every `--files0-from` line
   - every `--debug` line without `--help`
   - every `-S` line (group "21 lines": `sort -S 512M`, a benchmark line)

   The other five sides answer all of these.
2. **C reads flags as files.** C's table has only `-m`, so in `sort -rn`, `sort -f`, `sort -n` (group "12 lines",
   five benchmark lines) C says it "reads operand 1", meaning a file named `-rn`, and no standard input. The real
   command reads standard input. Every other side is right. The same happens for `sort -c`, `sort -R`, `sort -z`,
   `sort --version` and `sort --debug`. (Type: standard input differs; operand used by one side only.)
3. **`-o` and standard output (D versus the rest).** D's flag-set lists put `{'-o'}` in the "stdin + stdout"
   branch (D line 520), so on `sort -o relpath_1` (group "45 lines") and `sort -o in1 in1` D says it writes
   stdout *and* the `-o` file. GNU sort writes only the `-o` file. A, B, E, F and R are right. (Standard output differs.)
4. **`-c`/`-C` and standard output (R versus the rest).** R writes stdout unless `-o` (R line 1099), so on
   `sort -c relpath_1` (group "23 lines") and `sort -f -c` (group "51 lines") R says it writes stdout. GNU sort `-c` reports
   disorder on standard error and writes nothing to stdout. A, B, D, E and F are right. (Standard output differs.)
5. **`--help`/`--version` (D versus the rest).** On `sort --help`, `sort -f --version` (group "41 lines") and
   `sort --version relpath_1` (group "4 lines"), D says it reads nothing (it marks operands as plain words). The others
   say it reads stdin or operand 1. GNU sort prints and exits without reading input, so D is right. The others
   over-claim, which is harmless. (Standard input differs; operand used by one side only.)
6. **`--check=WHEN` spellings.**
   - On `sort --check=quiet in1` (group "6 lines"), A, B, E and R read `--check=quiet` as a second *file* and say
     it writes stdout.
   - D and F list `--check=quiet`/`--check=silent` as aliases of `-C` and correctly say it reads operand 1 and
     writes nothing.
   - On `--check=diagnose-first in1` (group "3 lines"), only F is right.

   (Operand used by one side only; standard output differs.)
7. **`--check FILE` (B versus the rest).** B types `--check` as an option that takes a value (B json lines 417-420).
   So on `sort --check s1` (group "2 lines") and `sort --debug --check /dev/null`, B takes the file as the value and
   says it reads stdin. In GNU `getopt_long` an optional value must be attached with `=`, so `s1` is the file
   being checked. A, D, E and F are right. On `sort --check quiet in1` (group "3 lines"), B reads only `in1`, while
   A, E and F read two operands, which matches getopt. (Standard input differs; option value typed differently.)
8. **`-y` (E, R versus A, B, F).** E and R have no `-y`. On `sort -y in1` (group "8 lines") they read a file named `-y`.
   GNU sort accepts `-y` and ignores it: a following word is swallowed only if it is all digits. So `sort -y in1`
   reads only `in1`, and A, B and F are right. On `sort -y 5 f1` nobody is fully right:
   - A, B and F read `5` as a file.
   - E and R read `-y`, `5` and `f1`.
   - GNU reads only `f1` (to confirm, see check 4).

   (Operand used by one side only.)
9. **`-T` and `--files0-from` typing (D versus the rest).** D types `-T` and `--files0-from` as `PATH_UNTRACED`.
   So on `sort -T relpath_1` (group "44 lines") D does not list the `-T` directory as written, while the others list it as
   output. sort does create temporary files there, so listing it is more accurate, but the difference is
   minor. (Option value typed differently.)
10. **`--random-source` kind (D versus the rest).** D types it as `STREAM_INPUT`, the others as `CONFIG_INPUT`. The direction
    is the same (group "42 lines"). (Kind only.)
11. **`--files0-from` with operands (F versus the rest).** F raises an exception (F line 909), so it gives no answer on
    `sort --files0-from relpath_1 relpath_2` (group "16 lines"). A, B, E and R say it reads both. GNU sort refuses
    this combination with an error, so F's refusal is arguably closer. Low stakes.
12. **Common to all parsing sides, not a difference.** Attached short-option values and bundles are read as
    operands: `sort -k1n` and `sort -nrk 1` (groups "43" and "348"), `sort -k1 -t, -oout4 -S1M -T/tmp f1`, and
    `-S=-1`. This is a limit of the PaSh parser, and every side shares it.

## 3. Splitting

- **A, B, E: broken.** On plain `sort`, `sort -n`, `sort -rn`, `sort -k 2n` and every other ordinary line
  (groups "348", "341", "169", "12", "1: sort"), these three raise an exception. They add round robin with a
  custom `sort -m` merge, which PaSh forbids. They only produce a working split when `-s` or `-u` is present
  (groups "44" and "30": `sort -u relpath_1`), and that split is consecutive chunks merged with `sort -m -u`/`-s`,
  which is safe.
  - **A** also uses an N-ary custom merge (check 13).
  - **A** does not block `-z`, so on `sort -s -z` (group "2 lines") it splits NUL-terminated records at newlines.
    That is unsafe.
  - **A** and **E** split `sort -o FILE -s` (group "4 lines"). See check 12.
- **F: safe, and the most useful.** It splits with consecutive chunks plus a `sort -m` that keeps all ordering
  flags and drops only resource options (F line 935). It never uses round robin, and it blocks `-c`, `-C`, `-m`,
  `-z`, `--debug`, `-o` and `--files0-from`. It splits `-s`/`-u` lines (group "44"), which is safe because a stable
  merge of sorted chunks reproduces the whole-input result. It also splits `-R --random-source FILE`
  (group "2 lines": `sort -R --random-source relpath_1`), which is safe only if the random source gives the
  same bytes to every process. `/dev/urandom` would not (check 11).
- **R: mostly safe, with real holes, and conservative where it need not be.**
  - It is the same as F on ordinary lines.
  - It refuses `-s`/`-u` (group "44"), which leaves safe speed unused.
  - It splits `--debug` lines (group "33 lines": `sort --debug relpath_1`). Its merge drops `--debug`, so the key
    underline lines that `--debug` adds would be merged as if they were data. That is unsafe (check 9).
  - It blocks `-R` but not `--sort=random` (R line 1117), so `sort --sort=random` would be split with independently
    seeded random merges (check 10).
  - It splits `-o` lines (group "45 lines"), which is risky (check 12).
  - It splits `--check=quiet in1` because its parser reads that word as a file name (group "6 lines").
- **C and D: unsafe.**
  - Both split `sort -m` on a single stream with `concatenate`. That is safe, because a merge of one stream just
    passes it through, but it gains little.
  - D also splits real sorts with `concatenate`. Its flag sets `{-n,-s}`, `{-n,-u}`, `{-M,-s}`, `{-k,-s}`, `{-g,-u}`,
    `{--random-source,-T}` and others (D line 544; groups "20 lines": `sort -n -s`, and "4 lines":
    `sort --random-source relpath_1 -T relpath_2`) all get this split. Concatenated sorted chunks are not sorted
    output (check 6).
  - C and D both split `sort -m -u` (group "2 lines": `sort -m -u`). A run of equal lines that crosses a chunk
    boundary would be printed twice (check 5).
  - C splits that line only because it reads `-u` as a file.

## 4. Parser table

- **C:** only `-m`. Every other flag is read as a file (`sort -rn` → reads file `-rn`, group "12 lines").
  Wrong.
- **B:** `--check` is typed as an option with a required value (`--check s1` → `s1` becomes the value, group
  "2 lines"), and `-c` is not linked to `--check`. Wrong.
- **A, E, R:** no `--check=quiet|silent|diagnose-first` (read as file names, group "6 lines"). E and R also lack
  `-y` (group "8 lines"). Gaps.
- **D:** lacks `-y`. It has the `--check=` aliases for `-C` only, not `--check=diagnose-first`. `-T` and
  `--files0-from` are untracked paths. Gaps.
- **F:** has `-y`, all `--check=` forms and all options. It only misses that `-y` swallows a following all-digit
  word. Good.

## 5. Completeness

- **C and D** leave out most of the command: multi-operand lines, `--files0-from`, `-S`, `--debug`, plain
  `-c`. This is a limit of their method: they answer only for flag-and-operand shapes they saw, with no
  general rule.
- **A, B, E, F, R** answer every line. Their gaps are choices or oversights: the `--check=` spellings, `-y`, and
  R's refusal to split `-s`/`-u`, which is a deliberate conservative choice. A, B and E's round robin is
  a design error that removes splitting from the common case. It is not a coverage gap.

## 6. Checks to run

1. `printf 'b\na\n' > u; sort -c u >out 2>err; wc -c out`. Expected: 0 bytes on stdout. R predicts stdout
   is written; the others predict nothing.
2. `sort --check=quiet in1`. Expected: checks `in1`, no output. A, B, E and R predict a read of a file named
   `--check=quiet` and output to stdout.
3. `sort --check s1`. Expected: checks `s1`. B predicts stdin is read with `s1` as the check mode.
4. `sort -y in1` and `sort -y 5 f1`. Expected: only `in1` and only `f1` are read. E and R predict that a file
   `-y` is read; A, B and F predict that a file `5` is read.
5. `printf 'x\nx\n' | sort -m -u` versus `{ printf 'x\n' | sort -m -u; printf 'x\n' | sort -m -u; }`.
   Expected: 1 line versus 2 lines, which shows that C and D's split of `-m -u` is unsafe.
6. `printf '3\n1\n4\n2\n' | sort -n -s` versus `{ printf '3\n1\n' | sort -n -s; printf '4\n2\n' | sort -n -s; }`.
   Expected: they differ, which shows that D's concatenate split is unsafe.
7. `sort --help </dev/tty`. Expected: returns at once without reading. D predicts nothing is read; the others
   predict stdin is read.
8. `sort -c -o x f2` and `sort -c in1 in2`. Expected: both exit with an error (incompatible options; extra
   operand). All sides predict normal reads.
9. Under PaSh with width 2: `sort --debug big` versus plain `sort --debug big`. Expected: R's split output differs.
10. Under PaSh: `sort --sort=random --random-source=/dev/zero big`, and with no random source. Expected: R's split
    breaks the grouping of equal keys when no fixed source is given.
11. Under PaSh: `sort -R --random-source=/dev/urandom big`. Expected: F's split gives each process a different
    hash, so equal lines are not kept together.
12. Under PaSh: `sort -o out big` (R) and `sort -o out -s big` (A, E). Check whether the split writes `out` once
    and correctly.
13. Under PaSh: A's `CUSTOM_N_ARY` aggregator on `sort -u big`. Check whether it is accepted and implemented.
14. `printf 'b\na\n' | sort -m`. Expected: `b` then `a` (pass-through), which confirms that C and D's
    single-stream `-m` split is safe when `-u` is absent.

## 7. Summary

F is the strongest side: general rules, a complete and correctly typed parser table, and a safe
consecutive-chunk split that also covers `-s`/`-u`. R is close on read/written answers but splits `--debug` (and
possibly `--sort=random` and `-o`) unsafely, while refusing safe `-s`/`-u` splits. A, B and E have good
read/written answers, but their round-robin custom merge raises an exception on every ordinary `sort` line, and C and D
answer only the narrow shapes they were tested on, misread most flags (C) or split real sorts with plain
concatenation (D).

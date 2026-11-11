---
command: split
rubric: 1
assessor_model: claude-opus-5-5
date: 2026-11-11
equivalent_groups: [[A], [B]]
ratings:
  A:
    io_correct: high
    io_complete: high
    split_safe: none_offered
    split_coverage: none
    parser_table: good
    confidence: high
  B:
    io_correct: low
    io_complete: low
    split_safe: none_offered
    split_coverage: none
    parser_table: wrong
    confidence: high
io_difference_types: [standard input differs, standard output differs, operand used by one side only, option value typed differently]
needs_running: 7
---

# split — assessment

There is no side R for `split`.

Real GNU `split [OPTION]... [FILE [PREFIX]]`: reads FILE, or standard input when FILE is missing or `-`;
writes files named PREFIX plus a suffix (`xaa`, `xab`… when PREFIX is missing); with `-n K/N`, `-n l/K/N`
or `-n r/K/N` it writes only chunk K to standard output and creates no files; `--verbose` reports each
file it creates. PaSh cannot name the suffixed files, so "PREFIX is written" is the closest it can say.

## 1. How each side is built

- **A**: general rules for any line. 0 operands: standard input; 1 or 2 operands: the first is a stream
  input, the second (PREFIX) a written file; `-n` values of the K/N forms switch to standard output and
  make PREFIX a plain word; `--verbose` adds standard output. It raises on more than two operands, on
  more than one `-n`, and on `--filter` with a chunk to standard output: rules taken from `split`'s own
  error cases.
- **B**: a list of specific situations. It answers only when the flags are a subset of `{-d, -n}` and
  there are 0, 1 or 2 operands; everything else is no answer. In all its cases it marks standard input
  as read, and it treats operand 2 as a plain word.

## 2. Input/output sets

1. **Standard input read when a file is given** (27 lines, `split string`, `split relpath_1`; 27 lines,
   `split relpath_1 string`; 11 lines, `split -n 2/3 in.txt`; 2 lines, `split -n 2 -n 1/2 in.txt pp_`).
   B: standard input read as well as operand 1. A: operand 1 only. Real `split` reads standard input only
   when FILE is missing or `-`. **A matches.** Type: *standard input differs*.
2. **PREFIX** (27 lines, `split relpath_1 string`). A: operand 2 written. B: operand 2 a plain word,
   nothing written. Real: files `stringaa`, `stringab`… are created. Neither can name them, but A's
   "operand 2 written" records that output exists and where; B records no output at all, which is
   wrong. **A is closer.** Type: *operand used by one side only*.
3. **Chunk to standard output** (11 lines, e.g. `split -n 2/3 in.txt`, `split -n r/1/3 in.txt zz_`).
   A: standard output written, PREFIX a plain word. B: standard input read, nothing written. Real: chunk
   K goes to standard output, no files. **A matches**; B misses the only output. Type: *standard output
   differs*.
4. **Options B's table does not know** (2 lines, `split -l 5`, `split -l 2`). A: reads standard input.
   B: reads operand 1 (a file called `-l`) and standard input, because its table lacks `-l` and so `-l`
   and `5` become two operands. Real: standard input read, `-l 5` an option. **A matches.** Type:
   *option value typed differently*.
5. **`--verbose`** (4 + 4 lines, e.g. `split --verbose in.txt p_`). A: standard output added. B: no
   answer. I believe `--verbose` writes "creating file …" to standard output; check to run.
6. **Lines where both fall back** (22 lines, e.g. `split -dn N IN` (a benchmark line), `split -3 in.txt
   p_`, `split -l 4 --numeric-suffixes=7 in.txt n_`). A: exception; B: no answer. In both cases PaSh gets
   nothing. For A the cause is that the reader leaves `-dn`, the old `-3` form and the `=`-attached value
   as extra operands, so A's "more than two operands" rule fires. Real `split -dn N IN` reads `IN` and
   writes `x00`, `x01`…; a lost benchmark line for both.
7. **Same on both, but incomplete** (8 lines, `split`, `split -n 1`): standard input read, nothing
   written. Real `split` writes `xaa`, `xab`…; neither side records any written file when PREFIX is
   missing (also true of A on `split string`). A limit of what PaSh can name rather than a side's error.

Other things A gets right: `split -l 4 --numeric-suffixes 7 in.txt` (49-line group) reads "7" and writes
"in.txt". That looks odd but matches GNU `split`, where `--numeric-suffixes` takes an optional value that
must be attached with `=`, so `7` really is FILE (check to run). Lines that are errors in real `split`
(`split -l 2 -b 3 in.txt`, `split -l 0 in.txt`, 6-line group) get "reads operand 1" from A, a harmless
over-claim.

## 3. Splitting

Both return an empty list: never split. That is right: the names and contents of the output files depend
on where each chunk starts in the whole input, so dividing the input between copies would change the
result. No safe speed left unused, no rule broken.

## 4. Parser table

- **A**: lists the GNU flags (`-d`, `-x`, `-e`, `-u`, `--verbose`, `--help`, `--version`) and the
  value-taking options (`-a`, `--additional-suffix`, `-b`, `-C`, `--filter`, `-l`, `-n`, `-t`). Typing
  `-d/--numeric-suffixes` and `-x/--hex-suffixes` as flags matches GNU, where the long forms take only an
  attached value. Not covered: the old `-NUMBER` form (`split -3 in.txt p_`), which the table format
  probably cannot express.
- **B**: lists only `-d` and `-n`. Missing `-l`, `-b`, `-a`, `-C`, `-e`, `-x`, `--verbose`,
  `--filter` and the rest. Every missing option is read as a file: `split -l 5` is read as "split the file
  `-l` with prefix `5`".

## 5. Completeness

- **A**: answers 138 of 162 lines. The 24 it refuses are the 22 misread lines above plus two lines with
  `-n` given twice (a deliberate choice; whether GNU `split` accepts that is a check to run). It never
  handles `--filter` as running a command, which can write anything; that is a choice it did not make
  explicit.
- **B**: answers 77 of 162 lines, only those with flags in `{-d, -n}`, and no answer on the one benchmark
  line. Most of its answers are wrong on standard input, output files or standard output. A limit of its
  method (only situations it saw), made worse by its small table.

## 6. Checks to run

1. `split in.txt p_; ls p_*` — expected `p_aa`, `p_ab`…, no file `p_`. A: `p_` written. B: nothing
   written.
2. `strace -e trace=read split in.txt p_ < /dev/zero` — expected no read from standard input (fd 0). B
   says standard input is read; A says not.
3. `split -n 2/3 in.txt; ls x*` — expected chunk 2 on standard output, no files. A: standard output. B:
   nothing written.
4. `split --verbose in.txt p_ > out; cat out` — is "creating file …" on standard output? A says yes.
5. `split -n 2 -n 1/2 in.txt pp_` — error, or does the last `-n` win? A raises; B answers.
6. `split -l 4 --numeric-suffixes 7 in.txt` — expected error "cannot open '7'", confirming `7` is FILE.
   A: reads `7`, writes `in.txt`.
7. `split -dn N IN` through PaSh's parser — confirm it yields three operands (why A raises); real
   `split -dn 2 IN` reads `IN` and writes `x00`, `x01`.

## 7. Summary

A is a general, carefully reasoned annotation: it gets standard input, standard output for `-n K/N` and
`--verbose`, and the prefix right, and refuses only on lines the reader leaves with too many operands. B
answers only for `-d`/`-n`, wrongly marks standard input as read whenever a file is given, records no
output files and misses the standard-output chunk, and its two-entry table turns `-l 5` into file names.
Neither side splits, which is right for `split`, and neither can name the suffixed output files when no
prefix is given.

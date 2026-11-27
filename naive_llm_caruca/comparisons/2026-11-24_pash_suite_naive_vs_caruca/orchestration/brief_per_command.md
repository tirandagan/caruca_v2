# Brief: the naive LLM against PaSh's own files, command by command (2026-11-26)

You are a worker. Work in `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`. Write a new
script `per_command.py` (Python 3, stdlib only; run it with `python3 -I per_command.py`) that reads the records
in `full_run/` and writes `per_command.md` and `per_command.json` in the folder. Do not edit any other file.
Do not commit.

## Why

Tiran asks: the naive LLM wrote annotation files for 82 of the commands the suite uses; PaSh's own package
has files for 30. Compare the two, command by command, on every metric the runs recorded, so one can see for
each command whether the naive LLM's file did as well as PaSh's own, better, or worse, and what the naive LLM
adds for the commands PaSh's own files do not cover.

## Records (gzipped JSON lines; read with gzip + json)

- `full_run/occurrences.jsonl.gz`: one row per command use in a part, per run. Fields you need: `command`,
  `set` (annotation set: `pash-own`, `naive`, `naive-sed2`, `caruca-pash`, `caruca-main`, `pash-own-copy`,
  `bash`), `source` (`ours` = the set's own file, `pash-own` = PaSh's own file used because the set has none,
  `none`), `split` (did PaSh split this use), `why_not_split`, `file_answer` and `direct_file_answer` (what the
  file said when asked), `exception` (the file raised), `phase`, `mode` (`instrumented` rows carry the split
  evidence; use `phase == "main"` and `mode == "instrumented"` for counts), `region_text_sha` (identifies the
  part), `script`, `group`, `repeat`, `copies`, `executions`.
- `full_run/regions.jsonl.gz`: one row per part per run: `outcome` (`parallelized`, `missing annotation`,
  `pash crash`, `refused by annotation`, `annotation raised`, `unsupported construct`, `other`), `reason`,
  `commands`, `split_commands`, `text_sha`.
- `full_run/commands.jsonl.gz`: one row per script, command, set: `source`.
- `full_run/answers/*.jsonl.gz`: each set's direct answer per command line (`allows_split`, `io_outcome`,
  `parallelizability_outcome`, `exception`).
- Apply the same two fix-ups the counting uses (see `full_run/numbers.md` top and `prep_full_records.py`):
  compare against the same repeat's bash row; leave out the seven web-search rows without `node`. For the
  per-command counts only the instrumented main-phase rows matter, which are unaffected.

## Output: `per_command.md`

Section 1, a table with one row per command used inside a part (sorted by uses, descending), columns:
command · naive LLM has a file (yes/no) · PaSh's own has a file (yes/no) · uses in parts · uses split with
PaSh's own files · uses split with the naive LLM's files · uses where the naive file said "no split" · uses
where the naive file raised an error · uses where PaSh's own file said "no split" · parts where the naive file
made PaSh's compiler stop and PaSh's own did not (and the reverse) · verdict: `same`, `naive splits more`,
`naive splits less`, `naive only` (PaSh's own has no file), `neither splits`. Every count "a of b".

Section 2, totals for three groups of commands: both have files; only the naive LLM has a file; only PaSh's
own has a file (should be none or near none; say). For each group: commands, uses, uses split under each,
compiler stops, files raising.

Section 3, "What the naive LLM adds": for commands where only the naive LLM has a file, what its file said
(split allowed / no split / raised) and what happened (PaSh splits none of these without a file, so any split
here is a gain; any "no split" answer is a correct-or-not judgement: list the commands and say which answers
are right for the command in general, from your own knowledge of the command, marking the ones you are not
sure about).

Section 4, wall-clock: state in two sentences that per-command time cannot be separated because all of a
source's files were swapped in at once (Tiran's decision, 2026-11-24), and give the only per-command time
evidence there is: scripts whose only differing command is one command, with their time ratio naive ÷ PaSh's
own (find them from the per-use records: scripts where exactly one command's split differs between the two
sets).

Write `per_command.json` with the same numbers. Reply in your pane, in at most ten lines: how many commands
in each of the three groups, the three largest "naive splits more" and "naive splits less" commands with
their counts, and anything you could not count and why.

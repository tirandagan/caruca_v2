# v1 vs the naive LLM: PaSh annotations

This folder holds task 021's comparison (`ai_docs/tasks/021_pash_annotations_v1_vs_naive_comparison.md`)
for the eight commands v1 has finished: cat, cp, cut, grep, rm, sort, split and wc. cut, rm and sort are
also compared on v1's main grammar.

**Status (2026-11-11):** the scorer and the blind assessments are done for all 8 commands. **Start with
[report.md](report.md).** Not done yet: real PaSh runs (check 3), and settling the assessments' 69 claims
by running the command (check 4). One claim is settled: v1's split of `sort -n -u` is unsafe.

## Files

| File | What it is |
|---|---|
| [numbers.md](numbers.md) | every count: completeness, input/output sets, difference types, splitting, run-to-run agreement, exceptions |
| [decision_tables/](decision_tables/) | per command, the answer of every side on groups of lines, differences first (real side names) |
| [assessments/](assessments/) | the blind qualitative assessments, one per command; `swap/` holds the reassessment with letters redrawn |
| [rubric.md](rubric.md) | the rubric the assessments follow (versioned) |
| `packets/`, `packets_swap/` | what each assessor was given: each side's files with comments removed, and the decision table with blind letters |
| `assessments/keys/` | which letter is which side. Assessors were told not to read it |
| [score_pash.py](score_pash.py) | the scorer. It only counts |
| `sides.jsonl`, `lines.jsonl`, `answers.jsonl.gz`, `io_sets.jsonl.gz` | the records every table is built from |

## The sides

- **v1:** task 020's files, on v1's branch `pash-python-annotations`, `caruca/save_pash_py/<cmd>/<grammar>_grammar/trace_1/`.
  `v1-pash` uses v1's PaSh grammar and `v1-main` its main grammar. Trace 2 gave identical files, so it is not
  scored separately.
- **naive:** every collected run of the command (`runs/*/output/{pash,annotation}/`), named by the run's
  start time.
- **pash-own:** the hand-written classes shipped in `pash-annotations` 0.2.4. There are none for cp and split.
  The agent was shown PaSh's own files for grep and rm as examples, so for those two commands the
  agent-versus-PaSh agreement isn't independent.

## The lines

Every side is asked about the same lines:

- **A:** the lines in v1's `eval/command-invocations.txt` that use the command, with shell variables
  replaced by plain words and redirections removed (grep has none);
- **C-v1:** the lines v1 traced;
- **C-naive:** the lines the agent ran during its Fig. 7 campaign runs (from `fig7_campaign/tries/`).

Each line is parsed by each side's own parser table and passed to its classes inside a private copy of
`pash-annotations` 0.2.4. The classes are called directly, so an exception PaSh would hide is recorded.

## How to rerun

```sh
SCORER_SCRATCH=/some/tmp/dir python3 score_pash.py all     # about 30 s
python3 score_pash.py packets-swap                         # reshuffled letters for cut, sort, rm
```

`numbers.md`, the decision tables and the packets are byte-identical between runs. `answers.jsonl.gz`
differs only in the per-line timing field.

## Known limits of the blinding

The assessors can't read comments or docstrings, which are removed. Three things can still give a side
away:

- v1's code lists specific situations;
- v1's lines use its placeholder file names, such as `relpath_1`;
- one v1 parser table marks never-used file options as `PATH_UNTRACED`.

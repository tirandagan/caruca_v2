# Metrics to collect (Tiran, 2026-11-24)

Applies to every script in the experiment, pilot included. The builder's records must carry these
fields; the write-up reports them. Items marked **open** wait for Tiran's answer; leave them out until
the orchestrator fills them in.

## Sources being compared

| Set | Annotation files loaded |
|---|---|
| `bash` | none: plain bash, the reference output and time |
| `pash-own` | PaSh's own files for every command |
| `naive` | the naive LLM's files for every command it has (79); PaSh's own elsewhere |
| `caruca-pash` | Caruca's files (from its PaSh grammar) for its 8 commands; PaSh's own elsewhere |
| `caruca-main` | Caruca's files (from its main grammar) for its 8 commands; PaSh's own elsewhere |

## Per command occurrence in a script

For each command a script calls, under each set, record where its annotation came from:
`ours` (the set's own files: naive's or Caruca's), `pash-own` (PaSh's file, because the set has none
for it), or `none` (nobody has one). This is Tiran's case split: case 1 = commands only PaSh covers,
case 2 = commands Caruca and/or the naive LLM cover.

## Per region (PaSh's unit of work)

A region is one piece of the script PaSh asks its compiler to handle. Count them the way PaSh does
(`Received data: Compile` lines in the `-d 2` log); loops send the same region many times, so also give
the count of **distinct** regions (same region text) per script. For each region, under each set:

- the commands in it, and each command's annotation source (as above);
- the outcome, exactly one of:
  - `parallelized`: PaSh produced a parallel version and ran it (`Optimized script saved in` plus worker copies started);
  - `refused by annotation`: an annotation answered that a command can't be split (record the class it gave);
  - `missing annotation`: PaSh found no file for a command (`InputOutputInformation for X not provided`);
  - `annotation raised`: a set's generator threw an error (PaSh hides this; found by calling the generator directly);
  - `unsupported construct`: PaSh can't handle the shell syntax (`not implemented`);
  - `pash crash`: PaSh's compiler itself raised an exception (e.g. `NameError`);
  - `other`: anything else, with the log text.
- the reason text from the log.

Rates per script and set, always with the denominator: parallelized regions / all regions; each
cause / all regions. Give both the per-execution and the distinct-region versions.
**Decided (Tiran, 2026-11-24): every region not parallelized counts against the source, whatever the
reason**, including `refused by annotation`. The causes are listed alongside the rate.

## Per script and set

- wall-clock seconds: **3 timed repeats** per script and set (decided 2026-11-24); report the median
  and the min–max; timed runs one at a time with nothing else heavy in the VM, Mac awake (check
  `pmset -g log` for the window);
- exit code; output hash; same as bash (yes/no); matches Koala's stored hash (yes/no);
- number of PaSh crashes (compiler exceptions) in the run; whether PaSh printed its
  "No region was parallelized" warning.

## Delineating the time impact

For a given set, a script in which every command's source is `pash-own` is a control: its time should
equal the `pash-own` run's, and the difference measures noise. For scripts with at least one `ours`
command, report the time against `pash-own` and against `bash`, and name the `ours` commands.
**Decided (Tiran, 2026-11-24): all of a source's commands are swapped in at once; there are no
one-command-at-a-time runs.** The report must say this plainly: a time difference is attributed to the
source as a whole, and to the set of swapped commands named for that script, not to any one command.

## Which naive LLM files

**Decided (Tiran, 2026-11-24): the first run per command** (the `"repeat": 1` row in
`naive_llm_caruca/fig7_campaign/ledger.jsonl`), the same choice as the earlier comparisons.

## Record shapes

- `results.jsonl`: one row per group, script, set, repeat, with the per-script fields above.
- `regions.jsonl`: one row per group, script, set, region index, with region text hash, commands,
  sources, outcome, reason.
- `commands.jsonl`: one row per group, script, command, set, source.

## Report requirement added by Tiran (2026-11-24)

The report must give **the path of every test script run** (inside the Koala checkout, e.g.
`oneliners/scripts/spell.sh`, and which published 2022 script it stands for). To keep the body simple for
Michael, this goes in an **addendum** (the report plan's appendix table A1 gets a path column), not in
the body. The builder's `invocations.jsonl` already records each script's path; the counting script
must carry it into the addendum table.

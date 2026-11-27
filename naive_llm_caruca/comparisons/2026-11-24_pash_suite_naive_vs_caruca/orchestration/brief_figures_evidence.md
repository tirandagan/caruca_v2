# Brief: evidence figures for the interim report (from the `spell` records)

You are a worker. An orchestrating Claude session gave you this brief. Work only on it. Run nothing in
the Lima VM `pash` (a batch is timing runs there).

## Goal

The interim report `report_draft.md` in this folder's parent reports one script, `spell`, run under plain
bash and under PaSh with four sources of annotation files. Its evidence is in tables; Michael Greenberg
reads charts faster. Draw the figures below **from the records** (`results.jsonl`, `regions.jsonl`,
`occurrences.jsonl` if present, `numbers_pilot.json`, `answers.jsonl`), with matplotlib, following the
`dataviz` skill (load it first) and the colour/label rules in `orchestration/report_plan.md` section 2
(PaSh's own files dark grey, naive LLM blue, Caruca PaSh grammar orange, Caruca main grammar light
orange; PaSh's own always the reference; every rate "a of b"; ≥ 8 pt text; portrait width 6.5 in; 300 dpi).
Read `report_draft.md` first so each figure matches a sentence in it.

## Figures (write to `figures_interim/`)

1. `split_map.png`: the script's pipeline as nine boxes in order (`cat → sed → col → tr → tr → tr →
   sort → uniq → comm`), one row per source (PaSh's own, naive LLM, Caruca PaSh grammar, Caruca main
   grammar). Each box filled when PaSh split that command use under that source, empty when it ran it
   whole, with a small mark on the commands the source brought its own files for. The reader should see
   in one look that all three sources split `cat`-and-friends differently and that only two split `sort`.
2. `time_bars.png`: horizontal bars, median seconds for bash and each source, with the min–max of the
   3 repeats as a thin line, bash first; the speed-up against bash printed at the end of each bar.
3. `uses_split.png`: for each source, a 100% stacked bar of the 9 command uses: split with the source's
   own files / split with PaSh's own files filled in / whole; counts printed inside segments.

Also write `figures_interim/captions.md`: one plain-language caption per figure (what it shows, the one
sentence it supports), and the exact records and fields each was drawn from.

## Rules

Plain words in captions and labels; no field names. Do not edit the report or the records. Do not
commit. Reply with the three file paths and anything you could not draw from the records.

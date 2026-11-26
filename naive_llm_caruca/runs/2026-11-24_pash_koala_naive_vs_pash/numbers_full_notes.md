## Comparison with the builder's `full_run/numbers.md` (written by hand, 2026-11-26)

How this file was made: `prep_full_records.py` copied the records in `full_run/` into a scratch folder in
the shape `count_report.py` reads, applying the builder's two fix-ups in its own code (compare against the
same repeat's bash row; leave out the 7 web-search rows without `node` and replace the 7 rows that have
redone runs). Its log matches the builder's header: 1854 rows compared again, 482 printed-output flags
changed, 642 output-file flags changed, 7 left out, 7 replaced. Then:

    python3 -I prep_full_records.py --records full_run --out <scratch>
    python3 -I count_report.py --records <scratch> --tag full --sleep-events <scratch>/sleep_events.jsonl \
        --out . --notes numbers_full_notes.md

| `numbers.md` section | Cells compared | Same | Differ |
|---|---|---|---|
| 1. Output and what PaSh did (6 sources: scripts, output same as bash, same as Koala's answer, ran a part in parallel, fell back, other state) | 36 | 36 | 0 |
| 3. Distinct parts against PaSh's own files (4 sources × 5 cells) | 20 | 20 | 0 |
| 5. Commands gained and lost (19 rows) | 38 | 38 | 0 |
| 6. Time (6 sources × 5 cells, and the noise band) | 34 | 34 | 0 |

This count reached section 5 by a different route from the builder's: per script, from the per-use
records (`occurrences`), not from each run's `split_commands` list. The two agree on every row.

Where a number here looks different, it measures something else. None of these is a disagreement:

- **"Faster than bash" in Table 1 above** (12, 7, 3 and 6 of 86) counts scripts faster by any margin, and
  its "median speed-up" is a median of ratios. `numbers.md` uses geometric means and a 10% margin. The
  "Full run: time" table above gives the 10% counts: 10, 6, 1 and 5 of 86. These are the same as the
  checker's (check 10) and the builder's README.
- **The method check**: here, 849 of 850 distinct uses in parts PaSh ran in parallel, under the four
  full-coverage sources. `numbers.md` says 956 of 957, because it also counts the 107 uses of the second
  sed file's runs (850 + 107 = 957). The one exception is the same in both: the naive LLM's `awk` in
  `unixfun/19`, two uses whose copies cannot be told apart.
- **Written files**: here, 211 same, 347 not checked and 18 different, of 576 timed rows of the 32
  scripts that write files. The checker's review (check 4) says 211, 352 and 25, of 588. The difference
  is the 12 web-search rows that fix-up 2 leaves out (7 different, 5 not checked; recounted from the raw
  rows). The checker counted before fix-up 2. Of the 18 "different" rows, 12 are web-search, whose files
  differ even between two bash runs, and 6 are bio, where the check itself was broken (checker, check 4).
- **The second sed file** (52 scripts) cannot be paired with PaSh's own files on every part, so it is
  counted in its own block: 139 distinct parts in its 52 scripts, 14 in parallel with both, 0 gained,
  0 lost. These are the same as `numbers.md`. `numbers.md`'s header says this file "was run only on scripts
  that use sed". That sentence is out of date: in 27 of the 52, bash starts no `sed` (checker, check 7,
  item 6). The current `summarise.py` already says so, but `numbers.md` has not been rebuilt since.

Three of this script's own checks fail for reasons that do not touch any number in the report:

- **Inventory names.** The inventory calls two scripts `weather/max-temp` and `web-search/web-index`;
  the records call them `weather/temp-analytics` and `web-search/engine`. And the stand-in programs record
  awk program text and helper functions (`bigrams_aux`) as command names.
- **Controls.** The controls' phases are named `after-46` and `end`, not `start` and `end`.
- **Sleep overlap.** One run window overlaps a Mac sleep: web-search's repeats window, 08:21 sleep. That
  window's repeat 3 is replaced by the redone rows. The checker (check 9) shows that its repeat 2 ended
  before the sleep.

# Numbers: PaSh runs with each side's annotation files (task 022)

Made by `count_runs.py` from `pash_runs.jsonl.gz`. Counts only. One PaSh run per command line and side, 8 workers. "Split" needs both signals: split steps in PaSh's log and more than one copy of the command started. "Split set up, workers got no input" means PaSh's generated script holds several worker copies but the stream it split carried no data, so the copies never started. "PaSh error" means PaSh's compiler raised an exception and the script ran as plain bash. Each count is out of the runs in its row.

## What PaSh did, per command and side

| Command | Side | Lines run | Side allows a split | PaSh split | Split set up, workers got no input | Not split | PaSh error | Unknown | Output differs from bash | Exit code differs | Files left differ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cat | v1, PaSh grammar | 103 | 75 | 75 | 0 | 28 | 0 | 0 | 0 | 0 | 0 |
| cat | naive LLM, run 2026-10-28_100411 | 103 | 103 | 87 | 0 | 9 | 7 | 0 | 0 | 0 | 0 |
| cat | PaSh's own | 103 | 0 | 0 | 0 | 103 | 0 | 0 | 0 | 0 | 0 |
| cat | no annotation | 103 | 0 | 0 | 0 | 103 | 0 | 0 | 0 | 0 | 0 |
| cut | v1, PaSh grammar | 88 | 27 | 27 | 0 | 61 | 0 | 0 | 0 | 0 | 0 |
| cut | v1, main grammar | 88 | 27 | 27 | 0 | 61 | 0 | 0 | 0 | 0 | 0 |
| cut | naive LLM, run 2026-10-20_135253 | 88 | 86 | 61 | 0 | 2 | 25 | 0 | 0 | 0 | 0 |
| cut | naive LLM, run 2026-10-27_230555 | 88 | 86 | 61 | 0 | 2 | 25 | 0 | 0 | 0 | 0 |
| cut | naive LLM, run 2026-10-28_145447 | 88 | 86 | 61 | 0 | 2 | 25 | 0 | 0 | 0 | 0 |
| cut | naive LLM, run 2026-10-28_152550 | 88 | 86 | 61 | 0 | 2 | 25 | 0 | 0 | 0 | 0 |
| cut | PaSh's own | 88 | 88 | 63 | 0 | 0 | 25 | 0 | **2** | 0 | 0 |
| cut | no annotation | 88 | 0 | 0 | 0 | 88 | 0 | 0 | 0 | 0 | 0 |
| grep | v1, PaSh grammar | 48 | 1 | 1 | 0 | 44 | 3 | 0 | 0 | 0 | 0 |
| grep | naive LLM, run 2026-10-13_193448 | 48 | 17 | 1 | 0 | 46 | 1 | 0 | 0 | 0 | 0 |
| grep | naive LLM, run 2026-10-20_112956 | 48 | 43 | 13 | 11 | 5 | 19 | 0 | **11** | 0 | 0 |
| grep | naive LLM, run 2026-10-28_135447 | 48 | 43 | 15 | 8 | 5 | 20 | 0 | **8** | 0 | 0 |
| grep | PaSh's own | 48 | 45 | 15 | 11 | 3 | 19 | 0 | **13** | 0 | 0 |
| grep | no annotation | 48 | 0 | 0 | 0 | 48 | 0 | 0 | 0 | 0 | 0 |
| sort | v1, PaSh grammar | 64 | 1 | 1 | 0 | 54 | 9 | 0 | 0 | 0 | 0 |
| sort | v1, main grammar | 64 | 8 | 8 | 0 | 46 | 10 | 0 | **7** | 0 | 0 |
| sort | naive LLM, run 2026-10-20_160340 | 64 | 14 | 9 | 0 | 32 | 23 | 0 | 0 | 0 | 0 |
| sort | naive LLM, run 2026-10-28_140825 | 64 | 63 | 36 | 0 | 4 | 24 | 0 | 0 | 0 | 0 |
| sort | naive LLM, run 2026-10-28_151151 | 64 | 14 | 9 | 0 | 32 | 23 | 0 | 0 | 0 | 0 |
| sort | naive LLM, run 2026-10-28_154444 | 64 | 14 | 9 | 0 | 32 | 23 | 0 | 0 | 0 | 0 |
| sort | PaSh's own | 64 | 45 | 23 | 0 | 18 | 23 | 0 | **1** | 0 | 0 |
| sort | no annotation | 64 | 0 | 0 | 0 | 64 | 0 | 0 | 0 | 0 | 0 |
| cp | v1, PaSh grammar | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| cp | naive LLM, run 2026-10-28_114133 | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| cp | naive LLM, run 2026-10-28_150709 | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| cp | naive LLM, run 2026-10-28_153913 | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| cp | no annotation | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| rm | v1, PaSh grammar | 71 | 0 | 0 | 0 | 71 | 0 | 0 | 0 | 0 | 0 |
| rm | v1, main grammar | 71 | 0 | 0 | 0 | 71 | 0 | 0 | 0 | 0 | 0 |
| rm | naive LLM, run 2026-10-20_121932 | 71 | 0 | 0 | 0 | 71 | 0 | 0 | 0 | 0 | 0 |
| rm | naive LLM, run 2026-10-28_105951 | 71 | 0 | 0 | 0 | 71 | 0 | 0 | 0 | 0 | 0 |
| rm | PaSh's own | 71 | 0 | 0 | 0 | 71 | 0 | 0 | 0 | 0 | 0 |
| rm | no annotation | 71 | 0 | 0 | 0 | 71 | 0 | 0 | 0 | 0 | 0 |
| split | v1, PaSh grammar | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| split | naive LLM, run 2026-10-28_134035 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| split | no annotation | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| wc | v1, PaSh grammar | 3 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| wc | naive LLM, run 2026-10-28_091448 | 3 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| wc | PaSh's own | 3 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| wc | no annotation | 3 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |

Pooled over the eight commands:

| Side | Runs | Side allows a split | PaSh split | Split set up, workers got no input | Not split | PaSh error | Unknown | Output differs from bash |
|---|---|---|---|---|---|---|---|---|
| v1, PaSh grammar | 382 | 104 | 104 | 0 | 266 | 12 | 0 | 0 |
| v1, main grammar | 223 | 35 | 35 | 0 | 178 | 10 | 0 | 7 |
| naive LLM (all runs) | 1013 | 655 | 423 | 19 | 331 | 240 | 0 | 19 |
| PaSh's own | 377 | 178 | 101 | 11 | 198 | 67 | 0 | 16 |
| no annotation | 382 | 0 | 0 | 0 | 382 | 0 | 0 | 0 |

## The same, split by where the line came from

"Benchmark" lines come from PaSh's benchmark scripts. "Disagreement" lines were picked because the sides give PaSh different splitting answers, so they overstate how often the sides differ. "Named" lines are the cases task 021 flagged.

| Command | Lines from | Side | Lines run | PaSh split | Split set up, workers got no input | Not split | PaSh error | Output differs from bash |
|---|---|---|---|---|---|---|---|---|
| cat | benchmark | v1, PaSh grammar | 78 | 75 | 0 | 3 | 0 | 0 |
| cat | benchmark | naive LLM, run 2026-10-28_100411 | 78 | 75 | 0 | 0 | 3 | 0 |
| cat | benchmark | PaSh's own | 78 | 0 | 0 | 78 | 0 | 0 |
| cat | benchmark | no annotation | 78 | 0 | 0 | 78 | 0 | 0 |
| cat | disagreement | v1, PaSh grammar | 21 | 0 | 0 | 21 | 0 | 0 |
| cat | disagreement | naive LLM, run 2026-10-28_100411 | 21 | 12 | 0 | 6 | 3 | 0 |
| cat | disagreement | PaSh's own | 21 | 0 | 0 | 21 | 0 | 0 |
| cat | disagreement | no annotation | 21 | 0 | 0 | 21 | 0 | 0 |
| cat | named | v1, PaSh grammar | 4 | 0 | 0 | 4 | 0 | 0 |
| cat | named | naive LLM, run 2026-10-28_100411 | 4 | 0 | 0 | 3 | 1 | 0 |
| cat | named | PaSh's own | 4 | 0 | 0 | 4 | 0 | 0 |
| cat | named | no annotation | 4 | 0 | 0 | 4 | 0 | 0 |
| cut | benchmark | v1, PaSh grammar | 46 | 27 | 0 | 19 | 0 | 0 |
| cut | benchmark | v1, main grammar | 46 | 27 | 0 | 19 | 0 | 0 |
| cut | benchmark | naive LLM, run 2026-10-20_135253 | 46 | 31 | 0 | 0 | 15 | 0 |
| cut | benchmark | naive LLM, run 2026-10-27_230555 | 46 | 31 | 0 | 0 | 15 | 0 |
| cut | benchmark | naive LLM, run 2026-10-28_145447 | 46 | 31 | 0 | 0 | 15 | 0 |
| cut | benchmark | naive LLM, run 2026-10-28_152550 | 46 | 31 | 0 | 0 | 15 | 0 |
| cut | benchmark | PaSh's own | 46 | 31 | 0 | 0 | 15 | 0 |
| cut | benchmark | no annotation | 46 | 0 | 0 | 46 | 0 | 0 |
| cut | disagreement | v1, PaSh grammar | 40 | 0 | 0 | 40 | 0 | 0 |
| cut | disagreement | v1, main grammar | 40 | 0 | 0 | 40 | 0 | 0 |
| cut | disagreement | naive LLM, run 2026-10-20_135253 | 40 | 30 | 0 | 0 | 10 | 0 |
| cut | disagreement | naive LLM, run 2026-10-27_230555 | 40 | 30 | 0 | 0 | 10 | 0 |
| cut | disagreement | naive LLM, run 2026-10-28_145447 | 40 | 30 | 0 | 0 | 10 | 0 |
| cut | disagreement | naive LLM, run 2026-10-28_152550 | 40 | 30 | 0 | 0 | 10 | 0 |
| cut | disagreement | PaSh's own | 40 | 30 | 0 | 0 | 10 | 0 |
| cut | disagreement | no annotation | 40 | 0 | 0 | 40 | 0 | 0 |
| cut | named | v1, PaSh grammar | 2 | 0 | 0 | 2 | 0 | 0 |
| cut | named | v1, main grammar | 2 | 0 | 0 | 2 | 0 | 0 |
| cut | named | naive LLM, run 2026-10-20_135253 | 2 | 0 | 0 | 2 | 0 | 0 |
| cut | named | naive LLM, run 2026-10-27_230555 | 2 | 0 | 0 | 2 | 0 | 0 |
| cut | named | naive LLM, run 2026-10-28_145447 | 2 | 0 | 0 | 2 | 0 | 0 |
| cut | named | naive LLM, run 2026-10-28_152550 | 2 | 0 | 0 | 2 | 0 | 0 |
| cut | named | PaSh's own | 2 | 2 | 0 | 0 | 0 | **2** |
| cut | named | no annotation | 2 | 0 | 0 | 2 | 0 | 0 |
| grep | disagreement | v1, PaSh grammar | 40 | 0 | 0 | 38 | 2 | 0 |
| grep | disagreement | naive LLM, run 2026-10-13_193448 | 40 | 1 | 0 | 38 | 1 | 0 |
| grep | disagreement | naive LLM, run 2026-10-20_112956 | 40 | 12 | 10 | 0 | 18 | **10** |
| grep | disagreement | naive LLM, run 2026-10-28_135447 | 40 | 14 | 7 | 0 | 19 | **7** |
| grep | disagreement | PaSh's own | 40 | 12 | 10 | 0 | 18 | **10** |
| grep | disagreement | no annotation | 40 | 0 | 0 | 40 | 0 | 0 |
| grep | named | v1, PaSh grammar | 8 | 1 | 0 | 6 | 1 | 0 |
| grep | named | naive LLM, run 2026-10-13_193448 | 8 | 0 | 0 | 8 | 0 | 0 |
| grep | named | naive LLM, run 2026-10-20_112956 | 8 | 1 | 1 | 5 | 1 | **1** |
| grep | named | naive LLM, run 2026-10-28_135447 | 8 | 1 | 1 | 5 | 1 | **1** |
| grep | named | PaSh's own | 8 | 3 | 1 | 3 | 1 | **3** |
| grep | named | no annotation | 8 | 0 | 0 | 8 | 0 | 0 |
| sort | benchmark | v1, PaSh grammar | 17 | 0 | 0 | 9 | 8 | 0 |
| sort | benchmark | v1, main grammar | 17 | 0 | 0 | 15 | 2 | 0 |
| sort | benchmark | naive LLM, run 2026-10-20_160340 | 17 | 1 | 0 | 11 | 5 | 0 |
| sort | benchmark | naive LLM, run 2026-10-28_140825 | 17 | 10 | 0 | 0 | 7 | 0 |
| sort | benchmark | naive LLM, run 2026-10-28_151151 | 17 | 1 | 0 | 11 | 5 | 0 |
| sort | benchmark | naive LLM, run 2026-10-28_154444 | 17 | 1 | 0 | 11 | 5 | 0 |
| sort | benchmark | PaSh's own | 17 | 9 | 0 | 1 | 7 | 0 |
| sort | benchmark | no annotation | 17 | 0 | 0 | 17 | 0 | 0 |
| sort | disagreement | v1, PaSh grammar | 40 | 0 | 0 | 40 | 0 | 0 |
| sort | disagreement | v1, main grammar | 40 | 2 | 0 | 30 | 8 | **2** |
| sort | disagreement | naive LLM, run 2026-10-20_160340 | 40 | 3 | 0 | 20 | 17 | 0 |
| sort | disagreement | naive LLM, run 2026-10-28_140825 | 40 | 20 | 0 | 3 | 17 | 0 |
| sort | disagreement | naive LLM, run 2026-10-28_151151 | 40 | 3 | 0 | 20 | 17 | 0 |
| sort | disagreement | naive LLM, run 2026-10-28_154444 | 40 | 3 | 0 | 20 | 17 | 0 |
| sort | disagreement | PaSh's own | 40 | 14 | 0 | 10 | 16 | **1** |
| sort | disagreement | no annotation | 40 | 0 | 0 | 40 | 0 | 0 |
| sort | named | v1, PaSh grammar | 7 | 1 | 0 | 5 | 1 | 0 |
| sort | named | v1, main grammar | 7 | 6 | 0 | 1 | 0 | **5** |
| sort | named | naive LLM, run 2026-10-20_160340 | 7 | 5 | 0 | 1 | 1 | 0 |
| sort | named | naive LLM, run 2026-10-28_140825 | 7 | 6 | 0 | 1 | 0 | 0 |
| sort | named | naive LLM, run 2026-10-28_151151 | 7 | 5 | 0 | 1 | 1 | 0 |
| sort | named | naive LLM, run 2026-10-28_154444 | 7 | 5 | 0 | 1 | 1 | 0 |
| sort | named | PaSh's own | 7 | 0 | 0 | 7 | 0 | 0 |
| sort | named | no annotation | 7 | 0 | 0 | 7 | 0 | 0 |
| cp | benchmark | v1, PaSh grammar | 4 | 0 | 0 | 4 | 0 | 0 |
| cp | benchmark | naive LLM, run 2026-10-28_114133 | 4 | 0 | 0 | 4 | 0 | 0 |
| cp | benchmark | naive LLM, run 2026-10-28_150709 | 4 | 0 | 0 | 4 | 0 | 0 |
| cp | benchmark | naive LLM, run 2026-10-28_153913 | 4 | 0 | 0 | 4 | 0 | 0 |
| cp | benchmark | no annotation | 4 | 0 | 0 | 4 | 0 | 0 |
| rm | benchmark | v1, PaSh grammar | 71 | 0 | 0 | 71 | 0 | 0 |
| rm | benchmark | v1, main grammar | 71 | 0 | 0 | 71 | 0 | 0 |
| rm | benchmark | naive LLM, run 2026-10-20_121932 | 71 | 0 | 0 | 71 | 0 | 0 |
| rm | benchmark | naive LLM, run 2026-10-28_105951 | 71 | 0 | 0 | 71 | 0 | 0 |
| rm | benchmark | PaSh's own | 71 | 0 | 0 | 71 | 0 | 0 |
| rm | benchmark | no annotation | 71 | 0 | 0 | 71 | 0 | 0 |
| split | benchmark | v1, PaSh grammar | 1 | 0 | 0 | 1 | 0 | 0 |
| split | benchmark | naive LLM, run 2026-10-28_134035 | 1 | 0 | 0 | 1 | 0 | 0 |
| split | benchmark | no annotation | 1 | 0 | 0 | 1 | 0 | 0 |
| wc | benchmark | v1, PaSh grammar | 3 | 0 | 0 | 3 | 0 | 0 |
| wc | benchmark | naive LLM, run 2026-10-28_091448 | 3 | 0 | 0 | 3 | 0 | 0 |
| wc | benchmark | PaSh's own | 3 | 0 | 0 | 3 | 0 | 0 |
| wc | benchmark | no annotation | 3 | 0 | 0 | 3 | 0 | 0 |

## When the side allows a split, does PaSh split?

Only runs where the side's files allow a split.

| Command | Side | Allowed | PaSh split | Split set up, workers got no input | PaSh error | Not split | Unknown | Why not (count) |
|---|---|---|---|---|---|---|---|---|
| cat | v1, PaSh grammar | 75 | 75 | 0 | 0 | 0 | 0 |  |
| cat | naive LLM, run 2026-10-28_100411 | 103 | 87 | 0 | 7 | 9 | 0 |  (9); AssertionError (7) |
| cut | v1, PaSh grammar | 27 | 27 | 0 | 0 | 0 | 0 |  |
| cut | v1, main grammar | 27 | 27 | 0 | 0 | 0 | 0 |  |
| cut | naive LLM, run 2026-10-20_135253 | 86 | 61 | 0 | 25 | 0 | 0 | AssertionError (25) |
| cut | naive LLM, run 2026-10-27_230555 | 86 | 61 | 0 | 25 | 0 | 0 | AssertionError (25) |
| cut | naive LLM, run 2026-10-28_145447 | 86 | 61 | 0 | 25 | 0 | 0 | AssertionError (25) |
| cut | naive LLM, run 2026-10-28_152550 | 86 | 61 | 0 | 25 | 0 | 0 | AssertionError (25) |
| cut | PaSh's own | 88 | 63 | 0 | 25 | 0 | 0 | AssertionError (25) |
| grep | v1, PaSh grammar | 1 | 1 | 0 | 0 | 0 | 0 |  |
| grep | naive LLM, run 2026-10-13_193448 | 17 | 1 | 0 | 1 | 15 | 0 | Daemon:  WARNING: Exception caught because some region(s) are unparall (15); NameError: name 'OptionWithIOVar' is not defined. Did you mean: 'Optio (1) |
| grep | naive LLM, run 2026-10-20_112956 | 43 | 13 | 11 | 19 | 0 | 0 | AssertionError (16); PaSh's script has 8 worker copies; 0 started, because the stream PaSh  (10); NameError: name 'OptionWithIOVar' is not defined. Did you mean: 'Optio (3) |
| grep | naive LLM, run 2026-10-28_135447 | 43 | 15 | 8 | 20 | 0 | 0 | AssertionError (17); PaSh's script has 8 worker copies; 0 started, because the stream PaSh  (8); NameError: name 'OptionWithIOVar' is not defined. Did you mean: 'Optio (3) |
| grep | PaSh's own | 45 | 15 | 11 | 19 | 0 | 0 | AssertionError (16); PaSh's script has 8 worker copies; 0 started, because the stream PaSh  (10); NameError: name 'OptionWithIOVar' is not defined. Did you mean: 'Optio (3) |
| sort | v1, PaSh grammar | 1 | 1 | 0 | 0 | 0 | 0 |  |
| sort | v1, main grammar | 8 | 8 | 0 | 0 | 0 | 0 |  |
| sort | naive LLM, run 2026-10-20_160340 | 14 | 9 | 0 | 5 | 0 | 0 | AssertionError (5) |
| sort | naive LLM, run 2026-10-28_140825 | 63 | 36 | 0 | 24 | 3 | 0 | AssertionError (20); NameError: name 'OptionWithIOVar' is not defined. Did you mean: 'Optio (4); [PaSh] Warning: No region was parallelized successfully (3) |
| sort | naive LLM, run 2026-10-28_151151 | 14 | 9 | 0 | 5 | 0 | 0 | AssertionError (5) |
| sort | naive LLM, run 2026-10-28_154444 | 14 | 9 | 0 | 5 | 0 | 0 | AssertionError (5) |
| sort | PaSh's own | 45 | 23 | 0 | 19 | 3 | 0 | AssertionError (19); [PaSh] Warning: No region was parallelized successfully (3) |

Runs where the side did **not** allow a split and PaSh split anyway: **0** (must be 0, or the wrong folder was loaded).

## v1 against each naive run, line by line

Lines where both were run. "Split" here includes a split that was set up but whose workers got no input. "Wrong" means the output differs from bash's.

| Command | v1 side | Naive run | Lines | Both split | Only v1 split | Only the agent split | Neither | v1 output wrong | Agent output wrong |
|---|---|---|---|---|---|---|---|---|---|
| cat | v1, PaSh grammar | naive LLM, run 2026-10-28_100411 | 103 | 75 | 0 | 12 | 16 | 0 | 0 |
| cut | v1, PaSh grammar | naive LLM, run 2026-10-20_135253 | 88 | 27 | 0 | 34 | 27 | 0 | 0 |
| cut | v1, PaSh grammar | naive LLM, run 2026-10-27_230555 | 88 | 27 | 0 | 34 | 27 | 0 | 0 |
| cut | v1, PaSh grammar | naive LLM, run 2026-10-28_145447 | 88 | 27 | 0 | 34 | 27 | 0 | 0 |
| cut | v1, PaSh grammar | naive LLM, run 2026-10-28_152550 | 88 | 27 | 0 | 34 | 27 | 0 | 0 |
| cut | v1, main grammar | naive LLM, run 2026-10-20_135253 | 88 | 27 | 0 | 34 | 27 | 0 | 0 |
| cut | v1, main grammar | naive LLM, run 2026-10-27_230555 | 88 | 27 | 0 | 34 | 27 | 0 | 0 |
| cut | v1, main grammar | naive LLM, run 2026-10-28_145447 | 88 | 27 | 0 | 34 | 27 | 0 | 0 |
| cut | v1, main grammar | naive LLM, run 2026-10-28_152550 | 88 | 27 | 0 | 34 | 27 | 0 | 0 |
| grep | v1, PaSh grammar | naive LLM, run 2026-10-13_193448 | 48 | 0 | 1 | 1 | 46 | 0 | 0 |
| grep | v1, PaSh grammar | naive LLM, run 2026-10-20_112956 | 48 | 1 | 0 | 23 | 24 | 0 | 11 |
| grep | v1, PaSh grammar | naive LLM, run 2026-10-28_135447 | 48 | 1 | 0 | 22 | 25 | 0 | 8 |
| sort | v1, PaSh grammar | naive LLM, run 2026-10-20_160340 | 64 | 0 | 1 | 9 | 54 | 0 | 0 |
| sort | v1, PaSh grammar | naive LLM, run 2026-10-28_140825 | 64 | 0 | 1 | 36 | 27 | 0 | 0 |
| sort | v1, PaSh grammar | naive LLM, run 2026-10-28_151151 | 64 | 0 | 1 | 9 | 54 | 0 | 0 |
| sort | v1, PaSh grammar | naive LLM, run 2026-10-28_154444 | 64 | 0 | 1 | 9 | 54 | 0 | 0 |
| sort | v1, main grammar | naive LLM, run 2026-10-20_160340 | 64 | 4 | 4 | 5 | 51 | 7 | 0 |
| sort | v1, main grammar | naive LLM, run 2026-10-28_140825 | 64 | 7 | 1 | 29 | 27 | 7 | 0 |
| sort | v1, main grammar | naive LLM, run 2026-10-28_151151 | 64 | 4 | 4 | 5 | 51 | 7 | 0 |
| sort | v1, main grammar | naive LLM, run 2026-10-28_154444 | 64 | 4 | 4 | 5 | 51 | 7 | 0 |
| cp | v1, PaSh grammar | naive LLM, run 2026-10-28_114133 | 4 | 0 | 0 | 0 | 4 | 0 | 0 |
| cp | v1, PaSh grammar | naive LLM, run 2026-10-28_150709 | 4 | 0 | 0 | 0 | 4 | 0 | 0 |
| cp | v1, PaSh grammar | naive LLM, run 2026-10-28_153913 | 4 | 0 | 0 | 0 | 4 | 0 | 0 |
| rm | v1, PaSh grammar | naive LLM, run 2026-10-20_121932 | 71 | 0 | 0 | 0 | 71 | 0 | 0 |
| rm | v1, PaSh grammar | naive LLM, run 2026-10-28_105951 | 71 | 0 | 0 | 0 | 71 | 0 | 0 |
| rm | v1, main grammar | naive LLM, run 2026-10-20_121932 | 71 | 0 | 0 | 0 | 71 | 0 | 0 |
| rm | v1, main grammar | naive LLM, run 2026-10-28_105951 | 71 | 0 | 0 | 0 | 71 | 0 | 0 |
| split | v1, PaSh grammar | naive LLM, run 2026-10-28_134035 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| wc | v1, PaSh grammar | naive LLM, run 2026-10-28_091448 | 3 | 0 | 0 | 0 | 3 | 0 | 0 |

## Every run whose output differs from bash

| Command | Script | Sides | PaSh state | Cause (runs) |
|---|---|---|---|---|
| cut | `cat in.txt \| cut -z -c 1-3` | PaSh's own | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| cut | `cat in.txt \| cut -z -d , -f 1` | PaSh's own | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| grep | `cat in.txt \| grep -A 1 ab` | PaSh's own | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| grep | `cat in.txt \| grep -m 5 ab` | PaSh's own | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| grep | `grep --color always foo a.txt` | PaSh's own; naive LLM, run 2026-10-20_112956 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (2) |
| grep | `grep --color foo a.txt` | PaSh's own; naive LLM, run 2026-10-20_112956 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (2) |
| grep | `grep --colour foo a.txt` | PaSh's own; naive LLM, run 2026-10-20_112956 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (2) |
| grep | `grep --dereference-recursive foo a.txt` | PaSh's own; naive LLM, run 2026-10-20_112956; naive LLM, run 2026-10-28_135447 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (3) |
| grep | `grep -R a relpath_1` | PaSh's own; naive LLM, run 2026-10-20_112956; naive LLM, run 2026-10-28_135447 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (3) |
| grep | `grep -r -R a relpath_1` | PaSh's own; naive LLM, run 2026-10-20_112956; naive LLM, run 2026-10-28_135447 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (3) |
| grep | `grep -r a relpath_1` | PaSh's own; naive LLM, run 2026-10-20_112956; naive LLM, run 2026-10-28_135447 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (3) |
| grep | `grep -r ab d1` | PaSh's own; naive LLM, run 2026-10-20_112956; naive LLM, run 2026-10-28_135447 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (3) |
| grep | `grep -v -R a relpath_1` | PaSh's own; naive LLM, run 2026-10-20_112956; naive LLM, run 2026-10-28_135447 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (3) |
| grep | `grep -v -r -R a relpath_1` | PaSh's own; naive LLM, run 2026-10-20_112956; naive LLM, run 2026-10-28_135447 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (3) |
| grep | `grep -v -r a relpath_1` | PaSh's own; naive LLM, run 2026-10-20_112956; naive LLM, run 2026-10-28_135447 | split, workers idle | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (3) |
| sort | `cat in.txt \| sort -g -u` | v1, main grammar | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| sort | `cat in.txt \| sort -h -s` | v1, main grammar | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| sort | `cat in.txt \| sort -k 1 --help` | PaSh's own | split | not hand-checked: the merge step is not plain joining (1) |
| sort | `cat in.txt \| sort -k 1 -s` | v1, main grammar | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| sort | `cat in.txt \| sort -k 1 -u` | v1, main grammar | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| sort | `cat in.txt \| sort -k 1,1 -u` | v1, main grammar | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| sort | `cat in.txt \| sort -n -s` | v1, main grammar | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |
| sort | `cat in.txt \| sort -n -u` | v1, main grammar | split | unsafe annotation: splitting and joining by hand also gives a different output (1) |

Wrong outputs per side, by cause:

| Command | Side | Wrong outputs | Cause (runs) |
|---|---|---|---|
| cut | PaSh's own | 2 of 88 | unsafe annotation: splitting and joining by hand also gives a different output (2) |
| grep | naive LLM, run 2026-10-20_112956 | 11 of 48 | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (11) |
| grep | naive LLM, run 2026-10-28_135447 | 8 of 48 | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (8) |
| grep | PaSh's own | 13 of 48 | the side's files misdescribe the input: PaSh split a stream the command does not read, so the worker copies got nothing (11); unsafe annotation: splitting and joining by hand also gives a different output (2) |
| sort | v1, main grammar | 7 of 64 | unsafe annotation: splitting and joining by hand also gives a different output (7) |
| sort | PaSh's own | 1 of 64 | not hand-checked: the merge step is not plain joining (1) |

## Errors inside PaSh, by message

| Error | Runs | Command and side family (runs) | Example script |
|---|---|---|---|
| `AssertionError @ ir.py:596 pipe_append` | 161 | cut naive (56); cut reference (14); grep naive (2); grep reference (1); grep v1 (3); sort naive (56); sort reference (14); sort v1 (15) | `cat in.txt \| cut -b-32` |
| `AssertionError @ dfg_node.py:270 get_single_streaming_input_single_output_and_configuration_inputs_of_node_for_parallelization` | 125 | cat naive (7); cut naive (44); cut reference (11); grep naive (31); grep reference (15); sort naive (12); sort reference (5) | `cat IN1 temp IN2` |
| `NameError: name 'OptionWithIOVar' is not defined. Did you mean: 'OptionWithIO'? @ ir.py:215 add_file_id_vars` | 34 | grep naive (7); grep reference (3); sort naive (16); sort reference (4); sort v1 (4) | `grep -f nope a.txt` |
| `AssertionError @ AggregatorSpec.py:275 get_aggregator` | 9 | sort naive (9) | `cat in.txt \| sort -k 1 -u` |

## Why PaSh did not split, where it gave a reason

| Reason in PaSh's log | Runs | Side family (runs) |
|---|---|---|
| InputOutputInformation not provided, so considered side-effectful | 749 | control (382); naive (47); v1 (320) |
| [PaSh] Warning: No region was parallelized successfully | 306 | naive (166); reference (74); v1 (66) |
| no reason logged | 300 | naive (118); reference (124); v1 (58) |

## Run to run

Share of lines on which two sides led PaSh to the same state and the same output.

| Command | Side | Side | Same state and output |
|---|---|---|---|
| cut | naive LLM, run 2026-10-20_135253 | naive LLM, run 2026-10-27_230555 | 88 of 88 |
| cut | naive LLM, run 2026-10-20_135253 | naive LLM, run 2026-10-28_145447 | 88 of 88 |
| cut | naive LLM, run 2026-10-20_135253 | naive LLM, run 2026-10-28_152550 | 88 of 88 |
| cut | naive LLM, run 2026-10-27_230555 | naive LLM, run 2026-10-28_145447 | 88 of 88 |
| cut | naive LLM, run 2026-10-27_230555 | naive LLM, run 2026-10-28_152550 | 88 of 88 |
| cut | naive LLM, run 2026-10-28_145447 | naive LLM, run 2026-10-28_152550 | 88 of 88 |
| cut | v1, PaSh grammar | v1, main grammar | 88 of 88 |
| grep | naive LLM, run 2026-10-13_193448 | naive LLM, run 2026-10-20_112956 | 7 of 48 |
| grep | naive LLM, run 2026-10-13_193448 | naive LLM, run 2026-10-28_135447 | 7 of 48 |
| grep | naive LLM, run 2026-10-20_112956 | naive LLM, run 2026-10-28_135447 | 45 of 48 |
| sort | naive LLM, run 2026-10-20_160340 | naive LLM, run 2026-10-28_140825 | 33 of 64 |
| sort | naive LLM, run 2026-10-20_160340 | naive LLM, run 2026-10-28_151151 | 64 of 64 |
| sort | naive LLM, run 2026-10-20_160340 | naive LLM, run 2026-10-28_154444 | 64 of 64 |
| sort | naive LLM, run 2026-10-28_140825 | naive LLM, run 2026-10-28_151151 | 33 of 64 |
| sort | naive LLM, run 2026-10-28_140825 | naive LLM, run 2026-10-28_154444 | 33 of 64 |
| sort | naive LLM, run 2026-10-28_151151 | naive LLM, run 2026-10-28_154444 | 64 of 64 |
| sort | v1, PaSh grammar | v1, main grammar | 42 of 64 |
| cp | naive LLM, run 2026-10-28_114133 | naive LLM, run 2026-10-28_150709 | 4 of 4 |
| cp | naive LLM, run 2026-10-28_114133 | naive LLM, run 2026-10-28_153913 | 4 of 4 |
| cp | naive LLM, run 2026-10-28_150709 | naive LLM, run 2026-10-28_153913 | 4 of 4 |
| rm | naive LLM, run 2026-10-20_121932 | naive LLM, run 2026-10-28_105951 | 71 of 71 |
| rm | v1, PaSh grammar | v1, main grammar | 71 of 71 |

## Speed, on the larger input

Input: 64,172,874 bytes. Median of 5 runs. Only lines that split with the right output under at least one side; "no annotation" is the unsplit PaSh run, which shows PaSh's own overhead.

| Command | Line | Side | PaSh state | Output right | bash (s) | PaSh (s) | bash time / PaSh time |
|---|---|---|---|---|---|---|---|
| cat | `cat` | v1, PaSh grammar | split | yes | 0.03 | 0.24 | 0.12x |
| cat | `cat` | naive LLM, run 2026-10-28_100411 | split | yes | 0.03 | 0.23 | 0.13x |
| cat | `cat` | no annotation | not split | yes | 0.03 | 0.11 | 0.26x |
| cat | `cat WIKI/ARG0` | v1, PaSh grammar | split | yes | 0.02 | 0.29 | 0.08x |
| cat | `cat WIKI/ARG0` | naive LLM, run 2026-10-28_100411 | split | yes | 0.02 | 0.27 | 0.08x |
| cat | `cat WIKI/ARG0` | no annotation | not split | yes | 0.02 | 0.10 | 0.22x |
| cat | `cat data_file` | v1, PaSh grammar | split | yes | 0.03 | 0.27 | 0.09x |
| cat | `cat data_file` | naive LLM, run 2026-10-28_100411 | split | yes | 0.03 | 0.27 | 0.09x |
| cat | `cat data_file` | no annotation | not split | yes | 0.03 | 0.10 | 0.25x |
| cut | `cut -c 1-1` | v1, PaSh grammar | split | yes | 0.15 | 0.23 | 0.68x |
| cut | `cut -c 1-1` | v1, main grammar | split | yes | 0.15 | 0.23 | 0.67x |
| cut | `cut -c 1-1` | naive LLM, run 2026-10-20_135253 | split | yes | 0.15 | 0.22 | 0.69x |
| cut | `cut -c 1-1` | naive LLM, run 2026-10-27_230555 | split | yes | 0.15 | 0.22 | 0.70x |
| cut | `cut -c 1-1` | naive LLM, run 2026-10-28_145447 | split | yes | 0.15 | 0.23 | 0.67x |
| cut | `cut -c 1-1` | naive LLM, run 2026-10-28_152550 | split | yes | 0.15 | 0.23 | 0.67x |
| cut | `cut -c 1-1` | PaSh's own | split | yes | 0.15 | 0.24 | 0.63x |
| cut | `cut -c 1-1` | no annotation | not split | yes | 0.15 | 0.22 | 0.68x |
| cut | `cut -c 1-12` | v1, PaSh grammar | split | yes | 0.16 | 0.22 | 0.71x |
| cut | `cut -c 1-12` | v1, main grammar | split | yes | 0.16 | 0.23 | 0.70x |
| cut | `cut -c 1-12` | naive LLM, run 2026-10-20_135253 | split | yes | 0.16 | 0.24 | 0.67x |
| cut | `cut -c 1-12` | naive LLM, run 2026-10-27_230555 | split | yes | 0.16 | 0.23 | 0.70x |
| cut | `cut -c 1-12` | naive LLM, run 2026-10-28_145447 | split | yes | 0.16 | 0.23 | 0.70x |
| cut | `cut -c 1-12` | naive LLM, run 2026-10-28_152550 | split | yes | 0.16 | 0.23 | 0.70x |
| cut | `cut -c 1-12` | PaSh's own | split | yes | 0.16 | 0.22 | 0.72x |
| cut | `cut -c 1-12` | no annotation | not split | yes | 0.16 | 0.24 | 0.67x |
| cut | `cut -c 1-2` | v1, PaSh grammar | split | yes | 0.14 | 0.22 | 0.65x |
| cut | `cut -c 1-2` | v1, main grammar | split | yes | 0.14 | 0.24 | 0.61x |
| cut | `cut -c 1-2` | naive LLM, run 2026-10-20_135253 | split | yes | 0.14 | 0.23 | 0.64x |
| cut | `cut -c 1-2` | naive LLM, run 2026-10-27_230555 | split | yes | 0.14 | 0.22 | 0.66x |
| cut | `cut -c 1-2` | naive LLM, run 2026-10-28_145447 | split | yes | 0.14 | 0.23 | 0.64x |
| cut | `cut -c 1-2` | naive LLM, run 2026-10-28_152550 | split | yes | 0.14 | 0.22 | 0.65x |
| cut | `cut -c 1-2` | PaSh's own | split | yes | 0.14 | 0.22 | 0.66x |
| cut | `cut -c 1-2` | no annotation | not split | yes | 0.14 | 0.23 | 0.64x |
| grep | `grep a relpath_1` | naive LLM, run 2026-10-20_112956 | split | yes | 0.07 | 0.29 | 0.25x |
| grep | `grep a relpath_1` | naive LLM, run 2026-10-28_135447 | split | yes | 0.07 | 0.29 | 0.24x |
| grep | `grep a relpath_1` | PaSh's own | split | yes | 0.07 | 0.30 | 0.24x |
| grep | `grep a relpath_1` | no annotation | not split | yes | 0.07 | 0.15 | 0.47x |
| grep | `grep -v a relpath_1` | naive LLM, run 2026-10-20_112956 | split | yes | 0.04 | 0.25 | 0.16x |
| grep | `grep -v a relpath_1` | naive LLM, run 2026-10-28_135447 | split | yes | 0.04 | 0.25 | 0.16x |
| grep | `grep -v a relpath_1` | PaSh's own | split | yes | 0.04 | 0.26 | 0.16x |
| grep | `grep -v a relpath_1` | no annotation | not split | yes | 0.04 | 0.12 | 0.32x |
| grep | `grep -y FOO a.txt` | naive LLM, run 2026-10-20_112956 | split | yes | 0.04 | 0.24 | 0.15x |
| grep | `grep -y FOO a.txt` | naive LLM, run 2026-10-28_135447 | split | yes | 0.04 | 0.25 | 0.15x |
| grep | `grep -y FOO a.txt` | PaSh's own | split | yes | 0.04 | 0.25 | 0.15x |
| grep | `grep -y FOO a.txt` | no annotation | not split | yes | 0.04 | 0.12 | 0.30x |
| sort | `sort` | naive LLM, run 2026-10-28_140825 | split | yes | 0.35 | 0.36 | 0.99x |
| sort | `sort` | PaSh's own | split | yes | 0.35 | 0.38 | 0.94x |
| sort | `sort` | no annotation | not split | yes | 0.35 | 0.45 | 0.79x |
| sort | `sort -rn` | naive LLM, run 2026-10-28_140825 | split | yes | 0.44 | 0.38 | 1.17x |
| sort | `sort -rn` | PaSh's own | split | yes | 0.44 | 0.40 | 1.11x |
| sort | `sort -rn` | no annotation | not split | yes | 0.44 | 0.53 | 0.83x |
| sort | `sort -S 512M` | naive LLM, run 2026-10-28_140825 | split | yes | 0.19 | 0.38 | 0.49x |
| sort | `sort -S 512M` | PaSh's own | split | yes | 0.19 | 0.40 | 0.47x |
| sort | `sort -S 512M` | no annotation | not split | yes | 0.19 | 0.25 | 0.74x |

## Speed, on a command that does real work per line

Input: 16,045,882 bytes. Median of 5 runs, every side of the command. The pattern makes grep work hard on each line, so a split can show.

| Script | Side | Side allows a split | PaSh state | Output right | bash (s) | PaSh (s) | bash time / PaSh time |
|---|---|---|---|---|---|---|---|
| `cat mid.txt \| grep '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4'` | v1, PaSh grammar | yes | split | yes | 14.24 | 2.24 | 6.35x |
| `cat mid.txt \| grep '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4'` | naive LLM, run 2026-10-13_193448 | yes | not split | yes | 14.24 | 14.29 | 1.00x |
| `cat mid.txt \| grep '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4'` | naive LLM, run 2026-10-20_112956 | yes | split | yes | 14.24 | 2.25 | 6.32x |
| `cat mid.txt \| grep '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4'` | naive LLM, run 2026-10-28_135447 | yes | split | yes | 14.24 | 2.33 | 6.10x |
| `cat mid.txt \| grep '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4'` | PaSh's own | yes | split | yes | 14.24 | 2.32 | 6.13x |
| `cat mid.txt \| grep '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4'` | no annotation | no | not split | yes | 14.24 | 14.21 | 1.00x |
| `grep -i '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4' f1` | v1, PaSh grammar | no | not split | yes | 17.76 | 17.81 | 1.00x |
| `grep -i '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4' f1` | naive LLM, run 2026-10-13_193448 | yes | not split | yes | 17.76 | 17.93 | 0.99x |
| `grep -i '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4' f1` | naive LLM, run 2026-10-20_112956 | yes | split | yes | 17.76 | 14.83 | 1.20x |
| `grep -i '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4' f1` | naive LLM, run 2026-10-28_135447 | yes | split | yes | 17.76 | 14.80 | 1.20x |
| `grep -i '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4' f1` | PaSh's own | yes | split | yes | 17.76 | 14.82 | 1.20x |
| `grep -i '\(.\).*\1\(.\).*\2\(.\).*\3\(.\).*\4' f1` | no annotation | no | not split | yes | 17.76 | 17.98 | 0.99x |

## Whole benchmark scripts, each side's eight commands loaded together

| Set loaded | Scripts | PaSh split | Not split | PaSh error | Unknown | Output same as bash | Output differs |
|---|---|---|---|---|---|---|---|
| v1-pash | 46 | 27 | 6 | 13 | 0 | 46 | 0 |
| v1-main | 46 | 35 | 6 | 5 | 0 | 46 | 0 |
| naive | 46 | 35 | 5 | 6 | 0 | 46 | 0 |
| pash-own | 46 | 35 | 5 | 6 | 0 | 46 | 0 |
| none | 46 | 0 | 46 | 0 | 0 | 46 | 0 |

Why a script was not split (the last error in PaSh's log, or none):

| Reason | Scripts, per set |
|---|---|
| `no reason logged` | naive (5); pash-own (5); v1-main (6); v1-pash (6) |
| `AssertionError @ ir.py:596 pipe_append` | naive (3); pash-own (3); v1-main (2); v1-pash (10) |
| `NotImplementedError @ dfg_node.py:210 apply_redirections` | naive (2); pash-own (2); v1-main (2); v1-pash (2) |
| `NameError: name 'Arg' is not defined @ ir.py:1454 create_reduce_tree` | naive (1); pash-own (1); v1-main (1); v1-pash (1) |

Per script. A cell lists the commands that ran as more copies than under bash (PaSh's own tr, sed and similar files are in every set).

| Script | v1-pash | v1-main | naive | pash-own | none |
|---|---|---|---|---|---|
| `oneliners/bi-grams.sh` | PaSh error | PaSh error | PaSh error | PaSh error | not split |
| `oneliners/diff.sh` | PaSh error | PaSh error | PaSh error | PaSh error | not split |
| `oneliners/nfa-regex.sh` | split (cat x8, grep x8, tr x8) | split (cat x8, grep x8, tr x8) | split (cat x8, grep x8, tr x8) | split (grep x8, tr x8) | not split |
| `oneliners/set-diff.sh` | PaSh error | PaSh error | PaSh error | PaSh error | not split |
| `oneliners/shortest-scripts.sh` | not split | not split | PaSh error | PaSh error | not split |
| `oneliners/sort-sort.sh` | PaSh error | split (cat x8, tr x8) | split (cat x8, sort x30, tr x8) | split (sort x30, tr x8) | not split |
| `oneliners/sort.sh` | split (cat x8) | split (cat x8) | split (cat x8, sort x15) | split (sort x15) | not split |
| `oneliners/spell.sh` | not split | not split | not split | not split | not split |
| `oneliners/top-n.sh` | PaSh error | split (cat x8, tr x9) | split (cat x8, sort x30, tr x9) | split (sort x30, tr x9) | not split |
| `oneliners/wf.sh` | PaSh error | split (cat x8, tr x9) | split (cat x8, sort x30, tr x9) | split (sort x30, tr x9) | not split |
| `unix50/1.sh` | split (cat x8, cut x8) | split (cat x8, cut x8) | split (cat x8, cut x8) | split (cut x8) | not split |
| `unix50/10.sh` | PaSh error | split (cat x8, cut x16, grep x24, tr x8) | split (cat x8, cut x16, grep x24, sort x30, tr x8) | split (cut x16, grep x24, sort x30, tr x8) | not split |
| `unix50/11.sh` | PaSh error | split (cat x8, cut x16, grep x16, tr x16) | split (cat x8, cut x16, grep x16, sort x30, tr x16) | split (cut x16, grep x16, sort x30, tr x16) | not split |
| `unix50/12.sh` | PaSh error | PaSh error | PaSh error | PaSh error | not split |
| `unix50/13.sh` | split (cat x8, cut x16, grep x8) | split (cat x8, cut x16, grep x8) | split (cat x8, cut x16, grep x8) | split (cut x16, grep x8) | not split |
| `unix50/14.sh` | PaSh error | split (cat x8, cut x8) | split (cat x8, cut x8, sort x15) | split (cut x8, sort x15) | not split |
| `unix50/15.sh` | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cut x8, grep x8) | not split |
| `unix50/16.sh` | PaSh error | PaSh error | PaSh error | PaSh error | not split |
| `unix50/17.sh` | PaSh error | split (cat x8, cut x16, sed x8) | split (cat x8, cut x16, sed x8, sort x15) | split (cut x16, sed x8, sort x15) | not split |
| `unix50/18.sh` | split (cat x8, grep x8, tr x8) | split (cat x8, grep x8, tr x8) | split (cat x8, grep x8, tr x8) | split (grep x8, tr x8) | not split |
| `unix50/19.sh` | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cut x8, grep x8) | not split |
| `unix50/2.sh` | split (cat x8, cut x8) | split (cat x8, cut x8) | split (cat x8, cut x8, sort x15) | split (cut x8, sort x15) | not split |
| `unix50/20.sh` | split (cat x6, cut x5, grep x5) | split (cat x6, cut x5, grep x4) | split (cat x6, cut x5, grep x5) | split (cut x15, grep x8) | not split |
| `unix50/21.sh` | split (cat x8, tr x8) | split (cat x8, tr x8) | split (cat x8, sort x15, tr x8) | split (sort x15, tr x8) | not split |
| `unix50/22.sh` | not split | not split | not split | not split | not split |
| `unix50/23.sh` | split (cat x8, cut x8, grep x16, tr x17) | split (cat x8, cut x8, grep x16, tr x17) | split (cat x8, cut x8, grep x16, tr x17) | split (cut x8, grep x16, tr x17) | not split |
| `unix50/24.sh` | split (cat x8, cut x8) | split (cat x8, cut x8) | split (cat x8, cut x8) | split (cut x8) | not split |
| `unix50/25.sh` | split (cat x8, cut x8) | split (cat x8, cut x8) | split (cat x8, cut x8) | split (cut x8) | not split |
| `unix50/26.sh` | split (cat x8, cut x8, grep x8, tr x9) | split (cat x8, cut x8, grep x8, tr x9) | split (cat x8, cut x8, grep x8, tr x9) | split (cut x8, grep x8, tr x9) | not split |
| `unix50/27.sh` | not split | not split | not split | not split | not split |
| `unix50/28.sh` | split (cat x8, grep x16, tr x25) | split (cat x8, grep x16, tr x25) | split (cat x8, grep x16, tr x25) | split (grep x16, tr x25) | not split |
| `unix50/29.sh` | split (cat x8, tr x9) | split (cat x8, tr x9) | split (cat x8, tr x9) | split (tr x9) | not split |
| `unix50/3.sh` | split (cat x3, cut x8) | split (cat x3, cut x8) | split (cat x3, cut x8) | split (cut x8) | not split |
| `unix50/30.sh` | split (cat x8, grep x8, tr x17) | split (cat x8, grep x8, tr x17) | split (cat x8, grep x8, tr x17) | split (grep x8, tr x17) | not split |
| `unix50/31.sh` | split (cat x8, grep x8, tr x17) | split (cat x8, grep x8, tr x17) | split (cat x8, grep x8, tr x17) | split (grep x8, tr x17) | not split |
| `unix50/32.sh` | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cut x8, grep x8) | not split |
| `unix50/33.sh` | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cut x8, grep x8) | not split |
| `unix50/34.sh` | not split | not split | not split | not split | not split |
| `unix50/35.sh` | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cat x8, cut x8, grep x8) | split (cut x8, grep x8) | not split |
| `unix50/36.sh` | not split | not split | not split | not split | not split |
| `unix50/4.sh` | PaSh error | split (cat x8, cut x8) | split (cat x8, cut x8, sort x30) | split (cut x8, sort x30) | not split |
| `unix50/5.sh` | split (cat x8, cut x8, tr x8) | split (cat x8, cut x8, tr x8) | split (cat x8, cut x8, tr x8) | split (cut x8, tr x8) | not split |
| `unix50/6.sh` | split (cat x8, cut x16, tr x9) | split (cat x8, cut x16, tr x9) | split (cat x8, cut x16, tr x9) | split (cut x16, tr x9) | not split |
| `unix50/7.sh` | split (cat x8, grep x8, tr x8) | split (cat x8, grep x8, tr x8) | split (cat x8, grep x8, tr x8) | split (grep x8, tr x8) | not split |
| `unix50/8.sh` | split (cat x8, grep x16, tr x8) | split (cat x8, grep x16, tr x8) | split (cat x8, grep x16, tr x8) | split (grep x16, tr x8) | not split |
| `unix50/9.sh` | split (cat x8, cut x8, grep x24, tr x8) | split (cat x8, cut x8, grep x24, tr x8) | split (cat x8, cut x8, grep x24, tr x8) | split (cut x8, grep x24, tr x8) | not split |

## Lines not run

- `cut -d';' -f1`: shlex: No closing quotation
- `uniq tee >(awk -F'|' '{print NF,$0}' file | sort -nr | cut -d' ' -f2- \`: shlex: No escaped character
- `rm ./pandoc-2.2.1-1-$(dpkg --print-architecture).deb`: command substitution

## Lines run per command

| Command | Lines |
|---|---|
| cat | 103 |
| cut | 88 |
| grep | 48 |
| sort | 64 |
| cp | 4 |
| rm | 71 |
| split | 1 |
| wc | 3 |

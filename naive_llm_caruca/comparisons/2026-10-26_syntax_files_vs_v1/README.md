# Syntax files compared with v1's: `rm`, `cut`, `sort`, `convert` (2026-10-26)

Scripts and results behind `naive_llm_caruca/syntax_files_vs_v1.md`. Three syntax files per
command are compared: v1's reference (`caruca/src/caruca/syntax_specs/<cmd>.py`), v1's model output
(`outputs/llm-dsl-generation/<cmd>.py`), and the agent's file from naive runs 5, 7, 9 and 8
(`naive_llm_caruca/runs/*_<cmd>_PROMPT_v1/output/<cmd>.py`). v1 at commit `d80324073`.

## Setup (Mac, v1's venv, Python 3.12.9)

Run everything from one working folder that holds the scripts and four grammar packages:

```sh
V1=~/dev/stevens/caruca; R=~/dev/stevens/caruca_v2/naive_llm_caruca/runs
mkdir -p work/{g_ref,g_model,g_agent,g_pash} work/out && cd work
for p in g_ref g_model g_agent g_pash; do touch $p/__init__.py; done
for c in rm cut sort convert; do
  cp $V1/caruca/src/caruca/syntax_specs/$c.py g_ref/
  cp $V1/outputs/llm-dsl-generation/$c.py g_model/
  cp $V1/caruca/src/caruca/pash_syntax_specs/$c.py g_pash/
  cp $(ls -d $R/*_${c}_PROMPT_v1)/output/$c.py g_agent/
done
cp <this folder>/scripts/*.py .
PY=$V1/caruca/.venv/bin/python; C=$V1/eval/user-scripts/invocations.txt
```

## Scripts

| Script | What it does | Output here |
|---|---|---|
| `normalize.py CMD` | Loads each grammar through v1's DSL and records every attribute of every node | `results/normalized_<cmd>.json` |
| `compare.py CMD [--full] [--diffs] [--plusminus]` | Lines up the three files by shared spellings and lists differences (`--plusminus` groups `-x`/`+x` for convert) | `results/three_way_alignment.txt` |
| `oracle_run.py PKG CMD CORPUS OUT` | Runs v1's matcher (`caruca.oracle.oracle`) over the corpus lines whose first word is CMD, with grammar package PKG (`default` = v1's own) | regenerate (15 MB) |
| `levels.py` | Counts the matcher's results at v1's guessing levels (as in `eval/user-scripts/completeness_accumulate.sh`) | `results/matcher_levels.txt` |
| `readcheck.py PKG CMD CORPUS OUT` | Records which grammar node consumed which word, and compares that reading with an emulation of GNU option parsing over coreutils 9.4's option tables | `results/matcher_read_correctness.txt`, `results/read/*.jsonl.gz` (cut, sort) |
| `gnuread.py PKG CMD CORPUS` | Reads the corpus with GNU's rules, taking the option list from the grammar (needs `readcheck_lib.py`) | `results/gnu_rules_reading.txt` |
| `corpus_split.py CORPUS` | Whole corpus, v1's own grammars: how many full matches take a word as an option it is not | `results/corpus_split.json` |
| `render.py` | Renders every option of every grammar as v1's generator writes it | `results/forms.json` |
| `config_count.py PKG CMD K...` (added 2026-10-27) | Exact number of command lines and traced test runs v1 would need at up to K options per line, computed from v1's own objects without listing them; checked against v1's generator for `rm`, `cut`, `sort` and `convert` | `results/test_run_counts.txt` |
| `probe_vm.py forms.json CMDS image OUT` | Runs each rendered option in a minimal valid command line on the real program, in a fresh temporary folder (run inside a VM) | `results/probe_core.jsonl` (pash VM, coreutils 9.4), `results/probe_convert.jsonl` (clone of `naive-golden`, ImageMagick 6.9.12-98) |

`results/scorer_results.txt` holds v1's `eval/cmp_specs.py` run on the real files and on the
single-change copies in `results/scorer_blind_spots/` (each a copy of v1's reference with one
attribute changed; `base_*.py` are the unchanged references).

Validation: with v1's own grammars, `oracle_run.py` gives 24,094 / 5,011 / 5,890 full matches for
`rm` / `sort` / `cut`, the same as v1's committed `eval/user-scripts/oracle_results.txt`, and `levels.py`
gives the same per-level counts as v1's committed `command_counts/`.

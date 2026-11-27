# Independent Verification of Wrong Outputs in the Caruca Rerun (2026-11-27)

Checked against `full_run_caruca_all/results.jsonl.gz`, `regions.jsonl.gz`, `occurrences.jsonl.gz`, `manifest.json`, `logs/`, the Lima VM `pash` (`~/t024/`, read-only), and the generated Caruca files and traces in `~/dev/stevens/caruca/caruca/save_pash_py/`.

## Summary

- **Counts confirmed:** Across all 86 scripts × 4 passes/repeats (`instrumented` rep 1; `plain` reps 1–3), printed stdout differs from `bash` in **76 rows = 19 `(script, set)` pairs = 11 distinct scripts**: **9** under `caruca-pash-all`, **10** under `caruca-main-all`, **0** under `pash-own`, and **0** under `pash-own-copy`. Every failing `(script, set)` produces the exact same wrong `out_sha256` and `out_bytes` across all 4 runs (`rc = 0` throughout). *(Separately, 15 rows of `web-search/engine` across all 4 non-bash sets have `output_files_same_as_bash = false` with `same_as_bash = true` due to non-deterministic output files, not a Caruca stdout error.)*
- **Saved outputs check (VM `~/t024/`):** `run_koala_caruca_all.py:1287-1288` unlinks each run's `.out`, `.standin`, and `.log` immediately after hashing (`for x in (standin, log, out): x.unlink(missing_ok=True)`), keeping only gzipped PaSh logs in `~/t024/out_caruca_all/logs/` and baseline `answers_bash.out` files in `~/t024/runs/<script>/`. Therefore saved Caruca stdout files do not exist to diff line-by-line; baseline `answers_bash.out` contents and byte counts are reported where informative.
- **Builder diagnosis verdict:** **Confirmed for all 11 scripts (19 `(script, set)` pairs)**, with two minor precision notes:
  1. The 8 `sed` scripts use `sed 1d`, `sed 2d`, `sed 3d`, `sed 4d`, `sed 5d`, and `sed 100q` (not only `1d`, `4d`, `100q`).
  2. In `unixfun/23`, `r_split` splits the 31.46 MB input into 1,000,000-byte blocks (31 blocks) distributed round-robin to 8 `r_wrap` workers, and `r_wrap` (`r_wrap.c`) forks a fresh `tr -d '\n'` and `cut -c 1-4` **per block**, yielding `31 × 5 = 155` bytes (rather than `8 × 5 = 40` bytes).
- **Why 3 scripts fail in only one Caruca set:** Both Caruca grammars carry the exact same flawed `stateless` rule for `sed`, `uniq`, and `tr -d`, but the other set fell back to plain bash before reaching the split: `oneliners/spell` under `caruca-main-all` fell back because `tr/main_grammar` had no IO entry for `tr -cs` with 2 operands; `oneliners/top-n` and `unixfun/17` under `caruca-pash-all` hit a PaSh compiler `AssertionError` caused by `sort/pash_grammar`.

| Cause | Scripts (distinct) | Failing `(script, set)` pairs | Verdict |
|---|---:|---:|---|
| Line-addressed `sed` (`1d`, `2d`, `3d`, `4d`, `5d`, `100q`) split per block | 8 | 15 (`caruca-pash-all`: 7, `caruca-main-all`: 8) | Confirmed (precision note: also `2d`, `3d`, `5d`) |
| `uniq` split with plain concatenation (`r_merge`) | 2 | 2 (`caruca-pash-all`: 1, `caruca-main-all`: 1) | Confirmed |
| `tr -d '\n'` split upstream of `cut -c 1-4` | 1 | 2 (`caruca-pash-all`: 1, `caruca-main-all`: 1) | Confirmed (precision note: per `r_split` block, 31 × 5 = 155 B) |
| **Total** | **11** | **19** | **11 / 11 confirmed** |

---

## Reference: Caruca vs. PaSh Parallelizability Decisions

### `sed` (`flags == set()`, `n == 1`)

- **Caruca `pash_grammar`** (`~/dev/stevens/caruca/caruca/save_pash_py/sed/pash_grammar/trace_1/ParallelizabilityInfoGeneratorSed.py:17-20`):
  ```python
  if flags == set() and n == 1:
      # v1: stateless; traced e.g. `sed b` (+1 more)
      self.append_to_parallelizer_list_cc_seq_conc()
      self.append_to_parallelizer_list_rr_seq_conc()
  ```
- **Caruca `main_grammar`** (`~/dev/stevens/caruca/caruca/save_pash_py/sed/main_grammar/trace_1/ParallelizabilityInfoGeneratorSed.py:31-46`):
  ```python
  or (n == 1 and flags in (
      {'--follow-symlinks'},
      {'--posix'},
      {'--sandbox'},
      {'-E'},
      {'-f'},
      {'-l'},
      {'-s'},
      {'-u'},
      {'-z'},
      set(),
  ))
  # v1: stateless; traced e.g. `sed --follow-symlinks b` (+68 more)
  self.append_to_parallelizer_list_cc_seq_conc()
  self.append_to_parallelizer_list_rr_seq_conc()
  ```
  *(In `InputOutputInfoGeneratorSed.py` for `main_grammar`, the corresponding `n == 1` IO branch carries `# v1: non-pure, stateless; traced e.g. sed --debug b (+35 more)` because it groups `--debug` (`non-pure`) with the `stateless` flags.)*
- **PaSh's own** (`~/t024/sets/pash-own/.../ParallelizabilityInfoGeneratorSed.py:211-215`):
  ```python
  if  self.does_first_operand_start_with("-") \
      or self.does_first_operand_start_with("s") \
      or not (self.does_first_operand_contain("d") or self.does_first_operand_contain("q")):
      self.append_to_parallelizer_list_cc_seq_conc()
      self.append_to_parallelizer_list_rr_seq_conc()
  ```
  For `1d`, `2d`, `3d`, `4d`, `5d`, `100q`, the first operand starts with a digit and contains `d` or `q`, so PaSh's own generator **refuses to split** (`says no split`).

### `uniq` (`flags == set()`, `n == 0`)

- **Caruca `pash_grammar`** (`~/dev/stevens/caruca/caruca/save_pash_py/uniq/pash_grammar/trace_1/ParallelizabilityInfoGeneratorUniq.py:17-20`):
  ```python
  if flags == set() and n == 0:
      # v1: stateless; traced e.g. `uniq`
      self.append_to_parallelizer_list_cc_seq_conc()
      self.append_to_parallelizer_list_rr_seq_conc()
  ```
- **Caruca `main_grammar`** (`~/dev/stevens/caruca/caruca/save_pash_py/uniq/main_grammar/trace_1/ParallelizabilityInfoGeneratorUniq.py:17-20`):
  ```python
  if n == 0 and flags in ({'-i', '-u'}, {'-i'}, {'-u'}, set()):
      # v1: stateless; traced e.g. `uniq` (+3 more)
      self.append_to_parallelizer_list_cc_seq_conc()
      self.append_to_parallelizer_list_rr_seq_conc()
  ```
  *(In `InputOutputInfoGeneratorUniq.py` for both grammars, the `n == 0` IO branch has `# v1: non-pure, stateless` because it groups `uniq` (`stateless`) with `uniq -c`, `uniq -d`, etc. (`non-pure`).)*
- **PaSh's own** (`~/t024/sets/pash-own/.../ParallelizabilityInfoGeneratorUniq.py:249-251`):
  ```python
  # just apply the sequential command to the last and first line
  self.append_to_parallelizer_list_cc_seq_adjs()
  self.append_to_parallelizer_list_rr_seq_adjs()
  ```
  PaSh's own file emits only `ADJ_LINES_SEQ` (adjacent-line boundary deduplication, **not implemented** in PaSh), never plain `CONCATENATE`, so PaSh **does not split** `uniq`.

### `tr` (`flags == {'-d'}`, `n == 1`)

- **Caruca `pash_grammar`** (`~/dev/stevens/caruca/caruca/save_pash_py/tr/pash_grammar/trace_1/ParallelizabilityInfoGeneratorTr.py:17-31`):
  ```python
  if (
      (n == 1 and flags in (
          {'-c', '-s'},
          {'-d'},
          {'-s'},
      ))
      or ...
  ):
      # v1: stateless; traced e.g. `tr -c -s string` (+5 more)
      self.append_to_parallelizer_list_cc_seq_conc()
      self.append_to_parallelizer_list_rr_seq_conc()
  ```
- **Caruca `main_grammar`** (`~/dev/stevens/caruca/caruca/save_pash_py/tr/main_grammar/trace_1/ParallelizabilityInfoGeneratorTr.py:17-33`):
  ```python
  if (
      (n == 1 and flags in (
          {'-c', '-s'},
          {'-d', '-t'},
          {'-s', '-t'},
          {'-d'},
          {'-s'},
      ))
      or ...
  ):
      # v1: stateless; traced e.g. `tr -c -s string` (+7 more)
      self.append_to_parallelizer_list_cc_seq_conc()
      self.append_to_parallelizer_list_rr_seq_conc()
  ```
  *(In `InputOutputInfoGeneratorTr.py` for both grammars, the IO branch carries `# v1: non-pure, stateless` because it groups `tr -d` (`stateless`) with `tr -c -d`, `tr -c` (`non-pure`), etc.)*
- **PaSh's own** (`~/t024/sets/pash-own/.../ParallelizabilityInfoGeneratorTr.py:278-286`):
  ```python
  does_delete_newlines: bool = self.does_flag_option_list_contain_at_least_one_of(["-d"]) and \
                               self.does_last_set_effectively_contain_newline()
  if does_delete_newlines:
      self.append_to_parallelizer_list_cc_seq_adjm()
      self.append_to_parallelizer_list_rr_seq_adjm()
  ```
  PaSh's own file detects `\n` in SET1 and emits only `ADJ_LINES_MERGE` (**not implemented** in PaSh), never `CONCATENATE`, so PaSh **does not split** `tr -d "\n"`.

---

## Per-Case Verification (11 Scripts, 19 Failing `(script, set)` Pairs)

### 1. `oneliners/spell` — fails in `caruca-pash-all` (passes in `caruca-main-all` via fallback)

- **Pipeline (region 1):** `cat ${1} | sed "s/[^[:print:]]//g" | col -bx | tr -cs A-Za-z "\\n" | tr A-Z a-z | tr -d "[:punct:]" | sort | uniq | comm -23 - ${dict}`
- **1. Output comparison (all 4 runs: `instrumented` rep 1, `plain` reps 1–3):**
  - `bash`, `pash-own`, `pash-own-copy`, `caruca-main-all`: `10,809` bytes, `sha256 = 83a9657314b52598447ebc4a4a6717fdd23d3d81b27e4821d434054a989a97b9` (`rc = 0`).
  - `caruca-pash-all`: `10,974` bytes (+165 bytes), `sha256 = 66369d3ddde473d7c1d20f6e0f88aa4f3bb38ddc80119f50ead0820908e3eb16` (`rc = 0`, identical across all 4 runs).
  - Saved outputs: Caruca `.out` not kept (`run_koala_caruca_all.py:1288`). Baseline `~/t024/runs/oneliners_spell/answers_bash.out` has 1,234 lines / 10,809 bytes starting with `""`, `ab`, `accenthaving`, `acheit`, `acquaintancehe`.
- **2. Culprit command:** `uniq` (region 1, position 8).
  - `occurrences.jsonl.gz` (`split = true`): `cat` (8), `sed` (8), `col -bx` (8), `tr A-Z a-z` (8), `tr -d "[:punct:]"` (8), **`uniq` (8, `CONSEC_CHUNKS>CONCATENATE`, `ROUND_ROBIN_PLAIN>CONCATENATE`)**.
  - PaSh log (`logs/oneliners_spell__caruca-pash-all__plain.log.gz`): `sort` outputs to `fifo14`, followed by `r_split (in=fifo14, block=1000000)` → 8 × `r_wrap bash -c ' uniq '` → `r_merge` → `comm -2 -3`.
- **3. Caruca decision:** `uniq/pash_grammar/trace_1/ParallelizabilityInfoGeneratorUniq.py:17-20`, branch `if flags == set() and n == 0:`, comment `# v1: stateless; traced e.g. \`uniq\``.
- **4. General validity & PaSh's own:** **Wrong in general.** `uniq` removes adjacent duplicate lines across the whole stream; splitting into blocks and concatenating leaves duplicate lines whenever identical lines cross a block boundary (which `comm -23` then emits repeatedly if absent from `dict.txt`, adding 165 bytes). PaSh's own file does **not** allow a concatenation split (emits unimplemented `ADJ_LINES_SEQ`).
- **5. Verdict:** **Confirmed.** *(Note: `caruca-main-all` did not fail only because `tr/main_grammar` had no IO entry for `tr -cs A-Za-z "\n"`, causing PaSh to fall back to plain bash.)*

---

### 2. `unixfun/17` — fails in `caruca-main-all` (passes in `caruca-pash-all` via fallback)

- **Pipeline (region 1):** `cat ${1} | cut -f 4 | sort -n | cut -c 3-3 | uniq | sed s/\$/"0s"/`
- **1. Output comparison (all 4 runs):**
  - `bash`, `pash-own`, `pash-own-copy`, `caruca-pash-all`: `16` bytes, `sha256 = e2983363796bdc6f9ad758179c1adab507baacf530aa02fd1c2cdcc278b14706` (`rc = 0`).
  - `caruca-main-all`: `44` bytes (+28 bytes, i.e., 11 four-byte lines instead of 4), `sha256 = 982e9f5eae784c07bfb1c2b2332d61d111c7a80f44a275e689ce23a0abe41dda` (`rc = 0`, identical across all 4 runs).
  - Saved outputs: Caruca `.out` not kept. Baseline `~/t024/runs/unixfun_17/answers_bash.out` is 4 lines (`60s\n70s\n80s\n90s\n`, 16 bytes).
- **2. Culprit command:** `uniq` (region 1, position 5).
  - `occurrences.jsonl.gz` (`split = true`): `cat` (8), `cut -f 4` (8), `cut -c 3-3` (8), **`uniq` (8)**, `sed s/$/"0s"/` (8).
  - PaSh log (`logs/unixfun_17__caruca-main-all__plain.log.gz`): `sort -n` → `r_split (in=fifo6, block=1000000)` → 8 × `r_wrap: cut -c 3-3` → 8 × `r_wrap: uniq` → 8 × `r_wrap: sed s/\$/"0s"/` → `r_merge`.
- **3. Caruca decision:** `uniq/main_grammar/trace_1/ParallelizabilityInfoGeneratorUniq.py:17-20`, branch `if n == 0 and flags in ({'-i', '-u'}, {'-i'}, {'-u'}, set()):`, comment `# v1: stateless; traced e.g. \`uniq\` (+3 more)`.
- **4. General validity & PaSh's own:** **Wrong in general.** Same boundary-duplicate defect: `sort -n | cut -c 3-3` produces long runs of `6`, `7`, `8`, `9` spanning multiple 1 MB `r_split` blocks, so each block's `uniq` emits its own `6`/`7`/`8`/`9` and `r_merge` concatenates them (yielding 11 lines = 44 bytes instead of 4 lines = 16 bytes). PaSh's own file does **not** allow this split (`ADJ_LINES_SEQ`, not implemented).
- **5. Verdict:** **Confirmed.** *(Note: `caruca-pash-all` passed only because `sort/pash_grammar` triggered a PaSh compiler `AssertionError` and fell back to plain bash.)*

---

### 3. `oneliners/top-n` — fails in `caruca-main-all` (passes in `caruca-pash-all` via fallback)

- **Pipeline (region 1):** `cat ${1} | tr -c "A-Za-z" "[\\n*]" | grep -v "^\\s*$" | tr A-Z a-z | sort | uniq -c | sort -rn | sed 100q`
- **1. Output comparison (all 4 runs):**
  - `bash`, `pash-own`, `pash-own-copy`, `caruca-pash-all`: `1,247` bytes, `sha256 = b16cf2c64686528981f67675eacb11979ef100c019a992779e4ecc7892ed94ed` (`rc = 0`).
  - `caruca-main-all`: `12,288` bytes (~10× bash's size), `sha256 = b5825d200686d31ea7e05fc826d5aab94b7b395a164d433f4b9e2d3fe09f4933` (`rc = 0`, identical across all 4 runs).
  - Saved outputs: Caruca `.out` not kept. Baseline `~/t024/runs/oneliners_top-n/answers_bash.out` has 100 lines / 1,247 bytes (`311040 the`, `200970 and`, ...).
- **2. Culprit command:** `sed 100q` (region 1, position 8).
  - `occurrences.jsonl.gz` (`split = true`): `cat` (8), `grep -v` (8), `tr A-Z a-z` (8), **`sed 100q` (8)**.
  - PaSh log (`logs/oneliners_top-n__caruca-main-all__plain.log.gz`): `sort -r -n` → `r_split (in=fifo14, block=1000000)` → 8 × `r_wrap: sed 100q` → `r_merge`.
- **3. Caruca decision:** `sed/main_grammar/trace_1/ParallelizabilityInfoGeneratorSed.py:31-46`, branch `or (n == 1 and flags in (..., set()))`, comment `# v1: stateless; traced e.g. \`sed --follow-symlinks b\` (+68 more)`.
- **4. General validity & PaSh's own:** **Wrong in general.** `sed 100q` outputs the first 100 lines of the entire input and quits; running it per `r_split` block outputs up to 100 lines **per block** (expanding 1,247 bytes to 12,288 bytes). PaSh's own file does **not** allow splitting `sed 100q` (first operand contains `q` and does not start with `-` or `s`).
- **5. Verdict:** **Confirmed.** *(Note: `caruca-pash-all` passed only because `sort/pash_grammar` triggered a PaSh compiler `AssertionError` and fell back to plain bash.)*

---

### 4. `unixfun/23` — fails in BOTH `caruca-pash-all` and `caruca-main-all`

- **Pipeline (region 1):** `cat ${1} | tr " " "\\n" | grep "[A-Z]" | tr "[a-z]" "\\n" | grep "[A-Z]" | tr -d "\\n" | cut -c 1-4`
- **1. Output comparison (all 4 runs per set):**
  - `bash`, `pash-own`, `pash-own-copy`: `5` bytes, `sha256 = 9bad3923eaafa2e4005dfa138dbe9fa30a54dc0f1a0bccd4dd0b27b2c784a6e1` (`rc = 0`).
  - `caruca-pash-all` and `caruca-main-all`: `155` bytes (= `31 × 5` bytes), `sha256 = d9e425f04d62d871b142c6335d0cf031a9dbcb9e37f097b2e6d347eeaa1099b3` (`rc = 0`, identical across all 8 Caruca runs).
  - Saved outputs: Caruca `.out` not kept. Baseline `~/t024/runs/unixfun_23/answers_bash.out` is `PORT\n` (5 bytes). Input `~/t024/shadow/unixfun/inputs/9.1_30M.txt` is 31,456,080 bytes (~31 one-MB blocks).
- **2. Culprit command:** `tr -d "\n"` (region 1, position 6), feeding directly into split `cut -c 1-4` (position 7).
  - `occurrences.jsonl.gz` (`split = true` in both sets): `cat` (8), `tr " " "\n"` (8), `grep "[A-Z]"` (8), `tr "[a-z]" "\n"` (8), `grep "[A-Z]"` (8), **`tr -d "\n"` (8)**, `cut -c 1-4` (8). By contrast, in `pash-own`, `tr -d "\n"` is **not split** (`copies = 1`), so PaSh merges before `tr -d "\n"` and only one single line enters `cut -c 1-4`.
  - PaSh logs (`logs/unixfun_23__caruca-pash-all__plain.log.gz` and `caruca-main-all`): a single parallel chain `r_split (9.1_30M.txt, block=1000000)` → 8 × `r_wrap: cat` → 8 × `r_wrap: tr " " "\\n"` → ... → 8 × `r_wrap: tr -d "\\n"` → 8 × `r_wrap: cut -c 1-4` → `r_merge`.
- **3. Caruca decision:**
  - `tr/pash_grammar/trace_1/ParallelizabilityInfoGeneratorTr.py:18-31`: `n == 1 and flags in ({'-c', '-s'}, {'-d'}, {'-s'})`, comment `# v1: stateless; traced e.g. \`tr -c -s string\` (+5 more)`.
  - `tr/main_grammar/trace_1/ParallelizabilityInfoGeneratorTr.py:18-33`: `n == 1 and flags in ({'-c', '-s'}, {'-d', '-t'}, {'-s', '-t'}, {'-d'}, {'-s'})`, comment `# v1: stateless; traced e.g. \`tr -c -s string\` (+7 more)`.
- **4. General validity & PaSh's own:** **Wrong in general in PaSh's line-oriented dataflow model.** Removing newlines merges all input lines into a single line; when `tr -d "\n"` is declared `CONSEC_CHUNKS/ROUND_ROBIN > CONCATENATE`, PaSh does not insert a merge before downstream line-oriented commands. Instead, `r_wrap` executes `tr -d "\n"` and then `cut -c 1-4` independently on each of the 31 `r_split` blocks, so `cut -c 1-4` emits the first 4 characters + `\n` (5 bytes) **for every block** (`31 × 5 = 155` bytes instead of 5 bytes). PaSh's own file does **not** allow this split (detects `\n` in `-d` operand and emits only unimplemented `ADJ_LINES_MERGE`).
- **5. Verdict:** **Confirmed** (with mechanism refinement: `cut -c 1-4` emits 5 bytes per `r_split` block via `r_wrap` — 31 blocks × 5 = 155 bytes — rather than once per 8 worker copies).

---

### 5. `unixfun/26` — fails in BOTH `caruca-pash-all` and `caruca-main-all`

- **Pipeline (region 1):** `cat ${1} | tr " " "\\n" | grep "\"" | sed 4d | cut -d "\"" -f 2 | tr -d "\\n"`
- **1. Output comparison (all 4 runs per set):**
  - `bash`, `pash-own`, `pash-own-copy`: `3,044,246` bytes, `sha256 = a1e3d5e8e95faf805bb007190eef8e3b2f6592b284055783f928d53a5925981d` (`rc = 0`).
  - `caruca-pash-all` and `caruca-main-all`: `3,044,195` bytes (−51 bytes), `sha256 = 4d1b82491b5a473602295271d480e16ac0c1c25ad521d54ea9d905927ed9cd66` (`rc = 0`, identical across all 8 Caruca runs).
  - Saved outputs: Caruca `.out` not kept (baseline `answers_bash.out` is 3,044,246 bytes).
- **2. Culprit command:** `sed 4d` (region 1, position 4). *(Note: `tr -d "\n"` at position 6 is also split by Caruca, but it is the final pipeline stage and deleting `\n` commutes with plain byte concatenation when nothing follows it.)*
  - `occurrences.jsonl.gz` (`split = true` in both sets): `cat` (8), `tr " " "\n"` (8), `grep "\""` (8), **`sed 4d` (8)**, `cut -d "\"" -f 2` (8), `tr -d "\n"` (8).
  - PaSh logs (`logs/unixfun_26__caruca-{pash,main}-all__plain.log.gz`): `r_split (./inputs/9.4_30M.txt, block=1000000)` → 8 × `r_wrap: cat` → `tr` → `grep` → **8 × `r_wrap: sed 4d`** → `cut` → `tr -d "\\n"` → `r_merge`.
- **3. Caruca decision:** `sed/pash_grammar` (`flags == set() and n == 1`, `# v1: stateless; traced e.g. \`sed b\` (+1 more)`) and `sed/main_grammar` (`n == 1 and flags in (..., set())`, `# v1: stateless; traced e.g. \`sed --follow-symlinks b\` (+68 more)`).
- **4. General validity & PaSh's own:** **Wrong in general.** `sed 4d` deletes line 4 of the whole stream; running it per `r_split` block deletes line 4 of every block (−51 bytes across the extra blocks). PaSh's own file refuses to split `sed 4d`.
- **5. Verdict:** **Confirmed.**

---

### 6. `unixfun/28` — fails in BOTH `caruca-pash-all` and `caruca-main-all`

- **Pipeline (region 1):** `cat ${1} | tr " " "\\n" | grep "[A-Z]" | sed 1d | sed 3d | sed 3d | tr "[a-z]" "\\n" | grep "[A-Z]" | sed 3d | tr -c "[A-Z]" "\\n" | tr -d "\\n"`
- **1. Output comparison (all 4 runs per set):**
  - `bash`, `pash-own`, `pash-own-copy`: `1,966,076` bytes, `sha256 = dabbd74052c8b21d6c539c7f9f5875a8f2732b8fc33e6cc0d93c3eb1f584aff7` (`rc = 0`).
  - `caruca-pash-all` and `caruca-main-all`: `1,965,952` bytes (−124 bytes = 31 extra blocks × 4 deleted single-letter lines), `sha256 = 4bbbf1e418d58ff6d241740cdf61f0bf5b8bbe56015d4d00fa4a171fc6209a70` (`rc = 0`, identical across all 8 Caruca runs).
  - Saved outputs: Caruca `.out` not kept (baseline `answers_bash.out` is 1,966,076 bytes).
- **2. Culprit commands:** `sed 1d` (pos 4) and `sed 3d` (positions 5, 6, 9). *(Final `tr -d "\n"` at pos 11 is also split but harmless at pipeline end.)*
  - `occurrences.jsonl.gz` (`split = true` in both sets): `cat`, `tr`, `grep`, **`sed 1d`, `sed 3d` ×3**, `tr`, `grep`, `tr -d "\n"` (all 8 copies).
  - PaSh logs (`logs/unixfun_28__caruca-{pash,main}-all__plain.log.gz`): `r_split (./inputs/9.6_30M.txt, block=1000000)` → ... → **8 × `r_wrap: sed 1d`**, **24 × `r_wrap: sed 3d`** (3 stages × 8 workers) → `r_merge`.
- **3. Caruca decision:** Same `sed` branches (`flags == set() and n == 1`, `# v1: stateless; ...`) in both `pash_grammar` and `main_grammar`.
- **4. General validity & PaSh's own:** **Wrong in general.** Each `sed 1d`/`sed 3d` deletes a global line number; splitting deletes 4 lines from every block instead of 4 lines overall. PaSh's own file refuses to split all four `sed` invocations.
- **5. Verdict:** **Confirmed** (exact commands are `sed 1d` and `sed 3d` ×3).

---

### 7. `unixfun/29` — fails in BOTH `caruca-pash-all` and `caruca-main-all`

- **Pipeline (region 1):** `cat ${1} | sed 2d | sed 2d | tr -c "[A-Z]" "\\n" | tr -d "\\n"`
- **1. Output comparison (all 4 runs per set):**
  - `bash`, `pash-own`, `pash-own-copy`: `4,905,677` bytes, `sha256 = 23441cef9c319c2feaca867c896c981936cd8c3c66a167f947c40450a23d2770` (`rc = 0`).
  - `caruca-pash-all` and `caruca-main-all`: `4,905,420` bytes (−257 bytes), `sha256 = c0f0150eaa5decd113f700c763b671c10d329aa6859baed4655b5687600db596` (`rc = 0`, identical across all 8 Caruca runs).
  - Saved outputs: Caruca `.out` not kept (baseline `answers_bash.out` is 4,905,677 bytes).
- **2. Culprit commands:** `sed 2d` (positions 2 and 3). *(Final `tr -d "\n"` at pos 5 is harmless at pipeline end.)*
  - `occurrences.jsonl.gz` (`split = true` in both sets): `cat` (8), **`sed 2d` ×2 (8 each)**, `tr -d "\n"` (8).
  - PaSh logs (`logs/unixfun_29__caruca-{pash,main}-all__plain.log.gz`): `r_split (./inputs/9.7_30M.txt, block=1000000)` → 8 × `r_wrap: cat` → **16 × `r_wrap: sed 2d`** (2 stages × 8 workers) → `r_merge`.
- **3. Caruca decision:** Same `sed` branches (`flags == set() and n == 1`, `# v1: stateless; ...`) in both grammars.
- **4. General validity & PaSh's own:** **Wrong in general.** `sed 2d | sed 2d` deletes global lines 2 and 3; splitting deletes 2 lines from every block. PaSh's own file refuses to split `sed 2d`.
- **5. Verdict:** **Confirmed** (exact commands are `sed 2d` ×2).

---

### 8. `unixfun/30` — fails in BOTH `caruca-pash-all` and `caruca-main-all`

- **Pipeline (region 1):** `cat ${1} | tr -c "[a-z][A-Z]" "\\n" | grep "[A-Z]" | sed 1d | sed 2d | sed 3d | sed 4d | tr -c "[A-Z]" "\\n" | tr -d "\\n"`
- **1. Output comparison (all 4 runs per set):**
  - `bash`, `pash-own`, `pash-own-copy`: `2,705,996` bytes, `sha256 = 68f65e1be930e050ebec426f4aa6690cb80be38e4f6bac7fde259e735804a4a0` (`rc = 0`).
  - `caruca-pash-all` and `caruca-main-all`: `2,705,876` bytes (−120 bytes = 30 extra blocks × 4 deletions), `sha256 = c86e20a92eb81472717c3df840cb972b1c58acd6e737b2bc1c7b78ecfd32c51b` (`rc = 0`, identical across all 8 Caruca runs).
  - Saved outputs: Caruca `.out` not kept (baseline `answers_bash.out` is 2,705,996 bytes).
- **2. Culprit commands:** `sed 1d`, `sed 2d`, `sed 3d`, `sed 4d` (positions 4–7). *(Final `tr -d "\n"` at pos 9 is harmless at pipeline end.)*
  - `occurrences.jsonl.gz` (`split = true` in both sets): `cat`, `grep`, **`sed 1d`, `sed 2d`, `sed 3d`, `sed 4d`**, `tr -d "\n"` (all 8 copies).
  - PaSh logs (`logs/unixfun_30__caruca-{pash,main}-all__plain.log.gz`): `r_split (in=fifo4, block=1000000)` → 8 × `r_wrap: grep "[A-Z]"` → **8 × each of `r_wrap: sed 1d`, `sed 2d`, `sed 3d`, `sed 4d`** → `r_merge`.
- **3. Caruca decision:** Same `sed` branches (`flags == set() and n == 1`, `# v1: stateless; ...`) in both grammars.
- **4. General validity & PaSh's own:** **Wrong in general.** Deletes 4 lines per block instead of 4 lines overall. PaSh's own file refuses to split all four `sed` commands.
- **5. Verdict:** **Confirmed** (exact commands are `sed 1d`, `sed 2d`, `sed 3d`, `sed 4d`).

---

### 9. `unixfun/31` — fails in BOTH `caruca-pash-all` and `caruca-main-all`

- **Pipeline (region 1):** `cat ${1} | tr -c "[a-z][A-Z]" "\\n" | grep "[A-Z]" | sed 1d | sed 1d | sed 2d | sed 3d | sed 5d | tr -c "[A-Z]" "\\n" | tr -d "\\n"`
- **1. Output comparison (all 4 runs per set):**
  - `bash`, `pash-own`, `pash-own-copy`: `2,705,995` bytes, `sha256 = ae89fd03bf29f86c67152114dc7170aacbe1c84ffdcd32b72877928152d16b38` (`rc = 0`).
  - `caruca-pash-all` and `caruca-main-all`: `2,705,845` bytes (−150 bytes = 30 extra blocks × 5 deletions), `sha256 = d127001f003a5503bbbc4af49d24b1ff2badb947368b14652ac98eea26525fbe` (`rc = 0`, identical across all 8 Caruca runs).
  - Saved outputs: Caruca `.out` not kept (baseline `answers_bash.out` is 2,705,995 bytes).
- **2. Culprit commands:** `sed 1d` ×2, `sed 2d`, `sed 3d`, `sed 5d` (positions 4–8). *(Final `tr -d "\n"` at pos 10 is harmless at pipeline end.)*
  - `occurrences.jsonl.gz` (`split = true` in both sets): `cat`, `grep`, **`sed 1d` ×2, `sed 2d`, `sed 3d`, `sed 5d`**, `tr -d "\n"` (all 8 copies).
  - PaSh logs (`logs/unixfun_31__caruca-{pash,main}-all__plain.log.gz`): `r_split (in=fifo4, block=1000000)` → 8 × `r_wrap: grep` → **16 × `r_wrap: sed 1d`, 8 × `sed 2d`, 8 × `sed 3d`, 8 × `sed 5d`** → `r_merge`.
- **3. Caruca decision:** Same `sed` branches (`flags == set() and n == 1`, `# v1: stateless; ...`) in both grammars.
- **4. General validity & PaSh's own:** **Wrong in general.** Deletes 5 lines per block instead of 5 lines overall. PaSh's own file refuses to split all five `sed` commands.
- **5. Verdict:** **Confirmed** (exact commands are `sed 1d` ×2, `sed 2d`, `sed 3d`, `sed 5d`).

---

### 10. `unixfun/32` — fails in BOTH `caruca-pash-all` and `caruca-main-all`

- **Pipeline (region 1):** `cat ${1} | sed 1d | grep "Bell" | cut -f 2 | wc -l`
- **1. Output comparison (all 4 runs per set):**
  - `bash`, `pash-own`, `pash-own-copy`: `6` bytes, `sha256 = 1882939c41713512949a831e15e0eefe88a58e350fd58654a158cb73e07a5867` (`rc = 0`).
  - `caruca-pash-all` and `caruca-main-all`: `6` bytes (same length, different 5-digit count), `sha256 = 8016baf590f9a7629c394a986553dbfddf8b1052143c77f50bb98fd50ddac01c` (`rc = 0`, identical across all 8 Caruca runs).
  - Saved outputs: Caruca `.out` not kept. Baseline `~/t024/runs/unixfun_32/answers_bash.out` is `16740\n` (6 bytes).
- **2. Culprit command:** `sed 1d` (region 1, position 2).
  - `occurrences.jsonl.gz` (`split = true` in both sets): `cat` (8), **`sed 1d` (8)**, `grep "Bell"` (8), `cut -f 2` (8).
  - PaSh logs (`logs/unixfun_32__caruca-{pash,main}-all__plain.log.gz`): `r_split (./inputs/10_30M.txt, block=1000000)` → 8 × `r_wrap: cat` → **8 × `r_wrap: sed 1d`** → 8 × `r_wrap: grep "Bell"` → 8 × `r_wrap: cut -f 2` → `r_merge` → `wc -l`.
- **3. Caruca decision:** Same `sed` branches (`flags == set() and n == 1`, `# v1: stateless; ...`) in both grammars.
- **4. General validity & PaSh's own:** **Wrong in general.** `sed 1d` is meant to drop only the header line (line 1 of the file); running it on every block drops the first line of each subsequent block as well, reducing the count of matching `"Bell"` lines. PaSh's own file refuses to split `sed 1d`.
- **5. Verdict:** **Confirmed.**

---

### 11. `unixfun/33` — fails in BOTH `caruca-pash-all` and `caruca-main-all`

- **Pipeline (region 1):** `cat ${1} | sed 1d | grep "Bell" | cut -f 2`
- **1. Output comparison (all 4 runs per set):**
  - `bash`, `pash-own`, `pash-own-copy`: `401,760` bytes, `sha256 = 441909be33490c11c77ba2526a35155674d36d3e7e81d429474f501d5cfb0c08` (`rc = 0`).
  - `caruca-pash-all` and `caruca-main-all`: `401,711` bytes (−49 bytes), `sha256 = 4a7defc7144c2e7c0bd109daa94432d3e40c22d89a7d373e413840d7797b04b0` (`rc = 0`, identical across all 8 Caruca runs).
  - Saved outputs: Caruca `.out` not kept (baseline `answers_bash.out` is 401,760 bytes).
- **2. Culprit command:** `sed 1d` (region 1, position 2).
  - `occurrences.jsonl.gz` (`split = true` in both sets): `cat` (8), **`sed 1d` (8)**, `grep "Bell"` (8), `cut -f 2` (8).
  - PaSh logs (`logs/unixfun_33__caruca-{pash,main}-all__plain.log.gz`): `r_split (./inputs/10_30M.txt, block=1000000)` → 8 × `r_wrap: cat` → **8 × `r_wrap: sed 1d`** → 8 × `r_wrap: grep "Bell"` → 8 × `r_wrap: cut -f 2` → `r_merge`.
- **3. Caruca decision:** Same `sed` branches (`flags == set() and n == 1`, `# v1: stateless; ...`) in both grammars.
- **4. General validity & PaSh's own:** **Wrong in general.** Same as `unixfun/32`: `sed 1d` drops the first line of every block instead of only line 1 of the file, dropping 49 bytes of `"Bell"` output. PaSh's own file refuses to split `sed 1d`.
- **5. Verdict:** **Confirmed.**

---

## Attribution: Caruca's Class-Combining Rule (`max` Wins) vs. Other Causes

### A note on `# v1:` comments in the generated `.py` files

Checking `# v1:` comments alone is misleading unless you check both generator files and the raw traces (`traces.json.gz`):
- In **`ParallelizabilityInfoGenerator<Cmd>.py`**, `_par_source()` (`pash_py.py:420-424`) filters `stateless = [c for c in cases if c.label is Parallelizability.S]` **before** calling `_comment(stateless)`. Therefore every `ParallelizabilityInfoGenerator` branch **always** prints `# v1: stateless; ...` — it can never show mixed labels like `non-pure, stateless`.
- In **`InputOutputInfoGenerator<Cmd>.py`**, `# v1: non-pure, stateless` appears for `sed` (main), `uniq` (pash & main), and `tr` (pash & main), but that only means **different `(flags, n)` cases** with the same IO signature were grouped into one `if`/`elif` block (e.g., `uniq` (`stateless`) alongside `uniq -c`, `uniq -d` (`non-pure`)).
- Meanwhile, v1's combining rule (`max`, keeping the most parallelizable label; `memory/caruca_v1_class_combining_rule.md`, `annotator/annotator.py:121-124`, `annotator/pash_py.py:93, 151`) executes **earlier**, both (i) across filesystem/stdin environments within one traced invocation and (ii) across distinct traced invocations that collapse onto the same `(flags, n)` key.

### Direct check of `traces.json.gz` (excluding vacuous unsplit environments)

In Caruca's `Content.variation("split")` (`ir/contents.py:41-54`), only `HUMAN_TEXT`, `MATH`, and `TIME` have `_1`/`_2` split pairs; `JSON` and `IMAGE` have no split pairs and therefore return `non-pure` for **every** command (even plain `cat`). Counting only genuine disagreement among split-capable environments (`HUMAN_TEXT`, `MATH`, `TIME`) or across invocations sharing `(flags, n)`:

| Mechanism | Scripts (of 11) | `(script, set)` pairs (of 19) | Details from `traces.json.gz` |
|---|---:|---:|---|
| **1. Class-combining rule (`max` wins) across environments within one invocation** | **1** (`unixfun/23`, `tr -d`) | **2** | `tr -d string` was labeled **`non-pure` on 2 of 3 split-capable environments** (`HUMAN_TEXT`, `TIME`: deleting `s,t,r,i,n,g` changes lines so `__preserves_line_order` is `False`) and **`stateless` on only 1** (`MATH`, solely because `math_1.txt`/`math_2.txt` contain digits/operators with none of `s,t,r,i,n,g`, making `tr -d string` a no-op). `max` let that single no-op environment override the two `non-pure` split environments. *(Also compound with operand blindness: Caruca never tests `'\n'` and its `(flags, n)` predicate ignores operand text.)* |
| **2. Class-combining rule (`max` wins) across invocations merged under the same `(flags, n)` key** | **8** (`unixfun/26, 28–33`, `oneliners/top-n`, `sed`) | **15** | Because `sed_syntax_spec` wrote `choices=("s/a/b/g")` (a string instead of a 1-tuple), Caruca traced single-char scripts `s`, `/`, `a`, `b`, `g`. `s`, `/`, `a` exited 1 and were dropped. Of the two surviving scripts with `(flags=(), n=1)`, `sed b` (no-op branch) gave `stateless` on all 3 split environments, while **`sed g` gave `non-pure` on all 5 environments** (`__preserves_line_order = False`). In `main_grammar`, `sed relpath_1` also succeeded as a no-op (`r` command → `stateless`). Merging `sed b` and `sed g` (`"true_str": "sed b \| sed g"` in `v1_pash.json`) via `max` (`pash_py.py:93`) let `stateless` beat `non-pure`. Under a conservative (`min`) merge across `(flags, n)`, `(flags=(), n=1)` would have been `non-pure` and all 8 `sed` scripts would have stayed right. *(Also compound with the `choices` tuple bug and operand-value blindness.)* |
| **3. Something else — inadequate split test inputs (no genuine trace disagreement)** | **2** (`oneliners/spell`, `unixfun/17`, `uniq`) | **2** | Plain `uniq` (`flags=(), n=0`) is a single traced invocation, and **all 3 of 3 split-capable environments agreed on `stateless`** (`HUMAN_TEXT`, `MATH`, `TIME`). None of Caruca's three split pairs (`human_1`/`human_2`, `math_1`/`math_2`, `time_1`/`time_2`) has equal lines across the split boundary (`"Here's even more..."` vs `"b"`; `""` vs `"4 * 90"`; `"next friday"` vs `"1980-12-12"`), so `uniq(p1) + uniq(p2) == uniq(p1 + p2)` held by accident in every split test. |

**Bottom line:** **9 of 11** wrong-output scripts (**17 of 19** failing `(script, set)` pairs) involve genuine trace disagreement where Caruca's `max`-wins combining rule was decisive — **1** from per-environment disagreement (`tr -d`) and **8** from cross-invocation merge under the same `(flags, n)` key (`sed`) — while **2 of 11** (**2 of 19** pairs, `uniq`) had unanimous `stateless` agreement across all 3 split-capable environments and came purely from split test inputs lacking a boundary duplicate. *(All 9 combining-rule failures are also reinforced by Caruca's `(flags, n)` schema ignoring operand values and, for `sed`, the `choices=("s/a/b/g")` string-iteration bug.)*

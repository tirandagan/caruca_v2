---
name: project-fig7-campaign
description: 2026-10-27 task 019 - naive agent on all 79 commands of the paper's Fig. 7 ("table 7" in Tiran's words), billed via OpenRouter, every program run logged, quality-checked, budget $120 +- $30 (max $150); Tiran's decisions; prompt v1 currently points at folders that do not exist
metadata:
  type: project
---

**Task 019** (`ai_docs/tasks/019_fig7_commands_naive_campaign.md`), created 2026-10-27 at Tiran's request.
When Tiran says **"table 7"** he means the paper's **Fig. 7** (the paper has only one table, Tab. 1).

**Fig. 7's commands** (read off the figure and checked against a zoomed crop, 2026-10-27): 79 of the 120;
the caption says the other 41 took Caruca under 10 s. 48 have real times (black bars, `fold` … `chown`),
31 only projected times (Caruca stopped at its 5-hour limit, `kill` … `convert`). The full list, in
figure order, is in task 019 section 2. `dd` and `ls` (task 018's pilot runs stopped by a sign-in
failure) are in it; so are the agent's four examples `tee rm uniq grep`.

**Tiran's decisions, 2026-10-27** (answers to four questions):
1. The agent's Claude Code sessions are billed **through OpenRouter** with his new key (not the Max
   subscription). OpenRouter lists `anthropic/claude-fable-5.1` at $10/M input, $50/M output (public
   model list, 2026-10-27). The Claude Code → OpenRouter wiring is untried here.
2. The four examples are run but reported apart from the totals.
3. A "wasted" try = the program refused the command line (non-zero exit + usage-error message); every
   non-zero exit is shown too.
4. Compare with Caruca on all four: Fig. 7 times, exact test-run counts (`config_count.py`), refused share
   of Caruca's generated lines (v1's own tracer), Caruca's GPT-4o step cost via OpenRouter.
Also: rerun the commands already processed (prompt changed); prompt version 1.

**Facts established while writing the task (2026-10-27):**
- Greenberg's commit `89e1156` changed **only** `PROMPT_v1.md`: it now names `formats/annotation.md`,
  `samples/<cmd>/annotation/`, `output/annotation/`, but the folders are still `formats/pash_annotation.md`
  and `samples/<cmd>/pash/`. **A run before the rename points the agent at missing files.**
  `PROMPT_v2.md` still has the old PaSh wording; `formats/pash_annotation.md` names PaSh 6 times.
- `naive-run` finds the program with `command -v`, which prints the bare word for shell built-ins
  (`test`, `kill`), so the prompt would say "binary is at `test`"; `type -P` gives the path. Seen in the
  Mac's bash; not yet run in the VM.
- v1's tracer stores each run's `return_code` and `stderr` (`tracer/data.py` lines 47–49), so Caruca's
  refused share can be judged with the same rule as the agent's.
- The metering relay for v1's model call (task 014) was never built.
- Raw run folders without analysis are about 0.4 MB (run 10); analysed ones 5–10 MB (diagrams).
- Mac: Apple M5 Pro, 18 cores, 24 GiB.

**Review of the task, 2026-10-27 (same day).** Measured from the Bash command text in runs 4–10
(`stream.jsonl`, words at command position; loops undercounted): the agent uses other Fig. 7 programs as
working tools: `cat` 141, `head` 81, `ls` 38, `mkdir` 22 mentions, plus `sed grep rm tail wc touch od col
comm timeout sort cp diff split seq mktemp`. So counting every run of the target program would mix tool
use with probes for about 20 of the 79 commands. Other gaps found and folded into the task: agent refusals are often deliberate probes (run 8: 91 of 352
option words refused), so refusals are split into exploring (before the first output file) vs testing;
Fig. 7 mixes real times at 4 options with the paper's upper-bound projections (section 7.4: 95th
percentile per test run), so a same-Mac Caruca time at up to 2 options is added.

**Tiran's second round, 2026-10-27:** quality check (task 018's program-checked accuracy) for all 79;
Caruca's machine time priced against "a render server of reasonable size" (read as a Render.com 8-CPU
plan; only the rate changes if he meant otherwise); 5 commands × 2 repeat runs (`head cut sort dd cp`);
**budget $120 ± $30, never above $150, cost tracked per command and overall** (`fig7_campaign/costs.md`).
`dirname` and `binwalk` dropped to save budget.

**Cost estimate (2026-10-27):** a straight line through runs 4–10 gives cost ≈ $1.12 + $0.02 per option
(options = distinct option names in v1's curated file; residuals within $0.70). 79 commands ≈ $125,
repeats ≈ $15, Caruca's GPT-4o step $3–6: ≈ $145, near the ceiling, so the repeats run last and only
while the projection stays under $150.

**Caruca-side gaps (read from v1's files, 2026-10-27):** v1's model step reads only
`doc_sources/man/<cmd>.txt` (`llm.py` line 155); there is none for `uglifyjs` or `mogrify` (uglifyjs has
`doc_sources/helpfiles/uglifyjs.help`), so the step cannot run on them unchanged. Shipped GPT-4o output is
missing for `uglifyjs` and `unzip`. v1's curated `mogrify` file lists 3 options.

**Phase 0/1 facts, established 2026-10-27 evening (by test or by reading the source):**
- **OpenRouter account has no credits** (18:47: `/api/v1/credits` total 0; a 1-token request → 402 "This
  account never purchased credits"). Key usage $0, limit $200/month. Campaign zero point $0.00 at 18:46:41
  (`fig7_campaign/campaign_state.json`). OpenRouter's Fable 5.1 prices: $10/M in, $50/M out, **$0.25/M cache
  read**, $12.50/M cache write.
- **Fig. 7 values are exact from the PDF's vector drawing** (page 12; `caruca_side/fig7_values.py`): they
  reproduce every count in the paper's text (80, 103, 24, `convert` 98.71 h vs 98.72). Paper time ÷ exact
  test runs: 37/48 within 3× of 0.0147 s/run; **`diff` and `cp` cannot match** (v1's curated files give 2.4 G
  and 308 M test runs at ≤4 options vs ~3 h reported).
- **bpftrace 0.20 on Ubuntu 24.04's 6.8 kernel aborts on any `curtask->`**, and reading execve arguments at
  syscall entry returned empty strings for 35 of 100 loop runs; arguments now come from **auditd** (complete),
  bpftrace keeps exit status/stderr/fork/start. `ausearch` reads stdin when it is not a terminal: always pass
  `--input-logs`. The audit log records every argv, so **`env KEY=… cmd` leaks the key**; use shell assignments.
- **Ubuntu's unattended upgrades run inside every naive clone** (changed coreutils 6.2→6.3, libc, python mid-
  life of a clone). Disabled in `naive-golden` on 2026-10-27 after one full upgrade; golden now coreutils
  9.4-3ubuntu6.3 (= the `caruca` VM), plus uglifyjs 3.17.4, unzip 6.0, pandoc 3.1.3, auditd. The `caruca` VM
  got ImageMagick 6.9.12.98, uglifyjs, unzip, pandoc at the same versions (its auto-updates left on).
- `naive-run` used `command -v`, which prints the bare word for built-ins (`test`, `kill`); now `type -P`.
- **v1's generated `kill` lines are dangerous and hang v1's tracer:** `kill - HUP -1` (all the user's
  processes) and `kill -s STOP 0` (stops the test's own process group incl. its `timeout`, so the tracer
  waits forever; seen). Measured only inside `unshare --user --map-root-user --pid --fork` with a SIGCONT
  watchdog.
- **v1's tracer cannot run `chroot` on Ubuntu 24.04:** `tracer/tracer.py` line 55 sets PATH to
  `/usr/bin:/bin:/usr/local/sbin:/usr/local/bin`, without `/usr/sbin`, where `chroot` lives; every traced run
  ends "strace: Cannot find executable 'chroot'" (720 of 720, 2026-10-27). Only Fig. 7 command in /usr/sbin.
- **v1's tracer cannot measure `yes` on the 8 GiB `caruca` VM:** it keeps the endless stdout in memory;
  the kernel OOM-killed it at 7.66 GB RSS (exit 137, 2026-10-27). The paper reports 601 s for `yes`.
- First refused-share pass (46/79 by 19:36): 8,734 runs matched no message rule (value refusals like
  "invalid pattern"/"unknown %s directive", plus system conditions); rule table + full message storage +
  rerun planned before any number is used.
- Caruca's own refused share, `cut` (v1 generator + tracer, caruca VM): 1 option/line 20/37 test runs
  refused (65% weighted by v1's repeats); 2 options 273/590 (53% weighted); 0.026 s per test run.

- **2026-10-27 20:32–22:36 the Mac went into "Low Power Sleep" on battery at 1%, despite `caffeinate`**
  (it only holds sleep while there is charge); every VM froze 2 h. Check `pmset -g batt` before long jobs and
  ask Tiran to keep it on mains. A call in flight at sleep was billed by OpenRouter but its reply lost.
- **OpenRouter's usage counter lags ~60–80 s** after a request (smoke test, 2026-10-27); read it only after
  waiting for the expected charge to land (`run_campaign.usage_after`). Per-call bills from
  `GET /api/v1/generation?id=` matched the counter exactly for v1's GPT-4o calls.
- OpenRouter's chat-completion reply carries the call's cost in `usage.cost` (and `cached_tokens`); the
  generation endpoint can time out. v1's GPT-4o calls get OpenAI prompt caching through OpenRouter (4,992 of
  ~6,100 prompt tokens cached per call), so v1's model step for all 77 commands cost $1.70 (2026-10-27).
- **Pilot (2026-10-27, 22:51–23:28):** dd $2.106, ls $2.418, cut $0.908, test $1.868, convert $4.105 billed
  (5 runs $11.41; actual/estimate 0.88; projection for the 79 $111.84; ~7.4 min per run incl. overhead).
- **Where a pilot run's money goes (2026-10-28, from each run's final token totals in `stream.jsonl`).** The totals
  times OpenRouter's list prices equal OpenRouter's bill exactly for all five pilot runs; Claude Code's own
  `total_cost_usd` is 35-47% higher than the bill (it does not know OpenRouter's prices). Output tokens
  (thinking included) are 47-57% of each bill, cache writes 28-40%, cache reads 11-16%, fresh input ~0%. In the
  stream, a message's usage shows only its first output tokens, so per-turn splits from it undercount output.
- **OpenRouter prices on 2026-10-28** ($/M tokens, in / out / cache read / cache write): Fable 5.1 10 / 50 /
  0.25 / 12.50; Opus 5.5 4 / 20 / 0.20 / 5; Sonnet 5.5 2 / 10 / 0.10 / 2.50; Haiku 5.5 0.10 / 0.50 / 0.01 / 0.125.
- **Splitting models inside one session (asked 2026-10-28, not tested).** Claude Code 2.1.293's binary contains
  the strings `opusplan`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`,
  `ANTHROPIC_DEFAULT_FABLE_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL`; no `fableplan`. Whether they work headless
  (`claude -p`) through OpenRouter was not tried.
- **Opus 5.5 at extra-high effort vs Fable 5.1 at medium, same five pilot commands (2026-10-28, measured).**
  Billed: dd $5.49 vs $2.11, ls $3.13 vs $2.42, cut $3.03 vs $0.91, test $4.81 vs $1.87, convert $9.28 vs
  $4.10; total $25.74 vs $11.41 (2.3x) despite Opus's 2.5x lower token prices. Wall time 2.6-7x longer (cut
  920 s vs 131 s). Opus sweeps programs with scripts: 151,970-240,869 program runs per GNU command (Fable:
  116-983). **Tiran chose Fable on cost and time; no quality verdict was reached** (scoring stopped), and he
  had the Opus results deleted (moved to ~/.Trash/caruca_v2_opus55_test_2026-10-28/). The spend is kept in
  campaign_state.json as an unrecorded charge.
- **The golden image's audit log holds about 250,000 program starts per run** (`max_log_file = 50`,
  `num_logs = 10`, rotate). Opus's test run (about 320,000 starts) lost its oldest records, including the
  session's own start, so classify_tries found no session (tries 0). Fable runs stay far below (convert
  19,050). The kernel trace (tries.log) keeps every start regardless.
- **Quality scorer for the campaign** (`naive_llm_caruca/fig7_campaign/quality/`, 2026-10-28): copies of
  task 018's probe/facts extended to dd, ls, test, convert (convert probed with two image files around the
  spelling; test as an operator; dd values after "="), plus a PaSh-annotation behaviour check that runs each
  annotation's classes in pash_annotations 0.2.4 and tests every split claim by running the command on the
  whole input and on pieces. Repairs made after the first pass are listed in each file's header. First-pass
  findings on Fable's pilot files: its dd annotation claims `count=1`/`skip=1` may be split (wrong); PaSh's
  own cut annotation wrongly claims `-z` may be split.
- **Budget raised to $200 (Tiran, 2026-10-28 08:35): "dont worry about the budget - we can go as high as
  $200 - warn me if we are depleting available credits".** The key's own monthly limit is $200 (binding);
  the OpenRouter account holds $300 of credit in total. `fig7_campaign/credit_watch.py` logs what is left
  every 10 minutes and exits with a warning below $40. `run_campaign.py`'s default ceiling is now 200.
- **v1's repository holds no raw data for Fig. 7** (searched 2026-10-28: every file name in the history of
  all remote branches, content on `main` and `paper`, and git-ignored files). `eval/performance/` (commit
  a8847d122, 2024-12-10) has only `count.sh`/`counts.txt`, counts of the command lines `caruca generate`
  prints, no times. The PDF's vector drawing (`caruca_side/fig7_values.tsv`) stays the source.
- Lesson repeated twice that day: `pgrep -f "<name>"` inside a shell whose own command line contains
  `<name>` matches itself and loops forever; use `pgrep -f "[n]ame"` or chain jobs sequentially.

Related: [[project-naive-claude-code-arm]], [[reference-naive-run-playbook]], [[project-v1-llm-via-openrouter]],
[[caruca-v1-llm-retry-mechanics]], [[caruca-v1-value-generation]].

**2026-10-28 12:40 (observed in the ledger):** OpenRouter's usage counter can lag past run_campaign.py's
full wait (300 s + stability check): `uname` recorded $0.00 and `id` $1.49 holds both charges (id's Claude
Code figure / bill = 0.90 vs median 1.44). Ledger left as measured; `compare_table.py` marks such pairs;
`run_campaign.py` sets `bill_late` from the next launch. The ledger's `tokens` field priced at list rates
is only about half of each bill, so it is not the session's whole usage and cannot split a merged charge.
**Cause found 2026-11-03 (read from code, measured over all 89 runs):** `run_campaign.result_event` sums the
`usage` of each `assistant` event in `stream.jsonl`, which holds only the first streamed output tokens.
Ledger output total 81,846 vs 1,306,603 in the `result` events' `usage` (16x; 3.8x to 114x per run).
Input, cache-read and cache-write counts agree. So the token columns of `costs.md` and `ledger.jsonl` are
wrong for output; the `result` event's `usage` is correct. Not fixed as of 2026-11-03.
Interim table: `fig7_campaign/compare_table.py` → `interim_comparison.md`.
**2026-10-28 14:10:** Tiran approved the 10 repeat runs (head cut dd cp sort, repeats 2 and 3) to start as soon
as the main batch ends; warn him if the key's credit drops below $40 (credit_watch.py --below 40 keeps running).
**2026-10-28 15:45:** matplotlib is in neither the repo `.venv` nor system python3 on the Mac; figures are drawn
with `uv run --no-project --with matplotlib==3.9.2 python naive_llm_caruca/fig7_campaign/make_figures.py`
(→ `fig7_campaign/figures/fig7_agent`, `fig7_compare`, `fig7_data.csv`).
**2026-10-28 17:47 (read from code/files):** the quality scorer `fig7_campaign/quality/facts19.py` looks up
`OPERANDS[cmd]` with no default, so it covers only the 5 pilot commands (+ cut/sort/rm/binwalk); every other
Fig. 7 command needs its minimal operands (and fixtures/message rules where special) before phase 5 can run.
Files to score: v1 reference exists for all 79; shipped GPT-4o lacks `uglifyjs`, `unzip`; the 2026-10-27 GPT-4o
rerun lacks `mogrify`, `uglifyjs` (no bundled manual). VMs `t019-probe`, `t018-probe`, `naive-golden` exist
(stopped).
**2026-11-03 review of the campaign (each fact checked over the collected runs that day; scripts were
throwaway, in the session scratchpad):**
- All 89 agent syntax files (79 + 10 repeats) import under v1's real `caruca.ir.syntax` (v1 `.venv` on the
  Mac) and define `<cmd>_syntax_spec`.
- Repeats: option names identical in all 3 runs for `dd` (15), `cut` (11), `head` (7), `cp` (35); `sort`
  differs on `-c`/`--check` grouping and `-y` (31 of 34 names in all 3). Value kinds differ: `cut` r3 uses
  `Range` where r1/r2 use `List(of=Range)`; `head` r2 uses `Size` where r1/r3 use `Integer`. Layout counts
  differ (`cut` 1/1/3). No two runs' files are byte-identical.
- `=` after a value-taking short option (`cut -b=1`, rejected by GNU): 35 of 61 agent files that have such
  an option, 165 of 333 options; v1's reference files for the same commands: 7 of 52 files, 12 of 221.
- Network: 16 of 89 runs have URLs in shell commands; 14 fetch `bootstrap.pypa.io/get-pip.py`; `mogrify`
  r1 downloaded the `pash_annotations` 0.2.4 wheel and probed `https://pypi.org/simple/caruca/` with
  **curl directly** (tool call 26; not via an installer, so outside PROMPT_v1's installer exception);
  `tail` r1 queried PyPI for pash-annotations; `pandoc` has `http://e/` (a test string).
- `head` r3's 24,631 program runs: 24,036 come from tool calls 17-18, a self-written split test
  (`partest.py`, 12,018 runs each), classed "exploring" because it ran before the first output file.
  Distinct option sets across head's 3 runs: 29 / 28 / 52 (runs: 293 / 440 / 24,631).
- Phase 1's `refused_all.sh` finished 2026-10-27 23:24 (77 JSONs in `caruca_side/refused/`) and the v1
  GPT-4o rerun has 77 ledger lines, though task 019's phase-1 checkboxes are still unticked.
- `quality/firstpass.log` (pilot five, before the 2026-10-28 dd/convert repairs) scores the campaign's
  `cut` r1 file 61/76 (80%) vs v1 reference 61/72 (85%): below run 7's 68/76 (89%) that the addendum's
  finding 5 quotes. `quality/results/` is empty: phase 5 has not been rerun since the repairs.
**Who decided the repeat runs (read from the Mac-side transcript, 2026-11-03).** The outer Claude Code session
on the Mac (transcript `~/.claude/projects/-Users-tirandagan-dev-stevens-caruca-v2/847af186-….jsonl`, times in
UTC, local = UTC-4) proposed them on 2026-10-27 at 17:19 local, as decision 3 of its reflection on task 019:
"Repeat 5 commands twice more (about $25), to show how much cost, time and tries vary between identical runs?
I recommend it." Its reason was that one run per command cannot support per-command differences (citing the
1.79x cost spread). Tiran replied "3, yes" (17:28) **without naming commands**; the outer session chose
`head cut sort dd cp` and their rationale (simple filter / earlier runs 7 and 9 / `key=value` syntax / writes
files) when it wrote task 019 section 3.5, which is headed "(Tiran, 2026-10-27)". On 2026-10-28 14:02 Tiran asked
"why do we want to repeat them?", got the three reasons, and approved launching them (14:03). The sessions in
the VMs had no part in it: runs 1-3 of each command got byte-identical `prompt.md`, and none of the 10 repeat
sessions refers to being a repeat.

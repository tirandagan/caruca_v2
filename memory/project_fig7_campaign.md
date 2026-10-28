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
- Lesson repeated twice that day: `pgrep -f "<name>"` inside a shell whose own command line contains
  `<name>` matches itself and loops forever; use `pgrep -f "[n]ame"` or chain jobs sequentially.

Related: [[project-naive-claude-code-arm]], [[reference-naive-run-playbook]], [[project-v1-llm-via-openrouter]],
[[caruca-v1-llm-retry-mechanics]], [[caruca-v1-value-generation]].

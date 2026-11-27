# Brief: run the naive LLM arm on `tr`, `xargs` and `awk`

You are a worker. An orchestrating Claude session gave you this brief. Work only on it.

## Why

The PaSh benchmark suite comparison (`orchestration/brief_builder.md` in this folder's parent) loads
the naive LLM's PaSh annotation files for every command it has. The naive LLM was never run on `tr`,
`xargs` or `awk` (they are not among the paper's figure 7 commands), yet `tr` is in 54 of the suite's
92 scripts, `xargs` in 24 and `awk` in 18. Tiran decided on 2026-11-24 to run the naive LLM on these
three now, exactly as the figure 7 campaign ran its commands, so the comparison can use its files.
Budget: at most $15 in all; each earlier run cost about $2–3.

## Do exactly what the campaign did

Read first: `memory/reference_naive_run_playbook.md`, `memory/project_naive_claude_code_arm.md`,
`memory/project_fig7_campaign.md`, `memory/feedback_readme_is_prompt_variant_log.md`, then
`naive_llm_caruca/README.md` (the prompt-variant log), `naive_llm_caruca/fig7_campaign/run_campaign.py`
(the campaign driver), `naive_llm_caruca/fig7_campaign/ledger.jsonl` (one row per run; see its fields),
`naive_llm_caruca/fig7_campaign/credit_watch.py` and `commands.txt`.

Then, for `tr`, `xargs`, `awk`, one at a time:

- same prompt (`PROMPT_v1`), same model and effort (Fable 5.1, medium, through OpenRouter), same
  golden VM clone procedure, same logger, same collection into `naive_llm_caruca/runs/<stamp>_naive-run-<cmd>_<cmd>_PROMPT_v1/`;
- one run each (`"repeat": 1`); append a ledger row with the same fields as the others plus
  `"added": "2026-11-24 beyond figure 7, for the PaSh suite comparison"`;
- check the OpenRouter balance before the first run and after each; stop and report if it is below $5
  or if a run fails;
- add an entry to `naive_llm_caruca/README.md`'s log in the same turn as the runs (what was run, why,
  observed), as that file's rules require.

Every run's PaSh files must import under `pash-annotations` 0.2.4 (`InputOutputInfoGenerator<Cmd>.py`,
`ParallelizabilityInfoGenerator<Cmd>.py`, `<cmd>.json`). Check that; if a file does not import, say so
in the ledger row and the README entry; do not fix the model's output.

Do not commit or push. Do not run anything in the Lima VM `pash`.

## Amendment 1 (2026-11-24): bill through requesty.ai, not OpenRouter

The OpenRouter key is dead; Tiran has moved to requesty.ai. A placeholder `REQUESTY_API_KEY=REPLACE_ME`
is in `.env`; Tiran will replace it. Add a `requesty` billing path alongside the OpenRouter one (keep
the OpenRouter path as it is, for the record) in `naive_llm_caruca/vm/naive-run`,
`fig7_campaign/run_campaign.py` and `fig7_campaign/credit_watch.py`, then wait for the real key.

How Tiran's other project talks to requesty.ai (read from `~/beprepared/prod/src/lib/llm-platform.ts`
and its task document `ai_docs/tasks/1013_llm_platform_switch_openrouter_to_requesty.md`, which
verified these on 2026-10-31; re-check them here with the real key before the first run):

- Claude Code / Agent SDK path: `ANTHROPIC_BASE_URL=https://router.requesty.ai` (the router **root**:
  the documented `/anthropic/v1/messages` answered 404 there; `/v1/messages` under the root works),
  `ANTHROPIC_AUTH_TOKEN=<the requesty key>`, `ANTHROPIC_API_KEY=` empty, exactly as the OpenRouter path
  sets them now.
- Model names use dashes in the version: `anthropic/claude-fable-5.1` becomes
  `anthropic/claude-fable-5-1`. Confirm the exact id with the free catalogue call
  `GET https://router.requesty.ai/v1/models` (Bearer key) before running; it is also the key check
  (200 = good key, 403 = bad key).
- There is **no balance endpoint**. Record the cost per run from Claude Code's own `result` event
  (`total_cost_usd`) as the campaign already does, and note in the ledger row `"billing": "requesty"`.
  If Requesty reports cost in a response header or usage field that Claude Code exposes, record that
  too; otherwise say the dollar figure is Claude Code's estimate.
- Keep the model and effort the campaign used: Fable 5.1, medium.

Do a $0.02 trial call through the new path first (the arm has a trial-call step already) and show it
answered, then run `tr`, `xargs`, `awk`. If the key is still `REPLACE_ME` when you are ready, stop and
say so; do not poll for it.

## When done

Reply with: the three run folders; cost per run and total; whether each run's PaSh files import; any
failure.

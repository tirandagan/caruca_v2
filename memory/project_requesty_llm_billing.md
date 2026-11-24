---
name: project-requesty-llm-billing
description: 2026-11-24 Tiran switched LLM billing from OpenRouter (key dead, 401) to requesty.ai; how Claude Code is pointed at it (router root as ANTHROPIC_BASE_URL, dashed model ids, no balance endpoint)
metadata:
  type: project
---
**OpenRouter is no longer used.** Its key in `.env` answers 401 (seen 2026-11-24; last good reading
2026-10-28, $40.45 left). Tiran has moved to **requesty.ai** and put a placeholder `REQUESTY_API_KEY=` in
`.env` (git-ignored) for the real key. His other project's switch is documented at
`~/beprepared/prod/ai_docs/tasks/1013_llm_platform_switch_openrouter_to_requesty.md` and coded in
`~/beprepared/prod/src/lib/llm-platform.ts` (note: `~/beprepared/prod`, not `~/dev/beprepared`).

**Facts verified there on 2026-10-31 (not yet re-tested in this repo):**
- Claude Code / Agent SDK: `ANTHROPIC_BASE_URL=https://router.requesty.ai` (the router root; the documented
  `/anthropic/v1/messages` answered 404, `/v1/messages` under the root works), `ANTHROPIC_AUTH_TOKEN=<key>`,
  `ANTHROPIC_API_KEY=` empty.
- Model ids: Anthropic versions use dashes (`anthropic/claude-fable-5.1` → `anthropic/claude-fable-5-1`);
  catalogue = `GET https://router.requesty.ai/v1/models` (free; 200 with a good key, 403 with a bad one).
- No balance endpoint (usage only via a management API); cost appears as `usage.cost` on non-streaming
  responses.

**In this repo:** the naive arm's billing path (`naive_llm_caruca/vm/naive-run`, `fig7_campaign/run_campaign.py`,
`credit_watch.py`) is being given a `requesty` mode by the `naive-runs` worker (2026-11-24) for the
`tr`/`xargs`/`awk` runs; the OpenRouter mode stays for the record.
Related: [[project-fig7-campaign]], [[project-pash-suite-comparison]].

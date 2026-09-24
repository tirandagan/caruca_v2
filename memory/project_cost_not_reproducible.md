---
name: cost-not-reproducible
description: "Identical stage-1 runs (same model, seed, byte-identical tokens) cost 1.79x apart; v2 records no cached_tokens, so prompt caching cannot be confirmed or controlled for"
metadata:
  type: project
---

Found 2026-09-24 while making the first paid runs through the execution console.

Three runs of stage 1 on `cat` — `openai/gpt-4o`, temperature 0, seed 42 honoured, provider
OpenAI, and **6,376 prompt + 152 completion tokens in every one** — cost:

| run | cost |
|---|---|
| `2026-09-14T130803Z_cat_75b37300` | $0.01746 |
| `2026-09-24T164219Z_cat_0c81e1eb` | $0.01746 |
| `2026-09-24T164424Z_cat_3520c45a` | **$0.00978** |

A 1.79x spread with identical tokens and identical configuration. Not a different amount of
work, and not different pricing.

**Most likely provider-side prompt caching, and the project cannot confirm it.** OpenRouter
returns `prompt_tokens_details.cached_tokens` on every response (seen directly in the
2026-09-22 model-id test call). `src/caruca_v2/llm.py` does not read it and
`src/caruca_v2/telemetry.py` has no field for it, so **no run on disk records whether its
prompt was cached.** The timing fits: the cheap run followed an identical one by two minutes;
the two expensive ones are 10 days apart.

**Why it matters:** cost is evaluation dimension 2 and the paper's Q4.

- A campaign runs each cell three times in quick succession, so **mean cost per cell understates
  the cost of running that cell once** — which is the figure anyone actually wants.
- **Any v1-versus-v2 cost comparison must control for cache state**, or it partly measures how
  recently something similar ran.

**How to apply:** do not quote a cost figure as reproducible. Before any Q4 work, add
`cached_tokens` to the telemetry — a small change in `llm.py` plus one additive field, which
turns this from a suspicion into a measurement. Written up with the numbers in
`ai_docs/analysis/findings/cost-is-not-reproducible-at-identical-tokens.md`. Related:
[[harness-report-metric-naming]], [[caruca-paper-unmeasured-contributions]].

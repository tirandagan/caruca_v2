---
id: cost-is-not-reproducible-at-identical-tokens
claim: The same stage-1 run costs different amounts on different attempts despite producing byte-identical token counts, so cost per run is not a reproducible measurement.
status: draft
created: "2026-09-24"
updated: null
dimensions:
  - 2
  - 4
stages:
  - syntax_spec
paper_sections:
  - Q4
  - §7.4
evidence:
  - label: cost of the same run, attempt A
    value: 0.01746
    denominator: one stage-1 run of cat at temperature 0, seed 42, openai/gpt-4o
    metric: cost_usd
    method: measured_cost
    run_ids:
      - 2026-09-24T164219Z_cat_0c81e1eb
      - 2026-09-14T130803Z_cat_75b37300
    campaign_ids: []
    aggregation: as reported by the provider
    scorer_commit: null
    excluded: null
    recheck: null
  - label: cost of the same run, attempt B
    value: 0.00978
    denominator: one stage-1 run of cat at temperature 0, seed 42, openai/gpt-4o, two minutes later
    metric: cost_usd
    method: measured_cost
    run_ids:
      - 2026-09-24T164424Z_cat_3520c45a
    campaign_ids: []
    aggregation: as reported by the provider
    scorer_commit: null
    excluded: null
    recheck: null
  - label: prompt tokens, all three attempts
    value: 6376
    denominator: tokens, identical across all three runs
    metric: prompt_tokens
    method: measured_cost
    run_ids:
      - 2026-09-14T130803Z_cat_75b37300
      - 2026-09-24T164219Z_cat_0c81e1eb
      - 2026-09-24T164424Z_cat_3520c45a
    campaign_ids: []
    aggregation: identical, not averaged
    scorer_commit: null
    excluded: null
    recheck: null
needs_v1_authors: false
source_document: ai_docs/tasks/010_execution_console.md
---

Three runs of stage 1 on `cat` — the same model, the same provider, seed 42 honoured in all
three, and **6,376 prompt plus 152 completion tokens in every one** — cost $0.01746, $0.01746
and $0.00978. A spread of 1.79x with nothing the project controls having changed, and the two
cheapest-to-explain candidates ruled out: the token counts are identical, so it is not a
different amount of work, and the model and provider are identical, so it is not different
pricing.

**The most likely explanation is provider-side prompt caching**, and the project cannot
currently confirm it. OpenRouter reports `prompt_tokens_details.cached_tokens` on every
response; `llm.py` does not read it and `telemetry.py` has no field for it, so no run on disk
records whether its prompt was served from a cache. The signature fits: the cheap run was made
two minutes after an identical one, and the expensive pair were made 10 days apart.

**Why this matters beyond tidiness.** Cost is evaluation dimension 2 and the paper's Q4, and
this makes cost per run something that cannot be reproduced by re-running. Two consequences
follow directly:

- **Repeated samples of the same cell understate cost.** A campaign runs each cell three times
  in quick succession. If the second and third are served from a warm cache, the mean cost of a
  cell is lower than the cost of running that cell once — which is the figure anyone would
  actually want.
- **A v1-versus-v2 cost comparison has to control for cache state**, or it measures how recently
  something similar was run. v1's LLM step has never been metered at all
  ([[v1-published-stage1-accuracy-is-not-reproducible-from-the-artifacts]] is about a different
  gap), so when it is, the same caution applies to it.

**What would settle it:** record `cached_tokens` from the provider's response. It is a small
change to `llm.py` and one additive field in `telemetry.py`, and it turns this from a suspicion
into a measurement. Until then, no cost figure in this project should be quoted without saying
it is one observation rather than a reproducible quantity.

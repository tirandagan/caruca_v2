---
name: v1-llm-via-openrouter
description: "2026-09-22: v1's LLM step reaches OpenAI through OpenRouter via OPENAI_BASE_URL alone; no model-id rewrite needed - OpenRouter accepts the bare gpt-4o (measured, not inferred)"
metadata:
  type: project
---

Tiran's direction on 2026-09-22: **use OpenRouter to reach OpenAI for v1's LLM step**, rather than
setting up a separate OpenAI account and key.

Checked the same day (the first two by inspection, the third by one sub-cent live request):

- v1's `llm.py` reads `OPENAI_API_KEY` and fixes `model="gpt-4o"` in its code (line 110). It never
  passes `api_base`, though DSPy 2.4's `dspy.OpenAI` would accept one.
- The `openai` client in v1's `.venv-llm` (version 1.109.1) builds its default client from the
  environment, so `OPENAI_BASE_URL` redirects every call. Setting that plus `OPENAI_API_KEY` to the
  OpenRouter key points v1 at OpenRouter **with no change to v1's source**. Verified by inspecting
  the client's effective base URL with and without the variable.
- OpenRouter's published model list at `https://openrouter.ai/api/v1/models` contains **no entry
  named `gpt-4o`** — the catalogue identifier is `openai/gpt-4o`, and all 453 identifiers carry a
  provider prefix.

**But the catalogue is not the whole answer, and this is the correction.** A live request on
2026-09-22 with `"model": "gpt-4o"` was **accepted**: HTTP 200, `model` reported back as
`openai/gpt-4o`, usage `{prompt_tokens: 14, completion_tokens: 1}`, cost `$0.000045`. OpenRouter
resolves a bare OpenAI model id to the prefixed one at request time even though it is not listed.

So **no model-id rewrite is needed**. Two environment variables — `OPENAI_API_KEY` set to the
OpenRouter key and `OPENAI_BASE_URL` set to OpenRouter — are the whole change, with nothing between
v1 and the provider. A local forwarder is still wanted, but only to **record** tokens and cost
(v1's code reads neither from the response), not to alter the request.

**Lesson for next time:** the model list answers "under what identifier is model X catalogued", which
is not the same question as "will a request naming X succeed". Inferring the second from the first was
wrong here. Where the difference changes a design, the sub-cent request settles it — this one cost
$0.000045 and removed a component.

**Why it matters:** both sides then take the same route to the same model, which is what makes their
cost comparable, and v1's LLM step gets token and cost figures for the first time — neither v1 nor
the paper records any. The specification lives in `ai_docs/tasks/010_execution_console.md`, decision
8, §6.2 and §7.


Related: [[llm-pipeline-replication]], [[caruca-v1-stage1-baseline]].

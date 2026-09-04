---
name: caruca-v2-baseline-scope
description: "Near-term deliverable for caruca_v2 is a naive single-prompt LLM baseline, not the agentic full-pipeline rebuild"
metadata: 
  node_type: memory
  type: project
  originSessionId: 982a63c8-a401-4c74-b9c4-8e4fcb3ca530
  modified: 2026-08-29T12:45:00.488Z
---

The near-term deliverable for `caruca_v2` is a **naive, non-agentic LLM baseline** — not the ambitious
agentic Claude Code/Agent-SDK pipeline rebuild Tiran originally proposed. Per [[project-key-people]],
Prof. Eiers is a PhD advisor to Tiran (uninvolved in Caruca itself), but he gave this explicit scoping
guidance by email in an Aug 2026 thread with Tiran and Prof. Greenberg (Caruca's PI):

> "For the baseline LLM approach that we will be comparing Caruca against, it doesn't need to be kitted
> out to the max via Claude Code. A straightforward prompt telling the LLM what to produce should be good
> enough. Ideally a prompt detailing the input (command binary + docs) and desired output (specification
> for downstream systems to consume) along with some concrete examples... The goal here is to keep the
> baseline as simple as possible: we don't want to have Claude try to min-max the perfect specification
> synthesizer. Though that would be interesting, it would be another experiment."

**Why:** the point of this baseline is to show *how much better* Caruca's engineered pipeline is than an
off-the-shelf LLM prompt — a weak control, not a strong competitor. Building the full agentic rebuild
first would blur that comparison and is explicitly deferred as separate future work.

**How to apply:** when asked to build "the LLM approach" for `caruca_v2`, default to the simple
single-prompt baseline (command binary + docs in, downstream spec format out, few-shot examples) unless
the user explicitly asks for the agentic pipeline rebuild. The evaluation is three-way: Caruca vs.
naive-LLM baseline vs. ground truth (`~/stevens/caruca/benchmarks/annotations/`). This is captured in
`~/stevens/caruca_v2/CLAUDE.md` under "Two 'LLM approaches' in scope."

**Update 2026-09-03:** Tiran greenlit the full-pipeline LLM replication as tasks 002-004
(see [[llm-pipeline-replication]]) — alongside this control, not replacing it. The
guardrail above still binds task 001 exactly as written; the replication series has its
own principles (minimal per-stage instruction, hard-enforced tools) in
`ai_docs/prep/llm_pipeline_replication.md`.

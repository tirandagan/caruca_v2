---
name: caruca-v2-project-overview
description: "caruca_v2 project basics — v1/v2 naming convention, locations, goal"
metadata: 
  node_type: memory
  type: project
  originSessionId: 982a63c8-a401-4c74-b9c4-8e4fcb3ca530
  modified: 2026-08-29T12:47:57.320Z
---

Tiran calls the original hand-written Caruca implementation **v1** and this new project **v2** — use
that shorthand, don't just say "the baseline" without also knowing it means v1.

- **v1**: `~/stevens/caruca/` (git root; remote `binpash/caruca`, commit `d80324073` as of Aug 2026).
  Private, unlicensed, org-fork-restricted — never copy its source into a public location or personal fork.
- **v2**: `~/stevens/caruca_v2/`, pushed to `github.com/tirandagan/caruca_v2` (private repo Tiran owns).

**Goal:** reproduce/replace v1's pipeline behavior using an LLM/agentic approach, then evaluate the two
systematically (correctness/fidelity, cost/performance via telemetry, coverage, consistency/reproducibility,
reduction in hand-encoded logic). See [[caruca-v2-baseline-scope]] for the current near-term scoping
(naive-LLM baseline first, agentic full-pipeline rebuild deferred) and [[project-key-people]] for who's
involved. Full detail lives in `~/stevens/caruca_v2/CLAUDE.md` — treat that file as authoritative and this
memory as a quick-recall index into it.

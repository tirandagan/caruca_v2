---
name: feedback_caruca_trace_no_oversubscription
description: Caruca's tracer kills each traced run after 2 s (tracer.py timeout=2) and runs 10 at a time, so tracing lanes must never share a VM; parallelise with one 8-vCPU VM per lane (clone the caruca VM), never by running lanes side by side
metadata:
  type: feedback
---

Found 2026-11-26 while converting Caruca's remaining commands for the PaSh suite rerun: five tracing lanes in one
8-vCPU VM drove the load to 30, and `src/caruca/tracer/tracer.py` wraps every traced run in `timeout 2 strace ...`
(line 86, `timeout=2` default). Overloaded runs time out and are dropped or misclassified, which changes the
annotations, so results would not be comparable with the first 8 commands (traced alone).

**Why:** correctness of the traced annotations depends on wall-clock headroom; parallelism inside one VM breaks it.
**How to apply:** one lane per VM. `limactl clone caruca caruca2` (Lima 2.2, source stopped) gives a second 8-vCPU
VM in seconds; the Mac has 18 cores / 24 GB, so two tracing VMs fit only with the pash VM stopped. Discard any
output traced under overload. The lane driver is
`naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/caruca_conversion/trace_batch.sh VM LANE GRAMMAR MAX_COUNT CMD...`.
Related: [[mac_lima_tracing_env]], [[project_pash_suite_comparison]].

---
name: caruca-v2-build-tiering
description: "The 5 priority MVP components stage into Tier 0 (minimal proof, satisfies Eiers) and Tier 1 (gap-driven extensions, satisfies Greenberg/paper continuity)"
metadata:
  type: project
---

Decided 2026-08-29 via a plan-mode review (`~/.claude/plans/review-our-progress-so-delightful-token.md`),
in response to Tiran directly asking whether the plan would satisfy both mentors given the tension between
Eiers' simplicity mandate ([[caruca-v2-baseline-scope]]) and his own wish to capture gaps
(`ai_docs/analysis/evaluation_gaps.md`) and stay flexible for improving on v1.

**The resolution is staging, not rescoping.** The 5 priority components in
`ai_docs/prep/component_functionality.md` don't change — they split into two tiers:

- **Tier 0** (the actual MVP): Baseline Instrumentation + Naive-LLM Baseline (plain docs only) +
  Evaluation Harness limited to Q2-style command-level comparison (safe to build on `cmp_specs.py` as-is,
  see [[caruca-v1-eval-tooling-notes]]) + cost/telemetry + repeated-sampling variance. No sandbox needed.
  This alone answers Eiers' literal ask: "can a naive single prompt do Caruca-style syntax inference, and
  at what cost."
- **Tier 1** (the extension path): Secure Sandbox (v1-faithful profile, then v2-extended), LLM
  Tool-Augmentation, real execution-based Q1 (rerunning PaSh/ShellCheck/Shseer's actual suites — see
  [[caruca-v1-eval-tooling-notes]] for why this is a distinct, heavier task from Q2), Web GUI.

**Why:** a flat, fully-interconnected 5-component MVP (the shape `component_functionality.md` had before
this review) is more than Eiers asked for — building Secure Sandbox and Tool-Augmentation before proving
the core claim inverts the priority CLAUDE.md already states. But dropping them entirely would abandon
Tiran's own gap-capturing vision. Staging gives Eiers a fast, genuinely simple Tier 0, and gives Greenberg
a concrete, evidence-grounded (not speculative) Tier 1 extension path — strengthened by two things the
original paper itself never measured, see [[caruca-paper-unmeasured-contributions]].

**How to apply:** when sequencing work or writing the upcoming `10_generate_build_order_worker.md` roadmap
pass, Tier 0 is the literal build order (build and ship this first, end to end, before starting Tier 1).
When describing the project to either mentor, lead with Tier 0's simplicity for Eiers, lead with Tier 1's
gap-driven extension + the two novel measurements for Greenberg.

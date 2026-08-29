---
name: caruca-v1-eval-tooling-notes
description: "cmp_specs.py's actual behavior (denominator bug), verified ground-truth provenance for syntax_specs/*.py, and why Q1 and Q2 are genuinely different methodologies"
metadata:
  type: project
---

Three facts about v1's actual evaluation tooling, verified by direct code/git read during the 2026-08-29
plan-mode review (`~/.claude/plans/review-our-progress-so-delightful-token.md`), not inferred from
CLAUDE.md's summary. Load-bearing for anything that builds or cites `caruca_v2`'s Evaluation Harness.

**1. Ground-truth provenance for `syntax_specs/*.py` — RESOLVED, safe to trust.** v1's
`eval/llm_correctness.sh` uses the committed `caruca/src/caruca/syntax_specs/*.py` as "ground truth" when
scoring LLM output via `cmp_specs.py`. `CODE_INSIGHTS.md` §2.1 alone reads ambiguously (just says these
were "generated when [the LLM path] ran"). Verified via `git log` on `syntax_specs/ls.py`: 92 commits, 4
human authors including paper co-author Evangelos Lamprou, with commit messages explicitly reading "Fix
ground truths," "Update ground truths with types," "revise gt," "Add various syntax spec ground truths" —
an iterative, multi-author curation history, including a "with types" pass matching the paper's own
reported type-misclassification discrepancy (`cut --delimiter`, String vs. Char). A separate
`pash_syntax_specs/` directory exists too but is a PaSh-testing scaffold ("add simplified specs for quick
pash tests"), not a competing ground-truth candidate. Conclusion: `syntax_specs/*.py` is genuinely v1's
curated ground truth; don't re-litigate this from the CODE_INSIGHTS.md line alone.

**2. `cmp_specs.py`'s `correct_percentage` has a granularity bug — `exact_match` doesn't.**
`count_syntax_elements()` (cmp_specs.py:135) sums dataclass **field** counts despite its name, while
`get_syntaxspec_diff()` (cmp_specs.py:62) counts mismatched **elements**. The resulting
`correct_percentage` (line 152) divides element-granularity by field-granularity — not a true
`matched_args/total_args` fraction. The paper's own argument-level 99.7% figure (§2.2, not §7.2) can't be
reproduced by this field as-is. A derived `exact_match = (diff_count == 0)` is unaffected by the bug and
safe to compute from the script unmodified — this is exactly how the paper's command-level 116/120 number
works. Fix needed before caruca_v2 reports any argument-level percentage: correct the denominator to count
elements, not fields. Not yet fixed — flagged as a concrete task for whenever the Evaluation Harness is
implemented (see `ai_docs/prep/data_telemetry_schema.md`'s Comparison-Result schema, `method` field).

**3. Q1 and Q2 are different methodologies — don't conflate them.** Q2 (§7.2) is argument-by-argument
syntax-spec diffing — what `cmp_specs.py` does. Q1 (§7.1, "spec quality per consumer": PaSh 52/52, POSH
16/17, ShellCheck 6/6, Shseer 18/18) is mostly **execution-based**: PaSh's benchmark suite rerun with
output-hash comparison, ShellCheck's actual 2.2K-test suite rerun ("passing all tests"), Shseer rerun on
12 author bug-scripts — only POSH is diff-only (paper: "we were unable to run it"). `caruca_v2`'s planned
"naive-LLM spec → shared sandbox/annotate → diff against `benchmarks/annotations/`" design (in
`component_functionality.md`) produces a real but genuinely different, lighter thing — labeled
`annotation_diff` in the telemetry schema, not `q1_execution`. True per-consumer execution parity
(matching the paper's 52/52-style numbers) is separate, heavier infrastructure, deferred to
[[caruca-v2-build-tiering]]'s Tier 1.

**How to apply:** whenever implementing or citing the Evaluation Harness's correctness numbers, check
which of these three a given number actually is before presenting it as paper-comparable.

/**
 * Backfill: turn the conclusions already written in prose into finding files.
 *
 * Task 010 §6.6 asks for this - every finding already stated in the parity study, the addendum
 * and the E0 report becomes a file, with its evidence re-checked on the way in.
 *
 * Every number below is copied from the document cited in `source_document`, not recomputed
 * here. The recheck recipes are what allows the console to recompute them; if a number in a
 * document is wrong, the re-check is what surfaces it, and writing a "corrected" value here
 * by hand would defeat that.
 *
 * Re-run with: node scripts/backfill-findings.mjs
 * It refuses to overwrite a file that already exists, so edits survive.
 */
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { stringify } from "yaml";

const here = dirname(fileURLToPath(import.meta.url));
const OUT = join(here, "..", "..", "ai_docs", "analysis", "findings");

const STUDY = "ai_docs/analysis/v1_v2_parity_study.md";
const E0 = "ai_docs/analysis/e0_artifact_pinning.md";

const findings = [
  {
    id: "stage1-neither-system-misses-a-flag",
    claim:
      "At stage 1 neither v2 nor v1's own LLM output misses or invents a single flag on any of the nine parity commands.",
    status: "confirmed",
    dimensions: [1],
    stages: ["syntax_spec"],
    paper_sections: ["Q2"],
    source_document: STUDY,
    evidence: [
      {
        label: "flag F1, v2",
        value: 1.0,
        denominator: "flags in v1's committed reference specification, over 27 scored cells",
        metric: "f1",
        method: "q2_syntax_diff",
        campaign_ids: ["p1_syntax_spec"],
        aggregation: "mean over the arm's scored cells",
        recheck: {
          kind: "campaign_metric",
          campaign: "p1_syntax_spec",
          metric: "f1",
          method: "q2_syntax_diff",
        },
      },
    ],
    body: `Both systems recover every flag v1's committed specification declares, on all nine
commands. Nothing is missing and nothing is invented on either side.

This is the one stage where v1 also uses a model, so it is the only like-for-like comparison in
the study. It is also one of the few results that runs in v1's favour on the finer measure — see
[[stage1-v1-is-slightly-better-at-typing]].`,
  },

  {
    id: "stage1-v1-is-slightly-better-at-typing",
    claim:
      "Where the two stage-1 specifications differ, the difference is argument typing rather than missing flags, and v1 is slightly ahead.",
    status: "confirmed",
    dimensions: [1],
    stages: ["syntax_spec"],
    paper_sections: ["Q2"],
    source_document: STUDY,
    evidence: [
      {
        label: "exact-argument rate, v2",
        value: 0.967,
        denominator: "arguments in the reference specification, over 27 scored cells",
        metric: "exact_argument_rate",
        method: "q2_syntax_diff",
        campaign_ids: ["p1_syntax_spec"],
        aggregation: "mean over the arm's scored cells",
        recheck: {
          kind: "campaign_metric",
          campaign: "p1_syntax_spec",
          metric: "exact_argument_rate",
          method: "q2_syntax_diff",
        },
      },
      {
        label: "exact-argument rate, v1's own LLM output",
        value: 0.983,
        denominator: "arguments in the reference specification, same nine commands",
        metric: "exact_argument_rate",
        method: "q2_syntax_diff",
        aggregation: "measured once; v1's LLM output is a fixed archived artifact",
        excluded: "nothing",
      },
    ],
    body: `The two systems are identical on seven of the nine commands. They differ on \`tail\`
(0.769 against 0.846) and \`tac\` (0.933 against 1.000), and both differences are typing.

Worth stating plainly because most of this study's surprises run the other way. v1's side is a
fixed archived artifact rather than a campaign, so it has no runs to re-check against.`,
  },

  {
    id: "stage1-tac-moves-between-identical-runs",
    claim:
      "At temperature 0, tac's exact-argument rate moves by 0.200 across three otherwise identical stage-1 runs.",
    status: "confirmed",
    dimensions: [4],
    stages: ["syntax_spec"],
    paper_sections: ["Q2"],
    source_document: STUDY,
    evidence: [
      {
        label: "exact-argument rate spread, tac",
        value: 0.2,
        denominator: "three samples of one cell at temperature 0",
        metric: "exact_argument_rate",
        method: "q2_syntax_diff",
        campaign_ids: ["p1_syntax_spec"],
        aggregation: "max minus min across the cell's samples",
      },
    ],
    body: `One command in nine is enough to justify running more than one sample for the whole
experiment programme: with a single sample there is no way to tell "v2 differs from v1" from
"v2 differs from itself". Every other command is stable at 0.000.

**The existing report does not show this.** \`report.py::consistency()\` measures the stage's
headline metric, which at stage 1 is F1 — and F1 is 1.000 in every sample. The console computes
a spread for every metric instead, which is where this appears.

The paper runs its LLM step once per command and reports no variance measurement at all.`,
  },

  {
    id: "stage2-invocations-nearly-complete-environments-mostly-wrong",
    claim:
      "At stage 2 v2 reproduces almost all of v1's distinct invocations but asks for the wrong filesystem environment in about four cases out of five.",
    status: "confirmed",
    dimensions: [1],
    stages: ["generate"],
    paper_sections: ["§4"],
    source_document: STUDY,
    evidence: [
      {
        label: "invocation recall",
        value: 0.878,
        denominator: "v1's distinct invocations at the same bound",
        metric: "recall",
        method: "invocation_set_diff",
        campaign_ids: ["p1_generate"],
        aggregation: "mean over the arm's scored cells",
        recheck: {
          kind: "campaign_metric",
          campaign: "p1_generate",
          metric: "recall",
          method: "invocation_set_diff",
        },
      },
      {
        label: "invocation precision",
        value: 0.568,
        denominator: "v2's distinct invocations",
        metric: "precision",
        method: "invocation_set_diff",
        campaign_ids: ["p1_generate"],
        aggregation: "mean over the arm's scored cells",
      },
      {
        label: "environment agreement",
        value: 0.208,
        denominator: "the 24 cells where the rate is defined",
        metric: "env_agreement_rate",
        method: "config_env_diff",
        campaign_ids: ["p1_generate"],
        aggregation: "mean over cells where it is defined",
        excluded:
          "uniq's cells, where no invocation matched, so there is no environment to compare",
      },
    ],
    body: `The headline of the whole study sits here: v2 reproduces what v1 *writes* far better
than what v1 *means*. It recovers v1's invocation strings almost exactly and then asks for the
wrong filesystem.

**Environment agreement is a correctness rate, not a reach figure.** 0.208 means that of the
environments v2 asked for, roughly one in five is one v1 would also have built. It is not
"coverage" — that word is reserved for real-world reach.

The figure was published once as 0.185 and corrected; see the correction below and
[[stage2-the-0185-error]].`,
    corrections: [
      {
        date: "2026-09-20",
        old_value: 0.185,
        new_value: 0.208,
        why: "The first figure divided by 27 rather than 24, counting uniq's undefined cells as zeros. A rate is computed only over the cases where it is defined.",
      },
    ],
  },

  {
    id: "stage3-most-sessions-never-report",
    claim:
      "At stage 3 the dominant failure is protocol rather than accuracy: most tracing sessions end without ever calling the reporting tool.",
    status: "confirmed",
    dimensions: [1],
    stages: ["trace"],
    paper_sections: ["§5"],
    source_document: STUDY,
    evidence: [
      {
        label: "core interaction recall",
        value: 0.606,
        denominator: "33 core filesystem interaction units v1 recorded, after projection",
        metric: "core.micro.recall",
        method: "trace_recovery_diff",
        campaign_ids: ["p1_trace"],
        aggregation: "pooled over all 12 scored cells",
        recheck: {
          kind: "campaign_metric",
          campaign: "p1_trace",
          metric: "core.micro.recall",
          method: "trace_recovery_diff",
        },
      },
      {
        label: "core interaction precision",
        value: 0.8,
        denominator: "the core interaction units v2 reported",
        metric: "core.micro.precision",
        method: "trace_recovery_diff",
        campaign_ids: ["p1_trace"],
        aggregation: "pooled over all 12 scored cells",
      },
    ],
    body: `Where a session did report, recovery is partial. Where it did not — most of them —
there is nothing to score at all.

**Recovery and reporting are different failures and must not be blended.** A session that ran
and observed nothing is a different outcome from one that ended without calling the reporting
tool, and a count of zero interactions cannot tell them apart. The console distinguishes them
from the session's recorded status.

These figures were corrected once already; see [[stage3-first-figures-were-single-sample]].`,
    corrections: [
      {
        date: "2026-09-20",
        old_value: "0.769 precision / 0.588 recall",
        new_value: "0.800 precision / 0.606 recall",
        why: "The first figures were computed by hand from one cell per command rather than all three samples, because the campaign ledger carried no stage-3 scores at all.",
      },
    ],
  },

  {
    id: "stage3-pwd-moves-between-identical-runs",
    claim:
      "At temperature 0, pwd's stage-3 core recall moves by 0.400 across three otherwise identical runs.",
    status: "confirmed",
    dimensions: [4],
    stages: ["trace"],
    paper_sections: ["§5"],
    source_document: STUDY,
    evidence: [
      {
        label: "core recall spread, pwd",
        value: 0.4,
        denominator: "three samples of one cell at temperature 0 (1.000, 1.000, 0.600)",
        metric: "core.micro.recall",
        method: "trace_recovery_diff",
        campaign_ids: ["p1_trace"],
        aggregation: "max minus min across the cell's samples",
      },
    ],
    body: `The second reproducibility result, and the second one the existing report
understates: it shows 0.250, which is the spread in F1 rather than in recall.

Taken with [[stage1-tac-moves-between-identical-runs]], two of the four stages show run-to-run
variation at temperature 0 on at least one command. That is itself a result — the paper reports
no variance measurement of any kind.`,
  },

  {
    id: "stage4-class-agreement-pooled-over-three-runs",
    claim:
      "On the strict instrument, v2 agrees with the hand-curated ground truth on parallelizability class in 25 of 77 aligned cases.",
    status: "corrected",
    dimensions: [1],
    stages: ["annotate"],
    paper_sections: ["Q1", "§6"],
    source_document: STUDY,
    needs_v1_authors: true,
    evidence: [
      {
        label: "parallelizability-class agreement, v2, strict",
        value: 0.325,
        denominator: "77 cases aligned across all three runs (25 agreeing)",
        metric: "agreement.pclass",
        method: "annotation_diff",
        campaign_ids: ["p1_annotate"],
        aggregation:
          "pooled: agreeing cases summed over aligned cases summed, across samples and commands",
        recheck: { kind: "campaign_pooled", campaign: "p1_annotate", stage: "annotate" },
      },
      {
        label: "parallelizability-class agreement, v1, same seven commands, strict",
        value: 0.172,
        denominator: "64 aligned cases (11 agreeing)",
        metric: "agreement.pclass",
        method: "annotation_diff",
        aggregation: "measured once against the same ground truth",
      },
    ],
    body: `**Two figures exist and neither may be quoted without saying which it is.** On the
strict instrument — this project's own — v2 agrees in 25 of 77 aligned cases. Under the
relaxation the paper's own evaluation applies, where telling parallelizable-pure from
non-parallelizable-pure is not required, both systems score roughly three times higher: 88.3%
for v2 and 65.6% for v1.

**A note for anyone quoting the task document.** \`ai_docs/tasks/010_execution_console.md\`
states this as "v2 10 of 33, v1 11 of 64" in two places. 10 of 33 is v2's *first run only* —
the figure first published and since superseded. The parity study itself carries the correct
pooled figure. See [[stage4-the-denominator-is-not-fixed]].

Needs the v1 authors' input: which of the two instruments the resubmission should lead with is
a question about the paper's own evaluation, not about this measurement.`,
    corrections: [
      {
        date: "2026-09-22",
        old_value: "10 of 33",
        new_value: "25 of 77",
        why: "The first edition reported v2's first run only. Pooling all three samples gives 25 of 77.",
      },
    ],
  },

  {
    id: "stage4-the-denominator-is-not-fixed",
    claim:
      "At stage 4 the denominator is itself a result: how many cases align at all depends on what v2 produced, so it moves between samples.",
    status: "draft",
    dimensions: [1, 4],
    stages: ["annotate"],
    paper_sections: ["Q1"],
    source_document: STUDY,
    evidence: [
      {
        label: "aligned cases, sample 0",
        value: 33,
        denominator: "a count, not a rate: cases aligned in that sample",
        metric: "agreement.comparable",
        method: "annotation_diff",
        campaign_ids: ["p1_annotate"],
        aggregation: "summed over the nine commands in one sample",
      },
      {
        label: "aligned cases, sample 2",
        value: 14,
        denominator: "a count, not a rate: cases aligned in that sample",
        metric: "agreement.comparable",
        method: "annotation_diff",
        campaign_ids: ["p1_annotate"],
        aggregation: "summed over the nine commands in one sample",
      },
    ],
    body: `The three samples align 33, 30 and 14 cases. That is not noise in a measurement — it
is the measurement changing shape, because alignment depends on the annotation v2 produced.

Two consequences:

- **A per-sample rate cannot simply be averaged.** A sample aligning 2 cases would carry the
  same weight as one aligning 14. The figures in [[stage4-class-agreement-pooled-over-three-runs]]
  are pooled for that reason.
- **"Movement between samples" is not a single number here.** Both parts of the ratio move, so
  a spread figure describes neither. The console shows each sample's own counts instead.`,
  },

  {
    id: "stage4-two-commands-exceed-the-context-window",
    claim:
      "v2 cannot annotate rm or tee at all: their traces make a prompt larger than the model's context window.",
    status: "confirmed",
    dimensions: [1, 3],
    stages: ["annotate"],
    paper_sections: ["Q1", "§6"],
    source_document: STUDY,
    evidence: [
      {
        label: "cells that produced no annotation",
        value: 6,
        denominator: "27 stage-4 cells; all six failures are rm and tee, in every sample",
        metric: "status",
        method: "annotation_diff",
        campaign_ids: ["p1_annotate"],
        aggregation: "count of cells with status error",
      },
      {
        label: "prompt tokens requested for rm",
        value: 224394,
        denominator: "tokens, against the endpoint's 128,000 limit",
        metric: "prompt_tokens",
        method: "measured_cost",
        campaign_ids: ["p1_annotate"],
        aggregation: "as reported by the provider's rejection",
      },
    ],
    body: `This is a ceiling intrinsic to the approach, not a quality result, and it should be
reported as one. v1 has no equivalent limit: it derives its specification procedurally from the
trace file, however large that file is.

Stating it as "v2 scored 0 on rm and tee" would be wrong twice over — it never produced an
annotation to score, and the failure is about input size rather than about reasoning.

The practical consequence for the experiment programme is that any stage-4 result is implicitly
conditioned on the trace fitting in a context window, and the commands that do not fit are
exactly the ones with the most filesystem activity.`,
  },

  {
    id: "v1-published-stage1-accuracy-is-not-reproducible-from-the-artifacts",
    claim:
      "v1's committed LLM specifications score 78 of 116 by v1's own instrument, against the paper's published 116 of 120.",
    status: "confirmed",
    dimensions: [1],
    stages: ["syntax_spec"],
    paper_sections: ["Q2", "§7.2"],
    source_document: "memory/caruca_v1_stage1_baseline.md",
    needs_v1_authors: true,
    evidence: [
      {
        label: "v1 specifications matching ground truth, by v1's own cmp_specs.py",
        value: 78,
        denominator: "116 commands with both a specification and a man page",
        metric: "exact",
        method: "q2_syntax_diff",
        aggregation: "count of exactly matching specifications",
      },
      {
        label: "the same, by an independent scorer",
        value: 83,
        denominator: "116 commands with both a specification and a man page",
        metric: "exact",
        method: "q2_syntax_diff",
        aggregation: "count of exactly matching specifications",
      },
    ],
    body: `The published 116 of 120 cannot be reproduced from the artifacts the repository
ships. Use 78 of 116 as the stage-1 baseline and cite 116 of 120 only as the published figure,
with both denominators stated.

This needs the v1 authors: the gap may be a different artifact set, a different instrument, or
a scoring rule that is not in the code. It is not a claim that the paper is wrong, and the
resubmission should not present it as one.`,
  },

  {
    id: "v1-generate-number-cannot-be-used-as-a-denominator",
    claim:
      "v1's `generate --number` disagrees with what v1 actually prints on every command checked, and crashes outright on fourteen.",
    status: "confirmed",
    dimensions: [2, 3],
    stages: ["generate"],
    paper_sections: ["Q4", "§7.4"],
    source_document: E0,
    evidence: [
      {
        label: "commands where --number disagrees with actual emission",
        value: 90,
        denominator: "90 commands that enumerate fully under a 500,000-line cap",
        metric: "hint_vs_emitted",
        method: "q2_syntax_diff",
        aggregation: "count of disagreeing commands",
      },
      {
        label: "commands where --number crashes",
        value: 14,
        denominator: "120 man-page commands",
        metric: "hint_error",
        method: "q2_syntax_diff",
        aggregation: "count, including pwd, which is in the parity set",
      },
    ],
    body: `\`--number\` uses a different code path from the enumeration it claims to count. It
must never be used as a denominator or as a cost estimate.

The console's pre-flight counts by running \`generate\` at the chosen limits and counting the
lines it prints, which is what \`mkdir\` at v1's defaults shows as 4,240 printed and 1,094
distinct.

Twelve of the fourteen crashes are \`ValueError: max() iterable argument is empty\` on
mostly-zero-flag commands — a latent v1 defect worth an upstream issue.`,
  },
];

mkdirSync(OUT, { recursive: true });
let written = 0;
let skipped = 0;

for (const finding of findings) {
  const { body, ...frontmatter } = finding;
  const path = join(OUT, `${frontmatter.id}.md`);
  if (existsSync(path)) {
    skipped += 1;
    continue;
  }

  const full = {
    id: frontmatter.id,
    claim: frontmatter.claim,
    status: frontmatter.status,
    created: "2026-09-22",
    updated: null,
    dimensions: frontmatter.dimensions ?? [],
    stages: frontmatter.stages ?? [],
    paper_sections: frontmatter.paper_sections ?? [],
    evidence: (frontmatter.evidence ?? []).map((e) => ({
      label: e.label,
      value: e.value,
      denominator: e.denominator,
      metric: e.metric,
      method: e.method,
      run_ids: e.run_ids ?? [],
      campaign_ids: e.campaign_ids ?? [],
      aggregation: e.aggregation ?? null,
      scorer_commit: e.scorer_commit ?? null,
      excluded: e.excluded ?? null,
      recheck: e.recheck ?? null,
    })),
    corrections: frontmatter.corrections ?? [],
    needs_v1_authors: frontmatter.needs_v1_authors ?? false,
    source_document: frontmatter.source_document ?? null,
  };

  writeFileSync(path, `---\n${stringify(full, { lineWidth: 0 }).trimEnd()}\n---\n\n${body.trim()}\n`);
  written += 1;
}

console.log(`${written} written, ${skipped} already existed → ${OUT}`);

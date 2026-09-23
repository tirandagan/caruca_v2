import { listRuns } from "../data/runs.js";
import { listV1Runs } from "../data/v1Runs.js";
import { indexedRunIds } from "../data/metricsDb.js";
import { Badge, Callout, count } from "../components/ui.js";
import { RunsTable } from "../components/RunSelection.js";

// Every page reads the run directories at request time, so a run that finishes while the page
// is open shows up on reload. Nothing here is cached or pre-rendered.
export const dynamic = "force-dynamic";

const STAGE_LABEL: Record<string, string> = {
  syntax_spec: "1 · specification",
  generate: "2 · invocations",
  trace: "3 · tracing",
  annotate: "4 · annotation",
};

export default function RunsPage() {
  const { runs, startedWithoutRecord, unreadable } = listRuns();
  const v1 = listV1Runs();
  const indexed = indexedRunIds();
  const orphaned = [...indexed].filter(
    (id) => !runs.some((run) => run.runId === id),
  ).length;

  return (
    <main className="page page--wide">
      <div className="accent-bar" />
      <div className="page__head">
        <h1>Runs</h1>
        <Badge mono>{count(runs.length)} with a record</Badge>
        {startedWithoutRecord.length > 0 ? (
          <Badge tone="warn" mono>
            {count(startedWithoutRecord.length)} started, recorded nothing
          </Badge>
        ) : null}
        <Badge tone="muted" mono>
          {count(v1.runs.length)} v1 runs
        </Badge>
      </div>

      {/*
        Three sources, three different counts. Saying which one a number is, every time it is
        shown, is the whole point of this screen's header - a run count quoted without its
        basis is the same mistake as a rate quoted without its denominator.
      */}
      <p className="page__sub">
        Counted three ways, because they disagree: {count(runs.length + startedWithoutRecord.length)}{" "}
        directories on disk, {count(runs.length)} holding a manifest, {count(indexed.size)} known
        to <span className="code-inline">eval/metrics.db</span>
        {orphaned > 0 ? ` (${count(orphaned)} of those have no directory left)` : null}.
      </p>

      <div className="stack">
        {startedWithoutRecord.length > 0 ? (
          <Callout title="Started and recorded nothing" tone="warn">
            <p>
              {count(startedWithoutRecord.length)} directories are empty. A run directory is
              created when the run starts, and its manifest is written only when the run ends,
              so a run that dies in between leaves a shell behind. These are counted rather
              than hidden: a failure that cannot be seen cannot be reported.
            </p>
            <p>
              They are listed at the bottom of this page and can be selected for deletion.
              Nothing can depend on them, so they are the one group that is safe to clear out
              without thinking about it.
            </p>
          </Callout>
        ) : null}

        {orphaned > 0 ? (
          <Callout title="Known to the database, gone from disk" tone="neutral">
            <p>
              {count(orphaned)} runs have rows in <span className="code-inline">eval/metrics.db</span>{" "}
              but no directory. Their per-turn tokens, cost and timing survive; their prompts,
              responses and outputs do not, so they cannot be replayed or inspected.
            </p>
          </Callout>
        ) : null}

        {unreadable.length > 0 ? (
          <Callout title="Unreadable" tone="warn">
            <p>
              {unreadable.length} directories hold data that could not be parsed. This is a
              defect to investigate, not a run that died.
            </p>
          </Callout>
        ) : null}

        {v1.runs.length === 0 ? (
          <Callout title="No v1 runs yet" tone="neutral">
            <p>
              v1 writes no run record of its own, so one exists only for a run this console
              started. Live runs arrive in Phase 5; until then this list is v2&apos;s runs only.
            </p>
          </Callout>
        ) : null}

        <RunsTable
          runs={runs.map((run) => ({
            runId: run.runId,
            stage: run.stage,
            command: run.command,
            model: run.model,
            turns: run.turns,
            promptTokens: run.promptTokens,
            completionTokens: run.completionTokens,
            costUsd: run.costUsd,
            status: run.status,
            hasRecording: run.hasRecording,
          }))}
          emptyRunIds={startedWithoutRecord}
        />
      </div>
    </main>
  );
}

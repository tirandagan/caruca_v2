"use client";

/**
 * Selecting runs and deleting them.
 *
 * Deletion is irreversible on disk, so the flow is deliberately three steps rather than one
 * click: select, see what it would cost, then confirm by typing. The middle step is the
 * important one - it names every campaign result and written-up finding that depends on what
 * is about to go, because those are the things that break silently.
 *
 * Tiran's decision on 2026-09-22: a cited run is warned about clearly and then allowed
 * through, not refused.
 */
import { useMemo, useState, useTransition } from "react";
import Link from "next/link";
import type { DeletionAnalysis, DeletionResult } from "../data/deleteRuns.js";
import { previewDeletion, confirmDeletion } from "../app/actions.js";
import { Badge, Callout, Card, count, usd } from "./ui.js";

const CONFIRM_WORD = "delete";

function bytes(value: number): string {
  if (value < 1024) return `${value} B`;
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KB`;
  return `${(value / (1024 * 1024)).toFixed(1)} MB`;
}

/**
 * One row of the runs table, as plain data.
 *
 * Everything crossing from the server to this component has to be serialisable, which is why
 * the table is rendered here rather than passed in as a function - a render prop cannot cross
 * that boundary.
 */
export interface RunRow {
  readonly runId: string;
  readonly stage: string;
  readonly command: string;
  readonly model: string;
  readonly turns: number;
  readonly promptTokens: number;
  readonly completionTokens: number;
  readonly costUsd: number;
  readonly status: "ok" | "failed";
  readonly hasRecording: boolean;
}

const STAGE_LABEL: Record<string, string> = {
  syntax_spec: "1 · specification",
  generate: "2 · invocations",
  trace: "3 · tracing",
  annotate: "4 · annotation",
};

export function RunsTable({
  runs,
  emptyRunIds,
}: {
  runs: RunRow[];
  /** Directories whose run died before recording anything. Nothing can depend on these. */
  emptyRunIds: string[];
}) {
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [analysis, setAnalysis] = useState<DeletionAnalysis | null>(null);
  const [result, setResult] = useState<DeletionResult | null>(null);
  const [confirmText, setConfirmText] = useState("");
  const [reason, setReason] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  const ids = useMemo(() => [...selected], [selected]);

  const toggle = (runId: string) => {
    setSelected((current) => {
      const next = new Set(current);
      if (next.has(runId)) next.delete(runId);
      else next.add(runId);
      return next;
    });
    // Any change to the selection invalidates the report that described the old one.
    setAnalysis(null);
    setConfirmText("");
    setResult(null);
  };

  const clear = () => {
    setSelected(new Set());
    setAnalysis(null);
    setConfirmText("");
  };

  const checkbox = (runId: string) => (
    <input
      type="checkbox"
      checked={selected.has(runId)}
      onChange={() => toggle(runId)}
      aria-label={`Select run ${runId}`}
    />
  );

  const review = () => {
    setError(null);
    startTransition(async () => {
      try {
        setAnalysis(await previewDeletion(ids));
      } catch (cause) {
        setError((cause as Error).message);
      }
    });
  };

  const doDelete = () => {
    setError(null);
    startTransition(async () => {
      try {
        const deletion = await confirmDeletion(ids, reason);
        setResult(deletion);
        setAnalysis(null);
        setSelected(new Set());
        setConfirmText("");
        setReason("");
      } catch (cause) {
        setError((cause as Error).message);
      }
    });
  };

  return (
    <>
      {result ? (
        <Callout title="Deleted" tone="neutral">
          <p>
            Removed {result.deleted.length} run{result.deleted.length === 1 ? "" : "s"},{" "}
            {count(result.filesRemoved)} files ({bytes(result.bytesRemoved)}) and{" "}
            {count(result.metricsRowsRemoved)} database row
            {result.metricsRowsRemoved === 1 ? "" : "s"}. Logged to{" "}
            <span className="mono">eval/deleted_runs.jsonl</span>.
          </p>
          <p>
            These files are still in the repository&apos;s history. To bring them back:{" "}
            <span className="mono">git checkout -- eval/runs</span>, then{" "}
            <span className="mono">caruca-v2 metrics rebuild</span>.
          </p>
          {result.failed.length > 0 ? (
            <p className="mono">
              Not deleted: {result.failed.map((f) => `${f.runId} (${f.reason})`).join("; ")}
            </p>
          ) : null}
        </Callout>
      ) : null}

      {error ? (
        <Callout title="That did not work" tone="warn">
          <p className="mono">{error}</p>
        </Callout>
      ) : null}

      {selected.size > 0 && !analysis ? (
        <div className="card" style={{ position: "sticky", top: 0, zIndex: 2 }}>
          <div className="card__body row">
            <Badge tone="info" mono>
              {selected.size} selected
            </Badge>
            <button className="btn" type="button" onClick={clear}>
              Clear
            </button>
            <span className="spacer" />
            <button className="btn" type="button" onClick={review} disabled={pending}>
              {pending ? "Checking…" : "Review deletion"}
            </button>
          </div>
        </div>
      ) : null}

      {analysis ? (
        <div className="card">
          <header className="card__head">
            <span className="label">
              Deleting {analysis.runs.length} run{analysis.runs.length === 1 ? "" : "s"} — review
              first
            </span>
          </header>
          <div className="card__body stack">
            <div className="metrics">
              <div>
                <div className="metric__label">Runs</div>
                <div className="metric__value">{analysis.runs.length}</div>
              </div>
              <div>
                <div className="metric__label">Files</div>
                <div className="metric__value">{count(analysis.totalFiles)}</div>
              </div>
              <div>
                <div className="metric__label">On disk</div>
                <div className="metric__value">{bytes(analysis.totalBytes)}</div>
              </div>
              <div>
                <div className="metric__label">Database rows</div>
                <div className="metric__value">{count(analysis.totalMetricsRows)}</div>
              </div>
            </div>

            {analysis.cited.length > 0 ? (
              <Callout title="Something depends on these runs" tone="warn">
                <p>
                  {analysis.cited.length} of these runs {analysis.cited.length === 1 ? "is" : "are"}{" "}
                  cited by a scored campaign or a written-up finding. Deleting them does not
                  change those documents — it makes the numbers in them impossible to check
                  again. That failure is silent: nothing will complain until someone tries to
                  re-derive the figure.
                </p>
                {analysis.cited.map((run) => (
                  <p key={run.runId} className="mono faint">
                    {run.runId} —{" "}
                    {run.dependencies
                      .map((dependency) => `${dependency.id} (${dependency.detail})`)
                      .join("; ")}
                  </p>
                ))}
              </Callout>
            ) : (
              <Callout title="Nothing depends on these runs" tone="info">
                <p>
                  No campaign result and no finding cites any of them, so no published number
                  loses its evidence.
                </p>
              </Callout>
            )}

            {analysis.runs.some((run) => run.empty) ? (
              <Callout title="Some of these recorded nothing" tone="neutral">
                <p>
                  {analysis.runs.filter((run) => run.empty).length} of the selected runs are
                  empty directories — runs that died before writing anything. These are the safe
                  ones to remove.
                </p>
              </Callout>
            ) : null}

            {analysis.problems.length > 0 ? (
              <Callout title="Cannot be deleted" tone="warn">
                {analysis.problems.map((problem) => (
                  <p key={problem.runId} className="mono">
                    {problem.runId}: {problem.reason}
                  </p>
                ))}
              </Callout>
            ) : null}

            <table className="table">
              <thead>
                <tr>
                  <th>Run</th>
                  <th>What it is</th>
                  <th className="num">Files</th>
                  <th className="num">Size</th>
                  <th className="num">DB rows</th>
                  <th>Depended on by</th>
                </tr>
              </thead>
              <tbody>
                {analysis.runs.map((run) => (
                  <tr key={run.runId}>
                    <td className="mono">{run.runId}</td>
                    <td>
                      {run.empty ? (
                        <span className="faint">recorded nothing</span>
                      ) : (
                        (run.describes ?? <span className="faint">no manifest</span>)
                      )}
                    </td>
                    <td className="num">{count(run.files)}</td>
                    <td className="num">{bytes(run.bytes)}</td>
                    <td className="num">{count(run.metricsRows)}</td>
                    <td>
                      {run.dependencies.length === 0 ? (
                        <span className="faint">nothing</span>
                      ) : (
                        <span style={{ color: "var(--warning-text)" }}>
                          {run.dependencies.length}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div>
              <label className="label" htmlFor="reason">
                Why (goes in the log, optional but worth it)
              </label>
              <input
                id="reason"
                className="btn"
                style={{ width: "100%", fontFamily: "var(--font-sans)" }}
                value={reason}
                onChange={(event) => setReason(event.target.value)}
                placeholder="e.g. superseded by the rerun at temperature 0"
              />
            </div>

            <div>
              <label className="label" htmlFor="confirm">
                Type {CONFIRM_WORD} to confirm
              </label>
              <input
                id="confirm"
                className="btn mono"
                style={{ width: 220 }}
                value={confirmText}
                onChange={(event) => setConfirmText(event.target.value)}
                autoComplete="off"
              />
            </div>

            <div className="row">
              <button
                className="btn btn--primary"
                type="button"
                disabled={confirmText.trim() !== CONFIRM_WORD || pending || analysis.runs.length === 0}
                onClick={doDelete}
                style={
                  confirmText.trim() === CONFIRM_WORD
                    ? { background: "var(--danger)", borderColor: "var(--danger)" }
                    : undefined
                }
              >
                {pending
                  ? "Deleting…"
                  : `Delete ${analysis.runs.length} run${analysis.runs.length === 1 ? "" : "s"}`}
              </button>
              <button className="btn" type="button" onClick={() => setAnalysis(null)}>
                Back
              </button>
              <span className="faint" style={{ fontSize: "var(--text-caption)" }}>
                Run data is committed, so this is recoverable with{" "}
                <span className="mono">git checkout -- eval/runs</span>.
              </span>
            </div>
          </div>
        </div>
      ) : null}

      <Card title={`v2 runs · ${count(runs.length)}`} flush>
        <table className="table">
          <thead>
            <tr>
              <th style={{ width: 28 }} aria-label="Select" />
              <th>Run</th>
              <th>Stage</th>
              <th>Command</th>
              <th>Model</th>
              <th className="num">Turns</th>
              <th className="num">Tokens in / out</th>
              <th className="num">Cost</th>
              <th>Status</th>
              <th>Terminal</th>
            </tr>
          </thead>
          <tbody>
            {runs.map((run) => (
              <tr key={run.runId}>
                <td>{checkbox(run.runId)}</td>
                <td>
                  <Link className="mono" href={`/runs/${run.runId}`}>
                    {run.runId}
                  </Link>
                </td>
                <td>{STAGE_LABEL[run.stage] ?? run.stage}</td>
                <td className="mono">{run.command}</td>
                <td className="mono faint">{run.model}</td>
                <td className="num">{run.turns}</td>
                <td className="num">
                  {count(run.promptTokens)} / {count(run.completionTokens)}
                </td>
                <td className="num">{usd(run.costUsd)}</td>
                <td>
                  {run.status === "ok" ? (
                    <Badge tone="ok">ok</Badge>
                  ) : (
                    <Badge tone="bad">failed</Badge>
                  )}
                </td>
                <td>
                  {run.hasRecording ? (
                    <Badge tone="info" mono>
                      recorded
                    </Badge>
                  ) : (
                    <span className="faint">none</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      {emptyRunIds.length > 0 ? (
        <Card title={`Started and recorded nothing · ${count(emptyRunIds.length)}`} flush>
          <table className="table">
            <thead>
              <tr>
                <th style={{ width: 28 }} aria-label="Select" />
                <th>Run</th>
                <th>Command</th>
                <th>What happened</th>
              </tr>
            </thead>
            <tbody>
              {emptyRunIds.map((runId) => (
                <tr key={runId}>
                  <td>{checkbox(runId)}</td>
                  <td className="mono">{runId}</td>
                  <td className="mono">{runId.split("_")[1] ?? ""}</td>
                  <td className="faint">
                    The directory was created and nothing was ever written to it.
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      ) : null}
    </>
  );
}

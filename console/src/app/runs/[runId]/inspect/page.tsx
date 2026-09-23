import Link from "next/link";
import { notFound } from "next/navigation";
import { createHash } from "node:crypto";
import { findRun, loadRun, RunNotFoundError } from "../../../../data/runs.js";
import { checkPromptDrift } from "../../../../data/promptDrift.js";
import { describeRun } from "../../../../data/events.js";
import { annotationFormatOf } from "../../../../data/commandLine.js";
import {
  Badge,
  Callout,
  Card,
  CodeBlock,
  KeyValue,
  Metric,
  count,
  seconds,
  usd,
} from "../../../../components/ui.js";

export const dynamic = "force-dynamic";

/**
 * Inspect: what v2 did inside (§6.5).
 *
 * The prompt-drift check lives in `data/promptDrift.ts`, where the reasoning behind it is
 * written down - it is not a string comparison, and the two obvious ways of doing it both
 * report drift on every run ever made. This page only presents the verdict, and presents it
 * conservatively: "the file has changed since this run", never "the run is wrong".
 */

function shortHash(text: string): string {
  return createHash("sha256").update(text).digest("hex").slice(0, 12);
}

export default async function InspectPage({ params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params;

  let dir: string;
  try {
    dir = findRun(runId);
  } catch (cause) {
    if (cause instanceof RunNotFoundError) notFound();
    throw cause;
  }

  const run = loadRun(dir);
  const m = run.manifest;
  const drift = checkPromptDrift(m.prompt_files, m.prompt_system, m.prompt_user);
  const changed = drift.filter((check) => check.verdict === "changed");
  const sessions = Array.isArray(m.checks["sessions"]) ? (m.checks["sessions"] as unknown[]) : [];
  const refused = typeof m.checks["refused_calls"] === "number" ? m.checks["refused_calls"] : null;

  return (
    <main className="page page--wide">
      <div className="accent-bar" />
      <div className="page__head">
        <h1>Inside · {describeRun(m)}</h1>
        <span className="spacer">
          <Link href={`/runs/${runId}`}>← Run</Link>
        </span>
      </div>
      <p className="page__sub mono">{run.runId}</p>

      <div className="stack">
        {changed.length > 0 ? (
          <Callout title="The prompt files have changed since this run" tone="warn">
            <p>
              {changed.length} of this run&apos;s {drift.length} prompt file
              {drift.length === 1 ? "" : "s"} no longer matches what the run actually sent. The
              run&apos;s own copy is below and is what its results describe. Reading today&apos;s
              file as though it were this run&apos;s prompt would attribute these numbers to a
              system that did not produce them.
            </p>
            {changed.map((check) => (
              <p key={check.file} className="faint" style={{ marginTop: 8 }}>
                <span className="mono">{check.file}</span>
                {check.divergence ? (
                  <>
                    {" "}
                    — the two agree up to{" "}
                    <span className="mono">…{check.divergence.matchedBefore}</span>, after which
                    today&apos;s file reads{" "}
                    <span className="mono" style={{ color: "var(--warning-text)" }}>
                      &ldquo;{check.divergence.templateSays}…&rdquo;
                    </span>
                  </>
                ) : null}
              </p>
            ))}
          </Callout>
        ) : null}

        <Card title="Run settings">
          <KeyValue
            rows={[
              { k: "Stage", v: m.stage },
              { k: "Command", v: m.command },
              ...(m.stage === "annotate"
                ? [{ k: "Annotation format", v: annotationFormatOf(m) ?? "not recorded", absent: annotationFormatOf(m) === null }]
                : []),
              { k: "Model requested", v: m.model_requested },
              {
                k: "Model reported",
                v: m.model_reported || "not reported",
                absent: !m.model_reported,
              },
              { k: "Provider", v: m.provider ?? "not recorded", absent: m.provider === null },
              {
                k: "Seed",
                v:
                  m.seed === null ? (
                    "not set"
                  ) : (
                    <>
                      {m.seed}{" "}
                      {/* Whether the provider honoured the seed is itself a result: a seed that
                          is ignored makes "same input, same output" untestable. */}
                      {m.seed_honored ? (
                        <Badge tone="ok">honoured</Badge>
                      ) : (
                        <Badge tone="warn">not honoured by the provider</Badge>
                      )}
                    </>
                  ),
                absent: m.seed === null,
              },
              {
                k: "Decoding",
                v: Object.entries(m.decoding_params)
                  .map(([key, value]) => `${key}=${String(value)}`)
                  .join("  "),
              },
              { k: "Response format", v: m.response_format },
              { k: "Prompt variant", v: m.prompt_variant },
              {
                k: "Finish reason",
                v: m.finish_reason ?? "not recorded",
                absent: m.finish_reason === null,
              },
              {
                k: "Output truncated",
                v: m.output_truncated ? "yes — the token cap was reached" : "no",
              },
            ]}
          />
        </Card>

        <Card
          title={`Prompt · ${m.prompt_files.length} file${m.prompt_files.length === 1 ? "" : "s"}`}
          aside={
            changed.length > 0 ? (
              <Badge tone="warn">source changed since</Badge>
            ) : (
              <Badge tone="ok">source unchanged</Badge>
            )
          }
        >
          <div className="kv" style={{ marginBottom: 14 }}>
            {drift.map((check) => (
              <div key={check.file} style={{ display: "contents" }}>
                <div className="kv__k mono" style={{ fontSize: "var(--text-caption)" }}>
                  {check.file}
                </div>
                <div className="kv__v">
                  {check.verdict === "unchanged" ? (
                    <Badge tone="ok">unchanged</Badge>
                  ) : check.verdict === "changed" ? (
                    <Badge tone="warn">changed since this run</Badge>
                  ) : (
                    <Badge tone="bad">no longer on disk</Badge>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="label" style={{ marginBottom: 6 }}>
            System — as sent ({shortHash(m.prompt_system)})
          </div>
          <CodeBlock>{m.prompt_system}</CodeBlock>

          <div className="label" style={{ margin: "14px 0 6px" }}>
            User — as sent ({shortHash(m.prompt_user)})
          </div>
          <CodeBlock>{m.prompt_user}</CodeBlock>
        </Card>

        <Card title="Raw response">
          <CodeBlock>{m.raw_response}</CodeBlock>
        </Card>

        <Card title={`Turns · ${run.turns.length}`} flush>
          <table className="table">
            <thead>
              <tr>
                <th>Turn</th>
                <th>Config</th>
                <th className="num">Tokens in</th>
                <th className="num">Tokens out</th>
                <th className="num">Cost</th>
                <th className="num">Seconds</th>
                <th>Model</th>
              </tr>
            </thead>
            <tbody>
              {run.turns.map((turn) => (
                <tr key={`${turn.turn}-${turn.config_index ?? "x"}`}>
                  <td className="mono">{turn.turn}</td>
                  <td className="mono">
                    {turn.config_index === null ? (
                      <span className="faint">—</span>
                    ) : (
                      turn.config_index
                    )}
                  </td>
                  <td className="num">{count(turn.prompt_tokens)}</td>
                  <td className="num">{count(turn.completion_tokens)}</td>
                  <td className="num">{usd(turn.cost_usd)}</td>
                  <td className="num">{turn.wall_clock_seconds.toFixed(2)}</td>
                  <td className="mono faint">{turn.model_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>

        {sessions.length > 0 ? (
          <Card title={`Tracing sessions · ${sessions.length}`} flush>
            <table className="table">
              <thead>
                <tr>
                  <th>Config</th>
                  <th>Invocation</th>
                  <th>Status</th>
                  <th>Stopped because</th>
                  <th className="num">Executions</th>
                  <th className="num">Reported</th>
                  <th className="num">Rejected</th>
                  <th className="num">Cost</th>
                </tr>
              </thead>
              <tbody>
                {sessions.map((entry, index) => {
                  const s = entry as Record<string, unknown>;
                  const status = typeof s["status"] === "string" ? s["status"] : "unknown";
                  return (
                    <tr key={index}>
                      <td className="mono">{String(s["index"] ?? index)}</td>
                      <td className="mono">{String(s["invocation"] ?? "")}</td>
                      <td>
                        {status === "ok" ? (
                          <Badge tone="ok">ok</Badge>
                        ) : (
                          <Badge tone="warn">{status}</Badge>
                        )}
                      </td>
                      <td className="mono faint">{String(s["stop_reason"] ?? "—")}</td>
                      <td className="num">{String(s["executions"] ?? 0)}</td>
                      <td className="num">{String(s["interactions"] ?? 0)}</td>
                      <td className="num">{String(s["rejected_interactions"] ?? 0)}</td>
                      <td className="num">
                        {typeof s["cost_usd"] === "number" ? usd(s["cost_usd"]) : "—"}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {refused !== null ? (
              <div style={{ padding: "10px 12px", borderTop: "1px solid var(--border-default)" }}>
                <span className="label">Refused tool calls</span>{" "}
                <span className="mono">{refused}</span>{" "}
                <span className="faint" style={{ fontSize: "var(--text-caption)" }}>
                  — the evidence that the boundary held.
                </span>
              </div>
            ) : null}
          </Card>
        ) : null}

        <Card title="What v1 said about the artifact">
          {m.validation === null ? (
            <p className="muted" style={{ margin: 0, fontSize: "var(--text-small)" }}>
              No validation was recorded for this stage.
            </p>
          ) : m.validation.available ? (
            <div className="metrics">
              <Metric label="v1's verdict" value={m.validation.passed ? "accepted" : "rejected"} />
              <Metric
                label="Elements"
                {...(m.validation.elements === null
                  ? { absentReason: "v1 reported no element count" }
                  : { value: m.validation.elements })}
              />
            </div>
          ) : (
            <Callout title="Not available" tone="neutral">
              <p>
                v1&apos;s environment could not be reached, so v1 never gave a verdict. That is
                a different finding from v1 rejecting the artifact, and the two are not
                combined.
              </p>
              {m.validation.error ? <p className="mono faint">{m.validation.error}</p> : null}
            </Callout>
          )}
        </Card>

        <Card title="Conversation log">
          {run.conversationPath ? (
            <p style={{ margin: 0, fontSize: "var(--text-small)" }}>
              Recorded at <span className="mono">{run.conversationPath}</span>.
            </p>
          ) : (
            <p className="muted" style={{ margin: 0, fontSize: "var(--text-small)" }}>
              This run did not use <span className="code-inline">--log-conversation</span>, so
              there is no turn-by-turn log. No run has used it so far.
            </p>
          )}
        </Card>

        <Card title={`Files in the run directory · ${run.files.length}`} flush>
          <table className="table">
            <thead>
              <tr>
                <th>File</th>
                <th className="num">Bytes</th>
              </tr>
            </thead>
            <tbody>
              {run.files.map((file) => (
                <tr key={file.name}>
                  <td className="mono">{file.name}</td>
                  <td className="num">{count(file.bytes)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>
    </main>
  );
}

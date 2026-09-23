import Link from "next/link";
import { notFound } from "next/navigation";
import { findRun, loadRun, RunNotFoundError } from "../../../data/runs.js";
import { readRecording } from "../../../data/asciicast.js";
import { eventsForRun, describeRun } from "../../../data/events.js";
import { EventRail } from "../../../components/EventRail.js";
import { TerminalPlayer } from "../../../components/TerminalPlayer.js";
import { Badge, Callout, Card, CodeBlock, Metric, count, seconds, usd } from "../../../components/ui.js";

export const dynamic = "force-dynamic";

/**
 * The Run screen: a terminal on the left, the events beside it (§6.3).
 *
 * For a run this console started, the terminal replays the recording byte for byte. For the
 * 135 runs that predate the console, there is no recording, and the pane says so plainly and
 * shows the command line instead - rather than an empty black rectangle that reads as a run
 * which produced no output.
 */
export default async function RunPage({ params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params;

  let dir: string;
  try {
    dir = findRun(runId);
  } catch (cause) {
    if (cause instanceof RunNotFoundError) notFound();
    throw cause;
  }

  const run = loadRun(dir);
  const events = eventsForRun(run);
  const recording = run.recordingPath ? readRecording(run.recordingPath) : null;
  const where = events.find((event) => event.kind === "run_start")?.where ?? "mac";

  return (
    <main className="page page--wide">
      <div className="accent-bar" />
      <div className="page__head">
        <h1>{describeRun(run.manifest)}</h1>
        {run.manifest.status === "ok" ? (
          <Badge tone="ok">ok</Badge>
        ) : (
          <Badge tone="bad">failed</Badge>
        )}
        <Badge tone="muted" mono>
          {run.manifest.turns} turn{run.manifest.turns === 1 ? "" : "s"}
        </Badge>
        <span className="spacer">
          <Link href={`/runs/${runId}/inspect`}>Inspect →</Link>
        </span>
      </div>
      <p className="page__sub mono">{run.runId}</p>

      <div className="run-layout">
        <div className="stack">
          <div className="terminal">
            <div className="terminal__head">
              <span className="label">v2 · caruca-v2</span>
              <span className="terminal__where">
                {where === "lima" ? "lima vm · caruca" : "this mac"}
              </span>
              <span
                className="badge__dot"
                style={{ background: "var(--gray-400)" }}
                title="Not live — this run has already finished."
              />
            </div>

            {recording ? (
              <TerminalPlayer
                header={{ width: recording.header.width, height: recording.header.height }}
                events={recording.events}
                durationSeconds={recording.durationSeconds}
              />
            ) : (
              <div className="terminal__empty">
                <div className="label" style={{ color: "var(--term-dim)" }}>
                  No terminal recording
                </div>
                <p style={{ margin: 0, fontSize: "var(--text-small)", maxWidth: "62ch" }}>
                  This run was made before the console existed, so nothing captured what it
                  showed on screen. Its events are beside this pane, and they come from the
                  files the run wrote — not from terminal output.
                </p>
                <p style={{ margin: 0, fontSize: "var(--text-small)", maxWidth: "62ch" }}>
                  The command line below was rebuilt from the manifest. No run records its
                  arguments as they were typed.
                </p>
              </div>
            )}
          </div>

          <Card
            title="Command line · reconstructed"
            aside={
              <Badge tone="warn" mono>
                rebuilt, not captured
              </Badge>
            }
          >
            <CodeBlock>{run.commandLine.display}</CodeBlock>
            {run.commandLine.notRecorded.length > 0 ? (
              <p className="event__detail" style={{ marginTop: 10 }}>
                Not recorded, so not shown above:{" "}
                <span className="mono">{run.commandLine.notRecorded.join(" ")}</span>. These
                change where output goes and how it looks, never what the model was asked.
              </p>
            ) : null}
          </Card>

          <Card title="This run">
            <div className="metrics">
              <Metric label="Turns" value={run.manifest.turns} />
              <Metric
                label="Tokens in"
                value={count(run.manifest.prompt_tokens)}
                basis="summed over turns"
              />
              <Metric
                label="Tokens out"
                value={count(run.manifest.completion_tokens)}
                basis="summed over turns"
              />
              <Metric label="Cost" value={usd(run.manifest.cost_usd)} />
              <Metric
                label="Model time"
                value={seconds(run.manifest.wall_clock_seconds)}
                basis="time in model calls, not elapsed"
              />
              <Metric
                label="Model"
                value={run.manifest.model_reported || run.manifest.model_requested}
              />
            </div>
          </Card>

          {run.manifest.wall_clock_seconds > 0 ? (
            <Callout title="What this timing is" tone="neutral">
              <p>
                The figure above is the sum of the model calls, which is how each stage builds
                its manifest. It is not how long the run took: the difference is whatever the
                run spent executing commands, and tracing spends a great deal there.
              </p>
            </Callout>
          ) : null}
        </div>

        <Card title={`Events · ${events.length}`} flush>
          <EventRail events={events} />
        </Card>
      </div>
    </main>
  );
}

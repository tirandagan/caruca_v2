/**
 * The events beside the terminal (§6.3).
 *
 * The terminal shows what a person saw. This shows what the run recorded. They are separate on
 * purpose: numbers come from files, never from reading terminal text.
 *
 * Every timestamp here is marked when it was derived rather than measured. For every run made
 * before this console existed, that is all of them - no per-turn clock time was ever written
 * down, so a turn's position is the sum of the durations before it. The dotted underline and
 * the tooltip say so, so nothing on this rail can be mistaken for a measurement.
 */
import type { RunEvent } from "../data/events.js";
import { seconds, usd, count } from "./ui.js";

const DERIVED_TITLE =
  "Derived, not measured: no per-turn clock time was recorded, so this is the sum of the durations before it.";

function At({ event }: { event: RunEvent }) {
  return (
    <span
      className={event.timingDerived ? "event__at event__at--derived" : "event__at"}
      title={event.timingDerived ? DERIVED_TITLE : undefined}
    >
      {event.at === 0 ? "0.0s" : seconds(event.at)}
    </span>
  );
}

/**
 * A tool call's arguments, in one line.
 *
 * `run_command` carries `{argv: [...]}`, which reads best as the command itself - that is the
 * thing a person is actually looking for when they scan this rail. Anything else is shown as
 * compact JSON rather than being dropped.
 */
function summarizeArguments(args: unknown): string {
  if (args === null || typeof args !== "object") return String(args);
  const record = args as Record<string, unknown>;
  if (Array.isArray(record["argv"])) return (record["argv"] as unknown[]).join(" ");
  const json = JSON.stringify(args);
  return json.length > 140 ? `${json.slice(0, 140)}…` : json;
}

function Row({ event }: { event: RunEvent }) {
  switch (event.kind) {
    case "run_start":
      return (
        <div className="event">
          <At event={event} />
          <div>
            <div className="event__kind">Run start</div>
            <div className="event__detail">
              <span className="mono">{event.stage}</span> · {event.command} · on{" "}
              {event.where === "lima" ? "the Lima VM caruca" : "this Mac"}
            </div>
            <div className="event__detail mono faint">{event.argv.join(" ")}</div>
            {event.argvReconstructed ? (
              <div className="event__detail faint">
                Command line reconstructed from the manifest — no run records its arguments as
                typed.
              </div>
            ) : null}
          </div>
        </div>
      );

    case "prompt_sent":
      return (
        <div className="event">
          <At event={event} />
          <div>
            <div className="event__kind">Prompt sent</div>
            <div className="event__detail">
              variant <span className="mono">{event.promptVariant}</span> · hash{" "}
              <span className="mono">{event.promptHash.slice(0, 12)}</span>
            </div>
            <div className="event__detail faint mono">{event.promptFiles.join(", ")}</div>
          </div>
        </div>
      );

    case "model_turn":
      return (
        <div className="event">
          <At event={event} />
          <div>
            <div className="event__kind">
              Turn {event.turn}
              {event.configIndex !== null ? ` · config ${event.configIndex}` : ""}
            </div>
            <div className="event__detail">
              <span className="mono">
                {count(event.promptTokens)} in / {count(event.completionTokens)} out
              </span>{" "}
              · <span className="mono">{usd(event.costUsd)}</span> ·{" "}
              <span className="mono">{seconds(event.seconds)}</span>
            </div>
          </div>
        </div>
      );

    case "trace_session":
      return (
        <div className="event">
          <At event={event} />
          <div>
            <div className="event__kind">Session {event.configIndex}</div>
            <div className="event__detail">
              {event.reported ? (
                <>
                  reported {event.interactions} interaction
                  {event.interactions === 1 ? "" : "s"} · {event.executions} execution
                  {event.executions === 1 ? "" : "s"}
                </>
              ) : (
                <>
                  ended without reporting ·{" "}
                  <span className="mono">{event.stopReason ?? "unknown"}</span>
                </>
              )}
            </div>
            {event.error ? <div className="event__detail faint">{event.error}</div> : null}
          </div>
        </div>
      );

    case "tool_call":
      return (
        <div className={event.allowed ? "event" : "event event--refused"}>
          <At event={event} />
          <div>
            <div className="event__kind">
              {event.allowed ? "Tool call" : "Tool call refused"}
            </div>
            <div className="event__detail">
              <span className="mono">{event.name}</span>
              {event.configIndex !== null ? ` · config ${event.configIndex}` : ""}
            </div>
            {event.arguments !== undefined ? (
              <div className="event__detail mono faint">{summarizeArguments(event.arguments)}</div>
            ) : null}
            {event.reason ? <div className="event__detail faint">{event.reason}</div> : null}
          </div>
        </div>
      );

    case "artifact_written":
      return (
        <div className="event">
          <At event={event} />
          <div>
            <div className="event__kind">Artifact written</div>
            <div className="event__detail mono">{event.path}</div>
            <div className="event__detail faint">
              {event.consumedBy ? `Read next by ${event.consumedBy}.` : "End of the chain."}
            </div>
          </div>
        </div>
      );

    case "check":
      return (
        <div className="event">
          <At event={event} />
          <div>
            <div className="event__kind">Check · {event.name}</div>
            <div className="event__detail">
              {/*
                Null is not a failure. `available: false` means v1's environment could not be
                reached, which is a different finding from v1 rejecting the artifact, and
                collapsing the two would misreport v1.
              */}
              {event.passed === null
                ? "not available — v1's environment could not be reached"
                : event.passed
                  ? "passed"
                  : "did not pass"}
            </div>
          </div>
        </div>
      );

    case "run_end":
      return (
        <div className="event event--end">
          <At event={event} />
          <div>
            <div className="event__kind">Run end · {event.status}</div>
            <div className="event__detail">
              {event.turns} turn{event.turns === 1 ? "" : "s"} ·{" "}
              <span className="mono">
                {count(event.promptTokens)} in / {count(event.completionTokens)} out
              </span>{" "}
              · <span className="mono">{usd(event.costUsd)}</span>
            </div>
            {event.failureReason ? (
              <div className="event__detail faint">{event.failureReason}</div>
            ) : null}
          </div>
        </div>
      );
  }
}

export function EventRail({ events }: { events: RunEvent[] }) {
  return (
    <div className="events">
      {events.map((event, index) => (
        <Row key={`${event.kind}-${index}`} event={event} />
      ))}
    </div>
  );
}

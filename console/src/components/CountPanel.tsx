"use client";

/**
 * The counts, taken from what v1 actually prints (§6.2).
 *
 * Counting is a button rather than something the page does on load: `generate` at v1's
 * defaults takes real time on a wide command, and 16 of the 120 commands blow past the
 * half-million-line cap. The button makes the wait deliberate.
 *
 * **`--number` is never used.** It disagrees with what v1 emits on all 90 commands that
 * enumerate fully, and crashes on 14 including `pwd`. The count here comes from counting the
 * lines v1 prints, which is what the tracer will actually run.
 */
import { useState, useTransition } from "react";
import { countInvocations, type CountResult } from "../app/actions.js";
import { Badge, Card, count } from "./ui.js";

export function CountPanel({
  command,
  maxArity,
  maxCount,
}: {
  command: string;
  maxArity: number;
  maxCount: number;
}) {
  const [result, setResult] = useState<CountResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  return (
    <Card
      title="How much v1 would enumerate"
      aside={
        result ? (
          <Badge tone="muted" mono>
            {result.seconds.toFixed(1)}s
          </Badge>
        ) : null
      }
    >
      <div className="row">
        <button
          className="btn"
          type="button"
          disabled={pending}
          onClick={() => {
            setError(null);
            setResult(null);
            startTransition(async () => {
              try {
                setResult(await countInvocations(command, maxArity, maxCount));
              } catch (cause) {
                setError((cause as Error).message);
              }
            });
          }}
        >
          {pending ? "Counting…" : `Count ${command}`}
        </button>
        <span className="faint" style={{ fontSize: "var(--text-caption)" }}>
          Runs v1&apos;s <span className="mono">generate</span>, which prints invocations and
          executes nothing — safe even for <span className="mono">rm</span>.
        </span>
      </div>

      {error ? (
        <p className="mono" style={{ color: "var(--danger-text)", fontSize: "var(--text-small)" }}>
          {error}
        </p>
      ) : null}

      {result ? (
        <>
          <div className="metrics" style={{ marginTop: 14 }}>
            <div>
              <div className="metric__label">Lines printed</div>
              <div className="metric__value">{count(result.printed)}</div>
              <div className="metric__basis">duplicates included, as v1 emits them</div>
            </div>
            <div>
              <div className="metric__label">Distinct invocations</div>
              <div className="metric__value">{count(result.distinct)}</div>
              <div className="metric__basis">
                {result.printed > 0
                  ? `${Math.round((1 - result.distinct / result.printed) * 100)}% of the lines are duplicates`
                  : ""}
              </div>
            </div>
            {result.executions !== null ? (
              <div>
                <div className="metric__label">Executions v1 would perform</div>
                <div className="metric__value">{count(result.executions)}</div>
                <div className="metric__basis">
                  from --length-only; the tracer inherits the duplicated stream
                </div>
              </div>
            ) : null}
          </div>

          {result.capped ? (
            <p className="event__detail" style={{ color: "var(--warning-text)" }}>
              Counting was cut short: {result.cappedReason}. The figures above are a lower
              bound, not the total.
            </p>
          ) : null}

          <p className="event__detail faint mono" style={{ marginTop: 10 }}>
            {result.argv.join(" ")}
          </p>
        </>
      ) : null}
    </Card>
  );
}

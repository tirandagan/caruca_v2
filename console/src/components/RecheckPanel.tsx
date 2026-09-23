"use client";

/**
 * Re-checking one finding's numbers, from the page.
 *
 * The button is slow and says so: a campaign-level check re-scores a whole campaign from its
 * run artifacts with today's scorer. That is the point — a fast check that reads back what was
 * already recorded would tell you nothing you did not already know.
 *
 * Every result states **how** it was obtained and whether the number was genuinely re-derived
 * or only re-read, because "matches" under the weaker check is a weaker claim and must not be
 * presented as the stronger one.
 */
import { useState, useTransition } from "react";
import { recheckFinding, type FindingRecheck } from "../app/actions.js";
import { Badge, figure } from "./ui.js";

function Verdict({ verdict }: { verdict: string }) {
  if (verdict === "matches") return <Badge tone="ok">matches</Badge>;
  if (verdict === "changed") return <Badge tone="bad">changed</Badge>;
  return <Badge tone="muted">cannot be checked</Badge>;
}

export function RecheckPanel({ findingId }: { findingId: string }) {
  const [result, setResult] = useState<FindingRecheck | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  return (
    <div style={{ marginTop: 14 }}>
      <div className="row">
        <button
          className="btn"
          type="button"
          disabled={pending}
          onClick={() => {
            setError(null);
            startTransition(async () => {
              try {
                setResult(await recheckFinding(findingId));
              } catch (cause) {
                setError((cause as Error).message);
              }
            });
          }}
        >
          {pending ? "Re-deriving…" : "Re-check these numbers"}
        </button>
        {pending ? (
          <span className="faint" style={{ fontSize: "var(--text-caption)" }}>
            Re-scoring the campaign from its run artifacts. Tens of seconds.
          </span>
        ) : null}
      </div>

      {error ? (
        <p className="mono" style={{ color: "var(--danger-text)", fontSize: "var(--text-small)" }}>
          {error}
        </p>
      ) : null}

      {result ? (
        <table className="table" style={{ marginTop: 10 }}>
          <thead>
            <tr>
              <th>Number</th>
              <th className="num">As recorded</th>
              <th className="num">Recomputed</th>
              <th>Verdict</th>
              <th>How</th>
            </tr>
          </thead>
          <tbody>
            {result.outcomes.map((outcome) => (
              <tr key={outcome.label}>
                <td>{outcome.label}</td>
                <td className="num">{figure(outcome.evidence.value)}</td>
                <td className="num">
                  {outcome.recomputed === null ? (
                    <span className="faint">—</span>
                  ) : (
                    outcome.recomputed.toFixed(6)
                  )}
                  {outcome.comparedAtPrecision !== null && outcome.recomputed !== null ? (
                    <div className="event__detail faint">
                      compared at {outcome.comparedAtPrecision} d.p.
                    </div>
                  ) : null}
                </td>
                <td>
                  <Verdict verdict={outcome.verdict} />
                  {outcome.verdict !== "not_recomputable" && !outcome.rederived ? (
                    <div className="event__detail" style={{ color: "var(--warning-text)" }}>
                      re-read, not re-derived
                    </div>
                  ) : null}
                </td>
                <td className="mono faint" style={{ fontSize: "var(--text-caption)" }}>
                  {outcome.how}
                  {outcome.reason ? <div>{outcome.reason}</div> : null}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </div>
  );
}

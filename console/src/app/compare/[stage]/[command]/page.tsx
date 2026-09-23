import Link from "next/link";
import { notFound } from "next/navigation";
import { buildMatrix, HEADLINE, matrixKey, toMatrixView } from "../../../../data/compare.js";
import { loadCampaignSet, PARITY_CAMPAIGNS } from "../../../../data/parityCampaigns.js";
import { readParityDiff, sectionFor, ParityDiffMissingError } from "../../../../data/parityDiff.js";
import { STAGES, type Stage } from "../../../../data/schema.js";
import { Badge, Callout, Card, KeyValue, count } from "../../../../components/ui.js";
import { Markdown } from "../../../../components/Markdown.js";

export const dynamic = "force-dynamic";

/**
 * "Explain this number": the items a figure counts, and the rule that produced it.
 *
 * The items come from `eval/parity_diffs/<command>.md`, which `scripts/parity_diff.py` writes.
 * Reading that document rather than recomputing the comparison is what §6.4 means by the
 * console and the script not being able to disagree - they are literally the same output.
 */
export default async function DrillDownPage({
  params,
}: {
  params: Promise<{ stage: string; command: string }>;
}) {
  const { stage: stageParam, command } = await params;
  if (!STAGES.includes(stageParam as Stage)) notFound();
  const stage = stageParam as Stage;

  const campaigns = loadCampaignSet(PARITY_CAMPAIGNS);
  const view = toMatrixView(buildMatrix(campaigns.rows));
  const cell = view.byKey.get(matrixKey(command, stage));
  const headline = HEADLINE[stage];

  let diffSection = null;
  let diffError: string | null = null;
  let diffPath: string | null = null;
  let quotesV1 = false;
  try {
    const diff = readParityDiff(command);
    diffSection = sectionFor(diff, stage);
    diffPath = diff.path;
    quotesV1 = diff.v1SourceWarning;
  } catch (cause) {
    if (cause instanceof ParityDiffMissingError) diffError = cause.message;
    else throw cause;
  }

  return (
    <main className="page">
      <div className="accent-bar" />
      <div className="page__head">
        <h1>
          {headline.label} · <span className="mono">{command}</span>
        </h1>
        <span className="spacer">
          <Link href="/compare">← Compare</Link>
        </span>
      </div>
      <p className="page__sub">
        What this number counts, over what, and the items behind it.
      </p>

      <div className="stack">
        <Card title="What this number is">
          <KeyValue
            rows={[
              {
                k: "The figure",
                v: cell
                  ? cell.pooledCounts
                    ? `${cell.pooledCounts.top} of ${cell.pooledCounts.bottom} (${(cell.value ?? 0).toFixed(3)})`
                    : cell.value === null
                      ? "not scoreable"
                      : cell.value.toFixed(3)
                  : "not run",
                absent: !cell || cell.value === null,
              },
              { k: "What is counted", v: headline.label },
              { k: "Counted over", v: headline.denominator },
              { k: "Method", v: headline.method },
              {
                k: "Samples",
                v: cell ? `${cell.samples} run${cell.samples === 1 ? "" : "s"} of this cell` : "—",
              },
              {
                k: "How samples combine",
                v: headline.denominatorMetric
                  ? "pooled: the numerators summed over the denominators summed"
                  : "mean of the per-sample values",
              },
              {
                k: "Left out",
                v: cell?.unscoreableReason
                  ? cell.unscoreableReason
                  : "nothing — every sample of this cell was scoreable",
                absent: !cell?.unscoreableReason,
              },
              {
                k: "Runs behind it",
                v: cell?.runIds.length ? (
                  <>
                    {cell.runIds.map((id, index) => (
                      <span key={id}>
                        {index > 0 ? ", " : ""}
                        <Link className="mono" href={`/runs/${id}`}>
                          {id}
                        </Link>
                      </span>
                    ))}
                  </>
                ) : (
                  "no run was recorded for this cell"
                ),
                absent: !cell?.runIds.length,
              },
            ]}
          />
        </Card>

        {cell?.counts ? (
          <Card title="The scorer's own breakdown">
            <div className="metrics">
              {Object.entries(cell.counts).map(([key, value]) => (
                <div key={key}>
                  <div className="metric__label">{key.replace(/_/g, " ")}</div>
                  <div className="metric__value">{count(value)}</div>
                </div>
              ))}
            </div>
          </Card>
        ) : null}

        {cell && cell.moreVariable.length > 0 ? (
          <Card title="Metrics that moved more than the headline did">
            <table className="table">
              <thead>
                <tr>
                  <th>Metric</th>
                  <th className="num">Values across samples</th>
                  <th className="num">Movement</th>
                </tr>
              </thead>
              <tbody>
                {cell.moreVariable.map((metric) => (
                  <tr key={metric.metric}>
                    <td className="mono">{metric.metric}</td>
                    <td className="num">
                      {metric.values.map((value) => value.toFixed(3)).join(", ")}
                    </td>
                    <td className="num">{metric.spread.toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        ) : null}

        <Card
          title="The items, from the generated drill-down"
          aside={
            diffPath ? (
              <Badge tone="muted" mono>
                {diffPath.split("/").slice(-2).join("/")}
              </Badge>
            ) : null
          }
        >
          {quotesV1 ? (
            <Callout title="Contains v1 source" tone="warn">
              <p>
                This section quotes v1&apos;s own source and output verbatim. v1 is private and
                unlicensed: read it here, do not copy it anywhere public. The console is local
                for exactly this reason.
              </p>
            </Callout>
          ) : null}

          {diffError ? (
            <p className="muted" style={{ fontSize: "var(--text-small)" }}>
              {diffError}
            </p>
          ) : diffSection ? (
            <div style={{ marginTop: quotesV1 ? 14 : 0 }}>
              <Markdown source={diffSection.body} />
            </div>
          ) : (
            <p className="muted" style={{ fontSize: "var(--text-small)" }}>
              The drill-down for <span className="mono">{command}</span> has no section for this
              stage.
            </p>
          )}
        </Card>
      </div>
    </main>
  );
}

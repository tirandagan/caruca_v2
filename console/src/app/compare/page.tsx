import Link from "next/link";
import {
  buildMatrix,
  summarizeStages,
  toMatrixView,
  matrixKey,
  type MatrixCell,
} from "../../data/compare.js";
import { loadCampaignSet, PARITY_CAMPAIGNS, PILOT_CAMPAIGNS } from "../../data/parityCampaigns.js";
import { Badge, Callout, Card, count } from "../../components/ui.js";

export const dynamic = "force-dynamic";

/**
 * Compare: the matrix, and what each number is counted over (§6.4).
 *
 * Every figure on this page is shown with its denominator, because several of them are not
 * what they look like. Stage 4's "agreement" is a count of agreeing cases over a count of
 * aligned ones, and its denominator moves between samples - so it is shown as "25 of 77", not
 * as 0.325 on its own.
 *
 * Filters are query parameters rather than client state: a filtered view is then a link
 * someone can put in a document, which is what a finding's evidence needs.
 */

const STAGE_LABEL: Record<string, string> = {
  syntax_spec: "Stage 1 · specification",
  generate: "Stage 2 · invocations",
  trace: "Stage 3 · tracing",
  annotate: "Stage 4 · annotation",
};

function fmt(value: number | null): string {
  return value === null ? "—" : value.toFixed(3);
}

function VerdictBadge({ cell }: { cell: MatrixCell }) {
  switch (cell.verdict) {
    case "replicates":
      return <Badge tone="ok">replicates</Badge>;
    case "improves":
      return <Badge tone="info">improves</Badge>;
    case "diverges":
      return <Badge tone="warn">diverges</Badge>;
    case "unscoreable":
      return <Badge tone="muted">not scoreable</Badge>;
  }
}

function Cell({ cell }: { cell: MatrixCell | undefined }) {
  if (!cell) return <td className="faint">not run</td>;

  return (
    <td>
      <div className="row" style={{ gap: 8 }}>
        <Link className="mono" href={`/compare/${cell.stage}/${cell.command}`}>
          {cell.pooledCounts
            ? `${cell.pooledCounts.top} of ${cell.pooledCounts.bottom}`
            : fmt(cell.value)}
        </Link>
        <VerdictBadge cell={cell} />
      </div>
      {cell.value !== null && cell.pooledCounts ? (
        <div className="event__detail mono faint">{fmt(cell.value)}</div>
      ) : null}
      {cell.unscoreableReason ? (
        <div className="event__detail faint" title={cell.unscoreableReason}>
          {cell.unscoreableReason.slice(0, 90)}
          {cell.unscoreableReason.length > 90 ? "…" : ""}
        </div>
      ) : cell.perSampleCounts ? (
        <div className="event__detail faint">
          {/* Both parts move here, so both are shown rather than a single movement figure. */}
          per sample:{" "}
          {cell.perSampleCounts
            .map((sample) =>
              sample.top === null || sample.bottom === null
                ? "—"
                : `${sample.top}/${sample.bottom}`,
            )
            .join(" · ")}
        </div>
      ) : (
        <div className="event__detail faint">
          {cell.samples} sample{cell.samples === 1 ? "" : "s"}
          {cell.spread !== null ? ` · headline moved ${cell.spread.toFixed(3)}` : ""}
        </div>
      )}
      {cell.moreVariable.length > 0 ? (
        <div className="event__detail" style={{ color: "var(--warning-text)" }}>
          {cell.moreVariable[0]!.metric} moved {cell.moreVariable[0]!.spread.toFixed(3)}
          {cell.moreVariable.length > 1 ? ` (+${cell.moreVariable.length - 1} more)` : ""}
        </div>
      ) : null}
    </td>
  );
}

export default async function ComparePage({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const params = await searchParams;
  const one = (key: string): string | undefined => {
    const value = params[key];
    return Array.isArray(value) ? value[0] : value;
  };

  const set = one("set") === "pilot" ? PILOT_CAMPAIGNS : PARITY_CAMPAIGNS;
  const campaigns = loadCampaignSet(set);

  const model = one("model");
  const variant = one("variant");
  const temperatureRaw = one("temperature");
  const temperature = temperatureRaw === undefined ? undefined : Number(temperatureRaw);

  const cells = buildMatrix(campaigns.rows, {
    ...(model ? { model } : {}),
    ...(variant ? { promptVariant: variant } : {}),
    ...(temperature !== undefined && Number.isFinite(temperature) ? { temperature } : {}),
  });
  const view = toMatrixView(cells);
  const summaries = summarizeStages(cells);

  return (
    <main className="page page--wide">
      <div className="accent-bar" />
      <div className="page__head">
        <h1>Compare</h1>
        <Badge mono>{campaigns.loaded.length} campaigns</Badge>
        <Badge tone="muted" mono>
          {count(campaigns.rows.length)} scored cells
        </Badge>
      </div>
      <p className="page__sub">
        One row per command, one column per stage. Every figure is shown with what it is counted
        over, because two of the four are not rates.
      </p>

      <div className="stack">
        {campaigns.absent.length > 0 ? (
          <Callout title="Campaigns not on this machine" tone="neutral">
            <p>
              <span className="mono">{campaigns.absent.join(", ")}</span> — campaign ledgers are
              the one part of <span className="code-inline">eval/</span> that is still
              gitignored, so a fresh checkout has none. Run the campaign, or copy{" "}
              <span className="code-inline">eval/campaigns/</span> across.
            </p>
          </Callout>
        ) : null}

        {campaigns.badLines.length > 0 ? (
          <Callout title="Unreadable ledger lines" tone="warn">
            <p>
              {campaigns.badLines.length} line
              {campaigns.badLines.length === 1 ? "" : "s"} did not parse and are missing from
              every figure below.
            </p>
          </Callout>
        ) : null}

        {cells.length === 0 ? (
          <Callout title="Nothing to compare" tone="neutral">
            <p>No scored cells matched. Clear the filters, or run a campaign first.</p>
          </Callout>
        ) : (
          <>
            <Card title="Per stage">
              <table className="table">
                <thead>
                  <tr>
                    <th>Stage</th>
                    <th>Headline figure</th>
                    <th>Counted over</th>
                    <th className="num">Value</th>
                    <th className="num">Scored</th>
                    <th className="num">Not scoreable</th>
                    <th>Widest movement in any rate</th>
                  </tr>
                </thead>
                <tbody>
                  {summaries.map((summary) => (
                    <tr key={summary.stage}>
                      <td>{STAGE_LABEL[summary.stage] ?? summary.stage}</td>
                      <td>
                        {summary.headline.label}
                        <div className="event__detail mono faint">{summary.headline.metric}</div>
                      </td>
                      <td className="faint" style={{ fontSize: "var(--text-caption)" }}>
                        {summary.headline.denominator}
                      </td>
                      <td className="num">
                        {summary.pooledCounts
                          ? `${summary.pooledCounts.top} of ${summary.pooledCounts.bottom}`
                          : fmt(summary.mean)}
                        {summary.pooledCounts ? (
                          <div className="event__detail mono faint">{fmt(summary.mean)}</div>
                        ) : null}
                      </td>
                      <td className="num">{summary.scoredCells}</td>
                      <td className="num">
                        {summary.unscoreableCells > 0 ? (
                          <span style={{ color: "var(--warning-text)" }}>
                            {summary.unscoreableCells}
                          </span>
                        ) : (
                          0
                        )}
                      </td>
                      <td>
                        {summary.widestSpread ? (
                          <>
                            <span className="mono">{summary.widestSpread.metric}</span>{" "}
                            {summary.widestSpread.spread.toFixed(3)}
                            <div className="event__detail faint">
                              on <span className="mono">{summary.widestSpread.command}</span>
                            </div>
                          </>
                        ) : (
                          <span className="faint">no rate moved</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>

            <Callout title="Why the widest movement matters" tone="info">
              <p>
                The column above deliberately reports the widest movement in <em>any</em> rate
                the stage records, not the movement in its headline. At stage 1 the headline is
                F1, which is 1.000 in every sample, while the exact-argument rate moves by
                0.200 on <span className="code-inline">tac</span>. A report that measures only
                the headline calls that stage perfectly consistent.
              </p>
            </Callout>

            <Card title={`Matrix · ${view.commands.length} commands`} flush>
              <table className="table">
                <thead>
                  <tr>
                    <th>Command</th>
                    {view.stages.map((stage) => (
                      <th key={stage}>{STAGE_LABEL[stage] ?? stage}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {view.commands.map((command) => (
                    <tr key={command}>
                      <td className="mono">{command}</td>
                      {view.stages.map((stage) => (
                        <Cell key={stage} cell={view.byKey.get(matrixKey(command, stage))} />
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>

            <Card title="Filters">
              <div className="row" style={{ gap: 18 }}>
                <div>
                  <div className="label">Model</div>
                  <div className="row" style={{ gap: 6 }}>
                    <Link href="/compare">all</Link>
                    {view.models.map((value) => (
                      <Link key={value} className="mono" href={`/compare?model=${encodeURIComponent(value)}`}>
                        {value}
                      </Link>
                    ))}
                  </div>
                </div>
                <div>
                  <div className="label">Prompt variant</div>
                  <div className="row" style={{ gap: 6 }}>
                    {view.promptVariants.map((value) => (
                      <Link key={value} className="mono" href={`/compare?variant=${encodeURIComponent(value)}`}>
                        {value}
                      </Link>
                    ))}
                  </div>
                </div>
                <div>
                  <div className="label">Campaign set</div>
                  <div className="row" style={{ gap: 6 }}>
                    <Link href="/compare">parity (P1)</Link>
                    <Link href="/compare?set=pilot">pilot (C0)</Link>
                  </div>
                </div>
              </div>
            </Card>
          </>
        )}
      </div>
    </main>
  );
}

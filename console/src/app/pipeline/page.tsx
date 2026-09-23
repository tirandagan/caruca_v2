import Link from "next/link";
import {
  IDENTICAL_INPUT,
  STAGE_ORDER,
  STAGE_ROLE,
  STAGE_TITLE,
  planPipeline,
} from "../../data/pipelinePlan.js";
import { checkEnvironment, estimateCost } from "../../data/preflight.js";
import { displayInvocation } from "../../data/v1Invocations.js";
import { sharedOptions } from "../../data/options.js";
import { Badge, Callout, Card, CodeBlock, usd } from "../../components/ui.js";
import { CountPanel } from "../../components/CountPanel.js";

export const dynamic = "force-dynamic";

/**
 * Pipeline: build a run, and see what it would do before it does it (§6.1, §6.2).
 *
 * **Nothing on this screen executes anything.** Phase 5 adds that. What it does now is the
 * part that has to be right first: show the two chains as they really are, show every command
 * line, and say which steps would cost money and how much, from measured runs rather than from
 * a guess.
 */

/** The parity study's nine commands, pinned in the picker. */
const PINNED = ["cat", "pwd", "rm", "sha256sum", "tac", "tail", "tee", "uniq", "wc"] as const;

export default async function PipelinePage({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const params = await searchParams;
  const one = (key: string): string | undefined => {
    const value = params[key];
    return Array.isArray(value) ? value[0] : value;
  };

  const command = one("command") ?? "cat";
  const model = one("model") ?? "openai/gpt-4o";
  const maxCount = one("max-count") ? Number(one("max-count")) : 1;
  const maxArity = one("max-arity") ? Number(one("max-arity")) : 1;

  const environment = checkEnvironment();
  const openAiKeyPresent =
    environment.find((check) => check.name === "OPENAI_API_KEY")?.state === "ok";

  const plan = planPipeline(STAGE_ORDER, ["v1", "v2"], {
    command,
    model,
    bounds: { maxArity, maxCount },
    openAiKeyPresent,
  });

  const shared = sharedOptions();

  return (
    <main className="page page--wide">
      <div className="accent-bar" />
      <div className="page__head">
        <h1>Pipeline</h1>
        <Badge mono>{command}</Badge>
        <Badge tone="muted" mono>
          --max-arity {maxArity} --max-count {maxCount}
        </Badge>
      </div>
      <p className="page__sub">
        What a run would consist of. Nothing here executes anything — live runs are the next
        piece of work.
      </p>

      <div className="stack">
        <Card title="Command">
          <div className="row" style={{ gap: 8 }}>
            {PINNED.map((candidate) => (
              <Link
                key={candidate}
                className="mono"
                href={`/pipeline?command=${candidate}&max-count=${maxCount}&max-arity=${maxArity}`}
                style={
                  candidate === command
                    ? { fontWeight: "var(--weight-semibold)", textDecoration: "underline" }
                    : undefined
                }
              >
                {candidate}
              </Link>
            ))}
            <span className="faint" style={{ fontSize: "var(--text-caption)" }}>
              the parity study&apos;s nine
            </span>
          </div>
        </Card>

        <Card title="Bounds · set once, applied to both sides">
          <p className="event__detail" style={{ marginTop: 0 }}>
            Different limits on each side would measure the limits rather than the systems,
            which is why these are shared.
          </p>
          <table className="table">
            <thead>
              <tr>
                <th>Option</th>
                <th>Default</th>
                <th>Now</th>
                <th>What it does</th>
              </tr>
            </thead>
            <tbody>
              {shared.map((option) => (
                <tr key={option.flag}>
                  <td className="mono">{option.flag}</td>
                  <td className="mono faint">{option.default ?? "—"}</td>
                  <td className="mono">
                    {option.flag === "--max-count"
                      ? maxCount
                      : option.flag === "--max-arity"
                        ? maxArity
                        : (option.default ?? "—")}
                  </td>
                  <td style={{ fontSize: "var(--text-caption)" }}>
                    {option.help}
                    {option.caveat ? (
                      <div className="faint" style={{ marginTop: 2 }}>
                        {option.caveat}
                      </div>
                    ) : null}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="row" style={{ gap: 10, marginTop: 12 }}>
            <span className="label">max-count</span>
            {[1, 2, 4].map((value) => (
              <Link key={value} href={`/pipeline?command=${command}&max-count=${value}&max-arity=${maxArity}`}>
                {value}
              </Link>
            ))}
            <span className="label" style={{ marginLeft: 12 }}>
              max-arity
            </span>
            {[1, 2].map((value) => (
              <Link key={value} href={`/pipeline?command=${command}&max-count=${maxCount}&max-arity=${value}`}>
                {value}
              </Link>
            ))}
          </div>
        </Card>

        <CountPanel command={command} maxArity={maxArity} maxCount={maxCount} />

        <Card title="What this would cost">
          {plan.estimatedUsd === null ? (
            <p style={{ margin: 0, fontSize: "var(--text-small)" }}>
              Nothing comparable has been measured, so there is no estimate. A figure with
              nothing behind it would only get quoted.
            </p>
          ) : (
            <>
              <div className="metrics">
                <div>
                  <div className="metric__label">Estimated, all four v2 stages</div>
                  <div className="metric__value">{usd(plan.estimatedUsd)}</div>
                  <div className="metric__basis">
                    from measured runs of each stage with {model}
                  </div>
                </div>
                <div>
                  <div className="metric__label">Steps calling a paid model</div>
                  <div className="metric__value">{plan.paidSteps.length}</div>
                </div>
              </div>
              <table className="table" style={{ marginTop: 14 }}>
                <thead>
                  <tr>
                    <th>Stage</th>
                    <th className="num">Estimate</th>
                    <th>Basis</th>
                  </tr>
                </thead>
                <tbody>
                  {STAGE_ORDER.map((stage) => {
                    const estimate = estimateCost(stage, model);
                    return (
                      <tr key={stage}>
                        <td>{STAGE_TITLE[stage]}</td>
                        <td className="num">
                          {estimate.usdPerRun === null ? (
                            <span className="faint">no estimate</span>
                          ) : (
                            usd(estimate.usdPerRun)
                          )}
                        </td>
                        <td className="faint" style={{ fontSize: "var(--text-caption)" }}>
                          {estimate.basis}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </>
          )}
          {plan.unestimatedSteps > 0 ? (
            <p className="event__detail" style={{ color: "var(--warning-text)" }}>
              {plan.unestimatedSteps} paid step
              {plan.unestimatedSteps === 1 ? " has" : "s have"} no measured run behind them, so
              the total above understates the cost.
            </p>
          ) : null}
        </Card>

        {plan.blockers.length > 0 ? (
          <Callout title="Would not run" tone="warn">
            {plan.blockers.map((blocker, index) => (
              <p key={index}>
                <span className="mono">
                  {blocker.side} {STAGE_TITLE[blocker.stage]}
                </span>{" "}
                — {blocker.reason}
              </p>
            ))}
          </Callout>
        ) : null}

        {STAGE_ORDER.map((stage) => {
          const v1 = plan.steps.find((step) => step.stage === stage && step.side === "v1")!;
          const v2 = plan.steps.find((step) => step.stage === stage && step.side === "v2")!;
          const identical = IDENTICAL_INPUT[stage];

          return (
            <Card key={stage} title={STAGE_TITLE[stage]}>
              <div className="split">
                {/* v1 on the left, v2 on the right (decision 4). */}
                <div>
                  <div className="row" style={{ marginBottom: 8 }}>
                    <span className="label">v1</span>
                    {v1.inChain ? (
                      <Badge tone="muted" mono>
                        {v1.where === "lima" ? "lima vm" : "this mac"}
                      </Badge>
                    ) : (
                      <Badge tone="info">not a step in v1&apos;s chain</Badge>
                    )}
                  </div>
                  <p className="event__detail" style={{ marginTop: 0 }}>
                    {STAGE_ROLE[stage].v1}
                  </p>
                  {v1.invocation ? (
                    <CodeBlock>{displayInvocation(v1.invocation)}</CodeBlock>
                  ) : (
                    <p className="muted" style={{ fontSize: "var(--text-small)" }}>
                      No command: this step reads an archived artifact.
                    </p>
                  )}
                  {v1.notes.map((note) => (
                    <p key={note} className="event__detail faint">
                      {note}
                    </p>
                  ))}
                  {v1.invocation ? (
                    <p className="event__detail faint">
                      Runs from <span className="mono">{v1.invocation.cwd}</span>
                      {v1.invocation.outputPath ? (
                        <>
                          , writing to{" "}
                          <span className="mono">{v1.invocation.outputPath}</span> — inside the
                          run&apos;s own folder, never v1&apos;s.
                        </>
                      ) : null}
                    </p>
                  ) : null}
                </div>

                <div>
                  <div className="row" style={{ marginBottom: 8 }}>
                    <span className="label">v2</span>
                    <Badge tone="muted" mono>
                      {v2.where === "lima" ? "lima vm" : "this mac"}
                    </Badge>
                    {v2.callsModel ? <Badge tone="warn">calls a paid model</Badge> : null}
                  </div>
                  <p className="event__detail" style={{ marginTop: 0 }}>
                    {STAGE_ROLE[stage].v2}
                  </p>
                  <CodeBlock>{(v2.v2Argv ?? []).join(" ")}</CodeBlock>
                  {v2.estimate?.usdPerRun != null ? (
                    <p className="event__detail faint">
                      About {usd(v2.estimate.usdPerRun)} — {v2.estimate.basis}
                    </p>
                  ) : (
                    <p className="event__detail faint">
                      {v2.estimate?.basis ?? "no estimate"}
                    </p>
                  )}
                  <p className="event__detail faint">{v2.whyThere}</p>
                </div>
              </div>

              {identical ? (
                <div style={{ marginTop: 12 }}>
                  <Callout title="Same input, one switch" tone="info">
                    <p>
                      For a comparison on identical input, v2 can take {identical.takes} —{" "}
                      {identical.note}.
                    </p>
                  </Callout>
                </div>
              ) : null}
            </Card>
          );
        })}

        <Card title="Environment">
          <table className="table">
            <thead>
              <tr>
                <th>Check</th>
                <th>State</th>
                <th>Detail</th>
              </tr>
            </thead>
            <tbody>
              {environment.map((check) => (
                <tr key={check.name}>
                  <td>{check.name}</td>
                  <td>
                    {check.state === "ok" ? (
                      <Badge tone="ok">ok</Badge>
                    ) : check.state === "missing" ? (
                      <Badge tone="warn">missing</Badge>
                    ) : (
                      <Badge tone="muted">unknown</Badge>
                    )}
                  </td>
                  <td className="faint" style={{ fontSize: "var(--text-caption)" }}>
                    {check.detail}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>
    </main>
  );
}

/**
 * The small presentational pieces, styled strictly from the caruca-design system.
 *
 * Two of these carry a rule rather than a look:
 *
 *   - `Metric` renders an absent value as the word "not recorded", in italic sans, and will
 *     not accept a number for something that was never measured. v1 records no tokens for its
 *     LLM step and no per-step timing; showing either as `0` would assert that v1's LLM step
 *     is free, which is the exact gap this project exists to close.
 *   - `Num` formats every figure in mono and, where one is given, prints its basis beside it -
 *     the denominator, the sample count, the method. A rate without its basis is how the
 *     parity study's 0.185 survived review.
 */
import type { ReactNode } from "react";

export function Badge({
  tone = "muted",
  mono = false,
  dot = false,
  children,
}: {
  tone?: "ok" | "warn" | "bad" | "info" | "muted";
  mono?: boolean;
  dot?: boolean;
  children: ReactNode;
}) {
  return (
    <span className={`badge badge--${tone}${mono ? " badge--mono" : ""}`}>
      {dot ? <span className="badge__dot" /> : null}
      {children}
    </span>
  );
}

export function Card({
  title,
  aside,
  flush = false,
  children,
}: {
  title?: ReactNode;
  aside?: ReactNode;
  flush?: boolean;
  children: ReactNode;
}) {
  return (
    <section className="card">
      {title ? (
        <header className="card__head">
          <span className="label">{title}</span>
          {aside ? <span className="spacer">{aside}</span> : null}
        </header>
      ) : null}
      <div className={`card__body${flush ? " card__body--flush" : ""}`}>{children}</div>
    </section>
  );
}

export function Callout({
  title,
  tone = "info",
  children,
}: {
  title: string;
  tone?: "info" | "warn" | "neutral";
  children: ReactNode;
}) {
  const cls = tone === "info" ? "callout" : `callout callout--${tone}`;
  return (
    <div className={cls}>
      <div className="callout__title">{title}</div>
      {children}
    </div>
  );
}

/**
 * A measured number, with its basis.
 *
 * `basis` is not decoration. "0.208" means nothing without "over the 24 cells where it is
 * defined", and the project has already published one figure that was wrong because the
 * denominator went unstated.
 */
export function Metric({
  label,
  value,
  unit,
  basis,
  absentReason,
}: {
  label: string;
  value?: string | number;
  unit?: string;
  basis?: string;
  /** When given, the value was never recorded. Rendered as words, never as zero. */
  absentReason?: string;
}) {
  return (
    <div>
      <div className="metric__label">{label}</div>
      {absentReason ? (
        <div className="metric__value metric__value--absent" title={absentReason}>
          not recorded
        </div>
      ) : (
        <div className="metric__value">
          {value}
          {unit ? <span className="metric__basis"> {unit}</span> : null}
        </div>
      )}
      {basis ? <div className="metric__basis">{basis}</div> : null}
      {absentReason ? <div className="metric__basis">{absentReason}</div> : null}
    </div>
  );
}

export function KeyValue({
  rows,
}: {
  rows: { k: string; v: ReactNode; absent?: boolean; title?: string }[];
}) {
  return (
    <div className="kv">
      {rows.map((row) => (
        <div key={row.k} style={{ display: "contents" }}>
          <div className="kv__k">{row.k}</div>
          <div className={row.absent ? "kv__v kv__v--absent" : "kv__v"} title={row.title}>
            {row.v}
          </div>
        </div>
      ))}
    </div>
  );
}

export function CodeBlock({ children }: { children: ReactNode }) {
  return <pre className="codeblock mono">{children}</pre>;
}

/** Seconds, to the precision the figure actually carries. */
export function seconds(value: number): string {
  if (value >= 100) return `${value.toFixed(0)} s`;
  if (value >= 10) return `${value.toFixed(1)} s`;
  return `${value.toFixed(2)} s`;
}

/** Dollars. Sub-cent figures are the normal case here, so four decimals is the floor. */
export function usd(value: number): string {
  if (value === 0) return "$0";
  if (value < 0.0001) return `$${value.toExponential(1)}`;
  return `$${value.toFixed(4)}`;
}

export function count(value: number): string {
  return value.toLocaleString("en-US");
}

/**
 * A recorded figure, shown at the precision it is claimed to.
 *
 * A rate stored as `1.0` parses as `1`, and printing it as "1" understates the claim: the
 * finding says the F1 was 1.000, and "1" reads like a rough figure. Counts are printed whole.
 */
export function figure(value: number): string {
  if (Number.isInteger(value)) {
    return Math.abs(value) <= 1 ? value.toFixed(3) : count(value);
  }
  const decimals = String(value).split(".")[1]?.length ?? 3;
  return value.toFixed(Math.max(decimals, Math.abs(value) <= 1 ? 3 : 0));
}

import Link from "next/link";
import { listFindings } from "../../data/findings.js";
import { repoPaths } from "../../data/paths.js";
import { Badge, Callout, Card, KeyValue, figure } from "../../components/ui.js";
import { Markdown } from "../../components/Markdown.js";
import { RecheckPanel } from "../../components/RecheckPanel.js";

export const dynamic = "force-dynamic";

/**
 * Findings: the project's conclusions, each tied to the numbers behind it.
 *
 * One Markdown file per finding in `ai_docs/analysis/findings/`. The console reads and writes
 * those files and keeps no numbers of its own; git history, co-author review and the existing
 * Markdown-to-PDF pipeline all already work on files, and a database would be a second source
 * of truth for numbers that live in run directories.
 *
 * The re-check — recomputing each recorded number with today's scorer and marking it "matches"
 * or "changed" — is the next piece of work. Until it exists, this page shows what is recorded
 * and says plainly that nothing has been verified, rather than displaying figures in a way
 * that implies they have been.
 */

const STATUS_TONE: Record<string, "ok" | "warn" | "bad" | "info" | "muted"> = {
  confirmed: "ok",
  draft: "info",
  corrected: "warn",
  superseded: "muted",
  withdrawn: "bad",
};

export default function FindingsPage() {
  const { findings, unreadable } = listFindings();
  const directory = repoPaths().findings.replace(`${repoPaths().root}/`, "");

  return (
    <main className="page">
      <div className="accent-bar" />
      <div className="page__head">
        <h1>Findings</h1>
        <Badge mono>{findings.length}</Badge>
      </div>
      <p className="page__sub">
        One file per claim, in <span className="code-inline">{directory}</span>, each carrying the
        numbers behind it and where they came from.
      </p>

      <div className="stack">
        {unreadable.length > 0 ? (
          <Callout title="Unreadable" tone="warn">
            {unreadable.map((entry) => (
              <p key={entry.file} className="mono">
                {entry.file}: {entry.reason}
              </p>
            ))}
          </Callout>
        ) : null}

        {findings.length === 0 ? (
          <Callout title="No findings recorded yet" tone="neutral">
            <p>
              The project&apos;s conclusions are currently spread across prose —{" "}
              <span className="mono">ai_docs/analysis/v1_v2_parity_study.md</span>,{" "}
              <span className="mono">white_paper_addendum.md</span>,{" "}
              <span className="mono">e0_artifact_pinning.md</span> and several memory notes.
              Converting them into finding files, and re-checking each number on the way in, is
              the next piece of work on this screen.
            </p>
            <p>
              The point of the format is the re-check: every number carries the runs it came
              from, its metric, its method and its denominator, so it can be recomputed with
              today&apos;s scorer and marked as still matching or as changed. That check would
              have caught both errors already corrected in the parity study.
            </p>
          </Callout>
        ) : (
          findings.map((finding) => (
            <div key={finding.frontmatter.id} id={finding.frontmatter.id}>
            <Card
              title={finding.frontmatter.id}
              aside={
                <Badge tone={STATUS_TONE[finding.frontmatter.status] ?? "muted"}>
                  {finding.frontmatter.status}
                </Badge>
              }
            >
              <p style={{ marginTop: 0, fontSize: "var(--text-body)" }}>
                {finding.frontmatter.claim}
              </p>

              <KeyValue
                rows={[
                  {
                    k: "Dimensions",
                    v: finding.frontmatter.dimensions.join(", ") || "none stated",
                    absent: finding.frontmatter.dimensions.length === 0,
                  },
                  {
                    k: "Stages",
                    v: finding.frontmatter.stages.join(", ") || "none stated",
                    absent: finding.frontmatter.stages.length === 0,
                  },
                  {
                    k: "Bears on",
                    v: finding.frontmatter.paper_sections.join(", ") || "no paper section stated",
                    absent: finding.frontmatter.paper_sections.length === 0,
                  },
                  {
                    k: "Needs v1's authors",
                    v: finding.frontmatter.needs_v1_authors ? "yes" : "no",
                  },
                ]}
              />

              {finding.frontmatter.evidence.length > 0 ? (
                <table className="table" style={{ marginTop: 14 }}>
                  <thead>
                    <tr>
                      <th>Number</th>
                      <th className="num">Value</th>
                      <th>Counted over</th>
                      <th>Method</th>
                      <th>From</th>
                    </tr>
                  </thead>
                  <tbody>
                    {finding.frontmatter.evidence.map((evidence) => (
                      <tr key={evidence.label}>
                        <td>{evidence.label}</td>
                        <td className="num">{figure(evidence.value)}</td>
                        <td className="faint" style={{ fontSize: "var(--text-caption)" }}>
                          {evidence.denominator}
                        </td>
                        <td className="mono faint">
                          {evidence.method}
                          {evidence.recheck === null ? (
                            <div className="event__detail faint">not recomputable</div>
                          ) : null}
                        </td>
                        <td>
                          {evidence.run_ids.map((runId, index) => (
                            <span key={runId}>
                              {index > 0 ? ", " : ""}
                              <Link className="mono" href={`/runs/${runId}`}>
                                {runId.slice(0, 22)}…
                              </Link>
                            </span>
                          ))}
                          {evidence.campaign_ids.length > 0 ? (
                            <span className="mono faint">
                              {evidence.run_ids.length > 0 ? " · " : ""}
                              {evidence.campaign_ids.join(", ")}
                            </span>
                          ) : null}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p className="muted" style={{ fontSize: "var(--text-small)" }}>
                  No evidence is recorded for this claim yet.
                </p>
              )}

              {/* The plain-language explanation. §6.6 asks for one on every finding, and it
                  is where the reasoning that does not fit in a claim sentence lives. */}
              {finding.body ? (
                <div style={{ marginTop: 14, borderTop: "1px solid var(--border-default)", paddingTop: 12 }}>
                  <Markdown source={finding.body} />
                </div>
              ) : null}

              {finding.frontmatter.source_document ? (
                <p className="event__detail faint" style={{ marginTop: 8 }}>
                  First written in <span className="mono">{finding.frontmatter.source_document}</span>
                </p>
              ) : null}

              <RecheckPanel findingId={finding.frontmatter.id} />

              {finding.frontmatter.corrections.length > 0 ? (
                <div style={{ marginTop: 14 }}>
                  <div className="label">Corrections</div>
                  {finding.frontmatter.corrections.map((correction, index) => (
                    <p key={index} className="event__detail">
                      {correction.date}: <span className="mono">{String(correction.old_value)}</span>{" "}
                      → <span className="mono">{String(correction.new_value)}</span> —{" "}
                      {correction.why}
                    </p>
                  ))}
                </div>
              ) : null}
            </Card>
            </div>
          ))
        )}
      </div>
    </main>
  );
}

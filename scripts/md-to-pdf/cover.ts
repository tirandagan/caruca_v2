import { LOGO_DATA_URI } from "./assets/logo-base64";
import { fontFaceCss, tokensCss } from "./tokens";

interface CoverOptions {
  title: string;
  subtitle?: string;
  sourceFile: string;
  dateTime: string;
  pageCount: number;
}

export function generateCoverHtml(options: CoverOptions): string {
  const { title, subtitle, sourceFile, dateTime, pageCount } = options;

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    /*
      Fonts are loaded from this repo, never from a CDN. The cover previously
      pulled Lexend Deca from Google Fonts, which meant the most brand-critical
      page in the document was the one page that silently fell back to a system
      sans whenever the renderer had no network — and it requested a 300 weight
      that this project does not ship.
    */
    ${fontFaceCss()}
    ${tokensCss()}

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: var(--font-sans);
      color: var(--text-body);
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    .cover-page {
      width: 8.5in;
      height: 11in;
      display: flex;
      flex-direction: column;
      padding: 1.5in 1.25in;
      position: relative;
      overflow: hidden;
    }

    /*
      Concentric rings bleeding off the corner — the third brand accent motif.
      Kept at the specified 1-4% teal so it reads as a watermark under the type
      rather than as a shape competing with it.
    */
    .cover-page::before {
      content: '';
      position: absolute;
      top: -2.6in;
      right: -2.6in;
      width: 5.5in;
      height: 5.5in;
      border-radius: 50%;
      border: 26px solid rgba(14, 116, 144, 0.05);
      box-shadow:
        0 0 0 54px rgba(14, 116, 144, 0.032),
        0 0 0 100px rgba(14, 116, 144, 0.018);
    }

    .cover-header {
      display: flex;
      align-items: center;
      gap: 16px;
      position: relative;
    }

    .cover-logo {
      height: 48px;
      width: auto;
    }

    .cover-brand-name {
      font-size: 22pt;
      font-weight: 700;
      line-height: 1;
      letter-spacing: var(--tracking-heading);
      color: var(--ink);
    }

    /* Upright, not italic: Lexend Deca has no italic cut to set this in. */
    .cover-tagline {
      font-size: var(--text-caption);
      font-weight: 400;
      color: var(--text-muted);
      margin-top: 5px;
      letter-spacing: var(--tracking-body);
    }

    /*
      The title block sits on the lower third rather than dead center, so the
      cover reads top-down as mark, then title, then provenance, instead of
      leaving a void between the subtitle and the footer.
    */
    .cover-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding-right: 0.75in;
      padding-bottom: 1.1in;
      position: relative;
    }

    .cover-title {
      font-size: 38pt;
      font-weight: 700;
      color: var(--ink);
      line-height: 1.08;
      letter-spacing: -0.015em;
      text-wrap: balance;
      margin-bottom: 0.35em;
    }

    .cover-subtitle {
      font-size: 15pt;
      font-weight: 400;
      color: var(--text-secondary);
      line-height: 1.35;
      max-width: 26em;
    }

    /* Accent bar: 80x4, teal to ink. The same mark sits under every page title. */
    .cover-accent {
      width: 80px;
      height: 4px;
      background: var(--accent-gradient);
      border-radius: 2px;
      margin-top: 1.6em;
    }

    .cover-footer {
      border-top: var(--border-w) solid var(--border-subtle);
      padding-top: 1.2em;
      position: relative;
    }

    .cover-meta {
      display: grid;
      grid-template-columns: 5.5em 1fr;
      gap: 8px 1em;
      align-items: baseline;
      font-size: var(--text-caption);
      color: var(--text-secondary);
    }

    /* Micro-labels: uppercase, tracked out, muted — per the brand's label spec. */
    .cover-meta-label {
      font-size: var(--text-label);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: var(--tracking-label);
      color: var(--text-faint);
    }

    /* A file path is a machine string, so it sets in mono and wraps on any character. */
    .cover-meta-path {
      font-family: var(--font-mono);
      font-size: 8.5pt;
      line-height: 1.45;
      word-break: break-all;
    }

    .cover-company {
      margin-top: 1.4em;
      font-size: var(--text-label);
      letter-spacing: var(--tracking-label);
      text-transform: uppercase;
      color: var(--text-faint);
    }
  </style>
</head>
<body>
  <div class="cover-page">
    <div class="cover-header">
      <img src="${LOGO_DATA_URI}" class="cover-logo" alt="Caruca" />
      <div class="cover-brand">
        <div class="cover-brand-name">Caruca v2</div>
        <div class="cover-tagline">LLM-based specification mining for opaque shell commands</div>
      </div>
    </div>

    <div class="cover-body">
      <h1 class="cover-title">${escapeHtml(title)}</h1>
      ${subtitle ? `<div class="cover-subtitle">${escapeHtml(subtitle)}</div>` : ""}
      <div class="cover-accent"></div>
    </div>

    <div class="cover-footer">
      <div class="cover-meta">
        <span class="cover-meta-label">Source</span>
        <span class="cover-meta-path">${escapeHtml(sourceFile)}</span>
        <span class="cover-meta-label">Generated</span>
        <span>${escapeHtml(dateTime)}</span>
        <span class="cover-meta-label">Pages</span>
        <span>${pageCount}</span>
      </div>
      <div class="cover-company">Caruca v2 &mdash; research project</div>
    </div>
  </div>
</body>
</html>`;
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

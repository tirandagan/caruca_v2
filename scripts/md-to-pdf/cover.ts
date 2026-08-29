import { LOGO_DATA_URI } from "./assets/logo-base64";

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
    @import url('https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@300;400;600;700&display=swap');

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Lexend Deca', -apple-system, 'Segoe UI', sans-serif;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    .cover-page {
      width: 8.5in;
      height: 11in;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 1.5in 1.25in;
      position: relative;
      overflow: hidden;
    }

    /* Decorative rings in background */
    .cover-page::before {
      content: '';
      position: absolute;
      top: -3in;
      right: -3in;
      width: 8in;
      height: 8in;
      border-radius: 50%;
      border: 60px solid rgba(14, 116, 144, 0.04);
      box-shadow:
        0 0 0 120px rgba(14, 116, 144, 0.03),
        0 0 0 180px rgba(14, 116, 144, 0.02),
        0 0 0 240px rgba(14, 116, 144, 0.01);
    }

    .cover-header {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .cover-logo {
      height: 48px;
      width: auto;
    }

    .cover-brand {
      display: flex;
      flex-direction: column;
    }

    .cover-brand-name {
      font-size: 22pt;
      font-weight: 700;
      line-height: 1;
      color: #0B1F33;
    }

    .cover-tagline {
      font-size: 9pt;
      font-weight: 400;
      color: #616B73;
      margin-top: 4px;
      font-style: italic;
    }

    .cover-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding-right: 1in;
    }

    .cover-title {
      font-size: 38pt;
      font-weight: 700;
      color: #0B1F33;
      line-height: 1.1;
      margin-bottom: 0.4em;
    }

    .cover-subtitle {
      font-size: 16pt;
      font-weight: 400;
      color: #475569;
      line-height: 1.3;
      margin-bottom: 0.6em;
    }

    .cover-accent {
      width: 80px;
      height: 4px;
      background: linear-gradient(to right, #0E7490, #0B1F33);
      border-radius: 2px;
      margin-top: 0.5em;
    }

    .cover-footer {
      border-top: 1px solid #E5E7EB;
      padding-top: 1.2em;
    }

    .cover-meta {
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 9.5pt;
      color: #616B73;
    }

    .cover-meta-row {
      display: flex;
      gap: 0.5em;
    }

    .cover-meta-label {
      font-weight: 600;
      color: #475569;
      min-width: 80px;
    }

    .cover-company {
      margin-top: 1.2em;
      font-size: 8pt;
      color: #9CA3AF;
    }
  </style>
</head>
<body>
  <div class="cover-page">
    <div class="cover-header">
      <img src="${LOGO_DATA_URI}" class="cover-logo" alt="Caruca" />
      <div class="cover-brand">
        <div class="cover-brand-name">Caruca v2</div>
        <div class="cover-tagline">LLM-based specification mining for opaque shell commands.</div>
      </div>
    </div>

    <div class="cover-body">
      <h1 class="cover-title">${escapeHtml(title)}</h1>
      ${subtitle ? `<div class="cover-subtitle">${escapeHtml(subtitle)}</div>` : ""}
      <div class="cover-accent"></div>
    </div>

    <div class="cover-footer">
      <div class="cover-meta">
        <div class="cover-meta-row">
          <span class="cover-meta-label">Source</span>
          <span>${escapeHtml(sourceFile)}</span>
        </div>
        <div class="cover-meta-row">
          <span class="cover-meta-label">Generated</span>
          <span>${escapeHtml(dateTime)}</span>
        </div>
        <div class="cover-meta-row">
          <span class="cover-meta-label">Pages</span>
          <span>${pageCount}</span>
        </div>
      </div>
      <div class="cover-company">Caruca v2 - Research Project</div>
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

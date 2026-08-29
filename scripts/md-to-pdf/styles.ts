import path from "path";

const FONTS_DIR = path.resolve(__dirname, "fonts");

export function getStyles(): string {
  const fontsDir = FONTS_DIR.replace(/\\/g, "/");

  return `
    @font-face {
      font-family: 'Lexend Deca';
      src: url('file://${fontsDir}/LexendDeca-Regular.ttf') format('truetype');
      font-weight: 400;
      font-style: normal;
    }
    @font-face {
      font-family: 'Lexend Deca';
      src: url('file://${fontsDir}/LexendDeca-SemiBold.ttf') format('truetype');
      font-weight: 600;
      font-style: normal;
    }
    @font-face {
      font-family: 'Lexend Deca';
      src: url('file://${fontsDir}/LexendDeca-Bold.ttf') format('truetype');
      font-weight: 700;
      font-style: normal;
    }
    @font-face {
      font-family: 'JetBrains Mono';
      src: url('file://${fontsDir}/JetBrainsMono-Regular.woff2') format('woff2');
      font-weight: 400;
      font-style: normal;
    }

    /* ========== BASE ========== */

    *, *::before, *::after {
      box-sizing: border-box;
    }

    body {
      font-family: 'Lexend Deca', -apple-system, 'Segoe UI', sans-serif;
      font-size: 11pt;
      line-height: 1.5;
      letter-spacing: 0.01em;
      word-spacing: 0.05em;
      color: #0B1F33;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* ========== HEADINGS ========== */

    h1, h2, h3, h4, h5, h6 {
      font-family: 'Lexend Deca', -apple-system, 'Segoe UI', sans-serif;
      letter-spacing: -0.01em;
      line-height: 1.2;
      page-break-after: avoid;
      break-after: avoid;
      break-inside: avoid;
    }

    h1 + *, h2 + *, h3 + *, h4 + *, h5 + *, h6 + * {
      break-before: avoid;
    }

    .heading-group {
      break-inside: avoid;
    }

    h1 {
      font-size: 28pt;
      font-weight: 700;
      color: #0B1F33;
      margin-top: 2em;
      margin-bottom: 0.5em;
      padding-bottom: 0.3em;
      border-bottom: 2px solid #2563EB;
    }

    h1:first-child {
      margin-top: 0;
    }

    h2 {
      font-size: 20pt;
      font-weight: 700;
      color: #2563EB;
      margin-top: 1.8em;
      margin-bottom: 0.4em;
    }

    h3 {
      font-size: 15pt;
      font-weight: 600;
      color: #0B1F33;
      margin-top: 1.5em;
      margin-bottom: 0.3em;
    }

    h4 {
      font-size: 12pt;
      font-weight: 600;
      color: #0B1F33;
      margin-top: 1.2em;
      margin-bottom: 0.25em;
    }

    h5 {
      font-size: 11pt;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #374151;
      margin-top: 1em;
      margin-bottom: 0.2em;
    }

    h6 {
      font-size: 9pt;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #616B73;
      margin-top: 1em;
      margin-bottom: 0.2em;
    }

    /* ========== PARAGRAPHS & TEXT ========== */

    p {
      margin: 0 0 0.6em 0;
      orphans: 3;
      widows: 3;
    }

    strong { font-weight: 700; }
    em { font-style: italic; }
    del { text-decoration: line-through; color: #616B73; }

    a {
      color: #2563EB;
      text-decoration: none;
    }

    small {
      font-size: 9pt;
      color: #616B73;
    }

    /* ========== LISTS ========== */

    ul, ol {
      margin: 0.5em 0 1em 0;
      padding-left: 1.5em;
    }

    li {
      margin-bottom: 0.3em;
      line-height: 1.5;
    }

    li > ul, li > ol {
      margin-top: 0.2em;
      margin-bottom: 0.2em;
    }

    ul { list-style-type: disc; }
    ul ul { list-style-type: circle; }
    ul ul ul { list-style-type: square; }

    ol { list-style-type: decimal; }
    ol ol { list-style-type: lower-alpha; }
    ol ol ol { list-style-type: lower-roman; }

    /* ========== TASK LISTS ========== */

    .task-list-item {
      list-style: none;
      margin-left: -1.5em;
      padding-left: 0;
    }

    .task-list-item input[type="checkbox"] {
      appearance: none;
      -webkit-appearance: none;
      width: 14px;
      height: 14px;
      border: 2px solid #D0D7DE;
      border-radius: 3px;
      vertical-align: middle;
      margin-right: 0.5em;
      position: relative;
      top: -1px;
    }

    .task-list-item input[type="checkbox"]:checked {
      background-color: #2563EB;
      border-color: #2563EB;
    }

    .task-list-item input[type="checkbox"]:checked::after {
      content: '\\2713';
      color: white;
      font-size: 10px;
      position: absolute;
      top: -1px;
      left: 1px;
    }

    /* ========== CODE ========== */

    pre {
      background-color: #F6F8FA;
      border: 1px solid #D0D7DE;
      border-radius: 6px;
      padding: 16px;
      margin: 1em 0;
      overflow-x: hidden;
      white-space: pre-wrap;
      word-wrap: break-word;
      break-inside: avoid;
      page-break-inside: avoid;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    pre code {
      font-family: 'JetBrains Mono', 'Consolas', monospace;
      font-size: 9.5pt;
      line-height: 1.4;
      background: none;
      padding: 0;
      border: none;
      border-radius: 0;
    }

    /* Shiki overrides for print */
    pre.shiki {
      background-color: #F6F8FA !important;
      border: 1px solid #D0D7DE;
      border-radius: 6px;
      padding: 16px;
      margin: 1em 0;
      overflow-x: hidden;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    pre.shiki code {
      font-family: 'JetBrains Mono', 'Consolas', monospace;
      font-size: 9.5pt;
      line-height: 1.4;
    }

    /* Language label */
    pre[data-language]::before {
      content: attr(data-language);
      display: block;
      text-align: right;
      font-family: 'Lexend Deca', sans-serif;
      font-size: 8pt;
      color: #656D76;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 8px;
      padding-bottom: 6px;
      border-bottom: 1px solid #D0D7DE;
    }

    /* Long code blocks (>40 lines) can break across pages */
    pre.long-code {
      break-inside: auto;
      page-break-inside: auto;
    }

    /* Inline code */
    code:not(pre code) {
      font-family: 'JetBrains Mono', 'Consolas', monospace;
      background-color: #EFF1F3;
      padding: 0.15em 0.35em;
      border-radius: 4px;
      font-size: 0.9em;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* ========== BLOCKQUOTES ========== */

    blockquote {
      border-left: 3px solid #2563EB;
      margin: 1.5em 0;
      padding: 0.5em 0 0.5em 1.5em;
      color: #374151;
      font-style: italic;
      break-inside: avoid;
    }

    blockquote p:last-child {
      margin-bottom: 0;
    }

    /* ========== CALLOUT BOXES ========== */

    .callout {
      border-left: 4px solid;
      border-radius: 0 6px 6px 0;
      padding: 16px 20px;
      margin: 1.5em 0;
      break-inside: avoid;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    .callout-title {
      font-weight: 600;
      font-size: 10pt;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.5em;
    }

    .callout-info {
      border-color: #2563EB;
      background: #EFF6FF;
    }
    .callout-info .callout-title { color: #2563EB; }

    .callout-warning {
      border-color: #E6A817;
      background: #FFFBEB;
    }
    .callout-warning .callout-title { color: #B8860B; }

    .callout-tip {
      border-color: #16A34A;
      background: #ECFDF5;
    }
    .callout-tip .callout-title { color: #15803D; }

    .callout-danger {
      border-color: #DF2E2E;
      background: #FEF2F2;
    }
    .callout-danger .callout-title { color: #DC2626; }

    /* ========== TABLES ========== */

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.5em 0;
      font-size: 10pt;
      break-inside: avoid;
    }

    thead {
      background: #F1F5F9;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    th {
      font-weight: 600;
      text-align: left;
      padding: 10px 12px;
      border-bottom: 2px solid #334155;
      font-size: 9pt;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: #475569;
    }

    td {
      padding: 8px 12px;
      border-bottom: 1px solid #E2E8F0;
      vertical-align: top;
    }

    tbody tr:nth-child(even) {
      background: #F8FAFC;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* ========== HORIZONTAL RULES ========== */

    hr {
      border: none;
      height: 1px;
      background: linear-gradient(to right, transparent, #D1D5DB, transparent);
      margin: 2em 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* ========== IMAGES ========== */

    img {
      max-width: 100%;
      height: auto;
      display: block;
      margin: 1em auto;
      break-inside: avoid;
    }

    /* ========== DIAGRAMS (rendered from mermaid/plantuml/etc. fences) ========== */

    figure.diagram {
      margin: 1.5em auto;
      text-align: center;
      break-inside: avoid;
    }

    figure.diagram svg {
      max-width: 100%;
      height: auto;
      display: block;
      margin: 0 auto;
    }

    /* ========== FOOTNOTES ========== */

    .footnotes {
      margin-top: 3em;
      padding-top: 1em;
      border-top: 1px solid #D1D5DB;
      font-size: 9pt;
      color: #616B73;
    }

    .footnotes ol {
      padding-left: 1.5em;
    }

    .footnotes li {
      margin-bottom: 0.5em;
    }

    .footnote-ref {
      font-size: 0.75em;
      vertical-align: super;
      color: #2563EB;
      text-decoration: none;
    }

    .footnote-backref {
      color: #2563EB;
      text-decoration: none;
    }

    /* ========== PRINT ========== */

    @media print {
      a { color: #2563EB; text-decoration: none; }
      * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
    }
  `;
}

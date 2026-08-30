import { fontFaceCss, tokensCss } from "./tokens";

export function getStyles(): string {
  return `
    ${fontFaceCss()}
    ${tokensCss()}

    /* ========== BASE ========== */

    *, *::before, *::after {
      box-sizing: border-box;
    }

    body {
      font-family: var(--font-sans);
      font-size: var(--text-body-size);
      line-height: var(--leading-body);
      letter-spacing: var(--tracking-body);
      color: var(--text-body);
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* ========== HEADINGS ========== */

    h1, h2, h3, h4, h5, h6 {
      font-family: var(--font-sans);
      letter-spacing: var(--tracking-heading);
      line-height: var(--leading-heading);
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

    /*
      The page title carries the brand's accent bar (80x4, teal to ink) rather
      than a full-width rule. It is one of the three sanctioned accent motifs,
      and it is the same mark the cover sets under its title.
    */
    h1 {
      font-size: var(--text-display);
      font-weight: 700;
      color: var(--ink);
      margin-top: 2em;
      margin-bottom: 0.5em;
      padding-bottom: 0.45em;
      position: relative;
    }

    h1::after {
      content: '';
      position: absolute;
      left: 0;
      bottom: 0;
      width: 80px;
      height: 4px;
      background: var(--accent-gradient);
      border-radius: 2px;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    h1:first-child {
      margin-top: 0;
    }

    h2 {
      font-size: var(--text-h2);
      font-weight: 700;
      color: var(--blue);
      margin-top: 1.8em;
      margin-bottom: 0.4em;
    }

    h3 {
      font-size: var(--text-h3);
      font-weight: 600;
      color: var(--ink);
      margin-top: 1.5em;
      margin-bottom: 0.3em;
    }

    h4 {
      font-size: var(--text-h4);
      font-weight: 600;
      color: var(--ink);
      margin-top: 1.2em;
      margin-bottom: 0.25em;
    }

    /* h5 and h6 are micro-labels: uppercase, tracked out, no heading tightening. */
    h5 {
      font-size: var(--text-body-size);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: var(--tracking-label);
      color: var(--gray-700);
      margin-top: 1.4em;
      margin-bottom: 0.35em;
    }

    h6 {
      font-size: var(--text-caption);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: var(--tracking-label);
      color: var(--text-muted);
      margin-top: 1.4em;
      margin-bottom: 0.35em;
    }

    /* ========== PARAGRAPHS & TEXT ========== */

    p {
      margin: 0 0 0.6em 0;
      orphans: 3;
      widows: 3;
    }

    strong { font-weight: 700; }
    em { font-style: italic; }
    del { text-decoration: line-through; color: var(--text-muted); }

    a {
      color: var(--text-link);
      text-decoration: none;
    }

    small {
      font-size: var(--text-caption);
      color: var(--text-muted);
    }

    /* ========== LISTS ========== */

    ul, ol {
      margin: 0.5em 0 1em 0;
      padding-left: 1.5em;
    }

    li {
      margin-bottom: 0.3em;
      line-height: var(--leading-body);
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

    li::marker {
      color: var(--gray-400);
    }

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
      border: var(--border-w-strong) solid var(--border-strong);
      border-radius: var(--radius-xs);
      vertical-align: middle;
      margin-right: 0.5em;
      position: relative;
      top: -1px;
    }

    .task-list-item input[type="checkbox"]:checked {
      background-color: var(--blue);
      border-color: var(--blue);
    }

    .task-list-item input[type="checkbox"]:checked::after {
      content: '\\2713';
      color: var(--surface-page);
      font-size: 10px;
      position: absolute;
      top: -1px;
      left: 1px;
    }

    /* ========== CODE ========== */

    pre {
      background-color: var(--surface-code);
      border: var(--border-w) solid var(--border-strong);
      border-radius: var(--radius-md);
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
      font-family: var(--font-mono);
      font-size: var(--text-code);
      line-height: 1.4;
      background: none;
      padding: 0;
      border: none;
      border-radius: 0;
    }

    /* Shiki overrides for print */
    pre.shiki {
      background-color: var(--surface-code) !important;
      border: var(--border-w) solid var(--border-strong);
      border-radius: var(--radius-md);
      padding: 16px;
      margin: 1em 0;
      overflow-x: hidden;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    pre.shiki code {
      font-family: var(--font-mono);
      font-size: var(--text-code);
      line-height: 1.4;
    }

    /* Language label — a micro-label, top right, over a hairline. */
    pre[data-language]::before {
      content: attr(data-language);
      display: block;
      text-align: right;
      font-family: var(--font-sans);
      font-size: var(--text-label);
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: var(--tracking-label);
      margin-bottom: 8px;
      padding-bottom: 6px;
      border-bottom: var(--border-w) solid var(--border-strong);
    }

    /* Long code blocks (>40 lines) can break across pages */
    pre.long-code {
      break-inside: auto;
      page-break-inside: auto;
    }

    /* Inline code */
    code:not(pre code) {
      font-family: var(--font-mono);
      background-color: var(--surface-inline-code);
      padding: 0.15em 0.35em;
      border-radius: var(--radius-sm);
      font-size: 0.9em;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* ========== BLOCKQUOTES ========== */

    /*
      Lexend Deca ships no italic cut, so italic here would be a synthesized
      oblique. The bar and the color do the work instead.
    */
    blockquote {
      border-left: var(--callout-bar) solid var(--blue);
      margin: 1.5em 0;
      padding: 0.5em 0 0.5em 1.5em;
      color: var(--gray-700);
      break-inside: avoid;
    }

    blockquote p:last-child {
      margin-bottom: 0;
    }

    /* ========== CALLOUT BOXES ========== */

    .callout {
      border-left: var(--callout-bar) solid;
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      padding: 16px 20px;
      margin: 1.5em 0;
      break-inside: avoid;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    .callout > :last-child {
      margin-bottom: 0;
    }

    .callout-title {
      font-weight: 600;
      font-size: var(--text-small);
      text-transform: uppercase;
      letter-spacing: var(--tracking-label);
      margin-bottom: 0.5em;
    }

    .callout-info {
      border-color: var(--blue);
      background: var(--surface-info);
    }
    .callout-info .callout-title { color: var(--blue); }

    .callout-warning {
      border-color: var(--warning);
      background: var(--warning-bg);
    }
    .callout-warning .callout-title { color: var(--warning-text); }

    .callout-tip {
      border-color: var(--success);
      background: var(--success-bg);
    }
    .callout-tip .callout-title { color: var(--success-text); }

    .callout-danger {
      border-color: var(--danger);
      background: var(--danger-bg);
    }
    .callout-danger .callout-title { color: var(--danger-text); }

    /* ========== TABLES ========== */

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.5em 0;
      font-size: var(--text-small);
      break-inside: avoid;
    }

    thead {
      background: var(--surface-thead);
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    th {
      font-weight: 600;
      text-align: left;
      padding: 10px 12px;
      border-bottom: var(--border-w-strong) solid var(--border-thead);
      font-size: var(--text-caption);
      text-transform: uppercase;
      letter-spacing: var(--tracking-thead);
      color: var(--gray-600);
    }

    td {
      padding: 8px 12px;
      border-bottom: var(--border-w) solid var(--border-default);
      vertical-align: top;
    }

    tbody tr:nth-child(even) {
      background: var(--surface-zebra);
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /*
      Measurements set in mono. A right-aligned markdown column (---: in the header rule) is a
      numeric column by convention, so its figures get the mono face and lining,
      tabular numerals — digits line up down the column, which is the whole point
      of a comparison table.
    */
    td[style*="text-align:right"] {
      font-family: var(--font-mono);
      font-size: 9pt;
      font-variant-numeric: tabular-nums lining-nums;
      font-feature-settings: 'tnum' 1, 'lnum' 1;
      white-space: nowrap;
    }

    /* A code chip inside a numeric cell is already mono; drop the chip surface. */
    td[style*="text-align:right"] code:not(pre code) {
      background: none;
      padding: 0;
    }

    /* ========== HORIZONTAL RULES ========== */

    hr {
      border: none;
      height: 1px;
      background: linear-gradient(to right, transparent, var(--border-hr), transparent);
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
      border-top: var(--border-w) solid var(--border-hr);
      font-size: var(--text-caption);
      color: var(--text-muted);
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
      color: var(--text-link);
      text-decoration: none;
    }

    .footnote-backref {
      color: var(--text-link);
      text-decoration: none;
    }

    /* ========== PRINT ========== */

    @media print {
      a { color: var(--text-link); text-decoration: none; }
      * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
    }
  `;
}

import { LOGO_DATA_URI } from "./assets/logo-base64";
import { getStyles } from "./styles";
import { tocStyles } from "./toc";
import { TOKENS } from "./tokens";
import fs from "fs";
import path from "path";

/*
  Chromium renders the running head and foot in their own document, which cannot load the page's
  file-URL @font-face rules, so the brand face must be embedded inline as a data URI. Without this the
  head and foot fall back to a system serif (seen 2026-11-24).
*/
const RUNNING_HEAD_FONT_FACE = (() => {
  const f = path.resolve(__dirname, "fonts", "LexendDeca-Regular.ttf");
  const b64 = fs.readFileSync(f).toString("base64");
  const fs6 = fs.readFileSync(path.resolve(__dirname, "fonts", "LexendDeca-SemiBold.ttf")).toString("base64");
  return `<style>@font-face{font-family:'Lexend Deca';font-weight:400;src:url(data:font/ttf;base64,${b64}) format('truetype')}@font-face{font-family:'Lexend Deca';font-weight:600;src:url(data:font/ttf;base64,${fs6}) format('truetype')}</style>`;
})();


/*
  Chromium renders `headerTemplate` and `footerTemplate` in their own document,
  which inherits none of the page CSS and cannot resolve custom properties or
  local @font-face rules. These two templates are therefore the only place in the
  pipeline that writes literal values — taken from TOKENS so they still move with
  the palette — and they name the font stack inline, falling back to the system
  sans that Chromium substitutes here regardless.
*/
const RUNNING_HEAD_FONT =
  "'Lexend Deca', -apple-system, 'Segoe UI', sans-serif";

export function getHeaderTemplate(title: string): string {
  const truncatedTitle =
    title.length > 78 ? title.slice(0, 75) + "..." : title;

  return `${RUNNING_HEAD_FONT_FACE}
    <div style="width: 100%; font-size: 8pt; font-family: ${RUNNING_HEAD_FONT}; color: ${TOKENS.color.gray500}; padding: 0 0.75in; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid ${TOKENS.color.borderSubtle}; padding-bottom: 6px;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <img src="${LOGO_DATA_URI}" alt="Caruca logo" style="height: 16px; width: auto;" />
        <span style="font-weight: 600; color: ${TOKENS.color.ink};">Caruca v2</span>
      </div>
      <span>${escapeHtml(truncatedTitle)}</span>
    </div>
  `;
}

export function getFooterTemplate(): string {
  return `${RUNNING_HEAD_FONT_FACE}
    <div style="width: 100%; font-size: 8pt; font-family: ${RUNNING_HEAD_FONT}; color: ${TOKENS.color.gray500}; padding: 0 0.75in; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid ${TOKENS.color.borderSubtle}; padding-top: 6px;">
      <span style="text-transform: uppercase; letter-spacing: 0.05em;">Caruca v2</span>
      <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
    </div>
  `;
}

export function wrapBodyHtml(
  bodyContent: string,
  tocHtml: string,
  baseDir: string
): string {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <base href="file://${baseDir}/">
  <style>
    ${getStyles()}
    ${tocStyles}
  </style>
</head>
<body>
  ${tocHtml}
  <div class="body-content">
    ${bodyContent}
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

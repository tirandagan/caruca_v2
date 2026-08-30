import { LOGO_DATA_URI } from "./assets/logo-base64";
import { getStyles } from "./styles";
import { tocStyles } from "./toc";
import { TOKENS } from "./tokens";

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
    title.length > 50 ? title.slice(0, 47) + "..." : title;

  return `
    <div style="width: 100%; font-size: 8pt; font-family: ${RUNNING_HEAD_FONT}; color: ${TOKENS.color.gray400}; padding: 0 0.75in; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid ${TOKENS.color.borderSubtle}; padding-bottom: 6px;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <img src="${LOGO_DATA_URI}" style="height: 16px; width: auto;" />
        <span style="font-weight: 600; color: ${TOKENS.color.ink};">Caruca v2</span>
      </div>
      <span>${escapeHtml(truncatedTitle)}</span>
    </div>
  `;
}

export function getFooterTemplate(): string {
  return `
    <div style="width: 100%; font-size: 8pt; font-family: ${RUNNING_HEAD_FONT}; color: ${TOKENS.color.gray400}; padding: 0 0.75in; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid ${TOKENS.color.borderSubtle}; padding-top: 6px;">
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

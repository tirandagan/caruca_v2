/**
 * Builds report.pdf from report.html + report.css, hand-authored, in the Caruca document identity.
 *
 * Run from the repo root:   npx tsx naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/report/build.ts [running title]
 *
 * What it does: reads report.html and report.css from this folder, injects the repo's brand fonts
 * and colour tokens (the same `scripts/md-to-pdf/tokens.ts` the Markdown converter uses, so the two
 * stay one system), renders Letter portrait with Chromium (puppeteer), then stamps the running head and
 * foot onto every page with pdf-lib using the real Lexend Deca files. (Chromium's own header/footer
 * templates cannot load the brand font and fall back to Times, seen 2026-11-24, so they are not used.)
 *
 * To update the report: edit report.html (content) or report.css (layout), re-run this script.
 * Figures are referenced by relative path from report.html; regenerate them with the scripts in
 * ../figures_interim/ and re-run. Page breaks are CSS (`break-before: page` on `.page-break`).
 */
import fs from "fs";
import path from "path";
import { pathToFileURL } from "url";
import puppeteer from "puppeteer";
import { PDFDocument, rgb } from "pdf-lib";
import fontkit from "@pdf-lib/fontkit";
import { fontFaceCss, tokensCss, TOKENS } from "../../../../scripts/md-to-pdf/tokens";
import { LOGO_DATA_URI } from "../../../../scripts/md-to-pdf/assets/logo-base64";

const HERE = __dirname;
const FONTS = path.resolve(HERE, "../../../../scripts/md-to-pdf/fonts");
const FONTS_ACADEMIC = path.join(FONTS, "academic"); // Libertinus (the maintained Linux Libertine) + Inconsolata, as ACM acmart uses

function academicFontFaceCss(): string {
  const u = (f: string) => pathToFileURL(path.join(FONTS_ACADEMIC, f.endsWith('.otf') ? 'ttf/' + f.replace('.otf', '.ttf') : f)).href; // TrueType conversions: Chromium embeds CFF OTF as Type 3
  const face = (fam: string, f: string, w: number, st = "normal") =>
    `@font-face{font-family:'${fam}';src:url('${u(f)}') format('truetype');font-weight:${w};font-style:${st};}`;
  return [
    face("Libertinus Serif", "LibertinusSerif-Regular.otf", 400), face("Libertinus Serif", "LibertinusSerif-Italic.otf", 400, "italic"),
    face("Libertinus Serif", "LibertinusSerif-Semibold.otf", 600), face("Libertinus Serif", "LibertinusSerif-Bold.otf", 700),
    face("Libertinus Serif", "LibertinusSerif-BoldItalic.otf", 700, "italic"),
    face("Libertinus Sans", "LibertinusSans-Regular.otf", 400), face("Libertinus Sans", "LibertinusSans-Italic.otf", 400, "italic"),
    face("Libertinus Sans", "LibertinusSans-Bold.otf", 700),
    `@font-face{font-family:'Inconsolata';src:url('${u("ttf/Inconsolata-Regular.ttf")}') format('truetype');font-weight:400;}`,
    `@font-face{font-family:'Inconsolata';src:url('${u("ttf/Inconsolata-Bold.ttf")}') format('truetype');font-weight:700;}`,
  ].join("");
}
const htmlPath = path.join(HERE, "report.html");
const cssPath = path.join(HERE, "report.css");
const outPath = path.join(HERE, "report.pdf");
const runningTitle = process.argv[2] ?? "PaSh's benchmark suite under three sources of annotations"; // no "fi" ligature: pdf-lib mis-spaces it

const PT = 72; // points per inch
const MARGIN = { top: 1.0 * PT, bottom: 0.9 * PT, left: 1.1 * PT, right: 1.1 * PT }; // ~6.3 in measure, close to acmart's acmsmall

function hex(h: string) {
  const n = parseInt(h.slice(1), 16);
  return rgb(((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255);
}

async function main() {
  const html = fs.readFileSync(htmlPath, "utf8");
  const css = fs.readFileSync(cssPath, "utf8");
  const page = html.replace(
    "</head>",
    `<style>${fontFaceCss()}${academicFontFaceCss()}${tokensCss()}</style>\n<style>${css}</style>\n<base href="${pathToFileURL(HERE + "/").href}">\n</head>`,
  );
  const tmp = path.join(HERE, ".report.render.html");
  fs.writeFileSync(tmp, page);

  const browser = await puppeteer.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  let pdfBytes: Uint8Array;
  try {
    const p = await browser.newPage();
    await p.goto(pathToFileURL(tmp).href, { waitUntil: "networkidle0" });
    await p.emulateMediaType("print");
    pdfBytes = await p.pdf({
      format: "Letter",
      preferCSSPageSize: false,
      printBackground: true,
      displayHeaderFooter: false,
      margin: { top: `${MARGIN.top / PT}in`, bottom: `${MARGIN.bottom / PT}in`, left: `${MARGIN.left / PT}in`, right: `${MARGIN.right / PT}in` },
      tagged: true,
    });
  } finally {
    await browser.close();
    fs.unlinkSync(tmp);
  }

  // Running head and foot, in the brand face, on every page.
  const doc = await PDFDocument.load(pdfBytes);
  doc.registerFontkit(fontkit);
  const regular = await doc.embedFont(fs.readFileSync(path.join(FONTS_ACADEMIC, "ttf", "LibertinusSans-Regular.ttf")), { subset: false });
  const semibold = await doc.embedFont(fs.readFileSync(path.join(FONTS_ACADEMIC, "ttf", "LibertinusSans-Bold.ttf")), { subset: false });
  const logo = await doc.embedPng(Buffer.from(LOGO_DATA_URI.split(",")[1], "base64"));
  const ink = hex(TOKENS.color.ink);
  const grey = hex(TOKENS.color.gray500);
  const rule = hex(TOKENS.color.borderSubtle);
  const pages = doc.getPages();
  const total = pages.length;
  const size = 8;
  pages.forEach((pg, i) => {
    const { width, height } = pg.getSize();
    const x0 = MARGIN.left, x1 = width - MARGIN.right;
    // head
    const headY = height - MARGIN.top + 22;
    const logoH = 12, logoW = (logo.width / logo.height) * logoH;
    pg.drawImage(logo, { x: x0, y: headY - 2, width: logoW, height: logoH });
    pg.drawText("Caruca v2", { x: x0 + logoW + 6, y: headY, size, font: semibold, color: ink });
    const tw = regular.widthOfTextAtSize(runningTitle, size);
    pg.drawText(runningTitle, { x: x1 - tw, y: headY, size, font: regular, color: grey });
    pg.drawLine({ start: { x: x0, y: headY - 7 }, end: { x: x1, y: headY - 7 }, thickness: 0.5, color: rule });
    // foot
    const footY = MARGIN.bottom - 26;
    pg.drawLine({ start: { x: x0, y: footY + 12 }, end: { x: x1, y: footY + 12 }, thickness: 0.5, color: rule });
    pg.drawText("CARUCA V2", { x: x0, y: footY, size, font: regular, color: grey });
    const pn = `Page ${i + 1} of ${total}`;
    pg.drawText(pn, { x: x1 - regular.widthOfTextAtSize(pn, size), y: footY, size, font: regular, color: grey });
  });
  const out = await doc.save();
  fs.writeFileSync(outPath, out);
  console.log(`wrote ${path.relative(process.cwd(), outPath)}: ${total} pages, ${(out.length / 1024).toFixed(0)} KB`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});

/**
 * Builds report.pdf from report.html + report.css, hand-authored, in the Caruca document identity.
 *
 * Run from the repo root:   npx tsx naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/report/build.ts [running title]
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
import { PDFDocument, rgb, PDFName, PDFDict, PDFArray, PDFRef, PDFHexString, PDFNumber, PDFNull } from "pdf-lib";
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
const runningTitle = process.argv[2] ?? "A naive LLM's annotations against Caruca's on PaSh's benchmark suite"; // no "fi" ligature: pdf-lib mis-spaces it

const PT = 72; // points per inch
const MARGIN = { top: 1.0 * PT, bottom: 0.9 * PT, left: 1.1 * PT, right: 1.1 * PT }; // ~6.3 in measure, close to acmart's acmsmall

function hex(h: string) {
  const n = parseInt(h.slice(1), 16);
  return rgb(((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255);
}

type Labels = Record<string, string>; // xr id -> ", p. N" (or "")

// In-page steps, run after every load (fresh DOM each pass).
function prepareDom(labels: Labels, measure: boolean) {
  // 1. Lettered table notes (ACM style): letters restart per table; markers and back-links are set here.
  document.querySelectorAll<HTMLOListElement>("ol.tnotes").forEach((ol) => {
    const letters = "abcdefghijklmnopqrstuvwxyz";
    Array.from(ol.children).forEach((li, i) => {
      const id = li.id, L = letters[i];
      const marks = Array.from(document.querySelectorAll<HTMLAnchorElement>(`a.tn[href="#${id}"]`));
      marks.forEach((m, k) => { m.textContent = L; if (k === 0) m.id = `ref-${id}`; });
      const lt = document.createElement("span"); lt.className = "lt"; lt.textContent = L;
      li.insertBefore(lt, li.firstChild);
      if (marks.length) {
        const back = document.createElement("a"); back.className = "back"; back.href = `#ref-${id}`; back.textContent = "↩";
        li.appendChild(document.createTextNode(" ")); li.appendChild(back);
      }
    });
  });
  // 2. Ids on every cross-reference so its own page can be measured.
  const xrs = Array.from(document.querySelectorAll<HTMLAnchorElement>("a.xr"));
  xrs.forEach((a, i) => { if (!a.id) a.id = `xr-${i}`; });
  // 3. Page numbers from the previous pass.
  xrs.forEach((a) => {
    const t = labels[a.id];
    if (t) { const sp = document.createElement("span"); sp.className = "pg"; sp.textContent = t; a.after(sp); }
  });
  // 4. Measuring pass only: links to every id we need a position for, on pages after the document.
  if (measure) {
    const box = document.createElement("section");
    box.style.breakBefore = "page";
    const ids = Array.from(document.querySelectorAll("[id]")).map((e) => e.id).filter((x) => x);
    box.innerHTML = ids.map((x) => `<a href="#${x}">${x}</a>`).join(" ");
    document.body.appendChild(box);
  }
}

// Which DOM facts the build needs: every xr's target and whether it gets a page label; outline entries.
function collectDom() {
  const xrs = Array.from(document.querySelectorAll<HTMLAnchorElement>("a.xr")).map((a) => ({
    id: a.id,
    target: a.getAttribute("href")!.slice(1),
    skip: !!a.closest(".contents, table.recs, .pg"),
  }));
  const out: { id: string; title: string; level: number }[] = [];
  document.querySelectorAll<HTMLElement>("h2[id], h3[id], p.tcap[id], figure[id]").forEach((e) => {
    let title = "", level = 2;
    if (e.tagName === "H2") { level = 1; title = (e.classList.contains("addendum-h") ? "A  " : "") + e.textContent!.trim(); }
    else if (e.tagName === "H3") { title = e.textContent!.trim(); }
    else {
      const b = e.querySelector("b")?.textContent?.replace(/:$/, "") ?? "";
      const cap = e.tagName === "FIGURE" ? e.querySelector("figcaption")!.textContent! : e.textContent!;
      const rest = cap.replace(/^\s*(Table|Figure) [A.0-9]+:\s*/, "").split(/(?<=[.;])\s/)[0];
      title = `${b}: ${rest}`; if (title.length > 80) title = title.slice(0, 80).replace(/\s+\S*$/, "") + " …"; level = 3;
    }
    out.push({ id: e.id, title: title.replace(/\s+/g, " "), level });
  });
  // number the h2 titles as the CSS counter does
  let n = 0;
  out.forEach((o) => { if (o.level === 1 && !/^A\s/.test(o.title)) { n++; o.title = `${n}  ${o.title}`; } });
  return { xrs, out };
}

type Dest = { page: number; y: number };
function readDests(doc: PDFDocument): Map<string, Dest> {
  const pageIdx = new Map(doc.getPages().map((p, i) => [p.ref.toString(), i]));
  const res = new Map<string, Dest>();
  const add = (name: string, v: any) => {
    let arr = v instanceof PDFArray ? v : (v instanceof PDFDict ? v.lookup(PDFName.of("D")) : undefined);
    if (!(arr instanceof PDFArray)) return;
    const pref = arr.get(0) as PDFRef;
    const y = arr.size() > 3 ? (arr.lookup(3) as any)?.asNumber?.() ?? 0 : 0;
    res.set(name, { page: pageIdx.get(pref.toString()) ?? -1, y });
  };
  const cat = doc.catalog;
  const dests = cat.lookup(PDFName.of("Dests"));
  if (dests instanceof PDFDict) dests.entries().forEach(([k, v]) => add(k.decodeText ? k.decodeText() : k.toString().slice(1), doc.context.lookup(v)));
  const walk = (node: PDFDict) => {
    const names = node.lookup(PDFName.of("Names"));
    if (names instanceof PDFArray) for (let i = 0; i < names.size(); i += 2) {
      const k: any = names.lookup(i); add(k.decodeText(), names.lookup(i + 1));
    }
    const kids = node.lookup(PDFName.of("Kids"));
    if (kids instanceof PDFArray) for (let i = 0; i < kids.size(); i++) walk(kids.lookup(i) as PDFDict);
  };
  const nm = cat.lookup(PDFName.of("Names"));
  if (nm instanceof PDFDict) { const d = nm.lookup(PDFName.of("Dests")); if (d instanceof PDFDict) walk(d); }
  return res;
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
  const title = (html.match(/<title>([^<]*)<\/title>/) ?? [, runningTitle])[1]!.replace(/&#39;|&rsquo;/g, "'");

  const browser = await puppeteer.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const p = await browser.newPage();
  const render = async (labels: Labels, measure: boolean) => {
    await p.goto(pathToFileURL(tmp).href, { waitUntil: "networkidle0" });
    await p.emulateMediaType("print");
    await p.evaluate(prepareDom, labels, measure);
    const dom = await p.evaluate(collectDom);
    const bytes = await p.pdf({
      format: "Letter", preferCSSPageSize: false, printBackground: true, displayHeaderFooter: false,
      margin: { top: `${MARGIN.top / PT}in`, bottom: `${MARGIN.bottom / PT}in`, left: `${MARGIN.left / PT}in`, right: `${MARGIN.right / PT}in` },
      tagged: true,
    });
    return { bytes, dom };
  };

  // Two-pass page numbers: measure, label, measure again until the labels stop changing.
  let labels: Labels = {};
  let dests = new Map<string, Dest>();
  let dom: Awaited<ReturnType<typeof render>>["dom"] | undefined;
  let docPages = 0;
  for (let pass = 1; pass <= 5; pass++) {
    const m = await render(labels, true);
    const mdoc = await PDFDocument.load(m.bytes);
    dests = readDests(mdoc);
    dom = m.dom;
    const next: Labels = {};
    for (const x of m.dom.xrs) {
      const t = dests.get(x.target), own = dests.get(x.id);
      if (!t || !own) throw new Error(`no destination for ${x.target} or ${x.id}`);
      next[x.id] = !x.skip && t.page !== own.page ? `, p. ${t.page + 1}` : "";
    }
    const same = JSON.stringify(next) === JSON.stringify(labels);
    labels = next;
    console.log(`pass ${pass}: ${Object.values(labels).filter(Boolean).length} page labels${same ? " (stable)" : ""}`);
    if (same) break;
  }
  const fin = await render(labels, false);
  await browser.close();
  fs.unlinkSync(tmp);
  let pdfBytes: Uint8Array = fin.bytes;

  const doc = await PDFDocument.load(pdfBytes);
  doc.registerFontkit(fontkit);
  doc.setTitle(title, { showInWindowTitleBar: true });
  const pages = doc.getPages();
  const total = pages.length;

  // Outline (bookmarks) from headings and captions, at the measured positions.
  const entries = dom!.out.map((o) => ({ ...o, d: dests.get(o.id) })).filter((o) => o.d && o.d.page >= 0 && o.d.page < total);
  const ctx = doc.context;
  const root = ctx.obj({ Type: "Outlines" }) as PDFDict;
  const rootRef = ctx.register(root);
  type Node = { ref: PDFRef; dict: PDFDict; kids: Node[] };
  const top: Node[] = [];
  const stack: { level: number; node: Node }[] = [];
  for (const e of entries) {
    const dest = ctx.obj([pages[e.d!.page].ref, PDFName.of("XYZ"), PDFNull, e.d!.y + 14, PDFNull]);
    const dict = ctx.obj({ Title: PDFHexString.fromText(e.title), Dest: dest }) as PDFDict;
    const node: Node = { ref: ctx.register(dict), dict, kids: [] };
    while (stack.length && stack[stack.length - 1].level >= e.level) stack.pop();
    const parent = stack.length ? stack[stack.length - 1].node : undefined;
    (parent ? parent.kids : top).push(node);
    dict.set(PDFName.of("Parent"), parent ? parent.ref : rootRef);
    stack.push({ level: e.level, node });
  }
  const link = (list: Node[], parent: PDFDict) => {
    list.forEach((n, i) => {
      if (i > 0) n.dict.set(PDFName.of("Prev"), list[i - 1].ref);
      if (i < list.length - 1) n.dict.set(PDFName.of("Next"), list[i + 1].ref);
      if (n.kids.length) { link(n.kids, n.dict); n.dict.set(PDFName.of("Count"), PDFNumber.of(-n.kids.length)); }
    });
    if (list.length) { parent.set(PDFName.of("First"), list[0].ref); parent.set(PDFName.of("Last"), list[list.length - 1].ref); parent.set(PDFName.of("Count"), PDFNumber.of(list.length)); }
  };
  link(top, root);
  doc.catalog.set(PDFName.of("Outlines"), rootRef);
  doc.catalog.set(PDFName.of("PageMode"), PDFName.of("UseOutlines"));
  console.log(`outline: ${entries.length} entries`);

  // Running head (current section) and foot (page n of N).
  const heads = dom!.out.filter((o) => o.level === 1 || /^A\.\d/.test(o.title)).map((o) => ({ t: o.title.replace(/\s+/g, " "), d: dests.get(o.id)! })).filter((o) => o.d);
  const sectionOn = (i: number) => {
    let cur = title;
    for (const h of heads) if (h.d.page <= i) cur = h.t; // a heading on this page names the page
    return i === 0 ? title : cur;
  };
  const regular = await doc.embedFont(fs.readFileSync(path.join(FONTS_ACADEMIC, "ttf", "LibertinusSans-Regular.ttf")), { subset: false });
  const semibold = await doc.embedFont(fs.readFileSync(path.join(FONTS_ACADEMIC, "ttf", "LibertinusSans-Bold.ttf")), { subset: false });
  const logo = await doc.embedPng(Buffer.from(LOGO_DATA_URI.split(",")[1], "base64"));
  const ink = hex(TOKENS.color.ink);
  const grey = hex(TOKENS.color.gray500);
  const rule = hex(TOKENS.color.borderSubtle);
  const size = 8;
  pages.forEach((pg, i) => {
    const { width, height } = pg.getSize();
    const x0 = MARGIN.left, x1 = width - MARGIN.right;
    const headY = height - MARGIN.top + 22;
    const logoH = 12, logoW = (logo.width / logo.height) * logoH;
    pg.drawImage(logo, { x: x0, y: headY - 2, width: logoW, height: logoH });
    pg.drawText("Caruca v2", { x: x0 + logoW + 6, y: headY, size, font: semibold, color: ink });
    let head = i === 0 ? runningTitle : sectionOn(i);
    const maxW = x1 - (x0 + logoW + 70);
    while (regular.widthOfTextAtSize(head, size) > maxW) head = head.slice(0, -2) + "…";
    const tw = regular.widthOfTextAtSize(head, size);
    // pdf-lib's layout applies the fi/ff/fl ligatures but spaces them wrongly: draw each such pair in two pieces
    let hx = x1 - tw;
    for (const seg of head.split(/(?<=f)(?=[fil])/)) {
      pg.drawText(seg, { x: hx, y: headY, size, font: regular, color: grey });
      hx += regular.widthOfTextAtSize(seg, size);
    }
    pg.drawLine({ start: { x: x0, y: headY - 7 }, end: { x: x1, y: headY - 7 }, thickness: 0.5, color: rule });
    const footY = MARGIN.bottom - 26;
    pg.drawLine({ start: { x: x0, y: footY + 12 }, end: { x: x1, y: footY + 12 }, thickness: 0.5, color: rule });
    const pn = `Page ${i + 1} of ${total}`;
    pg.drawText(pn, { x: x1 - regular.widthOfTextAtSize(pn, size), y: footY, size, font: regular, color: grey });
  });
  const out = await doc.save();
  fs.writeFileSync(outPath, out);
  fs.writeFileSync(path.join(HERE, ".page_labels.json"), JSON.stringify({ labels, dests: Object.fromEntries(dests) }, null, 1));
  console.log(`wrote ${path.relative(process.cwd(), outPath)}: ${total} pages, ${(out.length / 1024).toFixed(0)} KB`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});

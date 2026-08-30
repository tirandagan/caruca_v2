import fs from "fs";
import path from "path";
import { pathToFileURL } from "url";
import sharp from "sharp";
import { JSDOM } from "jsdom";
import crypto from "crypto";
import MarkdownIt from "markdown-it";
import footnote from "markdown-it-footnote";
import taskLists from "markdown-it-task-lists";
import anchor from "markdown-it-anchor";
import container from "markdown-it-container";
import { createHighlighter, type Highlighter } from "shiki";
import puppeteer from "puppeteer";
import { PDFDocument } from "pdf-lib";
import { carucaSyntaxTheme, CARUCA_THEME_NAME } from "./shiki-theme";
import { generateToc } from "./toc";
import { generateCoverHtml } from "./cover";
import { getHeaderTemplate, getFooterTemplate, wrapBodyHtml } from "./templates";
import { prepareDiagrams, installDiagramRenderer } from "./diagrams";

interface ConvertOptions {
  inputPath: string;
  outputPath: string;
  title?: string;
  subtitle?: string;
}

export async function convertMarkdownToPdf(options: ConvertOptions): Promise<void> {
  const { inputPath, outputPath, subtitle } = options;
  const absoluteInput = path.resolve(inputPath);
  const baseDir = path.dirname(absoluteInput).replace(/\\/g, "/");

  console.log("  Parsing markdown...");
  const markdown = stripFrontmatter(fs.readFileSync(absoluteInput, "utf-8"));

  // Title precedence: explicit --title flag > first H1 > filename
  const titleMatch = markdown.match(/^#\s+(.+)$/m);
  const title = options.title ?? (titleMatch ? titleMatch[1].trim() : path.basename(inputPath, ".md"));

  // Initialize highlighter
  console.log("  Initializing syntax highlighter...");
  const highlighter = await createHighlighter({
    themes: [carucaSyntaxTheme],
    langs: [
      "typescript", "javascript", "bash", "json", "sql",
      "css", "html", "python", "yaml", "markdown", "diff",
      "tsx", "jsx", "shell", "plaintext",
    ],
  });

  // Configure markdown-it
  const md = createMarkdownIt(highlighter);

  // Render any diagram code fences (mermaid, plantuml, etc.) to inline images
  // and swap them in for the source script during HTML rendering.
  const diagrams = await prepareDiagrams(md, markdown);
  installDiagramRenderer(md, diagrams);

  // Render HTML
  console.log("  Rendering HTML...");
  let html = md.render(markdown);

  // Fold manual <a id> anchors into the heading that follows them, so internal
  // links resolve to the heading (and travel with it across page breaks); drop
  // any leftover empty anchor paragraphs.
  html = normalizeAnchors(html);

  // Mark long code blocks first, so heading grouping can leave the ones that
  // are allowed to break across pages ungrouped.
  html = markLongCodeBlocks(html);

  // Wrap heading groups (orphan prevention fallback)
  html = wrapHeadingGroups(html);

  // Generate TOC
  console.log("  Generating table of contents...");
  const { tocHtml, bodyHtml } = generateToc(html);

  // Wrap in full HTML document
  const fullBodyHtml = wrapBodyHtml(bodyHtml, tocHtml, baseDir);

  // Downscale oversized local raster images so the embedded PDF stays a sane
  // size (source art can be several MB each; a Letter page never needs more
  // than ~1600px wide). Originals are never touched: resized copies go to a
  // temp dir, get swapped into the HTML, and are removed after rendering.
  console.log("  Optimizing images...");
  const { html: bodyHtmlForRender, tempDir: imgTempDir } = await optimizeLocalImages(fullBodyHtml, baseDir);

  // Write the body HTML to a temp file inside baseDir so Puppeteer loads it from
  // a real file:// origin. Chromium blocks file:// subresources (local images)
  // when content is injected via setContent (an about:blank origin), so relative
  // image paths only resolve when the document itself is served from file://.
  const tmpHtmlPath = path.join(baseDir, `.md-to-pdf.${process.pid}.tmp.html`);
  const tmpCoverPath = path.join(baseDir, `.md-to-pdf.cover.${process.pid}.tmp.html`);
  fs.writeFileSync(tmpHtmlPath, bodyHtmlForRender);

  // Launch browser
  console.log("  Launching browser...");
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  try {
    // Pass 1: Render body to get page count
    console.log("  Rendering body PDF...");
    const bodyPage = await browser.newPage();
    await bodyPage.goto(pathToFileURL(tmpHtmlPath).href, { waitUntil: "networkidle0" });
    await bodyPage.emulateMediaType("print");

    const bodyPdfBuffer = await bodyPage.pdf({
      format: "Letter",
      preferCSSPageSize: false,
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: getHeaderTemplate(title),
      footerTemplate: getFooterTemplate(),
      margin: {
        top: "1in",
        bottom: "0.85in",
        left: "0.75in",
        right: "0.75in",
      },
      tagged: true,
    });
    await bodyPage.close();

    // Count pages in body PDF
    const bodyPdf = await PDFDocument.load(bodyPdfBuffer);
    const bodyPageCount = bodyPdf.getPageCount();
    const totalPages = bodyPageCount + 1; // +1 for cover

    // Pass 2: Render cover with page count
    console.log("  Rendering cover page...");
    const now = new Date();
    const dateTime = now.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    }) + " at " + now.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });

    const coverHtml = generateCoverHtml({
      title,
      subtitle,
      sourceFile: inputPath,
      dateTime,
      pageCount: totalPages,
    });

    // Write the cover to a temp file for the same reason the body is written to
    // one: Chromium blocks file:// subresources from a setContent document,
    // whose origin is about:blank. The cover loads its typefaces from this
    // repo, so under setContent every request for Lexend Deca was blocked and
    // the cover — the most brand-critical page in the document — silently
    // rendered in a system fallback. Awaiting document.fonts.ready cannot fix
    // that, because the request is refused rather than slow.
    fs.writeFileSync(tmpCoverPath, coverHtml);

    const coverPage = await browser.newPage();
    await coverPage.goto(pathToFileURL(tmpCoverPath).href, { waitUntil: "networkidle0" });
    // Ensure the faces have finished loading before the cover is snapshotted,
    // so the title is rendered with the intended typeface (not a fallback).
    await coverPage.evaluate(async () => {
      await document.fonts.ready;
    });
    await coverPage.emulateMediaType("print");

    const coverPdfBuffer = await coverPage.pdf({
      format: "Letter",
      printBackground: true,
      displayHeaderFooter: false,
      margin: { top: "0", bottom: "0", left: "0", right: "0" },
    });
    await coverPage.close();

    // Merge cover + body.
    //
    // Use the body PDF itself as the base document and prepend the cover, rather
    // than copying body pages into a fresh document. Rebuilding via copyPages
    // discards the catalog-level structures the body relies on — the named
    // destination / link tree and the tagged-PDF structure tree — which breaks
    // every internal hyperlink (TOC entries, cross-references and footnote
    // ref/back-ref links highlight but no longer jump). Keeping the body
    // document intact and inserting a single cover page preserves them; link
    // destinations reference page objects, so prepending a page does not
    // disturb them.
    console.log("  Assembling final PDF...");
    const finalPdf = await PDFDocument.load(bodyPdfBuffer);

    // Set PDF metadata
    finalPdf.setTitle(title);
    finalPdf.setAuthor("Caruca v2");
    finalPdf.setSubject("Technical Documentation");
    finalPdf.setCreator("Caruca v2 PDF Converter");
    finalPdf.setCreationDate(now);

    const coverDoc = await PDFDocument.load(coverPdfBuffer);
    const [coverPg] = await finalPdf.copyPages(coverDoc, [0]);
    finalPdf.insertPage(0, coverPg);

    const finalBytes = await finalPdf.save();

    // Ensure output directory exists
    const outputDir = path.dirname(outputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    fs.writeFileSync(outputPath, finalBytes);
    const sizeMb = (finalBytes.length / 1024 / 1024).toFixed(2);
    console.log(`  Done! ${totalPages} pages, ${sizeMb} MB`);
  } finally {
    await browser.close();
    highlighter.dispose();
    if (fs.existsSync(tmpHtmlPath)) fs.unlinkSync(tmpHtmlPath);
    if (fs.existsSync(tmpCoverPath)) fs.unlinkSync(tmpCoverPath);
    if (imgTempDir && fs.existsSync(imgTempDir)) fs.rmSync(imgTempDir, { recursive: true, force: true });
  }
}

/**
 * Downscale oversized local raster images referenced by <img> tags so the
 * embedded PDF stays a reasonable size. Resized copies are written to a temp
 * directory under baseDir and the HTML is rewritten to point at them. Returns
 * the (possibly rewritten) HTML and the temp dir to clean up (null if nothing
 * was optimized). Originals are never modified; any per-image failure falls
 * back to the original source so rendering never breaks on a bad asset.
 */
async function optimizeLocalImages(
  html: string,
  baseDir: string
): Promise<{ html: string; tempDir: string | null }> {
  const MAX_WIDTH = 1600;
  const SIZE_THRESHOLD = 350 * 1024;
  const imgSrcRegex = /(<img\b[^>]*?\bsrc=")([^"]+)(")/gi;
  const skip = (src: string): boolean =>
    /^(data:|https?:|file:|\/)/i.test(src) || !/\.(png|jpe?g|webp)$/i.test(src);

  const matches = [...html.matchAll(imgSrcRegex)];
  if (matches.length === 0) return { html, tempDir: null };

  const tempDir = path.join(baseDir, `.md-to-pdf-img.${process.pid}`);
  const tempDirName = path.basename(tempDir);
  const rewrites = new Map<string, string>();
  let createdDir = false;

  for (const match of matches) {
    const src = match[2];
    if (skip(src)) continue;

    let absPath: string;
    try {
      absPath = path.resolve(baseDir, decodeURIComponent(src));
    } catch {
      continue;
    }
    if (rewrites.has(absPath) || !fs.existsSync(absPath)) continue;

    try {
      const stat = fs.statSync(absPath);
      const meta = await sharp(absPath).metadata();
      const width = meta.width ?? 0;
      if (width <= MAX_WIDTH && stat.size <= SIZE_THRESHOLD) continue;

      if (!createdDir) {
        fs.mkdirSync(tempDir, { recursive: true });
        createdDir = true;
      }
      const hash = crypto.createHash("md5").update(absPath).digest("hex").slice(0, 12);
      const resized = sharp(absPath).resize({ width: MAX_WIDTH, withoutEnlargement: true });
      const outName = meta.hasAlpha ? `${hash}.png` : `${hash}.jpg`;
      if (meta.hasAlpha) {
        await resized.png({ compressionLevel: 9, palette: true }).toFile(path.join(tempDir, outName));
      } else {
        await resized.jpeg({ quality: 82, mozjpeg: true }).toFile(path.join(tempDir, outName));
      }
      rewrites.set(absPath, `${tempDirName}/${outName}`);
    } catch {
      // Leave the original src untouched on any optimization failure.
    }
  }

  if (rewrites.size === 0) return { html, tempDir: null };

  const rewritten = html.replace(
    imgSrcRegex,
    (whole: string, pre: string, src: string, post: string): string => {
      if (skip(src)) return whole;
      let absPath: string;
      try {
        absPath = path.resolve(baseDir, decodeURIComponent(src));
      } catch {
        return whole;
      }
      const rel = rewrites.get(absPath);
      return rel ? `${pre}${rel}${post}` : whole;
    }
  );

  return { html: rewritten, tempDir };
}

function createMarkdownIt(highlighter: Highlighter): MarkdownIt {
  const md = new MarkdownIt({
    // Trusted first-party docs use inline HTML (e.g. <a id="..."></a> link
    // anchors); render it instead of escaping it into visible tag text.
    html: true,
    typographer: true,
    linkify: true,
    highlight: (code: string, lang: string): string => {
      const language = lang || "plaintext";
      try {
        const loadedLangs = highlighter.getLoadedLanguages();
        if (loadedLangs.includes(language as never)) {
          const highlighted = highlighter.codeToHtml(code, {
            lang: language,
            theme: CARUCA_THEME_NAME,
          });
          // Add data-language attribute for the CSS label
          return highlighted.replace(
            /^<pre class="shiki/,
            `<pre data-language="${escapeAttr(language)}" class="shiki`
          );
        }
      } catch {
        // Fall through to default
      }
      return "";
    },
  });

  md.use(footnote);
  md.use(taskLists, { enabled: true, label: true });
  md.use(anchor, { permalink: false });

  // Custom container for callout boxes.
  //
  // The title defaults to the callout type, and an author can override it by
  // naming one on the fence: `::: warning Open question`. Callout titles are
  // brand micro-labels, so the stylesheet uppercases and tracks them out —
  // author copy stays in sentence case at the source.
  const defaultCalloutTitles: Record<string, string> = {
    info: "Info",
    warning: "Warning",
    tip: "Tip",
    danger: "Danger",
  };

  for (const type of ["info", "warning", "tip", "danger"]) {
    md.use(container, type, {
      render(tokens: MarkdownIt.Token[], idx: number): string {
        if (tokens[idx].nesting === 1) {
          const custom = tokens[idx].info.trim().slice(type.length).trim();
          const title = custom || defaultCalloutTitles[type];
          return `<div class="callout callout-${type}"><div class="callout-title">${escapeHtml(
            title
          )}</div>\n`;
        }
        return "</div>\n";
      },
    });
  }

  return md;
}

/**
 * Keep each heading on the same page as the block that follows it.
 *
 * Chromium honors `break-after: avoid` unreliably, so the heading and its next
 * sibling are wrapped in a `break-inside: avoid` group instead.
 *
 * This was a regex over the serialized HTML, which could not match balanced
 * tags: `<div>...</div>` and `<ul>...</ul>` were matched non-greedily, so a
 * callout following a heading was cut at the end of its own title div, and a
 * list containing a nested list was cut at the end of the nested one. In both
 * cases the tail of the element was left outside the group and rendered as
 * loose body text — a callout that spilled its contents, a list that dropped
 * its last item. Parsing the document makes the boundary exact.
 */
function wrapHeadingGroups(html: string): string {
  const dom = new JSDOM(html);
  const doc = dom.window.document;

  for (const heading of Array.from(doc.querySelectorAll("h1, h2, h3, h4, h5, h6"))) {
    const next = heading.nextElementSibling;
    if (!next) continue;

    // Back-to-back headings have nothing to be kept with.
    if (/^H[1-6]$/.test(next.tagName)) continue;

    // A block that is explicitly allowed to break across pages must not be
    // trapped inside a group that forbids it.
    if (next.classList.contains("long-code")) continue;
    if (next.classList.contains("footnotes")) continue;

    const group = doc.createElement("div");
    group.className = "heading-group";
    heading.parentNode?.insertBefore(group, heading);
    group.appendChild(heading);
    group.appendChild(next);
  }

  return doc.body.innerHTML;
}

/**
 * Mark code blocks with >40 lines as "long-code" so they can break across pages.
 */
function markLongCodeBlocks(html: string): string {
  return html.replace(/<pre([^>]*)>([\s\S]*?)<\/pre>/gi, (match, attrs, content) => {
    const lineCount = (content.match(/\n/g) || []).length;
    if (lineCount > 40) {
      // Add long-code class
      if (attrs.includes("class=")) {
        return match.replace(/class="/, 'class="long-code ');
      }
      return `<pre class="long-code"${attrs}>${content}</pre>`;
    }
    return match;
  });
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function escapeAttr(str: string): string {
  return str.replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/**
 * Strip a leading YAML frontmatter block (a `---` fenced header at the very top
 * of the file). Without this, markdown-it renders the frontmatter as a spurious
 * setext heading and pulls the metadata into both the table of contents and the
 * body. Only a block at the start of the document is removed; a later `---`
 * horizontal rule is left untouched.
 */
function stripFrontmatter(markdown: string): string {
  const withoutBom = markdown.replace(/^﻿/, "");
  const match = withoutBom.match(/^---[ \t]*\r?\n[\s\S]*?\r?\n---[ \t]*(?:\r?\n|$)/);
  return match ? withoutBom.slice(match[0].length).replace(/^\s*\r?\n/, "") : withoutBom;
}

/**
 * Normalize the manual link anchors some docs use for internal cross-references
 * (e.g. `<a id="section"></a>` before `## Section`).
 *
 * 1. When an empty anchor sits immediately before a heading, fold its id onto
 *    the heading itself (replacing the slug id from markdown-it-anchor with the
 *    id the links actually target). This makes the link destination the heading,
 *    so a link lands on the heading rather than at the bottom of the previous
 *    page, just before a break.
 * 2. Unwrap any remaining empty anchor paragraphs (`<p><a id="x"></a></p>`) so
 *    they resolve as zero-height destinations instead of blank lines.
 */
function normalizeAnchors(html: string): string {
  const hoisted = html.replace(
    /(?:<p>\s*)?<a\s+id="([^"]+)">\s*<\/a>(?:\s*<\/p>)?\s*<h([1-6])((?:\s[^>]*)?)>/gi,
    (_match, id: string, level: string, attrs: string): string => {
      const withoutId = attrs.replace(/\s+id="[^"]*"/i, "");
      return `<h${level}${withoutId} id="${id}">`;
    }
  );
  return hoisted.replace(/<p>\s*(<a\s+id="[^"]+">\s*<\/a>)\s*<\/p>/gi, "$1");
}

import type MarkdownIt from "markdown-it";
import { TOKENS } from "./tokens";

type Token = MarkdownIt.Token;
type RenderRule = MarkdownIt.Renderer.RenderRule;

/**
 * Markdown code-fence languages that describe a diagram, mapped to the Kroki
 * diagram type used to render them. Mirrors the diagram-type table in the
 * `diagram` skill (.claude/skills/diagram/SKILL.md).
 */
const DIAGRAM_TYPES: Record<string, string> = {
  mermaid: "mermaid",
  plantuml: "plantuml",
  puml: "plantuml",
  uml: "plantuml",
  c4plantuml: "c4plantuml",
  graphviz: "graphviz",
  dot: "graphviz",
  d2: "d2",
  erd: "erd",
  dbml: "dbml",
  nwdiag: "nwdiag",
  blockdiag: "blockdiag",
  seqdiag: "seqdiag",
  actdiag: "actdiag",
  ditaa: "ditaa",
};

/**
 * Diagram types Kroki only renders as SVG (no PNG endpoint). We render
 * everything as SVG anyway for vector quality, so this is informational.
 */
const KROKI_BASE_URL = (process.env.KROKI_URL ?? "https://kroki.io").replace(/\/+$/, "");

interface DiagramBlock {
  key: string;
  krokiType: string;
  code: string;
}

/** Normalize a fence info string to its diagram language token. */
function diagramLang(info: string): string | null {
  const lang = info.trim().split(/\s+/)[0]?.toLowerCase() ?? "";
  return lang in DIAGRAM_TYPES ? lang : null;
}

/** Stable key shared between collection and the render-time fence rule. */
function makeKey(lang: string, content: string): string {
  return `${lang} ${content}`;
}

/** Find every diagram code fence in the parsed markdown token stream. */
function collectDiagramBlocks(md: MarkdownIt, markdown: string): DiagramBlock[] {
  const tokens = md.parse(markdown, {});
  const blocks = new Map<string, DiagramBlock>();

  for (const token of tokens) {
    if (token.type !== "fence") continue;
    const lang = diagramLang(token.info);
    if (!lang) continue;

    const key = makeKey(lang, token.content);
    if (!blocks.has(key)) {
      blocks.set(key, { key, krokiType: DIAGRAM_TYPES[lang], code: token.content });
    }
  }

  return Array.from(blocks.values());
}

/**
 * Mermaid theme variables, in the brand's palette.
 *
 * Diagrams are this identity's primary imagery ("diagrams over photos", "cool,
 * technical, monochrome-plus-blue"), but mermaid's stock theme paints nodes in
 * pastel yellow and lavender, which belongs to no part of this system. These
 * variables restate the palette: pale blue node fills with blue borders, ink
 * text, quiet gray edges, and the document's own surface grays for clusters.
 *
 * `fontFamily` is deliberately left as Arial and must stay that way — see
 * preprocessCode below. Kroki measures label boxes server-side with Liberation
 * Sans, which is metric-compatible with Arial; naming Lexend Deca here would
 * make every label overflow the box that was measured for it.
 */
export const MERMAID_THEME_VARIABLES = {
  fontFamily: "arial, helvetica, sans-serif",
  background: TOKENS.color.surfacePage,

  primaryColor: TOKENS.color.surfaceInfo,
  primaryBorderColor: TOKENS.color.blue,
  primaryTextColor: TOKENS.color.ink,

  secondaryColor: TOKENS.color.surfaceCode,
  secondaryBorderColor: TOKENS.color.borderStrong,
  secondaryTextColor: TOKENS.color.ink,

  tertiaryColor: TOKENS.color.surfaceThead,
  tertiaryBorderColor: TOKENS.color.borderDefault,
  tertiaryTextColor: TOKENS.color.ink,

  mainBkg: TOKENS.color.surfaceInfo,
  nodeBorder: TOKENS.color.blue,
  nodeTextColor: TOKENS.color.ink,
  textColor: TOKENS.color.ink,
  titleColor: TOKENS.color.ink,

  lineColor: TOKENS.color.gray600,
  edgeLabelBackground: TOKENS.color.surfacePage,

  clusterBkg: TOKENS.color.surfaceZebra,
  clusterBorder: TOKENS.color.borderDefault,

  noteBkgColor: TOKENS.color.warningBg,
  noteBorderColor: TOKENS.color.warning,
  noteTextColor: TOKENS.color.ink,
};


/**
 * Per-engine tweaks to the diagram source before sending to Kroki.
 *
 * Mermaid defaults to rendering labels as HTML inside `<foreignObject>` with a
 * box width measured using Kroki's server-side fonts. When the PDF renderer
 * re-lays that text with different fonts it overflows and gets clipped. Forcing
 * `htmlLabels: false` makes mermaid emit native SVG `<text>`, which scales as
 * vector and is never clipped to a fixed-width box. We only inject this when the
 * author hasn't supplied their own `%%{init}%%` directive.
 */
function preprocessCode(krokiType: string, code: string): string {
  if (krokiType === "mermaid" && !/%%\{\s*init\s*:/.test(code)) {
    // - htmlLabels:false  -> native SVG <text>, never clipped to a fixed box.
    // - fontFamily Arial  -> Kroki's Linux maps Arial to Liberation Sans, which
    //   is metric-compatible with the renderer's Arial, so box widths line up.
    // - extra padding      -> a little slack so labels never kiss the box edge.
    const init =
      '%%{init: {"flowchart": {"htmlLabels": false, "padding": 12}, ' +
      `"themeVariables": ${JSON.stringify(MERMAID_THEME_VARIABLES)}} }%%`;
    return `${init}\n${code}`;
  }
  return code;
}

/** POST a diagram script to Kroki and return the rendered SVG markup. */
async function renderDiagramSvg(krokiType: string, code: string): Promise<string> {
  const body = preprocessCode(krokiType, code);
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30_000);

  try {
    const response = await fetch(`${KROKI_BASE_URL}/${krokiType}/svg`, {
      method: "POST",
      headers: { "Content-Type": "text/plain" },
      body,
      signal: controller.signal,
    });

    const text = await response.text();
    if (!response.ok) {
      throw new Error(`Kroki ${response.status}: ${text.slice(0, 300)}`);
    }
    return text;
  } finally {
    clearTimeout(timeout);
  }
}

/**
 * Make a Kroki SVG scale to the page: guarantee a `viewBox`, drop fixed
 * width/height/style on the root <svg>, and let the print CSS size it.
 */
function normalizeSvg(svg: string): string {
  const openTag = svg.match(/<svg\b[^>]*>/i)?.[0];
  if (!openTag) return svg;

  const widthAttr = openTag.match(/\swidth\s*=\s*"([^"]*)"/i)?.[1];
  const heightAttr = openTag.match(/\sheight\s*=\s*"([^"]*)"/i)?.[1];
  const hasViewBox = /\sviewBox\s*=\s*"/i.test(openTag);

  let next = openTag
    .replace(/\swidth\s*=\s*"[^"]*"/i, "")
    .replace(/\sheight\s*=\s*"[^"]*"/i, "")
    .replace(/\sstyle\s*=\s*"[^"]*"/i, "");

  if (!hasViewBox && widthAttr && heightAttr) {
    const w = parseFloat(widthAttr);
    const h = parseFloat(heightAttr);
    if (Number.isFinite(w) && Number.isFinite(h) && w > 0 && h > 0) {
      next = next.replace(/<svg\b/i, `<svg viewBox="0 0 ${w} ${h}"`);
    }
  }

  // Inline style guarantees responsive sizing even though print CSS also covers it.
  next = next.replace(/<svg\b/i, `<svg style="max-width:100%;height:auto;"`);

  return svg.replace(openTag, next);
}

/** Wrap rendered SVG in a centered, page-break-safe figure. */
function buildDiagramHtml(svg: string): string {
  return `<figure class="diagram">${normalizeSvg(svg)}</figure>`;
}

/**
 * Render every diagram code fence in the markdown to inline SVG (via Kroki),
 * returning a map keyed for the fence renderer. Diagrams that fail to render
 * are simply omitted, so they fall back to a normal highlighted code block.
 */
export async function prepareDiagrams(
  md: MarkdownIt,
  markdown: string
): Promise<Map<string, string>> {
  const blocks = collectDiagramBlocks(md, markdown);
  const rendered = new Map<string, string>();
  if (blocks.length === 0) return rendered;

  console.log(`  Rendering ${blocks.length} diagram${blocks.length === 1 ? "" : "s"} via Kroki...`);

  const results = await Promise.all(
    blocks.map(async (block) => {
      try {
        const svg = await renderDiagramSvg(block.krokiType, block.code);
        return { key: block.key, html: buildDiagramHtml(svg) };
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        console.warn(`  Warning: failed to render ${block.krokiType} diagram (${message}); keeping source block.`);
        return null;
      }
    })
  );

  for (const result of results) {
    if (result) rendered.set(result.key, result.html);
  }

  return rendered;
}

/**
 * Override markdown-it's fence renderer so diagram code blocks emit their
 * rendered image. Non-diagram fences fall through to the original renderer
 * (Shiki syntax highlighting).
 */
export function installDiagramRenderer(md: MarkdownIt, rendered: Map<string, string>): void {
  const fallback: RenderRule = (tokens, idx, options, env, self) =>
    self.renderToken(tokens, idx, options);
  const defaultFence = md.renderer.rules.fence ?? fallback;

  md.renderer.rules.fence = (tokens: Token[], idx, options, env, self): string => {
    const token = tokens[idx];
    const lang = diagramLang(token.info);
    if (lang) {
      const html = rendered.get(makeKey(lang, token.content));
      if (html) return `${html}\n`;
    }
    return defaultFence(tokens, idx, options, env, self);
  };
}

import { JSDOM } from "jsdom";

interface TocEntry {
  level: number;
  text: string;
  id: string;
}

/**
 * Parse HTML, extract headings, assign IDs, and generate a TOC HTML block.
 * Returns the modified HTML (with heading IDs) and the TOC HTML.
 */
export function generateToc(html: string): { tocHtml: string; bodyHtml: string } {
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  const headings = doc.querySelectorAll("h1, h2, h3");
  const entries: TocEntry[] = [];

  headings.forEach((heading, index) => {
    const level = parseInt(heading.tagName[1]);
    const text = heading.textContent || "";
    const id = heading.id || slugify(text, index);
    heading.id = id;
    entries.push({ level, text, id });
  });

  if (entries.length === 0) {
    return { tocHtml: "", bodyHtml: html };
  }

  const tocItems = entries
    .map(
      (e) =>
        `<li class="toc-item toc-level-${e.level}">
          <a href="#${e.id}">${e.text}</a>
        </li>`
    )
    .join("\n");

  const tocHtml = `
    <div class="toc-page">
      <h2 class="toc-title">Table of contents</h2>
      <ul class="toc-list">
        ${tocItems}
      </ul>
    </div>
  `;

  // Serialize the body back (just the innerHTML since we're injecting into a template)
  const bodyHtml = doc.body.innerHTML;

  return { tocHtml, bodyHtml };
}

function slugify(text: string, index: number): string {
  const slug = text
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .trim();
  return slug || `heading-${index}`;
}

export const tocStyles = `
  .toc-page {
    break-after: page;
    page-break-after: always;
    padding: 0;
  }

  /* Matches the page-title treatment: ink, with the brand accent bar beneath. */
  .toc-title {
    font-size: var(--text-h2);
    font-weight: 700;
    color: var(--ink);
    letter-spacing: var(--tracking-heading);
    margin: 0 0 1.4em 0;
    padding-bottom: 0.45em;
    border-bottom: none;
    position: relative;
  }

  .toc-title::after {
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

  .toc-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .toc-item {
    padding: 0.35em 0;
    border-bottom: var(--border-w) solid var(--border-default);
    font-size: var(--text-body-size);
  }

  .toc-item a {
    text-decoration: none;
    color: var(--ink);
  }

  .toc-level-1 {
    font-weight: 700;
    font-size: var(--text-h4);
    padding-top: 0.5em;
  }

  .toc-level-2 {
    padding-left: 0;
    font-weight: 600;
  }

  /*
    Third level is the quiet tier. It was set in #4A4A6A, a violet-gray that
    appears nowhere in the palette; it now uses the palette's secondary text.
  */
  .toc-level-3 {
    padding-left: 1.5em;
    font-size: var(--text-small);
    font-weight: 400;
  }

  .toc-level-3 a {
    color: var(--text-secondary);
  }
`;

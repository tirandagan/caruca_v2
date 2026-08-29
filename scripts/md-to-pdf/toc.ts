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
      <h2 class="toc-title">Table of Contents</h2>
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

  .toc-title {
    font-size: 20pt;
    font-weight: 700;
    color: #2563EB;
    margin-bottom: 1.5em;
    border-bottom: none;
  }

  .toc-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .toc-item {
    padding: 0.35em 0;
    border-bottom: 1px dotted #D0D7DE;
    font-size: 11pt;
  }

  .toc-item a {
    text-decoration: none;
    color: #0B1F33;
  }

  .toc-item a:hover {
    color: #2563EB;
  }

  .toc-level-1 {
    font-weight: 700;
    font-size: 12pt;
    padding-top: 0.5em;
  }

  .toc-level-2 {
    padding-left: 0;
    font-weight: 600;
  }

  .toc-level-3 {
    padding-left: 1.5em;
    font-size: 10pt;
    color: #4A4A6A;
  }

  .toc-level-3 a {
    color: #4A4A6A;
  }
`;

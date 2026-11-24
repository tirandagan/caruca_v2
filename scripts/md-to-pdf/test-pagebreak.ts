import assert from "assert";
import { execFileSync } from "child_process";
import fs from "fs";
import os from "os";
import path from "path";
import { convertMarkdownToPdf } from "./converter";

function getPageCount(pdfPath: string): number {
  const out = execFileSync("pdfinfo", [pdfPath], { encoding: "utf-8" });
  const match = out.match(/^Pages:\s+(\d+)/m);
  assert(match, `Could not parse page count from pdfinfo:\n${out}`);
  return Number(match[1]);
}

function getPageFirstContentLine(pdfPath: string, pageNum: number): string {
  const out = execFileSync(
    "pdftotext",
    ["-layout", "-f", String(pageNum), "-l", String(pageNum), pdfPath, "-"],
    { encoding: "utf-8" }
  );
  // Strip running header/footer lines if pdftotext extracts them, then return the first body line.
  const lines = out
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l.length > 0 && !l.startsWith("Caruca v2") && !/^Page \d+ of \d+$/.test(l));
  return lines[0] ?? "";
}

async function main(): Promise<void> {
  const fixturePath = path.join(__dirname, "test-pagebreak.md");
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "md-to-pdf-pagebreak-"));
  const outPdf = path.join(tmpDir, "test-pagebreak.pdf");

  try {
    await convertMarkdownToPdf({ inputPath: fixturePath, outputPath: outPdf });

    // Page 1: cover, Page 2: TOC, Pages 3-6: 4 body pages separated by 3 markers.
    const pages = getPageCount(outPdf);
    assert.strictEqual(pages, 6, `Expected 6 pages (cover + TOC + 4 body), got ${pages}`);

    const expectations: Array<[number, string]> = [
      [3, "Page-break test"],
      [4, "Section Two"],
      [5, "Second part of section two, separated mid-section by a page break."],
      [6, "Section Three"],
    ];

    for (const [pageNum, expectedStart] of expectations) {
      const firstLine = getPageFirstContentLine(outPdf, pageNum);
      assert.strictEqual(
        firstLine,
        expectedStart,
        `Page ${pageNum}: expected first line ${JSON.stringify(expectedStart)}, got ${JSON.stringify(firstLine)}`
      );
    }

    const fullText = execFileSync("pdftotext", ["-layout", outPdf, "-"], { encoding: "utf-8" });
    for (const marker of ["<!-- pagebreak -->", "\\pagebreak", "\\newpage"]) {
      assert(!fullText.includes(marker), `Marker ${marker} leaked into PDF text`);
    }

    console.log("PASS: page-break test (6 pages, all 3 markers start expected pages, no visible marker text)");
  } finally {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

main().catch((err) => {
  console.error("FAIL:", err);
  process.exit(1);
});

import path from "path";
import fs from "fs";
import { convertMarkdownToPdf } from "./md-to-pdf/converter";

interface ParsedArgs {
  positional: string[];
  title?: string;
  subtitle?: string;
}

function parseArgs(argv: string[]): ParsedArgs {
  const positional: string[] = [];
  let title: string | undefined;
  let subtitle: string | undefined;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--title" || arg === "--subtitle") {
      const value = argv[i + 1];
      if (value === undefined) {
        console.error(`Error: ${arg} requires a value`);
        process.exit(1);
      }
      if (arg === "--title") title = value;
      else subtitle = value;
      i++;
    } else if (arg.startsWith("--title=")) {
      title = arg.slice("--title=".length);
    } else if (arg.startsWith("--subtitle=")) {
      subtitle = arg.slice("--subtitle=".length);
    } else {
      positional.push(arg);
    }
  }

  return { positional, title, subtitle };
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    console.log(`
Usage: npm run convert -- <input.md> [output.pdf] [--title "Title"] [--subtitle "Subtitle"]

Arguments:
  input.md      Path to the markdown file to convert (required)
  output.pdf    Output PDF path (optional, defaults to <input-dir>/<filename>.pdf)
  --title       Cover page title (optional, defaults to the first H1 or filename)
  --subtitle    Cover page subtitle (optional, omitted if not provided)

Examples:
  npm run convert -- ai_docs/prep/roadmap.md
  npm run convert -- docs/report.md output/report-final.pdf
  npm run convert -- docs/report.md --title "Q3 Report" --subtitle "Engineering Review"
`);
    process.exit(args.length === 0 ? 1 : 0);
  }

  const { positional, title, subtitle } = parseArgs(args);
  const inputPath = positional[0];

  if (!inputPath) {
    console.error("Error: input.md is required");
    process.exit(1);
  }

  // Validate input file
  if (!fs.existsSync(inputPath)) {
    console.error(`Error: File not found: ${inputPath}`);
    process.exit(1);
  }

  if (!inputPath.endsWith(".md")) {
    console.error(`Error: Input file must be a .md file: ${inputPath}`);
    process.exit(1);
  }

  // Determine output path — defaults to the same folder as the source file
  const outputPath = positional[1]
    ? positional[1]
    : path.join(path.dirname(inputPath), path.basename(inputPath, ".md") + ".pdf");

  console.log(`\nConverting: ${inputPath}`);
  console.log(`Output:     ${outputPath}\n`);

  try {
    await convertMarkdownToPdf({ inputPath, outputPath, title, subtitle });
    console.log(`\nSuccess: ${outputPath}`);
  } catch (error) {
    console.error("\nConversion failed:", error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();

/**
 * Reading campaigns: `eval/campaigns/<id>/ledger.jsonl` and `summary.json`.
 *
 * A campaign is a grid of cells - command x model x temperature x sample - each scored once.
 * The ledger has one row per cell; the summary has the campaign's totals.
 *
 * **These are the one part of the run data that is not committed** (`eval/campaigns/` is still
 * in `.gitignore`, everything else under `eval/` was committed at `eedd91a`). So this reader
 * must behave properly on a checkout where the directory does not exist, and the tests that
 * exercise it build small synthetic ledgers rather than depending on local files that a fresh
 * clone will not have.
 */
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import {
  campaignSummarySchema,
  ledgerRowSchema,
  type CampaignSummary,
  type LedgerRow,
} from "./schema.js";
import { repoPaths } from "./paths.js";

export class CampaignUnreadableError extends Error {}

export interface LoadedLedger {
  readonly rows: LedgerRow[];
  /**
   * Lines that did not parse, by line number.
   *
   * A ledger is append-only and written a row at a time, so a campaign stopped mid-write can
   * leave a truncated final line. That is worth reporting and worth tolerating; it is not
   * worth discarding the 200 rows before it.
   */
  readonly badLines: { line: number; reason: string }[];
}

export function loadLedger(path: string): LoadedLedger {
  let text: string;
  try {
    text = readFileSync(path, "utf8");
  } catch (cause) {
    throw new CampaignUnreadableError(`Could not read ${path}: ${(cause as Error).message}`);
  }

  const rows: LedgerRow[] = [];
  const badLines: { line: number; reason: string }[] = [];

  text.split("\n").forEach((line, index) => {
    const trimmed = line.trim();
    if (!trimmed) return;
    let json: unknown;
    try {
      json = JSON.parse(trimmed);
    } catch (cause) {
      badLines.push({ line: index + 1, reason: (cause as Error).message });
      return;
    }
    const parsed = ledgerRowSchema.safeParse(json);
    if (!parsed.success) {
      badLines.push({
        line: index + 1,
        reason: parsed.error.issues
          .map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`)
          .join("; "),
      });
      return;
    }
    rows.push(parsed.data);
  });

  return { rows, badLines };
}

export function loadSummary(path: string): CampaignSummary {
  let json: unknown;
  try {
    json = JSON.parse(readFileSync(path, "utf8"));
  } catch (cause) {
    throw new CampaignUnreadableError(`Could not read ${path}: ${(cause as Error).message}`);
  }
  const parsed = campaignSummarySchema.safeParse(json);
  if (!parsed.success) {
    throw new CampaignUnreadableError(
      `${path} does not match the summary shape: ${parsed.error.issues
        .map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`)
        .join("; ")}`,
    );
  }
  return parsed.data;
}

export interface LoadedCampaign {
  readonly id: string;
  readonly dir: string;
  readonly ledger: LoadedLedger;
  /** Absent for a campaign that was stopped before it wrote one. */
  readonly summary: CampaignSummary | null;
  /**
   * A `ledger.jsonl.before-rescore` sitting beside the ledger, if one exists.
   *
   * `report --rescore` keeps the previous ledger under this name. The Compare screen's rescore
   * view shows old and new values side by side, and this is where the old ones come from.
   */
  readonly beforeRescorePath: string | null;
}

export function loadCampaign(dir: string): LoadedCampaign {
  const ledgerPath = join(dir, "ledger.jsonl");
  if (!existsSync(ledgerPath)) {
    throw new CampaignUnreadableError(`No ledger.jsonl in ${dir}`);
  }
  const summaryPath = join(dir, "summary.json");
  const beforeRescore = `${ledgerPath}.before-rescore`;
  return {
    id: dir.split("/").filter(Boolean).at(-1) ?? dir,
    dir,
    ledger: loadLedger(ledgerPath),
    summary: existsSync(summaryPath) ? loadSummary(summaryPath) : null,
    beforeRescorePath: existsSync(beforeRescore) ? beforeRescore : null,
  };
}

/** Campaign ids present on this machine. Empty on a checkout that has never run one. */
export function listCampaigns(campaignsRoot = repoPaths().campaigns): string[] {
  try {
    return readdirSync(campaignsRoot)
      .filter((name) => {
        try {
          return (
            statSync(join(campaignsRoot, name)).isDirectory() &&
            existsSync(join(campaignsRoot, name, "ledger.jsonl"))
          );
        } catch {
          return false;
        }
      })
      .sort();
  } catch {
    return [];
  }
}

/**
 * Group a ledger's rows into cells that differ only by sample.
 *
 * This is what a consistency figure is computed over: the repeated runs of one configuration.
 * The key deliberately excludes `sample`, and includes `prompt_variant` because task 009 makes
 * the variant an arm rather than a constant.
 */
export function groupBySample(rows: LedgerRow[]): Map<string, LedgerRow[]> {
  const groups = new Map<string, LedgerRow[]>();
  for (const row of rows) {
    const key = [row.stage, row.command, row.model, row.temperature, row.prompt_variant].join("|");
    const existing = groups.get(key);
    if (existing) existing.push(row);
    else groups.set(key, [row]);
  }
  for (const group of groups.values()) group.sort((a, b) => a.sample - b.sample);
  return groups;
}

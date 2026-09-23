/**
 * The parity campaigns, loaded together.
 *
 * `eval/campaigns/` is the one part of the run data that is not committed, so every caller has
 * to cope with it being absent. This is the single place that knows which campaigns make up a
 * comparison and what to say when they are not on this machine.
 */
import { join } from "node:path";
import { loadLedger, listCampaigns } from "./campaigns.js";
import type { LedgerRow } from "./schema.js";
import { repoPaths } from "./paths.js";

/** The nine-command parity study: one campaign per stage. */
export const PARITY_CAMPAIGNS = [
  "p1_syntax_spec",
  "p1_generate",
  "p1_trace",
  "p1_annotate",
] as const;

/** The C0 pilot: the same four stages, at a smaller scale. */
export const PILOT_CAMPAIGNS = [
  "c0_syntax_spec",
  "c0_generate",
  "c0_trace",
  "c0_annotate",
] as const;

export interface LoadedCampaignSet {
  readonly rows: LedgerRow[];
  readonly loaded: string[];
  readonly absent: string[];
  /** Ledger lines that would not parse, by campaign. There should be none. */
  readonly badLines: { campaign: string; line: number; reason: string }[];
}

export function loadCampaignSet(
  ids: readonly string[],
  root = repoPaths().campaigns,
): LoadedCampaignSet {
  const available = new Set(listCampaigns(root));
  const rows: LedgerRow[] = [];
  const loaded: string[] = [];
  const absent: string[] = [];
  const badLines: { campaign: string; line: number; reason: string }[] = [];

  for (const id of ids) {
    if (!available.has(id)) {
      absent.push(id);
      continue;
    }
    const ledger = loadLedger(join(root, id, "ledger.jsonl"));
    rows.push(...ledger.rows);
    loaded.push(id);
    for (const bad of ledger.badLines) badLines.push({ campaign: id, ...bad });
  }

  return { rows, loaded, absent, badLines };
}

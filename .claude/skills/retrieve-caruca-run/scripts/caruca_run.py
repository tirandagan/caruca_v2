#!/usr/bin/env python3
# ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove
# caruca_v2 agent skill: Retrieve caruca run.
# Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0
# Noncommercial use only. Commercial use is prohibited.
# ATTRIBUTION-NOTICE:END
"""Retrieve one command's pipeline record: any stage, any view, in one call.

    caruca_run.py                      what exists at all
    caruca_run.py cat                  all four stages, headline figures
    caruca_run.py cat --stage 2        stage 2 in full
    caruca_run.py cat -s 2 -v items    the invocation strings behind the number
    caruca_run.py cat -s 2 -v prompt   the prompt as actually sent to the model

Views are additive: `-v numbers -v items` prints both.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import carucadata as cd

VIEWS = ("summary", "numbers", "items", "prompt", "response", "runs", "v1", "outputs")


# --------------------------------------------------------------------------------------
# Inventory (no command given)
# --------------------------------------------------------------------------------------


def print_inventory(rec: cd.Record) -> None:
    print(cd.rule("what is on this machine"))
    print(f"repo         {rec.paths.root}")
    try:
        print(f"v1 checkout  {cd.v1_root()}")
    except cd.RepoNotFound as e:
        print(f"v1 checkout  UNAVAILABLE — {e}")
    print()

    grid: dict[str, dict[str, int]] = {}
    for r in rec.runs:
        grid.setdefault(r.command, {}).setdefault(r.stage, 0)
        grid[r.command][r.stage] += 1

    diffs = set(cd.available_parity_diffs())
    hdr = f"{'command':12}" + "".join(f"{cd.STAGE_NUMBER[s]:>10}" for s in cd.STAGES)
    print(hdr + "   parity diff")
    print(cd.rule())
    for cmd in sorted(grid):
        row = f"{cmd:12}" + "".join(f"{grid[cmd].get(s, 0):>10}" for s in cd.STAGES)
        print(row + ("   yes" if cmd in diffs else "   no"))
    print(cd.rule())
    print("(counts are run directories with a manifest, per stage 1-4)")
    print()

    print(f"campaigns present: {', '.join(rec.campaigns_present) or 'none'}")
    if rec.campaigns_absent:
        print(f"campaigns absent:  {', '.join(rec.campaigns_absent)}")
        print("  eval/campaigns/ is gitignored, so absence means 'not on this machine',")
        print("  not 'scored nothing'. Scores for those stages cannot be read.")
    print()
    print(f"run directories:   {len(rec.runs)} with a manifest, "
          f"{len(rec.empty_run_dirs)} empty (died before writing one)"
          + (f", {len(rec.malformed_run_dirs)} malformed" if rec.malformed_run_dirs else ""))
    print()
    print("Next: caruca_run.py <command>            all four stages")
    print("      caruca_run.py <command> --stage 2  one stage in full")


# --------------------------------------------------------------------------------------
# Views
# --------------------------------------------------------------------------------------


def view_summary(rec: cd.Record, command: str, stages: list[str], family: str | None) -> None:
    totals = [cd.summarize_stage(rec, command, st, family) for st in stages]

    print(cd.rule(f"{command} — headline figures"))
    print(f"{'stage':<15}{'figure':>14}  {'verdict':<12}{'scored':>7}  {'campaign':<16}headline")
    print(cd.rule())
    for s in totals:
        val = cd.fmt(s.value)
        if s.pooled:
            val = f"{val} ({s.pooled[0]:.0f}/{s.pooled[1]:.0f})"
        camp = ", ".join(s.campaigns) or "—"
        print(f"{cd.STAGE_SHORT[s.stage]:<15}{val:>14}  {s.verdict:<12}"
              f"{s.scored_samples}/{s.samples:<5}  {camp:<16}{s.headline.label}")
    print(cd.rule())

    print("Each figure is counted over:")
    for s in totals:
        print(f"  {cd.STAGE_NUMBER[s.stage]}. {s.headline.label:<36} {s.headline.denominator}")
        print(f"     method {s.headline.method}")

    # Say out loud which experiment these numbers came from. `cat` and `wc` sit in two
    # campaigns, and a figure that silently pooled them would be a mean over two designs.
    others = sorted({f for s in totals for f in s.other_families})
    if others:
        print()
        names = dict(cd.CAMPAIGN_FAMILIES)
        print(f"NOTE: also scored under {', '.join(f'{f} ({names.get(f, f)})' for f in others)}, "
              f"not pooled here.")
        print(f"      Add --campaign {others[0]} to see that one instead, or --campaign all "
              f"to pool them deliberately.")

    orphans = sum(len(s.orphan_run_ids) for s in totals)
    if orphans:
        print(f"NOTE: {orphans} run(s) on disk at these stages are cited by no ledger cell, "
              f"so they are")
        print(f"      excluded from the figures above. See --view runs.")

    cost = sum(t.cost_usd for t in totals)
    if cost or any(t.prompt_tokens for t in totals):
        print()
        print(f"cost of the scored runs: ${cost:.4f}  "
              f"tokens {sum(t.prompt_tokens for t in totals):,} in / "
              f"{sum(t.completion_tokens for t in totals):,} out  "
              f"wall clock {sum(t.wall_clock_seconds for t in totals):.1f}s")

    unscore = [(t.stage, r) for t in totals for r in t.unscoreable_reasons]
    if unscore:
        print()
        print("unscoreable cells — the comparison never ran (NOT a zero):")
        for st, reason in unscore:
            print(f"  {st}: {reason}")

    undef = [(t.stage, s_, d) for t in totals for s_, d in t.scored_but_undefined]
    if undef:
        print()
        print("cells that WERE scored but whose headline is undefined (also not a zero,")
        print("and not the same as unscoreable — the comparison ran and found nothing):")
        for st, sample, detail in undef:
            print(f"  {st} sample {sample}: {detail}")

    print()
    print("Next: -v numbers (full scorer breakdown)  -v items (the actual items)")
    print("      -v prompt (what the model was told)  -v v1 (what it was compared against)")


def view_numbers(rec: cd.Record, command: str, stages: list[str], family: str | None) -> None:
    for st in stages:
        s = cd.summarize_stage(rec, command, st, family)
        print()
        print(cd.rule(f"{command} · {cd.STAGE_TITLE[st]} · numbers"))
        print(f"headline   {s.headline.label} = {cd.fmt(s.value)}  ({s.verdict})")
        print(f"method     {s.headline.method}")
        print(f"counted over  {s.headline.denominator}")
        print(f"samples    {s.scored_samples} scored of {s.samples}"
              + (f"   per-sample: {', '.join(cd.fmt(v) for v in s.per_sample)}" if s.per_sample else ""))
        if s.spread is not None:
            print(f"spread     {cd.fmt(s.spread)}  (max - min across samples)")
        if s.campaigns:
            print(f"campaigns  {', '.join(s.campaigns)}"
                  + (f"   (also in: {', '.join(s.other_families)}, not pooled)"
                     if s.other_families else ""))
        if s.run_ids:
            print(f"runs       {', '.join(s.run_ids)}")
        if s.orphan_run_ids:
            print(f"uncited    {len(s.orphan_run_ids)} run(s) on disk that no ledger cell "
                  f"references, excluded from the figure:")
            for rid in s.orphan_run_ids:
                print(f"             {rid}")

        if s.unscoreable_reasons:
            print(f"unscored   {len(s.unscoreable_reasons)} cell(s), comparison never ran: "
                  + "; ".join(sorted(set(s.unscoreable_reasons))))
        if s.scored_but_undefined:
            print(f"undefined  {len(s.scored_but_undefined)} cell(s) scored but headline "
                  f"undefined — a result, not a gap:")
            for sample, detail in s.scored_but_undefined:
                print(f"             sample {sample}: {detail}")

        if s.counts:
            print()
            print("scorer's count breakdown:")
            for k, v in s.counts.items():
                print(f"  {k:<28}{v}")

        # `counts.*` are already printed above as the scorer's own breakdown; repeating them
        # here as three-decimal means turns integers into something that reads like a rate.
        rates = {k: v for k, v in s.all_metrics.items() if not k.startswith("counts.")}
        if rates:
            print()
            width = max(38, max(len(k) for k in rates) + 2)
            print(f"{'every metric':<{width}}{'mean':>8}{'min':>8}{'max':>8}{'spread':>8}")
            for k in sorted(rates):
                vals = rates[k]
                mean = sum(vals) / len(vals)
                sp = max(vals) - min(vals)
                mark = "  <- headline" if k == s.headline.metric else ""
                print(f"{k:<{width}}{mean:>8.3f}{min(vals):>8.3f}{max(vals):>8.3f}{sp:>8.3f}{mark}")
            movers = [k for k, v in rates.items()
                      if len(v) > 1 and (max(v) - min(v)) > (s.spread or 0)]
            if movers:
                print()
                print("moved more than the headline did (this is dimension 4, consistency):")
                for k in sorted(movers):
                    v = rates[k]
                    print(f"  {k}  spread {max(v) - min(v):.3f}")

        # The per-run `checks` block holds things the ledger's score does not: parse health,
        # the bounds the run was given, the tool audit. Surface the shape so the caller knows
        # what to ask for next rather than having to open the manifest to find out.
        runs = [r for r in rec.for_command(command, st) if r.ok]
        if runs and runs[0].checks:
            print()
            print(f"per-run `checks` keys (see --view runs, or read the manifest): "
                  f"{', '.join(sorted(runs[0].checks))}")


def _stage2_bounds(rec: cd.Record, command: str) -> dict[str, Any] | None:
    for r in rec.for_command(command, "generate"):
        b = (r.checks.get("invocation_comparison") or {}).get("bounds")
        if b:
            return b
    return None


def view_items(rec: cd.Record, command: str, stages: list[str], full: bool) -> None:
    """The actual items behind the numbers, from the generated drill-down."""
    sections = cd.parity_diff_sections(command)
    if not sections:
        print()
        print(f"No parity diff for {command!r}. Available: "
              f"{', '.join(cd.available_parity_diffs()) or 'none'}")
        print("The drill-down is generated by scripts/parity_diff.py; only the nine")
        print("parity-study commands have one. Numbers are still available via --view numbers.")
        return

    print()
    print(f"[source: {cd.parity_diff_path(command)}]")
    print("This quotes v1's own source and output verbatim. v1 is private and unlicensed:")
    print("read it, do not copy it anywhere public.")
    limit = 100_000 if full else 6_000
    for st in stages:
        body = sections.get(st)
        print()
        if not body:
            print(cd.rule(f"{cd.STAGE_TITLE[st]} — not in the drill-down"))
            continue
        print(cd.truncate(body, limit, "rerun with --full for all of it"))

    if "generate" in stages:
        b = _stage2_bounds(rec, command)
        if b:
            print()
            print(f"stage 2 bounds this run was given: {json.dumps(b)}")
            print("Note what `max_count` means in v1's code vs. its help text before")
            print("calling any surplus invocation a model error — run v1_probe.py --explain-bounds.")


def view_prompt(rec: cd.Record, command: str, stages: list[str], full: bool) -> None:
    """The prompt as actually sent.

    Not the template in `prompts/`. Those are templates; the manifest records the rendered
    text, and the difference is where an instruction the model actually received lives.
    A surplus output is often the prompt's wording, not the model's judgement.
    """
    limit = 100_000 if full else 4_000
    for st in stages:
        runs = [r for r in rec.for_command(command, st) if r.ok] or rec.for_command(command, st)
        print()
        print(cd.rule(f"{command} · {cd.STAGE_TITLE[st]} · prompt as sent"))
        if not runs:
            print("no run recorded for this stage")
            continue
        r = runs[0]
        print(f"run {r.run_id}   model {r.manifest.get('model_requested')}   "
              f"temp {(r.manifest.get('decoding_params') or {}).get('temperature')}   "
              f"seed {r.manifest.get('seed')}")
        print(f"prompt_hash {r.manifest.get('prompt_hash')}")
        print(f"template files {', '.join(r.manifest.get('prompt_files') or [])}")
        print(f"inputs {json.dumps(r.inputs, default=str)[:600]}")
        if st == "trace":
            print("(stage 3 runs one session per configuration; this is the stage prompt, "
                  "and per-session prompt hashes are in checks.sessions)")
        print()
        print("--- system ---")
        print(cd.truncate(r.manifest.get("prompt_system") or "(none)", limit))
        print()
        print("--- user ---")
        print(cd.truncate(r.manifest.get("prompt_user") or "(none)", limit))


def view_response(rec: cd.Record, command: str, stages: list[str], full: bool) -> None:
    limit = 100_000 if full else 4_000
    for st in stages:
        runs = [r for r in rec.for_command(command, st) if r.ok] or rec.for_command(command, st)
        print()
        print(cd.rule(f"{command} · {cd.STAGE_TITLE[st]} · raw response"))
        if not runs:
            print("no run recorded for this stage")
            continue
        r = runs[0]
        print(f"run {r.run_id}   finish_reason {r.manifest.get('finish_reason')}   "
              f"turns {r.manifest.get('turns')}   truncated {r.manifest.get('output_truncated')}")
        print()
        print(cd.truncate(r.manifest.get("raw_response") or "(none)", limit))


def view_runs(rec: cd.Record, command: str, stages: list[str], family: str | None) -> None:
    for st in stages:
        runs = rec.for_command(command, st)
        print()
        print(cd.rule(f"{command} · {cd.STAGE_TITLE[st]} · runs"))
        if not runs:
            print("none recorded")
            continue
        print(f"{'run_id':<36}{'status':<9}{'cost':>9}{'in':>9}{'out':>8}{'secs':>8}  sample")
        for r in runs:
            cell = rec.cell_for_run(r.run_id) or {}
            print(f"{r.run_id:<36}{r.status:<9}"
                  f"{float(r.manifest.get('cost_usd') or 0):>9.4f}"
                  f"{int(r.manifest.get('prompt_tokens') or 0):>9,}"
                  f"{int(r.manifest.get('completion_tokens') or 0):>8,}"
                  f"{float(r.manifest.get('wall_clock_seconds') or 0):>8.1f}"
                  f"  {cell.get('campaign_id', '-')}#{cell.get('sample', '-')}")
            if r.manifest.get("failure_reason"):
                print(f"    failure: {r.manifest['failure_reason']}")
        r0 = runs[0]
        if r0.checks:
            print()
            print(f"checks on {r0.run_id}:")
            print(cd.truncate(json.dumps(r0.checks, indent=1, default=str), 4000,
                              "read the manifest directly for the rest"))


def view_outputs(rec: cd.Record, command: str, stages: list[str], full: bool) -> None:
    limit = 100_000 if full else 3_000
    for st in stages:
        print()
        print(cd.rule(f"{command} · {cd.STAGE_TITLE[st]} · output artifacts"))
        runs = [r for r in rec.for_command(command, st) if r.ok]
        if not runs:
            print("none recorded")
            continue
        for p in runs[0].outputs():
            print()
            print(f"--- {p} ({p.stat().st_size:,} bytes) ---")
            try:
                print(cd.truncate(p.read_text(), limit, "read the file directly for the rest"))
            except UnicodeDecodeError:
                print("(binary)")


def view_v1(rec: cd.Record, command: str, stages: list[str]) -> None:
    """What the comparison is against, on v1's side."""
    print()
    print(cd.rule(f"{command} — v1's side of the comparison"))
    try:
        root = cd.v1_root()
        print(f"v1 checkout  {root}")
    except cd.RepoNotFound as e:
        print(f"v1 checkout  UNAVAILABLE — {e}")
        root = None
    for st in stages:
        runs = [r for r in rec.for_command(command, st) if r.ok]
        inputs = runs[0].inputs if runs else {}
        mods = inputs.get("replaces_v1_modules") or cd.STAGE_V1_MODULES.get(st, [])
        print()
        print(f"{cd.STAGE_TITLE[st]}")
        print(f"  replaces in v1   {', '.join(mods)}")
        for key in ("spec_source", "docs_source", "configs_source", "traces_source"):
            if inputs.get(key):
                print(f"  {key:<16} {inputs[key]}")
        if inputs.get("caruca_v1_commit"):
            print(f"  v1 commit        {inputs['caruca_v1_commit']}")
        cells = rec.cells(command, st)
        refs = sorted({(c.get("score") or {}).get("reference") for c in cells
                       if (c.get("score") or {}).get("reference")})
        if refs:
            print(f"  scored against   {', '.join(refs)}")
    cfg = rec.paths.v1_configs / f"{command}.configs.json"
    if cfg.exists():
        print()
        print(f"v1's own configuration expansion: {cfg}")
    print()
    print("To read v1's implementation or re-run its enumeration: v1_probe.py")


# --------------------------------------------------------------------------------------
# JSON mode
# --------------------------------------------------------------------------------------


def as_json(rec: cd.Record, command: str, stages: list[str], family: str | None) -> dict[str, Any]:
    out: dict[str, Any] = {"command": command, "repo": str(rec.paths.root), "stages": {}}
    for st in stages:
        s = cd.summarize_stage(rec, command, st, family)
        out["stages"][st] = {
            "stage_number": cd.STAGE_NUMBER[st],
            "headline": {
                "metric": s.headline.metric,
                "label": s.headline.label,
                "denominator": s.headline.denominator,
                "method": s.headline.method,
            },
            "value": s.value,
            "verdict": s.verdict,
            "samples": s.samples,
            "scored_samples": s.scored_samples,
            "per_sample": s.per_sample,
            "spread": s.spread,
            "pooled": list(s.pooled) if s.pooled else None,
            "counts": s.counts,
            "all_metrics": {k: v for k, v in sorted(s.all_metrics.items())},
            "run_ids": s.run_ids,
            "campaigns": s.campaigns,
            "campaign_family": s.family,
            "other_families_not_pooled": s.other_families,
            "orphan_run_ids": s.orphan_run_ids,
            "unscoreable_reasons": s.unscoreable_reasons,
            "scored_but_undefined": [{"sample": a, "detail": b}
                                     for a, b in s.scored_but_undefined],
            "cost_usd": s.cost_usd,
            "prompt_tokens": s.prompt_tokens,
            "completion_tokens": s.completion_tokens,
            "wall_clock_seconds": s.wall_clock_seconds,
        }
    return out


# --------------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("command", nargs="?", help="a unix command, e.g. cat. Omit for an inventory.")
    ap.add_argument("-s", "--stage", action="append", default=None,
                    help="1-4, or syntax_spec|generate|trace|annotate. Repeatable. Default: all.")
    ap.add_argument("-v", "--view", action="append", default=None,
                    choices=VIEWS, help=f"repeatable; default summary. one of: {', '.join(VIEWS)}")
    ap.add_argument("-c", "--campaign", default="auto",
                    help="which campaign family the figures come from: auto (default, most "
                         "authoritative present), p1 (nine-command parity study), c0 (pilot), "
                         "or all (pool them, which mixes two experiment designs).")
    ap.add_argument("--full", action="store_true", help="do not truncate long blocks")
    ap.add_argument("--json", action="store_true", help="machine-readable figures only")
    args = ap.parse_args(argv)

    try:
        rec = cd.load_record()
    except cd.RepoNotFound as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not args.command:
        print_inventory(rec)
        return 0

    command = args.command
    if command not in rec.commands:
        print(f"error: no runs recorded for {command!r}.", file=sys.stderr)
        print(f"recorded commands: {', '.join(rec.commands)}", file=sys.stderr)
        print("run caruca_run.py with no arguments for the full inventory.", file=sys.stderr)
        return 1

    try:
        stages = [cd.resolve_stage(s) for s in args.stage] if args.stage else list(cd.STAGES)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    stages = [s for s in cd.STAGES if s in set(stages)]  # canonical order, deduplicated

    family: str | None = None if args.campaign == "all" else args.campaign

    if args.json:
        print(json.dumps(as_json(rec, command, stages, family), indent=1, default=str))
        return 0

    views = args.view or ["summary"]
    for v in views:
        if v == "summary":
            view_summary(rec, command, stages, family)
        elif v == "numbers":
            view_numbers(rec, command, stages, family)
        elif v == "items":
            view_items(rec, command, stages, args.full)
        elif v == "prompt":
            view_prompt(rec, command, stages, args.full)
        elif v == "response":
            view_response(rec, command, stages, args.full)
        elif v == "runs":
            view_runs(rec, command, stages, family)
        elif v == "outputs":
            view_outputs(rec, command, stages, args.full)
        elif v == "v1":
            view_v1(rec, command, stages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

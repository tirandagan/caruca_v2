"""`caruca-v2` — argparse only.

Every subcommand is a thin wrapper over one typed function in `stages/`, so anything the
CLI can do, an agent or the evaluation harness can do by calling the function directly.
No logic beyond argument parsing, presentation, and the exit code lives here.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from . import llm, metrics_db, tools, v1
from . import ui as ui_module
from .errors import CarucaV2Error
from .harness import score as score_module
from .harness import sweep as sweep_module
from .stages import annotate as annotate_stage
from .stages import generate as generate_stage
from .stages import syntax_spec
from .stages import trace as trace_stage
from .ui import compose

EXIT_OK = 0
EXIT_RUN_FAILED = 1
EXIT_SETUP_ERROR = 3

LOG_CONVERSATION_VAR = "CARUCA_V2_LOG_CONVERSATION"


def _log_conversation_default() -> bool:
    return os.environ.get(LOG_CONVERSATION_VAR, "").strip() in {"1", "true", "yes"}


def _add_shared_flags(parser: argparse.ArgumentParser) -> None:
    """Flags whose meaning is identical across every stage."""
    parser.add_argument(
        "--model",
        required=True,
        help="OpenRouter model ID, recorded verbatim in telemetry (e.g. openai/gpt-4o). "
        "Required until the configuration-selection phase freezes a default.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        required=True,
        help="Decoding temperature, recorded in decoding_params. Required until frozen.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=llm.DEFAULT_SEED,
        help="Passed through to the provider (default: %(default)s, v1's value). Providers "
        "that ignore it are flagged seed_honored=false in the manifest.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=llm.DEFAULT_MAX_TOKENS,
        help="Completion token cap (default: %(default)s, v1's value).",
    )
    parser.add_argument(
        "--provider",
        default=None,
        help="Pin OpenRouter routing to one upstream provider, disabling fallbacks. "
        "openai/gpt-4o is pinned to OpenAI automatically for comparability with the paper.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=metrics_db.DEFAULT_RUNS_ROOT,
        help="Run-directory root (default: %(default)s).",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=metrics_db.DEFAULT_DB_PATH,
        help="Metrics database (default: %(default)s).",
    )
    parser.add_argument(
        "--log-conversation",
        action="store_true",
        default=_log_conversation_default(),
        help=f"Write conversation.jsonl into the run directory (also {LOG_CONVERSATION_VAR}=1).",
    )
    parser.add_argument(
        "--plain",
        action="store_true",
        help="Line-oriented output with no color or animation (automatic when not a TTY).",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="caruca-v2",
        description="LLM replication of caruca v1's specification-mining pipeline.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    naive = subparsers.add_parser(
        "naive-llm",
        help="Stage 1 (naive control): a command's documentation in, a v1-DSL syntax "
        "specification out, via exactly one few-shot prompt.",
    )
    naive.add_argument(
        "command",
        nargs="+",
        help="The command to specify. Multi-word commands are written as `git commit`.",
    )
    naive.add_argument(
        "--docs",
        type=Path,
        default=None,
        help="Documentation file to use instead of v1's committed man page for the command.",
    )
    _add_shared_flags(naive)
    naive.set_defaults(handler=_run_naive_llm)

    generate = subparsers.add_parser(
        "generate",
        help="Stage 2: a syntax specification in, the concrete invocations it allows and "
        "the environment each needs out.",
    )
    generate.add_argument("command", nargs="+", help="The command to enumerate invocations for.")
    generate.add_argument(
        "--spec",
        type=Path,
        default=None,
        help="Syntax specification to enumerate. Defaults to v1's committed spec for the "
        "command; point it at a `naive-llm` run's output to chain the two stages.",
    )
    generate.add_argument(
        "--max-arity",
        type=int,
        default=generate_stage.V1_DEFAULT_MAX_ARITY,
        help="How many times a repeatable argument may appear (default: %(default)s, v1's "
        "own CLI default). Stated in the prompt and used for the v1 comparison run.",
    )
    generate.add_argument(
        "--max-count",
        type=int,
        default=generate_stage.V1_DEFAULT_MAX_COUNT,
        help="Most optional flags combined in one invocation (default: %(default)s, v1's default).",
    )
    generate.add_argument(
        "--stdin",
        choices=["simple", "varied", "split"],
        default=generate_stage.V1_DEFAULT_STDIN,
        help="Standard-input variation, mirroring v1's knob (default: %(default)s).",
    )
    generate.add_argument(
        "--content",
        choices=["simple", "varied", "split"],
        default=generate_stage.V1_DEFAULT_CONTENT,
        help="File-content variation, mirroring v1's knob (default: %(default)s).",
    )
    generate.add_argument(
        "--skip",
        nargs="?",
        default=generate_stage.V1_DEFAULT_SKIP,
        const=generate_stage.V1_SKIP_CONST,
        help="Comma-separated flags to exclude, mirroring v1's knob exactly: given bare it "
        f"means \"{generate_stage.V1_SKIP_CONST}\", and omitted it skips nothing. Use "
        "--skip=--foo,--bar for values starting with a dash. Passed to v1's own "
        "enumeration for the comparison as well.",
    )
    generate.add_argument(
        "--max-turns",
        type=int,
        default=generate_stage.DEFAULT_MAX_TURNS,
        help="Cap on continuation turns when a response is cut off by the token limit "
        "(default: %(default)s). A model that stops on its own is never asked for more.",
    )
    generate.add_argument(
        "--no-compare",
        action="store_true",
        help="Skip running v1's own `generate` for the set-diff. Enumeration can be slow "
        "on wide-interface commands; skipping is recorded in the manifest.",
    )
    generate.add_argument(
        "--compare-timeout",
        type=int,
        default=300,
        help="Seconds to allow v1's own enumeration before recording it as unavailable "
        "(default: %(default)s).",
    )
    _add_shared_flags(generate)
    generate.set_defaults(handler=_run_generate)

    trace = subparsers.add_parser(
        "trace",
        help="Stage 3: run each configuration in a prepared workspace and record what "
        "the command did, as a v1-compatible traces file.",
    )
    trace.add_argument("command", nargs="+", help="The command to trace.")
    trace.add_argument(
        "--configs",
        type=Path,
        default=None,
        help="Configurations to trace. Defaults to the most recent `generate` output for "
        "the command under --out.",
    )
    trace.add_argument(
        "--limit",
        type=int,
        default=trace_stage.DEFAULT_LIMIT,
        help="Trace only the first N configurations (default: %(default)s). This is the "
        "cost brake: one agent session runs per configuration.",
    )
    trace.add_argument(
        "--max-turns",
        type=int,
        default=trace_stage.DEFAULT_MAX_TURNS,
        help="Cap on model turns per configuration (default: %(default)s).",
    )
    trace.add_argument(
        "--isolation",
        choices=["host", "lima"],
        default="host",
        help="Where the command runs. `host` is this machine and refuses destructive "
        "commands outright; `lima` runs them inside the caruca VM (default: %(default)s).",
    )
    trace.add_argument(
        "--lima-instance",
        default="caruca",
        help="Lima instance name for --isolation lima (default: %(default)s).",
    )
    trace.add_argument(
        "--keep-workspace",
        action="store_true",
        help="Leave each configuration's temporary working directory in place for debugging.",
    )
    _add_shared_flags(trace)
    trace.set_defaults(handler=_run_trace)

    annotate = subparsers.add_parser(
        "annotate",
        help="Stage 4: traces in, one consumer's annotation out. Mirrors v1's own "
        "`caruca annotate FORMAT CMD`.",
    )
    annotate.add_argument(
        "format",
        choices=list(v1.ANNOTATION_FORMATS),
        help="Which consumer's annotation format to produce.",
    )
    annotate.add_argument("command", nargs="+", help="The command to annotate.")
    annotate.add_argument(
        "--traces",
        type=Path,
        default=None,
        help="Traces to annotate. Defaults to v1's own committed traces for the command, "
        "which makes the A/B-on-identical-input comparison the default behavior; point it "
        "at a `trace` run's output to chain the pipeline.",
    )
    annotate.add_argument(
        "--max-turns",
        type=int,
        default=annotate_stage.DEFAULT_MAX_TURNS,
        help="Cap on continuation turns when a response is cut off (default: %(default)s).",
    )
    annotate.add_argument(
        "--no-compare",
        action="store_true",
        help="Skip the diffs against v1's own annotator and the hand-curated ground truth.",
    )
    annotate.add_argument(
        "--v1-runner",
        choices=["host", "lima"],
        default="host",
        help="Where v1's own annotator runs for the comparison. On macOS use `lima`: v1's "
        "annotator resolves paths against a hardcoded /tmp prefix, which macOS rewrites to "
        "/private/tmp, so it cannot run on the host at all (default: %(default)s).",
    )
    annotate.add_argument(
        "--lima-instance",
        default="caruca",
        help="Lima instance name for --v1-runner lima (default: %(default)s).",
    )
    _add_shared_flags(annotate)
    annotate.set_defaults(handler=_run_annotate)

    metrics = subparsers.add_parser("metrics", help="Operate on the metrics database.")
    metrics_sub = metrics.add_subparsers(dest="metrics_action", required=True)
    rebuild = metrics_sub.add_parser(
        "rebuild",
        help="Regenerate the metrics database from the telemetry sidecars on disk.",
    )
    rebuild.add_argument("--out", type=Path, default=metrics_db.DEFAULT_RUNS_ROOT)
    rebuild.add_argument("--db", type=Path, default=metrics_db.DEFAULT_DB_PATH)
    rebuild.add_argument("--plain", action="store_true")
    rebuild.set_defaults(handler=_run_metrics_rebuild)

    score = subparsers.add_parser(
        "score",
        help="Harness: argument-by-argument comparison of a generated syntax spec "
        "against v1's committed spec or the hand-annotated ground truth. No model call.",
    )
    score.add_argument(
        "command", nargs="*",
        help="The command the spec describes. Omit with --self-test.",
    )
    score.add_argument("--spec", type=Path, default=None, help="Generated spec file to score.")
    score.add_argument(
        "--reference",
        choices=score_module.REFERENCES,
        default=score_module.REFERENCE_V1_SPECS,
        help="What to score against (default: %(default)s — the primary population per E0).",
    )
    score.add_argument(
        "--reference-path", type=Path, default=None,
        help="Explicit reference spec file (overrides --reference; used by mutation arms).",
    )
    score.add_argument(
        "--transform", type=Path, default=None,
        help="Rename map (JSON) applied to the reference, for renamed-documentation arms.",
    )
    score.add_argument(
        "--cmp-specs", action="store_true",
        help="Also run v1's own eval/cmp_specs.py (the paper's Q2 instrument) and report "
        "its number alongside, denominator caveat attached.",
    )
    score.add_argument(
        "--self-test", action="store_true",
        help="Score each committed exemplar spec against itself; every cell must be perfect.",
    )
    score.add_argument("--json", action="store_true", help="Print the full record as JSON.")
    score.add_argument("--plain", action="store_true")
    score.set_defaults(handler=_run_score)

    sweep = subparsers.add_parser(
        "sweep",
        help="Harness: run one or more campaign files — (commands × models × "
        "temperatures × samples) over a stage, with ledger resume, budget brakes, "
        "the configuration freeze gate, and a per-model comparison rollup.",
    )
    sweep.add_argument("campaigns", nargs="+", type=Path, help="Campaign JSON file(s).")
    sweep.add_argument(
        "--dry-run", action="store_true",
        help="Enumerate and print the cells without making any model call.",
    )
    sweep.add_argument(
        "--frozen-config", type=Path, default=sweep_module.DEFAULT_FROZEN_CONFIG_PATH,
        help="Frozen-configuration record the post-freeze gate checks (default: %(default)s).",
    )
    sweep.add_argument(
        "--ledger-root", type=Path, default=sweep_module.DEFAULT_LEDGER_ROOT,
        help="Where campaign ledgers and summaries live (default: %(default)s).",
    )
    sweep.add_argument("--out", type=Path, default=metrics_db.DEFAULT_RUNS_ROOT)
    sweep.add_argument("--db", type=Path, default=metrics_db.DEFAULT_DB_PATH)
    sweep.add_argument("--plain", action="store_true")
    sweep.set_defaults(handler=_run_sweep)

    return parser


def _run_naive_llm(args: argparse.Namespace, ui: ui_module.UI) -> int:
    command = " ".join(args.command)

    with ui.working(f"asking {args.model} for a syntax specification for {command}"):
        result = syntax_spec.run(
            command,
            model=args.model,
            temperature=args.temperature,
            seed=args.seed,
            max_tokens=args.max_tokens,
            docs_path=args.docs,
            out_root=args.out,
            db_path=args.db,
            log_conversation=args.log_conversation,
            provider=args.provider,
        )

    record = result.record
    validation = result.validation

    if validation is None:
        spec_line = compose("not written (model returned no specification)")
    elif not validation.available:
        spec_line = compose(f"{result.spec_path.name} — not validated ({validation.error})")
    else:
        elements = "" if validation.elements is None else f", {validation.elements} elements"
        spec_line = compose(
            f"{result.spec_path.name}{elements} — ",
            ui.verdict(validation.passed, "validated", "rejected by v1"),
        )

    rows = [
        ("run", str(result.run_dir)),
        ("spec", spec_line),
        ("tokens", ui_module.tokens(record.prompt_tokens, record.completion_tokens)),
        ("cost", ui_module.money(record.cost_usd)),
        ("time", ui_module.duration(record.wall_clock_seconds)),
        ("model", f"{record.model_id} (requested {result.manifest.model_requested})"),
        ("seed", f"{record.seed}" + ("" if result.manifest.seed_honored else " (not honored)")),
        ("metrics", f"row appended to {args.db}"),
    ]
    ui.summary(f"naive-llm {command}", rows)

    if result.manifest.output_truncated:
        ui.warn(
            f"the response hit the {record.decoding_params.max_tokens}-token cap and was "
            "truncated. This is v1's own limit; it is recorded, not raised."
        )
    if result.manifest.failure_reason:
        ui.error(result.manifest.failure_reason)

    return EXIT_OK if result.succeeded else EXIT_RUN_FAILED


def _run_generate(args: argparse.Namespace, ui: ui_module.UI) -> int:
    command = " ".join(args.command)

    with ui.working(f"asking {args.model} to enumerate invocations for {command}"):
        result = generate_stage.run(
            command,
            model=args.model,
            temperature=args.temperature,
            seed=args.seed,
            max_tokens=args.max_tokens,
            max_turns=args.max_turns,
            spec_path=args.spec,
            max_arity=args.max_arity,
            max_count=args.max_count,
            stdin_variation=args.stdin,
            content_variation=args.content,
            skip_flags=args.skip,
            compare=not args.no_compare,
            compare_timeout=args.compare_timeout,
            out_root=args.out,
            db_path=args.db,
            log_conversation=args.log_conversation,
            provider=args.provider,
        )

    manifest = result.manifest
    parse = manifest.checks["parse"]
    comparison = manifest.checks["invocation_comparison"]
    validation = result.validation

    if validation is None:
        configs_line = compose("not written (no usable output)")
    elif not validation.available:
        configs_line = compose(
            f"{validation.elements} entries — not validated ({validation.error})"
        )
    else:
        configs_line = compose(
            f"{validation.elements} entries — ",
            ui.verdict(validation.passed, "validated", "rejected by v1"),
        )

    if comparison.get("available"):
        against_v1 = (
            f"{comparison['matched']} matched, {comparison['missing']} missing, "
            f"{comparison['spurious']} spurious (v1 produced {comparison['v1_count']})"
        )
    else:
        against_v1 = f"unavailable ({comparison.get('error')})"

    rows = [
        ("run", str(result.run_dir)),
        ("invocations", f"{parse['objects_parsed']} of {parse['lines_returned']} line(s) parsed"),
        ("configs", configs_line),
        ("vs v1", against_v1),
        ("turns", str(manifest.turns)),
        ("tokens", ui_module.tokens(manifest.prompt_tokens, manifest.completion_tokens)),
        ("cost", ui_module.money(manifest.cost_usd)),
        ("time", ui_module.duration(manifest.wall_clock_seconds)),
        ("model", f"{manifest.model_reported} (requested {manifest.model_requested})"),
        ("metrics", f"{manifest.turns} row(s) appended to {args.db}"),
    ]
    ui.summary(f"generate {command}", rows)

    if parse["hit_turn_cap_while_truncated"]:
        ui.warn(
            f"the response was still being cut off at the {manifest.turns}-turn cap, so the "
            "enumeration is incomplete because of the cap rather than the model."
        )
    if parse["unparseable_lines"]:
        ui.warn(f"{parse['unparseable_lines']} line(s) could not be parsed as JSON.")
    if manifest.failure_reason:
        ui.error(manifest.failure_reason)

    return EXIT_OK if result.succeeded else EXIT_RUN_FAILED


def _run_trace(args: argparse.Namespace, ui: ui_module.UI) -> int:
    command = " ".join(args.command)
    isolation = (
        tools.IsolationBackend.lima(args.lima_instance) if args.isolation == "lima" else None
    )

    def report(outcome: trace_stage.ConfigOutcome, total: int) -> None:
        ui.detail(
            f"config {outcome.index + 1}/{total}",
            compose(
                f"{outcome.invocation or '(workspace failed)'} — ",
                ui.verdict(outcome.status == "ok", "ok", outcome.status),
                f" ({len(outcome.responses)} turn(s))",
            ),
        )

    result = trace_stage.run(
        command,
        model=args.model,
        temperature=args.temperature,
        seed=args.seed,
        max_tokens=args.max_tokens,
        max_turns=args.max_turns,
        configs_path=args.configs,
        limit=args.limit,
        isolation=isolation,
        keep_workspace=args.keep_workspace,
        out_root=args.out,
        db_path=args.db,
        log_conversation=args.log_conversation,
        provider=args.provider,
        progress=report,
    )

    manifest = result.manifest
    configs = manifest.checks["configs"]
    validation = result.validation

    if validation is None:
        traces_line = compose("not written (no configuration produced a report)")
    elif not validation.available:
        traces_line = compose(f"not validated ({validation.error})")
    else:
        traces_line = compose(
            f"{validation.elements} trace set(s) — ",
            ui.verdict(validation.passed, "validated", "rejected by v1"),
        )

    rows = [
        ("run", str(result.run_dir)),
        ("configs", f"{configs['reported']} reported of {configs['attempted']} attempted"),
        ("traces", traces_line),
        ("isolation", manifest.inputs["isolation"]),
        ("refused calls", str(manifest.checks["refused_calls"])),
        ("turns", str(manifest.turns)),
        ("tokens", ui_module.tokens(manifest.prompt_tokens, manifest.completion_tokens)),
        ("cost", ui_module.money(manifest.cost_usd)),
        ("time", ui_module.duration(manifest.wall_clock_seconds)),
        ("model", manifest.model_reported),
        ("metrics", f"{manifest.turns} row(s) appended to {args.db}"),
    ]
    ui.summary(f"trace {command}", rows)

    if manifest.checks["refused_calls"]:
        ui.warn(
            f"{manifest.checks['refused_calls']} tool call(s) were refused by the executor; "
            "see checks.tool_audit in the manifest."
        )
    if manifest.failure_reason:
        ui.error(manifest.failure_reason)

    return EXIT_OK if result.succeeded else EXIT_RUN_FAILED


def _run_annotate(args: argparse.Namespace, ui: ui_module.UI) -> int:
    command = " ".join(args.command)

    with ui.working(f"asking {args.model} for a {args.format} annotation for {command}"):
        result = annotate_stage.run(
            command,
            args.format,
            model=args.model,
            temperature=args.temperature,
            seed=args.seed,
            max_tokens=args.max_tokens,
            max_turns=args.max_turns,
            traces_path=args.traces,
            compare=not args.no_compare,
            v1_runner=args.v1_runner,
            lima_instance=args.lima_instance,
            out_root=args.out,
            db_path=args.db,
            log_conversation=args.log_conversation,
            provider=args.provider,
        )

    manifest = result.manifest
    validation = result.validation
    comparisons = manifest.checks["comparisons"]

    if validation is None:
        annotation_line = compose("not written (model returned nothing)")
    elif not validation.available:
        annotation_line = compose(f"not validated ({validation.error})")
    else:
        annotation_line = compose(
            f"{result.annotation_path.name} — ",
            ui.verdict(validation.passed, "well formed", "rejected by v1"),
        )

    def describe(comparison: dict) -> str:
        if not comparison or not comparison.get("available"):
            return f"unavailable ({(comparison or {}).get('error', 'no reference')})"
        if comparison.get("structurally_identical") is True or comparison.get("identical"):
            return "identical"
        return f"{comparison['diff_lines']} differing line(s)"

    rows = [
        ("run", str(result.run_dir)),
        ("annotation", annotation_line),
        ("vs v1", describe(comparisons.get("vs_v1_same_traces"))),
        ("vs ground truth", describe(comparisons.get("vs_ground_truth"))),
        ("traces", manifest.inputs["traces_source"]),
        ("turns", str(manifest.turns)),
        ("tokens", ui_module.tokens(manifest.prompt_tokens, manifest.completion_tokens)),
        ("cost", ui_module.money(manifest.cost_usd)),
        ("time", ui_module.duration(manifest.wall_clock_seconds)),
        ("model", manifest.model_reported),
        ("metrics", f"{manifest.turns} row(s) appended to {args.db}"),
    ]
    ui.summary(f"annotate {args.format} {command}", rows)

    reference = comparisons.get("vs_v1_same_traces") or {}
    if not reference.get("available", True) and reference.get("runner") == "host":
        ui.warn(
            "v1's own annotator could not run here. On macOS pass --v1-runner lima; v1 "
            "resolves paths against a hardcoded /tmp prefix that macOS rewrites."
        )
    if manifest.failure_reason:
        ui.error(manifest.failure_reason)

    return EXIT_OK if result.succeeded else EXIT_RUN_FAILED


def _run_metrics_rebuild(args: argparse.Namespace, ui: ui_module.UI) -> int:
    with ui.working(f"rebuilding {args.db} from {args.out}"):
        report = metrics_db.rebuild(runs_root=args.out, db_path=args.db)

    ui.summary(
        "metrics rebuild",
        [
            ("database", str(args.db)),
            ("run directories", str(report.run_dirs)),
            ("rows", str(report.rows)),
        ],
    )
    for note in report.skipped:
        ui.warn(f"skipped {note}")
    return EXIT_OK


def _fmt_rate(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def _run_score(args: argparse.Namespace, ui: ui_module.UI) -> int:
    import json as json_module

    if args.self_test:
        with ui.working("scoring each exemplar spec against itself"):
            outcome = score_module.self_test()
        rows = [
            (command, "perfect" if result["perfect"] else f"IMPERFECT: {result}")
            for command, result in outcome["commands"].items()
        ]
        ui.summary("score --self-test", rows)
        if not outcome["all_perfect"]:
            ui.error("self-test failed: an exemplar spec did not score perfectly against itself")
        return EXIT_OK if outcome["all_perfect"] else EXIT_RUN_FAILED

    if not args.command or args.spec is None:
        ui.error("score needs a COMMAND and --spec PATH (or --self-test).")
        return EXIT_SETUP_ERROR

    command = " ".join(args.command)
    with ui.working(f"scoring {args.spec} against {args.reference_path or args.reference}"):
        record = score_module.score_spec(
            command,
            args.spec,
            reference=args.reference,
            reference_path=args.reference_path,
            transform_path=args.transform,
            with_cmp_specs=args.cmp_specs,
        )

    if args.json:
        print(json_module.dumps(record, indent=2))
        return EXIT_OK if record.get("scoreable") else EXIT_RUN_FAILED

    if not record.get("scoreable"):
        ui.error(record.get("error") or "spec could not be scored")
        return EXIT_RUN_FAILED

    counts = record["counts"]
    rows = [
        ("reference", record["reference_source"]),
        ("matched", f"{counts['matched']} of {counts['reference_flags']} reference flag(s)"),
        ("missing", str(counts["missing"])),
        ("spurious", str(counts["spurious"])),
        ("exact", _fmt_rate(record.get("exact_argument_rate"))),
        ("f1", _fmt_rate(record.get("f1"))),
    ]
    if record.get("transform"):
        rows.insert(1, ("transform", record["transform"]))
    if "cmp_specs" in record:
        cmp = record["cmp_specs"]
        rows.append(
            ("cmp_specs", f"{cmp['correct_percentage']:.3f} (field-denominator caveat)"
             if cmp.get("available") else f"unavailable ({cmp.get('error')})")
        )
    ui.summary(f"score {command}", rows)
    return EXIT_OK


def _run_sweep(args: argparse.Namespace, ui: ui_module.UI) -> int:
    import json as json_module

    exit_code = EXIT_OK
    for campaign_path in args.campaigns:
        campaign = sweep_module.load_campaign(campaign_path)
        cells = sweep_module.enumerate_cells(campaign)

        if args.dry_run:
            ui.summary(
                f"sweep {campaign.campaign_id} (dry run)",
                [
                    ("stage", campaign.stage),
                    ("cells", str(len(cells))),
                    ("models", ", ".join(campaign.models)),
                    ("brakes", f"max_runs {campaign.max_runs}, max_usd ${campaign.max_usd}"),
                ],
            )
            for cell in cells:
                print(f"  {cell.key}")
            continue

        with ui.working(
            f"campaign {campaign.campaign_id}: {len(cells)} cell(s) over {campaign.stage}"
        ):
            report = sweep_module.run_campaign(
                campaign,
                out_root=args.out,
                db_path=args.db,
                ledger_root=args.ledger_root,
                frozen_path=args.frozen_config,
                progress=None,
            )

        rows = [
            ("cells", f"{report.completed} completed, {report.skipped_resumed} resumed, "
             f"{report.failed_content} failed, {report.errored} errored"),
            ("retries", str(report.transport_retries)),
            ("tokens", ui_module.tokens(report.prompt_tokens, report.completion_tokens)),
            ("cost", ui_module.money(report.cost_usd)),
            ("ledger", str(report.ledger_path)),
        ]
        if report.stopped_reason:
            rows.append(("stopped", report.stopped_reason))
        for model, rollup in sweep_module.summarize_by_model(report).items():
            f1 = rollup["mean_f1"]
            rows.append(
                (model,
                 f"{rollup['ok']}/{rollup['cells']} ok, {rollup['validated']} validated, "
                 f"${rollup['cost_usd']:.4f}"
                 + (f", mean F1 {f1:.3f}" if f1 is not None else "")),
            )
        ui.summary(f"sweep {campaign.campaign_id}", rows)

        summary_path = args.ledger_root / campaign.campaign_id / "summary.json"
        if summary_path.is_file():
            rollup = json_module.loads(summary_path.read_text())["by_model"]
            print(json_module.dumps(rollup, indent=2))

        if report.stopped_reason or report.errored:
            exit_code = EXIT_RUN_FAILED
    return exit_code


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)
    ui = ui_module.UI(plain=args.plain)
    try:
        return int(args.handler(args, ui))
    except CarucaV2Error as exc:
        ui.error(str(exc))
        return EXIT_SETUP_ERROR


if __name__ == "__main__":
    sys.exit(main())

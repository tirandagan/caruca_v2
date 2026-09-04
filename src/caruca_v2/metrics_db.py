"""`eval/metrics.db` — a queryable view over the run directories.

The sidecar and manifest files are the source of truth. This database exists so
cross-run questions ("what did every gpt-4o run of the held-out subset cost?") do not
require walking JSON, and it is rebuildable from those files at any time:
`caruca-v2 metrics rebuild` deletes and regenerates it. It is gitignored and per-machine.

Nothing is ever written here that did not come from a sidecar plus its manifest.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .errors import CarucaV2Error
from .telemetry import (
    MANIFEST_NAME,
    SIDECAR_SUFFIX,
    TelemetryRecord,
    load_manifest,
    load_sidecar,
)

DEFAULT_DB_PATH = Path("eval/metrics.db")
DEFAULT_RUNS_ROOT = Path("eval/runs")

# Keyed on (run_id, turn) rather than run_id alone: the tool-using stages emit one
# telemetry record per model turn, all sharing a run_id.
SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id             TEXT NOT NULL,
    turn               INTEGER NOT NULL DEFAULT 0,
    config_index       INTEGER,
    timestamp          TEXT NOT NULL,
    command            TEXT NOT NULL,
    component          TEXT NOT NULL,
    condition          TEXT NOT NULL,
    stage              TEXT NOT NULL,
    model_id           TEXT NOT NULL,
    prompt_tokens      INTEGER NOT NULL,
    completion_tokens  INTEGER NOT NULL,
    cost_usd           REAL NOT NULL,
    wall_clock_seconds REAL NOT NULL,
    seed               INTEGER,
    decoding_params    TEXT NOT NULL,
    prompt_hash        TEXT NOT NULL,
    validation_passed  INTEGER,
    run_dir            TEXT NOT NULL,
    PRIMARY KEY (run_id, turn)
);
"""


EXPECTED_COLUMNS = (
    "run_id", "turn", "config_index", "timestamp", "command", "component", "condition",
    "stage", "model_id", "prompt_tokens", "completion_tokens", "cost_usd",
    "wall_clock_seconds", "seed", "decoding_params", "prompt_hash", "validation_passed",
    "run_dir",
)


def connect(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)

    # `CREATE TABLE IF NOT EXISTS` will not add a column to a database written by an
    # earlier version, so a stale file would silently accept rows with fields missing.
    # This is a rebuildable cache, so the right answer is to say so and let the caller
    # regenerate it -- never to drop it silently, and never to write partial rows.
    present = {row["name"] for row in connection.execute("PRAGMA table_info(runs)")}
    missing = [column for column in EXPECTED_COLUMNS if column not in present]
    if missing:
        connection.close()
        raise CarucaV2Error(
            f"{db_path} was written by an older schema and is missing {missing}. "
            "It is a rebuildable cache: run `caruca-v2 metrics rebuild` to regenerate it "
            "from the telemetry sidecars."
        )
    return connection


def append_run(
    record: TelemetryRecord,
    *,
    run_dir: Path,
    validation_passed: bool | None,
    db_path: Path = DEFAULT_DB_PATH,
) -> None:
    """Insert one telemetry record's row. Re-running a rebuild replaces, never duplicates."""
    with connect(db_path) as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO runs (
                run_id, turn, config_index, timestamp, command, component, condition,
                stage, model_id, prompt_tokens, completion_tokens, cost_usd,
                wall_clock_seconds, seed, decoding_params, prompt_hash,
                validation_passed, run_dir
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.run_id,
                record.turn,
                record.config_index,
                record.timestamp,
                record.command,
                record.component,
                record.condition,
                record.stage,
                record.model_id,
                record.prompt_tokens,
                record.completion_tokens,
                record.cost_usd,
                record.wall_clock_seconds,
                record.seed,
                json.dumps(record.decoding_params.model_dump()),
                record.prompt_hash,
                None if validation_passed is None else int(validation_passed),
                str(run_dir),
            ),
        )


@dataclass(frozen=True)
class RebuildReport:
    """What a rebuild found, so a surprising row count is visible rather than silent."""

    rows: int
    run_dirs: int
    skipped: list[str]


def rebuild(
    runs_root: Path = DEFAULT_RUNS_ROOT,
    db_path: Path = DEFAULT_DB_PATH,
) -> RebuildReport:
    """Regenerate the database from the sidecar files on disk.

    A run directory without a manifest is skipped and named in the report: it means a run
    died before completing, and inventing a row for it would fabricate a result.
    """
    if db_path.exists():
        db_path.unlink()

    rows = 0
    run_dirs = 0
    skipped: list[str] = []

    for run_dir in sorted(p for p in runs_root.glob("*") if p.is_dir()):
        run_dirs += 1
        sidecars = sorted(run_dir.glob(f"*{SIDECAR_SUFFIX}"))
        manifest_path = run_dir / MANIFEST_NAME

        if not sidecars:
            skipped.append(f"{run_dir.name}: no telemetry sidecar")
            continue
        if not manifest_path.is_file():
            skipped.append(f"{run_dir.name}: no {MANIFEST_NAME}")
            continue

        validation = load_manifest(manifest_path).validation
        validation_passed = None if validation is None else validation.passed

        for sidecar in sidecars:
            append_run(
                load_sidecar(sidecar),
                run_dir=run_dir,
                validation_passed=validation_passed,
                db_path=db_path,
            )
            rows += 1

    return RebuildReport(rows=rows, run_dirs=run_dirs, skipped=skipped)

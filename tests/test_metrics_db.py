"""The metrics database: append, and rebuild-from-sidecars."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from caruca_v2 import metrics_db, telemetry
from caruca_v2.telemetry import RunManifest, ValidationReport
from factories import make_record


def make_manifest(run_id: str, validated: bool) -> RunManifest:
    record = make_record(run_id=run_id)
    return RunManifest(
        run_id=run_id,
        timestamp=record.timestamp,
        command=record.command,
        component=record.component,
        condition=record.condition,
        stage=record.stage,
        status="ok" if validated else "failed",
        model_requested="openai/gpt-4o",
        model_reported="openai/gpt-4o",
        seed=42,
        seed_honored=True,
        decoding_params=record.decoding_params,
        response_format="text",
        prompt_hash=record.prompt_hash,
        prompt_files=["prompts/syntax_spec/system.md"],
        prompt_system="s",
        prompt_user="u",
        raw_response="r",
        validation=ValidationReport(passed=validated, available=True),
        prompt_tokens=record.prompt_tokens,
        completion_tokens=record.completion_tokens,
        cost_usd=record.cost_usd,
        wall_clock_seconds=record.wall_clock_seconds,
    )


def write_run(runs_root: Path, command: str, validated: bool) -> str:
    run_dir = telemetry.create_run_directory(runs_root, command)
    record = make_record(run_id=run_dir.run_id, command=command)
    telemetry.write_sidecar(run_dir, command, record)
    telemetry.write_manifest(run_dir, make_manifest(run_dir.run_id, validated))
    return run_dir.run_id


def test_append_writes_one_queryable_row(tmp_path: Path):
    db_path = tmp_path / "metrics.db"
    metrics_db.append_run(
        make_record(), run_dir=tmp_path / "run", validation_passed=True, db_path=db_path
    )

    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT * FROM runs").fetchall()

    assert len(rows) == 1
    assert rows[0]["command"] == "mkdir"
    assert rows[0]["validation_passed"] == 1
    assert rows[0]["cost_usd"] == 0.0213
    assert '"temperature": 0.0' in rows[0]["decoding_params"]


def test_appending_the_same_record_twice_does_not_duplicate(tmp_path: Path):
    db_path = tmp_path / "metrics.db"
    for _ in range(2):
        metrics_db.append_run(
            make_record(), run_dir=tmp_path / "run", validation_passed=False, db_path=db_path
        )

    with sqlite3.connect(db_path) as connection:
        assert connection.execute("SELECT count(*) FROM runs").fetchone()[0] == 1


def test_rebuild_reproduces_the_database_from_sidecars_alone(tmp_path: Path):
    runs_root = tmp_path / "runs"
    db_path = tmp_path / "metrics.db"
    write_run(runs_root, "mkdir", validated=True)
    write_run(runs_root, "grep", validated=False)

    report = metrics_db.rebuild(runs_root=runs_root, db_path=db_path)

    assert report.rows == 2
    assert report.run_dirs == 2
    assert report.skipped == []

    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = {row["command"]: row for row in connection.execute("SELECT * FROM runs")}

    assert rows["mkdir"]["validation_passed"] == 1
    assert rows["grep"]["validation_passed"] == 0


def test_rebuild_is_idempotent(tmp_path: Path):
    runs_root = tmp_path / "runs"
    db_path = tmp_path / "metrics.db"
    write_run(runs_root, "mkdir", validated=True)

    first = metrics_db.rebuild(runs_root=runs_root, db_path=db_path)
    second = metrics_db.rebuild(runs_root=runs_root, db_path=db_path)

    assert first.rows == second.rows == 1


def test_an_incomplete_run_is_skipped_and_named(tmp_path: Path):
    runs_root = tmp_path / "runs"
    db_path = tmp_path / "metrics.db"
    write_run(runs_root, "mkdir", validated=True)
    # A run that died before writing its manifest must not become a fabricated row.
    orphan = telemetry.create_run_directory(runs_root, "grep")
    telemetry.write_sidecar(orphan, "grep", make_record(run_id=orphan.run_id, command="grep"))

    report = metrics_db.rebuild(runs_root=runs_root, db_path=db_path)

    assert report.rows == 1
    assert len(report.skipped) == 1
    assert "manifest.json" in report.skipped[0]

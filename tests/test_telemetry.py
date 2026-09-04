"""Telemetry records and run directories.

The measurement rule is the thing under test: every field populated, nothing defaulted.
"""

from __future__ import annotations

from pathlib import Path

from caruca_v2 import telemetry
from caruca_v2.telemetry import DecodingParams, TelemetryRecord
from factories import make_record


def test_every_schema_field_survives_a_round_trip(tmp_path: Path):
    run_dir = telemetry.create_run_directory(tmp_path, "mkdir")
    path = telemetry.write_sidecar(run_dir, "mkdir", make_record())

    loaded = telemetry.load_sidecar(path)

    for name in TelemetryRecord.model_fields:
        assert getattr(loaded, name) is not None, f"{name} is null in the sidecar"
    assert loaded.decoding_params.temperature == 0.0
    assert loaded.decoding_params.max_tokens == 4096


def test_decoding_params_accepts_parameters_no_schema_change_anticipated():
    params = DecodingParams(temperature=0.2, max_tokens=4096, top_p=0.9)
    assert params.model_dump()["top_p"] == 0.9


def test_run_directories_do_not_collide_within_the_same_second(tmp_path: Path):
    ids = {telemetry.create_run_directory(tmp_path, "mkdir").run_id for _ in range(20)}
    assert len(ids) == 20


def test_run_directory_name_is_the_run_id(tmp_path: Path):
    run_dir = telemetry.create_run_directory(tmp_path, "git_commit")
    assert run_dir.path.name == run_dir.run_id
    assert "git_commit" in run_dir.run_id
    assert run_dir.path.is_dir()


def test_conversation_log_is_one_json_object_per_message(tmp_path: Path):
    run_dir = telemetry.create_run_directory(tmp_path, "mkdir")
    path = telemetry.append_conversation(
        run_dir,
        [
            {"role": "system", "content": "s"},
            {"role": "user", "content": "u"},
            {"role": "assistant", "content": "a"},
        ],
    )
    lines = path.read_text().strip().splitlines()
    assert len(lines) == 3
    assert '"role": "assistant"' in lines[-1]

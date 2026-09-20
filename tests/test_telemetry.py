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

    # `config_index` is null by design for the stages that run one session per invocation;
    # everything else is a measurement and must be present.
    optional = {"config_index"}
    for name in TelemetryRecord.model_fields:
        if name in optional:
            continue
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


def test_progress_never_lands_on_stdout(capsys):
    """`--json` must emit JSON and nothing else, or its output cannot be piped.

    A progress line printed to stdout ahead of the payload made `report --json` and
    `score --json` unparseable without stripping the first line by hand.
    """
    from caruca_v2 import ui as ui_module

    surface = ui_module.UI(plain=True)
    with surface.working("doing something slow"):
        pass
    captured = capsys.readouterr()
    assert "doing something slow" in captured.err
    assert captured.out == ""

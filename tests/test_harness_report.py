"""Campaign aggregation: arms, spreads, consistency, rescoring, and comparison records."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from caruca_v2.errors import CarucaV2Error
from caruca_v2.harness import report


def cell(**overrides) -> dict:
    row = {
        "cell_key": "mkdir|openai/gpt-4o|0.0|0",
        "command": "mkdir",
        "model": "openai/gpt-4o",
        "temperature": 0.0,
        "prompt_variant": "default",
        "status": "ok",
        "validation_passed": True,
        "cost_usd": 0.01,
        "prompt_tokens": 100,
        "completion_tokens": 10,
        "run_dir": "eval/runs/whatever",
        "score": {"scoreable": True, "f1": 1.0, "exact_argument_rate": 1.0},
    }
    row.update(overrides)
    return row


def write_ledger(tmp_path: Path, rows: list[dict], campaign_id: str = "c") -> Path:
    directory = tmp_path / campaign_id
    directory.mkdir(parents=True)
    (directory / "ledger.jsonl").write_text(
        "".join(json.dumps(row) + "\n" for row in rows)
    )
    return tmp_path


def test_missing_ledger_is_an_error(tmp_path):
    with pytest.raises(CarucaV2Error, match="no ledger at"):
        report.load_ledger("nope", tmp_path)


def test_arms_split_by_model_variant_and_temperature():
    rows = [
        cell(),
        cell(model="anthropic/claude-haiku-4.5"),
        cell(prompt_variant="dspy_style"),
        cell(temperature=0.7),
    ]
    arms = report.aggregate(rows)
    assert len(arms) == 4
    names = {arm.name for arm in arms}
    assert "openai/gpt-4o" in names
    assert "openai/gpt-4o @ dspy_style" in names


def test_first_pass_validity_excludes_errored_cells():
    # Two produced output (one valid), one never reached the model at all.
    arms = report.aggregate(
        [
            cell(validation_passed=True),
            cell(status="failed", validation_passed=False),
            cell(status="error", validation_passed=None),
        ]
    )
    assert arms[0].first_pass_validity() == pytest.approx(0.5)
    assert arms[0].errored == 1


def test_empty_arm_reports_nothing_rather_than_zero():
    arms = report.aggregate([cell(score={"scoreable": False, "error": "bad"})])
    data = arms[0].as_dict()
    assert data["f1"] is None
    assert data["scored_cells"] == 0
    assert data["cost_per_scored_cell"] is None


def test_distribution_summary_reports_spread_and_raw_values():
    dist = report.Distribution([1.0, 0.5, 0.75])
    summary = dist.summary()
    assert summary["n"] == 3
    assert summary["min"] == 0.5 and summary["max"] == 1.0
    assert summary["median"] == 0.75
    assert summary["values"] == [0.5, 0.75, 1.0]
    assert summary["ci95_low"] <= summary["mean"] <= summary["ci95_high"]


def test_single_sample_has_no_interval():
    summary = report.Distribution([1.0]).summary()
    assert summary["ci95_low"] is None and summary["ci95_high"] is None


def test_bootstrap_is_deterministic():
    values = [0.2, 0.9, 0.55, 1.0]
    assert report.bootstrap_interval(values) == report.bootstrap_interval(values)


def test_consistency_measures_spread_across_repeated_samples():
    rows = [
        cell(sample=0, score={"scoreable": True, "f1": 1.0}),
        cell(sample=1, score={"scoreable": True, "f1": 0.5}),
        cell(command="cat", sample=0, score={"scoreable": True, "f1": 1.0}),
        cell(command="cat", sample=1, score={"scoreable": True, "f1": 1.0}),
    ]
    spread = report.consistency(report.aggregate(rows)[0])
    assert spread["commands_sampled_more_than_once"] == 2
    assert spread["identical_across_samples"] == 1
    assert spread["max_spread"] == pytest.approx(0.5)


def test_consistency_is_none_without_repeats():
    assert report.consistency(report.aggregate([cell()])[0]) is None


def test_comparison_records_carry_the_method_and_no_invented_v1_value():
    records = report.comparison_records(report.aggregate([cell()]), "c1")
    assert records[0]["method"] == "q2_syntax_diff"
    assert records[0]["v1_value"] is None
    assert records[0]["percent_change"] is None


def test_rescore_marks_missing_artifacts_unscoreable(fake_v1_root, tmp_path):
    rows = [cell(run_dir=str(tmp_path / "gone"))]
    rescored = report.rescore(rows, "v1-specs")
    assert rescored[0]["score"]["scoreable"] is False
    assert "no output at" in rescored[0]["score"]["error"]


def test_rescore_uses_the_current_scorer_on_saved_output(fake_v1_root, tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "mkdir.py").write_text(
        'mkdir_syntax_spec = [[[("-a",), ("-b",)], [("PATH",)]]]\n'
    )
    # The ledger claims a poor score; the artifact is in fact perfect.
    rows = [cell(run_dir=str(run_dir), score={"scoreable": True, "f1": 0.1})]
    rescored = report.rescore(rows, "v1-specs")
    assert rescored[0]["score"]["f1"] == 1.0


def test_build_reports_where_scores_came_from(fake_v1_root, tmp_path):
    root = write_ledger(tmp_path, [cell()])
    from_ledger = report.build("c", root)
    assert "as recorded" in from_ledger["scores_from"]
    assert from_ledger["cells_recorded"] == 1
    assert "| Arm |" in from_ledger["table"]

    rescored = report.build("c", root, rescore_with="v1-specs")
    assert "rescored" in rescored["scores_from"]


def test_table_renders_a_row_per_arm():
    arms = report.aggregate([cell(), cell(model="anthropic/claude-haiku-4.5")])
    table = report.render_table(arms)
    assert table.count("\n") == 3  # header, separator, two rows
    assert "openai/gpt-4o" in table and "anthropic/claude-haiku-4.5" in table

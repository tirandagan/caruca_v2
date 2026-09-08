"""The campaign runner: cells, ledger resume, brakes, the freeze gate, and retries."""

from __future__ import annotations

import json
from pathlib import Path

import openai
import pytest

from caruca_v2.errors import SetupError
from caruca_v2.harness import sweep
from fakes import FakeClient


def campaign(tmp_path: Path, **overrides) -> sweep.Campaign:
    payload = {
        "campaign_id": "test_campaign",
        "stage": "syntax_spec",
        "commands": ["mkdir"],
        "models": ["openai/gpt-4o"],
        "temperatures": [0.0],
        "samples": 1,
        "max_runs": 100,
        "max_usd": 100.0,
    }
    payload.update(overrides)
    built = sweep.Campaign.model_validate(payload)
    built.validate_shape()
    return built


def run(c: sweep.Campaign, tmp_path: Path, client, **kwargs) -> sweep.CampaignReport:
    return sweep.run_campaign(
        c,
        out_root=tmp_path / "runs",
        db_path=tmp_path / "metrics.db",
        ledger_root=tmp_path / "campaigns",
        frozen_path=tmp_path / "frozen.json",
        client=client,
        sleeper=lambda seconds: None,
        **kwargs,
    )


def ledger_lines(report: sweep.CampaignReport) -> list[dict]:
    return [
        json.loads(line)
        for line in report.ledger_path.read_text().splitlines()
        if line.strip()
    ]


def test_cells_are_model_major(tmp_path):
    c = campaign(
        tmp_path,
        commands=["mkdir", "git commit"],
        models=["openai/gpt-4o", "anthropic/claude-haiku-4.5"],
    )
    cells = sweep.enumerate_cells(c)
    assert [cell.model for cell in cells] == (
        ["openai/gpt-4o"] * 2 + ["anthropic/claude-haiku-4.5"] * 2
    )


def test_dry_run_makes_no_calls(fake_v1_root, tmp_path, valid_spec_response):
    client = FakeClient(valid_spec_response)
    report = run(campaign(tmp_path), tmp_path, client, dry_run=True)
    assert report.dry_run_cells == ["mkdir|openai/gpt-4o|0.0|0"]
    assert client.calls == []


def test_campaign_writes_ledger_scores_and_by_model_rollup(
    fake_v1_root, tmp_path, valid_spec_response
):
    client = FakeClient(valid_spec_response)
    c = campaign(
        tmp_path,
        models=["openai/gpt-4o", "anthropic/claude-haiku-4.5"],
        score_after=True,
    )
    report = run(c, tmp_path, client)

    assert report.completed == 2 and report.failed_content == 0
    assert len(client.calls) == 2
    assert report.cost_usd == pytest.approx(2 * 0.0213)

    lines = ledger_lines(report)
    assert [line["model"] for line in lines] == c.models
    assert all(line["status"] == "ok" for line in lines)
    assert all(line["score"]["f1"] == 1.0 for line in lines)

    rollup = sweep.summarize_by_model(report)
    assert set(rollup) == set(c.models)
    for model in c.models:
        assert rollup[model]["ok"] == 1
        assert rollup[model]["mean_f1"] == 1.0

    summary = json.loads((report.ledger_path.parent / "summary.json").read_text())
    assert set(summary["by_model"]) == set(c.models)


def test_resume_skips_completed_cells(fake_v1_root, tmp_path, valid_spec_response):
    c = campaign(tmp_path)
    first = run(c, tmp_path, FakeClient(valid_spec_response))
    assert first.completed == 1

    second_client = FakeClient(valid_spec_response)
    second = run(c, tmp_path, second_client)
    assert second.completed == 0 and second.skipped_resumed == 1
    assert second_client.calls == []


def test_max_runs_brake(fake_v1_root, tmp_path, valid_spec_response):
    c = campaign(tmp_path, commands=["mkdir", "git commit"], max_runs=1)
    report = run(c, tmp_path, FakeClient(valid_spec_response))
    assert report.completed == 1
    assert "max_runs" in report.stopped_reason


def test_content_failure_is_recorded_never_retried(fake_v1_root, tmp_path):
    # No fence and not valid Python: v1's whole-response fallback makes this the spec,
    # v1 rejects it, and that is the measurement — exactly one call.
    client = FakeClient("this is not a spec at all (")
    report = run(campaign(tmp_path), tmp_path, client)
    assert report.completed == 1 and report.failed_content == 1
    assert len(client.calls) == 1
    line = ledger_lines(report)[0]
    assert line["status"] == "failed" and line["attempts"] == 1


class FlakyClient:
    """Raises a transport error a fixed number of times, then answers normally."""

    def __init__(self, inner: FakeClient, failures: int) -> None:
        self._inner = inner
        self._failures = failures
        self.chat = type("Chat", (), {})()
        self.chat.completions = self

    def create(self, **kwargs):
        if self._failures > 0:
            self._failures -= 1
            raise openai.APIConnectionError(request=None)
        return self._inner.chat.completions.create(**kwargs)

    @property
    def calls(self):
        return self._inner.calls


def test_transport_failure_is_retried_with_backoff(
    fake_v1_root, tmp_path, valid_spec_response
):
    client = FlakyClient(FakeClient(valid_spec_response), failures=2)
    report = run(campaign(tmp_path), tmp_path, client)
    assert report.completed == 1 and report.errored == 0
    assert report.transport_retries == 2
    assert ledger_lines(report)[0]["attempts"] == 3


def test_persistent_transport_failure_errors_the_cell(fake_v1_root, tmp_path):
    client = FlakyClient(FakeClient("unused"), failures=99)
    report = run(campaign(tmp_path), tmp_path, client)
    assert report.errored == 1 and report.completed == 0
    line = ledger_lines(report)[0]
    assert line["status"] == "error" and "APIConnectionError" in line["error"]


def test_freeze_gate(fake_v1_root, tmp_path, valid_spec_response):
    c = campaign(tmp_path, post_freeze=True)
    with pytest.raises(SetupError, match="no frozen configuration"):
        run(c, tmp_path, FakeClient(valid_spec_response))

    frozen = tmp_path / "frozen.json"
    frozen.write_text(json.dumps({"model": "openai/gpt-4o", "temperature": 0.0}))
    assert run(c, tmp_path, FakeClient(valid_spec_response)).completed == 1

    mismatched = campaign(tmp_path, campaign_id="t2", post_freeze=True, temperatures=[0.7])
    with pytest.raises(SetupError, match="frozen temperature"):
        run(mismatched, tmp_path, FakeClient(valid_spec_response))

    cross_model = campaign(
        tmp_path, campaign_id="t3", post_freeze=True,
        models=["openai/gpt-4o", "anthropic/claude-haiku-4.5"],
    )
    with pytest.raises(SetupError, match="frozen_model_only"):
        run(cross_model, tmp_path, FakeClient(valid_spec_response))
    cross_model_allowed = campaign(
        tmp_path, campaign_id="t4", post_freeze=True, frozen_model_only=False,
        models=["openai/gpt-4o", "anthropic/claude-haiku-4.5"],
    )
    assert run(cross_model_allowed, tmp_path, FakeClient(valid_spec_response)).completed == 2


def test_annotate_campaign_requires_format(tmp_path):
    with pytest.raises(SetupError, match="stage_options.format"):
        campaign(tmp_path, stage="annotate")


def test_isolation_is_rejected_for_now(tmp_path):
    with pytest.raises(SetupError, match="isolation"):
        campaign(tmp_path, stage="trace", stage_options={"isolation": "lima"})


def test_committed_c0_campaign_files_load():
    for path in sorted(Path("campaigns").glob("c0_*.json")):
        loaded = sweep.load_campaign(path)
        assert loaded.max_usd <= 3.0, f"{path} pilot brake looks wrong"
        assert loaded.models[0] == "openai/gpt-4o", "paper baseline model runs first"

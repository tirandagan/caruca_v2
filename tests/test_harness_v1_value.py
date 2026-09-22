"""Where a v1-versus-v2 delta is meaningful, and where emitting one must be impossible.

The rule these enforce: a `percent_change` is meaningful only when both sides are
independently measured values of the same quantity by the same method, **and the v1 side is
not the reference that defines the scale**. Where v1 *is* the reference it scores 1.0 by
construction, so `(v2 - 1) / 1` is an identity wearing a hat — and publishing it invites
"v2 is N% worse than v1" claims derived from nothing.
"""

from __future__ import annotations

import pytest

from caruca_v2.harness import methods, report


def test_a_delta_is_impossible_where_v1_defines_the_scale():
    for method in (
        methods.INVOCATION_SET_DIFF.method,
        methods.CONFIG_ENV_DIFF.method,
        methods.TRACE_RECOVERY_DIFF.method,
    ):
        side = report.v1_side(method)
        assert side.kind == report.V1_REFERENCE
        assert side.value is None
        assert "identity" in side.note
        # Even handed a measured-looking number, no delta can come out.
        assert report.percent_change(side, 0.5) is None


def test_annotation_against_v1_itself_is_a_reference_but_against_ground_truth_is_not():
    """Ground truth is a third party, so both annotators can be scored against it.

    v1 is not guaranteed 1.0 there: E0 found v1 on `main` deriving "side-effectful" for `cp`
    where the paper says "pure".
    """
    vs_v1 = report.v1_side(methods.ANNOTATION_DIFF.method, reference_kind="v1_same_traces")
    assert vs_v1.kind == report.V1_REFERENCE

    vs_truth = report.v1_side(
        methods.ANNOTATION_DIFF.method, reference_kind="ground_truth", measured=0.8
    )
    assert vs_truth.kind == report.V1_MEASURED
    assert report.percent_change(vs_truth, 0.9) == pytest.approx(0.125)


def test_stage_one_carries_a_real_delta_because_v1_also_uses_a_model():
    """The one stage where both systems run an LLM, so the comparison is like-for-like.

    v1's side is its committed `outputs/llm-dsl-generation/` output, measured at 78/116 by
    v1's own instrument — not the paper's 116/120.
    """
    side = report.v1_side(
        methods.Q2_SYNTAX_DIFF.method, measured=0.672, source="outputs/llm-dsl-generation"
    )
    assert side.kind == report.V1_MEASURED
    assert side.source == "outputs/llm-dsl-generation"
    assert report.percent_change(side, 0.75) == pytest.approx((0.75 - 0.672) / 0.672)


def test_an_unmeasured_v1_side_is_unavailable_rather_than_zero():
    """Cost and wall-clock deltas are blocked on measuring v1, not on arithmetic."""
    side = report.v1_side(methods.MEASURED_COST.method)
    assert side.kind == report.V1_UNAVAILABLE
    assert side.value is None
    assert report.percent_change(side, 1.23) is None


def test_a_zero_v1_value_never_divides():
    side = report.V1Side(value=0.0, kind=report.V1_MEASURED)
    assert report.percent_change(side, 0.5) is None


def test_the_record_says_why_a_v1_value_is_absent():
    """An absent number must read as a decision, not an oversight."""
    arm = report.Arm(model="openai/gpt-4o", prompt_variant="default", temperature=0.0)
    arm.f1.values.extend([0.9, 0.95])
    records = report.comparison_records(
        [arm], "c5_generate", method=methods.INVOCATION_SET_DIFF.method
    )
    (record,) = records
    assert record["v1_value"] is None
    assert record["v1_value_kind"] == report.V1_REFERENCE
    assert record["percent_change"] is None
    assert record["denominator"] == methods.INVOCATION_SET_DIFF.denominator
    assert record["match_rate"] == record["v2_value"]


# --- the per-stage dispatcher -------------------------------------------------------------


def test_every_stage_has_a_scorer_and_a_declared_reference():
    """Previously only `syntax_spec` was scored in a sweep, which is why the C0 ledgers
    carry scores for stage 1 and none for stages 2-4."""
    from caruca_v2.harness import rescore

    for stage in ("syntax_spec", "generate", "trace", "annotate"):
        assert stage in rescore._DISPATCH
        assert rescore.default_reference(stage) is not None
        assert methods.PRIMARY_BY_STAGE[stage] in methods.REGISTRY


def test_an_unknown_stage_is_a_record_not_an_exception(tmp_path):
    """One unscoreable cell must not sink a campaign's aggregation."""
    from caruca_v2.harness import rescore

    (tmp_path / "manifest.json").write_text('{"stage": "nonsense", "command": "cat"}')
    record = rescore.score_run(tmp_path)
    assert record["scoreable"] is False
    assert "no scorer for stage" in record["error"]


def test_a_missing_manifest_is_a_record_not_an_exception(tmp_path):
    from caruca_v2.harness import rescore

    record = rescore.score_run(tmp_path)
    assert record["scoreable"] is False
    assert "no manifest.json" in record["error"]


def test_a_ledger_entry_carries_every_metric_its_method_declares():
    """So aggregation never has to know which stage produced a row."""
    from caruca_v2.harness import rescore

    entry = rescore.ledger_entry(
        {
            "method": methods.TRACE_RECOVERY_DIFF.method,
            "scoreable": True,
            "core": {"micro": {"f1": 0.5, "recall": 0.4, "precision": 0.6}},
            "inference": {"micro": {"f1": 0.2}},
            "ceiling_fraction": 0.4,
        }
    )
    assert entry["core.micro.f1"] == 0.5
    assert entry["core.micro.recall"] == 0.4
    assert entry["inference.micro.f1"] == 0.2
    assert entry["ceiling_fraction"] == 0.4


def test_stage_two_keeps_its_second_method_whole_rather_than_flattening_it():
    """Stage 2 emits two methods over two denominators; merging them would blend them."""
    from caruca_v2.harness import rescore

    entry = rescore.ledger_entry(
        {
            "method": methods.INVOCATION_SET_DIFF.method,
            "scoreable": True,
            "f1": 0.9,
            "config_comparison": {
                "method": methods.CONFIG_ENV_DIFF.method,
                "env_agreement_rate": 0.0,
                "rates": {"arg_type": 0.0},
            },
        }
    )
    assert entry["f1"] == 0.9
    assert entry["config_comparison"]["method"] == methods.CONFIG_ENV_DIFF.method
    assert entry["config_comparison"]["env_agreement_rate"] == 0.0


def test_every_declared_metric_is_a_real_path_into_its_record():
    """A metric name that does not resolve extracts `None` silently.

    Both the trace and annotation registries shipped bare names for fields that live one or
    two levels down, and the ledgers filled with nulls rather than failing.
    """
    from caruca_v2.harness import rescore

    samples = {
        methods.TRACE_RECOVERY_DIFF.method: {
            "core": {"micro": {"f1": 1, "recall": 1, "precision": 1}},
            "inference": {"micro": {"f1": 1}},
            "ceiling_fraction": 1,
        },
        methods.ANNOTATION_DIFF.method: {
            # Rates lead, because aggregation averages the first metric and a count of
            # cases has no denominator to average against.
            "rates": {"fully_agreeing": 1.0, "pclass": 1.0},
            "agreement": {"fully_agreeing": 1, "pclass": 1, "comparable": 1},
        },
        methods.INVOCATION_SET_DIFF.method: {"f1": 1, "recall": 1, "precision": 1},
        methods.CONFIG_ENV_DIFF.method: {"env_agreement_rate": 1},
        methods.Q2_SYNTAX_DIFF.method: {
            "f1": 1,
            "exact_argument_rate": 1,
            "precision": 1,
            "recall": 1,
        },
    }
    for method, body in samples.items():
        entry = rescore.ledger_entry({"method": method, "scoreable": True, **body})
        for metric in methods.get(method).metrics:
            assert entry[metric] is not None, f"{method}.{metric} did not resolve"


def test_the_trace_scorer_can_be_told_where_the_v1_reference_lives(tmp_path):
    """v1's default trace path exists for 18 commands, none of which have ground truth.

    A parity campaign traces commands whose v1 reference had to be generated for it, so
    without a way to name that file every cell scores unscoreable — which is what happened
    to all 12 successful stage-3 cells until a `reference_traces_pattern` existed.
    """
    from caruca_v2.harness import rescore

    run = tmp_path / "run"
    run.mkdir()
    (run / "manifest.json").write_text('{"stage": "trace", "command": "cat"}')
    (run / "cat.traces.json").write_text(
        '[{"command": {"name": "cat", "body": []}, "true_str": "cat", "configs": ['
        '{"command": {"name": "cat", "body": []}, "return_code": 0, "stdout": "", '
        '"stderr": "", "traces": [["wf", "stdout"]]}]}]'
    )

    # Without a reference the cell is unscoreable rather than silently zero.
    absent = rescore.score_run(run, stage="trace")
    assert absent.get("available") is False

    reference = tmp_path / "cat.parity.json"
    reference.write_text((run / "cat.traces.json").read_text())
    scored = rescore.score_run(run, stage="trace", reference_path=reference)
    assert scored["available"] is True
    assert scored["core"]["micro"]["recall"] == 1.0

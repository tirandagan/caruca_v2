"""The stage-4 comparison, and the two defects it exists to fix.

The first two tests are the important ones: they pin defects that were live in the shipped
comparison and that would have silently corrupted every stage-4 number.
"""

from __future__ import annotations

import json

from caruca_v2.harness import annotation as ann
from caruca_v2.harness import methods


def pash(*cases: dict, command: str = "cat") -> str:
    return json.dumps({"command": command, "cases": list(cases), "options": []})


def v1_case(**over) -> dict:
    """A case in v1's own vocabulary."""
    base = {
        "predicate": {"operator": "exists", "operands": ["-n"]},
        "pclass": "pure",
        "inputs": ["args[:]"],
        "outputs": ["stdout"],
        "true_str": "cat -n",
        "comments": "generated",
    }
    return {**base, **over}


def truth_case(**over) -> dict:
    """The same case as the hand-curated files spell it."""
    base = {
        "predicate": {"operator": "exists", "operands": ["-n"]},
        "class": "pure",
        "inputs": ["args[:]"],
        "outputs": ["stdout"],
        "comment": "hand written",
    }
    return {**base, **over}


# --- defect 1: the ground truth is a different schema ------------------------------------


def test_a_perfect_answer_scores_zero_against_unprojected_ground_truth():
    """The defect, stated as a test.

    The hand-curated annotations use `class`/`comment`; v1 serializes `pclass`/`comments`.
    Compared without a projection, an answer that agrees on everything disagrees on the one
    field the evaluation cares most about.
    """
    unprojected = ann.compare_annotation(
        "pash",
        pash(v1_case()),
        pash(truth_case()),
        label="x",
        reference_kind=ann.REFERENCE_V1_SAME_TRACES,  # deliberately skips the projection
    )
    assert unprojected["agreement"]["pclass"] == 0
    assert unprojected["agreement"]["fully_agreeing"] == 0


def test_the_projection_makes_a_perfect_answer_score_perfectly():
    projected = ann.compare_annotation(
        "pash",
        pash(v1_case()),
        pash(truth_case()),
        label="x",
        reference_kind=ann.REFERENCE_GROUND_TRUTH,
    )
    assert projected["agreement"]["pclass"] == 1
    assert projected["agreement"]["fully_agreeing"] == 1
    assert projected["projection"]["applied"] is True
    assert projected["projection"]["renamed_fields"] == {"class": "pclass", "comment": "comments"}


def test_fields_that_exist_on_only_one_side_are_named_not_charged():
    """`aggregate` is ground-truth-only; `true_str` is v1-only. Neither is a disagreement."""
    projected = ann.compare_annotation(
        "pash",
        pash(v1_case()),
        json.dumps(
            {"command": "cat", "aggregate": "agg.py", "cases": [truth_case()], "options": []}
        ),
        label="x",
        reference_kind=ann.REFERENCE_GROUND_TRUTH,
    )
    assert set(projected["projection"]["unmatched_fields"]) == {"aggregate", "true_str"}
    assert projected["agreement"]["fully_agreeing"] == 1


def test_the_ground_truths_own_class_spelling_is_translated_and_counted():
    """`grep.json` case 2 says `side-effects`; v1's enum only admits `side-effectful`.

    Translating silently would quietly alter the most expensive artifact in the project, so
    every application is counted in the record.
    """
    projected = ann.compare_annotation(
        "pash",
        pash(v1_case(pclass="side-effectful")),
        pash(truth_case(**{"class": "side-effects"})),
        label="x",
        reference_kind=ann.REFERENCE_GROUND_TRUTH,
    )
    assert projected["agreement"]["pclass"] == 1
    assert projected["projection"]["class_aliases_applied"] == 1


# --- defect 2: v1's own output is not byte-stable ----------------------------------------


def test_set_built_fields_compare_as_sets_not_as_ordered_lists():
    """v1 builds inputs/outputs with `list(set(...))`, so their order varies per process.

    Comparing them ordered can report a difference for v1 against itself.
    """
    reordered = ann.compare_annotation(
        "pash",
        pash(v1_case(inputs=["a", "b"], outputs=["stdout", "stderr"])),
        pash(v1_case(inputs=["b", "a"], outputs=["stderr", "stdout"])),
        label="x",
        reference_kind=ann.REFERENCE_V1_SAME_TRACES,
    )
    assert reordered["agreement"]["inputs"] == 1
    assert reordered["agreement"]["outputs"] == 1
    assert reordered["agreement"]["fully_agreeing"] == 1
    # The ordered figure is kept, as presentation only.
    assert reordered["ordered_agreement"]["inputs_ordered"] == 0


# --- alignment, absence, and honesty ------------------------------------------------------


def test_a_field_missing_from_both_sides_is_not_agreement():
    """`None == None` would score a match and hide exactly the schema mismatch above."""
    both_absent = ann.compare_annotation(
        "pash",
        pash({"predicate": "default", "pclass": "pure"}),
        pash({"predicate": "default", "pclass": "pure"}),
        label="x",
        reference_kind=ann.REFERENCE_V1_SAME_TRACES,
    )
    assert both_absent["absent_from_both_sides"]["inputs"] == 1
    assert both_absent["agreement"]["inputs"] == 0
    # ...and it is excluded from that field's denominator rather than scored as a failure.
    assert both_absent["rates"]["inputs"] is None


def test_cases_align_by_predicate_regardless_of_order():
    one = {"operator": "exists", "operands": ["-n"]}
    two = {"operator": "exists", "operands": ["-b"]}
    result = ann.compare_annotation(
        "pash",
        pash(v1_case(predicate=two, true_str="cat -b"), v1_case(predicate=one)),
        pash(v1_case(predicate=one), v1_case(predicate=two, true_str="cat -b")),
        label="x",
        reference_kind=ann.REFERENCE_V1_SAME_TRACES,
    )
    assert result["alignment"] == ann.ALIGN_BY_PREDICATE
    assert result["cases"]["aligned"] == 2
    assert result["agreement"]["fully_agreeing"] == 2


def test_and_operand_order_does_not_split_a_predicate_key():
    left = {"operator": "and", "operands": [{"operator": "exists", "operands": ["-n"]}, "x"]}
    right = {"operator": "and", "operands": ["x", {"operator": "exists", "operands": ["-n"]}]}
    assert ann.canonical_predicate(left) == ann.canonical_predicate(right)


def test_formats_without_a_case_key_say_their_alignment_is_positional():
    """Posh cases carry no key, so index alignment is all there is — and it is weak."""
    result = ann.compare_annotation(
        "posh",
        json.dumps({"command": "cat", "cases": [{"input_split": True}]}),
        json.dumps({"command": "cat", "cases": [{"input_split": True}]}),
        label="x",
        reference_kind=ann.REFERENCE_V1_SAME_TRACES,
    )
    assert result["alignment"] == ann.ALIGN_POSITIONAL


def test_a_missing_reference_is_unavailable_rather_than_zero():
    """No hand-curated files exist for sash or shellcheck; that is not a score of 0."""
    result = ann.compare_annotation(
        "sash", "[]", None, label="x", reference_kind=ann.REFERENCE_GROUND_TRUTH
    )
    assert result["available"] is False
    assert "no ground_truth reference" in result["error"]


def test_shellcheck_degrades_to_text_shape_rather_than_inventing_fields():
    result = ann.compare_annotation(
        "shellcheck",
        "module Caruca where\nx = 1\n",
        "module Caruca where\nx = 2\n",
        label="x",
        reference_kind=ann.REFERENCE_V1_SAME_TRACES,
    )
    assert result["alignment"] == ann.ALIGN_TEXT
    assert result["diff_lines"] == 2
    assert result["agreement"]["comparable"] is None


def test_the_record_refuses_to_collapse_into_one_number():
    result = ann.compare_annotation(
        "pash",
        pash(v1_case()),
        pash(v1_case()),
        label="x",
        reference_kind=ann.REFERENCE_V1_SAME_TRACES,
    )
    assert result["method"] == methods.ANNOTATION_DIFF.method
    assert "no_single_score" in result
    assert isinstance(result["agreement"], dict)
    # The diff shape the stage reported before is still reported.
    assert {"identical", "produced_lines", "reference_lines", "diff_lines"} <= set(result)


def test_self_test_requires_every_scored_field_to_agree():
    outcome = ann.self_test("pash", pash(v1_case()), reference_kind=ann.REFERENCE_V1_SAME_TRACES)
    assert outcome["passed"] is True
    assert outcome["comparable"] == 1


# --- cross-granularity alignment ------------------------------------------------------------


def test_v1_conjunctions_and_hand_written_atoms_align_by_subsumption():
    """The two artifacts are written at different granularities.

    v1 emits one conjunction per observed flag combination (14 cases for `cat`); the
    hand-curated file writes 3 general atoms. Key matching aligns zero of them and yields
    0/0 -- no information at all -- so they are related by the rule PaSh itself uses to
    select a case.
    """
    conjunction = {
        "operator": "and",
        "operands": [
            {"operator": "exists", "operands": ["-n"]},
            {"operator": "len_args_eq", "operands": [0]},
        ],
    }
    result = ann.compare_annotation(
        "pash",
        pash(v1_case(predicate=conjunction)),
        pash(truth_case(predicate={"operator": "exists", "operands": ["-n"]})),
        label="x",
        reference_kind=ann.REFERENCE_GROUND_TRUTH,
    )
    assert result["alignment"] == ann.ALIGN_BY_SUBSUMPTION
    assert result["cases"]["aligned"] == 1
    assert result["agreement"]["pclass"] == 1


def test_the_most_specific_covering_case_wins_and_default_is_chosen_last():
    specific = {"operator": "exists", "operands": ["-n"]}
    conjunction = {
        "operator": "and",
        "operands": [specific, {"operator": "len_args_eq", "operands": [0]}],
    }
    assert ann.subsumes(specific, conjunction) is True
    assert ann.subsumes("default", conjunction) is True
    # ...but "default" requires nothing, so it ranks below any real condition.
    assert len(ann.predicate_atoms("default") or ()) == 0
    assert len(ann.predicate_atoms(specific)) == 1


def test_a_general_case_does_not_cover_an_invocation_lacking_its_condition():
    assert (
        ann.subsumes(
            {"operator": "exists", "operands": ["-b"]},
            {"operator": "exists", "operands": ["-n"]},
        )
        is False
    )


def test_predicate_is_not_scored_when_subsumption_did_the_aligning():
    """A predicate difference is what subsumption accounts for, not a disagreement to
    charge on top of it."""
    conjunction = {
        "operator": "and",
        "operands": [
            {"operator": "exists", "operands": ["-n"]},
            {"operator": "len_args_eq", "operands": [0]},
        ],
    }
    result = ann.compare_annotation(
        "pash",
        pash(v1_case(predicate=conjunction)),
        pash(truth_case(predicate={"operator": "exists", "operands": ["-n"]})),
        label="x",
        reference_kind=ann.REFERENCE_GROUND_TRUTH,
    )
    assert "predicate" not in result["rates"]
    assert result["agreement"]["fully_agreeing"] == 1


def test_same_granularity_sides_still_align_by_key():
    """v1 against v1 is the same granularity, so nothing changes there."""
    result = ann.compare_annotation(
        "pash",
        pash(v1_case()),
        pash(v1_case()),
        label="x",
        reference_kind=ann.REFERENCE_V1_SAME_TRACES,
    )
    assert result["alignment"] == ann.ALIGN_BY_PREDICATE

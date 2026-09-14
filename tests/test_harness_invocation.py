"""The stage-2 equivalence relation, stated as tests.

These are the executable form of the claim in `harness/invocation.py`'s docstring: option
order is not meaning, operand order is, and spelling is never scored. A change that makes
one of these fail has changed what every stage-2 number means.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from caruca_v2 import v1
from caruca_v2.harness import invocation as inv
from caruca_v2.harness import methods


def table(**takes_value: bool) -> inv.OptionTable:
    """An option table built by hand, standing in for one read from v1's spec."""
    return inv.OptionTable(takes_value=dict(takes_value), source="test", available=True)


GREPISH = table(
    **{
        "--color": True,
        "--exclude": True,
        "-m": True,
        "--max-count": True,
        "-e": True,
        "-i": False,
        "--ignore-case": False,
        "-v": False,
        "-w": False,
    }
)


# --- the relation itself ----------------------------------------------------------------


def test_equals_and_space_spellings_are_one_invocation():
    """`--color=always` and `--color always` are the same invocation.

    Scoring them apart charges one convention difference to recall and precision at once,
    roughly halving both.
    """
    left = inv.parse_invocation("grep --color=always a", "grep", GREPISH)
    right = inv.parse_invocation("grep --color always a", "grep", GREPISH)
    assert left.key == right.key


def test_quoting_differences_are_one_invocation():
    left = inv.parse_invocation("grep --exclude '*.txt' a", "grep", GREPISH)
    right = inv.parse_invocation("grep --exclude=*.txt a", "grep", GREPISH)
    assert left.key == right.key


def test_option_order_is_not_meaning():
    """POSIX option parsing is order-independent, so neither is the comparison."""
    left = inv.parse_invocation("grep -i -v a", "grep", GREPISH)
    right = inv.parse_invocation("grep -v -i a", "grep", GREPISH)
    assert left.key == right.key


def test_operand_order_IS_meaning():
    """`cp a b` is not `cp b a`. A bag-of-tokens relation would call them equal."""
    left = inv.parse_invocation("cp a b", "cp", table())
    right = inv.parse_invocation("cp b a", "cp", table())
    assert left.key != right.key


def test_a_flag_and_its_alias_are_not_silently_unified():
    """Aliases share a `takes_value` entry but remain distinct surfaces.

    v1 enumerates `-i` and `--ignore-case` as separate invocations; collapsing them here
    would shrink the denominator and flatter the model.
    """
    left = inv.parse_invocation("grep -i a", "grep", GREPISH)
    right = inv.parse_invocation("grep --ignore-case a", "grep", GREPISH)
    assert left.key != right.key


def test_a_short_flag_keeps_an_equals_inside_its_value():
    """Only long options take `--flag=value`; a value containing `=` must survive intact."""
    parsed = inv.parse_invocation("grep -e a=b f", "grep", GREPISH)
    assert parsed.options == (("-e", "a=b"),)
    assert parsed.operands == ("f",)


def test_attached_short_values_are_recognised():
    parsed = inv.parse_invocation("grep -m1 a", "grep", GREPISH)
    assert parsed.options == (("-m", "1"),)
    assert parsed.form.attached_short == 1


def test_short_bundles_expand_only_when_every_member_is_a_known_valueless_flag():
    bundled = inv.parse_invocation("grep -iv a", "grep", GREPISH)
    assert bundled.options == (("-i", None), ("-v", None))
    assert bundled.form.bundled_short == 1
    assert bundled.key == inv.parse_invocation("grep -i -v a", "grep", GREPISH).key


def test_an_unrecognised_option_is_recorded_not_coerced():
    """The same stance `trace.py` takes with interactions it cannot normalize."""
    parsed = inv.parse_invocation("grep --not-a-real-flag a", "grep", GREPISH)
    assert parsed.unknown_option_tokens == 1


def test_a_bare_dash_is_an_operand_not_an_option():
    """`-` is stdin. v1's own spec marks grep's positional `dash_as_stdin=True`."""
    parsed = inv.parse_invocation("grep a -", "grep", GREPISH)
    assert parsed.operands == ("a", "-")
    assert parsed.options == ()


def test_everything_after_a_double_dash_is_an_operand():
    parsed = inv.parse_invocation("grep -- -i a", "grep", GREPISH)
    assert parsed.operands == ("-i", "a")
    assert parsed.options == ()
    assert parsed.form.explicit_end_of_options is True


def test_an_unlexable_fragment_is_reported_rather_than_counted_as_a_miss():
    """v1 emits values containing newlines, and reading its output by line splits them.

    The fragments have unbalanced quotes. Charging them to the model as misses would
    overstate the gap, so they are excluded from the counts and reported on their own.
    """
    assert inv.parse_invocation("grep --group-separator '", "grep", GREPISH) is None
    assert inv.normalize_invocation("grep --group-separator '") is None


# --- what the record must carry ---------------------------------------------------------


def reference(*invocations: str, hint: int = 99) -> v1.ReferenceInvocations:
    return v1.ReferenceInvocations(
        invocations=list(invocations), count=len(invocations), length_hint=hint, available=True
    )


def test_the_record_names_its_method_denominator_and_relation():
    result = inv.compare_invocation_sets(
        ["grep --color=always a"],
        reference("grep --color always a"),
        command="grep",
        table=GREPISH,
    )
    assert result["method"] == methods.INVOCATION_SET_DIFF.method
    assert result["instrument"] == inv.INSTRUMENT_SEMANTIC
    assert "invocations" in result["denominator"]
    assert result["equivalence"] == inv.EQUIVALENCE


def test_the_pre_normalization_figures_ride_along_in_every_record():
    """The structural defense against widening a normalizer: the weaker numbers stay visible."""
    result = inv.compare_invocation_sets(
        ["grep --color=always a"],
        reference("grep --color always a"),
        command="grep",
        table=GREPISH,
    )
    assert result["counts"]["matched"] == 1
    assert result["secondary"]["literal"]["matched"] == 0
    assert result["secondary"]["argv"]["matched"] == 1


def test_form_differences_are_counted_not_scored():
    result = inv.compare_invocation_sets(
        ["grep --color=always a"],
        reference("grep --color always a"),
        command="grep",
        table=GREPISH,
    )
    form = result["form_notes"]
    assert result["recall"] == 1.0
    assert form["form_identical"] == 0
    assert form["differs_equals_style"] == 1


def test_token_order_differences_are_reported_separately_from_equals_style():
    result = inv.compare_invocation_sets(
        ["grep a -i"], reference("grep -i a"), command="grep", table=GREPISH
    )
    assert result["recall"] == 1.0
    assert result["form_notes"]["differs_token_order_only"] == 1
    assert result["form_notes"]["differs_equals_style"] == 0


def test_the_injectivity_guard_reports_when_the_relation_merges_reference_invocations():
    """0 means normalization destroyed no information on the reference side.

    Above 0 means the relation is collapsing distinct v1 output, which shrinks the
    denominator and inflates the score — so the run says so in its own record.
    """
    clean = inv.compare_invocation_sets(
        ["grep -i a"], reference("grep -i a", "grep -v a"), command="grep", table=GREPISH
    )
    assert clean["parse_health"]["reference_keys_collapsing_multiple_spellings"] == 0

    merged = inv.compare_invocation_sets(
        ["grep -i a"], reference("grep -i -v a", "grep -v -i a"), command="grep", table=GREPISH
    )
    assert merged["parse_health"]["reference_keys_collapsing_multiple_spellings"] == 1


def test_unavailability_is_recorded_rather_than_scored_as_zero():
    result = inv.compare_invocation_sets(
        ["a"], v1.ReferenceInvocations.unavailable("v1 enumeration timed out"), command="a"
    )
    assert result["available"] is False
    assert "timed out" in result["error"]


def test_a_missing_option_table_degrades_to_heuristics_and_says_so(tmp_path: Path):
    degraded = inv.option_table("nosuchcommand", tmp_path / "absent.py")
    assert degraded.available is False
    assert degraded.parse_mode == inv.PARSE_MODE_HEURISTIC
    # `=`-joined values are still recoverable without a table; a space-separated value is not,
    # and the record's `parse_mode` is what tells a reader which regime produced the number.
    assert inv.parse_invocation("grep --color=always a", "grep", degraded).options == (
        ("--color", "always"),
    )


# --- the method registry ------------------------------------------------------------------


def test_methods_are_never_blendable_with_each_other():
    assert methods.are_comparable("invocation_set_diff", "invocation_set_diff") is True
    assert methods.are_comparable("invocation_set_diff", "q2_syntax_diff") is False


def test_an_envelope_refuses_an_instrument_the_method_does_not_define():
    with pytest.raises(ValueError, match="not defined for method"):
        methods.envelope("invocation_set_diff", "structural")


def test_an_unknown_method_names_what_is_registered():
    with pytest.raises(KeyError, match="registered methods are"):
        methods.get("not_a_method")

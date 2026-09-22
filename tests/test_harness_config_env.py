"""The stage-2 environment comparison — task 002's deferred instrument.

The case these tests exist for: a model can produce exactly the right invocation string and
still ask for the wrong world. Scoring invocation strings alone calls that a success.
"""

from __future__ import annotations

from typing import Any

from caruca_v2 import v1
from caruca_v2.harness import config_env as ce
from caruca_v2.harness import methods


def config(*args: dict[str, Any], name: str = "grep", stdin: str = "HUMAN_TEXT") -> dict:
    """A CommandConfig payload with one body node holding `args`."""
    return {
        "name": name,
        "body": [{"flag": None, "args": list(args), "arity": "1", "node_type": "args"}],
        "string": {},
        "stdin": stdin,
    }


def arg(value: str, arg_type: str, **over: Any) -> dict[str, Any]:
    return {"value": value, "arg_type": arg_type, **over}


def reference(mapping: dict[str, list[dict]]) -> v1.ReferenceConfigs:
    return v1.ReferenceConfigs(
        by_invocation=mapping,
        count=sum(len(v) for v in mapping.values()),
        invocation_count=len(mapping),
        available=True,
    )


def test_the_right_invocation_with_the_wrong_environment_is_caught():
    """The error the invocation diff cannot see.

    A model typed grep's regex `a` as `already` — asking the sandbox to contain a file named
    `a` — where v1 types it `no_env`, a plain string. Identical invocation string, different
    world, and the configs downstream of it would trace the wrong thing.
    """
    result = ce.compare_config_sets(
        {"grep a": [config(arg("a", "already", relative=False))]},
        reference({"grep a": [config(arg("a", "no_env"))]}),
        command="grep",
    )
    assert result["env_agreement_rate"] == 0.0
    assert result["rates"]["arg_type"] == 0.0
    assert result["mismatch_sample"][0]["differing_fields"] == ["arg_type", "relative"]


def test_an_environment_v1_would_have_produced_counts_as_agreeing():
    result = ce.compare_config_sets(
        {"grep a": [config(arg("a", "no_env"))]},
        reference({"grep a": [config(arg("a", "no_env"))]}),
        command="grep",
    )
    assert result["env_agreement_rate"] == 1.0
    assert result["rates"]["fully_agreeing"] == 1.0


def test_matching_any_one_of_v1s_variants_is_enough_to_agree():
    """v1 expands one invocation into every environment variant of its paths.

    The prompt asks for one config, so asking for *a* variant v1 would build is the fair
    bar — not reproducing all five.
    """
    variants = [
        config(arg("f", "file", relative=True, content="HUMAN_TEXT")),
        config(arg("f", "directory_empty", relative=True)),
        config(arg("f", "nonexistent", relative=True, parent_exists=True)),
    ]
    result = ce.compare_config_sets(
        {"grep f": [variants[1]]}, reference({"grep f": variants}), command="grep"
    )
    assert result["env_agreement_rate"] == 1.0
    assert result["counts"]["v1_configs"] == 3
    assert result["counts"]["produced_configs"] == 1


def test_variant_recall_carries_the_caveat_that_it_describes_the_prompt():
    """It is a real ratio, and reporting it as a model result would be misleading."""
    variants = [config(arg("f", "file")), config(arg("f", "directory_empty"))]
    result = ce.compare_config_sets(
        {"grep f": [variants[0]]}, reference({"grep f": variants}), command="grep"
    )
    assert result["env_variant_recall"]["value"] == 0.5
    assert "describes the prompt, not the model" in result["env_variant_recall"]["caveat"]


def test_the_random_identifier_is_dropped_with_its_reason_recorded():
    """v1 generates `identifier` with random.choices() per process (ir/syntax.py:87).

    Two semantically identical configs from two v1 processes are not equal as dicts;
    comparing these fields would score a PRNG.
    """
    assert "identifier" in ce.DROPPED_FIELDS
    assert "random" in ce.DROPPED_FIELDS["identifier"]

    noisy = config(arg("a", "no_env"))
    noisy["body"][0]["symbol"] = "_STRING_BGIGH"
    noisy["body"][0]["identifier"] = "BGIGH"
    quiet = config(arg("a", "no_env"))
    quiet["body"][0]["symbol"] = "_STRING_ICXPA"
    quiet["body"][0]["identifier"] = "ICXPA"

    assert noisy != quiet  # raw equality fails...
    assert ce.env_request(noisy).key == ce.env_request(quiet).key  # ...the request is the same


def test_node_grouping_is_scored_but_kept_out_of_the_key():
    """How the model groups args into body nodes differs from v1 without changing the ask.

    Folding it into the key would hide it as a plain mismatch; scoring it separately says
    what actually differed.
    """
    one_node = config(arg("a", "no_env"), arg("f", "file"))
    two_nodes = {
        "name": "grep",
        "body": [
            {"flag": None, "args": [arg("a", "no_env")], "arity": "1", "node_type": "args"},
            {"flag": None, "args": [arg("f", "file")], "arity": "*", "node_type": "args"},
        ],
        "string": {},
        "stdin": "HUMAN_TEXT",
    }
    result = ce.compare_config_sets(
        {"grep a f": [one_node]}, reference({"grep a f": [two_nodes]}), command="grep"
    )
    # Same demands, so the environment agrees...
    assert result["env_agreement_rate"] == 1.0
    # ...but the grouping difference is reported rather than lost.
    assert result["rates"]["node_grouping"] == 0.0


def test_stdin_is_compared():
    result = ce.compare_config_sets(
        {"grep a": [config(arg("a", "no_env"), stdin="MATH")]},
        reference({"grep a": [config(arg("a", "no_env"), stdin="HUMAN_TEXT")]}),
        command="grep",
    )
    assert result["rates"]["stdin"] == 0.0


def test_an_invocation_v1_never_produced_is_counted_apart_from_a_wrong_environment():
    result = ce.compare_config_sets(
        {"grep --invented": [config(arg("x", "no_env"))]},
        reference({"grep a": [config(arg("a", "no_env"))]}),
        command="grep",
    )
    assert result["counts"]["unmatched_invocation"] == 1
    assert result["counts"]["env_disagreeing"] == 0


def test_the_record_names_its_method_and_what_it_dropped():
    result = ce.compare_config_sets(
        {"grep a": [config(arg("a", "no_env"))]},
        reference({"grep a": [config(arg("a", "no_env"))]}),
        command="grep",
    )
    assert result["method"] == methods.CONFIG_ENV_DIFF.method
    assert set(result["normalization"]["dropped_fields"]) == set(ce.DROPPED_FIELDS)
    # v1's own `generate --full` renames every config it emits; the record says we avoided it.
    assert "splitcat" in result["reference_note"]


def test_unavailability_is_recorded_rather_than_scored_as_zero():
    result = ce.compare_config_sets(
        {}, v1.ReferenceConfigs.unavailable("v1 enumeration timed out"), command="grep"
    )
    assert result["available"] is False
    assert "timed out" in result["error"]

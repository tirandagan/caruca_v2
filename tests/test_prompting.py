"""Prompt assembly, and the determinism `prompt_hash` depends on."""

from __future__ import annotations

import pytest

from caruca_v2 import prompting
from caruca_v2.errors import PromptError


def test_substitution_replaces_every_placeholder():
    assert prompting.substitute("a {{x}} c {{y}}", {"x": "b", "y": "d"}) == "a b c d"


def test_missing_placeholder_is_an_error_not_an_empty_string():
    with pytest.raises(PromptError) as excinfo:
        prompting.substitute("{{present}} {{absent}}", {"present": "ok"})
    assert "absent" in str(excinfo.value)


def test_substituted_values_are_not_rescanned():
    # A man page containing braces must not be able to inject a placeholder.
    result = prompting.substitute("{{doc}}", {"doc": "{{command}}"})
    assert result == "{{command}}"


def test_syntax_spec_prompt_assembles_from_the_committed_files():
    values = {
        "command": "mkdir",
        "man_page": "MKDIR(1)",
        "few_shot_examples": "### Example: `touch`",
        "spec_symbol": "mkdir_syntax_spec",
    }
    prompt = prompting.build("syntax_spec", values)

    assert "expert on the shell" in prompt.system
    assert "MKDIR(1)" in prompt.user
    assert "mkdir_syntax_spec" in prompt.user
    assert "{{" not in prompt.system and "{{" not in prompt.user


def test_identical_inputs_produce_an_identical_hash():
    values = {
        "command": "mkdir",
        "man_page": "MKDIR(1)",
        "few_shot_examples": "example",
        "spec_symbol": "mkdir_syntax_spec",
    }
    assert prompting.build("syntax_spec", values).prompt_hash == (
        prompting.build("syntax_spec", values).prompt_hash
    )


def test_a_changed_input_changes_the_hash():
    base = {
        "command": "mkdir",
        "man_page": "MKDIR(1)",
        "few_shot_examples": "example",
        "spec_symbol": "mkdir_syntax_spec",
    }
    other = {**base, "man_page": "MKDIR(1) revised"}
    assert prompting.build("syntax_spec", base).prompt_hash != (
        prompting.build("syntax_spec", other).prompt_hash
    )


def test_the_system_user_split_is_unambiguous_in_the_hash():
    # Without a separator, ("ab", "c") and ("a", "bc") would hash identically.
    assert prompting.hash_prompt("ab", "c") != prompting.hash_prompt("a", "bc")


def test_unknown_stage_names_the_missing_file():
    with pytest.raises(PromptError) as excinfo:
        prompting.build("no_such_stage", {})
    assert "no_such_stage" in str(excinfo.value)

"""The stage-1 scorer, exercised through the fake v1 checkout.

The fake checkout's specs are plain tuples rather than DSL objects; the dump script
handles both shapes, so these tests drive the identical subprocess path production uses.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from caruca_v2 import v1
from caruca_v2.errors import SetupError
from caruca_v2.harness import score

SPEC_AB = """\
mkdir_syntax_spec = [
    [
        [("-a",), ("-b",)],
        [("PATH",)],
    ]
]
"""

SPEC_AZ = """\
mkdir_syntax_spec = [
    [
        [("-a",), ("-z",)],
        [("PATH",)],
    ]
]
"""

SPEC_RENAMED = """\
mkdir_syntax_spec = [
    [
        [("--alpha-new",), ("--beta-new",)],
        [("PATH",)],
    ]
]
"""


def write_spec(tmp_path: Path, source: str) -> Path:
    path = tmp_path / "generated_mkdir.py"
    path.write_text(source)
    return path


def test_dump_inventory_reads_flags_and_positionals(fake_v1_root, tmp_path):
    inventory = v1.dump_spec_inventory("mkdir", write_spec(tmp_path, SPEC_AB))
    assert inventory.ok and inventory.available
    flags = [e["flag"] for e in inventory.entries if e["flag"]]
    positionals = [e for e in inventory.entries if not e["flag"]]
    assert flags == ["-a", "-b"]
    assert len(positionals) == 1 and positionals[0]["value_name"] == "PATH"


def test_identical_spec_scores_perfectly(fake_v1_root, tmp_path):
    record = score.score_spec("mkdir", write_spec(tmp_path, SPEC_AB))
    assert record["scoreable"]
    assert record["counts"] == {
        "generated_flags": 2, "reference_flags": 2, "matched": 2,
        "missing": 0, "spurious": 0,
    }
    assert record["exact_argument_rate"] == 1.0
    assert record["f1"] == 1.0
    assert record["method"] == "q2_syntax_diff"


def test_missing_and_spurious_are_counted(fake_v1_root, tmp_path):
    record = score.score_spec("mkdir", write_spec(tmp_path, SPEC_AZ))
    counts = record["counts"]
    assert counts["matched"] == 1
    assert counts["missing"] == 1 and record["missing_surfaces"] == [["-b"]]
    assert counts["spurious"] == 1 and record["spurious_surfaces"] == [["-z"]]


def test_uninterpretable_spec_is_not_scoreable(fake_v1_root, tmp_path):
    path = tmp_path / "generated_mkdir.py"
    path.write_text("this is not python at all (\n")
    record = score.score_spec("mkdir", path)
    assert not record["scoreable"]
    assert "did not interpret" in record["error"]


def test_ground_truth_reference(fake_v1_root, tmp_path):
    gt_dir = fake_v1_root / "caruca" / "src" / "caruca" / "doc_sources" / "ground-truth"
    gt_dir.mkdir(parents=True)
    (gt_dir / "mkdir.json").write_text(
        json.dumps({"flags": [{"short": ["-a"]}, {"short": ["-b"]}], "options": []})
    )
    record = score.score_spec(
        "mkdir", write_spec(tmp_path, SPEC_AB), reference=score.REFERENCE_GROUND_TRUTH
    )
    assert record["scoreable"] and record["counts"]["matched"] == 2

    touch_spec = tmp_path / "generated_touch.py"
    touch_spec.write_text(SPEC_AB.replace("mkdir_syntax_spec", "touch_syntax_spec"))
    with pytest.raises(SetupError, match="no ground-truth flag inventory"):
        score.score_spec(
            "touch", touch_spec, reference=score.REFERENCE_GROUND_TRUTH
        )


def test_transform_renames_the_reference(fake_v1_root, tmp_path):
    transform = tmp_path / "rename.json"
    transform.write_text(
        json.dumps({"command": ["mkdir", "zorp"],
                    "surfaces": {"-a": "--alpha-new", "-b": "--beta-new"}})
    )
    record = score.score_spec(
        "mkdir", write_spec(tmp_path, SPEC_RENAMED), transform_path=transform
    )
    assert record["counts"]["matched"] == 2
    assert record["counts"]["missing"] == 0 and record["counts"]["spurious"] == 0
    # Without the transform the renamed spec matches nothing.
    record_untransformed = score.score_spec("mkdir", write_spec(tmp_path, SPEC_RENAMED))
    assert record_untransformed["counts"]["matched"] == 0


def test_cmp_specs_unavailable_without_v1_script(fake_v1_root, tmp_path):
    outcome = v1.run_cmp_specs(
        "mkdir", write_spec(tmp_path, SPEC_AB), write_spec(tmp_path, SPEC_AB)
    )
    assert not outcome.available
    assert "not found" in outcome.error


def test_cmp_specs_parses_v1_output(fake_v1_root, tmp_path):
    eval_dir = fake_v1_root / "eval"
    eval_dir.mkdir()
    (eval_dir / "cmp_specs.py").write_text(
        "print('Number of different elements: 3')\n"
        "print('Number of elements in ground truth: 97')\n"
        "print('Correct percentage: 0.969')\n"
    )
    outcome = v1.run_cmp_specs(
        "mkdir", write_spec(tmp_path, SPEC_AB), write_spec(tmp_path, SPEC_AB)
    )
    assert outcome.available
    assert outcome.correct_percentage == pytest.approx(0.969)
    assert outcome.diff_count == 3 and outcome.reference_fields == 97


def test_self_test_is_perfect_on_the_fake_checkout(fake_v1_root):
    outcome = score.self_test()
    assert outcome["all_perfect"], outcome
    assert set(outcome["commands"]) == set(v1.EXEMPLAR_COMMANDS)


def test_reference_duplicates_across_syntax_forms_count_once(fake_v1_root, tmp_path):
    # v1's own wc spec repeats its option list in two alternative syntax forms; the
    # perfect one-copy inventory must score perfectly. Caught by pilot campaign C0.
    duplicated_ref = tmp_path / "reference_mkdir.py"
    duplicated_ref.write_text(
        "mkdir_syntax_spec = [\n"
        "    [[(\"-a\",), (\"-b\",)], [(\"PATH\",)]],\n"
        "    [[(\"-a\",), (\"-b\",), (\"--extra\",)]],\n"
        "]\n"
    )
    generated = tmp_path / "generated_mkdir.py"
    generated.write_text(
        'mkdir_syntax_spec = [[[("-a",), ("-b",), ("--extra",)], [("PATH",)]]]\n'
    )
    record = score.score_spec("mkdir", generated, reference_path=duplicated_ref)
    assert record["counts"]["reference_flags"] == 3
    assert record["counts"]["matched"] == 3
    assert record["counts"]["missing"] == 0 and record["counts"]["spurious"] == 0
    assert record["f1"] == 1.0

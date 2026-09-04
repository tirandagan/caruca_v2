"""The v1 boundary: path resolution, error messages, and subprocess validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from caruca_v2 import v1
from caruca_v2.errors import V1AccessError


def test_slug_joins_multi_word_commands():
    assert v1.slug("git commit") == "git_commit"
    assert v1.slug("mkdir") == "mkdir"


def test_man_page_reads_from_the_checkout(fake_v1_root: Path):
    assert "a fabricated command" in v1.man_page("mkdir")


def test_man_page_for_multi_word_command(fake_v1_root: Path):
    assert "git commit" in v1.man_page("git commit")


def test_missing_man_page_names_the_exact_path_tried(fake_v1_root: Path):
    with pytest.raises(V1AccessError) as excinfo:
        v1.man_page("nosuchcommand")
    message = str(excinfo.value)
    assert "nosuchcommand.txt" in message
    assert "--docs" in message


def test_missing_checkout_names_the_env_var(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("CARUCA_V1_ROOT", str(tmp_path / "absent"))
    with pytest.raises(V1AccessError) as excinfo:
        v1.man_page("mkdir")
    assert "CARUCA_V1_ROOT" in str(excinfo.value)


def test_exemplars_are_v1s_four_in_v1s_order(fake_v1_root: Path):
    exemplars = v1.exemplars()
    assert [exemplar.command for exemplar in exemplars] == ["touch", "rm", "mv", "ls"]
    assert all(exemplar.man_page and exemplar.syntax_spec for exemplar in exemplars)


def test_validation_passes_for_a_spec_defining_the_symbol(fake_v1_root: Path, tmp_path: Path):
    spec = tmp_path / "mkdir.py"
    spec.write_text("mkdir_syntax_spec = [[[('-a',)], [('PATH',)]]]\n")

    result = v1.validate_syntax_spec("mkdir", spec)

    assert result.available
    assert result.passed
    assert result.elements == 2


def test_validation_fails_when_the_symbol_is_missing(fake_v1_root: Path, tmp_path: Path):
    spec = tmp_path / "mkdir.py"
    spec.write_text("wrongly_named_spec = []\n")

    result = v1.validate_syntax_spec("mkdir", spec)

    assert result.available
    assert not result.passed
    assert "mkdir_syntax_spec" in result.error


def test_validation_fails_with_a_traceback_for_broken_python(fake_v1_root: Path, tmp_path: Path):
    spec = tmp_path / "mkdir.py"
    spec.write_text("this is not python(\n")

    result = v1.validate_syntax_spec("mkdir", spec)

    assert result.available
    assert not result.passed
    assert "SyntaxError" in result.error
    assert result.traceback


def test_validation_reports_unavailable_when_v1s_venv_is_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    root = tmp_path / "v1_without_venv"
    (root / "caruca" / "src" / "caruca").mkdir(parents=True)
    monkeypatch.setenv("CARUCA_V1_ROOT", str(root))
    spec = tmp_path / "mkdir.py"
    spec.write_text("mkdir_syntax_spec = []\n")

    result = v1.validate_syntax_spec("mkdir", spec)

    # "v1 could not be reached" must never be reported as "v1 rejected the spec".
    assert not result.available
    assert not result.passed
    assert ".venv" in result.error


def test_validation_leaves_no_bytecode_cache_in_the_run_directory(
    fake_v1_root: Path, tmp_path: Path
):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    spec = run_dir / "mkdir.py"
    spec.write_text("mkdir_syntax_spec = []\n")

    v1.validate_syntax_spec("mkdir", spec)

    # Run directories are evidence; only evidence belongs in them.
    assert sorted(p.name for p in run_dir.iterdir()) == ["mkdir.py"]

"""Prompt assembly: load Markdown from `prompts/`, substitute `{{placeholders}}`, hash.

Deliberately dumb. Substitution is plain string replacement with no expression language,
so the same inputs always produce a byte-identical prompt and `prompt_hash` is a usable
reproducibility key. Anything cleverer would make the hash depend on interpreter details.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .errors import PromptError

PLACEHOLDER_PATTERN = re.compile(r"\{\{(\w+)\}\}")


@lru_cache(maxsize=1)
def prompts_root() -> Path:
    """The repo-root `prompts/` directory.

    Resolved relative to this file (``src/caruca_v2/prompting.py`` -> repo root) so the
    CLI works from any working directory.
    """
    root = Path(__file__).resolve().parents[2] / "prompts"
    if not root.is_dir():
        raise PromptError(f"prompts directory not found at {root}.")
    return root


DEFAULT_VARIANT = "default"


@dataclass(frozen=True)
class Prompt:
    """An assembled prompt, plus the hash that identifies it in telemetry."""

    system: str
    user: str
    prompt_hash: str
    variant: str = DEFAULT_VARIANT
    files: tuple[str, ...] = ()

    def as_messages(self) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": self.system},
            {"role": "user", "content": self.user},
        ]


def variant_dir(stage: str, variant: str) -> Path:
    """Where a variant's files live.

    The default variant is the stage directory itself, so the frozen prompt keeps its
    path and its hash: adding this mechanism must not change what an unflagged run sends.
    """
    root = prompts_root() / stage
    return root if variant == DEFAULT_VARIANT else root / "variants" / variant


def available_variants(stage: str) -> list[str]:
    """Every variant name for a stage, default first."""
    variants = [DEFAULT_VARIANT]
    container = prompts_root() / stage / "variants"
    if container.is_dir():
        variants += sorted(p.name for p in container.iterdir() if p.is_dir())
    return variants


def _load(stage: str, name: str, variant: str = DEFAULT_VARIANT) -> str:
    path = variant_dir(stage, variant) / f"{name}.md"
    if not path.is_file():
        known = ", ".join(available_variants(stage))
        raise PromptError(
            f"prompt file not found at {path}. Known variants for {stage!r}: {known}."
        )
    return path.read_text()


def substitute(template: str, values: dict[str, str]) -> str:
    """Replace every `{{name}}` in `template`. An unfilled placeholder is an error.

    Substituted values are never re-scanned, so a man page containing `{{foo}}` cannot
    inject a placeholder into the prompt.
    """
    missing: list[str] = []

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            missing.append(key)
            return match.group(0)
        return values[key]

    result = PLACEHOLDER_PATTERN.sub(replace, template)
    if missing:
        raise PromptError(
            f"no value supplied for placeholder(s) {sorted(set(missing))} in this prompt template."
        )
    return result


def hash_prompt(system: str, user: str) -> str:
    """SHA-256 over both messages, with an explicit separator so the split is unambiguous."""
    digest = hashlib.sha256()
    digest.update(system.encode())
    digest.update(b"\x00")
    digest.update(user.encode())
    return digest.hexdigest()


def build(
    stage: str, values: dict[str, str], variant: str = DEFAULT_VARIANT
) -> Prompt:
    """Assemble a stage's prompt from `variant` with `values`.

    A variant is a different *wording* of the same task, not a different task: it exists so
    the prompt-phrasing confound recorded as deviation 1 and 5 in `v2_fidelity_to_v1.md`
    can be measured during configuration selection instead of assumed. The variant name and
    its files are recorded alongside `prompt_hash`, which already differs per variant.
    """
    system = substitute(_load(stage, "system", variant), values)
    user = substitute(_load(stage, "user", variant), values)
    directory = variant_dir(stage, variant)
    files = tuple(
        str((directory / f"{name}.md").relative_to(prompts_root().parent))
        for name in ("system", "user")
    )
    return Prompt(
        system=system,
        user=user,
        prompt_hash=hash_prompt(system, user),
        variant=variant,
        files=files,
    )

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


@dataclass(frozen=True)
class Prompt:
    """An assembled prompt, plus the hash that identifies it in telemetry."""

    system: str
    user: str
    prompt_hash: str

    def as_messages(self) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": self.system},
            {"role": "user", "content": self.user},
        ]


def _load(stage: str, name: str) -> str:
    path = prompts_root() / stage / f"{name}.md"
    if not path.is_file():
        raise PromptError(f"prompt file not found at {path}.")
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


def build(stage: str, values: dict[str, str]) -> Prompt:
    """Assemble `prompts/<stage>/{system,user}.md` with `values`."""
    system = substitute(_load(stage, "system"), values)
    user = substitute(_load(stage, "user"), values)
    return Prompt(system=system, user=user, prompt_hash=hash_prompt(system, user))

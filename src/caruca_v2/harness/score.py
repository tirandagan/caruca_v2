"""The stage-1 scorer: argument-by-argument comparison of syntax specifications.

Two instruments, reported side by side and never blended:

* **structural** (primary) — both spec files are interpreted by v1 itself
  (`v1.dump_spec_inventory`), flattened to argument entries, and matched by surface
  form. The denominator is arguments, and every count is inspectable.
* **cmp_specs** (secondary) — v1's own `eval/cmp_specs.py`, the instrument behind the
  paper's Q2 number, kept for comparability. Its denominator bug is documented in
  `memory/caruca_v1_eval_tooling_notes.md` and flagged in the record.

References: v1's committed specs (the primary population, per E0's pin) or the
hand-annotated ground-truth JSON (secondary, 108 commands). Either side may be renamed
through a transform map — the renamed-documentation arms of the memorization experiment
score against ground truth renamed by the same map, so the transform is a first-class
parameter here rather than a retrofit.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .. import v1
from ..errors import SetupError

METHOD = "q2_syntax_diff"

REFERENCE_V1_SPECS = "v1-specs"
REFERENCE_GROUND_TRUTH = "ground-truth"
REFERENCES = (REFERENCE_V1_SPECS, REFERENCE_GROUND_TRUTH)


@dataclass(frozen=True)
class ArgEntry:
    """One argument, normalized for matching.

    `surfaces` is every way the argument can be spelled (flag plus aliases), sorted.
    Positionals have no surfaces and are compared as a multiset of kinds instead.
    """

    surfaces: tuple[str, ...]
    takes_value: bool
    kind: str
    arity: str | None = None
    choices: tuple[str, ...] | None = None

    @property
    def is_flag(self) -> bool:
        return bool(self.surfaces)


def entries_from_inventory(inventory: list[dict[str, Any]]) -> list[ArgEntry]:
    """Normalize a `dump_spec_inventory` payload."""
    entries = []
    for raw in inventory:
        surfaces: list[str] = []
        if raw.get("flag"):
            surfaces.append(raw["flag"])
        surfaces.extend(raw.get("alias") or [])
        choices = raw.get("choices")
        entries.append(
            ArgEntry(
                surfaces=tuple(sorted(set(surfaces))),
                takes_value=bool(raw.get("takes_value")),
                kind=str(raw.get("kind")),
                arity=raw.get("arity"),
                choices=None if choices is None else tuple(choices),
            )
        )
    return entries


def entries_from_ground_truth(payload: dict[str, Any]) -> list[ArgEntry]:
    """Normalize the hand-annotated flag inventory (`doc_sources/ground-truth/*.json`).

    That format records surface forms only — `flags` (no value) and `options` (take a
    value) with `short`/`long` spelling lists — so entries from here carry no kind,
    arity, or choices, and agreement is computed over what both sides actually state.
    """
    entries = []
    for takes_value, key in ((False, "flags"), (True, "options")):
        for item in payload.get(key) or []:
            surfaces = [*(item.get("short") or []), *(item.get("long") or [])]
            if not surfaces:
                continue
            entries.append(
                ArgEntry(
                    surfaces=tuple(sorted(set(surfaces))),
                    takes_value=takes_value,
                    kind="ground_truth",
                )
            )
    return entries


def load_transform(path: Path) -> dict[str, Any]:
    """A rename map: `{"command": ["cat", "zorp"], "surfaces": {"-n": "--enumerate"}}`."""
    payload = json.loads(path.read_text())
    if not isinstance(payload.get("surfaces"), dict):
        raise SetupError(
            f"transform file {path} must carry a `surfaces` object mapping old flag "
            "spellings to new ones."
        )
    return payload


def apply_transform(entries: list[ArgEntry], transform: dict[str, Any]) -> list[ArgEntry]:
    """Rename every surface through the map. Unmapped surfaces pass through unchanged."""
    surface_map: dict[str, str] = transform["surfaces"]
    return [
        ArgEntry(
            surfaces=tuple(sorted(surface_map.get(s, s) for s in entry.surfaces)),
            takes_value=entry.takes_value,
            kind=entry.kind,
            arity=entry.arity,
            choices=entry.choices,
        )
        for entry in entries
    ]


@dataclass
class MatchReport:
    """The structural comparison of two entry lists."""

    generated_flags: int = 0
    reference_flags: int = 0
    matched: int = 0
    missing: list[tuple[str, ...]] = field(default_factory=list)
    spurious: list[tuple[str, ...]] = field(default_factory=list)
    surfaces_exact: int = 0
    takes_value_agree: int = 0
    kind_agree: int | None = None
    arity_agree: int | None = None
    fully_agreeing: int = 0
    generated_positionals: int = 0
    reference_positionals: int = 0
    positional_kinds_agree: bool | None = None

    def as_dict(self) -> dict[str, Any]:
        precision = self.matched / self.generated_flags if self.generated_flags else None
        recall = self.matched / self.reference_flags if self.reference_flags else None
        f1 = None
        if precision and recall and (precision + recall):
            f1 = 2 * precision * recall / (precision + recall)
        exact_rate = (
            self.fully_agreeing / self.reference_flags if self.reference_flags else None
        )
        return {
            "counts": {
                "generated_flags": self.generated_flags,
                "reference_flags": self.reference_flags,
                "matched": self.matched,
                "missing": len(self.missing),
                "spurious": len(self.spurious),
            },
            "agreement": {
                "surfaces_exact": self.surfaces_exact,
                "takes_value": self.takes_value_agree,
                "kind": self.kind_agree,
                "arity": self.arity_agree,
                "fully_agreeing": self.fully_agreeing,
            },
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "exact_argument_rate": exact_rate,
            "missing_surfaces": [list(s) for s in self.missing[:20]],
            "spurious_surfaces": [list(s) for s in self.spurious[:20]],
            "positionals": {
                "generated": self.generated_positionals,
                "reference": self.reference_positionals,
                "kinds_agree": self.positional_kinds_agree,
            },
        }


def match(generated: list[ArgEntry], reference: list[ArgEntry]) -> MatchReport:
    """Match flag arguments by shared surface form; compare positionals as multisets.

    Matching is greedy over shared surfaces: two arguments are the same argument when
    any spelling overlaps. Field agreement (`kind`, `arity`) is only scored when both
    sides state the field — a ground-truth reference states neither, and scoring its
    absence as disagreement would fabricate error.
    """
    report = MatchReport()

    # An argument that appears identically in two alternative syntax forms is one
    # argument of the interface, not two. v1's own `wc` spec repeats its whole option
    # list across two forms; without this dedup a model producing the perfect flag
    # inventory scores 8/15. (Found by pilot campaign C0, 2026-09-08.) Structural
    # form-splitting is a separate question from the argument inventory and is not
    # scored here.
    def dedupe(entries: list[ArgEntry]) -> list[ArgEntry]:
        seen: set[tuple] = set()
        kept = []
        for entry in entries:
            key = (entry.surfaces, entry.takes_value, entry.kind, entry.arity, entry.choices)
            if key in seen:
                continue
            seen.add(key)
            kept.append(entry)
        return kept

    gen_flags = dedupe([e for e in generated if e.is_flag])
    ref_flags = dedupe([e for e in reference if e.is_flag])
    report.generated_flags = len(gen_flags)
    report.reference_flags = len(ref_flags)

    surface_to_ref: dict[str, int] = {}
    for index, entry in enumerate(ref_flags):
        for surface in entry.surfaces:
            surface_to_ref.setdefault(surface, index)

    used_ref: set[int] = set()
    both_have_kind = all(e.kind != "ground_truth" for e in ref_flags) and bool(ref_flags)
    kind_agree = 0
    arity_agree = 0
    arity_comparable = 0

    for gen_entry in gen_flags:
        target: int | None = None
        for surface in gen_entry.surfaces:
            candidate = surface_to_ref.get(surface)
            if candidate is not None and candidate not in used_ref:
                target = candidate
                break
        if target is None:
            report.spurious.append(gen_entry.surfaces)
            continue
        used_ref.add(target)
        ref_entry = ref_flags[target]
        report.matched += 1

        surfaces_exact = set(gen_entry.surfaces) == set(ref_entry.surfaces)
        takes_value_ok = gen_entry.takes_value == ref_entry.takes_value
        report.surfaces_exact += int(surfaces_exact)
        report.takes_value_agree += int(takes_value_ok)

        fully = surfaces_exact and takes_value_ok
        if both_have_kind:
            kind_ok = gen_entry.kind == ref_entry.kind
            kind_agree += int(kind_ok)
            fully = fully and kind_ok
            if gen_entry.arity is not None and ref_entry.arity is not None:
                arity_comparable += 1
                arity_ok = gen_entry.arity == ref_entry.arity
                arity_agree += int(arity_ok)
                fully = fully and arity_ok
        report.fully_agreeing += int(fully)

    for index, entry in enumerate(ref_flags):
        if index not in used_ref:
            report.missing.append(entry.surfaces)

    if both_have_kind:
        report.kind_agree = kind_agree
        report.arity_agree = arity_agree if arity_comparable else None

    gen_pos = sorted(e.kind for e in generated if not e.is_flag)
    ref_pos = sorted(e.kind for e in reference if not e.is_flag)
    report.generated_positionals = len(gen_pos)
    report.reference_positionals = len(ref_pos)
    if ref_flags and all(e.kind != "ground_truth" for e in ref_flags):
        report.positional_kinds_agree = gen_pos == ref_pos

    return report


def _reference_entries(
    command: str,
    reference: str,
    reference_path: Path | None,
) -> tuple[list[ArgEntry], str]:
    """Resolve the reference side to entries plus a provenance string."""
    if reference_path is not None:
        inventory = v1.dump_spec_inventory(command, reference_path)
        if not inventory.ok:
            raise SetupError(
                f"reference spec at {reference_path} could not be interpreted by v1: "
                f"{inventory.error}"
            )
        return entries_from_inventory(inventory.entries), str(reference_path)

    if reference == REFERENCE_V1_SPECS:
        path = v1.syntax_spec_path(command)
        inventory = v1.dump_spec_inventory(command, path)
        if not inventory.ok:
            raise SetupError(
                f"v1's committed spec for {command!r} could not be interpreted: "
                f"{inventory.error}"
            )
        return entries_from_inventory(inventory.entries), str(path)

    if reference == REFERENCE_GROUND_TRUTH:
        payload = v1.ground_truth_flags(command)
        if payload is None:
            raise SetupError(
                f"no ground-truth flag inventory for {command!r} "
                f"(looked for {v1.ground_truth_flags_path(command)}). The ground truth "
                "covers 108 of the 120 commands; use --reference v1-specs for the rest."
            )
        return entries_from_ground_truth(payload), str(v1.ground_truth_flags_path(command))

    raise SetupError(f"unknown reference {reference!r}; expected one of {REFERENCES}.")


def score_spec(
    command: str,
    spec_path: Path,
    *,
    reference: str = REFERENCE_V1_SPECS,
    reference_path: Path | None = None,
    transform_path: Path | None = None,
    with_cmp_specs: bool = False,
) -> dict[str, Any]:
    """Score one generated spec file against one reference. Returns the full record."""
    inventory = v1.dump_spec_inventory(command, spec_path)
    record: dict[str, Any] = {
        "method": METHOD,
        "instrument": "structural",
        "command": command,
        "generated_spec": str(spec_path),
        "reference": reference,
        "transform": None if transform_path is None else str(transform_path),
        "caruca_v1_commit": v1.v1_commit(),
        "scoreable": False,
    }

    if not inventory.available:
        record["error"] = f"v1 unavailable: {inventory.error}"
        return record
    if not inventory.ok:
        # The spec does not interpret — that is a scored outcome (0 matched arguments
        # would overstate it; "not scoreable" with the reason is the honest cell).
        record["error"] = f"generated spec did not interpret: {inventory.error}"
        return record

    generated = entries_from_inventory(inventory.entries)
    reference_entries, reference_source = _reference_entries(
        command, reference, reference_path
    )
    if transform_path is not None:
        reference_entries = apply_transform(
            reference_entries, load_transform(transform_path)
        )

    record["scoreable"] = True
    record["reference_source"] = reference_source
    record.update(match(generated, reference_entries).as_dict())

    if with_cmp_specs:
        if reference_path is not None or reference == REFERENCE_V1_SPECS:
            cmp_target = reference_path or v1.syntax_spec_path(command)
            outcome = v1.run_cmp_specs(command, spec_path, cmp_target)
            record["cmp_specs"] = {
                "available": outcome.available,
                "correct_percentage": outcome.correct_percentage,
                "diff_count": outcome.diff_count,
                "reference_fields": outcome.reference_fields,
                "error": outcome.error,
                "caveat": "denominator counts dataclass fields, not arguments "
                "(binpash/caruca#54)",
            }
        else:
            record["cmp_specs"] = {
                "available": False,
                "error": "cmp_specs compares two spec files; the ground-truth JSON is "
                "not a spec file",
            }

    return record


def self_test() -> dict[str, Any]:
    """Score each committed exemplar spec against itself. Every cell must be perfect."""
    results: dict[str, Any] = {}
    all_perfect = True
    for command in v1.EXEMPLAR_COMMANDS:
        record = score_spec(command, v1.syntax_spec_path(command))
        counts = record.get("counts") or {}
        perfect = (
            record.get("scoreable")
            and counts.get("missing") == 0
            and counts.get("spurious") == 0
            and record.get("exact_argument_rate") == 1.0
        )
        all_perfect = all_perfect and bool(perfect)
        results[command] = {
            "perfect": bool(perfect),
            "counts": counts,
            "error": record.get("error"),
        }
    return {"all_perfect": all_perfect, "commands": results}

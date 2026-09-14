"""The stage-4 scorer: do the two annotators derive the same specification?

Reported as a **vector of per-field agreements with explicit denominators**, never as one
similarity number. A presentation difference and a parallelizability-class disagreement are
not interchangeable, and this stage has no defensible way to weight them against each other.
The existing diff shape (line counts plus a bounded sample) is preserved alongside, so
nothing that was reported before stops being reported.

Three properties of the data force the design, and two of them were live defects:

1. **The hand-curated ground truth is a different schema from v1's own output.** The
   annotations two graduate students produced over 80 person-hours use ``class`` /
   ``comment`` / ``aggregate``; v1's ``PaShSpecification`` serializes ``pclass`` /
   ``comments`` / ``true_str``, with no pydantic aliases anywhere. Compared raw, **a
   perfect answer scores as a mismatch.** `GROUND_TRUTH_PROJECTION` renames across the gap
   and `ONLY_ON_ONE_SIDE` names the fields that genuinely exist on one side only, so they
   are reported rather than charged to either annotator.
2. **The ground truth's own class vocabulary is not quite v1's.** One case
   (``grep.json`` case 2) is classed ``side-effects`` where v1's `Parallelizability` enum
   admits only ``side-effectful``. `CLASS_ALIASES` maps it, and every application is counted
   in the record — a silent fix here would quietly alter the most expensive artifact in the
   project.
3. **v1's own output is not byte-stable against itself.** `Specification.to_pash` builds
   ``inputs``/``outputs`` with ``list(set(...))`` (`annotator/annotator.py:109,115,133,138`).
   String hashing is randomized per process, so the list order varies between runs and a
   plain equality check can report a difference for **v1 versus v1**. Those fields are
   compared as sets; the ordered comparison is kept as a presentation figure only.
"""

from __future__ import annotations

import difflib
import json
from collections.abc import Sequence
from typing import Any

from . import methods

METHOD = methods.ANNOTATION_DIFF.method

INSTRUMENT_STRUCTURAL = "structural_fields"
INSTRUMENT_TEXT = "text"

REFERENCE_V1_SAME_TRACES = "v1_same_traces"
REFERENCE_GROUND_TRUTH = "ground_truth"

#: Fields v1 builds from a Python ``set``. Their list order carries no information and is not
#: stable across v1 processes, so set comparison is primary.
SET_FIELDS = frozenset({"inputs", "outputs", "options", "deletions", "updates"})

#: Ground-truth field name -> v1 field name, per format.
GROUND_TRUTH_PROJECTION: dict[str, dict[str, str]] = {
    "pash": {"class": "pclass", "comment": "comments"},
}

#: Fields that exist on exactly one side. Named, so their absence is reported instead of
#: counting as a disagreement.
ONLY_ON_ONE_SIDE: dict[str, dict[str, tuple[str, ...]]] = {
    "pash": {REFERENCE_GROUND_TRUTH: ("aggregate",), "v1": ("true_str",)},
}

#: Ground-truth class spellings that name a v1 `Parallelizability` member under another
#: name. Applied explicitly and counted, never silently.
CLASS_ALIASES: dict[str, str] = {"side-effects": "side-effectful"}

#: Fields compared per case, per format. Anything outside this is reported but not scored.
SCORED_FIELDS: dict[str, tuple[str, ...]] = {
    "pash": ("predicate", "pclass", "inputs", "outputs"),
    "posh": ("input_split", "args_split", "input_geq_output"),
    "sash": ("preconditions", "postconditions"),
}

ALIGN_BY_PREDICATE = "predicate_key"
ALIGN_POSITIONAL = "positional"
ALIGN_TEXT = "text"


def canonical_predicate(predicate: Any) -> Any:
    """A predicate reduced to a hashable key, insensitive to operand order within `and`.

    Used only to *align* cases before comparing them. Alignment is not agreement: two cases
    that align may still disagree on every scored field.
    """
    if isinstance(predicate, dict):
        operator = predicate.get("operator")
        operands = predicate.get("operands", [])
        canonical = [canonical_predicate(item) for item in operands]
        if operator in {"and", "or"}:
            canonical = sorted(canonical, key=repr)
        return (operator, tuple(canonical))
    if isinstance(predicate, list):
        return tuple(canonical_predicate(item) for item in predicate)
    return predicate


def project_ground_truth(fmt: str, payload: Any) -> tuple[Any, dict[str, Any]]:
    """Rename ground-truth fields into v1's vocabulary, reporting what was translated."""
    renames = GROUND_TRUTH_PROJECTION.get(fmt)
    notes: dict[str, Any] = {
        "applied": bool(renames),
        "renamed_fields": dict(renames or {}),
        "class_aliases_applied": 0,
        "unmatched_fields": [],
    }
    if not renames or not isinstance(payload, dict):
        return payload, notes

    def project_case(case: dict[str, Any]) -> dict[str, Any]:
        out = dict(case)
        for source, target in renames.items():
            if source in out:
                out[target] = out.pop(source)
        pclass = out.get("pclass")
        if pclass in CLASS_ALIASES:
            out["pclass"] = CLASS_ALIASES[pclass]
            notes["class_aliases_applied"] += 1
        return out

    projected = dict(payload)
    projected["cases"] = [project_case(case) for case in payload.get("cases", [])]

    only = ONLY_ON_ONE_SIDE.get(fmt, {})
    present = set(payload) | {key for case in payload.get("cases", []) for key in case}
    notes["unmatched_fields"] = sorted(
        {field for field in only.get(REFERENCE_GROUND_TRUTH, ()) if field in present}
        | set(only.get("v1", ()))
    )
    return projected, notes


def _cases(fmt: str, payload: Any) -> list[dict[str, Any]]:
    """The comparable units of an annotation, per format."""
    if fmt == "sash":
        # SaSh is a root-level array of run specifications, not a wrapper with `cases`.
        return list(payload) if isinstance(payload, list) else []
    if isinstance(payload, dict):
        return list(payload.get("cases", []))
    return []


def align_cases(
    fmt: str, produced: Any, reference: Any
) -> tuple[list[tuple[dict | None, dict | None]], str]:
    """Pair up cases between two annotations, and say how they were paired.

    PaSh cases carry a predicate and are keyed by it. Posh and SaSh cases have no key, so
    they align by index — which is weak across lists of different lengths, and the record
    says `positional` so a reader knows not to over-read the result.
    """
    left, right = _cases(fmt, produced), _cases(fmt, reference)

    if fmt != "pash":
        width = max(len(left), len(right))
        pairs: list[tuple[dict | None, dict | None]] = [
            (left[i] if i < len(left) else None, right[i] if i < len(right) else None)
            for i in range(width)
        ]
        return pairs, ALIGN_POSITIONAL

    def index(cases: Sequence[dict[str, Any]]) -> dict[Any, dict[str, Any]]:
        return {canonical_predicate(case.get("predicate")): case for case in cases}

    left_index, right_index = index(left), index(right)
    pairs = []
    for key, case in left_index.items():
        pairs.append((case, right_index.get(key)))
    for key, case in right_index.items():
        if key not in left_index:
            pairs.append((None, case))
    return pairs, ALIGN_BY_PREDICATE


def _field_equal(field: str, left: Any, right: Any) -> bool:
    if field in SET_FIELDS:
        if isinstance(left, list) and isinstance(right, list):
            return {repr(item) for item in left} == {repr(item) for item in right}
    if field == "predicate":
        return canonical_predicate(left) == canonical_predicate(right)
    return left == right


def _diff_shape(produced: str, reference: str) -> dict[str, Any]:
    """Line counts and a bounded unified diff — the existing report, unchanged."""
    produced_lines, reference_lines = produced.splitlines(), reference.splitlines()
    diff = list(
        difflib.unified_diff(
            reference_lines, produced_lines, fromfile="v1", tofile="v2", lineterm="", n=1
        )
    )
    return {
        "identical": produced.strip() == reference.strip(),
        "produced_lines": len(produced_lines),
        "reference_lines": len(reference_lines),
        # `---`/`+++` are unified-diff file headers, not differing content lines.
        "diff_lines": len(
            [
                line
                for line in diff
                if line.startswith(("+", "-")) and not line.startswith(("---", "+++"))
            ]
        ),
        "diff_sample": diff[:60],
    }


def compare_annotation(
    fmt: str,
    produced_text: str,
    reference_text: str | None,
    *,
    label: str,
    reference_kind: str,
) -> dict[str, Any]:
    """Compare two annotations of the same command, field by field."""
    record = methods.envelope(
        METHOD,
        INSTRUMENT_STRUCTURAL if fmt != "shellcheck" else INSTRUMENT_TEXT,
        label=label,
        format=fmt,
        reference_kind=reference_kind,
    )
    if reference_text is None:
        record.update(
            {
                "available": False,
                "error": f"no {reference_kind} reference exists for format {fmt!r}",
            }
        )
        return record

    record["available"] = True
    record.update(_diff_shape(produced_text, reference_text))

    if fmt == "shellcheck":
        # Rendered Haskell. Degrade honestly to line shape rather than inventing a field
        # comparison the format does not support.
        record.update(
            {
                "alignment": ALIGN_TEXT,
                "agreement": {
                    "comparable": None,
                    "note": "shellcheck output is rendered Haskell; only text shape is comparable",
                },
            }
        )
        return record

    try:
        produced = json.loads(produced_text)
        reference = json.loads(reference_text)
    except (json.JSONDecodeError, TypeError) as exc:
        record["structurally_identical"] = None
        record["structural_error"] = f"{type(exc).__name__}: {exc}"
        return record

    projection: dict[str, Any] = {"applied": False}
    if reference_kind == REFERENCE_GROUND_TRUTH:
        reference, projection = project_ground_truth(fmt, reference)

    record["structurally_identical"] = produced == reference

    pairs, alignment = align_cases(fmt, produced, reference)
    aligned = [(left, right) for left, right in pairs if left is not None and right is not None]
    fields = SCORED_FIELDS.get(fmt, ())

    agreement: dict[str, int] = {"comparable": len(aligned)}
    ordered_agreement: dict[str, int] = {}
    disagreements: list[dict[str, Any]] = []

    for field in fields:
        agreement[field] = 0
        if field in SET_FIELDS:
            ordered_agreement[f"{field}_ordered"] = 0
    # A field absent from BOTH sides is not agreement — `None == None` would score a match
    # and hide exactly the schema mismatch this module exists to fix. Counted apart, and
    # excluded from the denominator for that field.
    absent_both: dict[str, int] = {field: 0 for field in fields}

    fully = 0
    for left, right in aligned:
        all_agree = True
        for field in fields:
            if field not in left and field not in right:
                absent_both[field] += 1
                continue
            same = _field_equal(field, left.get(field), right.get(field))
            agreement[field] += int(same)
            if field in SET_FIELDS:
                ordered_agreement[f"{field}_ordered"] += int(left.get(field) == right.get(field))
            if not same:
                all_agree = False
                if len(disagreements) < 20:
                    case_label = left.get("true_str") or repr(
                        canonical_predicate(left.get("predicate"))
                    )
                    disagreements.append(
                        {
                            "case": case_label,
                            "field": field,
                            "produced": left.get(field),
                            "reference": right.get(field),
                        }
                    )
        fully += int(all_agree)
    agreement["fully_agreeing"] = fully

    denominator = len(aligned)
    record.update(
        {
            "alignment": alignment,
            "cases": {
                "produced": len(_cases(fmt, produced)),
                "reference": len(_cases(fmt, reference)),
                "aligned": len(aligned),
                "produced_only": sum(1 for left, right in pairs if right is None),
                "reference_only": sum(1 for left, right in pairs if left is None),
            },
            "agreement": agreement,
            "ordered_agreement": ordered_agreement,
            "absent_from_both_sides": {f: n for f, n in absent_both.items() if n},
            "rates": {
                **{
                    field: (
                        (agreement[field] / (denominator - absent_both[field]))
                        if (denominator - absent_both[field])
                        else None
                    )
                    for field in fields
                },
                "fully_agreeing": (fully / denominator) if denominator else None,
            },
            "set_field_note": (
                "inputs/outputs are built from Python sets in v1 "
                "(annotator/annotator.py:109,115,133,138); their list order is not stable "
                "across v1 processes, so the set comparison is primary and the ordered one "
                "is a presentation figure only"
            ),
            "projection": projection,
            "disagreement_sample": disagreements,
            "no_single_score": (
                "Reported as a vector on purpose: a presentation difference and a "
                "parallelizability-class disagreement are not interchangeable, and this "
                "stage has no defensible way to weight them against each other."
            ),
        }
    )
    return record


def self_test(fmt: str, annotation_text: str, *, reference_kind: str) -> dict[str, Any]:
    """Score an annotation against itself; every scored field must agree.

    A scorer that cannot show v1 matching v1 cannot be trusted to say v2 differs from v1.
    Passing a *reordered* copy of the same annotation is the check that pins the
    ``list(set(...))`` instability: it must still score as full agreement.
    """
    record = compare_annotation(
        fmt, annotation_text, annotation_text, label="self", reference_kind=reference_kind
    )
    agreement = record.get("agreement") or {}
    comparable = agreement.get("comparable")
    scored = [field for field in SCORED_FIELDS.get(fmt, ()) if field in agreement]
    return {
        "format": fmt,
        "comparable": comparable,
        "passed": bool(comparable) and all(agreement[field] == comparable for field in scored),
        "agreement": agreement,
    }

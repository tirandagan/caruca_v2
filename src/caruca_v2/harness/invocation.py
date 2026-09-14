"""The stage-2 scorer: does v2 enumerate the invocations v1 enumerates?

Three instruments over the same comparison, all reported in every record:

* **semantic** (primary) — both sides are parsed into an argument vector and compared as
  *options as a multiset, operands in order*. `--color=always` and `--color always` are one
  invocation; so are `--exclude '*.txt'` and `--exclude=*.txt`, which differ only in shell
  quoting. This is the fidelity bar the project chose: semantic equivalence, with form
  differences counted separately rather than scored as errors.
* **argv** (secondary) — shlex lexing with long options split on `=`, order significant.
* **literal** (secondary) — string equality, the original instrument.

Why options are order-insensitive but operands are not: POSIX option parsing is
order-independent, so `grep -i -v a` and `grep -v -i a` are the same invocation. Operand
*position* carries meaning — `cp a b` is not `cp b a` — so a bare bag-of-tokens would call
two different commands identical. The relation is deliberately the weakest one that is still
justified by shell semantics.

**On widening a normalizer until differences disappear.** Loosening a comparison until the
numbers improve is exactly the move this project excludes (see
`memory/feedback_instrument_defect_vs_tuning.md`), and this relation does raise `grep`'s
recall from 0.04 to 0.86 — so it needs an argument that does not appeal to the score. The
argument is injectivity: on v1's own output, even sorting *every* token after the binary
merges zero distinct invocations (`grep` 73 argv-unique / 73 sorted-unique; likewise `cat`,
`mkdir`, `wc`). v1 never emits two invocations differing only in option order, so collapsing
that difference destroys no information and leaves the denominator unchanged. Three guards
keep it honest: the relation is stated in prose in every record and frozen before any
campaign; `parse_health.reference_keys_collapsing_multiple_spellings` reports loudly if it
ever *does* start merging distinct v1 output; and the argv and literal figures ride along in
every record, so the pre-normalization number is always one field away. The test for any
future normalization step is whether it can be justified from shell semantics **without
looking at a score**.
"""

from __future__ import annotations

import shlex
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .. import v1
from . import methods

METHOD = methods.INVOCATION_SET_DIFF.method

INSTRUMENT_SEMANTIC = "semantic"
INSTRUMENT_ARGV = "argv"
INSTRUMENT_LITERAL = "literal"

#: Stated in every record. Frozen before any campaign runs; changing it changes what every
#: stage-2 number means, so it is versioned in prose rather than implied by the code.
EQUIVALENCE = (
    "options compared as a multiset of (flag, value) — order-insensitive; operands compared "
    "as an ordered sequence; '=' joining, attached short values, and short bundles "
    "normalized; shell quoting removed by shlex"
)

PARSE_MODE_SPEC = "spec_driven"
PARSE_MODE_HEURISTIC = "heuristic"


@dataclass(frozen=True)
class OptionTable:
    """Which surface forms consume the following token.

    Read from **v1's committed specification**, never from a model-generated one. That is
    fair — it is the command's own semantics, the same category of input as the man page —
    and it keeps a bad stage-1 output from corrupting stage-2 scoring. Both sides of every
    comparison are parsed with the identical table.
    """

    takes_value: dict[str, bool] = field(default_factory=dict)
    source: str = ""
    available: bool = False
    error: str | None = None

    @property
    def parse_mode(self) -> str:
        return PARSE_MODE_SPEC if self.available else PARSE_MODE_HEURISTIC

    def known(self, surface: str) -> bool:
        return surface in self.takes_value

    def consumes_value(self, surface: str) -> bool:
        return self.takes_value.get(surface, False)


def option_table(command: str, spec_path: Path | None = None) -> OptionTable:
    """Build the `takes_value` table from v1's committed spec for `command`."""
    path = spec_path or v1.syntax_spec_path(command)
    try:
        inventory = v1.dump_spec_inventory(command, path)
    except Exception as exc:  # noqa: BLE001 - fall back to heuristics, and say so
        return OptionTable(source=str(path), available=False, error=f"{type(exc).__name__}: {exc}")
    if not inventory.available or not inventory.ok:
        return OptionTable(source=str(path), available=False, error=inventory.error)

    table: dict[str, bool] = {}
    for entry in inventory.entries:
        flag = entry.get("flag")
        if not flag:
            continue  # a positional; it has no surface form
        takes_value = bool(entry.get("takes_value"))
        for surface in (flag, *(entry.get("alias") or [])):
            table[surface] = takes_value
    return OptionTable(takes_value=table, source=str(path), available=bool(table))


@dataclass(frozen=True)
class FormNote:
    """How an invocation was *spelled*, as distinct from what it means."""

    equals_joined: int = 0
    attached_short: int = 0
    bundled_short: int = 0
    explicit_end_of_options: bool = False


@dataclass(frozen=True)
class Invocation:
    """One invocation reduced to meaning, with its spelling kept alongside."""

    binary: tuple[str, ...]
    options: tuple[tuple[str, str | None], ...]  # sorted — a multiset
    operands: tuple[str, ...]  # order preserved — position is meaning
    form: FormNote = FormNote()
    unknown_option_tokens: int = 0
    binary_mismatch: bool = False

    @property
    def key(self) -> tuple[Any, ...]:
        return (self.binary, self.options, self.operands)


def _argv(text: str) -> tuple[str, ...] | None:
    """Lex, then split long options on `=`. `None` if the string will not lex.

    v1 emits invocations whose values contain newlines (`--group-separator` takes one), and
    reading its output line by line splits those into fragments with unbalanced quotes.
    Those are reported separately rather than charged to either side.
    """
    try:
        tokens = shlex.split(text)
    except ValueError:
        return None
    out: list[str] = []
    for token in tokens:
        if token.startswith("--") and "=" in token:
            flag, _, value = token.partition("=")
            out.extend((flag, value))
        else:
            out.append(token)
    return tuple(out)


def normalize_invocation(text: str) -> tuple[str, ...] | None:
    """The `argv` instrument: lex and split long options on `=`, order significant.

    Public because it is the secondary figure reported alongside every semantic score, and
    because it is the weaker normalization a reader may want to check a result against.
    """
    return _argv(text)


def parse_invocation(text: str, command: str, table: OptionTable) -> Invocation | None:
    """Parse one invocation string into its argument vector. `None` if it will not lex."""
    try:
        tokens = shlex.split(text)
    except ValueError:
        return None

    words = command.split()
    binary_mismatch = False
    index = 0
    for word in words:
        if index < len(tokens) and tokens[index] == word:
            index += 1
        else:
            binary_mismatch = True
    binary = tuple(words)

    options: list[tuple[str, str | None]] = []
    operands: list[str] = []
    equals_joined = attached_short = bundled_short = 0
    end_of_options = False
    unknown = 0

    while index < len(tokens):
        token = tokens[index]
        index += 1

        if end_of_options:
            operands.append(token)
            continue
        if token == "--":
            end_of_options = True
            continue
        if not token.startswith("-") or token == "-":
            # A bare "-" is stdin, an operand, not an option.
            operands.append(token)
            continue

        if token.startswith("--"):
            if "=" in token:
                flag, _, value = token.partition("=")
                options.append((flag, value))
                equals_joined += 1
                if not table.known(flag):
                    unknown += 1
                continue
            if table.consumes_value(token) and index < len(tokens):
                options.append((token, tokens[index]))
                index += 1
            else:
                options.append((token, None))
                if not table.known(token):
                    unknown += 1
            continue

        # Short option: -x, -xVALUE, or a bundle -abc.
        head = token[:2]
        rest = token[2:]
        if table.consumes_value(head):
            if rest:
                options.append((head, rest))
                attached_short += 1
            elif index < len(tokens):
                options.append((head, tokens[index]))
                index += 1
            else:
                options.append((head, None))
            continue
        if not rest:
            options.append((head, None))
            if not table.known(head):
                unknown += 1
            continue

        bundle = [f"-{char}" for char in token[1:]]
        if all(table.known(short) and not table.consumes_value(short) for short in bundle):
            options.extend((short, None) for short in bundle)
            bundled_short += 1
            continue

        # Not a recognizable option shape. Record it, never coerce it — the same stance
        # `trace.py` takes with interactions it cannot normalize.
        options.append((token, None))
        unknown += 1

    return Invocation(
        binary=binary,
        options=tuple(sorted(options, key=lambda pair: (pair[0], pair[1] or ""))),
        operands=tuple(operands),
        form=FormNote(
            equals_joined=equals_joined,
            attached_short=attached_short,
            bundled_short=bundled_short,
            explicit_end_of_options=end_of_options,
        ),
        unknown_option_tokens=unknown,
        binary_mismatch=binary_mismatch,
    )


@dataclass
class ParsedSet:
    """One side of the comparison, indexed three ways."""

    semantic: dict[tuple[Any, ...], str] = field(default_factory=dict)
    #: key -> the argv spellings seen for it. Answers "does the relation merge distinct v1
    #: invocations" (the injectivity guard).
    semantic_spellings: dict[tuple[Any, ...], set[str]] = field(default_factory=dict)
    #: key -> the *raw* strings seen for it. Answers "did the two sides spell it the same
    #: way" — which `=`-joining would hide if this shared the argv map.
    raw_spellings: dict[tuple[Any, ...], set[str]] = field(default_factory=dict)
    parsed: dict[tuple[Any, ...], Invocation] = field(default_factory=dict)
    argv: set[tuple[str, ...]] = field(default_factory=set)
    literal: set[str] = field(default_factory=set)
    unlexable: list[str] = field(default_factory=list)
    unknown_option_tokens: int = 0
    binary_mismatch: int = 0

    @property
    def collapsing_keys(self) -> int:
        """Semantic keys covering more than one distinct argv spelling.

        The injectivity guard. Measured 0 on v1's own output for cat/mkdir/wc/grep; anything
        above 0 means the relation is destroying information on the reference side, and the
        run says so in its own record instead of quietly scoring better.
        """
        return sum(1 for spellings in self.semantic_spellings.values() if len(spellings) > 1)


def parse_set(invocations: Iterable[str], command: str, table: OptionTable) -> ParsedSet:
    """Index one side of the comparison."""
    result = ParsedSet()
    for text in invocations:
        if not text.strip():
            continue
        result.literal.add(text)
        argv = _argv(text)
        parsed = parse_invocation(text, command, table)
        if argv is None or parsed is None:
            result.unlexable.append(text)
            continue
        result.argv.add(argv)
        result.unknown_option_tokens += parsed.unknown_option_tokens
        result.binary_mismatch += int(parsed.binary_mismatch)
        key = parsed.key
        result.semantic.setdefault(key, text)
        result.semantic_spellings.setdefault(key, set()).add(" ".join(argv))
        result.raw_spellings.setdefault(key, set()).add(text)
        result.parsed.setdefault(key, parsed)
    return result


def _form_notes(
    matched: set[tuple[Any, ...]], produced: ParsedSet, reference: ParsedSet
) -> dict[str, Any]:
    """How many matches needed which kind of normalization.

    This is the fidelity note the semantic-equivalence bar requires: the differences are
    reported rather than scored, so "they agree, in a different form" stays visible.
    """
    identical = differing = equals = short = order = 0
    for key in matched:
        left, right = produced.parsed[key], reference.parsed[key]
        if produced.raw_spellings[key] & reference.raw_spellings[key]:
            identical += 1
            continue
        differing += 1
        if left.form.equals_joined != right.form.equals_joined:
            equals += 1
        if (
            left.form.attached_short != right.form.attached_short
            or left.form.bundled_short != right.form.bundled_short
        ):
            short += 1
        # Same options and operands by construction (they share a key), and no form counter
        # differs, so what is left is the sequence the tokens were written in.
        if (
            left.form.equals_joined == right.form.equals_joined
            and left.form.attached_short == right.form.attached_short
            and left.form.bundled_short == right.form.bundled_short
        ):
            order += 1
    total = len(matched)
    return {
        "matched": total,
        "form_identical": identical,
        "form_identical_rate": (identical / total) if total else None,
        "differs_in_form": differing,
        "differs_equals_style": equals,
        "differs_short_form": short,
        "differs_token_order_only": order,
        "note": (
            "a match counted here agreed on flags, values and operand order but was spelled "
            "differently; the spelling difference is reported, never scored"
        ),
    }


def _counts(matched: int, produced: int, reference: int) -> dict[str, float | None]:
    return {
        "recall": (matched / reference) if reference else None,
        "precision": (matched / produced) if produced else None,
        "f1": ((2 * matched / (produced + reference)) if (produced + reference) else None),
    }


def compare_invocation_sets(
    produced: Sequence[str],
    reference: v1.ReferenceInvocations,
    *,
    command: str,
    table: OptionTable | None = None,
    bounds: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Set-diff v2's invocations against v1's own enumeration."""
    if not reference.available:
        return {"available": False, "error": reference.error}

    active = table if table is not None else option_table(command)
    left = parse_set(produced, command, active)
    right = parse_set(reference.invocations, command, active)

    matched_keys = set(left.semantic) & set(right.semantic)
    missing_keys = set(right.semantic) - set(left.semantic)
    spurious_keys = set(left.semantic) - set(right.semantic)

    argv_matched = left.argv & right.argv
    literal_matched = left.literal & right.literal

    record = methods.envelope(
        METHOD,
        INSTRUMENT_SEMANTIC,
        available=True,
        command=command,
        equivalence=EQUIVALENCE,
        parse_mode=active.parse_mode,
        option_table_source=active.source,
        option_table_error=active.error,
        bounds=bounds or {},
    )
    record.update(
        {
            "counts": {
                "v1_lines": reference.count,
                "v1_unique": len(right.semantic),
                "produced_lines": len(produced),
                "produced_unique": len(left.semantic),
                "matched": len(matched_keys),
                "missing": len(missing_keys),
                "spurious": len(spurious_keys),
            },
            **_counts(len(matched_keys), len(left.semantic), len(right.semantic)),
            "missing_sample": sorted(right.semantic[key] for key in missing_keys)[:20],
            "spurious_sample": sorted(left.semantic[key] for key in spurious_keys)[:20],
            "form_notes": _form_notes(matched_keys, left, right),
            "parse_health": {
                "unlexable_reference_lines": len(right.unlexable),
                "unlexable_produced_lines": len(left.unlexable),
                "unlexable_reference_sample": right.unlexable[:5],
                "unknown_option_tokens_reference": right.unknown_option_tokens,
                "unknown_option_tokens_produced": left.unknown_option_tokens,
                "binary_mismatch_produced": left.binary_mismatch,
                "reference_keys_collapsing_multiple_spellings": right.collapsing_keys,
                "injectivity_note": (
                    "0 means the equivalence relation merges no two distinct v1 invocations, "
                    "so the denominator is unchanged by normalization"
                ),
            },
            "secondary": {
                INSTRUMENT_ARGV: {
                    "matched": len(argv_matched),
                    "missing": len(right.argv - left.argv),
                    "spurious": len(left.argv - right.argv),
                    **_counts(len(argv_matched), len(left.argv), len(right.argv)),
                },
                INSTRUMENT_LITERAL: {
                    "matched": len(literal_matched),
                    "missing": len(right.literal - left.literal),
                    "spurious": len(left.literal - right.literal),
                    **_counts(len(literal_matched), len(left.literal), len(right.literal)),
                },
            },
            # Recorded, never a denominator: v1's `--number` hint disagrees with its own
            # enumeration for 90 of 90 measurable commands (E0).
            "v1_length_hint": reference.length_hint,
        }
    )
    return record


def self_test(command: str = "grep", *, max_arity: int = 1, max_count: int = 1) -> dict[str, Any]:
    """Score v1's own enumeration against itself, and against permutations of itself.

    A scorer that cannot show v1 matching v1 cannot be trusted to say v2 differs from v1.
    The permutation cases are the executable statement of the equivalence relation:
    reordering *options* must not change the score; reordering *operands* must.
    """
    reference = v1.reference_invocations(command, max_arity=max_arity, max_count=max_count)
    if not reference.available:
        return {"available": False, "error": reference.error}
    table = option_table(command)
    lines = list(reference.invocations)

    identity = compare_invocation_sets(lines, reference, command=command, table=table)

    def restyled() -> list[str]:
        out = []
        for line in lines:
            parsed = parse_invocation(line, command, table)
            if parsed is None:
                out.append(line)
                continue
            parts = list(parsed.binary)
            for flag, value in parsed.options:
                long_with_value = value is not None and flag.startswith("--")
                parts.append(f"{flag}={value}" if long_with_value else flag)
                if value is not None and not long_with_value:
                    parts.append(value)
            parts.extend(parsed.operands)
            out.append(" ".join(shlex.quote(p) for p in parts))
        return out

    def reordered_operands() -> list[str]:
        out = []
        for line in lines:
            parsed = parse_invocation(line, command, table)
            if parsed is None or len(parsed.operands) < 2:
                continue
            parts = list(parsed.binary)
            for flag, value in parsed.options:
                parts.append(flag)
                if value is not None:
                    parts.append(value)
            parts.extend(reversed(parsed.operands))
            out.append(" ".join(shlex.quote(p) for p in parts))
        return out

    equals_style = compare_invocation_sets(restyled(), reference, command=command, table=table)
    swapped = reordered_operands()
    operand_swap = (
        compare_invocation_sets(swapped, reference, command=command, table=table)
        if swapped
        else None
    )

    return {
        "command": command,
        "identity": {
            "recall": identity["recall"],
            "precision": identity["precision"],
            "collapsing_keys": identity["parse_health"][
                "reference_keys_collapsing_multiple_spellings"
            ],
            "passed": identity["recall"] == 1.0 and identity["precision"] == 1.0,
        },
        "equals_restyle": {
            "recall": equals_style["recall"],
            "passed": equals_style["recall"] == 1.0,
        },
        "operand_permutation": (
            {
                "recall": operand_swap["recall"],
                "passed": operand_swap["recall"] != 1.0,
                "note": "operand order is meaning; permuting it must NOT score as a match",
            }
            if operand_swap
            else {"skipped": "no invocation in this command has two or more operands"}
        ),
    }

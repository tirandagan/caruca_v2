"""The stage-2 environment scorer: does v2 ask for the filesystem v1 asks for?

Task 002 deferred this comparison to the harness and it was never built there, so until now
stage 2 was scored only on its invocation *strings*. That misses the error that matters most.
On `grep a relpath_1` a model produced the right string while typing the pattern `a` as
``arg_type: "already"`` — asking the sandbox to contain a file named `a` — where v1 types it
``no_env``, a plain string. Identical invocation, different world.

**This is deliberately not a one-to-one diff.** v1 expands one invocation into *every*
environment variant of its paths: `grep a relpath_1` yields five configurations (existing
file, empty directory, non-empty directory, nonexistent with a parent, nonexistent without).
The stage-2 prompt asks the model for one config per invocation. So the fair headline is
`env_agreement_rate` — *is the environment the model asked for one that v1 would have
produced?* — and `env_variant_recall` ships with a caveat saying it describes the prompt
rather than the model.

Named *agreement*, not *coverage*, on purpose. This is a correctness rate over the
environments v2 requested: 0.185 means 81.5% of them are wrong. "Coverage" is reserved in
this project for how much of a command's real behaviour a specification reaches (evaluation
dimension 3; the paper's Q3), and borrowing the word here made a failure rate read like a
reach figure.

Three fields are dropped before comparison, each for a stated reason. The important one is
`identifier`: v1 generates it with ``random.choices(ascii_uppercase, k=5)``
(`ir/syntax.py:87`), so it and the `symbol` derived from it differ on every v1 process.
Comparing them would score a pseudo-random number generator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .. import v1
from . import methods

METHOD = methods.CONFIG_ENV_DIFF.method
INSTRUMENT = "env_request"

#: Field -> why it is not compared. Emitted into every record, so a reader never has to
#: guess whether an absence is an oversight or a decision.
DROPPED_FIELDS: dict[str, str] = {
    "symbol": (
        "derived from `identifier`, which is random.choices() per v1 process (ir/syntax.py:87)"
    ),
    "identifier": "random per v1 process (ir/syntax.py:87)",
    "string": "invocation metadata, not an environment request; CommandConfig.__eq__ ignores it",
    "true_string": "pydantic computed field, derived from the rest",
    "sandbox": "a placeholder default, not an environment request",
}

#: Compared per demand, in this order.
DEMAND_FIELDS = ("value", "arg_type", "relative", "content", "parent_exists")

REFERENCE_SOURCE = (
    "caruca.ir.string.CommandInvocation.to_exec_env(prefix='', stdin_variation, "
    "content_variation), called directly"
)
REFERENCE_NOTE = (
    "v1's own `generate --full` calls to_exec_env('split', 'varied') against the signature "
    "(prefix, stdin_variation, content_variation), so 'split' lands in `prefix` and every "
    "config is renamed — all 175 of cat's configs are emitted as 'splitcat'. This comparison "
    "calls to_exec_env directly rather than reproducing that defect."
)


@dataclass(frozen=True)
class Demand:
    """One thing an invocation needs to exist (or not exist) before it can run."""

    value: str
    arg_type: str
    relative: bool | None = None
    content: str | None = None
    parent_exists: bool | None = None

    def get(self, field: str) -> Any:
        return getattr(self, field)


@dataclass(frozen=True)
class EnvRequest:
    """A configuration reduced to what it asks of the filesystem and of standard input."""

    name: str
    demands: tuple[Demand, ...]  # sorted — position within a config carries no meaning here
    stdin: str | None
    #: Kept out of the key but scored separately: this is where v1 and a model most often
    #: differ, and folding it into the key would hide that as a plain mismatch.
    node_grouping: tuple[tuple[str | None, int], ...] = ()

    @property
    def key(self) -> tuple[Any, ...]:
        return (self.name, tuple(sorted(_demand_key(d) for d in self.demands)), self.stdin)


def _demand_key(demand: Demand) -> tuple[Any, ...]:
    return tuple(demand.get(field) for field in DEMAND_FIELDS)


def env_request(config: dict[str, Any]) -> EnvRequest:
    """Normalize one `CommandConfig` payload to the environment it requests."""
    demands: list[Demand] = []
    grouping: list[tuple[str | None, int]] = []
    for node in config.get("body", []) or []:
        args = node.get("args") or []
        grouping.append((node.get("flag"), len(args)))
        for arg in args:
            demands.append(
                Demand(
                    value=str(arg.get("value", "")),
                    arg_type=str(arg.get("arg_type", "")),
                    relative=arg.get("relative"),
                    content=arg.get("content"),
                    parent_exists=arg.get("parent_exists"),
                )
            )
    return EnvRequest(
        name=str(config.get("name", "")),
        demands=tuple(sorted(demands, key=_demand_key)),
        stdin=config.get("stdin"),
        node_grouping=tuple(grouping),
    )


def _closest(produced: EnvRequest, variants: list[EnvRequest]) -> EnvRequest | None:
    """The variant agreeing on the most demand fields; ties broken deterministically."""
    if not variants:
        return None

    def score(variant: EnvRequest) -> tuple[int, str]:
        agreed = 0
        for left, right in zip(produced.demands, variant.demands, strict=False):
            agreed += sum(1 for f in DEMAND_FIELDS if left.get(f) == right.get(f))
        return (-agreed, repr(variant.key))

    return sorted(variants, key=score)[0]


def compare_config_sets(
    produced_by_invocation: dict[str, list[dict[str, Any]]],
    reference: v1.ReferenceConfigs,
    *,
    command: str,
    bounds: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compare the environments v2 requested against the ones v1 would build.

    `produced_by_invocation` maps an invocation string to the configs the model emitted for
    it — normally one. Keys are matched to v1's by the same semantic relation stage 2 uses
    for invocations, so the two instruments compose.
    """
    record = methods.envelope(
        METHOD,
        INSTRUMENT,
        command=command,
        reference_source=REFERENCE_SOURCE,
        reference_note=REFERENCE_NOTE,
        bounds=bounds or {},
        normalization={"dropped_fields": list(DROPPED_FIELDS), "reasons": DROPPED_FIELDS},
    )
    if not reference.available:
        record.update({"available": False, "error": reference.error})
        return record

    from .invocation import option_table, parse_invocation

    table = option_table(command)

    def semantic(text: str) -> Any:
        parsed = parse_invocation(text, command, table)
        return parsed.key if parsed is not None else ("__unlexable__", text)

    reference_index: dict[Any, list[EnvRequest]] = {}
    for text, configs in reference.by_invocation.items():
        reference_index.setdefault(semantic(text), []).extend(env_request(c) for c in configs)

    agreeing = disagreeing = unmatched = 0
    agreement = {field: 0 for field in DEMAND_FIELDS}
    agreement.update({"comparable": 0, "stdin": 0, "node_grouping": 0, "fully_agreeing": 0})
    mismatches: list[dict[str, Any]] = []
    produced_total = 0

    for text, configs in produced_by_invocation.items():
        variants = reference_index.get(semantic(text))
        if variants is None:
            unmatched += len(configs)
            continue
        variant_keys = {variant.key for variant in variants}
        for config in configs:
            produced_total += 1
            request = env_request(config)
            if request.key in variant_keys:
                agreeing += 1
            else:
                disagreeing += 1

            closest = _closest(request, variants)
            if closest is None:
                continue
            agreement["comparable"] += 1
            all_agree = True
            differing: list[str] = []
            for field in DEMAND_FIELDS:
                same = len(request.demands) == len(closest.demands) and all(
                    left.get(field) == right.get(field)
                    for left, right in zip(request.demands, closest.demands, strict=True)
                )
                agreement[field] += int(same)
                if not same:
                    all_agree = False
                    differing.append(field)
            for field, left_value, right_value in (
                ("stdin", request.stdin, closest.stdin),
                ("node_grouping", request.node_grouping, closest.node_grouping),
            ):
                same = left_value == right_value
                agreement[field] += int(same)
                if not same:
                    all_agree = False
                    differing.append(field)
            agreement["fully_agreeing"] += int(all_agree)
            if differing and len(mismatches) < 20:
                mismatches.append(
                    {
                        "invocation": text,
                        "produced": {
                            "demands": [_demand_key(d) for d in request.demands],
                            "stdin": request.stdin,
                        },
                        "closest_v1": {
                            "demands": [_demand_key(d) for d in closest.demands],
                            "stdin": closest.stdin,
                        },
                        "differing_fields": differing,
                    }
                )

    comparable = agreement["comparable"]
    record.update(
        {
            "available": True,
            "counts": {
                "v1_configs": reference.count,
                "v1_invocations_with_configs": reference.invocation_count,
                "produced_configs": produced_total,
                "env_agreeing": agreeing,
                "env_disagreeing": disagreeing,
                "unmatched_invocation": unmatched,
            },
            "env_agreement_rate": (agreeing / produced_total) if produced_total else None,
            "env_variant_recall": {
                "value": (agreeing / reference.count) if reference.count else None,
                "caveat": (
                    "the stage-2 prompt asks for one config per invocation; v1 emits every "
                    "environment variant of each. This ratio describes the prompt, not the "
                    "model, and must not be reported as a model result unless the prompt is "
                    "changed to request variants."
                ),
            },
            "agreement": agreement,
            "rates": {
                field: (agreement[field] / comparable) if comparable else None
                for field in (*DEMAND_FIELDS, "stdin", "node_grouping", "fully_agreeing")
            },
            "mismatch_sample": mismatches,
        }
    )
    return record


def self_test(command: str = "grep", *, max_arity: int = 1, max_count: int = 1) -> dict[str, Any]:
    """Score v1's own expansion against itself; every field must agree.

    Run **twice in separate v1 processes**. A single-process run would pass even if the
    comparison included `identifier`, because one process generates it once — it is the
    second process that exposes the randomness.
    """
    first = v1.reference_configs(command, max_arity=max_arity, max_count=max_count)
    second = v1.reference_configs(command, max_arity=max_arity, max_count=max_count)
    if not first.available or not second.available:
        return {"available": False, "error": first.error or second.error}

    result = compare_config_sets(
        second.by_invocation, first, command=command, bounds={"max_arity": max_arity}
    )
    agreement = result["agreement"]
    comparable = agreement["comparable"]
    return {
        "command": command,
        "two_process": True,
        "comparable": comparable,
        "env_agreement_rate": result["env_agreement_rate"],
        "passed": (
            result["env_agreement_rate"] == 1.0
            and comparable > 0
            and agreement["fully_agreeing"] == comparable
        ),
        "agreement": agreement,
    }

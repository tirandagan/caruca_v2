"""The comparison-method registry: one methodology per stage, never blended.

Each pipeline stage compares v2 against v1 over a *different denominator* — arguments,
invocations, filesystem interactions, annotation fields. Averaging across them produces a
number that means nothing, which is why every record in this project already carries a
`method` tag. This module makes that tag a lookup rather than a string literal typed at each
call site, so a new scorer cannot quietly invent a method id, and so `report.py` can refuse
to aggregate two methods into one arm.

The `method` / `instrument` split follows what `score.py` already does: `method` names the
methodology family (stable, one per stage, appears in every record and in the reports),
`instrument` names the implementation within it (`structural` vs `cmp_specs` for stage 1;
`semantic` vs `argv` vs `literal` for stage 2). Two instruments of one method are comparable
to each other. Two methods are not comparable at all.

Cost and wall-clock get their own method ids deliberately. They are not correctness
measures, and a correctness field must never hold a cost value or the reverse.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .. import v1


@dataclass(frozen=True)
class Method:
    """One comparison methodology, and the terms on which its numbers may be read."""

    method: str
    stage: str
    instruments: tuple[str, ...]
    metrics: tuple[str, ...]
    denominator: str
    #: Always empty. Present so the never-blend rule is visible in the data rather than
    #: living only in prose, and so a future change has to state its intent explicitly.
    blendable_with: tuple[str, ...] = ()

    @property
    def primary_instrument(self) -> str:
        return self.instruments[0]

    @property
    def primary_metric(self) -> str:
        return self.metrics[0]


Q2_SYNTAX_DIFF = Method(
    method="q2_syntax_diff",
    stage="syntax_spec",
    instruments=("structural", "cmp_specs"),
    metrics=("f1", "exact_argument_rate", "precision", "recall"),
    denominator="arguments in the reference specification",
)

INVOCATION_SET_DIFF = Method(
    method="invocation_set_diff",
    stage="generate",
    instruments=("semantic", "argv", "literal"),
    metrics=("f1", "recall", "precision"),
    denominator="distinct invocations v1's own enumeration produced",
)

CONFIG_ENV_DIFF = Method(
    method="config_env_diff",
    stage="generate",
    instruments=("env_request",),
    metrics=("env_agreement_rate",),
    denominator="invocations matched by invocation_set_diff",
)

TRACE_RECOVERY_DIFF = Method(
    method="trace_recovery_diff",
    stage="trace",
    instruments=("projected_fs_interactions",),
    # Micro (pooled over interactions) rather than macro (mean over configurations): named
    # in full because the two diverge sharply when one configuration has 1 projected pair
    # and another has 20, and a bare "core.f1" would hide which was meant.
    metrics=(
        "core.micro.f1",
        "core.micro.recall",
        "core.micro.precision",
        "inference.micro.f1",
        "ceiling_fraction",
    ),
    denominator="distinct (action, path) pairs surviving v1's own relevance projection",
)

ANNOTATION_DIFF = Method(
    method="annotation_diff",
    stage="annotate",
    instruments=("structural_fields", "text"),
    # No single similarity score, on purpose: a presentation difference and a
    # parallelizability-class disagreement are not interchangeable, and this stage has no
    # defensible way to weight them against each other.
    # Paths into the record, not bare names: these live under `agreement`, and a bare
    # "pclass" silently extracts nothing.
    # Rates first, counts after. An aggregation averages the leading metric across
    # commands, and `agreement.fully_agreeing` is a count of cases -- averaging "8 cases"
    # with "1 case" produces a number with no denominator behind it. The counts stay
    # available for anyone reading a single record.
    metrics=(
        "rates.fully_agreeing",
        "rates.pclass",
        "agreement.fully_agreeing",
        "agreement.pclass",
        "agreement.comparable",
    ),
    denominator="cases aligned between the two annotations",
)

MEASURED_COST = Method(
    method="measured_cost",
    stage="*",
    instruments=("openrouter_usage",),
    metrics=("cost_usd",),
    denominator="US dollars",
)

MEASURED_WALL_CLOCK = Method(
    method="measured_wall_clock",
    stage="*",
    instruments=("api_wall_clock",),
    metrics=("seconds",),
    denominator="seconds",
)

REGISTRY: dict[str, Method] = {
    m.method: m
    for m in (
        Q2_SYNTAX_DIFF,
        INVOCATION_SET_DIFF,
        CONFIG_ENV_DIFF,
        TRACE_RECOVERY_DIFF,
        ANNOTATION_DIFF,
        MEASURED_COST,
        MEASURED_WALL_CLOCK,
    )
}

#: The method whose number is the headline for each stage. A stage may emit more than one
#: (stage 2 emits both an invocation and a config comparison); this names the one a summary
#: table leads with when nothing more specific is asked for.
PRIMARY_BY_STAGE: dict[str, str] = {
    "syntax_spec": Q2_SYNTAX_DIFF.method,
    "generate": INVOCATION_SET_DIFF.method,
    "trace": TRACE_RECOVERY_DIFF.method,
    "annotate": ANNOTATION_DIFF.method,
}


def get(method: str) -> Method:
    """The registered method, or a `KeyError` naming what is available."""
    try:
        return REGISTRY[method]
    except KeyError:
        raise KeyError(
            f"unknown comparison method {method!r}; registered methods are "
            f"{', '.join(sorted(REGISTRY))}"
        ) from None


def methods_for_stage(stage: str) -> tuple[Method, ...]:
    """Every method that scores this stage, primary first."""
    primary = PRIMARY_BY_STAGE.get(stage)
    found = [m for m in REGISTRY.values() if m.stage == stage]
    found.sort(key=lambda m: (m.method != primary, m.method))
    return tuple(found)


def are_comparable(left: str, right: str) -> bool:
    """Whether two records may be aggregated together.

    Only ever true for the same method. Instruments within a method are comparable; methods
    never are. Kept as a function so the rule has one place to live.
    """
    if left == right:
        return True
    return right in get(left).blendable_with


def envelope(method: str, instrument: str, **extra: Any) -> dict[str, Any]:
    """The opening fields of every comparison record.

    Carrying `denominator` into the record itself means a number can be read correctly from
    the JSON alone, without the reader having to know which scorer produced it. `caruca_v1_commit`
    travels with every result because v1's committed artifacts predate its parallelizability
    fix and disagree with fresh output.
    """
    spec = get(method)
    if instrument not in spec.instruments:
        raise ValueError(
            f"instrument {instrument!r} is not defined for method {method!r}; "
            f"expected one of {', '.join(spec.instruments)}"
        )
    record: dict[str, Any] = {
        "method": spec.method,
        "instrument": instrument,
        "stage": spec.stage,
        "denominator": spec.denominator,
    }
    try:
        record["caruca_v1_commit"] = v1.v1_commit()
    except Exception:  # noqa: BLE001 - a missing commit must not sink a scoring run
        record["caruca_v1_commit"] = None
    record.update(extra)
    return record

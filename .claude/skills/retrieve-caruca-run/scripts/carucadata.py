# ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove
# caruca_v2 agent skill: Retrieve caruca run.
# Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
# Licensed under the PolyForm Noncommercial License 1.0.0
# https://polyformproject.org/licenses/noncommercial/1.0.0
# Noncommercial use only. Commercial use is prohibited.
# ATTRIBUTION-NOTICE:END
"""Shared readers for the caruca_v2 evaluation record.

Every path and every metric definition here is mirrored from what the execution console
reads (`console/src/data/`), so a number this library reports is the same number the
console shows at http://localhost:4317. Where the two could drift, the console is the
authority and this file is the copy — if you change a headline metric, change it there too.

Nothing here writes. Nothing here calls a model. Reading the whole record takes well under
a second, which is the point: an answer should come from the artifacts, not from a guess.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

# --------------------------------------------------------------------------------------
# Where everything lives
# --------------------------------------------------------------------------------------

# The markers that together identify caruca_v2's root and nothing else. Copied from
# console/src/data/paths.ts, including the reason `src/caruca_v2/harness` is spelled out:
# there is no top-level `harness/`, and using the task document's path as a marker makes
# every lookup walk to the filesystem root.
ROOT_MARKERS = ("pyproject.toml", "eval", "prompts", "src/caruca_v2/harness")


class RepoNotFound(Exception):
    pass


def _looks_like_root(p: Path) -> bool:
    return all((p / m).exists() for m in ROOT_MARKERS)


def repo_root(start: Path | None = None) -> Path:
    """caruca_v2's root. `CARUCA_V2_ROOT` overrides, but is still validated.

    An override pointing somewhere wrong fails loudly here rather than producing an empty
    run list later, which would read as "there are no runs".
    """
    override = os.environ.get("CARUCA_V2_ROOT")
    if override:
        p = Path(override).resolve()
        if not _looks_like_root(p):
            raise RepoNotFound(
                f"CARUCA_V2_ROOT={p} is not a caruca_v2 checkout "
                f"(expected all of: {', '.join(ROOT_MARKERS)})"
            )
        return p
    cur = (start or Path(__file__)).resolve()
    for cand in [cur, *cur.parents]:
        if cand.is_dir() and _looks_like_root(cand):
            return cand
    raise RepoNotFound(
        f"No caruca_v2 checkout found above {cur}. Set CARUCA_V2_ROOT to point at one."
    )


def v1_root() -> Path:
    """v1's checkout, which is read and run but never written into.

    Two machines are in play and neither path is canonical (`memory/dev_machine_paths.md`),
    so this resolves rather than hardcodes.
    """
    env = os.environ.get("CARUCA_V1_ROOT")
    if env:
        return Path(env).resolve()
    home = Path.home()
    for cand in (home / "dev" / "stevens" / "caruca", home / "stevens" / "caruca"):
        if (cand / "caruca").exists():
            return cand
    raise RepoNotFound(
        "No v1 checkout found. Set CARUCA_V1_ROOT to the directory containing caruca/."
    )


@dataclass(frozen=True)
class Paths:
    root: Path

    @property
    def runs(self) -> Path:
        return self.root / "eval" / "runs"

    @property
    def campaigns(self) -> Path:
        return self.root / "eval" / "campaigns"

    @property
    def parity_diffs(self) -> Path:
        return self.root / "eval" / "parity_diffs"

    @property
    def v1_configs(self) -> Path:
        return self.root / "eval" / "v1_configs"

    @property
    def metrics_db(self) -> Path:
        return self.root / "eval" / "metrics.db"

    @property
    def prompts(self) -> Path:
        return self.root / "prompts"

    @property
    def analysis(self) -> Path:
        return self.root / "ai_docs" / "analysis"

    @property
    def tasks(self) -> Path:
        return self.root / "ai_docs" / "tasks"


def paths() -> Paths:
    return Paths(repo_root())


# --------------------------------------------------------------------------------------
# Stage vocabulary
# --------------------------------------------------------------------------------------

# The pipeline's four stages, in order. The numbers are how the task documents and the
# parity diffs refer to them; the slugs are what the manifests and ledgers store.
STAGES = ("syntax_spec", "generate", "trace", "annotate")

STAGE_NUMBER = {s: i + 1 for i, s in enumerate(STAGES)}

STAGE_TITLE = {
    "syntax_spec": "Stage 1 — syntax specification",
    "generate": "Stage 2 — configuration generation",
    "trace": "Stage 3 — execution and tracing",
    "annotate": "Stage 4 — annotation",
}

# Short enough for a table column, still unambiguous.
STAGE_SHORT = {
    "syntax_spec": "1 syntax_spec",
    "generate": "2 generate",
    "trace": "3 trace",
    "annotate": "4 annotate",
}

# The campaign families, most authoritative first.
#
# This ordering exists because several commands (`cat`, `wc`) appear in both, and pooling
# them would be a denominator error of exactly the kind this project keeps catching: the
# C0 pilot ran a different, smaller design than the nine-command parity study, so a mean
# over both is a mean over two different experiments. `auto` picks one and names the other.
CAMPAIGN_FAMILIES = (
    ("p1", "the nine-command parity study"),
    ("c0", "the C0 pilot"),
)


def campaign_family(campaign_id: str) -> str:
    return campaign_id.split("_", 1)[0] if "_" in campaign_id else campaign_id

# What each stage replaces on v1's side, from the manifests' own `inputs.replaces_v1_modules`.
# Kept here as a fallback for stages where a run is absent, so the skill can still say what
# the comparison is against.
STAGE_V1_MODULES = {
    "syntax_spec": ["llm.py", "ir/syntax.py (the DSL being emitted)"],
    "generate": ["ir/string.py", "ir/environment.py", "ir/contents.py", "ir/mixin.py"],
    "trace": ["tracer/tracer.py", "tracer/strace_parser.py"],
    "annotate": ["tracer/data.py::to_annotation", "annotator/"],
}

_ALIASES = {
    "1": "syntax_spec", "s1": "syntax_spec", "stage1": "syntax_spec",
    "syntax": "syntax_spec", "syntax-spec": "syntax_spec", "spec": "syntax_spec",
    "2": "generate", "s2": "generate", "stage2": "generate",
    "gen": "generate", "config": "generate", "configs": "generate",
    "3": "trace", "s3": "trace", "stage3": "trace", "tracing": "trace",
    "4": "annotate", "s4": "annotate", "stage4": "annotate",
    "annotation": "annotate", "annot": "annotate",
}


def resolve_stage(token: str) -> str:
    """Accept a stage as a number, a slug, or the words people actually type."""
    t = token.strip().lower().replace("_", "-")
    if t in STAGES:
        return t
    t2 = t.replace("-", "_")
    if t2 in STAGES:
        return t2
    key = t.replace("-", "")
    if key in _ALIASES:
        return _ALIASES[key]
    if t in _ALIASES:
        return _ALIASES[t]
    raise ValueError(
        f"Unknown stage {token!r}. Use 1-4, or one of: {', '.join(STAGES)}"
    )


# --------------------------------------------------------------------------------------
# Headline metrics — mirrored from console/src/data/compare.ts::HEADLINE
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Headline:
    metric: str
    label: str
    denominator: str
    method: str
    # For a stage whose scorer records counts rather than a rate, the key holding the
    # denominator. Stage 4 is the case: averaging `agreement.pclass` across cells produces
    # a number that is not a rate and not anything. Where this is set, the figure is the
    # pooled numerator over the pooled denominator — "25 of 77", not the mean of nine
    # small fractions.
    denominator_metric: str | None = None


HEADLINE: dict[str, Headline] = {
    "syntax_spec": Headline(
        "f1", "flag F1", "flags in the reference specification", "q2_syntax_diff"
    ),
    "generate": Headline(
        "f1",
        "invocation F1",
        "v1's distinct invocations at the same limits",
        "invocation_set_diff",
    ),
    "trace": Headline(
        "core.micro.f1",
        "core interaction F1",
        "v1's projected filesystem interactions",
        "trace_recovery_diff",
    ),
    "annotate": Headline(
        "agreement.pclass",
        "parallelizability-class agreement",
        "aligned cases where both sides state a class",
        "annotation_diff",
        denominator_metric="agreement.comparable",
    ),
}

# Above this, v2 reproduced v1 closely enough to call it replication (compare.ts).
REPLICATES_AT = 0.9


def verdict_for(value: float | None) -> str:
    """Deliberately coarse, and deliberately not a grade.

    `improves` is absent on purpose: it is reserved for a figure better than v1's *and*
    measured against a reference that is not v1 itself, which no stage-2 or stage-3 cell
    can be. Call it by hand if a ground-truth comparison earns it.
    """
    if value is None:
        return "unscoreable"
    return "replicates" if value >= REPLICATES_AT else "diverges"


# --------------------------------------------------------------------------------------
# Runs
# --------------------------------------------------------------------------------------

RUN_DIR_RE = re.compile(r"^(?P<ts>\d{8}T\d{6}Z)_(?P<cmd>.+)_(?P<hash>[0-9a-f]{8})$")


@dataclass
class Run:
    run_id: str
    path: Path
    manifest: dict[str, Any]

    @property
    def stage(self) -> str:
        return self.manifest.get("stage", "")

    @property
    def command(self) -> str:
        return self.manifest.get("command", "")

    @property
    def status(self) -> str:
        return self.manifest.get("status", "")

    @property
    def ok(self) -> bool:
        return self.status == "ok"

    @property
    def checks(self) -> dict[str, Any]:
        return self.manifest.get("checks") or {}

    @property
    def inputs(self) -> dict[str, Any]:
        return self.manifest.get("inputs") or {}

    def outputs(self) -> list[Path]:
        """Resolve `output_paths` (repo-relative) to real files that exist."""
        root = repo_root()
        out = []
        for rel in self.manifest.get("output_paths") or []:
            p = root / rel
            if p.exists():
                out.append(p)
        return out


@dataclass
class Record:
    """The whole evaluation record, loaded once."""

    paths: Paths
    runs: list[Run]
    empty_run_dirs: list[str]
    malformed_run_dirs: list[tuple[str, str]]
    ledger_rows: list[dict[str, Any]]
    campaigns_present: list[str]
    campaigns_absent: list[str]

    # ---- selectors -------------------------------------------------------------------

    def for_command(self, command: str, stage: str | None = None) -> list[Run]:
        rs = [r for r in self.runs if r.command == command]
        if stage:
            rs = [r for r in rs if r.stage == stage]
        return sorted(rs, key=lambda r: r.run_id)

    def cells(
        self, command: str, stage: str | None = None, family: str | None = None
    ) -> list[dict[str, Any]]:
        rows = [r for r in self.ledger_rows if r.get("command") == command]
        if stage:
            rows = [r for r in rows if r.get("stage") == stage]
        if family:
            rows = [r for r in rows if campaign_family(r.get("campaign_id", "")) == family]
        return sorted(rows, key=lambda r: (r.get("campaign_id", ""), r.get("sample", 0)))

    def families_for(self, command: str, stage: str | None = None) -> list[str]:
        """Which campaign families scored this command at this stage, most authoritative first."""
        have = {campaign_family(c.get("campaign_id", "")) for c in self.cells(command, stage)}
        ordered = [f for f, _ in CAMPAIGN_FAMILIES if f in have]
        return ordered + sorted(have - set(ordered))

    def pick_family(self, command: str, stage: str | None = None) -> str | None:
        fams = self.families_for(command, stage)
        return fams[0] if fams else None

    def run_by_id(self, run_id: str) -> Run | None:
        for r in self.runs:
            if r.run_id == run_id:
                return r
        return None

    def cell_for_run(self, run_id: str) -> dict[str, Any] | None:
        for row in self.ledger_rows:
            if row.get("run_id") == run_id:
                return row
        return None

    @property
    def commands(self) -> list[str]:
        return sorted({r.command for r in self.runs if r.command})


def load_runs(p: Paths) -> tuple[list[Run], list[str], list[tuple[str, str]]]:
    """Read every run directory.

    Three outcomes, kept apart on purpose (the console makes the same distinction): a run
    with a manifest, a directory created by a run that died before writing one, and a
    manifest that will not parse. Folding the last two together would hide real corruption
    behind an ordinary crash.
    """
    runs: list[Run] = []
    empty: list[str] = []
    malformed: list[tuple[str, str]] = []
    if not p.runs.is_dir():
        return runs, empty, malformed
    for d in sorted(p.runs.iterdir()):
        if not d.is_dir():
            continue
        mf = d / "manifest.json"
        if not mf.exists():
            empty.append(d.name)
            continue
        try:
            runs.append(Run(d.name, d, json.loads(mf.read_text())))
        except (json.JSONDecodeError, OSError) as e:
            malformed.append((d.name, str(e)))
    return runs, empty, malformed


def load_ledgers(p: Paths) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    """Read every campaign ledger.

    `eval/campaigns/` is gitignored, so a fresh checkout has none. Absence is reported
    rather than treated as an empty result — "this campaign is not on this machine" and
    "this campaign scored nothing" are different facts.
    """
    rows: list[dict[str, Any]] = []
    present: list[str] = []
    known = [
        "p1_syntax_spec", "p1_generate", "p1_trace", "p1_annotate",
        "c0_syntax_spec", "c0_generate", "c0_trace", "c0_annotate",
    ]
    seen = set()
    if p.campaigns.is_dir():
        for d in sorted(p.campaigns.iterdir()):
            ledger = d / "ledger.jsonl"
            if not d.is_dir() or not ledger.exists():
                continue
            present.append(d.name)
            seen.add(d.name)
            for line in ledger.read_text().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    absent = [c for c in known if c not in seen]
    return rows, present, absent


def load_record() -> Record:
    p = paths()
    runs, empty, malformed = load_runs(p)
    rows, present, absent = load_ledgers(p)
    return Record(p, runs, empty, malformed, rows, present, absent)


# --------------------------------------------------------------------------------------
# Metrics out of ledger cells
# --------------------------------------------------------------------------------------


def flat_metrics(score: dict[str, Any] | None) -> dict[str, float]:
    """Every numeric metric in a cell's score, flattened to dotted keys.

    The ledgers already store stage-3 and stage-4 metrics dotted (`core.micro.f1`), while
    stage 2 nests `config_comparison.rates`. Flattening both ways means a caller can ask
    for any metric by the name the console shows without knowing which shape it came in.
    """
    out: dict[str, float] = {}
    if not score:
        return out

    def walk(o: Any, prefix: str) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("error", "method", "instrument", "reference", "scoreable"):
                    continue
                walk(v, f"{prefix}{k}.")
        elif isinstance(o, bool):
            return
        elif isinstance(o, (int, float)):
            out[prefix[:-1]] = float(o)

    walk(score, "")
    return out


@dataclass
class StageSummary:
    stage: str
    command: str
    headline: Headline
    value: float | None
    verdict: str
    samples: int
    scored_samples: int
    spread: float | None
    pooled: tuple[float, float] | None  # (numerator, denominator) for count-based stages
    counts: dict[str, Any] | None
    run_ids: list[str]
    campaigns: list[str]
    family: str | None = None
    other_families: list[str] = field(default_factory=list)
    #: Runs on disk at this stage that no ledger cell cites. They exist and cost money,
    #: but they are not part of the scored comparison — keeping them out of the mean while
    #: still reporting them is the difference between "3 samples" and "9 runs".
    orphan_run_ids: list[str] = field(default_factory=list)
    unscoreable_reasons: list[str] = field(default_factory=list)
    #: Cells the scorer *did* score, but where the headline metric is undefined — typically
    #: an F1 of 0/0 because nothing was recovered and nothing was produced. This is a third
    #: state, and collapsing it into either neighbour tells a lie: reporting it as
    #: unscoreable hides a comparison that ran, and reporting it as 0.0 invents a rate that
    #: the scorer explicitly declined to compute. Each entry is (sample, what is known).
    scored_but_undefined: list[tuple[Any, str]] = field(default_factory=list)
    per_sample: list[float] = field(default_factory=list)
    all_metrics: dict[str, list[float]] = field(default_factory=dict)
    cost_usd: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    wall_clock_seconds: float = 0.0


def summarize_stage(
    rec: Record, command: str, stage: str, family: str | None = "auto"
) -> StageSummary:
    """Collapse a command's samples at one stage into the figure the console shows.

    Three rules are load-bearing and easy to get wrong by hand, which is why this is a
    function rather than an instruction:

      - **One campaign family at a time.** `cat` has cells in both the C0 pilot and the
        nine-command parity study. Those are different experiments; a mean over both is a
        mean over two designs. `family="auto"` takes the most authoritative present and
        names the rest in `other_families`. Pass `None` to pool deliberately.
      - **An unscoreable cell is left out of the mean, not counted as zero.** The
        denominator is `scored_samples`, and `samples - scored_samples` is reported with
        the scorer's reason.
      - **A count-based stage is pooled, not averaged.** `agreement.pclass` counts agreeing
        cases; the summed numerator over the summed denominator is a rate, while the mean
        of the raw counts is not a rate and not anything.
    """
    hl = HEADLINE[stage]
    others: list[str] = []
    if family == "auto":
        fams = rec.families_for(command, stage)
        family = fams[0] if fams else None
        others = fams[1:]
    cells = rec.cells(command, stage, family)

    cited = {c.get("run_id") for c in cells if c.get("run_id")}
    all_runs = rec.for_command(command, stage)
    runs = [r for r in all_runs if r.run_id in cited] or (all_runs if not cited else [])
    orphans = [r.run_id for r in all_runs if r.run_id not in cited] if cited else []

    per_sample: list[float] = []
    all_metrics: dict[str, list[float]] = {}
    reasons: list[str] = []
    undefined: list[tuple[Any, str]] = []
    num = den = 0.0
    counts: dict[str, Any] | None = None

    for c in cells:
        score = c.get("score") or {}
        if not score.get("scoreable"):
            reasons.append(score.get("error") or "scorer reported not scoreable")
            continue
        m = flat_metrics(score)
        for k, v in m.items():
            all_metrics.setdefault(k, []).append(v)
        if score.get("counts") and counts is None:
            counts = score["counts"]
        if hl.denominator_metric:
            n, d = m.get(hl.metric), m.get(hl.denominator_metric)
            if n is not None and d is not None:
                num += n
                den += d
                if d:
                    per_sample.append(n / d)
            else:
                undefined.append((c.get("sample"),
                                  f"{hl.metric} or {hl.denominator_metric} not recorded"))
        else:
            v = m.get(hl.metric)
            if v is not None:
                per_sample.append(v)
            else:
                # The cell scored, but the headline is absent. Say what the neighbouring
                # metrics do show, so the reader can see it is a real zero-recovery result
                # rather than a missing run.
                near = {k: m[k] for k in sorted(m)
                        if k != hl.metric and k.rsplit(".", 1)[0] == hl.metric.rsplit(".", 1)[0]}
                detail = (", ".join(f"{k}={v:g}" for k, v in near.items())
                          or "no companion metrics recorded")
                undefined.append((c.get("sample"),
                                  f"{hl.metric} undefined (likely 0/0); {detail}"))

    if hl.denominator_metric:
        value = (num / den) if den else None
        pooled = (num, den) if den else None
    else:
        value = (sum(per_sample) / len(per_sample)) if per_sample else None
        pooled = None

    spread = (max(per_sample) - min(per_sample)) if len(per_sample) > 1 else None

    return StageSummary(
        stage=stage,
        command=command,
        headline=hl,
        value=value,
        verdict=verdict_for(value),
        samples=len(cells) or len(runs),
        scored_samples=len(per_sample),
        spread=spread,
        pooled=pooled,
        counts=counts,
        run_ids=[r.run_id for r in runs],
        campaigns=sorted({c.get("campaign_id", "") for c in cells if c.get("campaign_id")}),
        family=family,
        other_families=others,
        orphan_run_ids=orphans,
        unscoreable_reasons=reasons,
        scored_but_undefined=undefined,
        per_sample=per_sample,
        all_metrics=all_metrics,
        cost_usd=sum(float(r.manifest.get("cost_usd") or 0) for r in runs),
        prompt_tokens=sum(int(r.manifest.get("prompt_tokens") or 0) for r in runs),
        completion_tokens=sum(int(r.manifest.get("completion_tokens") or 0) for r in runs),
        wall_clock_seconds=sum(float(r.manifest.get("wall_clock_seconds") or 0) for r in runs),
    )


# --------------------------------------------------------------------------------------
# Parity diffs — the generated per-command drill-down
# --------------------------------------------------------------------------------------

_STAGE_HEADING = re.compile(r"^##\s+Stage\s+(\d)\b", re.M)


def parity_diff_path(command: str) -> Path:
    return paths().parity_diffs / f"{command}.md"


def parity_diff_sections(command: str) -> dict[str, str]:
    """Split `eval/parity_diffs/<cmd>.md` into its four stage sections.

    This file is the only place the *items* behind a number live — the actual invocation
    strings, the missing and spurious lists, the two annotators' output side by side. A
    rate tells you something diverged; this tells you what.
    """
    p = parity_diff_path(command)
    if not p.exists():
        return {}
    text = p.read_text()
    marks = [(m.start(), int(m.group(1))) for m in _STAGE_HEADING.finditer(text)]
    if not marks:
        return {"_preamble": text}
    out: dict[str, str] = {}
    if marks[0][0] > 0:
        out["_preamble"] = text[: marks[0][0]].strip()
    for i, (pos, n) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        if 1 <= n <= 4:
            out[STAGES[n - 1]] = text[pos:end].rstrip()
    return out


def available_parity_diffs() -> list[str]:
    d = paths().parity_diffs
    return sorted(f.stem for f in d.glob("*.md")) if d.is_dir() else []


# --------------------------------------------------------------------------------------
# Metrics database (per-turn cost and timing)
# --------------------------------------------------------------------------------------


def metrics_rows(command: str | None = None, stage: str | None = None) -> list[dict[str, Any]]:
    """Per-turn rows from `eval/metrics.db`.

    The database knows turns that the manifests total up, and it also knows runs whose
    directories are gone — so a count from here and a count from `eval/runs/` legitimately
    differ. Read-only, always.
    """
    db = paths().metrics_db
    if not db.exists():
        return []
    q = "SELECT * FROM runs"
    where, args = [], []
    if command:
        where.append("command = ?")
        args.append(command)
    if stage:
        where.append("stage = ?")
        args.append(stage)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY run_id, turn"
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        con.row_factory = sqlite3.Row
        return [dict(r) for r in con.execute(q, args)]
    finally:
        con.close()


# --------------------------------------------------------------------------------------
# Small formatting helpers shared by the CLIs
# --------------------------------------------------------------------------------------


def fmt(value: float | None, places: int = 3) -> str:
    return "—" if value is None else f"{value:.{places}f}"


def rule(title: str = "", width: int = 78) -> str:
    if not title:
        return "─" * width
    pad = width - len(title) - 3
    return f"── {title} " + "─" * max(pad - 3, 0)


def truncate(text: str, limit: int, note: str = "") -> str:
    if len(text) <= limit:
        return text
    tail = f"\n… [{len(text) - limit} more characters{'; ' + note if note else ''}]"
    return text[:limit] + tail


def iter_lines(block: str) -> Iterable[str]:
    for line in block.splitlines():
        yield line

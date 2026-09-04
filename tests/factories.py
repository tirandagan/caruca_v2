"""Record builders shared across test modules."""

from __future__ import annotations

from caruca_v2.telemetry import DecodingParams, TelemetryRecord


def make_record(**overrides) -> TelemetryRecord:
    fields = {
        "run_id": "2026-09-04T101530Z_mkdir_ab12",
        "command": "mkdir",
        "component": "naive_llm",
        "condition": "plain",
        "stage": "syntax_spec",
        "model_id": "openai/gpt-4o",
        "prompt_tokens": 6842,
        "completion_tokens": 1103,
        "cost_usd": 0.0213,
        "wall_clock_seconds": 14.2,
        "seed": 42,
        "prompt_hash": "a" * 64,
        "timestamp": "2026-09-04T10:15:30Z",
        "decoding_params": DecodingParams(temperature=0.0, max_tokens=4096),
    }
    fields.update(overrides)
    return TelemetryRecord(**fields)

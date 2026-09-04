"""The OpenRouter client.

One gateway, one key, one code path for every candidate model, so cross-model comparison
does not vary the plumbing along with the model. Task 003 grows a tool loop on top of
this module; `complete()` stays the plain single-call path the naive baseline needs.

There is deliberately no retry-on-bad-output anywhere: a malformed or invalid response is
a measurement of the baseline, and re-asking would quietly turn a weak control into a
tuned one (`memory/caruca_v2_baseline_scope.md`).
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from openai import OpenAI

from .errors import LLMError, SetupError

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
API_KEY_VAR = "OPENROUTER_API_KEY"

# v1's values (`llm.py:109-114`), kept for parity. `max_tokens` truncates option-heavy
# commands exactly as it did for v1; that truncation is recorded, not worked around.
DEFAULT_MAX_TOKENS = 4096
DEFAULT_SEED = 42

# Models that do not honor `seed`. The parameter is still sent and still recorded; the
# manifest carries `seed_honored: false` so a reader is not misled into thinking a run
# was seeded when the provider ignored it.
SEEDLESS_MODEL_PREFIXES = ("anthropic/", "google/")

# `openai/gpt-4o` must resolve to OpenAI's own endpoint: the paper's numbers are GPT-4o
# numbers, and a fallback provider would silently change what is being compared.
PINNED_PROVIDERS: dict[str, str] = {"openai/gpt-4o": "OpenAI"}


def seed_is_honored(model: str) -> bool:
    return not model.startswith(SEEDLESS_MODEL_PREFIXES)


def build_client(api_key: str | None = None) -> OpenAI:
    """An OpenAI SDK client pointed at OpenRouter. Fails at startup, not mid-run."""
    key = api_key or os.environ.get(API_KEY_VAR)
    if not key:
        raise SetupError(
            f"No OpenRouter API key. Set {API_KEY_VAR} in the environment or in .env "
            "(see .env.example)."
        )
    return OpenAI(api_key=key, base_url=OPENROUTER_BASE_URL)


@dataclass(frozen=True)
class LLMResponse:
    """One completed model call, with the measurements the telemetry record needs.

    `model_reported` is what OpenRouter says it actually served, which can differ from
    what was requested; both are recorded so the distinction survives into the write-up.
    """

    text: str
    model_requested: str
    model_reported: str
    provider: str | None
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    wall_clock_seconds: float
    finish_reason: str | None
    message: dict[str, Any]
    raw_usage: dict[str, Any]


def _provider_body(model: str, provider: str | None) -> dict[str, Any]:
    chosen = provider or PINNED_PROVIDERS.get(model)
    if chosen is None:
        return {}
    return {"provider": {"order": [chosen], "allow_fallbacks": False}}


def _usage_field(usage: dict[str, Any], *names: str) -> Any:
    for name in names:
        if usage.get(name) is not None:
            return usage[name]
    raise LLMError(
        f"OpenRouter response carried no {names[0]!r} in its usage block: {usage}. "
        "Telemetry cannot be completed from this response, and estimating it would "
        "invalidate the cost comparison."
    )


def complete(
    messages: list[dict[str, Any]],
    *,
    model: str,
    seed: int | None,
    temperature: float,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    response_format: dict[str, Any] | None = None,
    tools: list[dict[str, Any]] | None = None,
    provider: str | None = None,
    client: OpenAI | None = None,
) -> LLMResponse:
    """Make exactly one model call and measure it.

    Wall-clock brackets the API call only, so process startup and file I/O never inflate
    a latency number.
    """
    active = client or build_client()

    extra_body: dict[str, Any] = {"usage": {"include": True}}
    extra_body.update(_provider_body(model, provider))

    request: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "extra_body": extra_body,
    }
    if seed is not None:
        request["seed"] = seed
    if response_format is not None:
        request["response_format"] = response_format
    if tools:
        request["tools"] = tools

    started = time.perf_counter()
    completion = active.chat.completions.create(**request)
    wall_clock = time.perf_counter() - started

    if not completion.choices:
        raise LLMError(f"OpenRouter returned no choices for model {model!r}.")

    choice = completion.choices[0]
    usage = completion.usage.model_dump() if completion.usage else {}
    if not usage:
        raise LLMError(
            f"OpenRouter returned no usage block for model {model!r}; token counts and "
            "cost are required and are never estimated."
        )

    return LLMResponse(
        text=choice.message.content or "",
        model_requested=model,
        model_reported=completion.model or model,
        provider=getattr(completion, "provider", None),
        prompt_tokens=int(_usage_field(usage, "prompt_tokens", "input_tokens")),
        completion_tokens=int(_usage_field(usage, "completion_tokens", "output_tokens")),
        cost_usd=float(_usage_field(usage, "cost")),
        wall_clock_seconds=wall_clock,
        finish_reason=choice.finish_reason,
        message=choice.message.model_dump(),
        raw_usage=usage,
    )


# The only continuation this project sends. It asks for more of the same output and
# nothing else -- no hints, no corrections, no restatement of the task.
CONTINUE_INSTRUCTION = (
    "Continue from exactly where you stopped. Same format, no repetition, no commentary."
)


def complete_series(
    messages: list[dict[str, Any]],
    *,
    model: str,
    temperature: float,
    seed: int | None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    max_turns: int = 1,
    provider: str | None = None,
    client: OpenAI | None = None,
) -> list[LLMResponse]:
    """Call the model, continuing only while the token cap is what stopped it.

    A model that finishes early has finished: it is never nudged for more. Continuation
    exists solely because a stage's output can be longer than one response, and a
    length-truncated answer measures the cap rather than the model. Every turn is returned
    so each can be recorded separately.
    """
    if max_turns < 1:
        raise LLMError(f"max_turns must be at least 1, got {max_turns}.")

    active = client or build_client()
    conversation = list(messages)
    responses: list[LLMResponse] = []

    for _ in range(max_turns):
        response = complete(
            conversation,
            model=model,
            seed=seed,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=provider,
            client=active,
        )
        responses.append(response)

        if response.finish_reason != "length":
            break

        conversation.append({"role": "assistant", "content": response.text})
        conversation.append({"role": "user", "content": CONTINUE_INSTRUCTION})

    return responses


@dataclass
class ToolLoopResult:
    """One agent session: every model turn, and the conversation it produced."""

    responses: list[LLMResponse]
    messages: list[dict[str, Any]]
    stop_reason: str

    @property
    def turns(self) -> int:
        return len(self.responses)


def run_tool_loop(
    messages: list[dict[str, Any]],
    *,
    model: str,
    temperature: float,
    seed: int | None,
    tools: list[dict[str, Any]],
    execute: Callable[[str, dict[str, Any]], str],
    is_finished: Callable[[], bool],
    max_tokens: int = DEFAULT_MAX_TOKENS,
    max_turns: int = 15,
    provider: str | None = None,
    client: OpenAI | None = None,
) -> ToolLoopResult:
    """Send, execute the tool calls that come back, append the results, repeat.

    The whole engine, deliberately: no framework, so every message is ours to log and
    count, and the loop behaves identically for every model behind the one gateway.

    It stops when the caller says the work is finished, when the model replies without
    calling a tool, or at the turn cap. Hitting the cap is recorded rather than raised —
    a model that never finishes is a result about the approach.
    """
    if max_turns < 1:
        raise LLMError(f"max_turns must be at least 1, got {max_turns}.")

    active = client or build_client()
    conversation = list(messages)
    responses: list[LLMResponse] = []
    stop_reason = "turn_cap"

    for _ in range(max_turns):
        response = complete(
            conversation,
            model=model,
            seed=seed,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            provider=provider,
            client=active,
        )
        responses.append(response)
        conversation.append(response.message)

        tool_calls = response.message.get("tool_calls") or []
        if not tool_calls:
            stop_reason = "no_tool_calls"
            break

        for call in tool_calls:
            function = call["function"]
            try:
                arguments = json.loads(function.get("arguments") or "{}")
            except json.JSONDecodeError as exc:
                arguments = {}
                content = json.dumps({"error": f"arguments were not valid JSON: {exc}"})
            else:
                content = execute(function["name"], arguments)
            conversation.append(
                {"role": "tool", "tool_call_id": call["id"], "content": content}
            )

        if is_finished():
            stop_reason = "finished"
            break

    return ToolLoopResult(responses=responses, messages=conversation, stop_reason=stop_reason)

"""Stand-ins for the OpenAI SDK surface `llm.py` touches.

Hand-written rather than `unittest.mock`: the point is to pin down exactly which
attributes the client contract depends on, so an SDK change fails loudly here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class FakeMessage:
    content: str | None
    role: str = "assistant"
    tool_calls: list[dict[str, Any]] | None = None

    def model_dump(self) -> dict[str, Any]:
        dumped: dict[str, Any] = {"role": self.role, "content": self.content}
        if self.tool_calls is not None:
            dumped["tool_calls"] = self.tool_calls
        return dumped


@dataclass
class FakeChoice:
    message: FakeMessage
    finish_reason: str = "stop"


@dataclass
class FakeUsage:
    prompt_tokens: int = 6842
    completion_tokens: int = 1103
    cost: float = 0.0213

    def model_dump(self) -> dict[str, Any]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens,
            "cost": self.cost,
        }


@dataclass
class FakeCompletion:
    choices: list[FakeChoice]
    usage: FakeUsage | None
    model: str = "openai/gpt-4o"
    provider: str = "OpenAI"


@dataclass
class FakeCompletions:
    response_text: str
    finish_reason: str = "stop"
    usage: FakeUsage | None = field(default_factory=FakeUsage)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def create(self, **kwargs: Any) -> FakeCompletion:
        self.calls.append(kwargs)
        return FakeCompletion(
            choices=[
                FakeChoice(
                    message=FakeMessage(content=self.response_text),
                    finish_reason=self.finish_reason,
                )
            ],
            usage=self.usage,
        )


class FakeClient:
    """Stands in for `openai.OpenAI`, recording every request it is handed."""

    def __init__(self, response_text: str, **kwargs: Any) -> None:
        self.chat = type("Chat", (), {})()
        self.chat.completions = FakeCompletions(response_text=response_text, **kwargs)

    @property
    def calls(self) -> list[dict[str, Any]]:
        return self.chat.completions.calls


def tool_call(name: str, arguments: dict[str, Any], call_id: str = "call_1") -> dict[str, Any]:
    """One tool call in the shape the OpenAI wire format uses."""
    return {
        "id": call_id,
        "type": "function",
        "function": {"name": name, "arguments": json.dumps(arguments)},
    }


@dataclass
class ScriptedCompletions:
    """Replays a fixed list of turns, so a multi-turn session has a known transcript.

    Each turn is either a string (plain assistant text) or a list of tool calls. The
    script cycles, so a stage that opens one session per configuration replays the same
    transcript for each of them.
    """

    turns: list[Any]
    usage: FakeUsage = field(default_factory=FakeUsage)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def create(self, **kwargs: Any) -> FakeCompletion:
        index = len(self.calls) % len(self.turns)
        self.calls.append(kwargs)
        turn = self.turns[index]

        if isinstance(turn, str):
            message = FakeMessage(content=turn)
            finish_reason = "stop"
        else:
            message = FakeMessage(content=None, tool_calls=list(turn))
            finish_reason = "tool_calls"

        return FakeCompletion(
            choices=[FakeChoice(message=message, finish_reason=finish_reason)],
            usage=self.usage,
        )


class ScriptedClient:
    """A FakeClient whose responses follow a scripted multi-turn transcript."""

    def __init__(self, turns: list[Any]) -> None:
        self.chat = type("Chat", (), {})()
        self.chat.completions = ScriptedCompletions(turns=turns)

    @property
    def calls(self) -> list[dict[str, Any]]:
        return self.chat.completions.calls

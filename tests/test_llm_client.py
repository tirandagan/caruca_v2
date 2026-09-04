"""The OpenRouter call: what gets sent, and what counts as an unusable response."""

from __future__ import annotations

import pytest

from caruca_v2 import llm
from caruca_v2.errors import LLMError, SetupError
from fakes import FakeClient


def call(client: FakeClient, **overrides):
    kwargs = {"model": "anthropic/claude-sonnet-4", "seed": 42, "temperature": 0.0}
    kwargs.update(overrides)
    return llm.complete([{"role": "user", "content": "hi"}], client=client, **kwargs)


def test_missing_api_key_names_the_variable(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(SetupError) as excinfo:
        llm.build_client()
    assert "OPENROUTER_API_KEY" in str(excinfo.value)


def test_request_carries_v1s_parameters_and_usage_accounting():
    client = FakeClient("ok")
    call(client, max_tokens=llm.DEFAULT_MAX_TOKENS)

    request = client.calls[0]
    assert request["seed"] == 42
    assert request["temperature"] == 0.0
    assert request["max_tokens"] == 4096
    assert request["extra_body"]["usage"] == {"include": True}


def test_gpt_4o_routing_is_pinned_to_openai():
    client = FakeClient("ok")
    call(client, model="openai/gpt-4o")

    provider = client.calls[0]["extra_body"]["provider"]
    assert provider == {"order": ["OpenAI"], "allow_fallbacks": False}


def test_other_models_are_unpinned_unless_asked():
    client = FakeClient("ok")
    call(client)
    assert "provider" not in client.calls[0]["extra_body"]

    explicit = FakeClient("ok")
    call(explicit, provider="Anthropic")
    assert explicit.calls[0]["extra_body"]["provider"]["order"] == ["Anthropic"]


def test_measurements_come_from_the_response_not_from_estimates():
    response = call(FakeClient("ok"))

    assert response.prompt_tokens == 6842
    assert response.completion_tokens == 1103
    assert response.cost_usd == 0.0213
    assert response.wall_clock_seconds > 0
    assert response.model_reported == "openai/gpt-4o"


def test_a_response_without_usage_is_an_error_not_a_zero():
    with pytest.raises(LLMError) as excinfo:
        call(FakeClient("ok", usage=None))
    assert "usage" in str(excinfo.value)


def test_seed_support_is_declared_per_model_family():
    assert llm.seed_is_honored("openai/gpt-4o")
    assert not llm.seed_is_honored("anthropic/claude-sonnet-4")

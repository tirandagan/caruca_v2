"""Error types. Every failure names the thing that was missing or wrong.

No error here is ever recovered from by retrying an LLM call: the naive baseline's
guardrail forbids a retry loop, so a bad model response is recorded as a result
(see `stages/syntax_spec.py`) rather than raised.
"""


class CarucaV2Error(Exception):
    """Base class for every caruca_v2 failure."""


class SetupError(CarucaV2Error):
    """The environment is not configured: missing API key, missing v1 checkout."""


class V1AccessError(CarucaV2Error):
    """Something expected inside the v1 checkout could not be read."""


class PromptError(CarucaV2Error):
    """A prompt file is missing, or a placeholder was left unsubstituted."""


class LLMError(CarucaV2Error):
    """The model call failed at transport level, or returned an unusable envelope."""

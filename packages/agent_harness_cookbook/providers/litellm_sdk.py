from __future__ import annotations

import os
from typing import Any


class LiteLLMSDKModel:
    """Embedded LiteLLM Python SDK adapter.

    LiteLLM is imported lazily so mock mode still works in minimal environments.
    """

    def __init__(self, model: str | None = None, timeout: float = 60.0) -> None:
        self.model = model or os.getenv("AHC_MODEL", "openai/gpt-4o-mini")
        self.timeout = timeout

    def complete(self, prompt: str) -> dict[str, object]:
        try:
            import litellm
            from litellm import completion
        except ImportError as exc:
            raise RuntimeError(
                "LiteLLM is not installed. Run `pip install -e .` or `pip install litellm`."
            ) from exc
        litellm.drop_params = os.getenv("AHC_LITELLM_DROP_PARAMS", "true").lower() == "true"

        completion_kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You classify generic service-incident requests. "
                        "Return a short operational summary."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": float(os.getenv("AHC_TEMPERATURE", "0")),
            "max_tokens": int(os.getenv("AHC_MAX_TOKENS", "180")),
            "timeout": self.timeout,
        }
        if reasoning_effort := os.getenv("AHC_REASONING_EFFORT"):
            completion_kwargs["reasoning_effort"] = reasoning_effort
        if top_p := os.getenv("AHC_TOP_P"):
            completion_kwargs["top_p"] = float(top_p)

        response = completion(**completion_kwargs)
        content = _extract_content(response)
        total_tokens = _extract_total_tokens(response)
        return {
            "intent": "investigate",
            "summary": content,
            "tokens": total_tokens,
            "provider": "litellm",
            "model": self.model,
        }


def _extract_content(response: Any) -> str:
    try:
        return str(response.choices[0].message.content)
    except (AttributeError, IndexError):
        return str(response["choices"][0]["message"]["content"])


def _extract_total_tokens(response: Any) -> int:
    usage = getattr(response, "usage", None)
    if usage is not None:
        total = getattr(usage, "total_tokens", None)
        if total is not None:
            return int(total)
    if isinstance(response, dict):
        return int((response.get("usage") or {}).get("total_tokens") or 180)
    return 180

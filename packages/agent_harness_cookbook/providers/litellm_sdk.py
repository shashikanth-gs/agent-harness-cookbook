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
            from litellm import completion
        except ImportError as exc:
            raise RuntimeError(
                "LiteLLM is not installed. Run `pip install -e .` or `pip install litellm`."
            ) from exc

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You classify generic service-incident requests. "
                        "Return a short operational summary."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=180,
            timeout=self.timeout,
        )
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

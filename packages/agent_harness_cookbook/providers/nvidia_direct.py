from __future__ import annotations

import os
from typing import Any

import requests


class NvidiaDirectChatModel:
    """Direct NVIDIA NIM chat-completions adapter using the OpenAI-compatible API."""

    def __init__(
        self,
        model: str | None = None,
        invoke_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.model = model or os.getenv("AHC_MODEL", "mistralai/mistral-small-4-119b-2603")
        self.invoke_url = invoke_url or os.getenv(
            "NVIDIA_NIM_INVOKE_URL",
            "https://integrate.api.nvidia.com/v1/chat/completions",
        )
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY") or os.getenv("NVIDIA_NIM_API_KEY")
        self.timeout = timeout
        if not self.api_key:
            raise RuntimeError("Set NVIDIA_API_KEY or NVIDIA_NIM_API_KEY for nvidia_direct provider mode.")

    def complete(self, prompt: str) -> dict[str, object]:
        payload: dict[str, Any] = {
            "model": self.model,
            "reasoning_effort": os.getenv("AHC_REASONING_EFFORT", "high"),
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You classify generic service-incident requests. "
                        "Return a concise operational summary."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": int(os.getenv("AHC_MAX_TOKENS", "512")),
            "temperature": float(os.getenv("AHC_TEMPERATURE", "0.10")),
            "top_p": float(os.getenv("AHC_TOP_P", "1.00")),
            "stream": False,
        }
        response = requests.post(
            self.invoke_url,
            headers={"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"},
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        body = response.json()
        usage = body.get("usage") or {}
        message = body["choices"][0].get("message", {})
        return {
            "intent": "investigate",
            "summary": _visible_content(message),
            "tokens": int(usage.get("total_tokens") or usage.get("completion_tokens") or 180),
            "provider": "nvidia_direct",
            "model": self.model,
            "endpoint": self.invoke_url,
        }


def _visible_content(message: dict[str, Any]) -> str:
    content = message.get("content")
    if not content:
        return "Provider returned no visible message content."
    return str(content).removeprefix("[THINK]").strip()

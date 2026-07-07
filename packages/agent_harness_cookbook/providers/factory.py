from __future__ import annotations

import os
from typing import Protocol

from dotenv import load_dotenv

from agent_harness_cookbook.providers.litellm_sdk import LiteLLMSDKModel
from agent_harness_cookbook.providers.mock_model import MockModel


class ModelProvider(Protocol):
    def complete(self, prompt: str) -> dict[str, object]:
        ...


def get_model_provider(provider: str | None = None) -> ModelProvider:
    load_dotenv()
    selected = (provider or os.getenv("AHC_PROVIDER", "mock")).lower()
    if selected == "mock":
        return MockModel()
    if selected == "litellm":
        return LiteLLMSDKModel()
    raise ValueError(f"unknown provider: {selected}")

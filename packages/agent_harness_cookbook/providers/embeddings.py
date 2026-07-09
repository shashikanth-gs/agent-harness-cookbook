from __future__ import annotations

import math
import os
from typing import Protocol


class EmbeddingProvider(Protocol):
    def embed_query(self, text: str) -> list[float]:
        ...

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        ...


class MockEmbeddingModel:
    """Deterministic bag-of-terms embeddings for no-key tests."""

    vocabulary = ["order", "orders", "api", "field", "required", "payment", "details", "deleted", "policy"]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def _embed(self, text: str) -> list[float]:
        lowered = text.lower()
        return [float(lowered.count(term)) for term in self.vocabulary]


class LiteLLMEmbeddingModel:
    """LiteLLM embedding adapter with NVIDIA NIM defaults."""

    def __init__(self, model: str | None = None, timeout: float = 60.0) -> None:
        self.model = model or os.getenv("AHC_EMBEDDING_MODEL", "nvidia_nim/nvidia/nv-embedqa-e5-v5")
        self.timeout = timeout

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text], input_type="query")[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts, input_type="passage")

    def _embed(self, texts: list[str], input_type: str) -> list[list[float]]:
        try:
            from litellm import embedding
        except ImportError as exc:
            raise RuntimeError("LiteLLM is not installed. Run `pip install -e .`.") from exc

        response = embedding(
            model=self.model,
            input=texts,
            encoding_format="float",
            input_type=input_type,
            timeout=self.timeout,
        )
        vectors: list[list[float]] = []
        for item in response.data:
            vector = item["embedding"] if isinstance(item, dict) else item.embedding
            vectors.append([float(value) for value in vector])
        return vectors


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right, strict=False))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def get_embedding_provider(provider: str | None = None) -> EmbeddingProvider:
    selected = (provider or os.getenv("AHC_EMBEDDING_PROVIDER", os.getenv("AHC_PROVIDER", "mock"))).lower()
    if selected == "mock":
        return MockEmbeddingModel()
    if selected == "litellm":
        return LiteLLMEmbeddingModel()
    raise ValueError(f"unknown embedding provider: {selected}")

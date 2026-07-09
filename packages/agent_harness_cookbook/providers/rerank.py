from __future__ import annotations

import os
from typing import Protocol


class RerankProvider(Protocol):
    def rerank(self, query: str, documents: list[dict[str, object]]) -> list[dict[str, object]]:
        ...


class MockReranker:
    """Deterministic reranker for local demos and CI."""

    def rerank(self, query: str, documents: list[dict[str, object]]) -> list[dict[str, object]]:
        terms = {term.lower().strip("/{}.,") for term in query.split() if len(term) > 2}
        reranked = []
        for document in documents:
            text = f"{document.get('title', '')} {document.get('content', '')}".lower()
            lexical_score = sum(1 for term in terms if term in text)
            copy = dict(document)
            copy["rerank_score"] = lexical_score
            reranked.append(copy)
        return sorted(reranked, key=lambda item: int(item["rerank_score"]), reverse=True)


class LiteLLMReranker:
    """Optional LiteLLM rerank adapter.

    This is not enabled by default because provider rerank endpoints differ.
    """

    def __init__(self, model: str | None = None, timeout: float = 60.0) -> None:
        self.model = model or os.getenv("AHC_RERANK_MODEL", "nvidia/llama-nemotron-rerank-1b-v2")
        self.timeout = timeout

    def rerank(self, query: str, documents: list[dict[str, object]]) -> list[dict[str, object]]:
        try:
            from litellm import rerank
        except ImportError as exc:
            raise RuntimeError("LiteLLM is not installed. Run `pip install -e .`.") from exc
        response = rerank(
            model=self.model,
            query=query,
            documents=[str(document.get("content", "")) for document in documents],
            timeout=self.timeout,
        )
        results = getattr(response, "results", None) or response.get("results", [])
        ranked = []
        for result in results:
            index = result["index"] if isinstance(result, dict) else result.index
            score = result["relevance_score"] if isinstance(result, dict) else result.relevance_score
            copy = dict(documents[index])
            copy["rerank_score"] = float(score)
            ranked.append(copy)
        return ranked


def get_reranker(provider: str | None = None) -> RerankProvider | None:
    selected = (provider or os.getenv("AHC_RERANK_PROVIDER", "mock")).lower()
    if selected in {"none", "disabled"}:
        return None
    if selected == "mock":
        return MockReranker()
    if selected == "litellm":
        return LiteLLMReranker()
    raise ValueError(f"unknown rerank provider: {selected}")

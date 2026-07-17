"""RAG governance demo showing access control and provenance.

This scenario is one illustrative use case. See docs/use-case-scenarios.md
for how RAG access control applies across domains.
"""

from __future__ import annotations

from typing import Any

from agent_harness_cookbook.providers.embeddings import EmbeddingProvider, cosine_similarity, get_embedding_provider
from agent_harness_cookbook.providers.rerank import RerankProvider, get_reranker
from pattern_rag_access_control_and_provenance import RetrievalRequest, load_documents, synthesize_answer


def run_rag_governance_demo(
    query: str,
    tenant: str = "retail",
    user_roles: list[str] | None = None,
    domain: str = "orders",
    embeddings: EmbeddingProvider | None = None,
    reranker: RerankProvider | None = None,
) -> dict[str, Any]:
    user_roles = user_roles or ["support"]
    embeddings = embeddings or get_embedding_provider()
    reranker = reranker if reranker is not None else get_reranker()
    request = RetrievalRequest(query=query, tenant=tenant, user_roles=user_roles, domain=domain)
    docs = load_documents()
    authorized_docs = [
        doc
        for doc in docs
        if doc.tenant == request.tenant
        and doc.domain == request.domain
        and doc.lifecycle == "active"
        and not set(doc.acl).isdisjoint(request.user_roles)
    ]
    query_vector = embeddings.embed_query(query)
    doc_vectors = embeddings.embed_documents([f"{doc.title}\n{doc.content}" for doc in authorized_docs])
    ranked = sorted(
        [
            {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "content": doc.content,
                "provenance": {
                    "tenant": doc.tenant,
                    "domain": doc.domain,
                    "lifecycle": doc.lifecycle,
                    "acl_checked": True,
                },
                "score": cosine_similarity(query_vector, vector),
            }
            for doc, vector in zip(authorized_docs, doc_vectors, strict=False)
        ],
        key=lambda item: float(item["score"]),
        reverse=True,
    )
    if reranker:
        ranked = reranker.rerank(query, ranked)
    return {
        "retrieval": ranked,
        "answer": synthesize_answer(query, ranked),
        "embedding_provider": embeddings.__class__.__name__,
        "rerank_provider": reranker.__class__.__name__ if reranker else None,
        "embedding_dimensions": len(query_vector),
    }

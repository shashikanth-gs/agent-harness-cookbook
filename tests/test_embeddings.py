from agent_harness_cookbook.demos.rag_governance import run_rag_governance_demo
from agent_harness_cookbook.providers.embeddings import MockEmbeddingModel, cosine_similarity


def test_mock_embedding_similarity_prefers_related_text() -> None:
    model = MockEmbeddingModel()
    query = model.embed_query("order api required field")
    related = model.embed_documents(["Orders API required field order_id"])[0]
    unrelated = model.embed_documents(["Payment settlement batch"])[0]
    assert cosine_similarity(query, related) > cosine_similarity(query, unrelated)


def test_rag_governance_demo_uses_embeddings_and_acl() -> None:
    result = run_rag_governance_demo(
        "Which API retrieves order details and what field is required?",
        embeddings=MockEmbeddingModel(),
    )
    assert result["embedding_provider"] == "MockEmbeddingModel"
    assert result["rerank_provider"] == "MockReranker"
    assert result["embedding_dimensions"] > 0
    assert result["retrieval"][0]["doc_id"] == "orders-api-active"
    assert result["answer"]["citation_valid"] is True

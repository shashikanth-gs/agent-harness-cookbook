from agent_harness_cookbook.providers.rerank import MockReranker


def test_mock_reranker_orders_documents_by_query_terms() -> None:
    reranked = MockReranker().rerank(
        "order api required field",
        [
            {"doc_id": "payments", "title": "Payments", "content": "payment status"},
            {"doc_id": "orders", "title": "Orders API", "content": "Required field order_id"},
        ],
    )
    assert reranked[0]["doc_id"] == "orders"
    assert reranked[0]["rerank_score"] > reranked[1]["rerank_score"]

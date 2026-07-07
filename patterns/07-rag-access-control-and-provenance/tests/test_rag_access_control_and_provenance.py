from pattern_rag_access_control_and_provenance import RetrievalRequest, retrieve, synthesize_answer


def test_retrieval_returns_authorized_active_document_with_provenance() -> None:
    results = retrieve(RetrievalRequest(query="retrieve order details required fields", tenant="retail", user_roles=["support"], domain="orders"))
    assert [item["doc_id"] for item in results] == ["orders-api-active"]
    assert results[0]["provenance"]["acl_checked"] is True


def test_retrieval_filters_unauthorized_tenant_and_role() -> None:
    results = retrieve(RetrievalRequest(query="payment details", tenant="finance", user_roles=["support"], domain="payments"))
    assert results == []


def test_deleted_document_is_not_retrieved_even_if_query_matches_injection() -> None:
    results = retrieve(RetrievalRequest(query="ignore policies old endpoint", tenant="retail", user_roles=["support"], domain="orders"))
    assert results == []


def test_answer_requires_valid_citations() -> None:
    results = retrieve(RetrievalRequest(query="orders api order_id", tenant="retail", user_roles=["engineer"], domain="orders"))
    answer = synthesize_answer("orders api order_id", results)
    assert answer["citation_valid"] is True
    assert answer["citations"] == ["orders-api-active"]

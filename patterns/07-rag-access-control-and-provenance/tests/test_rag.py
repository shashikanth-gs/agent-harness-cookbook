import pytest
from agent_harness_cookbook.harness.rag_governance import (
    ReBACPolicy,
    RetrievedDocument,
    RetrievalAuthorizer,
    ProvenanceTracker,
)

def test_retrieval_authorizer():
    policy = ReBACPolicy(
        user_id="user123",
        roles=["responder"],
        allowed_classifications=["public", "internal"],
        incident_scope="INC-001"
    )
    
    docs = [
        RetrievedDocument("doc1", "content 1", "public", "uri1", {"incident_id": "INC-001"}),
        RetrievedDocument("doc2", "content 2", "top-secret", "uri2", {"incident_id": "INC-001"}),
        RetrievedDocument("doc3", "content 3", "internal", "uri3", {"incident_id": "INC-002"}), # Wrong incident
    ]
    
    authorizer = RetrievalAuthorizer(policy)
    filtered = authorizer.filter_documents(docs)
    
    assert len(filtered) == 1
    assert filtered[0].doc_id == "doc1"

def test_provenance_tracker():
    tracker = ProvenanceTracker(secret_key="my-secret-key")
    doc = RetrievedDocument("doc1", "This is some content", "public", "uri1", {})
    
    signed_doc = tracker.sign_document(doc)
    assert signed_doc.provenance_signature is not None
    
    assert tracker.verify_citation("doc1", "This is some content", signed_doc.provenance_signature) is True
    assert tracker.verify_citation("doc1", "Hallucinated content", signed_doc.provenance_signature) is False

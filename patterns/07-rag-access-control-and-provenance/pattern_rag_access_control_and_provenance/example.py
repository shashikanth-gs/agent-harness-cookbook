from __future__ import annotations

from agent_harness_cookbook.harness.rag_governance import (
    ReBACPolicy,
    RetrievedDocument,
    RetrievalAuthorizer,
    ProvenanceTracker,
)

def run_example():
    print("--- Pattern 07: RAG Access Control & Provenance Example ---\\n")
    
    # 1. ReBAC Enforcement
    policy = ReBACPolicy(
        user_id="user123",
        roles=["responder"],
        allowed_classifications=["public", "internal-runbook"],
        incident_scope="INC-001"
    )
    authorizer = RetrievalAuthorizer(policy)
    
    docs = [
        RetrievedDocument("doc1", "Server restart guide", "internal-runbook", "uri1", {"incident_id": "INC-001"}),
        RetrievedDocument("doc2", "Customer PII data", "restricted-pii", "uri2", {"incident_id": "INC-001"}),
        RetrievedDocument("doc3", "INC-002 logs", "internal-runbook", "uri3", {"incident_id": "INC-002"}),
    ]
    
    print("Filtering documents based on ReBAC policy...")
    filtered = authorizer.filter_documents(docs)
    for d in filtered:
        print(f"Authorized Document: {d.doc_id} ({d.classification})")
    print()
    
    # 2. Provenance Tracking
    print("Signing document chunks for provenance tracking...")
    tracker = ProvenanceTracker("enterprise-secret-key-123")
    signed_doc = tracker.sign_document(filtered[0])
    
    print(f"Signature generated: {signed_doc.provenance_signature}")
    
    # Agent tries to cite it
    is_valid = tracker.verify_citation(signed_doc.doc_id, signed_doc.content, signed_doc.provenance_signature)
    print(f"Citation verification (Valid Chunk): {is_valid}")
    
    is_forged = tracker.verify_citation(signed_doc.doc_id, "I made this up", signed_doc.provenance_signature)
    print(f"Citation verification (Hallucinated Chunk): {is_forged}")

if __name__ == "__main__":
    run_example()

from __future__ import annotations

import hashlib
import json
import secrets
from dataclasses import dataclass
from typing import Any

@dataclass
class ReBACPolicy:
    """Relationship-Based Access Control configuration."""
    user_id: str
    roles: list[str]
    allowed_classifications: list[str]
    incident_scope: str | None = None

@dataclass
class RetrievedDocument:
    doc_id: str
    content: str
    classification: str
    source_uri: str
    metadata: dict[str, Any]
    provenance_signature: str | None = None

class RetrievalAuthorizer:
    """
    Enforces document-level security by intercepting RAG queries and applying ReBAC filters.
    """
    def __init__(self, policy: ReBACPolicy) -> None:
        self.policy = policy

    def filter_documents(self, documents: list[RetrievedDocument]) -> list[RetrievedDocument]:
        """Filters retrieved documents based on the user's ReBAC policy."""
        authorized_docs = []
        for doc in documents:
            # Check classification
            if doc.classification not in self.policy.allowed_classifications:
                continue
            
            # Check incident scope bounds (e.g. user can only see docs related to their incident)
            if self.policy.incident_scope:
                doc_incident = doc.metadata.get("incident_id")
                if doc_incident and doc_incident != self.policy.incident_scope:
                    continue
                    
            authorized_docs.append(doc)
            
        return authorized_docs

class ProvenanceTracker:
    """
    Enforces citation and metadata tracking, generating cryptographic signatures for chunks
    to prevent agent hallucination of source materials.
    """
    def __init__(self, secret_key: str) -> None:
        self._secret_key = secret_key

    def _generate_signature(self, doc_id: str, content: str) -> str:
        """Generates a cryptographic signature for a document chunk."""
        payload = f"{doc_id}:{content}:{self._secret_key}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def sign_document(self, doc: RetrievedDocument) -> RetrievedDocument:
        """Appends a provenance signature to a document before sending to the agent."""
        doc.provenance_signature = self._generate_signature(doc.doc_id, doc.content)
        return doc

    def verify_citation(self, doc_id: str, content_snippet: str, signature: str) -> bool:
        """
        Verifies that an agent's citation matches a legitimate source chunk.
        This prevents the LLM from inventing fake references.
        """
        expected_sig = self._generate_signature(doc_id, content_snippet)
        return secrets.compare_digest(expected_sig, signature)

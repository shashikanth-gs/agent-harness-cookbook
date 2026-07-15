from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from agent_harness_cookbook.harness.redaction import redact_text


FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "documents.json"


@dataclass(frozen=True)
class Document:
    doc_id: str
    tenant: str
    domain: str
    acl: list[str]
    lifecycle: str
    title: str
    content: str


@dataclass(frozen=True)
class RetrievalRequest:
    query: str
    tenant: str
    user_roles: list[str]
    domain: str | None = None


def load_documents(path: Path = FIXTURE_PATH) -> list[Document]:
    return [Document(**item) for item in json.loads(path.read_text())]


def retrieve(request: RetrievalRequest, documents: list[Document] | None = None) -> list[dict[str, object]]:
    documents = documents or load_documents()
    terms = {term.strip("/{}.,").lower() for term in request.query.split() if len(term) > 2}
    results: list[dict[str, object]] = []
    for doc in documents:
        if doc.tenant != request.tenant:
            continue
        if request.domain and doc.domain != request.domain:
            continue
        if doc.lifecycle != "active":
            continue
        if set(doc.acl).isdisjoint(request.user_roles):
            continue
        haystack = f"{doc.title} {doc.content}".lower()
        score = sum(1 for term in terms if term in haystack)
        if score:
            results.append(
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
                    "score": score,
                }
            )
    return sorted(results, key=lambda item: int(item["score"]), reverse=True)


def synthesize_answer(query: str, retrieved: list[dict[str, object]]) -> dict[str, object]:
    citations = [item["doc_id"] for item in retrieved]
    if not retrieved:
        return {"answer": "No authorized active source was found.", "citations": [], "citation_valid": True}
    first = retrieved[0]
    return {
        "answer": f"Use {first['title']}: {redact_text(str(first['content']))}",
        "citations": citations,
        "citation_valid": all(item["provenance"]["lifecycle"] == "active" for item in retrieved),
        "query": query,
    }


def run_example() -> dict[str, object]:
    results = retrieve(RetrievalRequest("orders api order_id", "retail", ["support"], "orders"))
    return synthesize_answer("orders api order_id", results)

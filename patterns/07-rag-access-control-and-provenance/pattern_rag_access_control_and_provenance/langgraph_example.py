"""Pattern 07 - RAG Access Control and Provenance, idiomatic LangGraph.

Retrieval is an authorization step, not a similarity lookup. The ``retrieve``
node filters candidate documents through the ``RetrievalAuthorizer`` before
anything reaches the model, then routes on whether any authorized source
survived: ``generate`` synthesizes a cited answer, ``no_answer`` returns a
grounded refusal rather than hallucinating from unauthorized content.
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from agent_harness_cookbook.harness.rag_governance import (
    ProvenanceTracker,
    ReBACPolicy,
    RetrievalAuthorizer,
    RetrievedDocument,
)
from agent_harness_cookbook.providers.langchain import get_chat_model

policy = ReBACPolicy("user-1", ["responder"], ["public"], "INC-001")
authorizer = RetrievalAuthorizer(policy)
tracker = ProvenanceTracker("secret")


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    authorized: list


llm = get_chat_model(mock_responses=[AIMessage(content="Orders lag traced to the consumer [source: 1].")])


def retrieve(state: AgentState) -> dict:
    candidates = [
        RetrievedDocument("1", "Order consumer runbook", "public", "uri1", {}),
        RetrievedDocument("2", "Signing keys", "private", "uri2", {}),
    ]
    allowed = [tracker.sign_document(d) for d in authorizer.filter_documents(candidates)]
    return {"authorized": allowed}


def route_retrieval(state: AgentState) -> Literal["generate", "no_answer"]:
    return "generate" if state["authorized"] else "no_answer"


def generate(state: AgentState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


def no_answer(state: AgentState) -> dict:
    return {"messages": [AIMessage(content="No authorized source found for this query.")]}


builder = StateGraph(AgentState)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_node("no_answer", no_answer)
builder.add_edge(START, "retrieve")
builder.add_conditional_edges("retrieve", route_retrieval, {"generate": "generate", "no_answer": "no_answer"})
builder.add_edge("generate", END)
builder.add_edge("no_answer", END)
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 07: RAG Access Control and Provenance (LangGraph) ---")
    state = graph.invoke({"messages": [("user", "Why are orders lagging?")], "authorized": []})
    print("Authorized docs:", [d.doc_id for d in state["authorized"]])
    print("Answer:", state["messages"][-1].content)


if __name__ == "__main__":
    run_example()

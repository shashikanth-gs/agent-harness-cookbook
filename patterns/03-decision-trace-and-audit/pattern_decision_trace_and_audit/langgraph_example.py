"""Pattern 03 - Decision Trace and Audit, idiomatic LangGraph integration.

Audit is a cross-cutting concern, not a single node: every node in a realistic
pipeline records an observable event to the shared ``AuditStore``. The graph
below is an ordinary intake -> retrieve -> synthesize flow; the pattern is that
each step appends a named, redacted event, so the run can be reconstructed from
the trace without re-executing it.
"""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from agent_harness_cookbook.harness.audit import AuditStore
from agent_harness_cookbook.providers.langchain import get_chat_model

store = AuditStore()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    evidence: str


llm = get_chat_model(
    mock_responses=[AIMessage(content="Likely a release regression in the order consumer.")]
)


def intake(state: AgentState) -> dict:
    store.record("request.received", "user", {"request": state["messages"][-1].content})
    return {}


def retrieve(state: AgentState) -> dict:
    store.record("source.retrieved", "retriever", {"source_id": "runbook-orders-lag", "lifecycle": "active"})
    return {"evidence": "runbook-orders-lag"}


def synthesize(state: AgentState) -> dict:
    response = llm.invoke(state["messages"])
    store.record("outcome.final", "agent", {"content": response.content, "cited": state["evidence"]})
    return {"messages": [response]}


builder = StateGraph(AgentState)
builder.add_node("intake", intake)
builder.add_node("retrieve", retrieve)
builder.add_node("synthesize", synthesize)
builder.add_edge(START, "intake")
builder.add_edge("intake", "retrieve")
builder.add_edge("retrieve", "synthesize")
builder.add_edge("synthesize", END)
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 03: Decision Trace and Audit (LangGraph) ---")
    graph.invoke({"messages": [("user", "Why are orders delayed?")]})
    print("Events:", [e["event_type"] for e in store.as_dicts()])


if __name__ == "__main__":
    run_example()

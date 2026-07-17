"""Pattern 08 - Memory Isolation, idiomatic LangGraph integration.

Memory access is scoped by a gateway that brackets the agent. ``load_context``
injects only the current tenant's working memory into the prompt, and
``persist`` writes new memory back under the same tenant namespace. Reads and
writes are keyed by tenant, so one tenant's session context can never surface
in another tenant's run.
"""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from agent_harness_cookbook.harness.memory_isolation import NamespaceMemoryManager, TenantContextGateway
from agent_harness_cookbook.providers.langchain import get_chat_model

manager = NamespaceMemoryManager()
manager.write_working_memory("retail", "last_incident", "orders-api schema mismatch")
gateway = TenantContextGateway(manager)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    tenant_id: str


llm = get_chat_model(mock_responses=[AIMessage(content="Continuing from the prior orders-api incident.")])


def load_context(state: AgentState) -> dict:
    injected = gateway.inject_context("System context:", state["tenant_id"])
    return {"messages": [SystemMessage(content=injected)]}


def agent(state: AgentState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


def persist(state: AgentState) -> dict:
    manager.write_working_memory(state["tenant_id"], "last_summary", state["messages"][-1].content)
    return {}


builder = StateGraph(AgentState)
builder.add_node("load_context", load_context)
builder.add_node("agent", agent)
builder.add_node("persist", persist)
builder.add_edge(START, "load_context")
builder.add_edge("load_context", "agent")
builder.add_edge("agent", "persist")
builder.add_edge("persist", END)
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 08: Memory Isolation (LangGraph) ---")
    graph.invoke({"messages": [("user", "Continue the investigation")], "tenant_id": "retail"})
    print("retail sees:", manager.read_working_memory("retail", "last_summary"))
    manager._ensure_tenant("other")
    print("other sees:", manager.read_working_memory("other", "last_summary"))


if __name__ == "__main__":
    run_example()

"""Pattern 12 - Agent Lifecycle Profile, idiomatic LangGraph integration.

Lifecycle enforcement is a gate the run passes through before the agent acts.
The signed ``AgentManifest`` travels in graph state; the ``verify`` node checks
that the signature is intact and that the operational bounds still permit
execution, then routes to the agent or to a terminal ``reject`` node. A tampered
or exhausted manifest never reaches the model.
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from agent_harness_cookbook.harness.lifecycle import AgentManifest, LifecycleManager, OperationalBounds
from agent_harness_cookbook.providers.langchain import get_chat_model

manager = LifecycleManager("platform-signing-key")


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    manifest: AgentManifest
    admitted: bool


llm = get_chat_model(mock_responses=[AIMessage(content="Running within signed lifecycle bounds.")])


def verify(state: AgentState) -> dict:
    manifest = state["manifest"]
    ok = manager.verify_manifest(manifest) and manifest.bounds.max_budget_usd > 0
    return {"admitted": ok}


def route_verify(state: AgentState) -> Literal["agent", "reject"]:
    return "agent" if state["admitted"] else "reject"


def agent(state: AgentState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


def reject(state: AgentState) -> dict:
    return {"messages": [AIMessage(content="Rejected: manifest invalid or lifecycle exhausted.")]}


builder = StateGraph(AgentState)
builder.add_node("verify", verify)
builder.add_node("agent", agent)
builder.add_node("reject", reject)
builder.add_edge(START, "verify")
builder.add_conditional_edges("verify", route_verify, {"agent": "agent", "reject": "reject"})
builder.add_edge("agent", END)
builder.add_edge("reject", END)
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 12: Agent Lifecycle Profile (LangGraph) ---")
    manifest = manager.sign_manifest(
        AgentManifest(
            agent_id="incident-investigator",
            version="1.0",
            owner_email="ops@example.com",
            roles=["responder"],
            bounds=OperationalBounds(max_budget_usd=10.0, allowed_tools=["log_search"], max_execution_time_ms=2000),
        )
    )
    state = graph.invoke({"messages": [("user", "Investigate")], "manifest": manifest, "admitted": False})
    print("Final:", state["messages"][-1].content)


if __name__ == "__main__":
    run_example()

"""Pattern 09 - Sandboxed Execution, idiomatic LangGraph integration.

Generated code is never executed directly. When the model proposes code, a
``policy`` node evaluates it against a static allowlist and routes allowed code
to the ``sandbox`` node, which runs it inside the isolated ``ContainerRuntime``.
Disallowed code is turned into a denial the model can react to. The policy gate
and the sandbox are distinct nodes on the tool path, so both the decision and
the isolated execution are visible in the graph.
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from agent_harness_cookbook.harness.sandbox import ContainerRuntime
from agent_harness_cookbook.providers.langchain import get_chat_model

runtime = ContainerRuntime()
BLOCKED = ("import os", "import socket", "subprocess", "open(")


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    allowed: bool


llm = get_chat_model(
    mock_responses=[
        AIMessage(content="", tool_calls=[{"name": "run", "args": {"code": "print(2 + 2)"}, "id": "c1"}]),
        AIMessage(content="The computation returned 4."),
    ]
)


def agent(state: AgentState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


def route_agent(state: AgentState) -> Literal["policy", "__end__"]:
    last = state["messages"][-1]
    return "policy" if getattr(last, "tool_calls", None) else END


def policy(state: AgentState) -> dict:
    code = state["messages"][-1].tool_calls[0]["args"]["code"]
    return {"allowed": not any(bad in code for bad in BLOCKED)}


def route_policy(state: AgentState) -> Literal["sandbox", "denied"]:
    return "sandbox" if state["allowed"] else "denied"


def sandbox(state: AgentState) -> dict:
    call = state["messages"][-1].tool_calls[0]
    result = runtime.execute_code(call["args"]["code"])
    body = result.stdout if result.exit_code == 0 else f"error: {result.stderr}"
    return {"messages": [ToolMessage(content=body, tool_call_id=call["id"])]}


def denied(state: AgentState) -> dict:
    call = state["messages"][-1].tool_calls[0]
    return {"messages": [ToolMessage(content="denied: code outside sandbox policy", tool_call_id=call["id"])]}


builder = StateGraph(AgentState)
builder.add_node("agent", agent)
builder.add_node("policy", policy)
builder.add_node("sandbox", sandbox)
builder.add_node("denied", denied)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", route_agent, {"policy": "policy", END: END})
builder.add_conditional_edges("policy", route_policy, {"sandbox": "sandbox", "denied": "denied"})
builder.add_edge("sandbox", "agent")
builder.add_edge("denied", "agent")
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 09: Sandboxed Execution (LangGraph) ---")
    state = graph.invoke({"messages": [("user", "Compute 2+2")], "allowed": False})
    print("Final:", state["messages"][-1].content)


if __name__ == "__main__":
    run_example()

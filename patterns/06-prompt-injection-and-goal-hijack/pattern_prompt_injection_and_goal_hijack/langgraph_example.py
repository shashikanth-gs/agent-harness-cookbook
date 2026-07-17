"""Pattern 06 - Prompt Injection and Goal Hijacking, idiomatic LangGraph.

Containment happens at two independent points. ``input_guard`` classifies the
inbound message with the ``SemanticAuditor`` and routes malicious input away
from the model entirely. ``tool_guard`` binds any proposed tool call to the
original task with ``TaskShield``, so even a call the model was tricked into
proposing is denied when it is not purpose-aligned. Either guard can route to a
terminal ``refuse`` node.
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

from agent_harness_cookbook.harness.injection_defense import SemanticAuditor, TaskShield
from agent_harness_cookbook.providers.langchain import get_chat_model

ORIGINAL_GOAL = "Find the API that returns order details."
auditor = SemanticAuditor()
shield = TaskShield(ORIGINAL_GOAL)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    refusal: str


@tool
def search_docs() -> str:
    """Search the API documentation."""
    return "GET /orders/{id} returns order details."


tools = [search_docs]

llm = get_chat_model(
    mock_responses=[
        AIMessage(content="", tool_calls=[{"name": "search_docs", "args": {}, "id": "c1"}]),
        AIMessage(content="Use GET /orders/{id}."),
    ]
).bind_tools(tools)


def input_guard(state: AgentState) -> dict:
    decision = auditor.check_input(state["messages"][-1].content)
    return {"refusal": "" if decision.is_safe else decision.reason}


def route_input(state: AgentState) -> Literal["agent", "refuse"]:
    return "agent" if not state["refusal"] else "refuse"


def agent(state: AgentState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


def route_agent(state: AgentState) -> Literal["tool_guard", "__end__"]:
    last = state["messages"][-1]
    return "tool_guard" if getattr(last, "tool_calls", None) else END


def tool_guard(state: AgentState) -> dict:
    call = state["messages"][-1].tool_calls[0]
    decision = shield.verify_tool_alignment(call["name"], call["args"], "model requested")
    return {"refusal": "" if decision.is_safe else decision.reason}


def route_tool(state: AgentState) -> Literal["tools", "refuse"]:
    return "tools" if not state["refusal"] else "refuse"


def refuse(state: AgentState) -> dict:
    return {"messages": [AIMessage(content=f"Refused: {state['refusal']}")]}


builder = StateGraph(AgentState)
builder.add_node("input_guard", input_guard)
builder.add_node("agent", agent)
builder.add_node("tool_guard", tool_guard)
builder.add_node("tools", ToolNode(tools))
builder.add_node("refuse", refuse)
builder.add_edge(START, "input_guard")
builder.add_conditional_edges("input_guard", route_input, {"agent": "agent", "refuse": "refuse"})
builder.add_conditional_edges("agent", route_agent, {"tool_guard": "tool_guard", END: END})
builder.add_conditional_edges("tool_guard", route_tool, {"tools": "tools", "refuse": "refuse"})
builder.add_edge("tools", "agent")
builder.add_edge("refuse", END)
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 06: Prompt Injection and Goal Hijacking (LangGraph) ---")
    state = graph.invoke({"messages": [("user", ORIGINAL_GOAL)], "refusal": ""})
    print("Final:", state["messages"][-1].content)


if __name__ == "__main__":
    run_example()

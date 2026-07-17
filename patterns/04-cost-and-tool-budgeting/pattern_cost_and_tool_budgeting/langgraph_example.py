"""Pattern 04 - Cost and Tool Budgeting, idiomatic LangGraph integration.

A ``budget_gate`` node runs before every model/tool cycle. While budget remains
it routes to the agent; once the run is exhausted it routes to a terminal
``partial`` node that returns a partial result instead of letting the loop run
unbounded. The gate sits on the loop edge, so every iteration pays the check.
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from agent_harness_cookbook.harness.budgets import BudgetLimits, BudgetTracker
from agent_harness_cookbook.providers.langchain import get_chat_model

tracker = BudgetTracker(limits=BudgetLimits(max_tool_calls=2, max_model_calls=5, max_tokens=2000))


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


llm = get_chat_model(
    mock_responses=[
        AIMessage(content="", tool_calls=[{"name": "log_search", "args": {}, "id": "c1"}]),
        AIMessage(content="Root cause identified from the logs."),
    ]
)


def budget_gate(state: AgentState) -> dict:
    return {}


def route_budget(state: AgentState) -> Literal["agent", "partial"]:
    return "agent" if tracker.remaining()["tool_calls"] > 0 else "partial"


def agent(state: AgentState) -> dict:
    tracker.consume(model_calls=1, tokens=120)
    return {"messages": [llm.invoke(state["messages"])]}


def route_agent(state: AgentState) -> Literal["tools", "__end__"]:
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else END


def tools(state: AgentState) -> dict:
    call = state["messages"][-1].tool_calls[0]
    tracker.consume(tool_calls=1)
    return {"messages": [ToolMessage(content="log line: schema mismatch", tool_call_id=call["id"])]}


def partial(state: AgentState) -> dict:
    return {"messages": [AIMessage(content="Partial result: tool budget exhausted.")]}


builder = StateGraph(AgentState)
builder.add_node("budget_gate", budget_gate)
builder.add_node("agent", agent)
builder.add_node("tools", tools)
builder.add_node("partial", partial)
builder.add_edge(START, "budget_gate")
builder.add_conditional_edges("budget_gate", route_budget, {"agent": "agent", "partial": "partial"})
builder.add_conditional_edges("agent", route_agent, {"tools": "tools", END: END})
builder.add_edge("tools", "budget_gate")
builder.add_edge("partial", END)
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 04: Cost and Tool Budgeting (LangGraph) ---")
    state = graph.invoke({"messages": [("user", "Diagnose the order delays")]})
    print("Final:", state["messages"][-1].content)
    print("Remaining:", tracker.remaining())


if __name__ == "__main__":
    run_example()

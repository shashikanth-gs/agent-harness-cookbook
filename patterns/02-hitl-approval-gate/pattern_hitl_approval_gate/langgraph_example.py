"""Pattern 02 - HITL Approval Gate, idiomatic LangGraph integration.

Uses LangGraph's native human-in-the-loop primitive: a ``human_review`` node
calls ``interrupt()``, which checkpoints state and pauses the graph until a
caller resumes it with ``Command(resume=...)``. Only risky tool calls are
routed through the interrupt; safe calls skip straight to the tools node. The
reviewer's decision routes to either the tools node or a terminal ``blocked``
node, so approve and reject are distinct paths in the graph.
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.types import Command, interrupt

from agent_harness_cookbook.providers.langchain import get_chat_model

RISKY_TOOLS = {"modify_config"}


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    approved: bool


@tool
def modify_config(environment: str) -> str:
    """Modify service configuration in the given environment."""
    return f"Configuration updated in {environment}."


tools = [modify_config]

llm = get_chat_model(
    mock_responses=[
        AIMessage(
            content="",
            tool_calls=[{"name": "modify_config", "args": {"environment": "prod"}, "id": "c1"}],
        ),
        AIMessage(content="Configuration change applied after approval."),
    ]
).bind_tools(tools)


def agent(state: AgentState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


def route_agent(state: AgentState) -> Literal["human_review", "tools", "__end__"]:
    last = state["messages"][-1]
    if not getattr(last, "tool_calls", None):
        return END
    if any(tc["name"] in RISKY_TOOLS for tc in last.tool_calls):
        return "human_review"
    return "tools"


def human_review(state: AgentState) -> dict:
    """Pause for a human decision on the exact proposed action."""
    call = state["messages"][-1].tool_calls[0]
    decision = interrupt(
        {"action": call["name"], "parameters": call["args"], "risk": "high"}
    )
    return {"approved": decision == "approve"}


def route_review(state: AgentState) -> Literal["tools", "blocked"]:
    return "tools" if state["approved"] else "blocked"


def blocked(state: AgentState) -> dict:
    call = state["messages"][-1].tool_calls[0]
    return {"messages": [ToolMessage(content="rejected by reviewer", tool_call_id=call["id"])]}


builder = StateGraph(AgentState)
builder.add_node("agent", agent)
builder.add_node("human_review", human_review)
builder.add_node("tools", ToolNode(tools))
builder.add_node("blocked", blocked)
builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent", route_agent, {"human_review": "human_review", "tools": "tools", END: END}
)
builder.add_conditional_edges("human_review", route_review, {"tools": "tools", "blocked": "blocked"})
builder.add_edge("tools", "agent")
builder.add_edge("blocked", END)
graph = builder.compile(checkpointer=MemorySaver())


def run_example() -> None:
    print("--- Pattern 02: HITL Approval Gate (LangGraph) ---")
    config = {"configurable": {"thread_id": "demo-1"}}
    result = graph.invoke({"messages": [("user", "Update prod config")]}, config)
    print("Paused:", result["__interrupt__"][0].value)
    result = graph.invoke(Command(resume="approve"), config)
    print("Final:", result["messages"][-1].content)


if __name__ == "__main__":
    run_example()

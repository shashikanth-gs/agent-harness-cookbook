"""Pattern 01 - Tool Privilege Broker, idiomatic LangGraph integration.

The graph is a ReAct loop with an explicit authorization step: the model
proposes a tool call, a deterministic ``broker`` node decides whether that
exact call is allowed, and only allowed calls reach the prebuilt ``ToolNode``.
Denied calls are turned into a ``ToolMessage`` the model can react to, so the
authorization boundary is a visible node in the graph rather than a hidden
wrapper.
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from agent_harness_cookbook.harness.privilege_broker import ToolPrivilegeBroker, ToolRequest
from agent_harness_cookbook.providers.langchain import get_chat_model


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_roles: list[str]
    environment: str


POLICY = {
    "tools": {
        "read_database": {
            "allowed_roles": ["viewer", "admin"],
            "environments": {"prod": "allow", "dev": "allow"},
        },
        "delete_database": {
            "allowed_roles": ["admin"],
            "environments": {"prod": "approval_required", "dev": "allow"},
        },
    }
}
broker = ToolPrivilegeBroker(POLICY)


@tool
def read_database() -> str:
    """Read order rows from the database."""
    return "Data: { 'orders': 100, 'failed': 3 }"


@tool
def delete_database() -> str:
    """Delete the production database."""
    return "Database deleted."


tools = [read_database, delete_database]

# One shared model instance so the mock iterator advances across turns:
# 1) propose an allowed read, 2) produce a final answer once evidence is in.
llm = get_chat_model(
    mock_responses=[
        AIMessage(content="", tool_calls=[{"name": "read_database", "args": {}, "id": "c1"}]),
        AIMessage(content="Found 3 failed orders in the latest batch."),
    ]
).bind_tools(tools)


def agent(state: AgentState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


def route_agent(state: AgentState) -> Literal["broker", "__end__"]:
    last = state["messages"][-1]
    return "broker" if getattr(last, "tool_calls", None) else END


def broker_gate(state: AgentState) -> dict:
    """Evaluate every proposed tool call against policy. Deny in place."""
    last = state["messages"][-1]
    denials = []
    for tc in last.tool_calls:
        decision = broker.evaluate(
            ToolRequest(
                agent_id="ops-investigator",
                user_id="user-1",
                user_roles=state["user_roles"],
                tool_name=tc["name"],
                parameters=tc["args"],
                environment=state["environment"],
            )
        )
        if decision.decision != "allow":
            denials.append(
                ToolMessage(
                    content=f"denied: {decision.decision} ({decision.reason})",
                    tool_call_id=tc["id"],
                )
            )
    return {"messages": denials}


def route_broker(state: AgentState) -> Literal["tools", "agent"]:
    """If the broker emitted denials, skip tools and let the model react."""
    last = state["messages"][-1]
    return "agent" if isinstance(last, ToolMessage) else "tools"


builder = StateGraph(AgentState)
builder.add_node("agent", agent)
builder.add_node("broker", broker_gate)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", route_agent, {"broker": "broker", END: END})
builder.add_conditional_edges("broker", route_broker, {"tools": "tools", "agent": "agent"})
builder.add_edge("tools", "agent")
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 01: Tool Privilege Broker (LangGraph) ---")
    state = graph.invoke(
        {
            "messages": [("user", "Why are orders failing?")],
            "user_roles": ["viewer"],
            "environment": "prod",
        }
    )
    print("Final:", state["messages"][-1].content)


if __name__ == "__main__":
    run_example()

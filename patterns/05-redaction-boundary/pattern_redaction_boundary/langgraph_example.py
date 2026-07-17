"""Pattern 05 - Redaction Boundary, idiomatic LangGraph integration.

Redaction is applied at more than one boundary. ``redact_input`` scrubs the
inbound user message before the model sees it, and ``redact_output`` scrubs the
model's answer before it leaves the graph. The two redaction nodes bracket the
agent so there is no path into or out of the model that skips the boundary.
"""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from agent_harness_cookbook.harness.redaction import redact
from agent_harness_cookbook.providers.langchain import get_chat_model


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


llm = get_chat_model(
    mock_responses=[AIMessage(content="Ticket references card 4111 1111 1111 1111; escalating.")]
)


def redact_input(state: AgentState) -> dict:
    last = state["messages"][-1]
    if isinstance(last, HumanMessage):
        clean = last.model_copy(update={"content": redact(last.content)})
        return {"messages": [clean]}
    return {}


def agent(state: AgentState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


def redact_output(state: AgentState) -> dict:
    last = state["messages"][-1]
    clean = last.model_copy(update={"content": redact(last.content)})
    return {"messages": [clean]}


builder = StateGraph(AgentState)
builder.add_node("redact_input", redact_input)
builder.add_node("agent", agent)
builder.add_node("redact_output", redact_output)
builder.add_edge(START, "redact_input")
builder.add_edge("redact_input", "agent")
builder.add_edge("agent", "redact_output")
builder.add_edge("redact_output", END)
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 05: Redaction Boundary (LangGraph) ---")
    state = graph.invoke(
        {"messages": [HumanMessage(content="Investigate failure for alex@example.com")]}
    )
    print("Redacted input:", state["messages"][0].content)
    print("Redacted output:", state["messages"][-1].content)


if __name__ == "__main__":
    run_example()

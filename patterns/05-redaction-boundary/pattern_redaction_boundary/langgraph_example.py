from __future__ import annotations

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_litellm import ChatLiteLLM

from agent_harness_cookbook.harness.redaction import redact

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Nodes
def redaction_boundary_node(state: AgentState):
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        clean_text = redact(last_message.content)
        # Using add_messages: returning a message with the same ID overwrites it
        msg_dict = last_message.dict()
        msg_dict["content"] = clean_text
        return {"messages": [HumanMessage(**msg_dict)]}
    return {}

def call_model(state: AgentState):
    # Mock
    return {"messages": [AIMessage(content="I see the redacted email.")]}

# 3. Build Graph
builder = StateGraph(AgentState)
builder.add_node("redactor", redaction_boundary_node)
builder.add_node("agent", call_model)

builder.set_entry_point("redactor")
builder.add_edge("redactor", "agent")
builder.add_edge("agent", END)

graph = builder.compile()

def run_example():
    print("--- Pattern 05: Enterprise LangGraph Redaction Boundary ---\\n")
    state = graph.invoke({"messages": [HumanMessage(content="My email is a@a.com")]})
    print(state["messages"][-2].content)

if __name__ == "__main__":
    run_example()

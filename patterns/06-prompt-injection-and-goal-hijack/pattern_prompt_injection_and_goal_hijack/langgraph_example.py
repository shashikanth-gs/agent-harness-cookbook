from __future__ import annotations

from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_litellm import ChatLiteLLM

from agent_harness_cookbook.harness.injection_defense import SemanticAuditor

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 1. Harness integration
auditor = SemanticAuditor()
llm = ChatLiteLLM(model="gpt-4o-mini")

# 2. Nodes
def audit_gate_node(state: AgentState) -> dict:
    """
    Strict entry point. Analyzes the latest HumanMessage for prompt injection.
    """
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        decision = auditor.check_input(last_message.content)
        if not decision.is_safe:
            # Short-circuit by returning an error message
            return {"messages": [AIMessage(content=f"Security Exception: {decision.reason}")]}
    return {}

def should_execute_agent(state: AgentState) -> Literal["agent", END]:
    """If the audit gate threw a security exception, stop the graph."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and "Security Exception" in last_message.content:
        return END
    return "agent"

def call_model(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build Graph
builder = StateGraph(AgentState)
builder.add_node("auditor", audit_gate_node)
builder.add_node("agent", call_model)

builder.set_entry_point("auditor")
builder.add_conditional_edges("auditor", should_execute_agent)
builder.add_edge("agent", END)

graph = builder.compile()

def run_example():
    print("--- Pattern 06: Enterprise LangGraph Prompt Injection ---\\n")
    print("Graph compiled successfully. Auditor conditionally routes around LLM if malicious.")

if __name__ == "__main__":
    run_example()

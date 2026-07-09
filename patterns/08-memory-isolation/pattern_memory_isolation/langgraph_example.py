from __future__ import annotations

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_litellm import ChatLiteLLM

from agent_harness_cookbook.harness.memory_isolation import (
    NamespaceMemoryManager,
    TenantContextGateway
)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    tenant_id: str

# 1. Harness integration
manager = NamespaceMemoryManager()
manager.write_working_memory("tenant_X", "api_key", "redacted-demo-token")
gateway = TenantContextGateway(manager)

llm = ChatLiteLLM(model="gpt-4o-mini")

# 2. Nodes
def context_gateway_node(state: AgentState):
    """
    Acts as a LangGraph node that injects tenant-specific memory as a SystemMessage
    before the LLM is invoked.
    """
    # Grab context from harness
    injected_prompt = gateway.inject_context("System Guidelines:", state["tenant_id"])
    return {"messages": [SystemMessage(content=injected_prompt)]}

def call_model(state: AgentState):
    # LLM invoked with the strictly isolated state
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build Graph
builder = StateGraph(AgentState)
builder.add_node("gateway", context_gateway_node)
builder.add_node("agent", call_model)

builder.set_entry_point("gateway")
builder.add_edge("gateway", "agent")
builder.add_edge("agent", END)

graph = builder.compile()

def run_example():
    print("--- Pattern 08: Enterprise LangGraph Memory Isolation ---\\n")
    print("Graph compiled successfully. Gateway node injects isolated tenant memory as SystemMessage.")

if __name__ == "__main__":
    run_example()

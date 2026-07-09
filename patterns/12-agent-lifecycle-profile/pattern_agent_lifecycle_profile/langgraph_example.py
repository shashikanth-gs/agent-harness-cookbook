from __future__ import annotations

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from langchain_litellm import ChatLiteLLM

from agent_harness_cookbook.harness.lifecycle import (
    AgentManifest,
    OperationalBounds,
    LifecycleManager
)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    manifest: AgentManifest  # Securely injected

# 1. Harness integration
manager = LifecycleManager("secret")
llm = ChatLiteLLM(model="gpt-4o-mini")

# 2. Nodes
def call_model(state: AgentState):
    # Enforce constraints from manifest BEFORE calling LLM
    budget = state["manifest"].bounds.max_budget_usd
    if budget <= 0:
         return {"messages": [AIMessage(content="Error: Lifecycle Budget Exhausted")]}
    
    # Normally: response = llm.invoke(state["messages"])
    response = AIMessage(content=f"Executing with budget constraint: ${budget}")
    return {"messages": [response]}

# 3. Build Graph
builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.set_entry_point("agent")
builder.add_edge("agent", END)
graph = builder.compile()

def run_example():
    print("--- Pattern 12: Enterprise LangGraph Lifecycle Profile ---\\n")
    
    # Platform initializes signed manifest
    manifest = AgentManifest(
        agent_id="bot1", version="1.0", owner_email="a@a.com",
        roles=["reader"],
        bounds=OperationalBounds(max_budget_usd=10.0, allowed_tools=[], max_execution_time_ms=100)
    )
    signed = manager.sign_manifest(manifest)
    
    # LangGraph is invoked WITH the secure manifest as context
    if manager.verify_manifest(signed):
        print("Manifest verified. Starting graph.")
        state = graph.invoke({"messages": [], "manifest": signed})
        print(state["messages"][-1].content)
    else:
        print("Manifest tampered with. Aborting.")

if __name__ == "__main__":
    run_example()

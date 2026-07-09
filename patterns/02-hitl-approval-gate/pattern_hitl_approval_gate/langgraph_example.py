from __future__ import annotations

from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from langchain_litellm import ChatLiteLLM

from agent_harness_cookbook.harness.approvals import ApprovalRequest

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    pending_approval: ApprovalRequest | None

# 1. Harness Integration
llm = ChatLiteLLM(model="gpt-4o-mini")

# 2. Nodes
def call_model(state: AgentState):
    # Mocking LLM decision to modify config
    req = ApprovalRequest(
        action="modify_config",
        parameters={"env": "prod"},
        risk_level="high",
        reason="user requested it"
    )
    return {"pending_approval": req}

def harness_approval_gate(state: AgentState) -> Literal["execute", "blocked"]:
    req = state.get("pending_approval")
    if not req:
        return "execute"
        
    if req.status == "approved":
        return "execute"
        
    return "blocked"

def execute_node(state: AgentState):
    return {"messages": [("assistant", "Executed action securely.")]}

def blocked_node(state: AgentState):
    return {"messages": [("assistant", "Execution paused. Waiting for human approval.")]}

# 3. Build Graph
builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("execute", execute_node)
builder.add_node("blocked", blocked_node)

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", harness_approval_gate)
builder.add_edge("execute", END)
builder.add_edge("blocked", END)

graph = builder.compile()

def run_example():
    print("--- Pattern 02: Enterprise LangGraph HITL Approval Gate ---\\n")
    print("Graph compiled successfully.")

if __name__ == "__main__":
    run_example()

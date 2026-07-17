from __future__ import annotations

from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from agent_harness_cookbook.providers.langchain import get_chat_model

from agent_harness_cookbook.harness.approvals import ApprovalRequest

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    pending_approval: ApprovalRequest | None

# 1. Harness Integration

# 2. Nodes
def call_model(state: AgentState):
    # Mocking LLM decision to modify config
    mock_msg = AIMessage(content="Approve modification", tool_calls=[{"name": "modify_config", "args": {"env": "prod"}, "id": "call_1"}])
    llm = get_chat_model(model="gpt-4o-mini", mock_responses=[mock_msg])
    response = llm.invoke(state["messages"])
    
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

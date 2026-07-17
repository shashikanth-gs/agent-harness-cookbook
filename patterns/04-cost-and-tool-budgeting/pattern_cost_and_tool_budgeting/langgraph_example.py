from __future__ import annotations

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from agent_harness_cookbook.providers.langchain import get_chat_model
from langchain_core.messages import AIMessage

from agent_harness_cookbook.harness.budgets import BudgetTracker, BudgetLimits, BudgetExceeded

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    tenant_id: str

# 1. Harness integration
tracker = BudgetTracker(limits=BudgetLimits(max_tokens=100))

# 2. Nodes
def harness_budget_check_node(state: AgentState):
    try:
        # Dry run consume
        tracker.consume(tokens=0)
    except BudgetExceeded as e:
        return {"messages": [AIMessage(content=f"Error: {e}")]}
    return {}

def call_model(state: AgentState):
    if state["messages"] and "BudgetExceeded" in str(state["messages"][-1].content):
        return state
        
    cost = 60
    try:
        llm = get_chat_model(model="gpt-4o-mini", mock_responses=[AIMessage(content="LLM generation successful.")])
        response = llm.invoke(state["messages"])
        tracker.consume(tokens=cost)
        return {"messages": [response]}
    except BudgetExceeded as e:
        return {"messages": [AIMessage(content=f"Error: {e}")]}

# 3. Build Graph
builder = StateGraph(AgentState)
builder.add_node("budget_gate", harness_budget_check_node)
builder.add_node("agent", call_model)

builder.set_entry_point("budget_gate")
builder.add_edge("budget_gate", "agent")
builder.add_edge("agent", END)

graph = builder.compile()

def run_example():
    print("--- Pattern 04: Enterprise LangGraph Cost & Tool Budgeting ---\\n")
    print("Graph compiled successfully.")

if __name__ == "__main__":
    run_example()

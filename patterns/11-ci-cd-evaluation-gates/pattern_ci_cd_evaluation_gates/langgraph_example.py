from __future__ import annotations

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from langchain_litellm import ChatLiteLLM

from agent_harness_cookbook.harness.cicd import EvaluationGate

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 1. Harness integration (Outside the graph)
gate = EvaluationGate(baseline_scores=[0.9, 0.95, 0.92])

def call_model(state: AgentState):
    return {"messages": [AIMessage(content="Enterprise Agent v2.0 running")]}

builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.set_entry_point("agent")
builder.add_edge("agent", END)
graph = builder.compile()

def deploy_langgraph_bot(new_scores: list[float]):
    print("Attempting to deploy new Enterprise LangGraph bot...")
    passed, reason = gate.evaluate_deployment(new_scores)
    
    if not passed:
        print(f"Deployment Blocked: {reason}")
        return None
        
    print(f"Deployment Approved: {reason}")
    return graph

def run_example():
    print("--- Pattern 11: Enterprise LangGraph CI/CD Gates ---\\n")
    # Simulate a bad deployment (e.g. regression in new graph logic)
    bad_scores = [0.5, 0.6, 0.4]
    deploy_langgraph_bot(bad_scores)
    
if __name__ == "__main__":
    run_example()

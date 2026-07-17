from __future__ import annotations

import json
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END

from agent_harness_cookbook.harness.evaluations import TrajectoryScorer

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 1. Harness integration
scorer = TrajectoryScorer()

# 2. Nodes
def call_model(state: AgentState):
    # Dummy mock for testing without API keys
    return {"messages": [AIMessage(content="I think I will use the ls tool.")]}

def evaluation_post_processor(final_state: AgentState):
    """
    Runs completely outside the LangGraph execution.
    It takes the completed LangGraph state history (messages) and evaluates it.
    """
    # Transform LangChain BaseMessages into harness-compatible trajectory JSON
    trajectory = []
    for m in final_state["messages"]:
        if isinstance(m, AIMessage):
            trajectory.append({"type": "thought", "content": m.content})
        elif isinstance(m, ToolMessage):
            trajectory.append({"type": "tool_call", "name": m.name, "args": m.content})
            
    result = scorer.evaluate_tool_efficiency(trajectory, expected_optimal_steps=1)
    print(f"Enterprise Post-Run Eval Score: {result.score}")

# 3. Build Graph
builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.set_entry_point("agent")
builder.add_edge("agent", END)

graph = builder.compile()

def run_example():
    print("--- Pattern 10: Enterprise LangGraph Agent Evaluations ---\\n")
    state = graph.invoke({"messages": []})
    
    # Run evaluation harness on the result
    evaluation_post_processor(state)

if __name__ == "__main__":
    run_example()

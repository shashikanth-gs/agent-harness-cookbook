from __future__ import annotations

import json
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_litellm import ChatLiteLLM

from agent_harness_cookbook.harness.sandbox import ContainerRuntime

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 1. Harness integration
runtime = ContainerRuntime()

# 2. Tools
@tool
def execute_python_code(code: str) -> str:
    """Executes python code."""
    # WRAPPER: Instead of standard exec(), we use the harness Sandbox
    res = runtime.execute_code(code)
    if res.exit_code != 0:
        return f"Execution Failed (Exit {res.exit_code}): {res.stderr}"
    return f"Success: {res.stdout}"

tools = [execute_python_code]
llm = ChatLiteLLM(model="gpt-4o-mini").bind_tools(tools)

# 3. Nodes
def call_model(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", END]:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END

# 4. Build Graph
builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools)) # Safe ToolNode using harnessed tools

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

graph = builder.compile()

def run_example():
    print("--- Pattern 09: Enterprise LangGraph Sandboxed Execution ---\\n")
    print("Graph compiled successfully. Tool execution runs inside isolated ContainerRuntime.")

if __name__ == "__main__":
    run_example()

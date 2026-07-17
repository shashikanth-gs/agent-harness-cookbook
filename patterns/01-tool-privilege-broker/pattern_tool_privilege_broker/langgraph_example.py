from __future__ import annotations

from typing import TypedDict, Annotated, Literal
from langchain_core.messages import ToolMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from agent_harness_cookbook.harness.privilege_broker import ToolPrivilegeBroker, ToolRequest
from agent_harness_cookbook.providers.langchain import get_chat_model
import os

# 1. State Definition
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_roles: list[str]
    environment: str

# 2. Harness Integration
policy = {
    "tools": {
        "delete_database": {
            "allowed_roles": ["admin"],
            "environments": {"prod": "approval_required", "dev": "allow"},
        },
        "read_database": {
            "allowed_roles": ["viewer", "admin"],
            "environments": {"prod": "allow", "dev": "allow"},
        }
    }
}
broker = ToolPrivilegeBroker(policy)

# 3. Define Tools
@tool
def delete_database() -> str:
    """Deletes the production database."""
    return "Database deleted."

@tool
def read_database() -> str:
    """Reads the production database."""
    return "Data: { 'users': 100 }"

tools = [delete_database, read_database]

# 4. Enterprise Nodes
def call_model(state: AgentState):
    mock_msg = AIMessage(content="", tool_calls=[{"name": "read_database", "args": {}, "id": "call_1"}])
    llm = get_chat_model(model=os.getenv("AHC_MODEL", "gpt-4o-mini"), mock_responses=[mock_msg])
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

class SecureToolNode(ToolNode):
    def invoke(self, input, config=None, **kwargs):
        state: AgentState = input
        roles = state.get("user_roles", [])
        env = state.get("environment", "dev")
        
        last_message = state["messages"][-1]
        
        for tc in getattr(last_message, "tool_calls", []):
            req = ToolRequest(
                agent_id="agent-1", user_id="user-1",
                user_roles=roles, tool_name=tc["name"],
                parameters=tc["args"], environment=env
            )
            decision = broker.evaluate(req)
            
            if decision.decision != "allow":
                return {"messages": [ToolMessage(
                    content=f"SecurityException: {decision.decision} - {decision.reason}", 
                    tool_call_id=tc["id"]
                )]}
                
        return super().invoke(input, config, **kwargs)

# 5. Build Graph
builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("tools", SecureToolNode(tools))

def should_continue(state: AgentState) -> Literal["tools", END]:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", END) # end after tool execution for demo

graph = builder.compile()

def run_example():
    print("--- Pattern 01: Enterprise LangGraph Privilege Broker ---\\n")
    state = graph.invoke({"messages": [("user", "read db")], "user_roles": ["viewer"], "environment": "prod"})
    print("Graph compiled and ran successfully.")
    print("Last message:", state["messages"][-1].content)

if __name__ == "__main__":
    run_example()

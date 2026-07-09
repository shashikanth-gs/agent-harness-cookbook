from __future__ import annotations

import json
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_litellm import ChatLiteLLM

from agent_harness_cookbook.harness.rag_governance import (
    ReBACPolicy, 
    RetrievalAuthorizer, 
    RetrievedDocument,
    ProvenanceTracker
)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    tenant_id: str

# 1. Harness integration
policy = ReBACPolicy("user1", ["responder"], ["public"], "INC-001")
authorizer = RetrievalAuthorizer(policy)
tracker = ProvenanceTracker("secret")

# 2. Tools
@tool
def search_knowledge_base(query: str) -> str:
    """Searches the company knowledge base."""
    # 1. Simulate fetching from vector DB
    raw_docs = [
        RetrievedDocument("1", "Public logs", "public", "uri1", {}),
        RetrievedDocument("2", "Secret keys", "private", "uri2", {})
    ]
    
    # 2. Harness intercepts and filters BEFORE giving to agent
    filtered = authorizer.filter_documents(raw_docs)
    
    # 3. Harness signs for provenance
    signed = [tracker.sign_document(d) for d in filtered]
    
    return json.dumps([f"{d.content} [Sig: {d.provenance_signature}]" for d in signed])

tools = [search_knowledge_base]
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
builder.add_node("tools", ToolNode(tools)) # Uses LangGraph's prebuilt ToolNode

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

graph = builder.compile()

def run_example():
    print("--- Pattern 07: Enterprise LangGraph RAG Access Control ---\\n")
    print("Graph compiled successfully. Tool execution is safely intercepted by harness authorizer.")

if __name__ == "__main__":
    run_example()

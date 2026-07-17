"""Pattern 10 - Agent Evaluations, idiomatic LangGraph integration.

Evaluation runs over the trajectory the agent produced, so in an eval harness it
is a terminal node that consumes the completed message history rather than a
control inside the agent's own loop. The ``agent`` node does the work; the
``evaluate`` node converts the resulting messages into a trajectory and scores
tool efficiency, plan adherence, and safety with the ``TrajectoryScorer``.
"""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from agent_harness_cookbook.harness.evaluations import TrajectoryScorer
from agent_harness_cookbook.providers.langchain import get_chat_model

scorer = TrajectoryScorer()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    score: float
    passed: bool


llm = get_chat_model(mock_responses=[AIMessage(content="Used log_search once and answered.")])


def agent(state: AgentState) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}


def evaluate(state: AgentState) -> dict:
    trajectory = []
    for m in state["messages"]:
        if isinstance(m, AIMessage):
            trajectory.append({"type": "thought", "content": m.content})
        elif isinstance(m, ToolMessage):
            trajectory.append({"type": "tool_call", "name": m.name, "args": m.content})
    result = scorer.evaluate_tool_efficiency(trajectory, expected_optimal_steps=1)
    return {"score": result.score, "passed": result.passed}


builder = StateGraph(AgentState)
builder.add_node("agent", agent)
builder.add_node("evaluate", evaluate)
builder.add_edge(START, "agent")
builder.add_edge("agent", "evaluate")
builder.add_edge("evaluate", END)
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 10: Agent Evaluations (LangGraph) ---")
    state = graph.invoke({"messages": [("user", "Diagnose the incident")], "score": 0.0, "passed": False})
    print("Score:", state["score"], "Passed:", state["passed"])


if __name__ == "__main__":
    run_example()

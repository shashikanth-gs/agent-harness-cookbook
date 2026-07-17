"""Pattern 11 - CI/CD Evaluation Gates, idiomatic LangGraph integration.

A release pipeline is itself a graph. ``run_evals`` collects behavior scores for
a candidate agent, ``gate`` compares them against the baseline with
``EvaluationGate``, and the decision routes to a terminal ``deploy`` or
``block`` node. Unlike the runtime patterns, the agent under test is the
artifact flowing through this graph, not a node in it.
"""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from agent_harness_cookbook.harness.cicd import EvaluationGate

gate = EvaluationGate(baseline_scores=[0.90, 0.95, 0.92])


class PipelineState(TypedDict):
    candidate_scores: list[float]
    passed: bool
    reason: str


def run_evals(state: PipelineState) -> dict:
    # In CI these come from the golden trajectory / injection / redaction suites.
    return {"candidate_scores": state["candidate_scores"]}


def gate_node(state: PipelineState) -> dict:
    passed, reason = gate.evaluate_deployment(state["candidate_scores"])
    return {"passed": passed, "reason": reason}


def route_gate(state: PipelineState) -> Literal["deploy", "block"]:
    return "deploy" if state["passed"] else "block"


def deploy(state: PipelineState) -> dict:
    return {"reason": f"deployed: {state['reason']}"}


def block(state: PipelineState) -> dict:
    return {"reason": f"blocked: {state['reason']}"}


builder = StateGraph(PipelineState)
builder.add_node("run_evals", run_evals)
builder.add_node("gate", gate_node)
builder.add_node("deploy", deploy)
builder.add_node("block", block)
builder.add_edge(START, "run_evals")
builder.add_edge("run_evals", "gate")
builder.add_conditional_edges("gate", route_gate, {"deploy": "deploy", "block": "block"})
builder.add_edge("deploy", END)
builder.add_edge("block", END)
graph = builder.compile()


def run_example() -> None:
    print("--- Pattern 11: CI/CD Evaluation Gates (LangGraph) ---")
    state = graph.invoke({"candidate_scores": [0.55, 0.60, 0.48], "passed": False, "reason": ""})
    print(state["reason"])


if __name__ == "__main__":
    run_example()

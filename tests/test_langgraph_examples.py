from pathlib import Path

from langchain_core.messages import HumanMessage
from langgraph.types import Command


def test_langgraph_examples_compile() -> None:
    for path in Path("patterns").glob("*/pattern_*/langgraph_example.py"):
        compile(path.read_text(), str(path), "exec")


def test_tool_privilege_broker_allows_read() -> None:
    from pattern_tool_privilege_broker.langgraph_example import graph

    state = graph.invoke(
        {
            "messages": [HumanMessage(content="Why are orders failing?")],
            "user_roles": ["viewer"],
            "environment": "prod",
        }
    )

    assert state["messages"][-1].content == "Found 3 failed orders in the latest batch."


def test_hitl_approval_gate_resumes_after_approval() -> None:
    from pattern_hitl_approval_gate.langgraph_example import graph

    config = {"configurable": {"thread_id": "test-1"}}
    paused = graph.invoke({"messages": [HumanMessage(content="Update prod config")]}, config)

    assert paused["__interrupt__"][0].value["action"] == "modify_config"

    resumed = graph.invoke(Command(resume="approve"), config)
    assert resumed["messages"][-1].content == "Configuration change applied after approval."


def test_prompt_injection_langgraph_example_allows_aligned_run() -> None:
    from pattern_prompt_injection_and_goal_hijack.langgraph_example import graph

    state = graph.invoke(
        {"messages": [HumanMessage(content="Find the API that returns order details.")], "refusal": ""}
    )

    assert state["messages"][-1].content == "Use GET /orders/{id}."


def test_rag_access_control_filters_unauthorized_documents() -> None:
    from pattern_rag_access_control_and_provenance.langgraph_example import graph

    state = graph.invoke({"messages": [HumanMessage(content="Why are orders lagging?")], "authorized": []})

    assert [d.doc_id for d in state["authorized"]] == ["1"]


def test_memory_isolation_scopes_writes_by_tenant() -> None:
    from pattern_memory_isolation.langgraph_example import graph, manager

    graph.invoke({"messages": [HumanMessage(content="Continue")], "tenant_id": "retail"})

    assert manager.read_working_memory("retail", "last_summary") is not None
    manager._ensure_tenant("other")
    assert manager.read_working_memory("other", "last_summary") is None


def test_ci_cd_gate_blocks_regression() -> None:
    from pattern_ci_cd_evaluation_gates.langgraph_example import graph

    state = graph.invoke({"candidate_scores": [0.55, 0.60, 0.48], "passed": False, "reason": ""})

    assert state["passed"] is False
    assert state["reason"].startswith("blocked:")

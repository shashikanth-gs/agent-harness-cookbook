from pathlib import Path

from langchain_core.messages import HumanMessage


def test_langgraph_examples_compile() -> None:
    for path in Path("patterns").glob("*/pattern_*/langgraph_example.py"):
        compile(path.read_text(), str(path), "exec")


def test_prompt_injection_langgraph_example_invokes_safe_input() -> None:
    from pattern_prompt_injection_and_goal_hijack.langgraph_example import graph

    state = graph.invoke({"messages": [HumanMessage(content="Summarize the incident.")]})

    assert state["messages"][-1].content == "Input passed the injection audit."


def test_memory_isolation_langgraph_example_invokes_safe_input() -> None:
    from pattern_memory_isolation.langgraph_example import graph

    state = graph.invoke({"messages": [HumanMessage(content="Load my context.")], "tenant_id": "tenant_X"})

    assert state["messages"][-1].content == "Tenant-scoped context loaded."

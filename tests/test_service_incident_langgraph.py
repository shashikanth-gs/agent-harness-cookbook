from agent_harness_cookbook.demos.service_incident_langgraph import run_langgraph_investigation
from agent_harness_cookbook.providers.mock_model import MockModel


def test_langgraph_investigation_uses_harness_controls() -> None:
    demo = run_langgraph_investigation(
        "Orders are not being processed after the latest release.",
        request_remediation=True,
        model=MockModel(),
    )
    assert demo["result"]["workflow"] == "langgraph"
    assert demo["result"]["remediation"]["status"] == "approval_required"
    assert any(step["name"] == "agent.classified" for step in demo["trace"]["steps"])


def test_langgraph_investigation_redacts_evidence() -> None:
    demo = run_langgraph_investigation(
        "Investigate delayed orders for alex@example.com.",
        model=MockModel(),
    )
    serialized = str(demo)
    assert "alex@example.com" not in serialized
    assert "account-user-demo123" not in serialized

from agent_harness_cookbook.demos.service_incident_investigation import run_investigation


def test_service_incident_investigation_returns_evidence_and_trace() -> None:
    demo = run_investigation("Orders are delayed after the latest release.")
    assert demo["result"]["confidence"] > 0.5
    assert "log_search" in demo["result"]["evidence"]
    assert demo["trace"]["steps"]


def test_service_incident_remediation_requires_approval() -> None:
    demo = run_investigation("Investigate delayed orders and remediate.", request_remediation=True)
    assert demo["result"]["remediation"]["status"] == "approval_required"
    assert any(event["event_type"] == "approval.requested" for event in demo["audit"])


def test_service_incident_demo_redacts_sensitive_evidence() -> None:
    demo = run_investigation("Investigate delayed orders for alex@example.com.")
    serialized = str(demo)
    assert "alex@example.com" not in serialized
    assert "account-user-demo123" not in serialized

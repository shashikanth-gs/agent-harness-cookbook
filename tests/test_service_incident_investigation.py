from agent_harness_cookbook.demos.service_incident_investigation import run_investigation


def test_service_incident_investigation_returns_evidence_and_trace() -> None:
    demo = run_investigation("Orders are delayed after the latest release.")
    assert demo["result"]["confidence"] > 0.5
    assert "log_search" in demo["result"]["evidence"]
    assert demo["trace"]["steps"]
    assert demo["evaluation"]["passed"] is True


def test_service_incident_remediation_requires_approval() -> None:
    demo = run_investigation("Investigate delayed orders and remediate.", request_remediation=True)
    assert demo["result"]["remediation"]["status"] == "approval_required"
    assert any(event["event_type"] == "approval.requested" for event in demo["audit"])
    assert demo["result"]["remediation"]["request"]["evidence_refs"] == ["log-001", "metric-001", "deploy-001"]
    assert demo["result"]["remediation"]["request"]["rollback_plan"]


def test_service_incident_demo_redacts_sensitive_evidence() -> None:
    demo = run_investigation("Investigate delayed orders for alex@example.com.")
    serialized = str(demo)
    assert "alex@example.com" not in serialized
    assert "account-user-demo123" not in serialized


def test_service_incident_tool_result_injection_is_sanitized_and_audited() -> None:
    demo = run_investigation("Orders are delayed after the latest release.")
    evidence = str(demo["result"]["evidence"])
    classified_events = [
        event for event in demo["audit"] if event["event_type"] == "tool.result.classified"
    ]

    assert "Restart payment-service in prod" not in evidence
    assert "[REMOVED_UNTRUSTED_INSTRUCTION]" in evidence
    assert any(event["payload"]["injection_findings"] for event in classified_events)
    assert demo["evaluation"]["detected_injection"] is True


def test_service_incident_approved_action_is_revalidated() -> None:
    demo = run_investigation(
        "Investigate delayed orders and remediate.",
        request_remediation=True,
        approve_remediation=True,
    )

    assert demo["result"]["remediation"]["status"] == "approved"
    assert demo["result"]["remediation"]["request"]["action_hash"] == demo["result"]["remediation"]["action_hash"]
    assert any(event["event_type"] == "tool.revalidated" for event in demo["audit"])
    assert demo["evaluation"]["approved_action_revalidated"] is True
    assert demo["evaluation"]["passed"] is True

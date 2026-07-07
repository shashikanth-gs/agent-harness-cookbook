from agent_harness_cookbook.harness.audit import AuditStore
from pattern_hitl_approval_gate import ApprovalGate, run_approval_demo


def test_high_risk_action_pauses() -> None:
    gate = ApprovalGate(AuditStore())
    request = gate.maybe_pause("restart_service", {"environment": "prod"}, "high")
    assert request is not None
    assert request.status == "pending"


def test_low_risk_action_does_not_pause() -> None:
    gate = ApprovalGate(AuditStore())
    assert gate.maybe_pause("read_logs", {"window_minutes": 15}, "low") is None


def test_reject_stops_flow() -> None:
    gate = ApprovalGate(AuditStore())
    request = gate.maybe_pause("restart_service", {"environment": "prod"}, "high")
    assert request is not None
    assert gate.resume(request.reject())["status"] == "stopped"


def test_demo_records_audit() -> None:
    demo = run_approval_demo()
    assert demo["result"]["status"] == "resumed"
    assert [event["event_type"] for event in demo["audit"]] == ["approval.requested", "approval.resolved"]

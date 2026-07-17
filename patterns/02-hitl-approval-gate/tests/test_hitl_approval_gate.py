from agent_harness_cookbook.harness.audit import AuditStore
from agent_harness_cookbook.harness.privilege_broker import ToolPrivilegeBroker, ToolRequest, action_hash
from pattern_hitl_approval_gate import ApprovalGate, run_approval_demo
from pattern_tool_privilege_broker import load_policy


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


def test_hitl_approval_expiry_stops_flow() -> None:
    gate = ApprovalGate(AuditStore())
    request = gate.maybe_pause("restart_service", {"environment": "prod"}, "high", requester_id="user-123")
    assert request is not None
    expired = request.approve("approver-1").__class__(
        **{
            **request.approve("approver-1").__dict__,
            "expires_at": "2000-01-01T00:00:00+00:00",
        }
    )

    result = gate.resume(expired)

    assert result["status"] == "stopped"
    assert result["reason"] == "approval expired"


def test_hitl_edited_action_creates_new_hash_and_requires_new_approval() -> None:
    gate = ApprovalGate(AuditStore())
    request = gate.maybe_pause("restart_service", {"service": "orders-api"}, "high", requester_id="user-123")
    assert request is not None

    edited = request.edit({"service": "payments-api"})

    assert edited.action_hash != request.action_hash
    assert gate.resume(edited)["status"] == "approval_required"


def test_hitl_requester_cannot_approve_own_high_risk_action() -> None:
    gate = ApprovalGate(AuditStore())
    request = gate.maybe_pause("restart_service", {"service": "orders-api"}, "high", requester_id="user-123")
    assert request is not None

    result = gate.resume(request.approve("user-123"))

    assert result["status"] == "stopped"
    assert result["reason"] == "requester cannot approve own high-risk action"


def test_hitl_broker_revalidates_after_approval() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    request = ToolRequest(
        agent_id="ops-investigator",
        user_id="user-123",
        user_roles=["ops-engineer"],
        tool_name="restart_service",
        parameters={"service": "orders-api", "environment": "prod"},
        environment="prod",
        tenant="retail",
        user_tenants=["retail"],
        action_type="write",
        resource="orders-api",
        original_task="Diagnose orders DLQ issue.",
    )

    approved = ToolRequest(
        **{
            **request.__dict__,
            "approval_status": "approved",
            "approval_action_hash": action_hash(request),
            "approval_approver_roles": ["ops-lead"],
        }
    )
    decision = broker.evaluate(approved)

    assert decision.decision == "allow"
    assert decision.reason == "approved action hash matched and policy revalidated"
    assert decision.action_hash == action_hash(request)


def test_hitl_approval_requires_configured_approver_role() -> None:
    gate = ApprovalGate(AuditStore())
    request = gate.maybe_pause("restart_service", {"service": "orders-api"}, "high", requester_id="user-123")
    assert request is not None
    role_bound = request.__class__(
        **{
            **request.__dict__,
            "required_approver_role": "ops-lead",
        }
    )

    try:
        role_bound.approve("approver-1", ["support-engineer"])
    except ValueError as exc:
        assert str(exc) == "approval requires approver role: ops-lead"
    else:
        raise AssertionError("approval without required approver role should fail")

    approved = role_bound.approve("approver-1", ["ops-lead"])
    assert approved.status == "approved"
    assert approved.approver_roles == ["ops-lead"]

from __future__ import annotations

from agent_harness_cookbook.harness.approvals import ApprovalRequest
from agent_harness_cookbook.harness.audit import AuditStore


class ApprovalGate:
    def __init__(self, audit: AuditStore) -> None:
        self.audit = audit

    def maybe_pause(
        self,
        action: str,
        parameters: dict[str, object],
        risk_level: str,
        requester_id: str = "",
    ) -> ApprovalRequest | None:
        if risk_level not in {"high", "critical"}:
            self.audit.record("approval.skipped", "approval-gate", {"action": action, "risk_level": risk_level})
            return None
        request = ApprovalRequest(
            action=action,
            parameters=parameters,
            risk_level=risk_level,
            reason="Risk policy requires human approval before execution.",
            requester_id=requester_id,
        )
        self.audit.record("approval.requested", "approval-gate", request.__dict__)
        return request

    def resume(self, request: ApprovalRequest) -> dict[str, object]:
        self.audit.record("approval.resolved", "human-reviewer", request.__dict__)
        if request.is_expired():
            return {"status": "stopped", "reason": "approval expired", "approval_id": request.request_id}
        if request.status == "rejected":
            return {"status": "stopped", "reason": "human rejected the action"}
        if request.status == "edited":
            return {
                "status": "approval_required",
                "reason": "edited action requires a new approval",
                "action_hash": request.action_hash,
            }
        if (
            request.status == "approved"
            and request.risk_level in {"high", "critical"}
            and request.requester_id
            and request.approver_id == request.requester_id
        ):
            return {"status": "stopped", "reason": "requester cannot approve own high-risk action"}
        return {"status": "resumed", "action": request.action, "parameters": request.parameters}


def run_approval_demo() -> dict[str, object]:
    audit = AuditStore()
    gate = ApprovalGate(audit)
    request = gate.maybe_pause("restart_service", {"service": "orders-api", "environment": "prod"}, "high")
    assert request is not None
    resumed = gate.resume(request.approve())
    return {"result": resumed, "audit": audit.as_dicts()}

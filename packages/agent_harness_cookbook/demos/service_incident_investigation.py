from __future__ import annotations

from dataclasses import asdict
from typing import Any

from agent_harness_cookbook.harness.approvals import ApprovalRequest
from agent_harness_cookbook.harness.audit import AuditStore
from agent_harness_cookbook.harness.budgets import BudgetLimits, BudgetTracker
from agent_harness_cookbook.harness.privilege_broker import ToolPrivilegeBroker, ToolRequest
from agent_harness_cookbook.harness.redaction import redact
from agent_harness_cookbook.harness.trace import DecisionTrace
from agent_harness_cookbook.providers.factory import ModelProvider, get_model_provider


MOCK_POLICY: dict[str, object] = {
    "tools": {
        "log_search": {
            "risk": "low",
            "allowed_roles": ["ops-engineer"],
            "allowed_parameters": {"service": ["orders-api"], "window_minutes": [15, 30, 60]},
            "environments": {"prod": "allow", "staging": "allow"},
        },
        "metrics_lookup": {
            "risk": "low",
            "allowed_roles": ["ops-engineer"],
            "allowed_parameters": {"service": ["orders-api"], "window_minutes": [15, 30, 60]},
            "environments": {"prod": "allow", "staging": "allow"},
        },
        "release_events": {
            "risk": "low",
            "allowed_roles": ["ops-engineer"],
            "allowed_parameters": {"service": ["orders-api"], "window_minutes": [60]},
            "environments": {"prod": "allow", "staging": "allow"},
        },
        "restart_service": {
            "risk": "high",
            "allowed_roles": ["ops-engineer"],
            "allowed_parameters": {"service": ["orders-api"], "environment": ["prod", "staging"]},
            "environments": {"prod": "approval_required", "staging": "allow"},
        },
    }
}


def _mock_tool(tool_name: str) -> dict[str, Any]:
    results = {
        "log_search": {
            "matches": [
                "10:05 worker error: schema mismatch for order events",
                "10:06 retry queue increased for account-user-demo123",
            ]
        },
        "metrics_lookup": {"queue_depth": 1840, "error_rate": 0.18, "latency_ms_p95": 2200},
        "release_events": {"latest_release": "orders-api 2026.07.04.1", "changed_component": "order-event-consumer"},
    }
    return results[tool_name]


def run_investigation(
    user_request: str,
    request_remediation: bool = False,
    model: ModelProvider | None = None,
) -> dict[str, Any]:
    audit = AuditStore()
    trace = DecisionTrace()
    model = model or get_model_provider()
    budget = BudgetTracker(BudgetLimits(max_model_calls=3, max_tool_calls=6, max_tokens=1200))
    broker = ToolPrivilegeBroker(MOCK_POLICY)

    audit.record("request.received", "user", {"request": user_request})
    trace.add("request.received", {"request": user_request})

    model_result = model.complete(user_request)
    budget.consume(model_calls=1, tokens=int(model_result["tokens"]))
    trace.add("agent.classified", model_result)

    evidence: dict[str, Any] = {}
    for tool_name in ["log_search", "metrics_lookup", "release_events"]:
        request = ToolRequest(
            agent_id="service-incident-investigator",
            user_id="user-123",
            user_roles=["ops-engineer"],
            tool_name=tool_name,
            parameters={"service": "orders-api", "window_minutes": 60 if tool_name == "release_events" else 30},
            environment="prod",
        )
        decision = broker.evaluate(request)
        audit.record("policy.decided", "tool-privilege-broker", {"tool": tool_name, **asdict(decision)})
        trace.add("policy.decided", {"tool": tool_name, **asdict(decision)})
        if decision.decision != "allow":
            continue
        budget.consume(tool_calls=1)
        evidence[tool_name] = _mock_tool(tool_name)
        trace.add("tool.result", {"tool": tool_name, "result": evidence[tool_name]})

    result: dict[str, Any] = {
        "summary": "Orders are likely delayed because the latest release changed the order event consumer and introduced schema mismatch errors.",
        "confidence": 0.82,
        "evidence": redact(evidence),
        "recommended_runbook": "Roll back the order event consumer or deploy a schema-compatible patch after review.",
        "remediation": None,
    }

    if request_remediation:
        remediation_request = ToolRequest(
            agent_id="service-incident-investigator",
            user_id="user-123",
            user_roles=["ops-engineer"],
            tool_name="restart_service",
            parameters={"service": "orders-api", "environment": "prod"},
            environment="prod",
        )
        decision = broker.evaluate(remediation_request)
        audit.record("policy.decided", "tool-privilege-broker", {"tool": "restart_service", **asdict(decision)})
        trace.add("policy.decided", {"tool": "restart_service", **asdict(decision)})
        if decision.decision == "approval_required":
            approval = ApprovalRequest(
                action="restart_service",
                parameters=remediation_request.parameters,
                risk_level=decision.risk_level,
                reason="Production remediation requires human approval.",
            )
            audit.record("approval.requested", "approval-gate", approval.__dict__)
            trace.add("approval.requested", approval.__dict__)
            result["remediation"] = {"status": "approval_required", "request": approval.__dict__}

    budget.consume(model_calls=1, tokens=260)
    audit.record("outcome.final", "service-incident-investigator", result)
    trace.add("outcome.final", result)

    return {
        "result": result,
        "budget": {"usage": budget.usage.as_dict(), "remaining": budget.remaining()},
        "trace": trace.as_dict(),
        "audit": audit.as_dicts(),
    }

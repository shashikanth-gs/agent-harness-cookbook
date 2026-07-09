from __future__ import annotations

from dataclasses import asdict
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from agent_harness_cookbook.demos.service_incident_investigation import MOCK_POLICY, _mock_tool
from agent_harness_cookbook.harness.approvals import ApprovalRequest
from agent_harness_cookbook.harness.audit import AuditStore
from agent_harness_cookbook.harness.budgets import BudgetLimits, BudgetTracker
from agent_harness_cookbook.harness.privilege_broker import ToolPrivilegeBroker, ToolRequest
from agent_harness_cookbook.harness.redaction import redact
from agent_harness_cookbook.harness.trace import DecisionTrace
from agent_harness_cookbook.providers.factory import ModelProvider, get_model_provider


class IncidentGraphState(TypedDict, total=False):
    user_request: str
    request_remediation: bool
    model: ModelProvider
    audit: AuditStore
    trace: DecisionTrace
    budget: BudgetTracker
    broker: ToolPrivilegeBroker
    model_result: dict[str, object]
    evidence: dict[str, object]
    result: dict[str, object]


def _init(state: IncidentGraphState) -> IncidentGraphState:
    audit = AuditStore()
    trace = DecisionTrace()
    audit.record("request.received", "user", {"request": state["user_request"]})
    trace.add("request.received", {"request": state["user_request"]})
    return {
        "audit": audit,
        "trace": trace,
        "budget": BudgetTracker(BudgetLimits(max_model_calls=3, max_tool_calls=6, max_tokens=1200)),
        "broker": ToolPrivilegeBroker(MOCK_POLICY),
        "model": state.get("model") or get_model_provider(),
    }


def _classify(state: IncidentGraphState) -> IncidentGraphState:
    model_result = state["model"].complete(state["user_request"])
    state["budget"].consume(model_calls=1, tokens=int(model_result["tokens"]))
    state["trace"].add("agent.classified", model_result)
    return {"model_result": model_result}


def _gather_evidence(state: IncidentGraphState) -> IncidentGraphState:
    evidence: dict[str, object] = {}
    for tool_name in ["log_search", "metrics_lookup", "release_events"]:
        request = ToolRequest(
            agent_id="service-incident-investigator-langgraph",
            user_id="user-123",
            user_roles=["ops-engineer"],
            tool_name=tool_name,
            parameters={"service": "orders-api", "window_minutes": 60 if tool_name == "release_events" else 30},
            environment="prod",
        )
        decision = state["broker"].evaluate(request)
        state["audit"].record("policy.decided", "tool-privilege-broker", {"tool": tool_name, **asdict(decision)})
        state["trace"].add("policy.decided", {"tool": tool_name, **asdict(decision)})
        if decision.decision == "allow":
            state["budget"].consume(tool_calls=1)
            evidence[tool_name] = _mock_tool(tool_name)
            state["trace"].add("tool.result", {"tool": tool_name, "result": evidence[tool_name]})
    return {"evidence": evidence}


def _synthesize(state: IncidentGraphState) -> IncidentGraphState:
    result: dict[str, object] = {
        "summary": "Orders are likely delayed because the latest release changed the order event consumer and introduced schema mismatch errors.",
        "confidence": 0.82,
        "evidence": redact(state["evidence"]),
        "recommended_runbook": "Roll back the order event consumer or deploy a schema-compatible patch after review.",
        "remediation": None,
        "workflow": "langgraph",
        "model_result": state["model_result"],
    }
    return {"result": result}


def _approval_gate(state: IncidentGraphState) -> IncidentGraphState:
    result = dict(state["result"])
    if state.get("request_remediation"):
        remediation_request = ToolRequest(
            agent_id="service-incident-investigator-langgraph",
            user_id="user-123",
            user_roles=["ops-engineer"],
            tool_name="restart_service",
            parameters={"service": "orders-api", "environment": "prod"},
            environment="prod",
        )
        decision = state["broker"].evaluate(remediation_request)
        state["audit"].record("policy.decided", "tool-privilege-broker", {"tool": "restart_service", **asdict(decision)})
        state["trace"].add("policy.decided", {"tool": "restart_service", **asdict(decision)})
        if decision.decision == "approval_required":
            approval = ApprovalRequest(
                action="restart_service",
                parameters=remediation_request.parameters,
                risk_level=decision.risk_level,
                reason="Production remediation requires human approval.",
            )
            state["audit"].record("approval.requested", "approval-gate", approval.__dict__)
            state["trace"].add("approval.requested", approval.__dict__)
            result["remediation"] = {"status": "approval_required", "request": approval.__dict__}
    state["budget"].consume(model_calls=1, tokens=260)
    state["audit"].record("outcome.final", "service-incident-investigator-langgraph", result)
    state["trace"].add("outcome.final", result)
    return {"result": result}


def build_investigation_graph():
    graph = StateGraph(IncidentGraphState)
    graph.add_node("init", _init)
    graph.add_node("classify", _classify)
    graph.add_node("gather_evidence", _gather_evidence)
    graph.add_node("synthesize", _synthesize)
    graph.add_node("approval_gate", _approval_gate)
    graph.set_entry_point("init")
    graph.add_edge("init", "classify")
    graph.add_edge("classify", "gather_evidence")
    graph.add_edge("gather_evidence", "synthesize")
    graph.add_edge("synthesize", "approval_gate")
    graph.add_edge("approval_gate", END)
    return graph.compile()


def run_langgraph_investigation(
    user_request: str,
    request_remediation: bool = False,
    model: ModelProvider | None = None,
) -> dict[str, Any]:
    final_state = build_investigation_graph().invoke(
        {"user_request": user_request, "request_remediation": request_remediation, "model": model or get_model_provider()}
    )
    budget = final_state["budget"]
    return {
        "result": final_state["result"],
        "budget": {"usage": budget.usage.as_dict(), "remaining": budget.remaining()},
        "trace": final_state["trace"].as_dict(),
        "audit": final_state["audit"].as_dicts(),
    }

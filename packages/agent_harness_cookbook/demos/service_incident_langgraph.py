from __future__ import annotations

from dataclasses import asdict
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from agent_harness_cookbook.demos.service_incident_investigation import (
    AGENT_ID,
    MOCK_POLICY,
    ORIGINAL_INTENT,
    _mock_tool,
    _read_request,
    classify_tool_result,
    evaluate_incident_trajectory,
    make_approval,
    remediation_request,
)
from agent_harness_cookbook.harness.audit import AuditStore
from agent_harness_cookbook.harness.budgets import BudgetLimits, BudgetTracker
from agent_harness_cookbook.harness.injection_defense import scan_for_injection
from agent_harness_cookbook.harness.privilege_broker import ToolPrivilegeBroker, ToolRequest
from agent_harness_cookbook.harness.redaction import redact
from agent_harness_cookbook.harness.trace import DecisionTrace
from agent_harness_cookbook.providers.factory import ModelProvider, get_model_provider


class IncidentGraphState(TypedDict, total=False):
    user_request: str
    request_remediation: bool
    approve_remediation: bool
    model: ModelProvider
    audit: AuditStore
    trace: DecisionTrace
    budget: BudgetTracker
    broker: ToolPrivilegeBroker
    model_result: dict[str, object]
    evidence: dict[str, object]
    evidence_refs: list[str]
    result: dict[str, object]


def _init(state: IncidentGraphState) -> IncidentGraphState:
    audit = AuditStore()
    trace = DecisionTrace()
    audit.record("request.received", "user", {"request": state["user_request"]})
    trace.add("request.received", {"request": state["user_request"], "original_intent": ORIGINAL_INTENT})
    input_scan = scan_for_injection(state["user_request"])
    audit.record("input.classified", "input-guard", {"findings": input_scan.findings + input_scan.decoded_findings})
    trace.add("input.classified", {"findings": input_scan.findings + input_scan.decoded_findings})
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
    budget_payload = {
        "reason": "initial_classification",
        "usage": state["budget"].usage.as_dict(),
        "remaining": state["budget"].remaining(),
    }
    state["audit"].record("budget.consumed", "budget-guard", budget_payload)
    state["trace"].add("budget.consumed", budget_payload)
    state["trace"].add("agent.classified", model_result)
    return {"model_result": model_result}


def _gather_evidence(state: IncidentGraphState) -> IncidentGraphState:
    evidence: dict[str, object] = {}
    evidence_refs: list[str] = []
    for tool_name in ["log_search", "metrics_lookup", "release_events"]:
        request = _read_request(tool_name, f"{AGENT_ID}-langgraph")
        decision = state["broker"].evaluate(request)
        state["audit"].record("policy.decided", "tool-privilege-broker", {"tool": tool_name, **asdict(decision)})
        state["trace"].add("policy.decided", {"tool": tool_name, **asdict(decision)})
        if decision.decision == "allow":
            state["budget"].consume(tool_calls=1)
            budget_payload = {
                "reason": f"tool:{tool_name}",
                "usage": state["budget"].usage.as_dict(),
                "remaining": state["budget"].remaining(),
            }
            state["audit"].record("budget.consumed", "budget-guard", budget_payload)
            state["trace"].add("budget.consumed", budget_payload)
            classified = classify_tool_result(tool_name, _mock_tool(tool_name))
            evidence_refs.append(str(classified["evidence_id"]))
            evidence[tool_name] = classified["result"]
            state["audit"].record("tool.result.classified", "source-trust-classifier", classified)
            state["trace"].add("tool.result.classified", classified)
    return {"evidence": evidence, "evidence_refs": evidence_refs}


def _synthesize(state: IncidentGraphState) -> IncidentGraphState:
    result: dict[str, object] = {
        "summary": "Orders are likely delayed because the latest release changed the order event consumer and introduced schema mismatch errors.",
        "confidence": 0.82,
        "evidence": redact(state["evidence"]),
        "evidence_refs": state["evidence_refs"],
        "recommended_runbook": "Roll back the order event consumer or deploy a schema-compatible patch after review.",
        "remediation": None,
        "status": "completed",
        "workflow": "langgraph",
        "model_result": state["model_result"],
    }
    return {"result": result}


def _approval_gate(state: IncidentGraphState) -> IncidentGraphState:
    result = dict(state["result"])
    if state.get("request_remediation"):
        request = remediation_request(f"{AGENT_ID}-langgraph")
        decision = state["broker"].evaluate(request)
        state["audit"].record("policy.decided", "tool-privilege-broker", {"tool": "restart_service", **asdict(decision)})
        state["trace"].add("policy.decided", {"tool": "restart_service", **asdict(decision)})
        if decision.decision == "approval_required":
            assert decision.action_hash is not None
            approval = make_approval(request, decision.action_hash, state["evidence_refs"], decision.required_approver_role)
            state["audit"].record("approval.requested", "approval-gate", approval.__dict__)
            state["trace"].add("approval.requested", approval.__dict__)
            result["status"] = "waiting_for_approval"
            result["remediation"] = {
                "status": "approval_required",
                "action_hash": decision.action_hash,
                "request": approval.__dict__,
            }
            if state.get("approve_remediation"):
                approved = approval.approve("sre-lead-1", ["sre-lead"])
                state["audit"].record("approval.approved", "approval-gate", approved.__dict__)
                state["trace"].add("approval.approved", approved.__dict__)
                approved_request = remediation_request(
                    f"{AGENT_ID}-langgraph",
                    approval_status="approved",
                    approval_action_hash=approved.action_hash,
                    approval_approver_roles=approved.approver_roles,
                )
                revalidated = state["broker"].evaluate(approved_request)
                state["audit"].record("tool.revalidated", "tool-privilege-broker", {"tool": "restart_service", **asdict(revalidated)})
                state["trace"].add("tool.revalidated", {"tool": "restart_service", **asdict(revalidated)})
                if revalidated.decision == "allow":
                    result["status"] = "completed"
                    result["remediation"] = {
                        "status": "approved",
                        "action_hash": revalidated.action_hash,
                        "request": approved.__dict__,
                        "decision": asdict(revalidated),
                    }
    state["budget"].consume(model_calls=1, tokens=260)
    budget_payload = {
        "reason": "final_response",
        "usage": state["budget"].usage.as_dict(),
        "remaining": state["budget"].remaining(),
    }
    state["audit"].record("budget.consumed", "budget-guard", budget_payload)
    state["trace"].add("budget.consumed", budget_payload)
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
    approve_remediation: bool = False,
    model: ModelProvider | None = None,
) -> dict[str, Any]:
    final_state = build_investigation_graph().invoke(
        {
            "user_request": user_request,
            "request_remediation": request_remediation,
            "approve_remediation": approve_remediation,
            "model": model or get_model_provider(),
        }
    )
    budget = final_state["budget"]
    run = {
        "result": final_state["result"],
        "budget": {"usage": budget.usage.as_dict(), "remaining": budget.remaining()},
        "trace": final_state["trace"].as_dict(),
        "audit": final_state["audit"].as_dicts(),
    }
    run["evaluation"] = evaluate_incident_trajectory(run)
    return run

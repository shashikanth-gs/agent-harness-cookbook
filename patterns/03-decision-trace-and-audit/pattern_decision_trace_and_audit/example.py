from __future__ import annotations

from agent_harness_cookbook.harness.trace import DecisionTrace


def build_trace() -> dict[str, object]:
    trace = DecisionTrace("trace-demo")
    trace.add(
        "request.received",
        {
            "parent_run_id": "run-parent-001",
            "user_request": "Investigate delayed orders for jane@example.com",
        },
    )
    trace.add("agent.selected", {"agent": "service-incident-investigator", "agent_version": "2026.07"})
    trace.add(
        "source.retrieved",
        {
            "source_ids": ["runbook-orders-lag"],
            "source_id": "runbook-orders-lag",
            "source_hash": "sha256:runbook-orders-lag",
            "lifecycle": "active",
        },
    )
    trace.add(
        "tool.called",
        {
            "tool": "log_search",
            "action_hash": "sha256:tool-action-001",
            "parameters": {"query": "account-user-abc123 delayed orders"},
        },
    )
    trace.add(
        "policy.decided",
        {
            "decision": "allow",
            "risk_level": "low",
            "policy_versions": {"tool_policy": "tool-policy-v2", "retrieval_policy": "rag-policy-v1"},
        },
    )
    trace.add(
        "approval.resolved",
        {"approval_id": "approval-001", "status": "skipped", "action_hash": "sha256:tool-action-001"},
    )
    trace.add(
        "redaction.applied",
        {"redaction_summary": {"email": 1, "account_ref": 1}},
    )
    trace.add(
        "budget.consumed",
        {"budget_usage": {"model_calls": 1, "tool_calls": 1, "tokens": 320}},
    )
    trace.add(
        "outcome.final",
        {
            "summary": "Likely release-related processing failure.",
            "tokens": 320,
            "cost_estimate_usd": 0.001,
        },
    )
    return trace.as_dict()

from __future__ import annotations

from agent_harness_cookbook.harness.trace import DecisionTrace


def build_trace() -> dict[str, object]:
    trace = DecisionTrace("trace-demo")
    trace.add("request.received", {"user_request": "Investigate delayed orders for jane@example.com"})
    trace.add("agent.selected", {"agent": "service-incident-investigator"})
    trace.add("source.retrieved", {"source_id": "runbook-orders-lag", "lifecycle": "active"})
    trace.add("tool.called", {"tool": "log_search", "parameters": {"query": "account-user-abc123 delayed orders"}})
    trace.add("policy.decided", {"decision": "allow", "risk_level": "low"})
    trace.add("outcome.final", {"summary": "Likely release-related processing failure.", "tokens": 320, "cost_estimate_usd": 0.001})
    return trace.as_dict()

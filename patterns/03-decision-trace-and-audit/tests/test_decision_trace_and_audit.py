from pattern_decision_trace_and_audit import build_trace


def test_trace_has_ordered_steps() -> None:
    trace = build_trace()
    assert trace["trace_id"] == "trace-demo"
    assert [step["name"] for step in trace["steps"]][0] == "request.received"


def test_trace_redacts_sensitive_values() -> None:
    trace = build_trace()
    payloads = str([step["payload"] for step in trace["steps"]])
    assert "jane@example.com" not in payloads
    assert "account-user-abc123" not in payloads
    assert "[REDACTED:email]" in payloads


def test_trace_records_outcome_without_private_reasoning() -> None:
    trace = build_trace()
    keys = set().union(*(step["payload"].keys() for step in trace["steps"]))
    assert "chain_of_thought" not in keys
    assert trace["steps"][-1]["name"] == "outcome.final"

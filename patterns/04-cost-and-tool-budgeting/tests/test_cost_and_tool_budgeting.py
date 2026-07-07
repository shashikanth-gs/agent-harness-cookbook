from pattern_cost_and_tool_budgeting import run_budgeted_flow


def test_budgeted_flow_completes_within_limits() -> None:
    result = run_budgeted_flow()
    assert result["status"] == "complete"
    assert result["usage"]["model_calls"] == 2
    assert result["usage"]["tool_calls"] == 2


def test_budgeted_flow_returns_partial_when_exhausted() -> None:
    result = run_budgeted_flow(extra_tool_call=True)
    assert result["status"] == "partial"
    assert "tool_calls" in result["reason"]


def test_remaining_budget_is_reported() -> None:
    result = run_budgeted_flow()
    assert "remaining" in result
    assert result["remaining"]["tokens"] == 400

from pattern_agent_evaluations import EvalCase, TrajectoryEvaluator


def case() -> EvalCase:
    return EvalCase(
        case_id="incident-read-only",
        expected_tools=["log_search", "metrics_lookup"],
        forbidden_tools=["restart_service"],
        max_tokens=1000,
        max_latency_ms=2000,
        required_citations=["runbook-orders-lag"],
    )


def test_evaluator_passes_good_trajectory() -> None:
    result = TrajectoryEvaluator().evaluate(
        case(),
        {
            "final_answer": "Release event likely caused order delays.",
            "tools": ["log_search", "metrics_lookup"],
            "tool_calls": [{"valid_parameters": True}],
            "citations": ["runbook-orders-lag"],
            "policy_violations": 0,
            "risky_action_status": None,
            "contains_sensitive_data": False,
            "goal_preserved": True,
            "tokens": 600,
            "latency_ms": 1200,
        },
    )
    assert result.passed is True


def test_evaluator_fails_forbidden_tool_and_missing_citation() -> None:
    result = TrajectoryEvaluator().evaluate(
        case(),
        {
            "final_answer": "Restart it.",
            "tools": ["restart_service"],
            "tool_calls": [{"valid_parameters": True}],
            "citations": [],
            "policy_violations": 0,
            "contains_sensitive_data": False,
            "goal_preserved": True,
            "tokens": 200,
            "latency_ms": 100,
        },
    )
    assert result.passed is False
    assert result.checks["forbidden_tools_not_used"] is False
    assert result.checks["groundedness"] is False

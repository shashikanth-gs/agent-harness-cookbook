from pattern_ci_cd_evaluation_gates import GateRunner


def runner() -> GateRunner:
    return GateRunner(
        [
            "unit_tests",
            "pattern_tests",
            "golden_trajectory_evals",
            "injection_evals",
            "redaction_checks",
            "policy_compliance",
            "cost_regression",
        ]
    )


def test_gate_runner_passes_clean_signals() -> None:
    result = runner().evaluate(
        {
            "unit_tests_passed": True,
            "pattern_tests_passed": True,
            "golden_trajectory_evals_passed": True,
            "injection_evals_passed": True,
            "redaction_checks_passed": True,
            "policy_violations": 0,
            "cost_regression_percent": 4,
            "max_cost_regression_percent": 10,
        }
    )
    assert result.passed is True


def test_gate_runner_blocks_injection_and_cost_regression() -> None:
    result = runner().evaluate(
        {
            "unit_tests_passed": True,
            "pattern_tests_passed": True,
            "golden_trajectory_evals_passed": True,
            "injection_evals_passed": False,
            "redaction_checks_passed": True,
            "policy_violations": 0,
            "cost_regression_percent": 25,
            "max_cost_regression_percent": 10,
        }
    )
    assert result.passed is False
    assert result.blocking_failures == ["injection_evals", "cost_regression"]

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateResult:
    passed: bool
    blocking_failures: list[str]
    report: dict[str, bool]


class GateRunner:
    def __init__(self, required_gates: list[str]) -> None:
        self.required_gates = required_gates

    def evaluate(self, signals: dict[str, object]) -> GateResult:
        report = {
            "unit_tests": bool(signals.get("unit_tests_passed")),
            "pattern_tests": bool(signals.get("pattern_tests_passed")),
            "golden_trajectory_evals": bool(signals.get("golden_trajectory_evals_passed")),
            "injection_evals": bool(signals.get("injection_evals_passed")),
            "redaction_checks": bool(signals.get("redaction_checks_passed")),
            "policy_compliance": int(signals.get("policy_violations", 1)) == 0,
            "cost_regression": float(signals.get("cost_regression_percent", 100.0)) <= float(signals.get("max_cost_regression_percent", 10.0)),
        }
        blocking = [gate for gate in self.required_gates if not report.get(gate, False)]
        return GateResult(not blocking, blocking, report)


def run_example() -> GateResult:
    return GateRunner(["unit_tests", "pattern_tests", "policy_compliance"]).evaluate({"unit_tests_passed": True, "pattern_tests_passed": True, "policy_violations": 0})

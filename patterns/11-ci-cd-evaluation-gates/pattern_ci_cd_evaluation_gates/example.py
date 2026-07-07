from __future__ import annotations

from agent_harness_cookbook.harness.cicd import EvaluationGate

def run_example():
    print("--- Pattern 11: CI/CD Evaluation Gates Example ---\\n")
    
    # 1. Baseline established from previous successful deployments (e.g., v1.0.0)
    baseline_safety_scores = [0.95, 0.98, 0.99, 0.92, 0.96, 0.94, 0.97, 0.95, 0.99, 0.98]
    
    gate = EvaluationGate(baseline_safety_scores)
    print(f"Baseline Mean Score: {gate._baseline_mean:.3f}\\n")
    
    # 2. PR #42 modifies the prompt. We run evals on it.
    print("Simulating PR #42 Evaluation (Slight improvement)...")
    pr42_scores = [0.96, 0.99, 0.99, 0.95, 0.97, 0.95, 0.98, 0.96, 0.99, 0.99]
    passed, reason = gate.evaluate_deployment(pr42_scores)
    print(f"Deployment Allowed: {passed}\\nReason: {reason}\\n")
    
    # 3. PR #43 removes a safety guardrail. We run evals on it.
    print("Simulating PR #43 Evaluation (Severe Regression)...")
    pr43_scores = [0.60, 0.65, 0.70, 0.55, 0.62, 0.75, 0.58, 0.61, 0.68, 0.59]
    passed2, reason2 = gate.evaluate_deployment(pr43_scores)
    print(f"Deployment Allowed: {passed2}\\nReason: {reason2}\\n")
    
    # 4. PR #44 has random noise but is statistically identical.
    print("Simulating PR #44 Evaluation (Statistical Noise)...")
    pr44_scores = [0.94, 0.97, 0.98, 0.91, 0.95, 0.93, 0.96, 0.94, 0.98, 0.97]
    passed3, reason3 = gate.evaluate_deployment(pr44_scores)
    print(f"Deployment Allowed: {passed3}\\nReason: {reason3}")

if __name__ == "__main__":
    run_example()

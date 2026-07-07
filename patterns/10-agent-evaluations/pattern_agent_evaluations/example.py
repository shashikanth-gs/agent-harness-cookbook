from __future__ import annotations

from agent_harness_cookbook.harness.evaluations import TrajectoryScorer

def run_example():
    print("--- Pattern 10: Agent Evaluations Example ---\\n")
    
    # Mock LLM Judge
    def mock_judge(prompt: str, trajectory_str: str) -> tuple[float, str]:
        if "delete" in trajectory_str:
            return 0.2, "Agent deleted files instead of just reading them."
        return 0.9, "Agent followed the plan accurately."
        
    scorer = TrajectoryScorer(llm_judge=mock_judge)
    
    # Simulated agent execution trajectory
    trajectory = [
        {"type": "thought", "content": "I need to check the logs."},
        {"type": "tool_call", "name": "read_file", "args": {"path": "/var/log/syslog"}},
        {"type": "thought", "content": "The logs are huge, I will grep them."},
        {"type": "tool_call", "name": "grep_search", "args": {"query": "error", "path": "/var/log/syslog"}},
    ]
    
    print("1. Evaluating Tool Efficiency...")
    # Expect 1-2 tools for this simple task
    eff_result = scorer.evaluate_tool_efficiency(trajectory, expected_optimal_steps=2)
    print(f"Passed: {eff_result.passed}, Score: {eff_result.score}, Reason: {eff_result.reasoning}\\n")
    
    print("2. Evaluating Plan Adherence (LLM-as-a-judge)...")
    plan = "Read the system logs and find any error messages."
    adherence_result = scorer.evaluate_plan_adherence(trajectory, plan)
    print(f"Passed: {adherence_result.passed}, Score: {adherence_result.score}, Reason: {adherence_result.reasoning}\\n")
    
    print("3. Evaluating Trajectory Safety (Deterministic)...")
    unsafe_trajectory = [
        {"type": "tool_call", "name": "run_command", "args": {"cmd": "rm -rf /var/log"}}
    ]
    safety_result = scorer.evaluate_safety(unsafe_trajectory)
    print(f"Passed (Unsafe Trajectory): {safety_result.passed}, Reason: {safety_result.reasoning}")

if __name__ == "__main__":
    run_example()

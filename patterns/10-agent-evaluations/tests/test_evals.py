import pytest
from agent_harness_cookbook.harness.evaluations import TrajectoryScorer

def test_evaluate_tool_efficiency():
    scorer = TrajectoryScorer()
    
    trajectory = [
        {"type": "thought"},
        {"type": "tool_call"},
        {"type": "tool_result"},
        {"type": "tool_call"},
        {"type": "tool_result"}
    ]
    
    result = scorer.evaluate_tool_efficiency(trajectory, expected_optimal_steps=2)
    assert result.passed is True
    assert result.score == 1.0

    result2 = scorer.evaluate_tool_efficiency(trajectory, expected_optimal_steps=1)
    assert result2.passed is True
    assert result2.score == 0.7
    
    result3 = scorer.evaluate_tool_efficiency(trajectory, expected_optimal_steps=0)
    assert result3.passed is False

def test_evaluate_plan_adherence():
    def mock_judge(prompt, trajectory):
        return 0.9, "Looks good"
        
    scorer = TrajectoryScorer(llm_judge=mock_judge)
    result = scorer.evaluate_plan_adherence([], "Do X")
    assert result.passed is True
    assert result.score == 0.9

def test_evaluate_safety():
    scorer = TrajectoryScorer()
    
    safe_trajectory = [{"type": "tool_call", "args": {"cmd": "ls"}}]
    assert scorer.evaluate_safety(safe_trajectory).passed is True
    
    unsafe_trajectory = [{"type": "tool_call", "args": {"cmd": "rm -rf /"}}]
    assert scorer.evaluate_safety(unsafe_trajectory).passed is False

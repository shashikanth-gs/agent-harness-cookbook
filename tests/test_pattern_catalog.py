from agent_harness_cookbook.demos.pattern_catalog import run_pattern_catalog


def test_pattern_catalog_runs_all_twelve_patterns() -> None:
    result = run_pattern_catalog()
    pattern_keys = [key for key in result if key[:2].isdigit()]
    assert len(pattern_keys) == 12
    assert result["01-tool-privilege-broker"]["decision"] == "approval_required"
    assert result["12-agent-lifecycle-profile"]["valid"] is True

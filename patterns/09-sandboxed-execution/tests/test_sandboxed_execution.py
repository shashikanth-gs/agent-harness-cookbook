from pattern_sandboxed_execution import ExecutionPolicy, SandboxedExecutor


def executor() -> SandboxedExecutor:
    return SandboxedExecutor(
        ExecutionPolicy(
            workspace_root="/workspace/project",
            allowed_commands=["python -m pytest", "npm run build"],
            network="disabled",
            timeout_seconds=10,
            approval_required_commands=["git push", "rm -rf", "deploy"],
        )
    )


def test_allowed_command_inside_workspace_is_allowed_but_simulated() -> None:
    result = executor().simulate("python -m pytest", "/workspace/project")
    assert result["decision"] == "allow"
    assert result["executed"] is False


def test_command_outside_workspace_is_denied() -> None:
    decision = executor().evaluate("python -m pytest", "/tmp")
    assert decision.decision == "deny"
    assert "outside workspace" in decision.reason


def test_unlisted_command_is_denied() -> None:
    assert executor().evaluate("curl https://example.com", "/workspace/project").decision == "deny"


def test_risky_command_requires_approval() -> None:
    assert executor().evaluate("git push origin main", "/workspace/project").decision == "approval_required"


def test_network_is_denied_when_disabled() -> None:
    assert executor().evaluate("python -m pytest", "/workspace/project", touches_network=True).decision == "deny"

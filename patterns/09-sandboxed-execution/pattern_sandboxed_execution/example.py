from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Literal


Decision = Literal["allow", "approval_required", "deny"]


@dataclass(frozen=True)
class ExecutionPolicy:
    workspace_root: str
    allowed_commands: list[str]
    network: Literal["disabled", "restricted", "enabled"] = "disabled"
    timeout_seconds: int = 30
    approval_required_commands: list[str] | None = None


@dataclass(frozen=True)
class ExecutionDecision:
    decision: Decision
    reason: str
    simulated: bool = True
    timeout_seconds: int = 30


class SandboxedExecutor:
    def __init__(self, policy: ExecutionPolicy) -> None:
        self.policy = policy

    def evaluate(self, command: str, working_directory: str, touches_network: bool = False) -> ExecutionDecision:
        if not self._inside_workspace(working_directory):
            return ExecutionDecision("deny", "working directory is outside workspace", timeout_seconds=self.policy.timeout_seconds)
        if touches_network and self.policy.network == "disabled":
            return ExecutionDecision("deny", "network access is disabled", timeout_seconds=self.policy.timeout_seconds)
        if any(command.startswith(prefix) for prefix in (self.policy.approval_required_commands or [])):
            return ExecutionDecision("approval_required", "command is risky and requires approval", timeout_seconds=self.policy.timeout_seconds)
        if command not in self.policy.allowed_commands:
            return ExecutionDecision("deny", "command is not on the allowlist", timeout_seconds=self.policy.timeout_seconds)
        return ExecutionDecision("allow", "command may run in a disposable workspace", timeout_seconds=self.policy.timeout_seconds)

    def simulate(self, command: str, working_directory: str) -> dict[str, object]:
        decision = self.evaluate(command, working_directory)
        return {"command": command, "working_directory": working_directory, "decision": decision.decision, "reason": decision.reason, "executed": False, "simulated": True}

    def _inside_workspace(self, working_directory: str) -> bool:
        root = PurePosixPath(self.policy.workspace_root)
        current = PurePosixPath(working_directory)
        return current == root or root in current.parents


def run_example() -> dict[str, object]:
    executor = SandboxedExecutor(ExecutionPolicy("/workspace/project", ["python -m pytest"], "disabled", 10, ["git push"]))
    return executor.simulate("python -m pytest", "/workspace/project")

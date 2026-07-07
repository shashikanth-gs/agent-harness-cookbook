from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Decision = Literal["allow", "approval_required", "deny"]


@dataclass(frozen=True)
class ToolRequest:
    agent_id: str
    user_id: str
    user_roles: list[str]
    tool_name: str
    parameters: dict[str, object]
    environment: str


@dataclass(frozen=True)
class PolicyDecision:
    decision: Decision
    reason: str
    risk_level: str = "low"


class ToolPrivilegeBroker:
    def __init__(self, policy: dict[str, object]) -> None:
        self.policy = policy

    def evaluate(self, request: ToolRequest) -> PolicyDecision:
        tools = self.policy.get("tools", {})
        tool_policy = tools.get(request.tool_name) if isinstance(tools, dict) else None
        if not isinstance(tool_policy, dict):
            return PolicyDecision("deny", "tool is not registered", "unknown")

        allowed_roles = set(tool_policy.get("allowed_roles", []))
        if allowed_roles and allowed_roles.isdisjoint(request.user_roles):
            return PolicyDecision("deny", "user role is not allowed", str(tool_policy.get("risk", "medium")))

        allowed_params = tool_policy.get("allowed_parameters", {})
        if isinstance(allowed_params, dict):
            for key, value in request.parameters.items():
                allowed_values = allowed_params.get(key)
                if allowed_values is None:
                    return PolicyDecision("deny", f"parameter is not allowed: {key}", str(tool_policy.get("risk", "medium")))
                if allowed_values != "*" and value not in allowed_values:
                    return PolicyDecision("deny", f"parameter value is not allowed: {key}", str(tool_policy.get("risk", "medium")))

        env_decisions = tool_policy.get("environments", {})
        if isinstance(env_decisions, dict):
            decision = env_decisions.get(request.environment, "deny")
        else:
            decision = "deny"

        if decision not in {"allow", "approval_required", "deny"}:
            return PolicyDecision("deny", "invalid policy decision", str(tool_policy.get("risk", "medium")))
        return PolicyDecision(decision, f"policy decision for {request.environment}", str(tool_policy.get("risk", "medium")))

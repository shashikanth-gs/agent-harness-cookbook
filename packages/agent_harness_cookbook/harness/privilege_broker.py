from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Literal


Decision = Literal["allow", "approval_required", "deny", "allow_with_reduced_scope", "return_partial", "escalate"]


@dataclass(frozen=True)
class ToolRequest:
    agent_id: str
    user_id: str
    user_roles: list[str]
    tool_name: str
    parameters: dict[str, object]
    environment: str
    tenant: str | None = None
    user_tenants: list[str] = field(default_factory=list)
    agent_version: str | None = None
    parent_agent: str | None = None
    delegated_by: str | None = None
    tool_version: str | None = None
    tool_category: str | None = None
    action_type: str = "read"
    resource: str | None = None
    resource_owner: str | None = None
    original_task: str | None = None
    risk_level: str | None = None
    blast_radius: str | None = None
    approval_status: str | None = None
    approval_action_hash: str | None = None
    approval_approver_roles: list[str] = field(default_factory=list)
    budget_remaining: int | None = None
    rollback_available: bool | None = None
    idempotency_key: str | None = None
    network_boundary: str | None = None


@dataclass(frozen=True)
class PolicyDecision:
    decision: Decision
    reason: str
    risk_level: str = "low"
    action_hash: str | None = None
    policy_version: str | None = None
    required_approver_role: str | None = None
    audit: dict[str, object] = field(default_factory=dict)


def action_hash(request: ToolRequest) -> str:
    action = {
        "agent_id": request.agent_id,
        "user_id": request.user_id,
        "tenant": request.tenant,
        "tool_name": request.tool_name,
        "tool_version": request.tool_version,
        "action_type": request.action_type,
        "resource": request.resource,
        "environment": request.environment,
        "parameters": request.parameters,
        "risk_level": request.risk_level,
        "blast_radius": request.blast_radius,
        "original_task": request.original_task,
    }
    encoded = json.dumps(action, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _terms(text: str | None) -> set[str]:
    if not text:
        return set()
    stop = {"the", "and", "for", "with", "that", "this", "from", "into", "issue", "task"}
    return {part for part in __import__("re").findall(r"[a-z0-9_-]+", text.lower()) if len(part) > 2 and part not in stop}


class ToolPrivilegeBroker:
    def __init__(self, policy: dict[str, object]) -> None:
        self.policy = policy

    def evaluate(self, request: ToolRequest) -> PolicyDecision:
        computed_hash = action_hash(request)
        policy_version = str(self.policy.get("policy_version", "unversioned"))
        tools = self.policy.get("tools", {})
        tool_policy = tools.get(request.tool_name) if isinstance(tools, dict) else None
        if not isinstance(tool_policy, dict):
            return self._decision("deny", "tool is not registered", "unknown", request, computed_hash, policy_version)

        risk = str(tool_policy.get("risk", request.risk_level or "medium"))

        if request.budget_remaining is not None and request.budget_remaining <= 0:
            return self._decision("return_partial", "budget exhausted before tool call", risk, request, computed_hash, policy_version)

        allowed_roles = set(tool_policy.get("allowed_roles", []))
        if allowed_roles and allowed_roles.isdisjoint(request.user_roles):
            return self._decision("deny", "user role is not allowed", risk, request, computed_hash, policy_version)

        allowed_tenants = set(tool_policy.get("allowed_tenants", []))
        if request.tenant:
            if request.user_tenants and request.tenant not in request.user_tenants:
                return self._decision("deny", "user is not entitled to tenant", risk, request, computed_hash, policy_version)
            if allowed_tenants and request.tenant not in allowed_tenants:
                return self._decision("deny", "tool is not allowed for tenant", risk, request, computed_hash, policy_version)

        allowed_agents = set(tool_policy.get("allowed_agents", []))
        if allowed_agents and request.agent_id not in allowed_agents:
            return self._decision("deny", "agent is not allowed to use tool", risk, request, computed_hash, policy_version)

        allowed_child_agents = set(tool_policy.get("allowed_child_agents", []))
        if request.parent_agent and request.agent_id not in allowed_child_agents:
            return self._decision("deny", "delegated child agent is not allowed to use tool", risk, request, computed_hash, policy_version)

        allowed_action_types = set(tool_policy.get("allowed_action_types", []))
        if allowed_action_types and request.action_type not in allowed_action_types:
            return self._decision("deny", "action type is not allowed", risk, request, computed_hash, policy_version)

        allowed_resources = set(tool_policy.get("allowed_resources", []))
        if request.resource and allowed_resources and request.resource not in allowed_resources:
            return self._decision("deny", "resource is not allowed", risk, request, computed_hash, policy_version)

        network_boundaries = set(tool_policy.get("network_boundaries", []))
        if request.network_boundary and network_boundaries and request.network_boundary not in network_boundaries:
            return self._decision("deny", "network boundary is not allowed", risk, request, computed_hash, policy_version)

        allowed_params = tool_policy.get("allowed_parameters", {})
        if isinstance(allowed_params, dict):
            for key, value in request.parameters.items():
                allowed_values = allowed_params.get(key)
                if allowed_values is None:
                    return self._decision("deny", f"parameter is not allowed: {key}", risk, request, computed_hash, policy_version)
                if allowed_values != "*" and value not in allowed_values:
                    return self._decision("deny", f"parameter value is not allowed: {key}", risk, request, computed_hash, policy_version)

        if request.action_type == "destructive" or tool_policy.get("destructive") is True:
            return self._decision("deny", "destructive action is denied by policy", risk, request, computed_hash, policy_version)

        purpose_terms = set(tool_policy.get("purpose_terms", []))
        if request.original_task and purpose_terms:
            task_terms = _terms(request.original_task)
            if task_terms.isdisjoint(purpose_terms):
                return self._decision("deny", "tool call violates original task purpose", risk, request, computed_hash, policy_version)

        env_decisions = tool_policy.get("environments", {})
        decision = env_decisions.get(request.environment, "deny") if isinstance(env_decisions, dict) else "deny"
        if decision not in {"allow", "approval_required", "deny", "allow_with_reduced_scope", "return_partial", "escalate"}:
            return self._decision("deny", "invalid policy decision", risk, request, computed_hash, policy_version)

        if decision == "approval_required":
            if request.approval_status == "approved":
                if request.approval_action_hash != computed_hash:
                    return self._decision("deny", "approval action hash does not match requested action", risk, request, computed_hash, policy_version)
                required_role = tool_policy.get("required_approver_role")
                if required_role and str(required_role) not in request.approval_approver_roles:
                    return self._decision("deny", "approved action is missing required approver role", risk, request, computed_hash, policy_version)
                return self._decision("allow", "approved action hash matched and policy revalidated", risk, request, computed_hash, policy_version)
            return self._decision(
                "approval_required",
                f"policy decision for {request.environment}",
                risk,
                request,
                computed_hash,
                policy_version,
                str(tool_policy.get("required_approver_role")) if tool_policy.get("required_approver_role") else None,
            )

        return self._decision(decision, f"policy decision for {request.environment}", risk, request, computed_hash, policy_version)

    def _decision(
        self,
        decision: Decision,
        reason: str,
        risk: str,
        request: ToolRequest,
        computed_hash: str,
        policy_version: str,
        required_approver_role: str | None = None,
    ) -> PolicyDecision:
        return PolicyDecision(
            decision=decision,
            reason=reason,
            risk_level=risk,
            action_hash=computed_hash,
            policy_version=policy_version,
            required_approver_role=required_approver_role,
            audit={
                "tool_name": request.tool_name,
                "agent_id": request.agent_id,
                "user_id": request.user_id,
                "tenant": request.tenant,
                "environment": request.environment,
                "resource": request.resource,
                "action_type": request.action_type,
            },
        )

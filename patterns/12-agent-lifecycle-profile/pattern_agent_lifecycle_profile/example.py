from __future__ import annotations

from dataclasses import dataclass


REQUIRED_FIELDS = {
    "agent_name",
    "owner",
    "purpose",
    "prohibited_use",
    "autonomy_tier",
    "risk_level",
    "data_sources",
    "model_provider",
    "tools",
    "memory_policy",
    "approval_policy",
    "eval_suite",
    "budget",
    "audit_requirements",
    "retirement",
    "status",
}


@dataclass(frozen=True)
class ProfileValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]


class LifecycleProfileValidator:
    def validate(self, profile: dict[str, object]) -> ProfileValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
        errors.extend(f"missing required field: {field}" for field in sorted(REQUIRED_FIELDS - set(profile)))
        if profile.get("status") == "retired" and profile.get("tools"):
            errors.append("retired agents must not have active tools")
        if profile.get("risk_level") in {"high", "critical"} and not profile.get("approval_policy"):
            errors.append("high-risk agents require an approval policy")
        if not profile.get("prohibited_use"):
            errors.append("profile must define prohibited use")
        budget = profile.get("budget")
        if not isinstance(budget, dict) or not {"max_model_calls", "max_tool_calls", "max_tokens"}.issubset(budget):
            errors.append("budget must include max_model_calls, max_tool_calls, and max_tokens")
        if profile.get("memory_policy") == "unrestricted":
            warnings.append("unrestricted memory policy is not recommended")
        return ProfileValidationResult(not errors, errors, warnings)


def run_example() -> ProfileValidationResult:
    return LifecycleProfileValidator().validate(
        {
            "agent_name": "service-incident-investigator",
            "owner": "platform-operations",
            "purpose": "Investigate generic service incidents.",
            "prohibited_use": ["automatic production remediation without approval"],
            "autonomy_tier": "assistive",
            "risk_level": "medium",
            "data_sources": ["mock_logs"],
            "model_provider": "mock_or_litellm",
            "tools": ["log_search"],
            "memory_policy": "session_only",
            "approval_policy": "required_for_high_risk_actions",
            "eval_suite": ["policy"],
            "budget": {"max_model_calls": 3, "max_tool_calls": 6, "max_tokens": 1200},
            "audit_requirements": ["request", "outcome"],
            "retirement": {"owner_review_required": True},
            "status": "active",
        }
    )

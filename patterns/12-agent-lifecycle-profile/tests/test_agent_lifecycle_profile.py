from pattern_agent_lifecycle_profile import LifecycleProfileValidator


def valid_profile() -> dict[str, object]:
    return {
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


def test_valid_profile_passes() -> None:
    result = LifecycleProfileValidator().validate(valid_profile())
    assert result.valid is True
    assert result.errors == []


def test_missing_owner_fails_validation() -> None:
    profile = valid_profile()
    profile.pop("owner")
    result = LifecycleProfileValidator().validate(profile)
    assert result.valid is False
    assert "missing required field: owner" in result.errors


def test_retired_agent_cannot_have_active_tools() -> None:
    profile = valid_profile()
    profile["status"] = "retired"
    result = LifecycleProfileValidator().validate(profile)
    assert result.valid is False
    assert "retired agents must not have active tools" in result.errors


def test_unrestricted_memory_warns() -> None:
    profile = valid_profile()
    profile["memory_policy"] = "unrestricted"
    result = LifecycleProfileValidator().validate(profile)
    assert result.valid is True
    assert result.warnings == ["unrestricted memory policy is not recommended"]

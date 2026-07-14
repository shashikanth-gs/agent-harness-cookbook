from agent_harness_cookbook.harness.privilege_broker import ToolPrivilegeBroker, ToolRequest, action_hash
from pattern_tool_privilege_broker import load_policy, propose_restart


def test_prod_restart_requires_approval() -> None:
    decision = propose_restart("prod")
    assert decision.decision == "approval_required"
    assert decision.risk_level == "high"


def test_dev_restart_is_allowed() -> None:
    assert propose_restart("dev").decision == "allow"


def test_unregistered_tool_is_denied() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    decision = broker.evaluate(
        ToolRequest(
            agent_id="ops-investigator",
            user_id="user-123",
            user_roles=["ops-engineer"],
            tool_name="delete_database",
            parameters={},
            environment="prod",
        )
    )
    assert decision.decision == "deny"


def test_wrong_role_is_denied() -> None:
    assert propose_restart("prod", user_roles=["viewer"]).decision == "deny"


def test_dev_read_only_tool_is_allowed_for_matching_tenant_and_role() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    decision = broker.evaluate(
        ToolRequest(
            agent_id="ops-investigator",
            user_id="user-123",
            user_roles=["support-engineer"],
            tool_name="read_logs",
            parameters={"service": "orders-api", "window_minutes": 30},
            environment="dev",
            tenant="retail",
            user_tenants=["retail"],
            action_type="read",
            resource="orders-api",
            original_task="Diagnose orders DLQ issue.",
        )
    )
    assert decision.decision == "allow"
    assert decision.policy_version == "tool-policy-v2"


def test_production_destructive_action_is_denied() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    decision = broker.evaluate(
        ToolRequest(
            agent_id="database-maintenance-agent",
            user_id="admin-123",
            user_roles=["database-admin"],
            tool_name="delete_database",
            parameters={"database": "orders-db"},
            environment="prod",
            tenant="retail",
            user_tenants=["retail"],
            action_type="destructive",
            resource="orders-db",
            original_task="Diagnose orders DLQ issue.",
        )
    )
    assert decision.decision == "deny"
    assert "destructive" in decision.reason


def test_same_tool_denied_for_unentitled_tenant() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    decision = broker.evaluate(
        ToolRequest(
            agent_id="ops-investigator",
            user_id="user-123",
            user_roles=["support-engineer"],
            tool_name="read_logs",
            parameters={"service": "orders-api", "window_minutes": 30},
            environment="prod",
            tenant="marketplace",
            user_tenants=["retail"],
            action_type="read",
            resource="orders-api",
            original_task="Diagnose orders DLQ issue.",
        )
    )
    assert decision.decision == "deny"
    assert decision.reason == "user is not entitled to tenant"


def test_child_agent_cannot_call_parent_only_tool() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    decision = broker.evaluate(
        ToolRequest(
            agent_id="log-reader",
            parent_agent="ops-investigator",
            delegated_by="ops-investigator",
            user_id="user-123",
            user_roles=["ops-engineer"],
            tool_name="restart_service",
            parameters={"service": "orders-api", "environment": "prod"},
            environment="prod",
            tenant="retail",
            user_tenants=["retail"],
            action_type="write",
            resource="orders-api",
            original_task="Diagnose orders DLQ issue.",
        )
    )
    assert decision.decision == "deny"
    assert decision.reason == "agent is not allowed to use tool"


def test_approval_replay_with_changed_parameters_is_rejected() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    approved = ToolRequest(
        agent_id="ops-investigator",
        user_id="user-123",
        user_roles=["ops-engineer"],
        tool_name="restart_service",
        parameters={"service": "orders-api", "environment": "prod"},
        environment="prod",
        tenant="retail",
        user_tenants=["retail"],
        action_type="write",
        resource="orders-api",
        original_task="Diagnose orders DLQ issue.",
    )
    changed = ToolRequest(
        agent_id="ops-investigator",
        user_id="user-123",
        user_roles=["ops-engineer"],
        tool_name="restart_service",
        parameters={"service": "inventory-api", "environment": "prod"},
        environment="prod",
        tenant="retail",
        user_tenants=["retail"],
        action_type="write",
        resource="inventory-api",
        original_task="Diagnose orders DLQ issue.",
        approval_status="approved",
        approval_action_hash=action_hash(approved),
    )
    decision = broker.evaluate(changed)
    assert decision.decision == "deny"
    assert decision.reason == "approval action hash does not match requested action"


def test_approved_exact_action_is_allowed_after_revalidation() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    request = ToolRequest(
        agent_id="ops-investigator",
        user_id="user-123",
        user_roles=["ops-engineer"],
        tool_name="restart_service",
        parameters={"service": "orders-api", "environment": "prod"},
        environment="prod",
        tenant="retail",
        user_tenants=["retail"],
        action_type="write",
        resource="orders-api",
        original_task="Diagnose orders DLQ issue.",
    )
    approved = ToolRequest(
        **{
            **request.__dict__,
            "approval_status": "approved",
            "approval_action_hash": action_hash(request),
        }
    )
    decision = broker.evaluate(approved)
    assert decision.decision == "allow"
    assert decision.reason == "approved action hash matched and policy revalidated"


def test_valid_tool_call_that_violates_original_purpose_is_denied() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    decision = broker.evaluate(
        ToolRequest(
            agent_id="privacy-export-agent",
            user_id="privacy-123",
            user_roles=["privacy-admin"],
            tool_name="export_customer_records",
            parameters={"tenant": "retail", "format": "csv"},
            environment="prod",
            tenant="retail",
            user_tenants=["retail"],
            action_type="export",
            resource="customer-profile",
            original_task="Diagnose orders DLQ issue.",
        )
    )
    assert decision.decision == "deny"
    assert decision.reason == "tool call violates original task purpose"


def test_budget_exhausted_returns_partial_before_tool_call() -> None:
    broker = ToolPrivilegeBroker(load_policy())
    decision = broker.evaluate(
        ToolRequest(
            agent_id="ops-investigator",
            user_id="user-123",
            user_roles=["support-engineer"],
            tool_name="read_logs",
            parameters={"service": "orders-api", "window_minutes": 30},
            environment="prod",
            tenant="retail",
            user_tenants=["retail"],
            action_type="read",
            resource="orders-api",
            original_task="Diagnose orders DLQ issue.",
            budget_remaining=0,
        )
    )
    assert decision.decision == "return_partial"
    assert decision.reason == "budget exhausted before tool call"

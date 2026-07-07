from agent_harness_cookbook.harness.privilege_broker import ToolPrivilegeBroker, ToolRequest
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

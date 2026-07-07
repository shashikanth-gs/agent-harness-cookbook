from __future__ import annotations

import json
from pathlib import Path

from agent_harness_cookbook.harness.privilege_broker import (
    PolicyDecision,
    ToolPrivilegeBroker,
    ToolRequest,
)


FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "tool_policy.json"


def load_policy(path: Path = FIXTURE_PATH) -> dict[str, object]:
    return json.loads(path.read_text())


def propose_restart(environment: str, user_roles: list[str] | None = None) -> PolicyDecision:
    request = ToolRequest(
        agent_id="ops-investigator",
        user_id="user-123",
        user_roles=user_roles or ["ops-engineer"],
        tool_name="restart_service",
        parameters={"service": "orders-api", "environment": environment},
        environment=environment,
    )
    return ToolPrivilegeBroker(load_policy()).evaluate(request)

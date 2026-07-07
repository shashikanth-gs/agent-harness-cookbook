from __future__ import annotations

from agent_harness_cookbook.harness.redaction import redact


def redact_demo_payload() -> dict[str, object]:
    payload = {
        "input": "Investigate order failure for alex@example.com and account-user-abc123.",
        "tool_result": {
            "headers": {"authorization": "Bearer abcdefghijklmnopqrstuvwxyz123456"},
            "payment_hint": "4111 1111 1111 1111",
            "api_key": "sk_abcdefghijklmnop123456",
        },
    }
    return redact(payload)

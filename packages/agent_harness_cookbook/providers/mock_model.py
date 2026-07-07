from __future__ import annotations


class MockModel:
    """A deterministic stand-in for an LLM provider."""

    def complete(self, prompt: str) -> dict[str, object]:
        lowered = prompt.lower()
        if "remediate" in lowered or "restart" in lowered:
            return {
                "intent": "request_remediation",
                "summary": "The user is asking for investigation and a possible operational change.",
                "tokens": 180,
            }
        return {
            "intent": "investigate",
            "summary": "The user is asking for an incident investigation.",
            "tokens": 140,
        }

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from agent_harness_cookbook.harness.redaction import redact


@dataclass(frozen=True)
class TraceStep:
    name: str
    payload: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class DecisionTrace:
    def __init__(self, trace_id: str | None = None) -> None:
        self.trace_id = trace_id or str(uuid4())
        self.steps: list[TraceStep] = []

    def add(self, name: str, payload: dict[str, Any]) -> None:
        self.steps.append(TraceStep(name=name, payload=redact(payload)))

    def as_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "steps": [
                {"name": step.name, "timestamp": step.timestamp, "payload": step.payload}
                for step in self.steps
            ],
        }

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from agent_harness_cookbook.harness.redaction import redact


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    actor: str
    payload: dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class AuditStore:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event_type: str, actor: str, payload: dict[str, Any]) -> AuditEvent:
        event = AuditEvent(event_type=event_type, actor=actor, payload=redact(payload))
        self._events.append(event)
        return event

    def list_events(self) -> list[AuditEvent]:
        return list(self._events)

    def as_dicts(self) -> list[dict[str, Any]]:
        return [
            {
                "event_id": event.event_id,
                "timestamp": event.timestamp,
                "event_type": event.event_type,
                "actor": event.actor,
                "payload": event.payload,
            }
            for event in self._events
        ]

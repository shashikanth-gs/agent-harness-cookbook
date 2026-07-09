from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4


MemoryType = Literal["session", "user_preference", "task_state", "long_term_knowledge", "operational_memory", "audit_record"]


class MemoryWriteRejected(Exception):
    pass


@dataclass(frozen=True)
class MemoryRecord:
    memory_type: MemoryType
    owner_id: str
    key: str
    value: object
    trust_level: str
    validated: bool = False
    record_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class MemoryStore:
    def __init__(self) -> None:
        self._records: dict[str, list[MemoryRecord]] = {kind: [] for kind in MemoryType.__args__}

    def write(self, record: MemoryRecord) -> None:
        if record.memory_type == "audit_record":
            raise MemoryWriteRejected("audit records must be written through the audit system")
        if record.memory_type == "user_preference":
            if record.key not in {"timezone", "notification_channel", "language"} or not record.validated:
                raise MemoryWriteRejected("user preference write requires an allowed key and validation")
        if record.memory_type in {"long_term_knowledge", "operational_memory"} and not record.validated:
            raise MemoryWriteRejected(f"{record.memory_type} writes require validation")
        self._records[record.memory_type].append(record)

    def read(self, memory_type: MemoryType, owner_id: str) -> list[MemoryRecord]:
        return [record for record in self._records[memory_type] if record.owner_id == owner_id]

    def clear_session(self, owner_id: str) -> None:
        self._records["session"] = [record for record in self._records["session"] if record.owner_id != owner_id]


def run_example() -> dict[str, object]:
    store = MemoryStore()
    store.write(MemoryRecord("session", "user-demo", "last_request", "investigate orders", "low"))
    return {"session_records": len(store.read("session", "user-demo"))}

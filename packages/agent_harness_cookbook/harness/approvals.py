from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime, timedelta
from typing import Literal
from uuid import uuid4


ApprovalStatus = Literal["pending", "approved", "edited", "rejected"]


@dataclass(frozen=True)
class ApprovalRequest:
    action: str
    parameters: dict[str, object]
    risk_level: str
    reason: str
    requester_id: str = ""
    request_id: str = ""
    action_hash: str = ""
    approver_id: str | None = None
    expires_at: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    rollback_plan: str = ""
    required_approver_role: str | None = None
    approver_roles: list[str] = field(default_factory=list)
    status: ApprovalStatus = "pending"

    def __post_init__(self) -> None:
        if not self.request_id:
            object.__setattr__(self, "request_id", str(uuid4()))
        if not self.action_hash:
            object.__setattr__(self, "action_hash", self.compute_action_hash())
        if not self.expires_at:
            expires_at = datetime.now(UTC) + timedelta(minutes=15)
            object.__setattr__(self, "expires_at", expires_at.isoformat())

    def compute_action_hash(self) -> str:
        payload = {
            "action": self.action,
            "parameters": self.parameters,
            "risk_level": self.risk_level,
            "requester_id": self.requester_id,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def is_expired(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(UTC)
        return now >= datetime.fromisoformat(self.expires_at)

    def approve(self, approver_id: str | None = None, approver_roles: list[str] | None = None) -> "ApprovalRequest":
        roles = approver_roles or []
        if self.required_approver_role and self.required_approver_role not in roles:
            raise ValueError(f"approval requires approver role: {self.required_approver_role}")
        return replace(self, status="approved", approver_id=approver_id, approver_roles=roles)

    def edit(self, parameters: dict[str, object]) -> "ApprovalRequest":
        return replace(self, parameters=parameters, status="edited", action_hash="")

    def reject(self) -> "ApprovalRequest":
        return replace(self, status="rejected")

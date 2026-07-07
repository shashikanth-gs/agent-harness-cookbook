from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal
from uuid import uuid4


ApprovalStatus = Literal["pending", "approved", "edited", "rejected"]


@dataclass(frozen=True)
class ApprovalRequest:
    action: str
    parameters: dict[str, object]
    risk_level: str
    reason: str
    request_id: str = ""
    status: ApprovalStatus = "pending"

    def __post_init__(self) -> None:
        if not self.request_id:
            object.__setattr__(self, "request_id", str(uuid4()))

    def approve(self) -> "ApprovalRequest":
        return replace(self, status="approved")

    def edit(self, parameters: dict[str, object]) -> "ApprovalRequest":
        return replace(self, parameters=parameters, status="edited")

    def reject(self) -> "ApprovalRequest":
        return replace(self, status="rejected")

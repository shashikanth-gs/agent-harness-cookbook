from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any


REDACTION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("api_key", re.compile(r"\b(?:sk|pk|api|key)_[A-Za-z0-9]{12,}\b", re.IGNORECASE)),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}\b", re.IGNORECASE)),
    ("credit_card", re.compile(r"\b(?:\d[ -]*?){13,16}\b")),
    ("account_ref", re.compile(r"\b(?:acct|account|passenger|user)-[A-Za-z0-9-]{6,}\b", re.IGNORECASE)),
]


def redact_text(value: str) -> str:
    redacted = value
    for label, pattern in REDACTION_PATTERNS:
        redacted = pattern.sub(f"[REDACTED:{label}]", redacted)
    return redacted


def redact(value: Any) -> Any:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, Mapping):
        return {key: redact(inner) for key, inner in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, bytes | bytearray):
        return [redact(inner) for inner in value]
    return value

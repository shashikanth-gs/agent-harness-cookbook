from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetLimits:
    max_model_calls: int = 4
    max_tool_calls: int = 8
    max_retries: int = 1
    max_agent_handoffs: int = 1
    max_retrieved_documents: int = 5
    max_tokens: int = 4000


@dataclass
class BudgetUsage:
    model_calls: int = 0
    tool_calls: int = 0
    retries: int = 0
    agent_handoffs: int = 0
    retrieved_documents: int = 0
    tokens: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "model_calls": self.model_calls,
            "tool_calls": self.tool_calls,
            "retries": self.retries,
            "agent_handoffs": self.agent_handoffs,
            "retrieved_documents": self.retrieved_documents,
            "tokens": self.tokens,
        }


class BudgetExceeded(Exception):
    pass


class BudgetTracker:
    def __init__(self, limits: BudgetLimits) -> None:
        self.limits = limits
        self.usage = BudgetUsage()

    def consume(self, **increments: int) -> None:
        for key, amount in increments.items():
            if amount < 0:
                raise ValueError("budget increments must be non-negative")
            if not hasattr(self.usage, key):
                raise KeyError(f"unknown budget key: {key}")
            setattr(self.usage, key, getattr(self.usage, key) + amount)
        self._enforce()

    def remaining(self) -> dict[str, int]:
        return {
            "model_calls": self.limits.max_model_calls - self.usage.model_calls,
            "tool_calls": self.limits.max_tool_calls - self.usage.tool_calls,
            "retries": self.limits.max_retries - self.usage.retries,
            "agent_handoffs": self.limits.max_agent_handoffs - self.usage.agent_handoffs,
            "retrieved_documents": self.limits.max_retrieved_documents - self.usage.retrieved_documents,
            "tokens": self.limits.max_tokens - self.usage.tokens,
        }

    def _enforce(self) -> None:
        checks = {
            "model_calls": self.usage.model_calls <= self.limits.max_model_calls,
            "tool_calls": self.usage.tool_calls <= self.limits.max_tool_calls,
            "retries": self.usage.retries <= self.limits.max_retries,
            "agent_handoffs": self.usage.agent_handoffs <= self.limits.max_agent_handoffs,
            "retrieved_documents": self.usage.retrieved_documents <= self.limits.max_retrieved_documents,
            "tokens": self.usage.tokens <= self.limits.max_tokens,
        }
        exceeded = [key for key, ok in checks.items() if not ok]
        if exceeded:
            raise BudgetExceeded(f"budget exceeded: {', '.join(exceeded)}")

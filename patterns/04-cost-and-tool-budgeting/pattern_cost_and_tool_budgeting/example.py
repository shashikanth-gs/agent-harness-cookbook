from __future__ import annotations

from agent_harness_cookbook.harness.budgets import BudgetExceeded, BudgetLimits, BudgetTracker


def run_budgeted_flow(extra_tool_call: bool = False) -> dict[str, object]:
    tracker = BudgetTracker(BudgetLimits(max_model_calls=2, max_tool_calls=3, max_tokens=800, max_agent_handoffs=0))
    try:
        tracker.consume(model_calls=1, tokens=140)
        tracker.consume(tool_calls=1)
        tracker.consume(tool_calls=1)
        tracker.consume(model_calls=1, tokens=260)
        if extra_tool_call:
            tracker.consume(tool_calls=2)
        return {"status": "complete", "usage": tracker.usage.as_dict(), "remaining": tracker.remaining()}
    except BudgetExceeded as exc:
        return {
            "status": "partial",
            "reason": str(exc),
            "usage": tracker.usage.as_dict(),
            "remaining": tracker.remaining(),
        }

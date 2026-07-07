# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation changes:

- OWASP LLM Top 10 2025: unbounded consumption and excessive agency.
- OpenTelemetry GenAI semantic conventions: token and model-call telemetry.
- OpenAI Agents SDK docs: usage, results, tools, and tracing.
- Framework docs for LangGraph, Microsoft Agent Framework, CrewAI, and Google
  ADK where they expose retries, loops, or workflow limits.

Design consequence: budgets should cover model calls, tool calls, retries,
handoffs, retrieved documents, execution time, and tokens. Exhaustion should
produce a partial result or escalation, not silent failure.

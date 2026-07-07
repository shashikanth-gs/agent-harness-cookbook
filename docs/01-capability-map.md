# Capability Map

Core harness capabilities:

- tool privilege brokerage,
- human approval gates,
- decision trace and audit,
- cost and tool budgeting,
- redaction boundaries,
- prompt injection and goal hijack mitigation,
- RAG authorization and provenance,
- memory isolation,
- sandboxed execution,
- trajectory evaluation,
- CI/CD evaluation gates,
- lifecycle profiles.

The capabilities should map cleanly to current agent runtimes without requiring
one of them. For example, approval gates can be implemented with LangGraph
interrupts, OpenAI Agents SDK human review, Microsoft Agent Framework workflow
checkpointing, CrewAI flow controls, Google ADK workflow steps, or a custom
runtime pause/resume mechanism.

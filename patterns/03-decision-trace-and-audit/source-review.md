# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation changes:

- OpenAI Agents SDK tracing docs.
- OpenTelemetry GenAI semantic conventions.
- Microsoft Agent Framework workflow observability and checkpointing docs.
- CrewAI observability docs.
- NIST AI RMF and Generative AI Profile: measurement, monitoring, and
  accountability.

Design consequence: capture observable events such as requests, tool calls,
retrieval metadata, policy decisions, approvals, validation, latency, token
usage, and outcomes. Do not store private chain-of-thought.

# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation:

- Framework docs for evals and tracing in OpenAI Agents SDK, Google ADK,
  Microsoft Agent Framework, LangGraph, and CrewAI.
- NIST AI RMF and Generative AI Profile: measurement and monitoring.
- OWASP LLM Top 10 2025: security-oriented eval coverage.

Design consequence: evals should cover full trajectories: final answer quality,
groundedness, tool choice, parameters, policy compliance, approval behavior,
redaction, prompt injection resistance, cost, and latency.

# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation changes:

- OpenAI Agents SDK docs: tools, MCP, guardrails, human review, and tracing.
- Model Context Protocol specification and MCP authorization guidance.
- OWASP LLM Top 10 2025: excessive agency, insecure plugin/tool design,
  sensitive information disclosure, and unbounded consumption.
- Microsoft Agent Framework docs: tools, workflows, checkpointing, and HITL.
- Google ADK docs: tool and agent orchestration concepts.

Design consequence: tool access must be validated outside the model path. The
broker should remain deterministic, identity-aware, policy-driven, auditable,
and adaptable to function tools, MCP tools, framework-native tools, or internal
enterprise tools.

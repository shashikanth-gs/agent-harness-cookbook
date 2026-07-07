# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation:

- OWASP LLM Top 10 2025: prompt injection and excessive agency.
- MCP specification and security guidance for tool/context trust boundaries.
- Framework docs for tool calling and guardrails in OpenAI Agents SDK,
  LangGraph, Microsoft Agent Framework, CrewAI, and Google ADK.
- Current security guidance from recognized security organizations.

Design consequence: the pattern must present layered risk reduction, not a claim
that prompt injection can be fully solved.

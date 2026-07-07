# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation:

- Framework docs for memory in CrewAI, LangGraph, OpenAI Agents SDK,
  Microsoft Agent Framework, Semantic Kernel, and Google ADK.
- OWASP LLM Top 10 2025: sensitive information disclosure and data/model
  poisoning.
- NIST AI RMF and Generative AI Profile: lifecycle governance and privacy.

Design consequence: memory must be separated by type, owner, trust level,
retention, and validation policy. Audit records are not conversational memory.

# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation changes:

- OWASP LLM Top 10 2025: sensitive information disclosure.
- NIST AI RMF and Generative AI Profile: privacy and information integrity.
- MCP authorization and security guidance for tool/context boundaries.
- Provider and framework docs for logging/tracing behavior before storing
  prompts, tool results, or model outputs.

Design consequence: redaction must apply recursively at model, tool, retrieval,
audit, trace, UI, and side-band event boundaries. Regex masking is a teaching
example, not a complete data-loss-prevention system.

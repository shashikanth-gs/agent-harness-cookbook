# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation:

- OWASP LLM Top 10 2025: vector and embedding weaknesses.
- NIST AI RMF and Generative AI Profile: provenance, monitoring, and governance.
- OpenTelemetry GenAI semantic conventions for retrieval telemetry.
- Current framework docs for retrieval, knowledge, citations, and tool/context
  integration.

Design consequence: vector search is not authorization. Retrieval must enforce
identity, tenant/domain labels, document ACLs, lifecycle state, provenance, and
citation validation.

# Control Matrix Overview

The control matrix maps threats to harness control points. It is not a checklist
that makes an agent safe by itself. It is a way to avoid vague controls.

| Threat | Primary Control | Supporting Controls | Evidence |
| --- | --- | --- | --- |
| Direct injection | input guard | instruction/data separator, tool broker | classified input, denied action |
| Indirect RAG injection | retrieval guard | source trust labels, citation validation, tool broker | source id, source hash, decision |
| Tool-result injection | context builder | observation labeling, tool broker, audit | tool result id, reduced scope |
| MCP injection | static scanner | tool broker, source trust, approval gate | MCP metadata finding |
| Skill-file injection | static scanner | authority classifier, tool broker | file finding, blocked capability |
| Memory poisoning | memory write gate | source trust, validation, approval | rejected memory candidate |
| Cross-agent goal hijack | delegation policy | parent/child scope, trace | handoff decision |
| Tool misuse | tool broker | schema validation, approval gate | tool request hash |
| Approval replay | approval gate | action hash, expiry, broker recheck | approval request id |
| Audit gaps | audit sink | schema validation, trace eval | missing event finding |

## Minimum Control Set

For the top five patterns, the minimum serious control set is:

- source trust classification,
- authority vs context labeling,
- purpose-bound tool broker,
- exact-action approval,
- redacted decision trace,
- threat cases,
- trajectory evals.

Without these, the repo remains a set of examples rather than a harness
cookbook.

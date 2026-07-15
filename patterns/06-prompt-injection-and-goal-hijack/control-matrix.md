# Control Matrix

| Threat | Primary Control | Supporting Controls | Expected Evidence |
| --- | --- | --- | --- |
| Direct injection | input guard | tool broker, audit sink | `input.classified`, `injection.detected`, `tool.denied` |
| Indirect RAG injection | source trust classifier | retrieval guard, context builder, tool broker | source id/hash, `tool.denied` |
| Tool-result injection | context builder | observation labeling, tool broker | `tool.observed`, reduced scope |
| MCP injection | static scan | source trust, sandbox, tool broker | `mcp.metadata_scanned`, denied action |
| Skill-file injection | static scan | authority classifier, sandbox, broker | `skill.scanned`, capability denied |
| Memory poisoning | memory write gate | source trust, redaction, audit | `memory.write_denied` |
| Cross-agent hijack | delegation policy | tool broker, trace | `handoff.requested`, `delegation.denied` |
| Detection miss | tool broker | purpose binding, approval gate, audit | `tool.proposed`, `tool.denied` |

## Evaluation Checks

- final answer preserves the original goal,
- untrusted sources require citations,
- unsafe tool proposals are denied or escalated,
- memory poisoning attempts are not persisted,
- delegated agents cannot exceed scope,
- trace records the containment path.

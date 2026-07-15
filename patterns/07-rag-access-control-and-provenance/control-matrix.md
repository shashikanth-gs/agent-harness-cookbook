# Control Matrix

| Threat | Primary Control | Supporting Controls | Expected Evidence |
| --- | --- | --- | --- |
| Unauthorized retrieval | retrieval guard | tenant labels, role ACL | `source.denied` |
| Cross-tenant leakage | tenant filter | chunk ACL, audit | tenant denial |
| Poisoned source | source trust classifier | context labels, tool broker | injection finding |
| Deleted source | lifecycle filter | cache invalidation | `source.excluded` |
| Query expansion | purpose filter | original query trace | scope reduction |
| Missing citation | citation validator | output guard | citation failure |
| Sensitive field | redaction boundary | clearance labels | redaction summary |

## Evaluation Checks

- authorized active documents are cited,
- unauthorized chunks never enter context,
- poisoned authorized docs do not authorize tools,
- deprecated docs include warnings,
- deleted docs are excluded,
- cached chunks are revalidated,
- no-answer behavior avoids hallucination.

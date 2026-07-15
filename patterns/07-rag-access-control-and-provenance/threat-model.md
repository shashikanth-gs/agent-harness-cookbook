# Threat Model

RAG risk comes from treating retrieval as relevance only. Unauthorized,
poisoned, stale, deleted, or overly sensitive chunks can enter model context and
influence answers or tool calls.

## Ingress Surfaces

- retrieval query,
- query rewrite,
- vector index,
- hybrid search results,
- cached context,
- source metadata,
- OpenAPI and AsyncAPI descriptions,
- Confluence runbooks,
- schema fragments,
- model output citations.

## Assets at Risk

- tenant-isolated documents,
- confidential API schemas,
- deleted or unloaded sources,
- source integrity,
- citation trust,
- user-facing answer correctness,
- downstream tool actions based on retrieved evidence.

## Control Points

- retrieval guard,
- pre-retrieval authorization,
- post-retrieval validation,
- source trust classifier,
- context builder,
- citation validator,
- redaction boundary,
- audit sink,
- eval sink.

## Containment Goal

Relevant content should enter context only when it is authorized, active,
properly scoped, and traceable to source metadata. If no authorized source
exists, the agent should say so.

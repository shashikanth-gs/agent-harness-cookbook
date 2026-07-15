# Implementation Spec

## Objective

Implement RAG retrieval as an authorization-aware harness control. Relevance
must not be treated as permission. Only authorized, active, scoped, and
traceable source chunks may enter model context.

## Inputs

- User id, tenant id, roles, and clearance.
- Original user query and any rewritten query.
- Retrieval domain and purpose.
- Candidate documents or chunks.
- Source metadata: tenant, domain, ACL, confidentiality, lifecycle, version,
  hash, ingestion timestamp, owner.
- Cached context, if any.

## Outputs

- Authorized retrieved chunks with provenance.
- Denied or excluded source records for audit.
- Citation metadata for answer validation.
- No-answer result when no authorized active source exists.
- Redaction summary when sensitive fields are masked or omitted.

## Control Flow

```text
query
  -> preserve original task
  -> authorize tenant/domain/role before context
  -> exclude deleted or unloaded sources
  -> mark deprecated sources with warning
  -> revalidate cached context
  -> rank authorized candidates
  -> label retrieved content as evidence
  -> synthesize answer with citations
  -> validate citations against retrieved source ids
```

## Policy Model

Policies should cover:

- tenant and role ACL,
- chunk-level ACL,
- domain labels,
- confidentiality labels,
- lifecycle states,
- source version and hash,
- cache invalidation,
- query rewrite scope,
- citation requirements,
- redaction rules.

## Edge Cases

- Authorized source contains prompt injection.
- Deleted source remains in vector index.
- Query rewrite broadens scope.
- Cached context is no longer authorized.
- Deprecated API is relevant but risky.
- Sensitive schema fields exceed user clearance.
- No authorized source exists.

## Tests

Tests should cover happy path, cross-tenant denial, poisoned authorized source,
deprecated warning, deleted exclusion, cache invalidation, query rewrite
narrowing, citation failure, no-answer behavior, and sensitive field masking.

## What Not To Implement

- Do not rely on vector score as permission.
- Do not put unauthorized chunks into model context.
- Do not treat retrieved text as authority.
- Do not hallucinate when no authorized source exists.

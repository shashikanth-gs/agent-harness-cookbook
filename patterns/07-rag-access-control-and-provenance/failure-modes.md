# Failure Modes

## Vector Search as Authorization

The retriever returns the most similar chunk without checking whether the user
or agent may see it.

## Cross-Tenant Retrieval

Chunks from another tenant are retrieved because they share vocabulary with the
query.

## Poisoned Authorized Source

An authorized document includes instruction-like text that attempts tool misuse.

## Stale or Deleted Context

Deleted, unloaded, or entitlement-invalidated content remains in the index or
cache.

## Query Rewrite Expansion

A rewrite turns a narrow query into a broader request that crosses tenant,
domain, or confidentiality boundaries.

## Citation Failure

The answer makes claims without citing retrieved source ids, or cites a source
that was not retrieved.

## Sensitive Field Exposure

Schema fragments include fields above the user's clearance.

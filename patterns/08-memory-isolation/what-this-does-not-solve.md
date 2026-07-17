# What Memory Isolation Does Not Solve

Memory isolation scopes agent memory to the right tenant, user, task, and agent.
It prevents cross-tenant data leakage through memory boundaries and TTL-based
expiration. It does not solve the following.

## Not Solved

- **Memory storage security.** The isolation layer scopes access. It does not
  encrypt memory at rest, manage storage-level access controls, or enforce
  retention policies. Production deployments need encrypted storage with
  key-per-tenant isolation.

- **Memory poisoning detection.** The isolation layer prevents cross-tenant
  reads. It does not detect whether memory contents within a tenant have been
  poisoned by injection attacks in prior sessions. Memory validation requires
  the injection defense layer (Pattern 06) and memory write gates.

- **Semantic deduplication.** The isolation layer stores and retrieves memory by
  namespace. It does not detect when the same information is stored redundantly
  across sessions, or when contradictory memories exist within a namespace.

- **Right to deletion.** GDPR and similar regulations require the ability to
  delete all data associated with a specific user. The isolation layer scopes
  memory by tenant and user but does not implement cross-system deletion
  workflows that also purge embeddings, audit logs, and cached context.

- **Memory capacity management.** The isolation layer does not limit how much
  memory a tenant or user can consume. Unbounded memory growth requires separate
  quota management.

- **Embedding-level isolation.** If memory uses vector embeddings for retrieval,
  the isolation must extend to the embedding store. Shared embedding indices
  across tenants can leak information through similarity queries even when
  access controls exist at the application layer.

- **Backup and disaster recovery.** The isolation layer operates at runtime. It
  does not address how isolated memory is backed up, restored, or migrated
  across deployments without breaking isolation boundaries.

## Residual Risk

Residual risk remains when memory isolation relies on application-layer
namespace separation without storage-level enforcement, when embedding indices
are shared across tenants, or when memory TTLs are set too long and stale
context influences future decisions.

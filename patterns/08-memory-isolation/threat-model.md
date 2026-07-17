# Threat Model

The Memory Isolation pattern defends against cross-tenant data leakage, Sleeper Agent (delayed injection) attacks, and unauthorized context sharing.

## Ingress Surfaces

- **Long-term Vector Stores:** Databases like Pinecone or ChromaDB used to store past conversation turns.
- **State Checkpointers:** Framework-level persistence mechanisms (like LangGraph's SQLite/Postgres checkpointers) that store the exact graph state.
- **Shared Agent Instances:** A single worker node handling asynchronous requests from multiple disconnected users.

## Assets at Risk

- **Cross-Tenant Data:** Sensitive session information leaking from Tenant A to Tenant B.
- **Identity Spillage:** User A discovering the PII or query history of User B.
- **System Integrity (Sleeper Agents):** A malicious instruction injected into memory today that lies dormant until a high-privileged agent retrieves it weeks later.

## Control Points

- **Composite Key Enforcer:** The database abstraction layer that forces all `read` and `write` operations to include `tenant_id` and `user_id`.
- **Memory Input Guard:** A scanner that re-evaluates retrieved memory for malicious payloads before injecting it into the prompt.
- **Lifecycle Wipers:** Automated background jobs that purge ephemeral memory at the end of a session.

## Failure Boundary

If a memory retrieval request is missing the required identity context (e.g., `user_id` is null), the system must fail closed and return an empty context array rather than returning global or un-scoped memories.

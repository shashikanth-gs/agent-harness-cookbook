# Deployment: Personal Domain vs Multi-Tenant Cloud

When deploying an agent harness, the physical and logical architecture dictates which threat vectors are most critical. The Agent Harness Cookbook identifies two primary deployment architectures: the **Personal Domain** and the **Multi-Tenant Cloud**.

## 1. The Personal Domain (Local/Single-Tenant)
In this model, the agent runs directly on the user's local machine (e.g., a desktop app, a CLI tool) or in an isolated, single-tenant cloud VPC dedicated entirely to one user.
- **Characteristics:** The agent operates under the exact IAM identity of the user. There is no shared memory or shared database.
- **Primary Risk:** **Privilege Escalation via Prompt Injection.** Because the agent has the user's full permissions, if it reads a malicious webpage, the attacker can force the agent to execute actions (like deleting local files or sending emails) as the user.
- **Critical Patterns:**
  - Pattern 09: Sandboxed Execution (to protect the local host).
  - Pattern 01: Tool Privilege Broker (to restrict what local tools the agent can use).
- **Deprioritized Patterns:** Pattern 08 (Memory Isolation) is less critical, as there are no other tenants to leak data to.

## 2. The Multi-Tenant Cloud (SaaS)
In this model, a centralized cluster of worker nodes hosts agent runtimes for thousands of different users and organizations simultaneously.
- **Characteristics:** Memory, databases, and compute resources are shared. The agent's identity is dynamically resolved per request.
- **Primary Risk:** **Cross-Tenant Data Leakage and DoS.** If the agent's context is not cryptographically scoped to the requesting tenant, it will leak one company's secrets to another. Furthermore, a single malicious user can exhaust the API quota for the entire platform.
- **Critical Patterns:**
  - Pattern 08: Memory Isolation (Strict composite key checking).
  - Pattern 04: Cost and Tool Budgeting (Tenant quota registries).
  - Pattern 05: Redaction Boundaries (To ensure PII doesn't leak into shared logs).

## Architectural Implication
You cannot take a harness designed for a Personal Domain and blindly deploy it to a Multi-Tenant Cloud. If you are building a SaaS agent platform, your implementation of the Tool Privilege Broker must explicitly evaluate the `tenant_id` at every single node boundary, forcing the agent to fail closed if the context is missing.

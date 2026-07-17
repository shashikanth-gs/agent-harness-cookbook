# Capability Map

To safely deploy autonomous agents in an enterprise environment, a robust harness must provide a specific set of defensive and operational capabilities. This capability map defines the architectural requirements of the Agent Harness Cookbook.

## 1. Identity & Context Resolution
Before any model is invoked, the harness must resolve exactly who is initiating the action and under what context.
- **Actor Chain Validation:** Tracking the invocation path (User -> Parent Agent -> Child Agent -> Tool).
- **Tenant Isolation:** Enforcing cryptographically secure boundaries so data and execution cannot leak across organizational tenants.
- **Purpose Binding:** Validating that an action aligns with the original business intent, regardless of what the LLM decides.

## 2. Input/Output Interception (The Boundaries)
The harness must sit as a deterministic proxy between the LLM, the user, and the backend systems.
- **Redaction Boundary:** Stripping PII, PHI, and credentials from prompts before hitting external LLM APIs, and preventing hallucinated secrets from reaching the user.
- **Memory Guard:** Scanning retrieved long-term memory for injected payloads (Sleeper Agents) before it enters the context window.
- **RAG Provenance:** Forcing retrieved documents to carry source trust labels and cryptographic hashes to verify origin.

## 3. Execution Governance
When the model proposes an action that mutates the environment (e.g., executing code, modifying a database), the harness must apply strict constraints.
- **Tool Privilege Broker:** A deterministic policy engine evaluating the proposed tool, arguments, and actor chain against RBAC/ABAC rules.
- **Sandboxing:** Executing agent-generated code (Python, bash) in ephemeral, network-isolated containers (e.g., Docker/gVisor) with hard resource quotas.
- **Approval Gates (HITL):** Enforcing cryptographic action hashes to ensure human approvers are signing off on the *exact* parameter set the agent intends to run, preventing replay attacks.

## 4. Operational Controls
Agents are non-deterministic, unbounded loops that can exhaust resources or fail silently.
- **Budget Tracking:** Enforcing hard caps on token consumption, graph depth, and backend compute cost per run and per tenant.
- **Audit & Traceability:** Emitting immutable event logs of every intercepted decision, prompt, and tool call.
- **Lifecycle Enforcement:** Rejecting execution requests for agents marked as `deprecated` or `development` in production environments.

## 5. Continuous Evaluation
Safety boundaries must be continuously tested against model drift and regressions.
- **Trajectory Assertions:** Testing that the harness intercepts and logs a blocked action, rather than just checking if the final answer is safe.
- **CI/CD Evaluation Gates:** Automatically running adversarial prompt fuzzing on every Pull Request before merging harness changes.

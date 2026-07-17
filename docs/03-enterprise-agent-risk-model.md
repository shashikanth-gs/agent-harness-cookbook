# Enterprise Agent Risk Model

Deploying autonomous agents fundamentally shifts the enterprise risk model. Unlike traditional software, which has predictable, deterministic execution paths, an LLM-driven agent uses non-deterministic probabilistic reasoning to decide its own execution path. 

This requires a new taxonomy of risk. The Agent Harness Cookbook categorizes these risks into four primary pillars.

## 1. Goal Hijacking & Prompt Injection
The most pervasive risk in agentic systems is the manipulation of the agent's intent. Because instructions (the system prompt) and data (user inputs, retrieved documents) share the same execution channel (the context window), an attacker can embed instructions within data.
- **Direct Injection:** A user explicitly commands the agent to ignore its rules.
- **Indirect Injection (RAG):** The agent fetches a document from an internal wiki that contains hidden instructions to exfiltrate data.
- **Impact:** The agent abandons its enterprise purpose and becomes a confused deputy, acting on behalf of the attacker.

## 2. Unbounded Agency & Privilege Escalation
Agents are often given access to tools (e.g., `execute_sql`, `delete_user`). If the agent's reasoning engine fails—or if it is hijacked—it may attempt to use these tools outside of its authorized scope.
- **Tenant Bleed:** An agent operating for Tenant A uses a tool to read Tenant B's data because the tenant boundary wasn't enforced at the tool layer.
- **Delegation Escalation:** A low-privileged child agent tricks a high-privileged parent agent into executing a dangerous action.
- **Impact:** Data breaches, destructive infrastructure actions, and compliance violations.

## 3. Data Sovereignty & Exfiltration
Agents often process highly sensitive data (PII, PHI, trade secrets). 
- **API Leakage:** The agent includes sensitive data in its context window, which is then sent to a third-party LLM provider (e.g., OpenAI, Anthropic), violating data residency laws or NDAs.
- **Hallucination Leakage:** The model hallucinates sensitive data (learned during training or leaked from a shared memory pool) and presents it to an unauthorized user.
- **Impact:** Regulatory fines (GDPR/HIPAA), loss of intellectual property, and reputational damage.

## 4. Resource Exhaustion (Denial of Wallet)
Agents operate in loops (e.g., ReAct). An agent can easily get stuck in a failure loop or be intentionally triggered into an infinite recursion by a malicious prompt.
- **Token Exhaustion:** The agent continuously loops, generating massive API bills from the LLM provider.
- **Compute Overload:** The agent repeatedly calls an expensive backend API or database query, taking down internal infrastructure.
- **Impact:** Financial loss, system downtime, and degraded performance for other tenants.

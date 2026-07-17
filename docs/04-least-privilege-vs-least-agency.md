# Least Privilege vs Least Agency

When designing enterprise agents, security teams often attempt to apply traditional IAM (Identity and Access Management) principles. The most common principle is **Least Privilege**. However, for autonomous agents, Least Privilege is necessary but insufficient. We must also design for **Least Agency**.

## Least Privilege (Limiting Access)
Least privilege limits *what an entity can access*. It is the authorization boundary.
- **Example:** An agent is assigned a service account that only has `read` access to the `orders` table in the database. It cannot execute `DROP TABLE`.
- **The Problem:** If an attacker hijacks the agent and forces it to download all 10 million orders and exfiltrate them via a summary email, the agent hasn't violated its privilege (it was allowed to read the table and send emails). 

Least privilege secures the API layer, but it does not secure the agent's intent.

## Least Agency (Limiting Autonomy)
Least agency limits *how much autonomy the entity has to achieve its goal*. It is the operational boundary.
- **Example:** An agent is explicitly scoped to only answer questions about the *last 30 days* of orders, and it is hard-capped at 3 tool calls per session. If it attempts to iterate over the entire database, the harness forcefully terminates its loop.
- **The Goal:** Reduce the agent's autonomy to the bare minimum required to solve the specific task it was designed for.

## Balancing the Two
Enterprise agents require both, but the balance depends entirely on the use case.

1. **High Privilege, Low Agency (The CI/CD Bot):**
   - *Privilege:* Highly privileged (can commit code, merge PRs).
   - *Agency:* Extremely low. It cannot decide *what* to code. It is triggered deterministically by a webhook, runs a strict set of linters, and terminates.
   - *Control:* Heavy loop budgeting and Sandboxing.

2. **Low Privilege, High Agency (The Researcher Bot):**
   - *Privilege:* Extremely low (can only search the public internet).
   - *Agency:* Very high. It can spawn sub-agents, loop for hours, and dynamically adjust its search strategy based on findings.
   - *Control:* Heavy Redaction Boundaries (to prevent leaking internal prompts) and Cost Budgeting.

3. **High Privilege, High Agency (The SRE Bot):**
   - *Privilege:* High (can restart production servers).
   - *Agency:* High (can dynamically diagnose incidents).
   - *Control:* Requires the strictest application of the harness. Every write action requires a **Human-in-the-loop (HITL) Approval Gate**, and memory must be strictly isolated per incident.

The goal of the Agent Harness Cookbook is not to block useful work by turning high-agency agents into brittle scripts. The goal is to make the agent's capabilities explicit, bounded, and deterministic, ensuring that autonomy never supersedes security.

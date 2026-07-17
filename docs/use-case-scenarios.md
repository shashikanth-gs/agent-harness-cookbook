# Use-Case Scenarios

The service incident investigation demo in this cookbook is one illustrative
scenario. The harness patterns apply to any domain where an agent acts on behalf
of users with tools, memory, and retrieval.

This document describes six scenarios across different industries. For each
scenario, it maps which harness patterns are critical and which are optional.
The patterns themselves are domain-agnostic — the same tool privilege broker,
approval gate, and audit trace work whether the agent is investigating an outage
or reviewing a contract.

---

## Scenario 1: Service Incident Investigation (Reference Implementation)

> Orders are not being processed after the latest release. Investigate the
> likely cause and recommend next steps.

**Domain:** Site reliability engineering / DevOps

**Agent capabilities:** Search logs, query metrics, list recent releases, propose
and execute remediation (restart, rollback, config change).

**Why harness controls matter:** The agent has read access to production systems
and may propose write actions (restart, rollback) that could make the situation
worse. Untrusted content in logs and runbooks can contain indirect injection
attempts. Remediation actions are high-risk and difficult to reverse.

**Pattern mapping:**

| Pattern | Role in this scenario | Priority |
| --- | --- | --- |
| 01 Tool Privilege Broker | Allow read tools, require approval for write tools | Critical |
| 02 HITL Approval Gate | Pause before restart or rollback | Critical |
| 03 Decision Trace and Audit | Record investigation steps for post-incident review | Critical |
| 04 Cost and Tool Budgeting | Prevent runaway investigation loops | Important |
| 05 Redaction Boundary | Mask credentials in log excerpts | Important |
| 06 Prompt Injection | Detect injection in retrieved logs and runbooks | Critical |
| 07 RAG Access Control | Authorize access to runbooks by team | Important |
| 08 Memory Isolation | Scope investigation context to the incident | Optional |
| 09 Sandboxed Execution | Sandbox diagnostic scripts | Important |
| 10 Agent Evaluations | Evaluate investigation quality | Important |
| 11 CI/CD Evaluation Gates | Gate agent version deployments | Optional |
| 12 Agent Lifecycle Profile | Track agent version and status | Optional |

This scenario is the reference implementation in the cookbook. See
[service_incident_investigation.py](../packages/agent_harness_cookbook/demos/service_incident_investigation.py).

---

## Scenario 2: Healthcare Clinical Decision Support

> A patient presents with symptoms X, Y, Z. Review their medical history,
> suggest differential diagnoses, and recommend next steps.

**Domain:** Healthcare / clinical operations

**Agent capabilities:** Query electronic health records (EHR), search medical
literature, suggest diagnoses, recommend tests, draft clinical notes, flag
drug interactions.

**Why harness controls matter:** Patient data is highly sensitive (HIPAA, GDPR).
Diagnostic suggestions directly affect patient outcomes. The agent must not
hallucinate drug interactions or miss contraindications. Clinical decisions
require physician review. Data must not cross patient or facility boundaries.

**Pattern mapping:**

| Pattern | Role in this scenario | Priority |
| --- | --- | --- |
| 01 Tool Privilege Broker | Restrict EHR access by provider role and patient relationship | Critical |
| 02 HITL Approval Gate | Require physician approval for treatment recommendations | Critical |
| 03 Decision Trace and Audit | Full audit trail for clinical decision accountability | Critical |
| 04 Cost and Tool Budgeting | Limit queries to relevant records | Optional |
| 05 Redaction Boundary | Redact PHI in model context and logs | Critical |
| 06 Prompt Injection | Detect injection in imported medical records | Important |
| 07 RAG Access Control | Authorize medical literature access, track citations | Critical |
| 08 Memory Isolation | Isolate patient data by facility and provider | Critical |
| 09 Sandboxed Execution | Sandbox any diagnostic calculation code | Optional |
| 10 Agent Evaluations | Evaluate diagnostic accuracy and citation quality | Critical |
| 11 CI/CD Evaluation Gates | Gate model updates that affect clinical recommendations | Critical |
| 12 Agent Lifecycle Profile | Track agent certification status per facility | Important |

**Industry context:** Kaiser Permanente has deployed AI across 40 hospitals.
Healthcare AI generates $600M+ annually in ambient scribe revenue alone.
Clinical decision support agents require the strictest harness controls because
errors directly impact patient safety.

---

## Scenario 3: Financial Compliance and Transaction Processing

> Review this batch of transactions for compliance violations. Flag suspicious
> patterns and prepare a Suspicious Activity Report (SAR) if warranted.

**Domain:** Financial services / compliance

**Agent capabilities:** Query transaction databases, apply compliance rules,
search regulatory guidance, flag suspicious patterns, draft SARs, route
alerts to compliance officers.

**Why harness controls matter:** Financial data is regulated (SOX, PCI-DSS,
AML/KYC). The agent handles personally identifiable financial information.
False negatives in compliance checking create regulatory risk. False positives
waste compliance officer time. Transaction data must not leak across client
boundaries. Agent decisions may be examined by regulators.

**Pattern mapping:**

| Pattern | Role in this scenario | Priority |
| --- | --- | --- |
| 01 Tool Privilege Broker | Restrict transaction access by analyst role and client scope | Critical |
| 02 HITL Approval Gate | Require compliance officer sign-off on SARs | Critical |
| 03 Decision Trace and Audit | Regulatory-grade audit trail with timestamps | Critical |
| 04 Cost and Tool Budgeting | Limit query scope to prevent full-database scans | Important |
| 05 Redaction Boundary | Redact account numbers, SSNs in model context | Critical |
| 06 Prompt Injection | Detect injection in imported transaction metadata | Important |
| 07 RAG Access Control | Authorize access to regulatory guidance by jurisdiction | Important |
| 08 Memory Isolation | Isolate client data in multi-client deployments | Critical |
| 09 Sandboxed Execution | Sandbox rule evaluation scripts | Optional |
| 10 Agent Evaluations | Evaluate detection accuracy against labeled data | Critical |
| 11 CI/CD Evaluation Gates | Gate rule updates that affect compliance decisions | Critical |
| 12 Agent Lifecycle Profile | Track agent approval status per regulatory jurisdiction | Important |

**Industry context:** JPMorgan deployed 450+ AI agents across investment banking
by 2025-2026. Financial agents require the most rigorous audit trails because
regulatory examiners may review agent decisions years after they were made.

---

## Scenario 4: Legal Contract Review

> Review this vendor contract. Identify non-standard clauses, flag high-risk
> terms, and summarize key obligations.

**Domain:** Legal / contract management

**Agent capabilities:** Parse contract documents, compare against standard
templates, identify deviations, flag risk clauses (indemnification, liability
caps, termination), extract key dates and obligations, draft review summaries.

**Why harness controls matter:** Contracts contain confidential business terms.
Missed risk clauses can create significant financial exposure. The agent should
surface risks but not make legal judgments. Contract data must not leak across
client matters. Attorney-client privilege may apply to agent-generated analysis.

**Pattern mapping:**

| Pattern | Role in this scenario | Priority |
| --- | --- | --- |
| 01 Tool Privilege Broker | Restrict document access by matter and attorney role | Critical |
| 02 HITL Approval Gate | Require attorney review of flagged risk clauses | Critical |
| 03 Decision Trace and Audit | Record which clauses were flagged and why | Critical |
| 04 Cost and Tool Budgeting | Limit document processing scope per review | Optional |
| 05 Redaction Boundary | Redact party names and financial terms in logs | Important |
| 06 Prompt Injection | Detect injection in uploaded contract documents | Important |
| 07 RAG Access Control | Authorize access to precedent contracts by matter | Critical |
| 08 Memory Isolation | Isolate client matter data strictly | Critical |
| 09 Sandboxed Execution | Not typically needed | Optional |
| 10 Agent Evaluations | Evaluate clause detection accuracy | Important |
| 11 CI/CD Evaluation Gates | Gate template updates that affect risk scoring | Important |
| 12 Agent Lifecycle Profile | Track agent certification per practice area | Optional |

**Industry context:** Salesforce cut $5M in legal costs through contract
automation. Legal review agents benefit most from RAG access control (Pattern 07)
and memory isolation (Pattern 08) because of strict matter separation
requirements.

---

## Scenario 5: Customer Service Agent

> A customer reports they were charged twice for an order. Investigate the
> issue, apply the appropriate resolution, and update the customer.

**Domain:** Customer service / support

**Agent capabilities:** Query order history, check payment records, apply
refunds or credits, update ticket status, draft customer communications,
escalate to human agents.

**Why harness controls matter:** The agent accesses customer PII and payment
data. Refund actions have direct financial impact. Customer communications
represent the company's brand. The agent must not disclose one customer's data
to another. Automated resolutions must follow company policy.

**Pattern mapping:**

| Pattern | Role in this scenario | Priority |
| --- | --- | --- |
| 01 Tool Privilege Broker | Allow lookups, require approval for refunds above threshold | Critical |
| 02 HITL Approval Gate | Escalate high-value refunds to supervisors | Critical |
| 03 Decision Trace and Audit | Record resolution steps for QA review | Important |
| 04 Cost and Tool Budgeting | Cap automated resolution value per session | Critical |
| 05 Redaction Boundary | Redact credit card numbers, email addresses | Critical |
| 06 Prompt Injection | Detect social engineering in customer messages | Important |
| 07 RAG Access Control | Authorize access to resolution policies | Optional |
| 08 Memory Isolation | Isolate customer data per session | Critical |
| 09 Sandboxed Execution | Not typically needed | Optional |
| 10 Agent Evaluations | Evaluate resolution accuracy and customer satisfaction | Important |
| 11 CI/CD Evaluation Gates | Gate policy changes that affect resolution logic | Optional |
| 12 Agent Lifecycle Profile | Track agent version per support channel | Optional |

**Industry context:** Klarna's AI agent handled the workload of 853 employees
and saved $60M by Q3 2025. Customer service is the most common enterprise AI
agent use case and benefits most from cost budgeting (Pattern 04) and redaction
(Pattern 05).

---

## Scenario 6: Code Review and DevOps Automation

> Review this pull request for security vulnerabilities, test coverage gaps,
> and code quality issues. If approved, deploy to staging.

**Domain:** Software engineering / DevOps

**Agent capabilities:** Read code repositories, run static analysis, execute
test suites, review PR diffs, post review comments, trigger CI/CD pipelines,
deploy to staging environments.

**Why harness controls matter:** The agent has access to source code (IP) and
CI/CD infrastructure. Code execution in review must be sandboxed. Deployment
actions are high-risk. The agent should not merge or deploy without human
approval. Malicious code in PRs could exploit the review agent.

**Pattern mapping:**

| Pattern | Role in this scenario | Priority |
| --- | --- | --- |
| 01 Tool Privilege Broker | Allow reads, require approval for deploy actions | Critical |
| 02 HITL Approval Gate | Require engineer approval before staging deploy | Critical |
| 03 Decision Trace and Audit | Record review findings and deploy decisions | Important |
| 04 Cost and Tool Budgeting | Limit CI resource consumption per review | Important |
| 05 Redaction Boundary | Redact secrets found in code | Critical |
| 06 Prompt Injection | Detect injection in PR descriptions and code comments | Critical |
| 07 RAG Access Control | Authorize access to internal documentation | Optional |
| 08 Memory Isolation | Isolate review context per PR | Optional |
| 09 Sandboxed Execution | Sandbox test execution and static analysis | Critical |
| 10 Agent Evaluations | Evaluate review accuracy against known vulnerabilities | Important |
| 11 CI/CD Evaluation Gates | Gate agent updates that affect review criteria | Critical |
| 12 Agent Lifecycle Profile | Track agent version and approved review scope | Important |

**Industry context:** Code review and DevOps automation agents benefit most from
sandboxed execution (Pattern 09) and prompt injection defense (Pattern 06)
because they process untrusted code that could contain adversarial content
targeting the agent itself.

---

## Cross-Scenario Observations

1. **Patterns 01, 02, and 03 are critical in every scenario.** Tool
   authorization, human approval for high-risk actions, and audit trails are
   universal requirements regardless of domain.

2. **Pattern priority varies by domain.** Healthcare prioritizes redaction and
   memory isolation. Finance prioritizes audit and evaluation gates. DevOps
   prioritizes sandboxing and injection defense.

3. **The harness is domain-agnostic.** The same `ToolPrivilegeBroker`,
   `ApprovalGate`, and `AuditSink` implementations work across all scenarios.
   What changes is the policy configuration: which tools exist, which roles can
   call them, which actions require approval, and what data must be redacted.

4. **Every scenario needs identity propagation.** See
   [Identity and Principal Propagation](identity-and-principal-propagation.md)
   for how user identity flows from authentication through tool calls to backend
   systems.

5. **Every scenario needs infrastructure beyond the harness.** See
   [What This Cookbook Does Not Cover](what-this-cookbook-does-not-cover.md) for
   the broader enterprise stack.

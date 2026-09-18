# Content Plan — Agent Harness Cookbook Series

## Overall Intent

This series teaches enterprise teams how to build a **harness layer** around AI agents — deterministic controls that govern tool access, approval, audit, redaction, and safety regardless of the model or framework underneath.

The 12 patterns covered are a **necessary but not sufficient starting set**. Production deployment requires additional infrastructure (API gateways, identity federation, secret management, network security, compliance frameworks) that the harness depends on but does not implement.

The service incident investigation scenario is the **reference implementation** — one story framing. These patterns apply equally to healthcare, finance, legal, customer service, DevOps, and any domain where agents act on behalf of users with tools, memory, and retrieval.

**Audience:** Engineering leads, platform architects, and security engineers building or evaluating agentic AI systems.

**Tone:** Technical, direct, opinionated. Show working code. State what is proven and what is not. No hype.

**Source repo:** [agent-harness-cookbook](https://github.com/shashikanth-gs/agent-harness-cookbook)

---

## Article Tracker

| # | Slug | Title | Status | Key Points | References | Depends On | Notes |
|---|------|-------|--------|------------|------------|------------|-------|
| 00 | introduction | Introduction to the Agent Harness | published | series scope, 12-pattern overview, cross-domain applicability, authority hierarchy | OWASP Agentic Top 10, NIST AI RMF, Simon Willison lethal trifecta | — | Sets framing for entire series |
| 01 | tool-privilege-broker | Tool Privilege Broker | published | least privilege, action hash, approval binding, budget enforcement | ClawGuard, arxiv 2605.05440, OWASP ASI02 | — | Core pattern, referenced by most others |
| 02 | hitl-approval-gate | HITL Approval Gate | published | hash-bound approval, TTL, escalation, async approval flow | NIST AI RMF, Google DeepMind AI Control Roadmap | 01 | Extends broker with human-in-the-loop |
| 03 | decision-trace-and-audit | Decision Trace and Audit | published | immutable trace, structured events, audit sink interface | HarnessAudit, SOC 2/HIPAA evidence | 01, 02 | Foundation for compliance |
| 04 | cost-budgeting | Cost Budgeting and Rate Governance | published | token budget, cost ceiling, partial-result fallback | — | 01 | Prevents runaway spend |
| 05 | redaction-boundary | Redaction Boundary | published | PII/PHI redaction, regex + NER, redact-before-log | HIPAA Safe Harbor, PCI-DSS | 03 | Must integrate with audit |
| 06 | prompt-injection-defense | Prompt Injection and Goal Hijacking | published | layered containment, input classification, canary tokens, trajectory safety | Simon Willison, Google DeepMind, arxiv 2505.18333, MonitoringBench | 01, 03 | Highest threat pattern |
| 07 | rag-access-control | RAG Source Access Control | published | source trust classification, retrieval guard, tenant-scoped retrieval | SkillInject, AgentDojo | 01, 05 | Critical for multi-tenant |
| 08 | memory-isolation | Memory Isolation | published | tenant-scoped memory, session boundaries, cross-contamination prevention | — | 07 | Pairs with RAG access |
| 09 | sandboxed-execution | Sandboxed Tool Execution | published | container isolation, resource limits, network policy, timeout enforcement | Anthropic Computer Use guidance | 01, 02 | Runtime containment |
| 10 | agent-evaluations | Agent Evaluations | published | scenario-driven evals, outcome grading, regression detection | SciTrace, Agent Audit | 03 | Quality gate |
| 11 | cicd-eval-gates | CI/CD Evaluation Gates | published | pre-deploy eval, threshold enforcement, gate-or-block | — | 10 | Operationalizes evals |
| 12 | agent-lifecycle-profile | Agent Lifecycle Profile | published | agent manifest, version lifecycle, deprecation enforcement, signing | OIDC-A, AIP | 01, 11 | Identity + lifecycle |
| 13 | identity-propagation | Identity and Principal Propagation | planned | OAuth/OIDC, JWT flow, on-behalf-of, delegation chains, harness-to-tool identity | arxiv 2605.05440, OIDC-A, AIP (2603.24775), RFC 8693 | 01, 02, 12 | Cross-cutting concern referenced by many patterns |
| 14 | multi-agent-delegation | Multi-Agent Delegation Safety | planned | parent-child scope, delegation depth limits, capability narrowing, cross-agent audit | arxiv 2603.09002, PCAS | 01, 03, 12 | Builds on broker + lifecycle |
| 15 | observability-integration | Observability and Operational Health | planned | OpenTelemetry export, SIEM integration, alerting on control failures, kill switches | Google DeepMind AI Control Roadmap, CSA Agentic AI Governance | 03, 10 | Connects harness to ops |
| 16 | compliance-evidence | Compliance Evidence Collection | planned | SOC 2 mapping, HIPAA evidence, EU AI Act documentation, audit trail completeness | EU AI Act, NIST AI RMF, Deloitte 2026 AI report | 03, 05 | Regulatory bridge |
| 17 | threat-modeling | Threat Modeling for Agentic Systems | planned | STRIDE for agents, attack surface mapping, control-to-threat mapping | OWASP Agentic Top 10, arxiv 2603.11088, BraveGuard | 06, 07 | Systematic risk assessment |
| 18 | real-world-scenarios | Cross-Domain Scenario Walkthrough | planned | healthcare, finance, legal, customer service — same patterns, different config | Klarna, JPMorgan, Kaiser, Gartner 2026 | all | Tie it all together |

---

## Reference Library

These are trusted sources used across the series. When drafting, cite the most relevant 2-4 per article.

### Standards and Governance
- OWASP Top 10 for Agentic Applications (Dec 2025) — [owasp.org](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)
- NIST AI Risk Management Framework 1.0 and Agent Standards Initiative (Feb 2026)
- EU AI Act enforcement phases (2025–2026)
- Singapore IMDA Agentic AI Governance Framework (Jan 2026, World Economic Forum)
- CSA Agentic AI Governance NIST Profile (Mar 2026)

### Prompt Injection and Safety
- Simon Willison — "The lethal trifecta for AI agents" (private data + untrusted content + ability to act)
- Google DeepMind — "Defeating Prompt Injections by Design" (Apr 2025)
- Google DeepMind AI Control Roadmap (Jun 2026)
- "A Critical Evaluation of Defenses against Prompt Injection Attacks" (arxiv 2505.18333)
- "The Attack and Defense Landscape of Agentic AI" (arxiv 2603.11088)
- "MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring" (arxiv 2605.09684)
- "BraveGuard: From Open-World Threats to Safer Computer-Use Agents" (arxiv 2606.01166)

### Authorization and Identity
- "Authorization Propagation in Multi-Agent AI Systems" (arxiv 2605.05440)
- AIP: Agent Identity Protocol (arxiv 2603.24775)
- OIDC-A: OpenID Foundation agentic identity whitepaper (2025)
- "Trust Without Trusting: A Recomputable Trust Protocol" (arxiv 2605.06738)
- PCAS — agent state as dependency graph with Datalog-derived policies (2026)

### Safety Research
- Stanford Trustworthy AI — fine-tuning attacks bypass guardrails (Claude Haiku 72%, GPT-4o 57%)
- "Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents" (arxiv 2509.26354)
- "SciTrace: Trajectory-Aware Safety Reasoning" (arxiv 2606.08234)
- "Security Considerations for Multi-agent Systems" (arxiv 2603.09002)
- The 2025 AI Agent Index (arxiv 2602.17753)

### Tool-Call Boundary
- ClawGuard — task-specific allowed actions (arxiv 2604.11790)
- AgentDojo — benchmark for prompt injection in tool-calling agents
- SkillInject — injection through tool descriptions
- HarnessAudit — structured audit for harness controls

### Industry
- Microsoft Agent Governance Toolkit (Apr 2026)
- Amazon Bedrock Policy feature for tool access definitions
- Anthropic Computer Use safety guidance — VMs/containers with minimal privileges
- Klarna AI agent — 853 employees' workload (2025)
- JPMorgan — 450+ AI agent deployments (2025–2026)
- Gartner: 40% of enterprise apps embed AI agents by end of 2026

---

## Backlog Ideas

Articles not yet scoped. Add here when an idea surfaces.

- Secret management integration (Vault, cloud KMS, short-lived credentials)
- Network segmentation for agent tool calls
- Model supply chain security (model provenance, signed weights)
- Agent-to-agent authentication protocols
- Incident response runbooks for agentic systems
- Fine-tuning attack surface and defenses
- Data residency and sovereignty in multi-tenant agent systems

# Source Landscape

This repo is a cookbook that translates current agent security and agent
runtime lessons into implementable harness patterns. It is not a replacement for
the projects or papers listed here.

These 12 patterns are a starting set of harness-layer controls. They do not
cover the full enterprise stack required for production agent deployment. See
[What This Cookbook Does Not Cover](what-this-cookbook-does-not-cover.md) for the
broader picture.

---

## Standards and Governance Frameworks

### OWASP Agent Security

OWASP agent security material provides a broad baseline: tool security, least
privilege, prompt injection defense, memory protection, multi-agent security,
output validation, monitoring, and privacy.

Use this repo to convert those concerns into local control points: tool broker,
approval gate, memory write gate, redaction boundary, audit trace, and evals.

The OWASP Top 10 for Agentic Applications (December 2025), built by 100+
security researchers, introduced agent-specific risks including Agent Goal
Hijack (ASI01:2026) and Tool Misuse and Exploitation (ASI02:2026). It works
alongside the NIST AI Risk Management Framework and complements the OWASP Top 10
for LLMs (2025).

Reference:

- https://github.com/OWASP/CheatSheetSeries/issues/2041
- https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/

### NIST AI Risk Management Framework

The NIST AI RMF provides a structured approach to governing AI risk through four
core functions: GOVERN, MAP, MEASURE, and MANAGE. NIST recognized that the
original RMF 1.0 was designed around a premise that humans make the decisions.
In February 2026, NIST announced the AI Agent Standards Initiative, signaling
that purpose-built governance guidance for autonomous systems is a federal
priority.

Reference:

- https://www.nist.gov/artificial-intelligence/ai-risk-management-framework

### EU AI Act

The EU AI Act entered enforcement in stages throughout 2025-2026, with broad
enforcement starting August 2, 2026. Autonomous computer-controlling AI may
fall under high-risk classification requiring additional compliance measures
including human oversight. SOC 2 and GDPR audits increasingly scrutinize AI
agent access patterns.

### Singapore IMDA Agentic AI Governance

In January 2026, Singapore's IMDA launched the world's first governance framework
built specifically for agentic AI, announced at the World Economic Forum in
Davos.

### CSA Agentic AI Governance

The Cloud Security Alliance published an Agentic AI Governance NIST profile in
March 2026, mapping agentic AI risks to the NIST AI RMF structure.

Reference:

- https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/

---

## Prompt Injection and Agent Safety Research

### Simon Willison — The Lethal Trifecta

Simon Willison identified the lethal trifecta of agent vulnerability: if a
system has access to private data, exposure to untrusted content, and a way to
act on that data, it is vulnerable. Prompt injection is the SQL injection of
the AI era. The "Agents Rule of Two" extends this by adding "changing state" as
a fourth property to consider.

Reference:

- https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents
- https://simonw.substack.com/p/new-prompt-injection-papers-agents
- https://simonwillison.net/series/prompt-injection/

### Google DeepMind — Defeating Prompt Injections by Design

Google DeepMind proposed credible design-level solutions to prompt injection
challenges against tool-using LLM systems (April 2025). Their AI Control
Roadmap (June 2026) outlined safeguards for agents deployed inside Google
infrastructure, including monitoring, access controls, and blocking mechanisms
designed to limit damage if alignment fails.

Reference:

- https://deepmind.google/blog/investing-in-multi-agent-ai-safety-research/

### Stanford Trustworthy AI Research

Stanford's Trustworthy AI Research Lab found that model-level guardrails alone
are insufficient. Fine-tuning attacks bypassed Claude Haiku in 72% of cases and
GPT-4o in 57%. This reinforces the cookbook's core premise: deterministic
harness controls must sit outside the model.

### Attack and Defense Surveys

Recent comprehensive surveys document the full landscape of attacks and defenses
for agentic AI systems, including prompt injection, tool misuse, memory
poisoning, and multi-agent goal hijack.

Reference:

- https://arxiv.org/pdf/2603.11088 — The Attack and Defense Landscape of Agentic AI
- https://arxiv.org/pdf/2505.18333 — A Critical Evaluation of Defenses against Prompt Injection Attacks
- https://arxiv.org/pdf/2605.15030 — WARD: Adversarially Robust Defense of Web Agents
- https://arxiv.org/pdf/2605.09684 — MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring
- https://arxiv.org/pdf/2606.01166 — BraveGuard: From Open-World Threats to Safer Computer-Use Agents

---

## Authorization and Identity

### Authorization Propagation in Multi-Agent Systems

Multi-agent systems create a distinct authorization problem: maintaining
authorization invariants as non-human principals retrieve data, delegate tasks,
and synthesize results across changing boundaries. This has been formalized as
a workflow-level property with three sub-problems (transitive delegation,
aggregation inference, temporal validity) and seven structural requirements.

Reference:

- https://arxiv.org/abs/2605.05440

### Agent Identity Protocol (AIP)

AIP addresses the gap in defining agent identity for tool invocation via MCP
and inter-agent collaboration via A2A protocols.

Reference:

- https://arxiv.org/abs/2603.24775

### OIDC-A — Agentic Identity

The OpenID Foundation published a consensus whitepaper on agentic identity in
2025. OIDC-A extends OIDC with agent identity, delegation chain validation,
attestation verification, and capability-based authorization.

### Trust Without Trusting

A recomputable trust protocol for autonomous agents, addressing how trust can
be established without relying on the agent's self-report.

Reference:

- https://arxiv.org/abs/2605.06738

---

## Trajectory Safety and Evaluation

### HarnessAudit

HarnessAudit focuses on full execution trajectories. The central lesson is that
final output correctness does not prove boundary compliance, execution fidelity,
or system stability.

Reference:

- https://arxiv.org/abs/2605.14271
- https://harnessaudit.github.io/

### SciTrace

SciTrace introduces trajectory-aware safety reasoning for scientific discovery
agents, reinforcing the cookbook's position that mid-run behavior matters as
much as final answers.

Reference:

- https://arxiv.org/abs/2606.08234

### Constraint Drift

Research on emergent risks in self-evolving LLM agents identifies constraint
drift as a primary failure vector in long-running deployments, where agents
gradually shift away from their original safety boundaries.

Reference:

- https://arxiv.org/abs/2509.26354

### The 2025 AI Agent Index

A systematic documentation of technical and safety features of deployed agentic
AI systems, providing a baseline for comparing guardrail implementations across
consumer and enterprise agents.

Reference:

- https://arxiv.org/abs/2602.17753

---

## Tool-Call Boundary Research

### ClawGuard

ClawGuard's key lesson is tool-call boundary enforcement. Do not rely only on
model alignment or regex filtering. Derive task-specific allowed actions from
the user's objective and enforce them before tool calls produce real-world
effects.

Reference:

- https://arxiv.org/abs/2604.11790

### AgentDojo

AgentDojo frames agent safety as adversarial tool-use evaluation. Agents operate
over untrusted data, so evals need benign tasks, attack tasks, and
utility/safety tradeoff checks.

Reference:

- https://agentdojo.spylab.ai/
- https://openreview.net/forum?id=m1YYAQjO3w

---

## Supply Chain and Skill-File Attacks

### SkillInject

SkillInject makes skill-file and instruction-file poisoning a first-class
surface. `SKILL.md`, `AGENTS.md`, MCP descriptions, tool descriptions, and local
workflow instructions can become supply-chain inputs to the agent.

Reference:

- https://arxiv.org/abs/2602.20156
- https://www.skill-inject.com/

---

## Static Analysis and CI Scanning

### Agent Audit

Agent Audit adds a static and CI scanning angle: inspect Python agent code,
deployment artifacts, credentials, MCP configs, tool descriptions, and
privilege-risk paths. Findings should be machine-readable so CI can act on them.

Reference:

- https://arxiv.org/html/2603.22853v1

---

## Agent Architecture and Skills

### Skill-Mediated LLM Agents

Architectural patterns and a reference architecture for skill-mediated LLM
agents, including patterns for how agents discover, compose, and execute skills
under governance constraints.

Reference:

- https://arxiv.org/abs/2606.20631

### Pre-Deployment Assurance

Ontology-grounded simulation and trust certification for enterprise AI agents,
addressing how to validate agent behavior before production deployment.

Reference:

- https://arxiv.org/abs/2606.04037

---

## Industry Guidance

### Anthropic

Anthropic recommends running Computer Use agents in virtual machines or
containers with minimal privileges. Per-agent service-account identity with no
shared logins. Vault-based credential injection, never in prompt.

### Google DeepMind

The AI Control Roadmap (June 2026) outlines monitoring, access controls, and
blocking mechanisms for agents deployed inside Google infrastructure.

### Microsoft

The Agent Governance Toolkit (April 2026) provides deterministic policy
enforcement for agent systems.

### Amazon

Bedrock's Policy feature enables declarative tool access definitions, moving
from probabilistic security toward deterministic security.

---

## Agent Runtimes

LangGraph, Deep Agents, OpenAI Agents SDK, and similar runtimes provide useful
execution features: state, sessions, handoffs, tool loops, tracing, approvals,
MCP, persistence, and memory.

The cookbook sits around those runtimes. It describes the controls that teams
need regardless of which runtime they choose.

OpenAI Agents SDK reference:

- https://developers.openai.com/api/docs/guides/agents
- https://openai.github.io/openai-agents-python/tracing/

---

## Multi-Agent Security

### Security Considerations for Multi-Agent Systems

Addresses security challenges specific to systems where multiple agents
interact, delegate, and share state.

Reference:

- https://arxiv.org/abs/2603.09002

---

## Market Context

These patterns are becoming urgent as enterprise agent adoption accelerates:

- Gartner predicts 40% of enterprise applications will embed AI agents by end of
  2026, up from less than 5% in 2025.
- Deloitte's 2026 AI report found only 20% of organizations have mature
  governance models.
- Klarna's AI agent handled the workload of 853 employees in customer service
  by Q3 2025.
- JPMorgan deployed 450+ AI agents across investment banking by 2025-2026.

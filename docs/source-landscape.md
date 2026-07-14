# Source Landscape

This repo is a cookbook that translates current agent security and agent
runtime lessons into implementable harness patterns. It is not a replacement for
the projects or papers listed here.

## OWASP Agent Security

OWASP agent security material provides a broad baseline: tool security, least
privilege, prompt injection defense, memory protection, multi-agent security,
output validation, monitoring, and privacy.

Use this repo to convert those concerns into local control points: tool broker,
approval gate, memory write gate, redaction boundary, audit trace, and evals.

Reference:

- https://github.com/OWASP/CheatSheetSeries/issues/2041
- https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/

## ClawGuard

ClawGuard's key lesson is tool-call boundary enforcement. Do not rely only on
model alignment or regex filtering. Derive task-specific allowed actions from
the user's objective and enforce them before tool calls produce real-world
effects.

Reference:

- https://arxiv.org/abs/2604.11790

## AgentDojo

AgentDojo frames agent safety as adversarial tool-use evaluation. Agents operate
over untrusted data, so evals need benign tasks, attack tasks, and
utility/safety tradeoff checks.

Reference:

- https://agentdojo.spylab.ai/
- https://openreview.net/forum?id=m1YYAQjO3w

## SkillInject

SkillInject makes skill-file and instruction-file poisoning a first-class
surface. `SKILL.md`, `AGENTS.md`, MCP descriptions, tool descriptions, and local
workflow instructions can become supply-chain inputs to the agent.

Reference:

- https://arxiv.org/abs/2602.20156
- https://www.skill-inject.com/

## HarnessAudit

HarnessAudit focuses on full execution trajectories. The central lesson is that
final output correctness does not prove boundary compliance, execution fidelity,
or system stability.

Reference:

- https://arxiv.org/abs/2605.14271
- https://harnessaudit.github.io/

## Agent Audit

Agent Audit adds a static and CI scanning angle: inspect Python agent code,
deployment artifacts, credentials, MCP configs, tool descriptions, and
privilege-risk paths. Findings should be machine-readable so CI can act on them.

Reference:

- https://arxiv.org/html/2603.22853v1

## Agent Runtimes

LangGraph, Deep Agents, OpenAI Agents SDK, and similar runtimes provide useful
execution features: state, sessions, handoffs, tool loops, tracing, approvals,
MCP, persistence, and memory.

The cookbook sits around those runtimes. It describes the controls that teams
need regardless of which runtime they choose.

OpenAI Agents SDK reference:

- https://developers.openai.com/api/docs/guides/agents
- https://openai.github.io/openai-agents-python/tracing/

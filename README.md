# Agent Harness Cookbook

Agent Harness Cookbook is a practical reference for designing enterprise-grade
AI agent harnesses.

It is not a framework. It is not a production platform. It is not a strict
guardrails product. It is a cookbook of patterns, threat cases, reference
implementations, eval cases, and implementation specs.

The goal is not to block every agent action. The goal is to make agent
capabilities explicit, bounded, observable, governable, testable, and auditable.

The repo helps engineers answer:

> I know how to build an agent. What must I consider around the agent to make it
> safer, governable, observable, auditable, reliable, and enterprise-ready?

## Start Here

1. Read [what is an agent harness](docs/00-what-is-an-agent-harness.md).
2. Read [authority vs context](docs/05-authority-vs-context.md).
3. Read the [enterprise threat model](docs/03-enterprise-agent-threat-model.md).
4. Run the service incident investigation demo.
5. Review [Prompt Injection and Goal Hijack](patterns/06-prompt-injection-and-goal-hijack/README.md).
6. Review [Tool Privilege Broker](patterns/01-tool-privilege-broker/README.md).
7. Review [Decision Trace and Audit](patterns/03-decision-trace-and-audit/README.md).

## Core Idea

An agent harness is the layer around an agent that controls how instructions,
tools, memory, retrieved content, approvals, traces, budgets, and evaluations
work together.

The harness repeatedly separates these concepts:

```text
Trusted policy / system instruction = authority
User instruction = task intent
Retrieved document = evidence, not authority
Tool result = observation, not authority
Memory = context, not authority unless validated
Other agent = peer/delegate, not authority unless explicitly delegated
```

This distinction is not enough by itself. The harness must also enforce policy
deterministically at control points such as retrieval, context building,
tool-call authorization, approval, memory writes, output validation, audit, and
evaluation.

## What This Includes

- Pattern articles and implementation specs.
- Threat cases for the highest-risk patterns.
- Self-contained reference packages for implemented patterns.
- Pattern-local tests beside each reference implementation.
- Mock data only. No external services, cloud accounts, real databases, or real
  LLM keys are required.
- Local demo API and lightweight website.
- Prompts that help coding agents implement and review harness patterns.

## Pattern Priority

The repo has twelve patterns, but not all of them should be deepened equally at
the same time. The first five are the core control surface:

1. Prompt Injection and Goal Hijack
2. Tool Privilege Broker
3. RAG Access Control and Provenance
4. HITL Approval Gate
5. Decision Trace and Audit

Supporting patterns connect to those controls:

- Redaction Boundary
- Cost and Tool Budgeting
- Agent Evaluations
- CI/CD Evaluation Gates
- Memory Isolation
- Sandboxed Execution
- Agent Lifecycle Profile

## v1 Patterns

All twelve patterns are grouped under `patterns/`:

- `01-tool-privilege-broker`
- `02-hitl-approval-gate`
- `03-decision-trace-and-audit`
- `04-cost-and-tool-budgeting`
- `05-redaction-boundary`
- `06-prompt-injection-and-goal-hijack`
- `07-rag-access-control-and-provenance`
- `08-memory-isolation`
- `09-sandboxed-execution`
- `10-agent-evaluations`
- `11-ci-cd-evaluation-gates`
- `12-agent-lifecycle-profile`

Each pattern is intended to answer:

1. What can go wrong?
2. Where can unsafe input or action enter?
3. How does it propagate?
4. Which harness control point catches it?
5. What is allowed?
6. What is denied?
7. What requires approval?
8. What should be logged?
9. How is it evaluated?
10. What residual risks remain?

## Demo

The current demo is `service-incident-investigation`, a generic operations
scenario:

> Orders are not being processed after the latest release. Investigate the
> likely cause and recommend next steps.

The demo uses only mock tools: logs, metrics, release events, runbooks, audit,
redaction, budget tracking, and human approval for risky remediation.

The next depth target is to make this demo cover three scenarios:

- normal root-cause investigation,
- indirect injection hidden in logs,
- risky remediation requiring exact-action approval.

## Local Setup

One command:

```bash
make quickstart
```

Or step by step:

```bash
make setup
make dev
```

Open:

- Website: `http://localhost:5173`
- API: `http://localhost:8000`

Run tests:

```bash
make test
```

## Optional Real Provider Testing With Embedded LiteLLM

Mock mode is the default and needs no API keys. To test with real model
providers, use the embedded LiteLLM Python SDK:

```bash
cp .env.example .env
# edit .env:
#   AHC_PROVIDER=litellm
#   AHC_MODEL=openai/gpt-4o-mini
#   OPENAI_API_KEY=...
make dev
```

Provider adapters are optional. The cookbook must remain runnable locally with
mock tools, local JSON fixtures, local policies, local traces, and local evals.

## Repository Shape

```text
patterns/<pattern>/
  README.md
  source-review.md
  article.md
  pattern.md
  threat-model.md
  failure-modes.md
  control-matrix.md
  adoption-levels.md
  implementation-spec.md
  threat-cases.yaml
  eval-cases.md
  what-this-does-not-solve.md
  fixtures/
  pattern_<name>/
  tests/
```

Not every pattern has reached this target structure yet. The priority is to
bring the top five patterns to this shape first.

---
name: agent-harness-cookbook-authoring
description: Use when working on this repository's agent harness cookbook patterns, documentation, threat cases, eval cases, tests, or reference implementations.
---

# Agent Harness Cookbook Authoring Guide

This repository is a practical cookbook for enterprise AI agent harness design.
It is not a framework, production platform, guardrails product, chatbot starter,
or replacement for LangGraph, OpenAI Agents SDK, Deep Agents, Semantic Kernel,
CrewAI, AutoGen, or custom runtimes.

The goal is not to block every agent action. The goal is to make agent
capabilities explicit, bounded, observable, governable, testable, and auditable.

## Core Writing Rule

Write from the harness boundary outward:

```text
unsafe input/action enters
  -> propagates through the agent loop
  -> reaches a harness control point
  -> is allowed, denied, reduced, approved, or audited
  -> becomes an eval assertion
```

Do not write vague pattern summaries. Every pattern must explain:

1. What can go wrong.
2. Where the unsafe input or action enters.
3. How it propagates.
4. Which control point catches it.
5. What is allowed.
6. What is denied.
7. What requires approval.
8. What is logged.
9. How it is evaluated.
10. What residual risk remains.

## Authority vs Context

Use this model consistently:

```text
Trusted policy / system instruction = authority
User instruction = task intent
Retrieved document = evidence, not authority
Tool result = observation, not authority
Memory = context, not authority unless validated
Other agent = peer/delegate, not authority unless explicitly delegated
```

This distinction must be enforced outside the model through retrieval guards,
context builders, tool brokers, approval gates, memory gates, audit traces, and
trajectory evals.

## Required Source Docs

Before changing top-level pattern docs, read:

- `docs/03-enterprise-agent-threat-model.md`
- `docs/05-authority-vs-context.md`
- `docs/07-trajectory-safety.md`
- `docs/control-matrix-overview.md`
- `docs/threat-case-taxonomy.md`
- `docs/evaluation-philosophy.md`
- `docs/risk-adaptive-adoption-levels.md`

These are the source of truth for language, structure, and risk framing.

## Pattern Folder Contract

Each serious pattern should have:

```text
patterns/XX-pattern-name/
  README.md
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

For the top five patterns, this structure is mandatory:

1. `06-prompt-injection-and-goal-hijack`
2. `01-tool-privilege-broker`
3. `07-rag-access-control-and-provenance`
4. `02-hitl-approval-gate`
5. `03-decision-trace-and-audit`

Do not add new patterns until these are deep in docs, implementation, and tests.

## Article Standard

`article.md` is the teaching chapter. It must be deeper than
`threat-cases.yaml`.

Good article sections include:

- enterprise problem,
- ingress surfaces,
- propagation path,
- authority/context distinction,
- control points,
- implementation behavior,
- eval strategy,
- residual risks.

Do not write one-paragraph articles. Do not market the pattern. Do not claim
that a pattern fully prevents a broad class of attacks.

Use containment language:

- detect and record,
- deny action,
- require approval,
- allow with reduced scope,
- fail closed,
- return partial,
- pass with warning,
- residual risk remains.

Avoid:

- bulletproof,
- guarantees safety,
- fully prevents,
- solves prompt injection,
- seamless security.

## Threat Case YAML Standard

Threat cases must be clean, multiline, valid YAML.

Every file should include:

```yaml
pattern: pattern-name
control_points:
  - control_point_name
cases:
  - id: PAT-001
    title: Short scenario title
    ingress_surface: user_input
    benign_goal: What the user legitimately wants.
    malicious_content: What unsafe content or action enters.
    propagation_path:
      - ingress
      - control_point
      - decision
    expected_controls:
      - concrete control behavior
    expected_decision: deny
    audit_events:
      - event.name
    eval_assertion: What the test/eval should prove.
    residual_risk: What remains risky after containment.
```

For a non-malicious but risky case, use `risky_action` instead of
`malicious_content` only when that is clearer. Keep the schema machine-testable.

## Implementation Spec Standard

`implementation-spec.md` should be usable by another coding agent.

Include:

- objective,
- inputs,
- outputs,
- control flow,
- state model,
- policy model,
- edge cases,
- tests,
- expected artifacts,
- what not to implement,
- safety constraints.

Do not describe vague components that do not exist in the repo. Align the spec
with actual or planned local fixtures and tests.

## Eval Case Standard

Evals must inspect trajectories, not only final answers.

Eval dimensions:

- final answer,
- groundedness,
- citation validity,
- authorized retrieval,
- tool selection,
- tool parameter correctness,
- approval behavior,
- policy compliance,
- sensitive data leakage,
- goal preservation,
- cross-agent information flow,
- memory write safety,
- cost and latency,
- failure recovery.

Examples:

- Correct final answer but unauthorized resource accessed: fail.
- Safe final answer but sensitive data appeared in audit: fail.
- Prompt injection appears in retrieved doc and no unsafe tool call occurs: pass
  with warning.
- Human rejected action and graph stopped: pass.

## Implementation Rules

Core harness code in `packages/agent_harness_cookbook/harness/` must remain
framework-agnostic. It should use standard Python structures and local fixtures.

Pattern examples should be split:

- `example.py`: pure Python local reference implementation.
- `langgraph_example.py`: optional adaptation showing how the pure harness can
  wrap a runtime.

Do not put LangGraph, OpenAI Agents SDK, CrewAI, AutoGen, or other runtime
dependencies inside the core harness package.

## Local-First Rule

Everything required for tests and demos should run locally.

Use:

- mock tools,
- local JSON fixtures,
- local policies,
- local traces,
- local eval runners,
- simulated execution.

Do not require:

- cloud accounts,
- real databases,
- Kubernetes,
- real Splunk or Prometheus,
- real OpenAI keys,
- real production APIs.

## Validation

Use the local venv:

```bash
make test
.venv/bin/python -m pytest -q
```

If changing `threat-cases.yaml`, parse the YAML and verify each case has the
required fields.

Do not report a pass count as article content. In docs, explain what behavior is
being tested and what it proves.

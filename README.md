# Agent Harness Cookbook

[![CI](https://github.com/shashikanth-gs/agent-harness-cookbook/actions/workflows/ci.yml/badge.svg)](https://github.com/shashikanth-gs/agent-harness-cookbook/actions/workflows/ci.yml)

Agent Harness Cookbook is a practical reference for designing the control layer
around enterprise AI agents.

It is not an agent framework or hosted platform. It is a collection of patterns,
threat cases, reference implementations, eval cases, and implementation specs
for making agent capabilities explicit, bounded, observable, governable,
testable, and auditable.

Use this repo when you already know how to build an agent and need to answer:

> What must sit around the agent so its tools, memory, retrieval, approvals,
> traces, budgets, and evaluations are safe enough for enterprise use?

## Start Here

1. Read [What Is an Agent Harness?](docs/00-what-is-an-agent-harness.md).
2. Read [Authority vs Context](docs/05-authority-vs-context.md).
3. Read the [Enterprise Agent Threat Model](docs/03-enterprise-agent-threat-model.md).
4. Run the local tests with `make test`.
5. Open the first pattern: [Tool Privilege Broker](patterns/01-tool-privilege-broker/README.md).
6. Then review [Prompt Injection and Goal Hijack](patterns/06-prompt-injection-and-goal-hijack/README.md).
7. Use the [End-to-End Harness Implementation Spec](docs/end-to-end-harness-implementation-spec.md) to see how the patterns connect.

## Quick Start

```bash
make setup
make test
```

Run the local demo app:

```bash
make dev
```

Open:

- Website: `http://localhost:5173`
- API: `http://localhost:8000`

Mock mode is the default. No cloud account, real database, external service, or
LLM API key is required.

## Core Idea

An agent harness is the layer around an agent that decides what the agent may
read, remember, retrieve, call, approve, execute, log, and return.

The harness treats different inputs differently:

```text
Trusted policy / system instruction = authority
User instruction = task intent
Retrieved document = evidence, not authority
Tool result = observation, not authority
Memory = context, not authority unless validated
Other agent = peer/delegate, not authority unless explicitly delegated
```

The distinction only matters if the harness enforces it at concrete control
points: retrieval, context building, tool authorization, approval, memory
writes, redaction, sandboxing, audit, and evaluation.

## Documentation Map

| Topic | Start here |
| --- | --- |
| Architecture | [Reference Architecture](docs/reference-architecture.md) |
| Capabilities | [Capability Map](docs/01-capability-map.md) |
| Framework positioning | [Harness vs Framework vs Platform](docs/02-harness-vs-framework-vs-platform.md) |
| Threat modeling | [Enterprise Agent Threat Model](docs/03-enterprise-agent-threat-model.md) |
| Authority boundaries | [Authority vs Context](docs/05-authority-vs-context.md) |
| Adoption maturity | [Adoption Levels](docs/06-adoption-levels.md) |
| Trajectory evaluation | [Trajectory Safety](docs/07-trajectory-safety.md) and [Evaluation Philosophy](docs/evaluation-philosophy.md) |
| Provider adapters | [Provider Gateway and LiteLLM](docs/08-provider-gateway-and-litellm.md) |
| Coding-agent usage | [How to Use This Repo With Coding Agents](docs/05-how-to-use-this-repo-with-coding-agents.md) |

## Pattern Catalog

Each pattern folder contains local docs, reference code, fixtures, and tests.

| Pattern | Use it when the agent needs to... | Docs |
| --- | --- | --- |
| 01 Tool Privilege Broker | decide whether a tool call is allowed | [README](patterns/01-tool-privilege-broker/README.md), [threat model](patterns/01-tool-privilege-broker/threat-model.md), [control matrix](patterns/01-tool-privilege-broker/control-matrix.md) |
| 02 HITL Approval Gate | pause risky actions for exact-action approval | [README](patterns/02-hitl-approval-gate/README.md), [implementation spec](patterns/02-hitl-approval-gate/implementation-spec.md), [eval cases](patterns/02-hitl-approval-gate/eval-cases.md) |
| 03 Decision Trace and Audit | explain and evaluate what happened during a run | [README](patterns/03-decision-trace-and-audit/README.md), [threat model](patterns/03-decision-trace-and-audit/threat-model.md), [failure modes](patterns/03-decision-trace-and-audit/failure-modes.md) |
| 04 Cost and Tool Budgeting | prevent runaway loops and resource exhaustion | [README](patterns/04-cost-and-tool-budgeting/README.md), [threat model](patterns/04-cost-and-tool-budgeting/threat-model.md), [control matrix](patterns/04-cost-and-tool-budgeting/control-matrix.md) |
| 05 Redaction Boundary | prevent sensitive data from crossing model/tool boundaries | [README](patterns/05-redaction-boundary/README.md), [failure modes](patterns/05-redaction-boundary/failure-modes.md), [control matrix](patterns/05-redaction-boundary/control-matrix.md) |
| 06 Prompt Injection and Goal Hijack | keep untrusted content from becoming authority | [README](patterns/06-prompt-injection-and-goal-hijack/README.md), [threat model](patterns/06-prompt-injection-and-goal-hijack/threat-model.md), [eval cases](patterns/06-prompt-injection-and-goal-hijack/eval-cases.md) |
| 07 RAG Access Control and Provenance | authorize retrieved content and preserve citations | [README](patterns/07-rag-access-control-and-provenance/README.md), [implementation spec](patterns/07-rag-access-control-and-provenance/implementation-spec.md), [control matrix](patterns/07-rag-access-control-and-provenance/control-matrix.md) |
| 08 Memory Isolation | keep memory scoped to the right tenant, user, task, and agent | [README](patterns/08-memory-isolation/README.md), [threat model](patterns/08-memory-isolation/threat-model.md), [failure modes](patterns/08-memory-isolation/failure-modes.md) |
| 09 Sandboxed Execution | run generated code without trusting the host | [README](patterns/09-sandboxed-execution/README.md), [threat model](patterns/09-sandboxed-execution/threat-model.md), [control matrix](patterns/09-sandboxed-execution/control-matrix.md) |
| 10 Agent Evaluations | test trajectories, not only final answers | [README](patterns/10-agent-evaluations/README.md), [eval cases](patterns/10-agent-evaluations/eval-cases.md), [failure modes](patterns/10-agent-evaluations/failure-modes.md) |
| 11 CI/CD Evaluation Gates | block regressions before deployment | [README](patterns/11-ci-cd-evaluation-gates/README.md), [implementation spec](patterns/11-ci-cd-evaluation-gates/implementation-spec.md), [threat model](patterns/11-ci-cd-evaluation-gates/threat-model.md) |
| 12 Agent Lifecycle Profile | bind runtime behavior to agent identity and lifecycle | [README](patterns/12-agent-lifecycle-profile/README.md), [threat model](patterns/12-agent-lifecycle-profile/threat-model.md), [control matrix](patterns/12-agent-lifecycle-profile/control-matrix.md) |

## Demo

The main demo is `service-incident-investigation`, a mock operations scenario:

> Orders are not being processed after the latest release. Investigate the
> likely cause and recommend next steps.

The demo covers:

- normal root-cause investigation,
- indirect injection hidden in logs and retrieved content,
- risky remediation requiring exact-action approval,
- budget tracking, redaction, audit, and trajectory evaluation.

Relevant entry points:

- [Raw Python workflow](packages/agent_harness_cookbook/demos/service_incident_investigation.py)
- [LangGraph workflow](packages/agent_harness_cookbook/demos/service_incident_langgraph.py)
- [End-to-end harness](packages/agent_harness_cookbook/demos/end_to_end_harness.py)
- [End-to-end tests](tests/test_end_to_end_harness.py)

## Optional Real Provider Testing

The default provider is a deterministic mock. To test with a real model through
LiteLLM:

```bash
cp .env.example .env
# edit .env:
#   AHC_PROVIDER=litellm
#   AHC_MODEL=openai/gpt-4o-mini
#   OPENAI_API_KEY=...
make dev
```

Provider adapters are optional. The cookbook should remain runnable with local
mocks, local policies, local traces, and local evals.

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

## Development

```bash
make test
.venv/bin/python -m compileall packages patterns
npm --prefix apps/demo-site run build
```

CI runs these checks on push and pull request.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). For coding-agent workflows, see
[How to Use This Repo With Coding Agents](docs/05-how-to-use-this-repo-with-coding-agents.md).

## License

[MIT](LICENSE)

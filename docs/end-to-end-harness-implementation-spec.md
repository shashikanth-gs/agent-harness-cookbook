# End-to-End Harness Implementation Spec

## Objective

Implement one local, executable end-to-end harness workflow that demonstrates
how patterns `01` through `12` compose around a single service incident
scenario.

This is not a new framework, provider, UI, or production adapter. It is a
spec-driven reference workflow that uses existing harness primitives and mock
data so tests can inspect the full trajectory.

## Scenario

User asks the agent to investigate delayed order processing after a deployment
and optionally remediate if safe.

The workflow must include:

- direct user input classification,
- authorized RAG evidence with a poisoned instruction,
- tool-result injection inside mock logs,
- tenant and role-bound tool decisions,
- production remediation requiring exact-action approval,
- approved-action revalidation,
- budget accounting,
- redacted audit and trace,
- sandboxed execution boundary,
- memory isolation boundary,
- deterministic trajectory evaluation,
- CI/CD gate signal,
- lifecycle manifest validation.

## Inputs

- `user_request: str`
- `approve_remediation: bool = False`
- `tamper_manifest: bool = False`
- `force_budget_exhaustion: bool = False`

## Outputs

Return a dictionary with:

- `status`: `completed`, `waiting_for_approval`, `partial`, or `denied`
- `summary`
- `evidence`
- `remediation`
- `budget`
- `audit`
- `trace`
- `pattern_coverage`
- `evaluation`

## Pattern Mapping

| Pattern | Required Control Event | Required Assertion |
| --- | --- | --- |
| `01-tool-privilege-broker` | `tool.decision` | broker records allow, deny, approval, or revalidation with action hash |
| `02-hitl-approval-gate` | `approval.requested` / `approval.approved` | production write pauses or revalidates exact approved action |
| `03-decision-trace-and-audit` | `audit.trace_checked` | trace contains policy versions, source ids, action hash, approval id, redaction summary, budget usage |
| `04-cost-and-tool-budgeting` | `budget.consumed` / `budget.exhausted` | budget usage is recorded and exhaustion returns partial |
| `05-redaction-boundary` | `redaction.checked` | sensitive values do not appear in result, audit, or trace |
| `06-prompt-injection-and-goal-hijack` | `injection.detected` | injected text is not allowed to authorize action |
| `07-rag-access-control-and-provenance` | `source.authorized` | only authorized sources enter context with provenance |
| `08-memory-isolation` | `memory.scope_checked` | tenant-scoped memory does not cross into another tenant |
| `09-sandboxed-execution` | `sandbox.evaluated` | unsafe network execution is denied by sandbox policy |
| `10-agent-evaluations` | `trajectory.evaluated` | trajectory evaluator passes only when controls fired |
| `11-ci-cd-evaluation-gates` | `ci.gate_evaluated` | local gate signal passes for the safe trajectory |
| `12-agent-lifecycle-profile` | `lifecycle.verified` | signed manifest is valid; tampering fails closed |

## Control Flow

```text
validate lifecycle manifest
  -> classify user request
  -> check memory scope
  -> retrieve authorized source evidence
  -> classify and sanitize poisoned source text
  -> broker read tools
  -> classify and sanitize poisoned tool results
  -> enforce sandbox boundary
  -> synthesize local answer from safe evidence
  -> broker production remediation
  -> request exact-action approval when needed
  -> optionally approve and revalidate exact action
  -> record budget, trace, audit, redaction, and CI gate signals
  -> evaluate trajectory
```

## What Not To Implement

- Do not call external LLMs, cloud services, databases, or production APIs.
- Do not execute remediation tools.
- Do not add a UI or provider.
- Do not use LangGraph as a required dependency for this workflow.
- Do not claim the workflow prevents all prompt injection.

## Tests

Add tests that prove:

- all 12 pattern ids are covered by event-backed assertions,
- poisoned RAG and log instructions are contained,
- production remediation requires approval by default,
- approved remediation revalidates the exact action hash,
- tampered lifecycle manifest fails closed,
- forced budget exhaustion returns partial,
- audit and trace are redacted and contain required governance fields.

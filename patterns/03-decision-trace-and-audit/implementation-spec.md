# Implementation Spec

## Objective

Implement a structured decision trace that records observable trajectory events
without storing private chain-of-thought.

## Inputs

- Run id, trace id, parent run id.
- User, tenant, session, and agent identity.
- Agent, model, prompt, tool-policy, budget-policy, and retrieval-policy
  versions.
- Input and source classifications.
- Retrieved source ids and chunk hashes.
- Tool proposals and action hashes.
- Broker decisions.
- Approval requests and resolutions.
- Redaction summaries.
- Budget usage.
- Output classification and final status.

## Outputs

- Ordered trace events.
- Redacted audit payloads.
- Reconstructable run history.
- Eval-ready trajectory data.

## Control Flow

```text
request received
  -> trace started
  -> input/source classifications recorded
  -> retrieval and context events recorded
  -> tool proposals and decisions recorded
  -> approval events recorded
  -> redaction and budget events recorded
  -> final outcome recorded
  -> trajectory eval consumes trace
```

## Event Classification

Classify events as:

- model suggestion,
- policy decision,
- human approval,
- tool observation,
- system validation.

## Storage Model

The local implementation can use in-memory or JSON-like traces. Production
adaptations may use append-only JSONL, hash-chained events, OpenTelemetry, SIEM
export, WORM retention, or cloud log analytics.

## Edge Cases

- Denied tool call.
- Approval rejection.
- Injection detected.
- Injection missed but broker blocks action.
- Cross-agent handoff.
- Redaction before audit.
- Budget exhaustion.
- Partial result.

## Tests

Tests should check ordered steps, redaction, no private reasoning requirement,
denied action visibility, approval traceability, handoff correlation, budget
events, and eval readiness.

## What Not To Implement

- Do not store private chain-of-thought.
- Do not store raw secrets.
- Do not treat logs as a substitute for decision trace.
- Do not rely only on final answer inspection.

# Decision Trace and Audit

Decision Trace and Audit is the pattern that makes an agent run
reconstructable. It is not generic logging and it should not store private
chain-of-thought. It records observable evidence: who asked, which agent acted,
which sources entered context, which tool calls were proposed, which policies
decided, which approvals happened, what was redacted, what budget was consumed,
and how the run ended.

Final answer safety is insufficient. A run can produce a safe final answer after
attempting an unauthorized retrieval, unsafe tool call, approval replay, memory
write, or cross-agent handoff. The trace is what lets evaluation and forensics
see those mid-trajectory events.

## Decision vs Observation

Classify events:

- model suggestion: untrusted proposal,
- policy decision: deterministic broker or guard decision,
- human approval: accountable reviewer decision,
- tool observation: data returned by a tool,
- system validation: schema, redaction, budget, or state check.

This distinction matters. A model suggestion to restart production is not the
same thing as a broker decision allowing restart.

## What to Capture

A serious trace should include:

- run id and trace id,
- parent run id for handoffs,
- user, tenant, and session,
- agent id and version,
- model and prompt versions,
- tool, budget, and retrieval policy versions,
- input classification,
- source trust classifications,
- retrieved source ids and chunk hashes,
- tool request id and action hash,
- tool decision,
- approval request id and actor,
- redaction summary,
- output classification,
- token usage, cost estimate, and latency,
- final status and failure reason.

## Storage Options

The local cookbook can use JSON-like traces. Production systems may use
append-only files, hash-chained events, SIEM export, OpenTelemetry, WORM
retention, or cloud log analytics. The storage can vary; the event semantics
should remain stable.

## Evaluation Focus

Trace evals should answer:

- did an unsafe proposal occur,
- which control caught it,
- was sensitive data redacted before audit,
- did approval bind to the exact action,
- did denied actions stay denied,
- did budget exhaustion return partial,
- can a reviewer reconstruct the run without hidden reasoning.

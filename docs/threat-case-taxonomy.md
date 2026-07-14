# Threat Case Taxonomy

Threat cases should be concrete enough that a developer can turn them into
fixtures and tests.

Each threat case should include:

- id,
- title,
- pattern,
- ingress surface,
- attacker goal,
- benign user goal,
- malicious content,
- propagation path,
- expected control point,
- expected decision,
- audit events,
- eval assertion,
- residual risk.

## Decision Vocabulary

Use consistent decision terms:

- `allow`,
- `deny`,
- `approval_required`,
- `allow_with_reduced_scope`,
- `return_partial`,
- `escalate`.

## Outcome Vocabulary

Use precise outcome language:

- detects and records,
- contains failure,
- blocks action,
- requires approval,
- fails closed,
- returns partial evidence,
- passes with warning,
- residual risk remains.

Avoid claiming complete prevention for a broad class of attacks.

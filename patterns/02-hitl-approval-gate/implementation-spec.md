# Implementation Spec

## Objective

Implement an approval gate that pauses only when policy requires human judgment
and binds approval to an exact action object.

## Inputs

- Broker decision.
- Proposed action object.
- Action hash.
- Requested user and agent.
- Parent agent, if delegated.
- Tool name, parameters, resource, environment, risk, blast radius.
- Evidence references.
- Rollback plan and idempotency.
- Expiration and required approver role.
- Human decision: approve, edit, reject, or escalate.

## Outputs

- Approval request with stable id and action hash.
- Resolution event.
- Resume decision.
- Edited action requiring a new hash.
- Stopped status on rejection.
- Escalation when approver policy fails.

## Control Flow

```text
broker decision
  -> if low risk, record approval.skipped
  -> if approval_required, build exact action request
  -> reviewer approves, edits, rejects, or escalates
  -> validate actor, expiry, and action hash
  -> broker revalidates approved action
  -> resume or stop graph
```

## Policy Model

Policies should define:

- which risk levels require approval,
- required approver role by action type and environment,
- separation of duties,
- expiration window,
- required evidence fields,
- whether edits create a new request,
- broker revalidation requirement.

## Edge Cases

- Human edits action before approving.
- Approval expires.
- Requester approves own high-risk action.
- Approval is replayed with changed parameters.
- Evidence or rollback plan is missing.
- Broker policy changes after approval.

## Tests

Tests should cover approval skip, approval request creation, approve, edit,
reject, expiry, self-approval escalation, evidence requirements, and broker
revalidation.

## What Not To Implement

- Do not approve vague intent.
- Do not execute directly from the approval gate.
- Do not skip broker revalidation.
- Do not allow changed parameters to reuse the original approval.

# Implementation Spec

## Objective

Implement a deterministic broker that evaluates proposed tool actions before
execution. The broker must not execute the tool. It returns a decision object
with reason, risk, policy version, action hash, and audit fields.

The broker is the containment layer for prompt injection, delegated-agent abuse,
overbroad tools, approval replay, tenant leakage, purpose mismatch, and budget
exhaustion.

## Inputs

`ToolRequest` includes:

- user identity and roles,
- tenant and user tenant entitlements,
- agent identity and parent/delegation fields,
- tool name, version, category, and parameters,
- action type,
- resource and resource owner,
- environment,
- original user task,
- risk and blast radius,
- approval status and approval action hash,
- budget remaining,
- rollback and idempotency metadata,
- network boundary.

## Outputs

`PolicyDecision` includes:

- `decision`: `allow`, `deny`, `approval_required`, `allow_with_reduced_scope`,
  `return_partial`, or `escalate`,
- reason,
- risk level,
- action hash,
- policy version,
- required approver role when applicable,
- audit payload.

## Control Flow

```text
ToolRequest
  -> compute exact action hash
  -> load tool policy
  -> check budget
  -> check role and tenant
  -> check agent and delegated child scope
  -> check action type and resource
  -> check network boundary
  -> validate parameters
  -> deny destructive actions
  -> enforce purpose binding
  -> evaluate environment decision
  -> validate approval hash if already approved
  -> return PolicyDecision
```

## Policy Model

The policy is local JSON in the playground. Each tool can define:

- risk,
- allowed roles,
- allowed tenants,
- allowed agents,
- allowed child agents,
- allowed action types,
- allowed resources,
- purpose terms,
- required approver role,
- allowed parameters,
- environment decisions,
- destructive flag.

## Purpose Binding

Purpose binding checks that the tool action serves the original user task. A
valid tool can still be denied when the task does not justify it.

Example:

```text
Original task: Diagnose orders DLQ issue.
Allowed: read orders logs, read metrics, read deployment events.
Not allowed: export customer records, restart payment-service, read HR data.
```

## Action Hash

The action hash binds approval to the exact action object:

- agent id,
- user id,
- tenant,
- tool name and version,
- action type,
- resource,
- environment,
- parameters,
- risk and blast radius,
- original task.

If parameters or resource change after approval, the hash changes and approval
is invalid.

## Tests

The tests cover:

- production restart requiring approval,
- development restart allowed,
- unregistered or wrong-role tool use denied,
- dev read-only evidence collection allowed,
- destructive production action denied,
- tenant entitlement denied,
- child-agent scope denied,
- approval replay with changed parameters rejected,
- exact approved action allowed after revalidation,
- valid tool denied when purpose mismatches,
- budget exhaustion returning partial before tool work.

## What Not To Implement

- Do not execute tools from the broker.
- Do not call external policy engines.
- Do not rely on the model to self-authorize.
- Do not allow vague approval to authorize changed action parameters.

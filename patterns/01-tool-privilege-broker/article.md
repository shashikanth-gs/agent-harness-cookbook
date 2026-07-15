# Tool Privilege Broker

The Tool Privilege Broker is the deterministic boundary between an agent's
suggestion and real tool authority. The model can propose an action, but the
broker decides whether that exact action is allowed, denied, requires approval,
should run with reduced scope, or should return partial because a budget or
policy boundary has been reached.

This pattern is not a simple allowlist. Enterprise tool governance needs user
identity, tenant, role, agent identity, delegated agent scope, tool version,
action type, resource, environment, parameters, original user task, approval
state, budget, rollback availability, and audit metadata.

## Why This Matters

Prompt injection containment depends on tool-boundary enforcement. A poisoned
document may cause the model to propose `restart_service`. The broker must still
ask whether restart is in scope for the original task, whether the user and
agent are allowed to use it, whether the target tenant and environment are
allowed, and whether a human approved the exact action.

## Purpose Binding

Purpose binding connects a tool call to the original task:

```text
Original task: Diagnose orders DLQ issue.
Allowed: read orders logs, read metrics, read deployment events.
Not allowed: export customer records, restart payment-service, read HR data.
```

A tool can be valid and still be denied because it does not serve the task.

## Exact Action Approval

Human approval must bind to the exact action object. The action hash should
cover tool name, parameters, resource, environment, risk, requester, agent,
tenant, and purpose. If any of these change, the approval is invalid.

This prevents approval replay:

```text
Approved: rollback orders-api in prod.
Attempted: rollback payment-service in prod.
Decision: deny.
```

## Delegation

Child agents do not automatically inherit parent tools. A parent may delegate
log reading to a child agent without delegating rollback authority. The broker
must check parent agent, child agent, allowed child tools, tenant, and resource.

## Budget and Partial Results

The broker should also respect runtime budgets. If a run has no tool budget
remaining, the decision should be `return_partial` before another tool call is
authorized.

## Implementation

The reference broker evaluates `ToolRequest` against a local JSON policy. It
does not execute the tool. It returns a `PolicyDecision` with decision, reason,
risk level, policy version, action hash, optional approver role, and audit
payload.

Run:

```bash
.venv/bin/python -m pytest -q patterns/01-tool-privilege-broker/tests
```

The verification scenarios cover production approval, development allow,
destructive denial, tenant mismatch, child-agent scope, approval replay, exact
approved action revalidation, purpose mismatch, and budget exhaustion.

# Tool Privilege Broker

The Tool Privilege Broker is the deterministic boundary between an agent's
suggestion and real tool authority. The model can propose an action, but the
broker decides whether that exact action is allowed, denied, requires approval,
should run with reduced scope, or should return partial because a budget or
policy boundary has been reached.

This pattern is not a simple allowlist. Enterprise tool governance needs the
full action context: actor chain, user identity, agent identity, delegated
agents, tenant, resource owner, original task purpose, parameters, environment,
blast radius, rollback, approval state, budget, policy version, and audit
metadata.

## Why This Matters

Prompt injection containment depends on tool-boundary enforcement. A poisoned
document may cause the model to propose `restart_service`. The broker must still
ask whether restart is in scope for the original task, whether the user and
agent are allowed to use it, whether the target tenant and environment are
allowed, and whether a human approved the exact action.

The broker turns agent intent into a governed action decision. That decision is
outside the model and should fail closed when required policy is missing.

## Actor Chain

Every tool request should carry the actor chain:

```text
user -> parent agent -> child agent -> tool
```

The user may have tenant and role entitlements. The parent agent may have broad
coordination authority. The child agent may have only read-only delegated scope.
The broker should evaluate the whole chain, not only the tool name.

Important fields:

- `user_id`,
- `user_roles`,
- `tenant`,
- `user_tenants`,
- `agent_id`,
- `agent_version`,
- `parent_agent`,
- `delegated_by`.

## User, Agent, and Delegation Checks

A user role check is necessary but not sufficient. The broker also needs to know
which agent is acting and whether that agent is acting as a delegated child.

Example:

```text
Parent agent: incident-manager
Child agent: log-reader
Delegated scope: read logs and metrics
Attempted action: rollback_deployment
Decision: deny
```

This prevents lower-privilege agents from gaining authority by routing work
through another part of the graph.

## Tenant Boundary and Resource Ownership

Tools must be scoped by tenant and resource. A valid log-reading tool is unsafe
when it reads another tenant's logs. A valid remediation tool is unsafe when it
targets a resource outside the user's task.

The broker should check:

- requested tenant against user entitlement,
- tool policy against allowed tenants,
- resource against allowed resources,
- resource owner when ownership matters,
- network boundary when tools cross environments.

## Purpose Binding

Purpose binding connects a tool call to the original task:

```text
Original task: Diagnose orders DLQ issue.
Allowed: read orders logs, read metrics, read deployment events.
Not allowed: export customer records, restart payment-service, read HR data.
```

A tool can be valid and still be denied because it does not serve the task. This
is how the broker contains many prompt-injection misses. If the model proposes a
production action unrelated to the task, the broker rejects it even if the
injection detector missed the malicious text.

## Parameter Schema Validation

The broker must validate both parameter names and values. Unknown parameters
should fail closed. Constrained values should be checked against policy.

Example:

```text
Allowed parameter: service in [orders-api, inventory-api]
Attempted parameter: service = payment-service
Decision: deny
```

This prevents a model from using a valid tool with a resource or option that was
not intended by policy.

## Environment Policy

The same action can have different decisions by environment:

```text
read_logs in dev: allow
read_logs in prod: allow
restart_service in dev: allow
restart_service in prod: approval_required
delete_database in prod: deny
```

Environment policy should be explicit. Missing environment rules should fail
closed.

## Blast Radius, Rollback, and Idempotency

Production write actions need more than a role check. The approval request or
decision record should carry blast radius, rollback availability, and
idempotency. A safe approval flow should ask:

- What resource changes?
- How many users or tenants can be affected?
- Can the action be rolled back?
- Is the action idempotent?
- What evidence supports the action?

These fields help the HITL Approval Gate decide whether the action is reviewable
and what role should approve it.

## Action Hash and Approval Binding

Human approval must bind to the exact action object. The action hash should
cover:

- tool name,
- tool version,
- parameters,
- resource,
- environment,
- tenant,
- risk,
- blast radius,
- requester,
- agent,
- original task.

If any of these change, approval is invalid.

Example:

```text
Approved: rollback orders-api in prod.
Attempted: rollback payment-service in prod.
Decision: deny.
```

This prevents approval replay and parameter swapping after review.

## Budget State

The broker should check runtime budget before authorizing a tool call. If no
tool budget remains, the decision should be `return_partial`. This avoids a
common failure mode where an agent keeps gathering evidence after the run should
have stopped.

Budget state belongs in the same decision path as tool policy because both
determine whether another tool call is allowed.

## Policy Versioning and Audit

Every decision should carry the policy version and enough audit metadata to
reconstruct the action:

- tool name,
- agent id,
- user id,
- tenant,
- environment,
- resource,
- action type,
- action hash,
- decision,
- reason.

This matters for incident review. A denial without policy version or action
hash is hard to evaluate later.

## Fail-Closed Behavior

The broker should deny when:

- the tool is not registered,
- the environment decision is missing or invalid,
- the user role is not allowed,
- tenant entitlement is missing,
- the agent or child agent is not allowed,
- parameter schema validation fails,
- purpose binding fails,
- approval hash does not match,
- policy is malformed.

Failing closed is what makes the broker a boundary instead of a logging layer.

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

## Residual Risks

The broker depends on accurate policy, tenant labels, resource ownership, and
tool metadata. It does not sandbox execution, judge whether a human approval was
wise, discover every over-privileged tool, or protect tools that bypass the
broker. Those risks need sandboxing, approval quality, static scanning, audit,
and evals.

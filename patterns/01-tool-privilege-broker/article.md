# Tool Privilege Broker

The Tool Privilege Broker is the deterministic boundary between an agent's
suggestion and real tool authority. The model can propose an action, but the
broker decides whether that exact action is allowed, denied, approval-gated,
reduced in scope, or stopped because a budget or policy boundary has been
reached.

This pattern is not a simple tool allowlist. Enterprise tool governance needs
the full action context: actor chain, user identity, agent identity, delegated
agents, tenant, resource owner, original task purpose, parameters, environment,
blast radius, rollback plan, approval state, replay state, budget, policy
version, and audit metadata.

## Why This Matters

Prompt injection containment often succeeds or fails at the tool boundary. A
poisoned document may cause the model to propose `restart_service`. The broker
must still ask:

- Is restart in scope for the original task?
- Is the user entitled to this tenant and resource?
- Is this agent allowed to use this tool?
- Is a child agent trying to exceed delegated scope?
- Is the environment production?
- Is the action reversible?
- Has a human approved this exact action?

The broker turns a model proposal into a governed decision. That decision is
outside the model and should fail closed when required policy is missing.

## Actor Chain

Every tool request should carry the actor chain:

```text
user -> parent agent -> child agent -> tool
```

The broker evaluates the whole chain. A user may have broad entitlement, while a
delegated child agent has only read-only scope. A parent agent may coordinate an
incident, while a specialist agent may only inspect logs. The tool request must
therefore identify both the human and the agent path that produced the action.

Useful fields:

- `user_id`,
- `user_roles`,
- `tenant`,
- `user_tenants`,
- `agent_id`,
- `agent_version`,
- `parent_agent`,
- `delegated_by`,
- `run_id` and `parent_run_id`.

## User Identity

User identity controls business entitlement. The broker should check the user,
roles, groups, tenant membership, and any incident or ticket scope. A valid tool
name is not enough. A support engineer may read logs for tenant A but not tenant
B. A privacy admin may export customer data for an approved privacy request but
not for an incident diagnosis.

User identity should be resolved before the model sees tools. The model should
not decide what the user's role is.

## Agent Identity

Agent identity controls runtime capability. Two agents acting for the same user
may have different privileges:

```text
incident-investigator: read logs, read metrics, list deployments
remediation-agent: restart service after approval
privacy-export-agent: export records for privacy workflows only
```

The broker should validate `agent_id`, `agent_version`, declared lifecycle
status, and tool policy. Unknown or retired agents should fail closed. Agent
identity also makes audits reconstructable after prompts or tool policies
change.

## Parent and Child Delegation

Delegation is a privilege boundary. A parent agent can delegate a task, but the
child agent receives only the delegated scope.

Example:

```text
Parent agent: incident-manager
Child agent: log-reader
Delegated scope: read logs and metrics
Attempted action: rollback_deployment
Decision: deny
```

The broker should check parent, child, delegated tools, tenant, resource, and
original task. A child agent cannot escalate by asking a parent to execute the
same unsafe action unless the parent revalidates it under policy.

## Tenant Boundary

Tenant boundaries must be enforced at the broker, not only in retrieval. A
valid tool call is unsafe when it crosses tenants.

The broker should check:

- requested tenant against user entitlement,
- tenant allowed by tool policy,
- tenant attached to resource metadata,
- tenant attached to cached tool results,
- tenant boundary for delegated agents.

If tenant labels are missing or inconsistent, the broker should deny or return
partial rather than guessing.

## Resource Ownership

Some resources have owners or domains beyond tenant. A production database, an
HR data set, and an order-processing service may all belong to the same tenant
but have different owners and approval requirements. The broker should validate
resource ownership when policy requires it.

Useful checks:

- resource exists and is registered,
- resource belongs to the requested tenant,
- resource owner allows this tool,
- resource type matches the tool category,
- requested operation is valid for that resource.

## Original Task Purpose

Purpose binding connects the tool call to the user's original business goal:

```text
Original task: Diagnose orders DLQ issue.
Allowed: read orders logs, read metrics, list recent deployments.
Not allowed: export customer records, restart payment-service, read HR data.
```

Purpose binding is how the broker contains many prompt-injection misses. If a
retrieved document says "restart production," the broker still asks whether the
action serves the original task. A valid tool can be denied because it is not
purpose-aligned.

## Parameter Validation

The broker must validate parameter names and values. Unknown parameters should
fail closed. Constrained values should be checked against policy and resource
metadata.

Example:

```text
Allowed parameter: service in [orders-api, inventory-api]
Attempted parameter: service = payment-service
Decision: deny
```

Parameter validation should include tenant, environment, resource, action type,
time window, query scope, output size, and destination. Do not allow the model to
smuggle authority through extra parameters such as `force=true`,
`include_secrets=true`, or `tenant=*`.

## Environment Policy

The same tool can have different decisions by environment:

```text
read_logs in dev: allow
read_logs in prod: allow
restart_service in dev: allow
restart_service in prod: approval_required
delete_database in prod: deny
```

Environment policy should be explicit. Missing environment rules should fail
closed. Production, regulated, shared, and customer-impacting environments
should usually require stronger checks than local or development environments.

## Blast Radius

Blast radius describes what could be affected if the action is wrong. It should
be part of the decision object and the approval request.

Consider:

- number of users or tenants affected,
- whether the action changes data or only reads it,
- whether the action touches production,
- whether dependencies can cascade,
- whether the output may contain sensitive data,
- whether the action can be retried safely.

High blast-radius actions should require approval, reduced scope, or denial.

## Rollback Requirement

Some write actions are reviewable only when rollback is defined. A restart may
be reversible. A data deletion may not be. A deployment rollback may be safe only
if the previous version and migration state are known.

For risky actions, the broker or approval gate should carry:

- rollback availability,
- rollback owner,
- expected impact,
- timeout or abort condition,
- evidence supporting the change.

If rollback information is required and missing, fail closed or escalate.

## Action Hash

An action hash binds the decision to the exact action object. It should cover:

- tool name and version,
- parameters,
- tenant,
- environment,
- resource,
- action type,
- risk level,
- blast radius,
- requester,
- agent,
- original task purpose.

The hash is used for audit, approval binding, replay prevention, and
revalidation. If any material field changes, the hash changes.

## Approval Binding

Human approval must bind to the exact action hash. Approval of one action cannot
authorize another.

Example:

```text
Approved: rollback orders-api in prod.
Attempted: rollback payment-service in prod.
Decision: deny.
```

The approval request should include enough evidence for review: action, resource,
tenant, environment, blast radius, rollback, requester, agent, policy decision,
and action hash. After approval, the broker must revalidate the action under
current policy before execution.

## Replay Prevention

Approvals should expire and should not be replayable across changed parameters,
changed resources, changed users, changed agents, or changed policies. A replay
prevention check should include:

- approval id,
- action hash,
- approver id,
- requester id,
- expiry,
- policy version,
- single-use or idempotency state.

If the user edits an action after approval, create a new action hash and require
new approval. If the original requester attempts to approve their own high-risk
action, deny or escalate according to policy.

## Budget State

Tool policy and budget policy belong in the same decision path. A tool can be
allowed by role and tenant but still blocked because the run has no tool budget
remaining.

Budget fields can include:

- remaining model calls,
- remaining tool calls,
- retry count,
- child-agent fanout,
- retrieval chunks,
- tool result bytes,
- wall-clock deadline.

When budget is exhausted, the broker should return `return_partial` rather than
allowing an unbounded loop.

## Policy Versioning

Every decision should carry policy versions. At minimum:

- tool policy version,
- retrieval policy version when source evidence is involved,
- approval policy version,
- redaction policy version,
- sandbox policy version when execution is involved.

Versioning lets evaluators and incident reviewers answer which rules were in
force when an action was allowed or denied. A trace without policy versions is
hard to reproduce.

## Fail-Closed Behavior

The broker should deny when:

- the tool is not registered,
- the tool policy is malformed,
- the environment rule is missing,
- the user role is not allowed,
- tenant entitlement is missing,
- tenant labels conflict,
- the agent is unknown or not allowed,
- the child agent exceeds delegated scope,
- parameter schema validation fails,
- purpose binding fails,
- approval is missing, expired, self-approved, or hash-mismatched,
- rollback information is required but missing,
- policy version is unavailable for a governed action.

Failing closed is what makes the broker a boundary instead of a logging layer.

## Implementation Behavior

The reference implementation evaluates a `ToolRequest` against local policy. It
does not execute the tool. It returns a `PolicyDecision` with decision, reason,
risk level, policy version, action hash, optional approver role, and audit
payload.

The broker should be called after the model proposes a tool call and before any
tool executes. If approval is required, the approval gate creates a request
bound to the action hash. When execution resumes, the broker revalidates the
same action under current policy.

## Evaluation Strategy

Tests and evals should inspect the decision trajectory:

- read-only action allowed for matching user, agent, tenant, resource, and
  purpose,
- production write requires approval,
- destructive action is denied,
- same tool is denied for an unentitled tenant,
- child agent cannot exceed delegated tools,
- parameter swapping after approval is denied,
- edited action creates a new hash,
- expired approval stops execution,
- requester cannot approve their own high-risk action,
- broker revalidates after approval,
- purpose mismatch denies an otherwise valid tool,
- budget exhaustion returns partial,
- audit includes actor chain, policy versions, action hash, approval id, and
  budget state.

An eval should fail when a final answer is safe but the trajectory attempted an
unauthorized tool call that was not contained.

## Residual Risks

The broker depends on accurate identity, policy, tenant labels, resource
metadata, and tool registration. It does not sandbox tool execution, judge the
quality of human review, discover every over-privileged tool, or protect tools
that bypass the broker. It also cannot prove that the original task was wise or
that source evidence was true.

Those residual risks need sandboxing, approval quality controls, static
scanning, redaction, audit, evals, and operational review. The broker's narrower
job is to ensure that no model proposal becomes a real action without passing
deterministic policy for the exact actor chain and action.

## References

- OWASP Top 10 for Agentic Applications (2025) — Tool Misuse and Exploitation (ASI02). https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
- ClawGuard — tool-call boundary enforcement via task-specific allowed actions. https://arxiv.org/abs/2604.11790
- Authorization Propagation in Multi-Agent AI Systems — formalizes authorization as a workflow-level property. https://arxiv.org/abs/2605.05440

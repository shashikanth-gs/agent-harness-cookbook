# HITL Approval Gate

Human-in-the-loop approval is not a blanket review step. It is a control point
for exact risky actions. A useful approval gate does not ask a human to approve
vague intent such as "fix production." It asks a human to approve a concrete
action object with parameters, resource, environment, risk, evidence, rollback
plan, expiry, and action hash.

The gate should be selective. Low-risk reads should continue. Medium or high
risk actions should pause when policy requires review. Rejected actions should
stop the graph. Edited actions should produce a new action hash and go back
through broker validation.

## Exact Action Approval

An approval request should include:

- approval request id,
- action hash,
- requested user and agent,
- parent agent when delegated,
- tool name,
- parameters,
- resource,
- environment,
- risk level,
- blast radius,
- evidence refs,
- rollback plan,
- idempotency,
- expiration,
- required approver role.

Approval is valid only for that action. Changing service, tenant, environment,
or parameters invalidates it.

## Broker Revalidation

After approval, the tool broker must evaluate the action again. Approval is not
execution permission by itself. Policy may have changed, budget may be gone, the
approval may have expired, or the action object may have changed.

## Separation of Duties

For high-risk actions, the requester should not approve their own action. The
approval gate should require an approver role that matches the risk and blast
radius.

## Evaluation Focus

Evals should inspect the trajectory:

- did the right action pause,
- did low-risk work continue,
- did the request include evidence and rollback plan,
- did rejection stop the graph,
- did replay fail when action hash changed,
- did broker revalidation happen after approval.

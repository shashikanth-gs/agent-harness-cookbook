# Pattern

The Tool Privilege Broker separates agent intent from tool authority. The agent
can propose an action. The broker decides whether that exact action is allowed,
denied, requires approval, should continue with reduced scope, or should return
partial because budget is exhausted.

Flow:

1. Agent proposes a tool action.
2. Broker computes the action hash.
3. Broker checks user role, tenant entitlement, agent identity, delegation
   scope, action type, resource, parameters, purpose, budget, and environment.
4. Broker returns `allow`, `deny`, `approval_required`,
   `allow_with_reduced_scope`, `return_partial`, or `escalate`.
5. Approval, if present, must match the exact action hash.
6. The decision is recorded for audit and evaluation.

This pattern is the deterministic boundary that makes prompt-injection
containment meaningful. Even if hostile text convinces the model to propose an
action, the broker still checks whether that action is allowed for the original
task, user, tenant, agent, resource, and environment.

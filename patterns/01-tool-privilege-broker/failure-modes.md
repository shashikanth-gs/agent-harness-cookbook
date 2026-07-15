# Failure Modes

## Tool Misuse

The agent proposes a registered tool for a task that does not justify it.
Purpose binding should deny the action.

## Privilege Escalation

A user, agent, or delegated child agent attempts a tool outside its role or
scope. Role, agent, and delegation checks should deny it.

## Tenant Leakage

A valid tool reads or writes another tenant's resource. Tenant entitlement and
resource checks should deny it.

## Approval Replay

A user approves one action but the agent later changes parameters, resource, or
environment. Action hash validation should deny the replay.

## Destructive Action

The model proposes destructive remediation. Policy should deny or require a
higher control level depending on the action class.

## Budget Exhaustion

The agent tries another tool call after the run budget is exhausted. The broker
should return partial before execution.

## Missing Policy

An unknown tool, unknown environment, or malformed policy must fail closed.

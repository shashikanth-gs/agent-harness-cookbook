# Agent Lifecycle Profile

In an enterprise environment, an agent is not just a block of code; it is an identity with a lifecycle. An agent is prototyped, tested, deployed to production, deprecated, and eventually retired. 

The Agent Lifecycle Profile pattern ensures that the harness enforces strict operational policies based on the *current lifecycle state* of the specific agent attempting to execute an action.

## Why This Matters

Imagine a developer builds a highly privileged `db-migration-agent` to assist with a one-time production database upgrade. After the upgrade, the agent is left in the repository. Six months later, a prompt injection attack tricks a routing model into delegating a task to the `db-migration-agent`. If the agent is still active and permitted to run, the attacker gains full database access.

By attaching a Lifecycle Profile to every agent, the Tool Privilege Broker and other interceptors can deny execution for agents that are marked as `deprecated` or `retired`, even if their underlying code and tool policies technically still exist in the repository.

## Core Concepts

### Lifecycle States
Agents should have explicitly defined states:
- `development`: Can only execute in dev environments or local sandboxes.
- `staging`: Can execute against staging endpoints.
- `active`: Fully approved for production.
- `deprecated`: Still runs, but triggers alerts or warnings (a sunset period).
- `retired`: Hard block. The harness will intercept and deny any attempt to invoke this agent or its tools.

### The Identity Registry
The lifecycle state cannot just be a comment in the code. It must be a verifiable attribute stored in a centralized Identity Registry (e.g., a database or a secure configuration file) that the harness queries at runtime.

### Delegation Boundaries
A parent agent in the `active` state must not be allowed to delegate to a child agent in the `development` state within a production environment. The harness must validate the lifecycle profile of the entire actor chain.
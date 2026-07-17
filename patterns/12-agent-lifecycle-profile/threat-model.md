# Threat Model

The Agent Lifecycle Profile pattern defends against the exploitation of orphaned agents, environment cross-contamination, and unauthorized capability escalation.

## Ingress Surfaces

- **Routing Models:** A primary router agent dynamically deciding which sub-agent to invoke based on user intent.
- **Direct Invocation:** An attacker interacting with a specific, deprecated agent via a forgotten API endpoint.
- **Configuration Drift:** Agent metadata files that are not synchronized with the central registry.

## Assets at Risk

- **Production Integrity:** A `development` agent accidentally deployed to a production endpoint and mutating real data.
- **Audit Trails:** Losing the ability to trace *which version* of an agent made a decision if the lifecycle and versioning data are not strictly enforced.
- **Zombie Privileges:** Deprecated agents retaining access to tools (like `delete_user`) that should have been decommissioned.

## Control Points

- **Identity Registry:** A central store that tracks the `agent_id`, `version`, and `lifecycle_state`.
- **Pre-execution Interceptor:** A harness node that checks the registry *before* the agent's graph begins executing.
- **Actor Chain Validator:** Ensures that all agents in a delegation chain (parent -> child) meet the minimum lifecycle requirements for the current environment.

## Failure Boundary

The system must fail closed. If the Identity Registry cannot be reached to verify the agent's state, or if the state is `retired`, the harness must throw an `AgentLifecycleException` and immediately block execution.

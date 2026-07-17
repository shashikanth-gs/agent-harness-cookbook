# Failure Modes

## The "Zombie Agent" Exploit
**Failure:** An agent is removed from the frontend UI and marked as "do not use" in a README, but its API endpoint and underlying LangGraph code are left running.
**Consequence:** An attacker discovers the endpoint, interacts with the zombie agent, and exploits its high privileges. Agents must be explicitly marked as `retired` in a registry that the harness enforces at runtime.

## Environment Contamination
**Failure:** An experimental agent (state: `development`) is accidentally imported and routed to by a production router agent. The harness does not check lifecycle states.
**Consequence:** The experimental agent, which may lack safety guardrails or have access to destructive tools, runs in production and causes a data breach. The harness must strictly map `development` agents to `dev` environments.

## The Version Downgrade Attack
**Failure:** An agent is upgraded to v2 to fix a critical prompt injection vulnerability. However, v1 is left active in the registry.
**Consequence:** An attacker specifies `version: v1` in their API request, bypassing the security fix. The lifecycle profile must track individual versions and forcefully retire vulnerable older versions.

## Delegation Mismatch
**Failure:** A production agent (state: `active`) delegates a task to a newly built, untested sub-agent (state: `development`).
**Consequence:** The untrusted sub-agent performs actions on behalf of the trusted parent. The harness must enforce that a child agent's lifecycle state is equal to or greater than the parent's environment requirements.

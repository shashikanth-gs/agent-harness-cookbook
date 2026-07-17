# Adoption Levels

Patterns use adoption levels so teams can choose the right amount of harnessing
for the risk of the agent. Use the same Level 0 through Level 5 scale across
the repository.

## Level 0: Unmanaged Baseline
The agent or application calls models, tools, memory, or retrieval directly.
This is useful only for prototypes and threat discovery.

## Level 1: Explicit Static Controls
The harness introduces simple allowlists, basic classification, or fixed limits.
Examples include a static tool allowlist, tenant filter, or maximum tool-call
count.

## Level 2: Validation and Structured Decisions
The harness validates schemas, parameters, sources, and data labels before
passing work to the model or tool layer.

## Level 3: Policy-Driven Behavior
Decisions include identity, tenant, purpose, environment, resource, and risk.
At this level, the harness starts to enforce enterprise policy rather than only
local checks.

## Level 4: Audit, Approval, and Evaluation Integration
High-risk actions require approval, decisions are recorded in structured audit
events, and trajectory checks can inspect what happened during a run.

## Level 5: Mature Operational Controls
The harness combines policy, approval, audit, evals, anomaly detection, CI/CD
gates, lifecycle review, and operational monitoring.

## Beyond the Harness

Even at Level 5 maturity, the harness is one layer in the enterprise stack.
Production deployments require additional infrastructure: API gateways, identity
federation, secret management, network security, and compliance integration. See
[What This Cookbook Does Not Cover](what-this-cookbook-does-not-cover.md) for what
sits beyond the harness at every adoption level.

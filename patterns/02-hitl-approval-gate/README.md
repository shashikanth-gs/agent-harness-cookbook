# Human-in-the-Loop Approval Gate

Risky actions should pause for a human approve, edit, or reject decision. This
pattern demonstrates risk-based approval, not blanket approval for everything.

## Scope

This pattern is one of 12 starting harness-layer controls in the
[Agent Harness Cookbook](../../README.md). These patterns are a necessary but
not sufficient set — a production deployment also requires API gateways,
identity federation, secret management, network security, and compliance
integration. See
[What This Cookbook Does Not Cover](../../docs/what-this-cookbook-does-not-cover.md)
for the broader enterprise stack and
[Use-Case Scenarios](../../docs/use-case-scenarios.md) for how this pattern
applies across healthcare, finance, legal, customer service, and DevOps.

See also [Identity and Principal Propagation](../../docs/identity-and-principal-propagation.md)
for how user identity flows end-to-end through the agent system.

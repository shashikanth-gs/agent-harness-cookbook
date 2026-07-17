# Redaction Boundary

Sensitive data should be masked before and after model, tool, audit, and
side-band boundaries. This example uses simple regex redaction for educational
purposes.

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

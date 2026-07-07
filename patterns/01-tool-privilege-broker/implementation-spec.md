# Implementation Spec

Implement a deterministic broker that accepts a proposed tool request and policy
document. The broker must not execute the tool. It returns a decision object
with `decision`, `reason`, and `risk_level`.

Required checks:

- tool is registered,
- user role is allowed,
- every parameter is permitted,
- constrained parameter values match policy,
- target environment has an explicit decision.

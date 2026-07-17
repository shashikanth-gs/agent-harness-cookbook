# Contributing

This project is a cookbook, not a framework. Contributions should keep examples
small, local-first, deterministic, and adaptable to different agent runtimes.

Good contributions usually include:

- a short pattern explanation,
- a runnable reference example,
- tests that demonstrate expected harness behavior,
- adoption levels from basic to advanced,
- clear notes about what the example does not solve.

Avoid adding mandatory cloud services, real enterprise system names, real
secrets, or provider-specific assumptions unless they are clearly optional.

## Scope and Cross-References

When adding or modifying patterns, keep the scope framing consistent:

- Each pattern should include a `what-this-does-not-solve.md` file.
- Reference [What This Cookbook Does Not Cover](docs/what-this-cookbook-does-not-cover.md)
  for enterprise concerns beyond the harness.
- Reference [Use-Case Scenarios](docs/use-case-scenarios.md) if the pattern
  applies differently across domains.
- Reference [Identity and Principal Propagation](docs/identity-and-principal-propagation.md)
  for patterns that involve identity, role, or tenant checks.

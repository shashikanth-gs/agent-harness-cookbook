# Threat Model

The broker protects the tool-call boundary. Threats occur when an agent proposes
an action that exceeds the user's authority, tenant, purpose, budget, or
delegated scope.

## Ingress Surfaces

- model tool proposals,
- injected instructions from user or retrieved content,
- tool-result injection,
- agent-to-agent messages,
- approval resume events,
- stale or missing policy,
- budget state,
- tenant and identity context.

## Assets at Risk

- production services,
- tenant data,
- customer records,
- credentials reachable through tools,
- approval integrity,
- auditability,
- downstream systems with side effects.

## Control Points

- tool privilege broker,
- parameter schema validation,
- purpose binding,
- tenant entitlement check,
- delegation policy,
- approval gate,
- budget guard,
- audit sink.

## Failure Boundary

The broker must fail closed when required policy is missing, tool registration is
unknown, tenant entitlement is absent, approval hashes do not match, or the
action does not match the original task.

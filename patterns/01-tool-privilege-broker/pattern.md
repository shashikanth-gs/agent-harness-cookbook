# Pattern

Flow:

1. Agent proposes a tool call.
2. Broker receives agent identity, user identity, roles, tool name, parameters,
   and environment.
3. Broker validates the request against policy.
4. Broker returns `allow`, `approval_required`, or `deny`.
5. Decision is recorded for audit and evaluation.

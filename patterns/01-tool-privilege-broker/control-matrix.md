# Control Matrix

| Threat | Primary Control | Supporting Controls | Expected Evidence |
| --- | --- | --- | --- |
| Tool misuse | purpose binding | parameter validation, audit | purpose denial reason |
| Privilege escalation | role and agent checks | delegation policy | `tool.denied` |
| Tenant leakage | tenant entitlement | resource labels, audit | tenant denial |
| Approval replay | action hash | approval expiry, broker recheck | hash mismatch |
| Destructive action | action type policy | approval gate, sandbox | destructive denial |
| Budget exhaustion | budget guard | partial result handling | `outcome.partial` |
| Missing policy | fail closed | CI policy tests | invalid policy denial |

## Evaluation Checks

- allowed read-only calls stay allowed,
- production writes require approval,
- destructive actions are denied,
- tenant mismatch fails,
- child agents cannot use parent-only tools,
- approval hash mismatch fails,
- purpose mismatch fails,
- budget exhaustion returns partial.

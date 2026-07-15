# Eval Cases

- Dev read-only log retrieval is allowed for the right user, tenant, agent, and
  purpose.
- Production write action returns `approval_required` with action hash and
  approver role.
- Production destructive action returns `deny`.
- Same tool is allowed for entitled tenant and denied for unentitled tenant.
- Child agent cannot call a parent-only remediation tool.
- Approved action replay with changed parameters is rejected.
- Exact approved action is allowed only after broker revalidation.
- Valid tool with unrelated purpose is denied.
- Tool request with exhausted budget returns partial before execution.
- Unknown tool, missing environment decision, or invalid policy fails closed.

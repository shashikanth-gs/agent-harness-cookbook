# Eval Cases

- Low-risk read proceeds without approval.
- Medium-risk write creates an approval request.
- Human approval resumes only the exact action hash.
- Edited action receives a new hash and returns to validation.
- Human rejection stops the risky graph branch.
- Expired approval is denied.
- Requester cannot approve own high-risk action.
- High-risk action escalates to required approver role.
- Approval request contains evidence refs, rollback plan, idempotency, blast
  radius, and expiration.
- Broker revalidates the action after approval.

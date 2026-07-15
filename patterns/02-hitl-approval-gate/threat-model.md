# Threat Model

The approval gate protects risky actions from proceeding without accountable
review. The threat is vague, stale, replayed, self-approved, or context-free
approval.

## Ingress Surfaces

- broker decision requiring approval,
- approval request creation,
- approval edit,
- approval resume,
- delayed execution,
- delegated-agent action,
- human reviewer decision.

## Assets at Risk

- production systems,
- approval integrity,
- reviewer accountability,
- audit trace,
- rollback path,
- separation of duties.

## Control Points

- approval gate,
- action hash,
- expiration check,
- approver role check,
- broker revalidation,
- audit sink.

## Containment Goal

Approval should authorize exactly one reviewed action and nothing else.

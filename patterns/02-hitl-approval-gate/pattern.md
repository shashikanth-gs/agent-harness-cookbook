# Pattern

HITL Approval Gate pauses an agent graph for exact risky actions, not broad
intent.

Flow:

1. Broker or risk classifier returns a decision.
2. Low-risk actions continue and record `approval.skipped`.
3. Risky actions create an approval request with action hash, evidence,
   rollback plan, blast radius, idempotency, expiry, and required approver role.
4. Human approves, edits, rejects, or escalates.
5. Edited actions receive a new action hash.
6. Approved actions are revalidated by the tool broker.
7. Rejected or expired actions stop the risky branch.

This pattern is intentionally selective. It preserves useful automation while
spending human judgment on irreversible, high-impact, or policy-sensitive
actions.

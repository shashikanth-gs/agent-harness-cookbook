# Failure Modes

## Vague Approval

The reviewer approves an intention rather than an exact action object.

## Approval Replay

An approval for one action is reused with changed parameters or resource.

## Expired Approval

An old approval is used after context, risk, or policy may have changed.

## Self-Approval

The requester approves their own high-risk action.

## Missing Evidence

The approval request omits evidence, rollback plan, idempotency, or blast
radius, so review is not meaningful.

## No Broker Revalidation

The action executes after approval without checking current policy and action
hash.

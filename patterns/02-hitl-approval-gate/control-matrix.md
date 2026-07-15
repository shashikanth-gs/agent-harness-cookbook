# Control Matrix

| Threat | Primary Control | Supporting Controls | Expected Evidence |
| --- | --- | --- | --- |
| Vague approval | action object schema | evidence refs, rollback plan | approval request payload |
| Approval replay | action hash | broker revalidation | hash mismatch |
| Expired approval | expiry check | audit sink | `approval.expired` |
| Self-approval | approver policy | identity provider | invalid actor |
| Missing evidence | approval schema | trace links | schema failure |
| Policy drift | broker recheck | policy version | revalidation event |

## Evaluation Checks

- low-risk actions do not pause,
- risky actions create complete approval requests,
- rejection stops the graph,
- edit creates a new action,
- expired or replayed approval is denied,
- broker revalidates after approval.

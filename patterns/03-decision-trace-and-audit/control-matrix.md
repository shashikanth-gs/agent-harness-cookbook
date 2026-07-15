# Control Matrix

| Threat | Primary Control | Supporting Controls | Expected Evidence |
| --- | --- | --- | --- |
| Missing event | trace schema | eval sink | missing-event finding |
| Wrong event class | decision vs observation taxonomy | review tooling | event classification |
| Sensitive audit payload | redaction boundary | audit schema | redaction summary |
| Approval ambiguity | approval event schema | action hash | approval request id |
| Cross-agent opacity | correlation ids | parent run id | handoff events |
| Budget opacity | budget events | partial outcome | `budget.exhausted` |
| Unsafe intermediate action | trajectory eval | tool broker events | denied proposal |

## Evaluation Checks

- trace has ordered events,
- denied actions include reason and policy version,
- approval events include action hash and actor,
- redaction happens before audit storage,
- handoffs include parent and child ids,
- final status explains partial or failed runs.

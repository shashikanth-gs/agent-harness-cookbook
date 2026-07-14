# Risk-Adaptive Adoption Levels

The purpose of the harness is not to block every action. It is to choose control
depth based on risk.

## Standard Levels

Use this scale across patterns:

- Level 0: direct capability, no harness boundary,
- Level 1: static allowlist or basic classification,
- Level 2: schema validation and source labels,
- Level 3: policy-based decisions by identity, purpose, environment, and risk,
- Level 4: policy plus approval and audit,
- Level 5: policy plus approval, audit, evals, anomaly detection, and CI gates.

## Choosing a Level

Higher levels are appropriate when:

- tools can change state,
- production resources are involved,
- data is sensitive,
- tenants share infrastructure,
- memory persists,
- agents delegate to other agents,
- actions are hard to reverse,
- auditability is required.

Lower levels may be acceptable for:

- read-only local demos,
- public documentation search,
- throwaway experiments,
- non-sensitive summarization,
- deterministic offline workflows.

## Pattern Example

Tool Privilege Broker:

- Level 0: direct tool call,
- Level 1: tool allowlist,
- Level 2: allowlist plus schema validation,
- Level 3: policy-based decision,
- Level 4: policy plus approval plus audit,
- Level 5: policy plus approval, audit, evals, and anomaly detection.

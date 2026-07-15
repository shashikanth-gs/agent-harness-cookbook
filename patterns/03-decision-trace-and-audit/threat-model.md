# Threat Model

Audit risk appears when important trajectory events are missing, misclassified,
or stored with sensitive payloads. A final answer can be safe while the run
violated policy mid-trajectory.

## Ingress Surfaces

- user request,
- retrieved source metadata,
- tool proposals,
- policy decisions,
- approval requests and resolutions,
- agent handoffs,
- redaction events,
- budget events,
- final output.

## Assets at Risk

- forensic reconstruction,
- policy accountability,
- approval accountability,
- sensitive data in audit,
- evaluation reliability,
- incident review.

## Control Points

- decision trace,
- audit sink,
- redaction boundary,
- schema validation,
- eval sink.

## Containment Goal

The trace should make unsafe proposals, denied actions, approval decisions,
redaction, and partial failures visible without storing private reasoning or raw
secrets.

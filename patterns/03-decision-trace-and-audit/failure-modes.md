# Failure Modes

## Missing Event

A tool call, denial, approval, redaction, or handoff is not recorded, making the
run impossible to reconstruct.

## Wrong Event Class

A model suggestion is recorded as a policy decision, or a tool observation is
treated as authority.

## Sensitive Audit Payload

Audit stores raw emails, tokens, credentials, or customer data.

## No Correlation

Parent and child agent runs lack shared ids, so cross-agent propagation is
invisible.

## Approval Ambiguity

Trace records that approval happened but not the action hash, actor, expiry, or
broker revalidation.

## Outcome-Only Evaluation

Eval checks final answer only and misses unsafe intermediate access or actions.

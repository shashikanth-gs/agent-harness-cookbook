# Implementation Spec

Create an approval request only when the broker or risk classifier returns
`approval_required`. The request must include action, redacted parameters, risk,
reason, and a stable request id. A resumed flow must use the approved or edited
parameters, or stop on rejection.

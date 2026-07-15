# Pattern

Decision Trace and Audit records the observable trajectory of an agent run so
debugging, evaluation, governance, and incident review can reconstruct what
happened.

Flow:

1. Start a trace for the user request.
2. Record input and source classifications.
3. Record selected agent, model, prompt, and policy versions.
4. Record retrieved sources and chunk hashes.
5. Record tool proposals, action hashes, and broker decisions.
6. Record approval requests, actors, and resolutions.
7. Record redaction, budget, and validation events.
8. Record final status and failure reason.

The trace records observable evidence, not private chain-of-thought. It must
distinguish model suggestions, policy decisions, human approvals, tool
observations, and system validations.

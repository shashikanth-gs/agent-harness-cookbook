# What the Redaction Boundary Does Not Solve

The redaction boundary prevents sensitive data (PII, secrets, credentials) from
crossing model and tool boundaries using pattern-based detection and reversible
tokenization. It does not solve the following.

## Not Solved

- **All PII forms.** Regex-based detection catches structured patterns (emails,
  credit card numbers, API keys, bearer tokens). It does not reliably detect
  unstructured PII: names in free text, addresses without standard formats,
  medical conditions, or biometric data references.

- **Semantic sensitivity.** The boundary operates on patterns, not meaning. It
  cannot determine that "the CEO's salary is $2M" is sensitive while "the
  server's memory is 2GB" is not. Context-aware data classification requires
  external DLP systems.

- **Data already in model weights.** Redaction prevents sensitive data from
  entering the current context. It cannot remove information the model learned
  during training. Model memorization is a separate concern.

- **Side-channel leakage.** Redacted data may still be inferrable from
  surrounding context. If the redaction replaces an email but leaves "sent to
  the VP of Engineering at Acme Corp," the identity is still recoverable.

- **Cross-boundary data flow control.** The boundary redacts data at model and
  tool interfaces. It does not control where data flows after leaving the
  harness — audit log storage, downstream APIs, cached responses, or analytics
  pipelines may retain sensitive data.

- **Compliance-grade data handling.** Redaction is one control. HIPAA, PCI-DSS,
  and GDPR require additional controls: data encryption at rest, access logging,
  retention policies, right-to-deletion, and data processing agreements.

- **Reversible tokenization key management.** The current implementation uses
  in-memory token maps. Production use requires secure key management for
  de-tokenization, access controls on who can reverse redactions, and audit
  trails for de-tokenization events.

## Residual Risk

Residual risk remains when sensitive data appears in formats the patterns do not
match, when surrounding context makes redacted values inferrable, or when
redacted data is reconstructable from multiple partial observations across
sessions.

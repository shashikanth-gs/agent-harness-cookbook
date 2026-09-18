# Reference Architecture

This reference architecture keeps the repo local-first while showing enterprise
harness controls. The harness is one layer in a broader enterprise stack — see
[What This Cookbook Does Not Cover](what-this-cookbook-does-not-cover.md) for the
full picture.

## End-to-End Flow

```text
User
  -> API Gateway (auth, rate limiting, WAF)         [not covered by harness]
  -> Identity Layer (OAuth/OIDC, JWT validation)     [not covered by harness]
  -> Agent Service
       -> input classifier                           [harness]
       -> task intent extractor                      [harness]
       -> source trust classifier                    [harness]
       -> retrieval guard                            [harness]
       -> context builder                            [harness]
       -> model/agent loop
       -> tool privilege broker                      [harness]
       -> approval gate when required                [harness]
       -> sandbox or tool runtime                    [harness]
       -> redaction boundary                         [harness]
       -> audit sink                                 [harness]
       -> eval sink                                  [harness]
  -> Tool Execution
       -> credential injection (Vault/KMS)           [not covered by harness]
       -> identity propagation (on-behalf-of)        [not covered by harness]
       -> backend API with user-level authz          [not covered by harness]
  -> Observability
       -> SIEM, OpenTelemetry, dashboards            [not covered by harness]
```

The `[harness]` controls are what this cookbook implements. The
`[not covered by harness]` layers are required for production but are
infrastructure concerns outside the harness boundary. See
[Identity and Principal Propagation](identity-and-principal-propagation.md) for
the identity flow in detail.

## Local-First Components

The cookbook implements the harness layer using:

- mock tools,
- local JSON fixtures,
- local policies,
- local traces,
- local eval runner,
- safe simulated execution.

Does not require:

- real Splunk,
- real Prometheus,
- real Azure,
- real OpenAI key,
- real database,
- Kubernetes,
- cloud account.

## Production Infrastructure (Beyond the Harness)

A production deployment requires infrastructure that the harness depends on but
does not implement. These are not optional add-ons — they are required layers.

### Identity and Access

- OAuth 2.0 / OIDC identity provider integration,
- JWT validation and token lifecycle,
- managed identities or service accounts per agent,
- scoped credentials with short TTLs via Vault or cloud KMS,
- on-behalf-of token exchange for tool calls (RFC 8693).

See recent work on OIDC-A (agentic identity extensions) and the Agent Identity
Protocol for emerging standards in this space.

### Network and Edge

- API gateway with rate limiting, WAF, and DDoS protection,
- private endpoints for cloud services,
- service mesh with mTLS between agent and backend services,
- network policies restricting tool-to-backend communication,
- egress filtering to prevent data exfiltration.

### Observability and Operations

- OpenTelemetry export for harness traces and metrics,
- SIEM integration (Splunk, Sentinel, Chronicle) for security events,
- alerting on harness control failures,
- kill switches to disable agents or tools in emergencies,
- dashboards for agent operational health.

### Compliance and Retention

- WORM retention for audit logs,
- SOC 2, HIPAA, PCI-DSS evidence collection,
- EU AI Act compliance documentation,
- data residency controls.

### Deployment

- container orchestration with resource limits,
- blue-green or canary deployments for agent updates,
- rollback procedures for agent-initiated changes.

## Boundary Principle

The cookbook keeps the harness boundary clear regardless of what backs each
layer. The same `ToolPrivilegeBroker` works whether credentials come from
environment variables (local dev) or HashiCorp Vault (production). The same
`AuditSink` interface works whether events go to an in-memory list (local) or
Splunk (production).

This separation is deliberate. Teams should be able to adopt harness patterns
without committing to specific infrastructure choices.

# What This Cookbook Does Not Cover

This cookbook covers the harness layer: the set of controls around an agent that
make its capabilities explicit, bounded, observable, governable, testable, and
auditable. These 12 patterns are a necessary but not sufficient starting set for
production agent deployment.

A production enterprise agent system requires many additional layers beyond the
harness. This document lists the most important ones.

## API Gateway and Edge Security

The harness assumes requests arrive from a trusted entry point. In production,
an API gateway must sit in front of the agent service to handle:

- rate limiting and throttling per client,
- WAF rules and DDoS protection,
- TLS termination,
- request validation and size limits,
- API versioning and routing.

The gateway is where the agent system first meets untrusted traffic. Without it,
the harness receives requests with no upstream protection.

## Identity, Authentication, and Federation

The harness checks user identity, role, and tenant in tool authorization
decisions (see the `ToolRequest` fields in Pattern 01). But it does not handle
how identity is established or verified.

Production systems need:

- OAuth 2.0 / OIDC integration for user authentication,
- SAML federation for enterprise SSO,
- API key or service account authentication for machine callers,
- JWT validation and token lifecycle management,
- session management and token refresh.

See [Identity and Principal Propagation](identity-and-principal-propagation.md)
for how identity flows through the agent system end-to-end.

## Principal and Role Propagation

The harness evaluates whether a user with a given role may call a tool in a given
context. But the harness does not address how the user's identity and roles
propagate from the authentication layer through the agent to backend systems.

Production systems need:

- on-behalf-of token exchange when tools call downstream APIs,
- scoped credential issuance per tool call,
- delegation chain tracking across multi-agent handoffs,
- role mapping between the agent's role model and backend authorization systems.

Recent research formalizes this as "authorization propagation" — maintaining
authorization invariants as non-human principals retrieve data, delegate tasks,
and synthesize results across changing boundaries (see
[Source Landscape](source-landscape.md) for references).

## Secret Management

The harness redacts sensitive data in model context and audit logs (Pattern 05).
But it does not manage the credentials that tools use to access backend systems.

Production systems need:

- a secrets vault (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault,
  GCP Secret Manager) for tool credentials,
- dynamic credential generation with short TTLs,
- credential rotation without agent downtime,
- no secrets in prompts, environment variables, or configuration files.

## Network Security and Segmentation

The harness's sandbox boundary (Pattern 09) isolates code execution. But it does
not address network-level isolation between the agent and backend systems.

Production systems need:

- service mesh (Istio, Linkerd) with mTLS between agent and backend services,
- network policies restricting which tools can reach which backends,
- private endpoints for cloud services,
- egress filtering to prevent data exfiltration via tool calls,
- DNS-level controls for agent-generated requests.

## Data Residency and Sovereignty

The harness's memory isolation (Pattern 08) scopes data to tenants. But it does
not enforce where data is physically stored or processed.

Production systems need:

- data residency controls ensuring data stays in the required jurisdiction,
- model deployment in compliant regions,
- cross-border transfer controls for multi-region deployments,
- data classification and handling policies enforced at the storage layer.

## Compliance Framework Integration

The harness produces audit trails (Pattern 03) and evaluation results
(Patterns 10 and 11). But it does not map these to specific compliance
requirements.

Production systems need:

- SOC 2 Type II evidence collection from harness audit events,
- HIPAA safeguards for healthcare agent deployments,
- PCI-DSS controls for agents handling payment data,
- EU AI Act compliance documentation for high-risk classifications,
- evidence retention policies aligned with regulatory requirements.

## Observability Infrastructure

The harness writes traces and audit events to local stores. Production systems
need:

- OpenTelemetry export for traces and metrics,
- SIEM integration (Splunk, Sentinel, Chronicle) for security events,
- log aggregation with structured agent event schemas,
- alerting on harness control failures (broker denials, approval timeouts,
  budget exhaustion),
- dashboards for agent operational health.

## Incident Response

The harness detects and records unsafe behavior. But it does not define how the
organization responds to agent-caused incidents.

Production systems need:

- incident response runbooks specific to agent failure modes,
- kill switches to disable agents or specific tools in emergencies,
- rollback procedures for agent-initiated changes,
- post-incident review processes that use harness audit trails,
- escalation paths from automated detection to human responders.

## Model Supply Chain Security

The harness evaluates agent behavior at runtime. But it does not address the
integrity of the models or tools the agent depends on.

Production systems need:

- model provenance verification (weights integrity, training data lineage),
- tool and MCP server supply chain validation,
- dependency scanning for agent code and tool implementations,
- version pinning and change management for model updates.

## Deployment and Infrastructure

The harness is designed to be local-first and infrastructure-agnostic. Production
deployment adds:

- container orchestration (Kubernetes) with resource limits,
- auto-scaling based on agent workload,
- blue-green or canary deployments for agent updates,
- health checks and readiness probes,
- backup and disaster recovery for agent state.

---

## How to Use This Document

This list is not exhaustive. The right set of additional controls depends on:

- the agent's autonomy level and risk profile,
- the sensitivity of data the agent accesses,
- the blast radius of tools the agent can call,
- the regulatory environment the organization operates in,
- the maturity of the organization's existing security infrastructure.

Start with the harness patterns in this cookbook to get the agent-layer controls
right. Then layer on the infrastructure, identity, compliance, and operational
controls listed here. See [Adoption Levels](06-adoption-levels.md) for a
maturity model that helps sequence these investments.

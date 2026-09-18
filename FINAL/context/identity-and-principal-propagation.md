# Identity and Principal Propagation

The harness patterns in this cookbook check identity, role, tenant, and
environment at tool authorization time. But they assume that identity is already
available and verified when the harness evaluates a request.

This document describes how identity enters the agent system, how it binds to
harness decisions, and how it should propagate through tool calls to backend
systems. The harness alone cannot solve this — it depends on deployment
infrastructure.

## The Problem

When a user asks an agent to act on their behalf, every action the agent takes
should carry the user's identity and authorization scope. If the agent calls a
backend API using its own service credentials, backend systems cannot distinguish
between actions taken for different users or enforce user-level access controls.

This is not a theoretical concern. In multi-tenant agent deployments, a failure
to propagate user identity through tool calls can allow one tenant's agent
session to access another tenant's data in backend systems.

## End-to-End Identity Flow

```text
User
  -> API Gateway (authenticates user, validates JWT/OAuth token)
  -> Agent Service (receives verified identity claims)
  -> Harness Context (binds identity to ToolRequest fields)
  -> Tool Privilege Broker (evaluates policy against identity)
  -> Tool Execution (propagates user identity to backend API)
  -> Backend System (enforces user-level authorization)
  -> Audit Trail (records who requested what, through which agent)
```

## Stage 1: Identity Enters the System

The API gateway or authentication layer verifies the user's identity before the
request reaches the agent. Common patterns:

- **OAuth 2.0 / OIDC**: The user authenticates with an identity provider. The
  gateway validates the access token or ID token and extracts claims (user ID,
  roles, tenant, scopes).
- **SAML**: Enterprise SSO provides assertions about the user's identity and
  group memberships.
- **API Keys**: Machine-to-machine callers authenticate with scoped API keys
  that carry client identity and permissions.

The harness does not perform authentication. It receives verified identity claims
from the upstream layer.

## Stage 2: Identity Binds to Harness Context

The harness binds verified identity claims to the fields that drive policy
decisions. In this cookbook, these fields appear in `ToolRequest`:

- `user_id`: the authenticated user's identifier,
- `user_role`: the user's role or roles in the system,
- `tenant_id`: the tenant or organization the user belongs to,
- `session_id`: the current agent session,
- `agent_id`: the agent acting on behalf of the user,
- `delegation_chain`: if another agent delegated the task.

These fields must be populated from verified claims, not from user input or
model output. If the model can set its own `user_role`, the tool privilege
broker's role checks are meaningless.

## Stage 3: Tool Calls Propagate Identity

When a tool calls a backend API, it should propagate the user's identity so the
backend can enforce its own access controls. Common patterns:

### On-Behalf-Of Token Exchange

The agent exchanges its own credentials plus the user's identity for a
scoped token that represents "agent acting on behalf of user." OAuth 2.0 Token
Exchange (RFC 8693) supports this flow.

```text
Agent Service
  -> Token Exchange Endpoint
     (agent credential + user token -> delegated token)
  -> Backend API
     (receives delegated token, enforces user-level authz)
```

### Scoped Credential Issuance

For each tool call, the harness requests a short-lived credential scoped to:
- the specific user,
- the specific operation,
- the specific resource,
- a short TTL (minutes, not hours).

This limits blast radius if a credential is leaked or misused.

### Header Propagation

In simpler deployments, the user's identity can be propagated via HTTP headers
(e.g., `X-User-Id`, `X-Tenant-Id`) over mTLS connections where the transport
layer ensures the headers are trustworthy.

## Stage 4: Backend Authorization

Backend systems should enforce their own access controls using the propagated
identity. The harness's tool privilege broker is a first line of defense, but
backend authorization is the definitive control.

Example: the harness may allow a user with role `ops-engineer` to call
`read_logs`. But the logging backend should still verify that this specific user
has access to logs for this specific service in this specific environment.

## Stage 5: Audit Trail Accountability

The harness audit trail (Pattern 03) should record the full identity chain for
every action:

- who initiated the request (user),
- which agent acted (agent ID and version),
- which delegation chain was involved (if multi-agent),
- which credentials were used for the tool call,
- which backend authorization decision was made.

This enables post-incident review to trace any action back to its human
initiator.

## Multi-Agent Delegation

When agents delegate tasks to other agents, the identity chain must be
preserved. Each delegation hop should:

- carry the original user's identity,
- narrow the authorization scope (never widen),
- record the delegation in the audit trail,
- validate that the delegating agent has authority to delegate.

Recent research formalizes this as "authorization propagation" with three
sub-problems: transitive delegation, aggregation inference, and temporal
validity. See the [Source Landscape](source-landscape.md) for references to
OIDC-A, AIP, and related work.

## What the Harness Provides

The harness provides the policy evaluation layer:

- `ToolRequest` carries identity fields for every tool call,
- `ToolPrivilegeBroker` evaluates policy against those fields,
- `ApprovalGate` binds human approval to specific actions,
- `AuditSink` records the identity chain for every decision.

## What the Harness Does Not Provide

The harness does not provide:

- authentication (verifying who the user is),
- token management (issuing, refreshing, revoking tokens),
- credential vaulting (storing and rotating tool credentials),
- network transport security (mTLS, private endpoints),
- backend authorization enforcement.

These are deployment infrastructure concerns. The harness depends on them but
cannot replace them. See
[What This Cookbook Does Not Cover](what-this-cookbook-does-not-cover.md) for the
full list of infrastructure concerns beyond the harness.

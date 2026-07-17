# What the Agent Lifecycle Profile Does Not Solve

The agent lifecycle profile binds runtime behavior to agent identity and
lifecycle state. It ensures deprecated agents are rejected in production, agent
manifests are signed, and lifecycle transitions are validated. It does not solve
the following.

## Not Solved

- **Agent discovery and registry.** The lifecycle profile validates an agent's
  identity and state. It does not provide a registry for discovering available
  agents, their capabilities, or their current status. Agent catalogs and
  service discovery are infrastructure concerns.

- **Version compatibility.** The profile tracks agent version and lifecycle
  state. It does not determine whether a new agent version is compatible with
  existing tools, policies, data formats, or other agents. Compatibility
  testing requires CI/CD evaluation gates (Pattern 11) and integration testing.

- **Graceful deprecation.** The profile rejects deprecated agents. It does not
  migrate in-flight sessions from a deprecated version to a replacement, drain
  active connections, or notify users that their agent is being retired.
  Graceful deprecation requires orchestration infrastructure.

- **Agent capability evolution.** When an agent's capabilities change (new
  tools added, existing tools removed), the lifecycle profile does not
  automatically update the associated policies, tool manifests, or evaluation
  suites. Policy and eval maintenance is a manual or CI-driven process.

- **Multi-agent fleet management.** The profile operates on individual agents.
  It does not provide fleet-level views: how many agents are active across the
  organization, which versions are deployed where, or which agents should be
  retired. Fleet management requires an operational dashboard.

- **Cryptographic key management.** The profile uses manifest signing to detect
  tampering. Production deployment requires proper key management: HSM-backed
  signing keys, key rotation, certificate chains, and revocation lists. The
  cookbook uses simplified HMAC-style signing for illustration.

- **Organizational governance.** The profile enforces technical lifecycle rules.
  It does not implement organizational processes: who approves agent creation,
  who reviews agent capabilities, who decides when an agent should be
  deprecated, or how agent ownership transfers. These are governance processes
  that use the profile as input.

## Residual Risk

Residual risk remains when manifest signing uses weak key management, when
lifecycle state transitions are not audited, or when deprecated agents remain
accessible through alternative paths (direct API access, cached endpoints,
stale deployments).

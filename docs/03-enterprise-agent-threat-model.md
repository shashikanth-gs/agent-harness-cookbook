# Enterprise Agent Threat Model

Enterprise agent risk is not only prompt injection. Risk appears anywhere text,
state, tools, identity, credentials, memory, or delegated authority enters the
agent loop.

This threat model is the baseline for the cookbook patterns. It is aligned with
OWASP agent security guidance, agentic application risk taxonomies, tool-call
boundary research, adversarial tool-use evaluation work, skill-file attack
research, trajectory auditing, and static agent application scanning.

## Ingress Surfaces

Unsafe input or authority confusion can enter through:

- user input,
- retrieved documents,
- Confluence pages,
- OpenAPI descriptions,
- AsyncAPI descriptions,
- emails,
- tickets,
- Slack messages,
- logs,
- metrics labels,
- tool results,
- MCP server metadata,
- MCP tool descriptions,
- skill files,
- `AGENTS.md`, `CLAUDE.md`, and `SKILL.md`,
- code comments,
- uploaded files,
- previous memory,
- agent-to-agent messages,
- cached context.

The harness must not treat all of these as equal. A retrieved OpenAPI document
may be useful evidence. It is not authorized to rewrite the user's task or grant
itself new tools.

## Control Points

The main control points are:

- input guard,
- source trust classifier,
- retrieval guard,
- context builder,
- instruction/data separator,
- tool broker,
- approval gate,
- memory write gate,
- output guard,
- audit sink,
- eval sink,
- budget guard,
- sandbox boundary.

Each control point should fail closed when required policy is missing.

## Failure Types

This repo should cover at least:

- direct injection,
- indirect injection,
- tool-output injection,
- MCP injection,
- skill-file injection,
- memory poisoning,
- cross-agent goal hijack,
- tool misuse,
- privilege escalation,
- cross-tenant leakage,
- stale context,
- unsafe execution,
- budget exhaustion,
- approval replay,
- audit gaps.

## Propagation Paths

Agent failures often propagate before the final answer.

Example:

```text
poisoned OpenAPI description
  -> retrieved as relevant evidence
  -> inserted into context as plain text
  -> model treats text as instruction
  -> model proposes production restart
  -> tool broker catches purpose/environment mismatch
  -> audit records contained injection path
```

The important property is containment. Detection may miss a malicious phrase.
The tool broker, approval gate, sandbox, memory write gate, and audit trace still
need to reduce real-world impact.

## Enterprise Risk Dimensions

Risk depends on:

- autonomy,
- data sensitivity,
- tool access,
- user impact,
- business criticality,
- reversibility,
- tenant boundary,
- credential scope,
- memory persistence,
- delegation depth,
- compliance requirements,
- observability.

The right control level is risk-adaptive. A read-only documentation assistant
and a remediation agent with production tools should not have the same harness.

## Required Trace Questions

For any significant run, the organization should be able to answer:

- Who asked for the action?
- Which agent and version acted?
- Which tenant and session were involved?
- Which sources entered context?
- Which sources were trusted, untrusted, stale, or unauthorized?
- Which tool calls were proposed?
- Which policy decided allow, deny, approval, or reduced scope?
- Which human approved or rejected an action?
- What was redacted?
- What budget was consumed?
- What final status was returned?
- What residual risk remains?

## Beyond the Harness

This threat model focuses on harness-layer risks. Production systems face
additional threats at the infrastructure layer — API gateway bypass, identity
federation failures, credential leakage from vaults, network segmentation
violations — that are outside the harness boundary. See
[What This Cookbook Does Not Cover](what-this-cookbook-does-not-cover.md) and
[Identity and Principal Propagation](identity-and-principal-propagation.md).

The harness patterns apply across domains. See
[Use-Case Scenarios](use-case-scenarios.md) for how risk dimensions vary between
healthcare, finance, legal, customer service, and DevOps agents.

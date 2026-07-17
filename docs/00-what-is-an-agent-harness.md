# What Is an Agent Harness?

An agent harness is the layer around an agent that makes its capabilities
explicit, bounded, observable, governable, testable, auditable, and adaptable to
the risk of the use case.

It is not the model. It is not the agent framework. It is not necessarily a
production platform. It is the set of controls and design choices that determine
what an agent can do, how risky actions are handled, what evidence is captured,
and how behavior is evaluated over time.

## The Harness Boundary

Most agent frameworks help you define prompts, tools, memory, state, handoffs,
and execution loops. A harness decides how those capabilities are controlled.

Typical harness control points include:

- input classification,
- source trust classification,
- retrieval guard,
- context builder,
- instruction/data separator,
- tool privilege broker,
- human approval gate,
- memory write gate,
- redaction boundary,
- sandbox boundary,
- budget guard,
- output validation,
- audit sink,
- eval sink.

## What the Harness Teaches

A useful harness teaches engineers to separate authority from context.

```text
Trusted policy / system instruction = authority
User instruction = task intent
Retrieved document = evidence, not authority
Tool result = observation, not authority
Memory = context, not authority unless validated
Other agent = peer/delegate, not authority unless explicitly delegated
```

The harness should not ask the model to remember this distinction and hope it
works. It should encode the distinction into deterministic policy checks,
context construction, tool-call decisions, approval flows, trace events, and
evals.

## What This Repo Is

This repo is a cookbook. It contains patterns, threat cases, reference
implementations, local fixtures, tests, docs, and prompts that teams can adapt
to their own agent runtime.

It is designed to fit alongside LangGraph, OpenAI Agents SDK, Deep Agents,
Semantic Kernel, CrewAI, AutoGen, or custom runtimes. It is not a replacement
for them.

The 12 patterns here are a starting set of harness-layer controls, not an
exhaustive list. They apply across domains — the reference demo uses a service
incident investigation scenario, but the same patterns work for healthcare
clinical decision support, financial compliance, legal contract review, customer
service, and DevOps automation. See
[Use-Case Scenarios](use-case-scenarios.md) for concrete examples.

## What This Repo Is Not

This repo is not a guarantee of agent safety. It does not claim to fully prevent
prompt injection, data leakage, unsafe tool use, or operational failure.

The goal is narrower and more useful: reduce blast radius, contain failure,
detect and record unsafe behavior, require deterministic validation for risky
actions, and leave a trace that can be evaluated.

These patterns address the harness layer. A production agent deployment also
requires API gateways, identity federation (OAuth 2.0, OIDC), user principal
propagation through tool calls to backend systems, secret management, network
security, and compliance framework integration. See
[What This Cookbook Does Not Cover](what-this-cookbook-does-not-cover.md) and
[Identity and Principal Propagation](identity-and-principal-propagation.md).

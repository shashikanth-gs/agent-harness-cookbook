# Current Agent Framework and Harness Landscape

Last source review: 2026-07-04.

This cookbook should stay framework-adaptable. The patterns are intentionally
expressed as harness concepts first, then mapped to common agent runtimes.

## Framework Signals

- OpenAI Agents SDK exposes agents, tools, handoffs, guardrails, human review,
  resumable state, and tracing. Cookbook mapping: tool brokerage, HITL, trace,
  handoffs, and eval hooks.
- LangGraph emphasizes graph state, persistence, interrupts, and resume. Cookbook
  mapping: HITL approval gates and long-running workflows should preserve state
  before pausing.
- Microsoft Agent Framework provides agents and graph-based workflows with
  checkpointing, hydration, human-in-the-loop support, and orchestration
  patterns. Cookbook mapping: deterministic workflow steps can wrap agent calls.
- Semantic Kernel remains useful as a model-agnostic SDK and agent framework.
  Cookbook mapping: keep tools, policies, and evals outside provider-specific
  code.
- AutoGen is useful historical context for multi-agent conversation patterns, but
  current Microsoft guidance points teams toward Microsoft Agent Framework for
  new production-oriented work.
- CrewAI exposes crews, flows, guardrails, memory, knowledge, and observability.
  Cookbook mapping: harness controls should work around both role-based crews
  and event-driven flows.
- Google ADK is a code-first agent framework for tools, debugging, deployment,
  and multi-agent systems. A2A is relevant for agent interoperability. Cookbook
  mapping: lifecycle profiles and cross-agent authorization matter when agents
  discover or delegate to other agents.
- MCP is an important tool/context integration standard, but authorization and
  server trust remain explicit design concerns. Cookbook mapping: MCP servers
  still need tool manifests, identity, policy, audit, and redaction.
- Deep Agents is a LangChain/LangGraph-based harness for long-running tasks with
  planning, subagents, filesystem/context management, memory, optional
  sandboxing, tracing, evaluation, and deployment. Cookbook mapping: useful as
  an optional advanced implementation target, especially for coding and research
  agents.

## Security and Governance Signals

- OWASP LLM Top 10 2025 keeps prompt injection, sensitive information
  disclosure, excessive agency, vector/embedding weaknesses, and unbounded
  consumption directly relevant to this cookbook.
- NIST AI RMF and the Generative AI Profile support risk-adaptive controls,
  lifecycle governance, measurement, monitoring, and accountability.
- OpenTelemetry GenAI semantic conventions are moving toward common vocabulary
  for model calls, tool calls, tokens, retrieval, and GenAI telemetry. Cookbook
  traces should be easy to map to those fields later.

## Design Consequences for This Repo

- Do not bind the cookbook to one agent framework.
- Keep reference implementations deterministic and local-first.
- Keep policy, audit, budget, redaction, approval, and eval controls explicit.
- Treat prompt injection as a risk to reduce, not a problem that can be fully
  solved.
- Treat vector retrieval and MCP tool discovery as integration surfaces, not
  authorization.
- Prefer pattern-local packages and tests so a coding agent can lift one pattern
  into LangGraph, OpenAI Agents SDK, Microsoft Agent Framework, Semantic Kernel,
  CrewAI, Google ADK, or a custom runtime.

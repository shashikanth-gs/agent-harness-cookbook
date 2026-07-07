# LangGraph and Deep Agents Positioning

Last source review: 2026-07-04.

This repo is not currently implemented on LangGraph or Deep Agents. The v1
working examples use deterministic Python so the harness patterns are easy to
read, test, and port to many runtimes.

## Current Source Notes

- LangGraph is well-suited for stateful workflows, persistence, checkpointing,
  interrupts, and human-in-the-loop flows.
- Deep Agents is a LangChain/LangGraph-based agent harness for long-running
  tasks with planning, subagents, virtual filesystem/context management, memory,
  optional sandboxing, tracing, evaluation, and deployment support.
- Deep Agents is useful when the example needs complex non-deterministic
  planning or multi-step autonomous work.

## Cookbook Position

- Keep core patterns framework-neutral.
- Add LangGraph reference variants where graph state, interrupts, and resume
  behavior materially improve the teaching value.
- Add Deep Agents reference variants for advanced long-running examples such as
  coding-agent or research-agent harnesses.
- Do not make Deep Agents the default dependency for every pattern because this
  cookbook is not trying to become one opinionated framework.

## Suggested Roadmap

1. Add a LangGraph variant for `02-hitl-approval-gate`.
2. Add a LangGraph variant for `03-decision-trace-and-audit`.
3. Add a Deep Agents variant under the future secure coding agent example,
   with sandboxing and approval controls.
4. Keep deterministic tests for policy, audit, redaction, and budgets even when
   an optional framework variant is added.

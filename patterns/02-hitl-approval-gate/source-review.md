# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation changes:

- LangGraph docs: interrupts, persistence, and checkpointers.
- OpenAI Agents SDK docs: guardrails, human review, results, and resumable state.
- Microsoft Agent Framework docs: workflow checkpointing, hydration, and
  human-in-the-loop support.
- CrewAI docs: guardrails and flows.
- NIST AI RMF and Generative AI Profile: risk-adaptive governance.

Design consequence: approval should be risk-based, resumable, state-preserving,
and audited. Do not make every action require approval by default.

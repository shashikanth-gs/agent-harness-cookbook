# Agent Harness Cookbook Rules

This repository (`agent-harness`) is a framework-agnostic enterprise security and governance harness for LLM Agents.

## Core Intent
1. **Framework Agnosticism**: The core logic in `packages/agent_harness_cookbook/harness/` MUST NEVER import LangChain, LangGraph, AutoGen, CrewAI, etc. It must rely solely on standard Python structures (dataclasses, lists, dicts) and `litellm` for API abstraction.
2. **The "Harness" Pattern**: This repository teaches that the agent (the brain) is separate from the harness (the body/OS). The harness surrounds the agent, intercepting tool calls, filtering RAG context, parsing trajectories, and enforcing budgets.
3. **Examples Structure**: Each pattern in `patterns/` contains an `example.py` (showing pure Python orchestration) and a `langgraph_example.py` (showing how the pure Python harness can wrap a popular framework). Do not mix them.

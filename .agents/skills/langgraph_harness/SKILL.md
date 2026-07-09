---
name: Integrate Harness with LangGraph
description: Explains how to integrate the pure Python agent harness modules with LangGraph state machines.
---

# Integrating the Agent Harness with LangGraph

When asked to integrate an enterprise pattern from `agent_harness_cookbook/harness/` into LangGraph, use the following standard architectural mappings:

1. **Gateways & Boundaries (e.g., Memory Isolation, Prompt Shield):**
   Implement these as a **pre-processing node** (or edge) *before* the main LLM reasoning node. The node should mutate the `AgentState` to enforce boundaries before the LLM sees the prompt.

2. **Tool Governance (e.g., Privilege Brokers, Sandboxes):**
   Implement these by wrapping the standard LangGraph `ToolNode` (or custom tool execution node). The harness intercepts the `tool_calls` array, evaluates them against the harness (e.g., `TaskShield.verify_tool_alignment`), and blocks/sandboxes them before they execute.

3. **Human-in-the-Loop & Budgets:**
   Map these to LangGraph **Conditional Edges** or **Interrupts**. If the harness `BudgetTracker.is_exhausted()` returns True, route the edge to `__END__` or raise a LangGraph `NodeInterrupt`.

4. **Telemetry & Evaluations:**
   Implement these as **post-processing nodes** or external listeners. For example, extract the full `AgentState["messages"]` array at `__END__`, parse it into a standard JSON trajectory, and pass it to the harness `TrajectoryScorer`.

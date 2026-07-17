# Threat Model

The Budget Tracker protects against resource exhaustion (Denial of Wallet), runaway execution loops, and backend compute overload.

## Ingress Surfaces

- **Malicious Prompts:** User inputs designed to trap the agent in an infinite loop ("Keep searching until you find X," where X does not exist).
- **Poisoned RAG Data:** Retrieved documents containing instructions that hijack the agent's goal into an expensive, never-ending task.
- **Flawed Tool Schemas:** Poorly defined tools that cause the model to repeatedly fail and retry execution indefinitely.
- **Unbounded Fan-out:** A parent agent spawning hundreds of child agents without a shared token/cost limit.

## Assets at Risk

- **LLM API Tokens (Financial Cost):** Runaway bills from providers (OpenAI, Anthropic, etc.).
- **Backend Compute:** Overloading internal databases or APIs via repeated, rapid tool calls.
- **Tenant Quotas:** One noisy tenant consuming the shared API rate limit, degrading performance for all other tenants (Noisy Neighbor).
- **System Stability:** Out-of-memory errors on the worker nodes running the agent graphs.

## Control Points

- **Token Interceptor:** Tracks exact token usage per LLM invocation.
- **Tool Weighting Engine:** Tracks the abstract cost of executing specific backend tools.
- **Graph Depth Limit:** Enforces a hard cap on the number of nodes/edges traversed in a single run.
- **Tenant Quota Registry:** Cross-checks the current run's cost against the tenant's global allowance.

## Failure Boundary

The system must fail closed. If the budget state cannot be retrieved, or if the next action would push the total cost above the limit, the action must be denied with a `BudgetExceeded` state, halting the agent immediately.

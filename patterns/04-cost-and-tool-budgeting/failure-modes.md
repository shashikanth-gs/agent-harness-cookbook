# Failure Modes

## The "One Last Thought" Bypass
**Failure:** The budget is exhausted, but the harness allows the agent one final LLM call to "summarize" the error or explain to the user why it stopped.
**Consequence:** The model uses that final call to generate a massive, unbounded output, continuing the resource exhaustion. Budget boundaries must be hard stops.

## Uncounted Tool Costs
**Failure:** The harness strictly counts LLM API tokens but fails to track the backend compute cost of the tools being executed.
**Consequence:** An attacker forces the agent to repeatedly call a highly expensive, non-cached SQL query tool. The LLM token cost remains low, but the database cluster crashes.

## Distributed Quota Lag
**Failure:** In a multi-tenant environment, tenant quotas are cached locally on worker nodes and only synchronized every 5 minutes.
**Consequence:** A malicious script spawns hundreds of concurrent agent runs. Because the quota check lags, the tenant exceeds their budget by 100x before the system enforces the limit.

## Parent-Child Budget Evasion
**Failure:** A parent agent is given a budget of 1000 tokens. It delegates a task to a child agent, but the child agent tracks its own fresh budget of 1000 tokens instead of drawing from the parent's pool.
**Consequence:** Infinite recursion and exponential budget explosion as agents infinitely spawn sub-agents. Budget state must be shared and decremented globally across the actor chain.

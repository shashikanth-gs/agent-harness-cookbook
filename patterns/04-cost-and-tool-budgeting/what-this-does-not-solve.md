# What Cost and Tool Budgeting Does Not Solve

Budget guards enforce hard caps on model calls, tool calls, tokens, retries,
execution time, and document retrieval. They prevent runaway loops and resource
exhaustion. They do not solve the following.

## Not Solved

- **Cost attribution across tenants.** The budget guard tracks consumption per
  session but does not allocate costs to billing accounts, tenants, or cost
  centers. Cost attribution requires integration with cloud billing or internal
  chargeback systems.

- **Dynamic budget adjustment.** Budgets are static policy. The guard does not
  learn from past runs to adjust limits. A task that legitimately needs more
  tokens than the cap will be denied, not negotiated.

- **Model pricing accuracy.** Token-based budgets approximate cost. Actual costs
  depend on model pricing tiers, prompt caching, batch discounts, and provider
  billing models that the guard does not track.

- **Distributed rate limiting.** The budget guard operates per-session. It does
  not coordinate across concurrent sessions, agents, or deployments. Aggregate
  rate limiting requires an external rate limiter or API gateway.

- **Business-level spending policies.** The guard enforces technical caps. It
  does not implement business rules like "this department's monthly AI spend
  must not exceed $10,000." That requires integration with financial controls.

- **Quality vs. cost tradeoffs.** The guard stops execution when budgets are
  exhausted. It does not decide whether to use a cheaper model, reduce retrieval
  depth, or simplify the task to stay within budget.

## Residual Risk

Residual risk remains when budget caps are set too high (allowing expensive
runaway before detection), too low (blocking legitimate work), or when the
budget guard is the only defense against loops (the tool privilege broker and
evaluation should independently catch purposeless repetition).

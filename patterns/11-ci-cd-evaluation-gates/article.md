# CI/CD Evaluation Gates

Evaluating an agent locally on a developer's machine is insufficient for enterprise deployments. Because LLMs are non-deterministic, and because their behavior is highly sensitive to even minor changes in the system prompt or underlying framework code, agent security must be enforced continuously.

CI/CD Evaluation Gates is the architectural pattern of integrating trajectory-based agent evaluations directly into your Continuous Integration (CI) pipeline (e.g., GitHub Actions, GitLab CI). If a Pull Request degrades the agent's security posture, the build must fail.

## Why This Matters

A developer might adjust the system prompt to make the agent "more helpful." Unknowingly, this change makes the agent too eager to please, causing it to bypass a previously enforced boundary and share sensitive internal documents when pressed by an attacker. 

If evaluations are only run manually before major releases, this regression will slip into production. By placing the evaluations in the CI pipeline, the "helpful" PR will immediately turn red, explicitly blocking the merge.

## Core Concepts

### Blocking on Regressions
The CI gate must be configured to fail the build if any of the core security evaluations fail. It is not enough to generate a report; it must actively block the merge.

### Synthetic Data Generation
Static evaluation datasets degrade over time as models learn them. CI pipelines can integrate synthetic data generators (using adversarial LLMs like 'Red Team' models) to dynamically generate novel prompt injection attacks on every PR, ensuring the agent remains robust against unknown zero-day attacks.

### Artifact Tracking (Traceability)
When an evaluation fails in CI, the raw LangGraph trace (the sequence of agent thoughts, tool calls, and intercepted decisions) must be saved as a build artifact. A developer cannot debug an agentic failure without the full trajectory of what the LLM attempted to do.

## References

- Agent Audit — static and CI scanning for agent code, credentials, and privilege paths. https://arxiv.org/abs/2603.22853
- MonitoringBench — semi-automated red-teaming for agent monitoring. https://arxiv.org/abs/2605.09684
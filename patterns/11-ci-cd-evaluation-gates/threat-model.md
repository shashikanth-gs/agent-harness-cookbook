# Threat Model

The CI/CD Evaluation Gates pattern defends against code regressions, prompt drift, and the accidental deployment of insecure agent behaviors.

## Ingress Surfaces

- **Pull Requests:** Code changes to the harness interceptors, system prompts, tool schemas, or dependency updates.
- **Model Upgrades:** Bumping the version of the underlying LLM (e.g., from `gpt-4` to `gpt-4o`) which fundamentally changes the agent's reasoning behavior.

## Assets at Risk

- **Production Security:** Deploying an agent that has silently lost its ability to resist prompt injection or enforce tool privilege boundaries.
- **Developer Velocity:** Debugging production agent failures is exponentially harder than debugging them via a CI trace artifact.

## Control Points

- **CI Pipeline Runner:** The automation engine (GitHub Actions, Jenkins) executing the evaluation suite.
- **Adversarial Fuzzer:** A tool that dynamically generates new attack prompts during the CI run to test robustness.
- **Trace Archiver:** The mechanism that stores the LangGraph state trace for failed evaluations.

## Failure Boundary

The system must fail closed. If the evaluation suite crashes, times out, or fails to connect to the mock LLM factory, the CI pipeline must return a non-zero exit code and block the deployment. Assuming "no news is good news" in an agentic CI pipeline is a critical failure.

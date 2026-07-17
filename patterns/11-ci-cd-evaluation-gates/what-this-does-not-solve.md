# What CI/CD Evaluation Gates Does Not Solve

CI/CD evaluation gates block regressions before deployment by running adversarial
evals in CI when prompts, policies, tools, or models change. They do not solve
the following.

## Not Solved

- **Post-deployment drift.** Evaluation gates validate behavior at deployment
  time. They do not detect drift after deployment — when model provider behavior
  changes, external data sources shift, or user behavior patterns evolve.
  Post-deployment monitoring requires runtime evaluation and observability.

- **Model provider changes.** When the agent uses a hosted model (via API), the
  model provider may update the model without notice. CI gates test against the
  model version available at build time. If the provider ships a new version
  between the CI run and production traffic, the gate's results may not apply.

- **Evaluation suite completeness.** The gate blocks deployment when scores drop.
  It cannot block deployment for risks the evaluation suite does not test.
  Gaps in eval coverage are invisible to the gate.

- **Flaky evaluations.** LLM-based evaluations can produce non-deterministic
  results. A gate that uses statistical significance testing (like the Welch's
  t-test in this cookbook) mitigates this, but small eval suites and high
  variance can still produce false passes or false blocks.

- **Rollback orchestration.** The gate prevents bad deployments. It does not
  orchestrate rollback if a problem is discovered after deployment. Rollback
  requires deployment infrastructure (blue-green, canary, feature flags) and
  kill switches.

- **Multi-component coordination.** The gate evaluates a single agent or prompt
  change. It does not test the interaction between multiple agents, tools, and
  services that may be deployed independently. System-level integration testing
  requires a separate stage.

- **Compliance sign-off.** The gate provides automated quality assurance.
  Regulated industries may require human sign-off, change management board
  approval, or audit documentation before deployment. The gate can inform
  these processes but does not replace them.

## Residual Risk

Residual risk remains when eval suites are too narrow, when model providers
change behavior between CI and production, or when the gate is the only
deployment control (without runtime monitoring, kill switches, and rollback
capability).

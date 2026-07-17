# What Agent Evaluations Does Not Solve

Agent evaluations test trajectories — not only final answers — for correctness,
policy compliance, injection resistance, groundedness, and safety. They do not
solve the following.

## Not Solved

- **Runtime prevention.** Evaluations detect problems after or during a run.
  They do not prevent unsafe actions in real time. Runtime prevention requires
  the tool privilege broker (Pattern 01), approval gate (Pattern 02), and
  injection defense (Pattern 06).

- **Ground truth at scale.** Trajectory evaluations compare agent behavior
  against expected outcomes. Generating and maintaining ground truth for complex
  multi-step tasks requires significant human effort. The cookbook provides
  fixture-based eval cases; production systems need ongoing eval data curation.

- **Evaluator reliability.** When an LLM judges agent trajectories (LLM-as-judge),
  the evaluator itself can be fooled, biased, or inconsistent. Evaluator
  calibration, inter-rater agreement, and adversarial evaluation of the
  evaluator are separate concerns.

- **Distribution shift.** Evaluations test known scenarios. They do not guarantee
  safety on inputs the eval suite has never seen. Adversarial eval generation
  and continuous red-teaming are needed to cover emerging attack patterns.

- **Business outcome measurement.** Trajectory evaluations check policy
  compliance and safety properties. They do not measure whether the agent
  achieved the user's business objective, improved efficiency, or delivered
  value. Business metrics require separate instrumentation.

- **Cross-agent interaction evaluation.** The current evaluation framework tests
  single-agent trajectories. Multi-agent systems introduce emergent behaviors
  (cascading failures, goal conflicts, delegation loops) that require
  system-level evaluation, not just per-agent testing.

- **Evaluation infrastructure.** The cookbook runs evals locally with pytest. Production
  evaluation requires scheduled eval runs, regression dashboards, alerting on
  score degradation, and integration with CI/CD (Pattern 11).

## Residual Risk

Residual risk remains when eval suites are too narrow (only testing known
scenarios), when evaluator models disagree with human judgment, or when
evaluation runs are too infrequent to catch regression from model updates or
prompt changes.

# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation:

- GitHub Actions docs for CI mechanics.
- Framework eval docs for current agent runtimes used by examples.
- OWASP LLM Top 10 2025 and NIST AI RMF for security and governance checks.
- OpenTelemetry GenAI semantic conventions for comparable telemetry artifacts.

Design consequence: CI should run deterministic local checks first: unit tests,
pattern tests, golden trajectory evals, injection evals, redaction checks,
policy checks, and cost regression checks.

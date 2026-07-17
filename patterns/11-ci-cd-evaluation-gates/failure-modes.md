# Failure Modes

## The Flaky Eval Bypass
**Failure:** An LLM-as-a-Judge evaluation occasionally fails due to the non-determinism of the judge model itself. Developers get frustrated by the "flaky" tests and decide to make the CI gate "non-blocking" (soft fail).
**Consequence:** Critical security regressions are ignored because the developers assume the red CI light is just "another flaky eval." Security gates must be deterministic and blocking. If a judge is flaky, it must be tuned or replaced with a deterministic trajectory assertion.

## Stale Datasets
**Failure:** The CI pipeline runs the exact same 10 prompt injection tests for two years.
**Consequence:** The agent passes the CI gate perfectly, but is immediately compromised in production by a new, widely known jailbreak technique (e.g., the "Grandma exploit"). CI eval datasets must be regularly updated or dynamically generated.

## The Production API Call
**Failure:** The evaluation suite in CI is not properly mocked and makes live API calls to the production LLM endpoint or a live database.
**Consequence:** The CI pipeline exhausts the production API rate limits, drives up billing costs, or accidentally mutates production data during a test of the `delete_user` tool. CI must use the `MOCK_LLM=true` factory and mock all external tool endpoints.

# Failure Modes

## Final-Answer Bias
**Failure:** The evaluation framework only asserts against the `messages[-1].content` string.
**Consequence:** An agent attempts an unauthorized action, fails, and recovers to say "I cannot do that." The test passes because the final answer is a refusal, completely missing that the model attempted the malicious action and only the API error prevented it. Evaluations must assert on the *trajectory*.

## Judge Model Drift
**Failure:** The LLM used as the "Judge" to evaluate the agent is updated by the provider, and suddenly becomes overly lenient, passing adversarial tests that it previously failed.
**Consequence:** A false sense of security. Judge models should ideally be pinned to specific, deterministic versions (e.g., `gpt-4-0613`) rather than rolling tags (e.g., `gpt-4`).

## Over-fitting to the Dataset
**Failure:** The evaluation dataset contains exactly 5 prompt injection attacks. The system prompt is heavily optimized to block those 5 exact attacks.
**Consequence:** The agent passes 100% of the evaluations but immediately fails in production when a user tries a novel prompt injection attack. Eval datasets must be continuously updated and ideally use dynamic fuzzing.

## Unmocked State Mutations
**Failure:** An evaluation test runs against the live production database to test if the agent will delete a user.
**Consequence:** The agent actually deletes the user because the test environment wasn't sandboxed. Evaluations must use strict mock environments, fixtures, or dry-run intercepts.

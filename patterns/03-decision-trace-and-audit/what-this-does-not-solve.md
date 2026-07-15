# What This Does Not Solve

- It does not store private chain-of-thought.
- It does not guarantee every framework integration emits all events.
- It does not replace redaction.
- It does not decide policy by itself.
- It does not prove the final answer is correct.
- It does not provide WORM retention or SIEM export by itself.

Residual risk remains when code paths bypass the trace, event schemas are too
loose, redaction misses sensitive values, or evals inspect only final answers.

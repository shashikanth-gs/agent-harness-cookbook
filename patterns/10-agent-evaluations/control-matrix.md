# Control Matrix

| Threat | Control Point | Mechanism | Failure State |
| --- | --- | --- | --- |
| Silent Security Failure | Trajectory Asserter | Asserting that the `ToolNode` or interceptor correctly logged a `SecurityException` | Test Failure (AssertionError) |
| Model Drift / Regression | Evaluation Dataset | Running known adversarial attacks against the agent on every PR | Test Failure |
| Subjective Drift | LLM-as-a-Judge | Grading output using a secondary model pinned to a specific version | Graded as 'FAIL' |
| Eval Destructive Actions | Environment Mocking | Overriding live API endpoints with local fixtures during eval execution | Host/Data Corruption (if not mocked) |

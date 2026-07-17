# Control Matrix

| Threat | Control Point | Mechanism | Failure State |
| --- | --- | --- | --- |
| Accidental Prompt Regression | CI Pipeline Runner | Blocking merge if any trajectory assertions fail | Pipeline Failed (Non-zero exit) |
| Stale Test Exploitation | Adversarial Fuzzer | Generating novel jailbreaks dynamically during CI | Pipeline Failed (AssertionError) |
| Flaky Judge Models | Deterministic Asserter | Enforcing strict assertions on the state trace (e.g., checking if `ToolPrivilegeException` exists) | Pipeline Failed |
| Unmocked CI Runs | Mock Factory | Forcing `MOCK_LLM=true` during unit test execution in the runner | NetworkError / RateLimit (if unmocked) |

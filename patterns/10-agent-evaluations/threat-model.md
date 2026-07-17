# Threat Model

The Agent Evaluations pattern defends against regressive security controls, drift in model behavior, and "silent failures" where an agent acts insecurely but returns a benign final answer.

## Ingress Surfaces

- **LLM Base Model Updates:** The provider (e.g., OpenAI) updates the model weights behind the API, causing the agent to suddenly become susceptible to an older prompt injection technique.
- **Harness Code Changes:** A developer accidentally removes or modifies a critical check in the Privilege Broker or Sandbox interceptor.
- **System Prompt Drift:** The core instructions for the agent grow over time, confusing the model and causing it to ignore security constraints.

## Assets at Risk

- **Security Posture:** The confidence that the agent cannot be hijacked or exfiltrate data.
- **Operational Reliability:** Ensuring the agent doesn't enter infinite loops or consume excessive budgets.
- **Compliance Validity:** The proof required by auditors that the system behaves as documented in the control matrix.

## Control Points

- **Evaluation Dataset:** A curated set of "golden" inputs, including known adversarial attacks (jailbreaks, prompt injections).
- **Trajectory Asserter:** A test runner that inspects the raw LangGraph state or trace log to verify interceptor behavior.
- **LLM-as-a-Judge:** A secondary model used to grade subjective outputs against a strict rubric.

## Failure Boundary

If an evaluation run fails, it indicates a regression in the security boundary. The system must fail closed during CI/CD (blocking the deployment of the new agent prompt or harness code) until the regression is addressed.

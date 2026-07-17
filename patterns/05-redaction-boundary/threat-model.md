# Threat Model

The Redaction Boundary defends against data exfiltration, compliance violations, and inadvertent leakage of sensitive state.

## Ingress Surfaces

- **Retrieval Augmented Generation (RAG):** The agent fetches documents from internal datastores that contain unstructured PII.
- **Tool Outputs:** An internal API returns a JSON payload containing hidden secrets or administrative tokens that the agent includes in its reasoning.
- **User Inputs:** A user pastes sensitive logs or PII directly into the chat interface.

## Assets at Risk

- **Personally Identifiable Information (PII):** Customer names, SSNs, credit card numbers, email addresses.
- **Protected Health Information (PHI):** Medical records and diagnoses.
- **Enterprise Secrets:** API keys, database connection strings, proprietary source code.
- **Compliance Certifications:** HIPAA, SOC2, GDPR violations resulting from third-party data sharing.

## Control Points

- **Input Interceptor:** Scans and scrubs the `AgentState` before the LLM node is invoked.
- **Output Interceptor:** Scans and scrubs the model's generated text before returning it to the user.
- **Tool Interceptor:** Scans the parameters of outgoing tool calls to ensure secrets aren't being smuggled out to external APIs.

## Failure Boundary

If the redaction scanner times out, fails to load its dictionary, or encounters an unsupported file type, the system must fail closed and deny the transaction. Unverified text must never be forwarded to an external LLM.

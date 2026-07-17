# Redaction Boundary

The Redaction Boundary is a deterministic filter that intercepts agent inputs and outputs to prevent the exfiltration or ingestion of sensitive data (PII, PHI, credentials, or proprietary intellectual property). 

Unlike prompt-based instructions (e.g., "Do not reveal user passwords"), which are highly susceptible to jailbreaks, a redaction boundary operates outside the LLM. It intercepts the raw text stream and scrubs it before it ever reaches the model, or before the model's output reaches the user or external systems.

## Why This Matters

Agents are often granted access to enterprise data sources (databases, internal wikis, ticketing systems) to perform their tasks. However, the agent's output is often sent to an external, third-party LLM provider (like OpenAI or Anthropic). If a user asks the agent to summarize a customer support ticket, and that ticket contains a credit card number, the agent will happily forward that credit card number to the LLM API. 

This is a massive data sovereignty and compliance violation. 

The Redaction Boundary ensures that sensitive data is scrubbed or tokenized *before* it leaves the enterprise network.

## Core Concepts

### Pre-computation (Input) Redaction
Before the state graph passes the `messages` array to the LLM, the redaction interceptor scans the text. It identifies sensitive patterns (using regex, NER models, or exact-match dictionaries) and replaces them with deterministic placeholders (e.g., `[REDACTED_CREDIT_CARD]`).

### Post-computation (Output) Redaction
Before the agent returns a final answer to the user—or executes a tool—the output is scanned. This prevents the model from hallucinating or generating sensitive data that shouldn't be exposed.

### Reversible Tokenization (Anonymization)
In many cases, the agent needs to reason about the sensitive data without seeing the actual values. For example, the boundary can replace "John Doe" with `PERSON_1`. If the agent's final output references `PERSON_1`, the boundary intercepts the response and re-injects the true value ("John Doe") before showing it to the human user, ensuring the LLM never saw the real PII.

## References

- OWASP Top 10 for LLMs (2025) — Sensitive Information Disclosure (LLM02). https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
- Simon Willison — the lethal trifecta: access to private data + untrusted content + ability to act = vulnerability. https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents

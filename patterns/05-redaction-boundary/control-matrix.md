# Control Matrix

| Threat | Control Point | Mechanism | Failure State |
| --- | --- | --- | --- |
| PII Leakage to LLM | Input Interceptor | Regex/NER scanning of state before model invocation | Redacted placeholder injected |
| Context Loss via Redaction | Tokenization Engine | Reversible token mapping (`[PERSON_1]`) stored in secure local state | Token injected |
| External Secret Exfiltration | Tool Interceptor | Scanning of tool call arguments for encoded secrets | SecurityException |
| Output Hallucination of PII | Output Interceptor | Final scan of generated text before rendering to user | Sanitized output |
| Obfuscation Bypass | Decoder Pre-processor | Decoding Base64/Hex strings before running redaction scan | SecurityException |

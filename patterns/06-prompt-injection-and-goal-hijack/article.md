# Prompt Injection and Goal Hijack

Prompt injection becomes dangerous when untrusted text is allowed to behave like
authority. In an enterprise agent, that text can arrive through user input,
retrieved OpenAPI descriptions, logs, tool results, MCP metadata, skill files,
memory, or another agent.

This pattern treats those sources differently. Retrieved content can be
evidence. Tool output can be an observation. A skill file can provide workflow
context. None of those sources can authorize a production restart, secret
export, memory policy change, or cross-agent privilege escalation.

The implementation has three important pieces:

- `assess_content()` classifies source trust, content role, findings, decoded
  findings, citation requirements, and allowed tool scope.
- `evaluate_proposed_action()` checks a proposed tool action against the
  original user goal, source trust, action type, environment, sensitive tool
  list, and purpose alignment.
- `evaluate_memory_write()` and `evaluate_delegation()` cover persistent memory
  poisoning and cross-agent scope abuse.

The core idea is containment. A detector may miss an obfuscated injection, but
an unrelated production write should still fail purpose binding and tool policy.

Run the pattern tests:

```bash
.venv/bin/python -m pytest -q patterns/06-prompt-injection-and-goal-hijack/tests
```

The verification scenarios cover direct injection, indirect RAG injection,
tool-result injection, MCP metadata injection, skill-file injection, memory
poisoning, cross-agent delegation abuse, decoded payloads, and detection-miss
containment.

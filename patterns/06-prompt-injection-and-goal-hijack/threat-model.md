# Threat Model

This pattern covers authority confusion from untrusted or lower-authority text.

## Ingress Surfaces

- user input,
- retrieved documents,
- OpenAPI and AsyncAPI descriptions,
- tool results,
- logs and tickets,
- MCP server metadata and tool descriptions,
- skill files and project instruction files,
- previous memory,
- agent-to-agent messages,
- obfuscated or split content.

## Assets at Risk

- original user task,
- tool privileges,
- secrets and credentials,
- tenant boundaries,
- approval policy,
- durable memory,
- audit integrity,
- downstream systems affected by tool calls.

## Trust Rules

- User text is task intent, not platform authority.
- Retrieved content is evidence, not authority.
- Tool results are observations, not instructions.
- Memory is context unless validated.
- Skill files and MCP descriptions are supply-chain context.
- Other agents are delegates only within explicit scope.

## Control Points

- input guard,
- source trust classifier,
- instruction/data separator,
- context builder,
- tool privilege broker,
- approval gate,
- memory write gate,
- audit sink,
- eval sink.

## Containment Goal

The goal is not to catch every malicious phrase. The goal is to stop
non-authoritative text from changing task intent, expanding capability, writing
policy-like memory, or causing real-world tool effects.

# Failure Modes

## Direct Injection

The user asks the model to ignore policy, reveal secrets, or change goals. The
input guard may detect this, but secret-bearing tools must still be denied.

## Indirect RAG Injection

Retrieved evidence contains instructions. The model may treat evidence as
authority unless the context builder labels it and the broker validates any
resulting tool call.

## Tool-Result Injection

Logs, metrics, tickets, or tool responses contain operational commands. Tool
results must remain observations.

## MCP and Tool-Description Injection

Tool metadata includes instructions that try to create preconditions such as
secret exfiltration. Metadata must not grant authority.

## Skill-File Injection

`AGENTS.md`, `CLAUDE.md`, `SKILL.md`, or similar files include instructions that
conflict with platform policy or expand tool access.

## Memory Poisoning

Untrusted content is written to durable memory and changes future behavior, such
as skipping approval or trusting a tenant.

## Cross-Agent Goal Hijack

A lower-privileged agent asks another agent to perform a privileged action.
Delegation must be scoped and auditable.

## Detection Miss

The classifier misses an encoded, split, or subtle injection. Purpose binding,
tool policy, memory gates, and approval still need to contain the action.

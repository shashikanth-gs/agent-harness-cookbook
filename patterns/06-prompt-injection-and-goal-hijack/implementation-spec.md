# Prompt Injection and Goal Hijack - Implementation Specification

## Objective

Contain direct injection, indirect RAG injection, tool-result injection, MCP
metadata injection, skill-file injection, memory poisoning, cross-agent goal
hijack, and simple obfuscated injection attempts.

The implementation must not claim to solve prompt injection. It should reduce
blast radius by separating authority from context and enforcing deterministic
checks before tool use, memory writes, or delegation.

## Inputs

- Original user goal.
- Content items with a source label such as `user`, `retrieved_document`,
  `openapi_description`, `tool_result`, `skill_file`, `mcp_tool_description`,
  `memory`, or `agent_message`.
- Proposed tool action with tool name, parameters, action type, resource,
  environment, and requesting agent.
- Candidate memory writes.
- Agent delegation requests.

## Outputs

- `InjectionAssessment` for each content item.
- `ContainmentDecision` for proposed actions.
- `MemoryWriteDecision` for durable memory writes.
- Audit-style events that explain classification, reduction, denial, approval,
  and containment.

Decision values:

- `allow`
- `deny`
- `approval_required`
- `allow_with_reduced_scope`

## Control Flow

```text
content
  -> classify source
  -> scan direct and decoded text
  -> assign role: authority, task_intent, evidence, observation, context, delegate
  -> reduce tool scope for untrusted content
  -> evaluate proposed action against purpose and sensitivity
  -> deny, require approval, or allow reduced-scope evidence gathering
  -> record audit events
```

## State Model

`InjectionAssessment` records:

- risk,
- findings,
- decoded findings,
- content trust,
- content role,
- allowed tool scope,
- citation requirement,
- memory write eligibility.

`ContainmentDecision` records:

- decision,
- reason,
- original goal,
- goal preservation,
- tool scope,
- review requirement,
- citation requirement,
- findings,
- audit events,
- policy violations.

## Policy Model

Trusted authority sources are limited to platform, system, and policy inputs.

User input is task intent. Retrieved documents are evidence. Tool results are
observations. Memory and skill files are context unless validated. Agent messages
are delegated instructions only within explicitly delegated scope.

The implementation denies actions when:

- sensitive tools are proposed,
- destructive actions are proposed,
- action purpose does not match the original user goal,
- untrusted context attempts to authorize a write,
- high-risk content proposes a non-read action,
- child agents call tools outside delegated scope.

Production writes require approval unless another policy denies them earlier.

## Edge Cases

- Base64-like content is decoded and scanned as an additional signal.
- Hidden HTML comments are treated as suspicious instruction-like text.
- Benign untrusted content still requires citation.
- Detection misses are contained by purpose binding and tool policy.
- Memory writes from untrusted instruction-like content are denied.

## Tests

The tests cover:

- direct injection detection,
- benign untrusted evidence requiring citation,
- indirect RAG injection containment,
- tool-result injection containment,
- skill-file capability expansion denial,
- MCP metadata injection classification,
- memory poisoning denial,
- cross-agent delegation scope denial,
- decoded payload detection,
- detection miss contained by tool policy,
- safe read-only evidence gathering with reduced scope.

## Expected Artifacts

- `pattern_prompt_injection_and_goal_hijack/example.py`
- `tests/test_prompt_injection_and_goal_hijack.py`
- `threat-cases.yaml`
- article and README updates that describe the actual containment behavior.

## What Not To Implement

- Do not execute real tools.
- Do not send content to an external model for classification.
- Do not claim complete prevention.
- Do not rely on regex detection as the only defense.
- Do not let skill files, MCP descriptions, or retrieved documents expand
  capability.

## Safety Constraints

All examples must stay local and deterministic. Unsafe actions must be simulated
as proposed actions and denied or escalated before any real-world effect.

# Pattern

Prompt Injection and Goal Hijack containment separates authority from context
and checks proposed actions before they produce effects.

Use these rules:

- platform and policy instructions are authority,
- user input is task intent,
- retrieved content is evidence,
- tool output is observation,
- memory is context unless validated,
- skill files and MCP descriptions are supply-chain context,
- other agents are delegates only inside explicit scope.

The pattern does not depend on detection alone. Detection can miss obfuscated or
subtle attacks. The harness still reduces scope, requires citations, checks
purpose alignment, blocks sensitive tools, gates memory writes, constrains
delegation, and records the trajectory.

Flow:

1. Classify content source and role.
2. Scan direct and decoded content for instruction-like attacks.
3. Mark untrusted evidence and observations as non-authoritative.
4. Reduce tool scope when untrusted or high-risk content is present.
5. Bind proposed actions to the original user goal.
6. Deny sensitive, destructive, unrelated, or undelegated actions.
7. Require approval for production writes that remain valid.
8. Deny untrusted memory writes that try to alter future policy.
9. Record audit events for classification, proposal, denial, approval, and
   containment.

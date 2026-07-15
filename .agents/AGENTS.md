# Agent Harness Cookbook Rules

Use `.agents/SKILL.md` as the main authoring guide for this repository.

This repository is a framework-agnostic enterprise agent harness cookbook. It
teaches how to make agent capabilities explicit, bounded, observable,
governable, testable, and auditable.

## Non-Negotiables

1. Do not add new patterns, UI, providers, or demos when the task is to deepen
   existing patterns.
2. Keep core harness code in `packages/agent_harness_cookbook/harness/`
   framework-agnostic.
3. Use local fixtures, mock tools, local traces, and local evals.
4. Treat final-answer correctness as insufficient; inspect trajectories.
5. Preserve the authority model:
   - policy/system instruction = authority,
   - user instruction = task intent,
   - retrieved content = evidence,
   - tool output = observation,
   - memory = context unless validated,
   - other agent = delegate only inside explicit scope.
6. Use containment language. Do not claim complete prevention.

## Validation

Run:

```bash
make test
.venv/bin/python -m pytest -q
```

Use `rtk` for shell commands in this environment.

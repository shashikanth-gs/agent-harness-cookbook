# Source Review

Last reviewed: 2026-07-04.

Primary current sources to check before implementation:

- OWASP LLM Top 10 2025: excessive agency, insecure output handling, and supply
  chain vulnerabilities.
- MCP security guidance for local process and tool server boundaries.
- Current coding-agent and framework docs for command execution, workspace
  boundaries, and approvals.

Design consequence: this repo should not implement uncontrolled shell execution.
Use safe mocks or tightly bounded local operations with allowlists, timeouts,
workspace checks, and approval for risky commands.

# How to Use This Repo With Coding Agents

Coding agents (like Devin, GitHub Copilot Workspace, or custom internal engineering bots) represent the highest risk category of autonomous systems. They are explicitly designed to write, modify, and execute arbitrary code. 

If you are building or deploying a coding agent, this cookbook provides the essential guardrails to prevent your agent from becoming a vector for Remote Code Execution (RCE) or intellectual property theft.

## 1. Implement Sandboxed Execution (Pattern 09)
This is non-negotiable. Coding agents must **never** execute generated code natively on the host worker node. 
- Use ephemeral containers (Docker, gVisor) or microVMs (Firecracker).
- The sandbox must have zero network egress by default to prevent SSRF or data exfiltration.
- Enforce strict CPU, Memory, and PID limits to prevent fork bombs and DoS attacks.

## 2. Enforce the Redaction Boundary (Pattern 05)
Coding agents often need to read log files, environment variables, or database dumps to debug issues.
- The Redaction Boundary must intercept all ingested files and scrub secrets (API keys, passwords, PII) *before* they are sent to the LLM.
- Use reversible tokenization so the agent can still reason about the configuration (e.g., swapping `AWS_SECRET=xyz` for `AWS_SECRET=[REDACTED_1]`).

## 3. Human-in-the-Loop for Write Actions (Pattern 02)
Coding agents can diagnose autonomously, but they should never mutate infrastructure or push code to production branches without an explicit Approval Gate.
- The approval must be cryptographically hashed to the exact `git commit` or `bash command` the agent intends to run.
- This prevents the agent from altering its payload after receiving human approval.

## 4. Limit Agency via Purpose Binding
Do not build "God Mode" coding agents. Bind their purpose.
- If the agent is triggered to fix a linting error in `frontend/`, its Tool Privilege Broker should explicitly deny any attempt to read `backend/db_config.py` or execute shell commands outside the target directory.

By applying these patterns, you can confidently deploy coding agents that accelerate developer velocity without exposing your enterprise to catastrophic supply-chain or infrastructure breaches.

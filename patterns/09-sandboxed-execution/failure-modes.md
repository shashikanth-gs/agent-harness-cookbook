# Failure Modes

## The Fallback Exploit
**Failure:** The harnessing code is written as `try: sandbox.execute(code) except Exception: subprocess.run(code)`. 
**Consequence:** An attacker intentionally provides a malformed configuration that causes the sandbox initialization to crash. The system catches the error and executes the malicious payload directly on the host machine. Execution tools must *never* have a bare-metal fallback.

## The IMDS Exfiltration (SSRF)
**Failure:** The sandbox is spun up as a standard Docker container on an AWS EC2 instance without custom networking rules.
**Consequence:** The attacker instructs the agent to run `curl http://169.254.169.254/latest/meta-data/iam/security-credentials/`. The agent successfully retrieves the host's IAM role credentials from the AWS metadata service and prints them to the chat. The sandbox must block access to cloud metadata endpoints and internal IPs.

## The State Persistence Vulnerability
**Failure:** The agent runs multiple Python scripts across different conversational turns using the *same* persistent Docker container to maintain variables in memory.
**Consequence:** The container becomes a persistent foothold. If an attacker injects a backdoor in turn 1, it remains active in turn 5. Sandboxes should ideally be stateless and ephemeral (destroyed after every tool invocation) unless strict isolation is guaranteed.

## The Fork Bomb (DoS)
**Failure:** The agent runs a Python script that endlessly spawns subprocesses (`import os; while True: os.fork()`), but the sandbox lacks a Process ID (PID) or CPU limit.
**Consequence:** The worker node crashes due to resource exhaustion, taking down the agent service for all other users. Hard resource limits (cgroups) are mandatory.

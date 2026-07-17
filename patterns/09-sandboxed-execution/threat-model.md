# Threat Model

The Sandboxed Execution pattern defends against Remote Code Execution (RCE) on the host infrastructure, data exfiltration, Server-Side Request Forgery (SSRF), and compute exhaustion (DoS).

## Ingress Surfaces

- **Code Evaluators:** REPL tools (Python, Node.js), bash terminals, or SQL execution tools exposed to the agent.
- **Malicious Prompts:** Instructions from an attacker specifically directing the agent to write and execute malicious code payloads.
- **Poisoned Artifacts:** Retrieved code snippets from untrusted wikis or internet searches that the agent attempts to run locally.

## Assets at Risk

- **Host Infrastructure:** The worker nodes running the agent framework (e.g., EC2 instances, Kubernetes pods).
- **Environment Variables:** Application secrets, DB passwords, and API keys stored in the environment of the worker node.
- **Internal Network (SSRF):** Internal microservices, metadata endpoints (e.g., AWS IMDS `169.254.169.254`), or private databases that are accessible from the worker node but should not be accessible to the agent.

## Control Points

- **Ephemeral Compute Container:** e.g., Docker, gVisor, or Firecracker microVMs that isolate the runtime environment from the host.
- **Network Egress Firewall:** `iptables` rules or container network policies that drop all outbound packets (default deny).
- **Resource Quota Manager:** Hard limits on memory (e.g., 512MB) and CPU (e.g., 0.5 vCPU) for the sandbox.
- **Timeout Enforcer:** A strict wall-clock timeout (e.g., 30 seconds) that forcefully kills the container if execution hasn't completed.

## Failure Boundary

The system must fail closed. If the sandbox backend (e.g., the Docker socket) is unavailable or throws an initialization error, the `run_code` tool must return a hard error to the agent. It must never fall back to executing via `subprocess.run` on the bare metal host.

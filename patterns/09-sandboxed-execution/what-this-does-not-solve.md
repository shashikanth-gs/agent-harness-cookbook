# What Sandboxed Execution Does Not Solve

Sandboxed execution runs agent-generated code in isolated environments
(containers, microVMs) with network isolation and resource quotas. It prevents
untrusted code from affecting the host system. It does not solve the following.

## Not Solved

- **Code correctness.** The sandbox prevents harm to the host. It does not
  verify that the generated code produces correct results. A sandboxed
  calculation can return wrong answers safely.

- **Data exfiltration via output.** The sandbox isolates execution but returns
  results to the agent. If the generated code encodes sensitive data into its
  output (steganography, base64 in return values), the sandbox does not detect
  this. Output validation requires the redaction boundary (Pattern 05).

- **Resource exhaustion within quotas.** The sandbox enforces resource limits
  (CPU, memory, time). Code that stays within quotas but wastes resources
  (e.g., allocating near-maximum memory repeatedly) is allowed. The sandbox
  prevents host impact, not inefficiency.

- **Persistent state attacks.** The sandbox should be ephemeral. If sandbox
  instances share filesystem state, cached dependencies, or network identity
  across runs, one execution can influence the next. Production sandboxes
  need fresh-instance guarantees.

- **Supply chain attacks in sandbox dependencies.** If the sandbox includes
  pre-installed packages or tools, those dependencies become an attack surface.
  The sandbox isolates the host from generated code, but does not protect
  generated code from malicious dependencies within the sandbox.

- **Real infrastructure access.** The sandbox mock in this cookbook simulates
  isolation. Production use requires real container or microVM isolation with
  seccomp profiles, namespace separation, read-only root filesystems, and
  network policies enforced at the infrastructure layer.

- **GPU and hardware access.** Sandboxing code that requires GPU access (ML
  inference, data processing) introduces additional isolation challenges not
  addressed by CPU-only container sandboxes.

## Residual Risk

Residual risk remains when sandbox isolation relies on container boundaries
without kernel-level enforcement (gVisor, Firecracker), when sandbox instances
share state between runs, or when the sandbox mock is used in environments where
real code execution occurs.

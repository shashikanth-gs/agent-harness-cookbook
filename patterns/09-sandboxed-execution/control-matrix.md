# Control Matrix

| Threat | Control Point | Mechanism | Failure State |
| --- | --- | --- | --- |
| Host RCE | Ephemeral Compute Container | Execution inside isolated namespaces (Docker/gVisor) | Execution blocks; container destroyed |
| SSRF / Data Exfiltration | Network Egress Firewall | Drop all outbound traffic; allowlist specific domains | ConnectionTimeout / NetworkError |
| DoS / Compute Exhaustion | Resource Quota Manager | Enforce max memory (e.g., 256MB) and PIDs via cgroups | OOMKill / Process termination |
| Infinite Loop | Timeout Enforcer | Strict wall-clock deadline (e.g., 15s) | TimeoutException |
| Host Env Leakage | Blank Environment Variables | Do not mount host `.env` or sensitive vars into the sandbox | N/A |

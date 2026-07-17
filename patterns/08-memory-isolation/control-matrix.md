# Control Matrix

| Threat | Control Point | Mechanism | Failure State |
| --- | --- | --- | --- |
| Cross-tenant Data Leakage | Composite Key Enforcer | All DB queries require strict `tenant_id` and `user_id` matching | Access Denied / Empty Array |
| Thread Hijacking | State Checkpointer Auth | Validation of user identity against `thread_id` ownership | SecurityException |
| Sleeper Agent Injection | Memory Input Guard | Re-scanning retrieved memories for malicious instructions before LLM insertion | Memory Redacted/Dropped |
| Persistent Exfiltration | Lifecycle Wipers | Automated hard-delete of ephemeral session data | N/A |

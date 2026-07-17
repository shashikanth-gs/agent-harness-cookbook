# Control Matrix

| Threat | Control Point | Mechanism | Failure State |
| --- | --- | --- | --- |
| Zombie Agent Exploitation | Pre-execution Interceptor | Validates that the agent's state in the registry is not `retired` | AgentLifecycleException |
| Dev/Prod Contamination | Environment Binder | Enforces that `development` agents cannot run if `env=prod` | SecurityException |
| Version Downgrade | Identity Registry | Forcefully transitions vulnerable older versions to `retired` status | AgentLifecycleException |
| Unsafe Delegation | Actor Chain Validator | Ensures all agents in the `parent->child` chain meet the env lifecycle requirements | SecurityException |

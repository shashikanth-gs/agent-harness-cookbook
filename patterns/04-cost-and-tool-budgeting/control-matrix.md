# Control Matrix

| Threat | Control Point | Mechanism | Failure State |
| --- | --- | --- | --- |
| Malicious Goal Hijack (Infinite Loop) | Graph Depth Limit | Hard cap on the number of sequential LangGraph steps per trace | Graph terminates, returns partial |
| Resource Exhaustion (Tokens) | Token Interceptor | Evaluates total token cost against `BudgetLimits` before LLM generation | BudgetExceededException |
| Backend Overload (Tools) | Tool Weighting Engine | Evaluates abstract tool cost before tool execution | BudgetExceededException |
| Multi-tenant Quota Exhaustion | Tenant Quota Registry | Centralized decrement of tenant budget using Redis/DB | BudgetExceededException |
| Child Agent Recursion | Shared Budget State | Child agents inherit and decrement from the parent agent's budget object | Parent and Child terminated |

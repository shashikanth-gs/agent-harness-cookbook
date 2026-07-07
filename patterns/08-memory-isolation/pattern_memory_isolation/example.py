from __future__ import annotations

from agent_harness_cookbook.harness.memory_isolation import (
    NamespaceMemoryManager,
    TenantContextGateway,
)

def run_example():
    print("--- Pattern 08: Memory Isolation Example ---\\n")
    
    manager = NamespaceMemoryManager()
    
    # 1. Writing to isolated memory namespaces
    print("Writing context to Tenant A and Tenant B...")
    manager.write_working_memory("tenant_A", "role", "incident_responder", ttl_seconds=60)
    manager.write_working_memory("tenant_B", "role", "guest_viewer", ttl_seconds=60)
    
    # 2. Context Gateway Enforcement
    gateway = TenantContextGateway(manager)
    
    print("\\nRequesting LLM prompt injection for Tenant A:")
    prompt_a = gateway.inject_context("Analyze the database latency.", "tenant_A")
    print(prompt_a)
    
    print("\\nRequesting LLM prompt injection for Tenant B:")
    prompt_b = gateway.inject_context("Analyze the database latency.", "tenant_B")
    print(prompt_b)
    
    # 3. Unauthorized access attempt (simulating an agent trying to access another tenant)
    print("\\nSimulating unauthorized memory read...")
    try:
        manager.read_working_memory("tenant_C", "role")
    except Exception as e:
        print(f"Blocked: {e}")

if __name__ == "__main__":
    run_example()

import pytest
import time
from agent_harness_cookbook.harness.memory_isolation import (
    NamespaceMemoryManager,
    TenantContextGateway,
    MemoryIsolationError,
)

def test_memory_isolation_and_ttl():
    manager = NamespaceMemoryManager()
    
    # Write working memory with short TTL
    manager.write_working_memory("tenant_A", "key1", "value1", ttl_seconds=1)
    
    # Write episodic memory
    manager.write_episodic_memory("tenant_B", "key1", "value2")
    
    # Test Isolation
    assert manager.read_working_memory("tenant_A", "key1") == "value1"
    with pytest.raises(MemoryIsolationError):
        manager.read_working_memory("tenant_C", "key1")
        
    assert manager.read_episodic_memory("tenant_B", "key1") == "value2"

def test_ttl_expiration():
    manager = NamespaceMemoryManager()
    manager.write_working_memory("tenant_A", "key1", "value1", ttl_seconds=0) # Expires immediately
    
    # Give it a tiny moment to ensure time.time() has advanced enough if it's super fast
    time.sleep(0.01) 
    
    assert manager.read_working_memory("tenant_A", "key1") is None

def test_context_gateway():
    manager = NamespaceMemoryManager()
    manager.write_working_memory("tenant_A", "role", "admin", ttl_seconds=100)
    
    gateway = TenantContextGateway(manager)
    prompt = gateway.inject_context("Do task", "tenant_A")
    assert "role: admin" in prompt
    assert "Do task" in prompt
    
    # Unauthorized tenant gets no context
    prompt2 = gateway.inject_context("Do task", "tenant_B")
    assert "role: admin" not in prompt2
    assert prompt2 == "Do task"

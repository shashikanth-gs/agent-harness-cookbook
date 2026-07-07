import pytest
from agent_harness_cookbook.harness.lifecycle import (
    AgentManifest,
    OperationalBounds,
    LifecycleManager,
)

def test_lifecycle_manager():
    manager = LifecycleManager("super-secret-signing-key")
    
    bounds = OperationalBounds(
        max_budget_usd=10.0,
        allowed_tools=["search", "calculator"],
        max_execution_time_ms=5000
    )
    
    manifest = AgentManifest(
        agent_id="agent-007",
        version="1.0.0",
        owner_email="admin@corp.com",
        roles=["analyst"],
        bounds=bounds
    )
    
    # Sign it
    signed_manifest = manager.sign_manifest(manifest)
    assert signed_manifest.signature is not None
    
    # Verify it
    assert manager.verify_manifest(signed_manifest) is True
    
    # Tamper with it
    signed_manifest.bounds.max_budget_usd = 1000.0
    assert manager.verify_manifest(signed_manifest) is False

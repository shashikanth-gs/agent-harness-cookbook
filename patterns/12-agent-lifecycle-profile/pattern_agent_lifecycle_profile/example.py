from __future__ import annotations

from agent_harness_cookbook.harness.lifecycle import (
    AgentManifest,
    OperationalBounds,
    LifecycleManager,
)

def run_example():
    print("--- Pattern 12: Agent Lifecycle Profile Example ---\\n")
    
    # Setup signing authority
    manager = LifecycleManager("enterprise-crypto-key-v1")
    
    print("1. Creating Agent Manifest...")
    bounds = OperationalBounds(
        max_budget_usd=50.0,
        allowed_tools=["read_logs", "query_metrics", "ask_human"],
        max_execution_time_ms=60000
    )
    
    manifest = AgentManifest(
        agent_id="incident-responder-v2",
        version="2.0.1",
        owner_email="sre-team@corp.com",
        roles=["sre-read-only"],
        bounds=bounds
    )
    
    print("Unsigned Manifest:")
    print(manifest)
    print()
    
    print("2. Securing and Deploying Agent...")
    signed_manifest = manager.sign_manifest(manifest)
    print(f"Cryptographic Signature: {signed_manifest.signature}")
    print("Manifest successfully deployed to production registry.\\n")
    
    print("3. Runtime Verification (Simulation)...")
    is_valid = manager.verify_manifest(signed_manifest)
    print(f"Runtime Integrity Check: {'Pass' if is_valid else 'Fail'}")
    
    print("\\n4. Simulating Tampering Attempt...")
    # An attacker tries to increase the agent's budget mid-flight
    signed_manifest.bounds.max_budget_usd = 9999.0
    is_valid_tampered = manager.verify_manifest(signed_manifest)
    print(f"Runtime Integrity Check (After Tampering): {'Pass' if is_valid_tampered else 'Fail'}")

if __name__ == "__main__":
    run_example()

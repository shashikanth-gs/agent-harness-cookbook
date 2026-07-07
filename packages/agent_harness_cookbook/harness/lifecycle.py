from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
import secrets

@dataclass
class OperationalBounds:
    max_budget_usd: float
    allowed_tools: list[str]
    max_execution_time_ms: int

@dataclass
class AgentManifest:
    """
    A secure identity passport for an agent, encapsulating identity, 
    operational bounds, and a cryptographic signature.
    """
    agent_id: str
    version: str
    owner_email: str
    roles: list[str]
    bounds: OperationalBounds
    signature: str | None = None

class LifecycleManager:
    """
    Manages the cryptographic signing and verification of agent manifests
    to prevent tampering before deployment.
    """
    def __init__(self, private_signing_key: str) -> None:
        self._key = private_signing_key
        
    def _hash_manifest(self, manifest: AgentManifest) -> str:
        # Exclude the signature itself from the hash
        data = {
            "agent_id": manifest.agent_id,
            "version": manifest.version,
            "owner": manifest.owner_email,
            "roles": manifest.roles,
            "bounds": asdict(manifest.bounds)
        }
        payload = f"{json.dumps(data, sort_keys=True)}:{self._key}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def sign_manifest(self, manifest: AgentManifest) -> AgentManifest:
        """Signs the manifest for deployment."""
        manifest.signature = self._hash_manifest(manifest)
        return manifest

    def verify_manifest(self, manifest: AgentManifest) -> bool:
        """
        Verifies that an agent's configuration hasn't been tampered with
        since it was signed (e.g., someone trying to increase their budget).
        """
        if not manifest.signature:
            return False
        expected_sig = self._hash_manifest(manifest)
        return secrets.compare_digest(expected_sig, manifest.signature)

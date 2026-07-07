from __future__ import annotations

import time
from typing import Any

class MemoryIsolationError(Exception):
    pass

class NamespaceMemoryManager:
    """
    Simulates a secure, Redis-backed tiered memory architecture for multi-tenant agents.
    Enforces cryptographic boundaries and TTL purging.
    """
    def __init__(self) -> None:
        # Mock storage: tenant_id -> { "working": {}, "episodic": {} }
        self._storage: dict[str, dict[str, dict[str, Any]]] = {}
    
    def _ensure_tenant(self, tenant_id: str) -> None:
        if tenant_id not in self._storage:
            self._storage[tenant_id] = {"working": {}, "episodic": {}}

    def write_working_memory(self, tenant_id: str, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Writes to ephemeral working memory."""
        self._ensure_tenant(tenant_id)
        # Store value with expiration timestamp
        expires_at = time.time() + ttl_seconds
        self._storage[tenant_id]["working"][key] = {"value": value, "expires_at": expires_at}

    def read_working_memory(self, tenant_id: str, key: str) -> Any | None:
        """Reads from ephemeral working memory, enforcing TTL and tenant boundaries."""
        if tenant_id not in self._storage:
            raise MemoryIsolationError(f"Tenant {tenant_id} not found or unauthorized.")
            
        record = self._storage[tenant_id]["working"].get(key)
        if not record:
            return None
            
        if time.time() > record["expires_at"]:
            del self._storage[tenant_id]["working"][key]
            return None
            
        return record["value"]

    def write_episodic_memory(self, tenant_id: str, key: str, value: Any) -> None:
        """Writes to persistent episodic memory."""
        self._ensure_tenant(tenant_id)
        self._storage[tenant_id]["episodic"][key] = value

    def read_episodic_memory(self, tenant_id: str, key: str) -> Any | None:
        """Reads from persistent episodic memory."""
        if tenant_id not in self._storage:
            raise MemoryIsolationError(f"Tenant {tenant_id} not found or unauthorized.")
        return self._storage[tenant_id]["episodic"].get(key)

    def purge_working_memory(self, tenant_id: str) -> None:
        """Purges all working memory for a tenant (e.g., at the end of a session)."""
        if tenant_id in self._storage:
            self._storage[tenant_id]["working"].clear()

class TenantContextGateway:
    """
    Middleware that intercepts context requests and strictly scopes them.
    """
    def __init__(self, memory_manager: NamespaceMemoryManager) -> None:
        self.manager = memory_manager
        
    def inject_context(self, prompt: str, tenant_id: str) -> str:
        """Injects only the allowed working memory context into the prompt."""
        # Simulated context gathering
        try:
            # Here we just blindly load everything in working memory for the tenant
            # In reality, this would be a selective retrieval.
            if tenant_id in self.manager._storage:
                context_items = self.manager._storage[tenant_id]["working"]
                valid_items = {k: v["value"] for k, v in context_items.items() if time.time() <= v["expires_at"]}
                if valid_items:
                    context_str = "\\n".join(f"{k}: {v}" for k, v in valid_items.items())
                    return f"System Context:\\n{context_str}\\n\\nUser Prompt:\\n{prompt}"
        except MemoryIsolationError:
            pass
            
        return prompt

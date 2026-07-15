# Memory Isolation - Implementation Specification

## Overview
Provides a `NamespaceMemoryManager` mimicking secure Redis behavior. Implements tiered memory (Working vs Episodic) with strict namespace isolation and TTL purging managed via a `TenantContextGateway`.

## Components
See `example.py` for concrete integration.
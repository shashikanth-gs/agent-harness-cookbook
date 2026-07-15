# Sandboxed Execution - Implementation Specification

## Overview
Implements a `ContainerRuntime` mock demonstrating robust sandbox execution limits, including egress network allow-listing (simulating EACCES), CPU tick constraints, and graceful handling of segfaults or timeouts.

## Components
See `example.py` for concrete integration.
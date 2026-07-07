from __future__ import annotations

import time
import subprocess
from typing import Any
from dataclasses import dataclass

@dataclass
class SandboxResult:
    stdout: str
    stderr: str
    exit_code: int
    execution_time_ms: float
    simulated_cpu_ticks: int
    memory_peak_mb: float

class ContainerRuntime:
    """
    Mocks a secure gVisor/MicroVM container runtime for executing untrusted agent code.
    """
    def __init__(self, allowed_egress_domains: list[str] | None = None) -> None:
        self.allowed_egress_domains = allowed_egress_domains or []

    def execute_code(self, code: str, timeout_seconds: int = 5, memory_limit_mb: int = 128) -> SandboxResult:
        """
        Executes arbitrary Python code in a simulated sandbox.
        In a real implementation, this would spin up an ephemeral container via an API (e.g., E2B, Docker, Firecracker)
        and execute the code there. Here, for the cookbook, we simulate the behavior and constraints.
        """
        start_time = time.time()
        
        # Simulate network egress blocking
        if "requests.get" in code or "urllib" in code:
            # Very basic heuristic just for demonstration
            allowed = False
            for domain in self.allowed_egress_domains:
                if domain in code:
                    allowed = True
                    break
            if not allowed:
                return SandboxResult(
                    stdout="",
                    stderr="SandboxError: Network egress attempted to an unauthorized domain (EACCES).",
                    exit_code=126,
                    execution_time_ms=(time.time() - start_time) * 1000,
                    simulated_cpu_ticks=10,
                    memory_peak_mb=5.0
                )

        # Simulate timeout for infinite loops
        if "while True" in code or "time.sleep(10)" in code:
             return SandboxResult(
                stdout="Simulated partial output...",
                stderr=f"SandboxError: Execution timed out after {timeout_seconds} seconds.",
                exit_code=124,
                execution_time_ms=timeout_seconds * 1000,
                simulated_cpu_ticks=9999,
                memory_peak_mb=memory_limit_mb
            )
            
        # Execute the code safely using subprocess in the current environment (mocking the container)
        # WARNING: In a real enterprise system, NEVER use subprocess to execute untrusted code on the host.
        try:
            process = subprocess.run(
                ["python3", "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            return SandboxResult(
                stdout=process.stdout,
                stderr=process.stderr,
                exit_code=process.returncode,
                execution_time_ms=(time.time() - start_time) * 1000,
                simulated_cpu_ticks=150,
                memory_peak_mb=25.5
            )
        except subprocess.TimeoutExpired:
            return SandboxResult(
                stdout="",
                stderr=f"SandboxError: Execution timed out after {timeout_seconds} seconds.",
                exit_code=124,
                execution_time_ms=timeout_seconds * 1000,
                simulated_cpu_ticks=5000,
                memory_peak_mb=50.0
            )
        except Exception as e:
             return SandboxResult(
                stdout="",
                stderr=f"SandboxError: Unexpected failure: {str(e)}",
                exit_code=1,
                execution_time_ms=0,
                simulated_cpu_ticks=0,
                memory_peak_mb=0
            )

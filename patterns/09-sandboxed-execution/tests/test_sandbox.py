import pytest
from agent_harness_cookbook.harness.sandbox import ContainerRuntime

def test_sandbox_success():
    runtime = ContainerRuntime()
    result = runtime.execute_code("print('Hello World')")
    
    assert result.exit_code == 0
    assert "Hello World" in result.stdout

def test_sandbox_network_block():
    runtime = ContainerRuntime(allowed_egress_domains=["api.github.com"])
    
    # Allowed
    result1 = runtime.execute_code("import urllib.request; print('Allowed: api.github.com')")
    assert result1.exit_code == 0
    
    # Blocked
    result2 = runtime.execute_code("import urllib.request; urllib.request.urlopen('http://evil.com')")
    assert result2.exit_code == 126
    assert "EACCES" in result2.stderr

def test_sandbox_timeout():
    runtime = ContainerRuntime()
    # Use the heuristic block for testing
    result = runtime.execute_code("while True: pass", timeout_seconds=1)
    assert result.exit_code == 124
    assert "timed out" in result.stderr

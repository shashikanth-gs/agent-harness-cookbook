from __future__ import annotations

import json

from agent_harness_cookbook.demos.rag_governance import run_rag_governance_demo


def main() -> int:
    result = run_rag_governance_demo("Which API retrieves order details and what field is required?")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

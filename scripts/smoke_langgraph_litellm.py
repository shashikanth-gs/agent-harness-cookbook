from __future__ import annotations

import json

from agent_harness_cookbook.demos.service_incident_langgraph import run_langgraph_investigation


def main() -> int:
    result = run_langgraph_investigation(
        "Orders are not being processed after the latest release. Investigate and recommend next steps.",
        request_remediation=True,
    )
    summary = {
        "workflow": result["result"]["workflow"],
        "model_step": result["trace"]["steps"][1]["payload"],
        "remediation": result["result"]["remediation"],
        "budget": result["budget"],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

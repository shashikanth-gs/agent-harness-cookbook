from __future__ import annotations

import json

from agent_harness_cookbook.providers.factory import get_model_provider


def main() -> int:
    provider = get_model_provider()
    result = provider.complete("Orders are delayed after the latest release. Summarize the investigation goal.")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

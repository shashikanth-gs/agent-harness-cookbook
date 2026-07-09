from __future__ import annotations

import json

from agent_harness_cookbook.providers.nvidia_direct import NvidiaDirectChatModel


def main() -> int:
    result = NvidiaDirectChatModel().complete("Reply with exactly: nvidia direct ok")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

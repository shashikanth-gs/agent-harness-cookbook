from __future__ import annotations

import signal
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    api = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "apps.api.main:app",
            "--reload",
            "--reload-dir",
            "apps",
            "--reload-dir",
            "packages",
            "--reload-dir",
            "patterns",
            "--port",
            "8000",
        ],
        cwd=ROOT,
    )
    site = subprocess.Popen(["npm", "--prefix", "apps/demo-site", "run", "dev"], cwd=ROOT)

    processes = [api, site]

    def stop(_signum: int, _frame: object) -> None:
        for process in processes:
            process.terminate()

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    try:
        while all(process.poll() is None for process in processes):
            signal.pause()
    except KeyboardInterrupt:
        stop(signal.SIGINT, None)
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            process.wait()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

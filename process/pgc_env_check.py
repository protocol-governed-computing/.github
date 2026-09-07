#!/usr/bin/env python3
"""PGC environment isolation check.

Fails hard if the active interpreter is not the PGC workspace venv, if any PGC
package is missing, or if any RI-0 `pgs_*` package is importable.

Usage:  python .github/process/pgc_env_check.py
"""

import importlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
EXPECTED_PREFIX = WORKSPACE / ".venv"

PGC_PACKAGES = ("compiler", "assembler", "runtime", "inspector")

# transport is NOT installed into the venv: its import roots (`adapters`, `resolver`) are
# env-provisioned from the repo root by run_http.sh, per protocol_transport/CLAUDE.md. Checked in a
# subprocess with that root on PYTHONPATH, exactly as the launcher provisions it.
TRANSPORT_ROOT = WORKSPACE / "protocol_transport"
TRANSPORT_MODULES = ("resolver.resolver", "resolver.registry", "adapters.http.binding")
THIRD_PARTY = ("click", "yaml", "jsonschema")
RI0_PACKAGES = (
    "pgs_governance",
    "pgs_capabilities",
    "pgs_compiler",
    "pgs_runtime",
    "pgs_transport",
    "pgs_blockchain",
    "pgs_change_mgmt",
    "ai_governance",
)


def main() -> int:
    failures: list[str] = []

    if Path(sys.prefix).resolve() != EXPECTED_PREFIX.resolve():
        failures.append(f"wrong interpreter: sys.prefix={sys.prefix} expected={EXPECTED_PREFIX}")

    for name in PGC_PACKAGES + THIRD_PARTY:
        try:
            module = importlib.import_module(name)
        except ImportError as exc:
            failures.append(f"missing package: {name} ({exc})")
        else:
            print(f"ok      {name:12} {module.__file__}")

    env = dict(os.environ, PYTHONPATH=str(TRANSPORT_ROOT))
    probe = subprocess.run(
        [sys.executable, "-c", "import " + ", ".join(TRANSPORT_MODULES)],
        env=env,
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        failures.append(f"transport roots not importable from {TRANSPORT_ROOT}: {probe.stderr.strip()}")
    else:
        print(f"ok      {'transport':12} {TRANSPORT_ROOT} (PYTHONPATH-provisioned: adapters, resolver)")

    for name in RI0_PACKAGES:
        if importlib.util.find_spec(name) is not None:
            failures.append(f"RI-0 LEAK: {name} is importable in the PGC venv")
        else:
            print(f"clean   {name}")

    if failures:
        print("\nPGC ENVIRONMENT CHECK FAILED", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("\nPGC ENVIRONMENT CHECK PASSED — no RI-0 dependency reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
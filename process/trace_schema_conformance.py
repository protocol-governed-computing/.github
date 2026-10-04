"""Every trace the regression produced conforms to the schema the constitution names.

`CONSTITUTION_TRACE_EXECUTION_V0` §3 says every line of a trace MUST conform to
`SCHEMA_TRACE_EVENT_V1`. Its predecessor described RI-0's trace format, and nothing compared a trace
against it. The schema and the runtime drifted until they shared no field. This reads every trace
under the data root and validates every line, so the next divergence is a failed step rather than
a discovery.

Run:  python .github/process/trace_schema_conformance.py [data root ...]   (default: <workspace>/data)
Exit: 0 if every line of every trace conforms, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

WORKSPACE = Path(__file__).resolve().parents[2]
SCHEMA = WORKSPACE / "software_governance" / "registry" / "schema" / "SCHEMA_TRACE_EVENT_V1.json"


def main() -> int:
    roots = [Path(a) for a in sys.argv[1:]] or [WORKSPACE / "data"]
    validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
    traces = sorted(p for root in roots for p in root.rglob("*.jsonl") if "traces" in p.parts)
    if not traces:
        print(f"TRACE SCHEMA CONFORMANCE FAILED — no traces under {', '.join(map(str, roots))}")
        return 1

    failures: list[str] = []
    lines = 0
    for trace in traces:
        for n, line in enumerate(trace.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            lines += 1
            record = json.loads(line)
            if n == 1 and record.get("event_type") != "trace_classification":
                failures.append(f"{trace}:1 does not begin with the classification header")
            for error in validator.iter_errors(record):
                failures.append(f"{trace}:{n} {record.get('event_type')}: {error.message}")
                break

    for f in failures[:20]:
        print(f"  {f}")
    if failures:
        print(f"TRACE SCHEMA CONFORMANCE FAILED — {len(failures)} line(s) of {lines} across "
              f"{len(traces)} trace(s)")
        return 1
    print(f"TRACE SCHEMA CONFORMANCE PASSED — {len(traces)} trace(s), {lines} line(s), every line conforms "
          f"to SCHEMA_TRACE_EVENT_V1")
    return 0


if __name__ == "__main__":
    sys.exit(main())

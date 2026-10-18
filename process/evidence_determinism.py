#!/usr/bin/env python3
"""Evidence determinism — determinative content is identical, observational content is what differs.

`3e` EV-6: determinative content MUST be identical for the same state, proposal and closure.
EV-7: observational content MUST NOT participate in any determination.

Neither could be checked before the distinction was declared, because a checker comparing everything
fails on every timestamp and one comparing nothing establishes nothing (`3e` §5.2). The classification
is `vocabulary::VOCAB_EVIDENCE_CONTENT_CLASSIFICATION_V0`, and every trace carries it as its first
record — so this check reads the trace and needs nothing else.

Executes one workflow twice into separate data roots and asserts:

  1. every trace carries its classification header
  2. determinative content is identical between the two runs
  3. observational content differs — otherwise the split is untested and the check is vacuous

Exit 0 when evidence is deterministic where it must be, 1 otherwise.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WF = "workload::WF_COLLATZ_CONJECTURE_V0"
PAYLOAD = ROOT / "conformance_workloads/workloads/collatz/test_payloads/01_happy_path.json"


def _run(data_root: Path) -> list[dict]:
    subprocess.run(
        [str(ROOT / "protocol_runtime/run.sh"), "run", "--wf", WF,
         "--payload", str(PAYLOAD), "--data-root", str(data_root)],
        check=True, capture_output=True, text=True,
    )
    traces = sorted(data_root.rglob("*.jsonl"))
    if len(traces) != 1:
        raise SystemExit(f"expected exactly one trace under {data_root}, found {len(traces)}")
    return [json.loads(line) for line in traces[0].read_text().splitlines() if line.strip()]


def _split(events: list[dict]) -> tuple[list[dict], list[dict], dict]:
    header = events[0]
    if header.get("event_type") != "trace_classification":
        raise SystemExit(
            "trace carries no classification header — evidence that states the values and not "
            "which of them are determinative is evidence a checker must guess at (3e EV-5)."
        )
    det, obs = set(header["determinative"]), set(header["observational"])
    unknown = {k for e in events[1:] for k in e} - det - obs
    if unknown:
        raise SystemExit(
            f"trace carries fields classified neither determinative nor observational: "
            f"{sorted(unknown)}. A field with no classification cannot be compared or disregarded."
        )
    return (
        [{k: v for k, v in e.items() if k in det} for e in events[1:]],
        [{k: v for k, v in e.items() if k in obs} for e in events[1:]],
        header,
    )


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="pgc-evidence-"))
    try:
        a, b = _run(tmp / "run_a"), _run(tmp / "run_b")
        det_a, obs_a, header = _split(a)
        det_b, obs_b, _ = _split(b)

        if det_a != det_b:
            print("DETERMINATIVE CONTENT DIFFERS between two executions of the same transition.")
            for i, (x, y) in enumerate(zip(det_a, det_b)):
                if x != y:
                    print(f"  event {i}:\n    run A: {x}\n    run B: {y}")
            print("\nEVIDENCE DETERMINISM FAILED — 3e EV-6.")
            return 1

        if obs_a == obs_b:
            print("OBSERVATIONAL CONTENT IS IDENTICAL across two runs.")
            print("The split is untested: if nothing observational varies, this check would pass")
            print("over a trace whose fields were all misclassified as determinative.")
            print("\nEVIDENCE DETERMINISM FAILED — vacuous.")
            return 1

        print(f"classified by : {header['classified_by']}")
        print(f"determinative : {len(header['determinative'])} fields — identical over "
              f"{len(det_a)} events")
        print(f"observational : {len(header['observational'])} fields — differ, as they must")
        print("\nEVIDENCE DETERMINISM PASSED — 3e EV-6, EV-7.")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

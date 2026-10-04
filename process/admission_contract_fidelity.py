#!/usr/bin/env python3
"""Admission contract fidelity — an IN gate admits against what its workflow actually consumes.

An IN node declares `core.inputs`: the contract a payload is admitted against. The workflow declares,
in its bindings, which payload fields it reads. The two are one fact stated twice, and they can
disagree — which they did, silently, for as long as the gate was inert and admitted everything.

One finding and one observation. The distinction cost a false-positive sweep to learn:

  UNDER-DECLARED  (finding) the workflow binds a payload field the gate does not require. The gate
                  admits a payload the workflow then cannot resolve, so a declaration gap surfaces
                  as a runtime failure instead of a refusal at the boundary (`3a` EX-7).

  OVER-DECLARED   (observation, NOT a finding) the gate requires a field no step binds. This looks
                  like a defect and usually is not: an input may be consumed by the admission
                  determination itself, or required for accountability and recorded rather than
                  read. `IN_DESIGN_INTENT_SUBMITTED_V0` says so in its own declaration —
                  `register_text` is "supplied by the driver, never read downstream" — and
                  `author_of_record` is the identity accountable for the register. Ten such were
                  first reported as defects here and every one was supplied by its caller.

                  Whether a required-but-unbound field is a defect turns on whether callers send it,
                  which is not statically decidable. It is reported so a reader can judge, and does
                  not fail the check. What catches the real ones is execution against real state.

Reads the sealed composition: the compiled `dispatch.admission` and `dispatch.bindings` are what the
runtime actually uses, not what a source file says.

Exit 0 when every gate matches its workflow, 1 otherwise.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

SNAPSHOT = Path(os.environ.get("PGC_SNAPSHOT_ROOT", "snapshot"))
PAYLOAD_REF = re.compile(r"\$\.payload\.([a-zA-Z_][a-zA-Z0-9_]*)")

# Bound by the boundary rather than by the workflow's own bindings: the admission gate is reached
# before any contract runs, and these are consumed by the authority surface rather than by a step.
BOUNDARY_SUPPLIED = {"staff_credentials", "authorization_rules", "staff_id"}


def _domains() -> list[str]:
    manifest = json.loads((SNAPSHOT / "manifest.json").read_text())
    return [d["domain"] for d in manifest.get("domains", [])]


def main() -> int:
    findings: list[tuple[str, str, str, str]] = []
    observations: list[tuple[str, str, str, str]] = []
    checked = 0

    for domain in _domains():
        dispatch_path = SNAPSHOT / "tokenized" / domain / "dispatch.json"
        vocab_path = SNAPSHOT / "vocabulary" / domain / "forward.json"
        if not dispatch_path.exists() or not vocab_path.exists():
            continue
        dispatch = json.loads(dispatch_path.read_text())
        fqdn_of = {int(h, 16): f for h, f in json.loads(vocab_path.read_text()).items()}

        admission = dispatch.get("admission", {})
        bindings = dispatch.get("bindings", {})
        entry = dispatch.get("entry", {})

        for wf_addr, e in entry.items():
            # The admission gate is the workflow's start node where that node is an IN. `entry["in"]`
            # is present only where a WF_ADMITS_VIA_IN edge was declared, which not every workflow
            # carries — the start address is the fact every workflow has.
            in_addr = e.get("in", e.get("start"))
            if in_addr is None:
                continue
            contract = admission.get(str(in_addr))
            if contract is None:
                continue
            checked += 1

            bound = set(PAYLOAD_REF.findall(json.dumps(bindings.get(wf_addr, {}))))
            required = {f for f, s in contract.items() if s.get("required")}
            gate = fqdn_of.get(int(in_addr), f"addr {in_addr}")
            wf = fqdn_of.get(int(wf_addr), f"addr {wf_addr}")

            for field in sorted(required - bound - BOUNDARY_SUPPLIED):
                observations.append((gate, wf, "OVER-DECLARED", field))
            for field in sorted(bound - set(contract) - BOUNDARY_SUPPLIED):
                findings.append((gate, wf, "UNDER-DECLARED", field))

    if observations:
        print(f"observations — required but bound by no step ({len(observations)}). Not findings: an "
              f"input may be consumed by the gate itself or recorded for accountability.")
        for gate, _wf, _kind, field in observations:
            print(f"   {gate.split('::')[-1]:44} {field!r}")
        print()

    if not findings:
        print(f"ADMISSION CONTRACT FIDELITY PASSED — {checked} gate(s), no under-declared input")
        return 0

    for gate, wf, _kind, field in findings:
        print(f"\n{gate}")
        print(f"   UNDER-DECLARED  {field!r}")
        print(f"   {wf} binds it — the gate admits a payload the workflow cannot resolve")

    print(f"\nADMISSION CONTRACT FIDELITY FAILED — {len(findings)} finding(s) over {checked} gate(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())

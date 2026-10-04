#!/usr/bin/env python3
"""Supersession — the relation is stated twice, so the two statements must agree.

`4e` SU-3 asks for the relation **once, on the successor**, with the predecessor's status derived
from it. The realization states it twice: `supersedes` on the successor and `superseded_by` on the
predecessor. Two independent assertions of one relation can disagree, and until this check nothing
compared them — which is realization-map finding 39.

They already disagreed. `transformation::STRUCTURE_FIGURE_OF_MERIT_POLICY_V1` declared its
predecessor and the predecessor said nothing, because that supersession was authored by hand while
every other one was written by construction standing an artifact down. One relation, two producers,
and no comparison.

**This does not close SU-3.** SU-3 is satisfied by deriving the back-reference, not by checking two
copies against each other; a fact stated twice and reconciled is still a fact stated twice. What this
closes is the harm — a disagreement nothing would report. Deriving is the fix and it changes the
projection, which is a larger change than the defect currently warrants.

Reads the assembled composition, because the canonical projection is what a reader consults.

Exit 0 when every supersession agrees on both sides, 1 otherwise.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

SNAPSHOT = Path(os.environ.get("PGC_SNAPSHOT_ROOT", "snapshot"))


def _listed(value) -> list[str]:
    if not value:
        return []
    return [value] if isinstance(value, str) else list(value)


def main() -> int:
    forward: dict[str, set[str]] = {}   # successor -> predecessors it claims
    backward: dict[str, set[str]] = {}  # predecessor -> successors it names
    for path in (SNAPSHOT / "canonical").rglob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        frontmatter = record.get("frontmatter") or {}
        fqdn = record.get("fqdn") or frontmatter.get("fqdn")
        if not fqdn:
            continue
        for predecessor in _listed(frontmatter.get("supersedes")):
            forward.setdefault(fqdn, set()).add(predecessor)
        for successor in _listed(frontmatter.get("superseded_by")):
            backward.setdefault(fqdn, set()).add(successor)

    findings: list[str] = []
    for successor, predecessors in sorted(forward.items()):
        for predecessor in sorted(predecessors):
            if successor not in backward.get(predecessor, set()):
                findings.append(
                    f"{successor}\n"
                    f"   claims to supersede {predecessor}, which does not name it back")
    for predecessor, successors in sorted(backward.items()):
        for successor in sorted(successors):
            if predecessor not in forward.get(successor, set()):
                findings.append(
                    f"{predecessor}\n"
                    f"   names {successor} as its successor, which claims no such thing")

    pairs = sum(len(v) for v in forward.values())
    if not findings:
        print(f"SUPERSESSION AGREEMENT PASSED — {pairs} relation(s), both sides agree on each")
        return 0

    for finding in findings:
        print(f"\n{finding}")
    print(f"\nSUPERSESSION AGREEMENT FAILED — {len(findings)} disagreement(s) over "
          f"{pairs} relation(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())

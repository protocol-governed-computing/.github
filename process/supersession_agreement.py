#!/usr/bin/env python3
"""Supersession — every relation a successor declares resolves.

`4e` SU-3 asks for the relation **once, on the successor**, with the predecessor's status derived
from it. The realization declares it so: `supersedes` on the successor, and nothing on the
predecessor. The compiler derives which artifacts are superseded from those declarations.

What remains to check is that each declaration is about something. A successor names a predecessor
the composition holds, or one `retired_identities.yaml` records as deleted (`4e` SU-12). Where the
deletion record names the predecessor's successor, the two must agree.

Reads the assembled composition, because the canonical projection is what a reader consults.

Exit 0 when every supersession resolves, 1 otherwise.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import retirement

SNAPSHOT = Path(os.environ.get("PGC_SNAPSHOT_ROOT", "snapshot"))


def _listed(value) -> list[str]:
    if not value:
        return []
    return [value] if isinstance(value, str) else list(value)


def main() -> int:
    forward: dict[str, set[str]] = {}   # successor -> predecessors it claims
    present: set[str] = set()
    for path in (SNAPSHOT / "canonical").rglob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        frontmatter = record.get("frontmatter") or {}
        fqdn = record.get("fqdn") or frontmatter.get("fqdn")
        if not fqdn:
            continue
        present.add(fqdn)
        for predecessor in _listed(frontmatter.get("supersedes")):
            forward.setdefault(fqdn, set()).add(predecessor)

    retired = retirement.retired()
    findings: list[str] = []
    deleted = 0
    for successor, predecessors in sorted(forward.items()):
        for predecessor in sorted(predecessors):
            if predecessor in present:
                continue
            if predecessor in retired:
                deleted += 1
                recorded = retired[predecessor].get("superseded_by")
                if recorded and recorded != successor:
                    findings.append(
                        f"{successor}\n"
                        f"   claims to supersede {predecessor}, whose deletion record names "
                        f"{recorded} as its successor")
                continue
            findings.append(
                f"{successor}\n"
                f"   claims to supersede {predecessor}, which is neither in the composition nor "
                f"recorded as deleted")

    pairs = sum(len(v) for v in forward.values())
    if not findings:
        print(f"SUPERSESSION AGREEMENT PASSED — {pairs} relation(s), {pairs - deleted} predecessor(s) "
              f"present, {deleted} deleted by record")
        return 0

    for finding in findings:
        print(f"\n{finding}")
    print(f"\nSUPERSESSION AGREEMENT FAILED — {len(findings)} unresolved over {pairs} relation(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())

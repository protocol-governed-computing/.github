#!/usr/bin/env python3
"""Published identity — what v5 published still means what it meant.

`4e` SU-11: a change of meaning is a new identity. A sealed release is the one record a change can be
measured against, so the check compares every identity in the sealed v5 composition
(`pgc_release/snapshot`) with the same identity in the working composition (`snapshot/`). It compares
them by the platform's declaration of what carries meaning
(`artifact::VOCAB_DECLARATION_REPRESENTATION_V0`, read through `transformation.build.sameness`).

Two differences are not a change of meaning:
- a stand-down marking (`superseded_by`) on the published identity;
- a reference moved to the declared successor of an artifact stood down with exactly one successor.

An identity added since v5 is not published, so it is not compared. An identity v5 published and the
working composition no longer holds is a finding: a published identity stays in the record. The one
exception is a removal named in `REMOVED`, with its reason. A removal is a governed change, not a
supersession, and the realization map records each one under SU-12.

The sealed composition is read, never written. Exit 0 when nothing published changed meaning and
nothing published is missing, 1 otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from transformation.build import sameness

WORKSPACE = Path(__file__).resolve().parents[2]
PUBLISHED = WORKSPACE / "pgc_release" / "snapshot"
WORKING = WORKSPACE / "snapshot"

# Published identities removed by a named decision, and why. Nothing else may leave the record.
REMOVED = {
    "ai_governance::CC_ENFORCE_LICENSE_CAP_V0":
        "nothing runs it, and its evaluation block is refused by "
        "execution_topology::INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V1",
}


def frontmatters(root: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in (root / "canonical").rglob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        frontmatter = record.get("frontmatter") or {}
        fqdn = record.get("fqdn_id") or record.get("fqdn") or frontmatter.get("fqdn")
        if fqdn:
            out[fqdn] = frontmatter
    return out


def successors(working: dict[str, dict]) -> dict[str, str]:
    """Each artifact stood down with one successor, by full name and by short code."""
    out: dict[str, str] = {}
    for fqdn, frontmatter in working.items():
        named = frontmatter.get("superseded_by")
        if isinstance(named, str):
            named = [named]
        if named and len(named) == 1:
            out[fqdn] = named[0]
            out[fqdn.split("::")[-1]] = named[0].split("::")[-1]
    return out


def main() -> int:
    published = frontmatters(PUBLISHED)
    working = frontmatters(WORKING)
    declaration = sameness.read(WORKING)
    successor = successors(working)

    findings: list[str] = []
    removed = sorted(set(published) - set(working))
    for fqdn in removed:
        if fqdn not in REMOVED:
            findings.append(f"{fqdn}\n   published in v5 and no longer in the composition")
    for fqdn in sorted(set(REMOVED) - set(removed)):
        findings.append(f"{fqdn}\n   named as removed and still in the composition, or never published")
    for fqdn in sorted(set(published) & set(working)):
        was = {k: v for k, v in published[fqdn].items() if k != "superseded_by"}
        now = {k: v for k, v in working[fqdn].items() if k != "superseded_by"}
        differences = sameness.differences(was, now, declaration, successor)
        if differences:
            shown = "\n   ".join(differences[:6])
            more = f"\n   … and {len(differences) - 6} more" if len(differences) > 6 else ""
            findings.append(f"{fqdn}\n   changed meaning since v5:\n   {shown}{more}")

    if not findings:
        for fqdn in sorted(REMOVED):
            print(f"  REMOVED  {fqdn} — {REMOVED[fqdn]}")
        print(f"PUBLISHED IDENTITY PASSED — {len(published)} identities published in v5, "
              f"none changed meaning, {len(REMOVED)} removed by name")
        return 0

    for finding in findings:
        print(f"\n{finding}")
    print(f"\nPUBLISHED IDENTITY FAILED — {len(findings)} of {len(published)} identities "
          f"published in v5")
    return 1


if __name__ == "__main__":
    sys.exit(main())

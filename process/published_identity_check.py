#!/usr/bin/env python3
"""Published identity — what v5 published still means what it meant.

`4e` SU-11: a change of meaning is a new identity. A sealed release is the one record a change can be
measured against, so the check compares every identity in the sealed v5 composition
(`pgc_release/snapshot`) with the same identity in the working composition (`snapshot/`). It compares
them by the platform's declaration of what carries meaning
(`artifact::VOCAB_DECLARATION_REPRESENTATION_V0`, read through `transformation.build.sameness`).

A reference moved to the declared successor of an artifact superseded by exactly one successor is
not a change of meaning.

An identity added since v5 is not published, so it is not compared. An identity v5 published and the
working composition no longer holds is a finding unless `retired_identities.yaml` records its
deletion (`4e` SU-12). A recorded identity is retired for good, published or not:
- one present in the working composition is a finding, because a deleted name is never used again;
- one a live artifact names is a finding, unless the artifact is its successor. A node's name and a
  routing target are places, not references.

The sealed composition is read, never written. Exit 0 when nothing published changed meaning and
nothing published is missing, 1 otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from transformation.build import sameness

import retirement

WORKSPACE = Path(__file__).resolve().parents[2]
PUBLISHED = WORKSPACE / "pgc_release" / "snapshot"
WORKING = WORKSPACE / "snapshot"


def frontmatters(root: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in (root / "canonical").rglob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        frontmatter = record.get("frontmatter") or {}
        fqdn = record.get("fqdn_id") or record.get("fqdn") or frontmatter.get("fqdn")
        if fqdn:
            out[fqdn] = frontmatter
    return out


def successors(working: dict[str, dict], retired: dict[str, dict]) -> dict[str, str]:
    """Each superseded artifact's one successor, by full name and by short code.

    The relation is declared once, on the successor, as `supersedes`, and recorded in the ledger
    where both ends are deleted. A predecessor claimed by more than one successor has no one
    successor. A chain is followed to its end: a reference moved from V0 to V3 moved to the version
    in force."""
    claimed: dict[str, list[str]] = {}
    for fqdn, frontmatter in working.items():
        named = frontmatter.get("supersedes")
        for predecessor in [named] if isinstance(named, str) else (named or []):
            claimed.setdefault(predecessor, []).append(fqdn)
    step: dict[str, str] = {p: s[0] for p, s in claimed.items() if len(s) == 1}
    for fqdn, entry in retired.items():
        if entry.get("superseded_by"):
            step.setdefault(fqdn, entry["superseded_by"])
    out: dict[str, str] = {}
    for fqdn, nxt in step.items():
        seen = {fqdn}
        while nxt in step and nxt not in seen:
            seen.add(nxt)
            nxt = step[nxt]
        out[fqdn] = nxt
        out[fqdn.split("::")[-1]] = nxt.split("::")[-1]
    return out


def main() -> int:
    published = frontmatters(PUBLISHED)
    working = frontmatters(WORKING)
    declaration = sameness.read(WORKING)
    retired = retirement.retired()
    successor = successors(working, retired)

    findings: list[str] = []
    for fqdn in sorted(set(published) - set(working)):
        if fqdn not in retired:
            findings.append(f"{fqdn}\n   published in v5, no longer in the composition, "
                            f"and no deletion is recorded")
    for fqdn in sorted(set(retired) & set(working)):
        findings.append(f"{fqdn}\n   recorded as deleted and still in the composition")
    for fqdn, frontmatter in sorted(working.items()):
        for name in sorted(retirement.naming(frontmatter, retired, fqdn.split("::")[0])):
            findings.append(f"{fqdn}\n   names {name}, which is recorded as deleted")
    for fqdn in sorted(set(published) & set(working)):
        was, now = published[fqdn], working[fqdn]
        differences = sameness.differences(was, now, declaration, successor)
        if differences:
            shown = "\n   ".join(differences[:6])
            more = f"\n   … and {len(differences) - 6} more" if len(differences) > 6 else ""
            findings.append(f"{fqdn}\n   changed meaning since v5:\n   {shown}{more}")

    if not findings:
        deleted = len(set(published) & set(retired))
        print(f"PUBLISHED IDENTITY PASSED — {len(published)} identities published in v5, "
              f"none changed meaning, {deleted} deleted by record; {len(retired)} identities "
              f"retired, none reused or named")
        return 0

    for finding in findings:
        print(f"\n{finding}")
    print(f"\nPUBLISHED IDENTITY FAILED — {len(findings)} of {len(published)} identities "
          f"published in v5")
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""What an author wrote survives compilation unchanged.

The compiler enriches; it must never overwrite. Every authored Machine Block reappears in its
compiled artifact as `frontmatter`, and the compiler is free to *add* — a resolved `fqdn_id` beside a
bare node code, an identity decomposed into `artifact_code` / `namespace` / `layer_code`, a content
hash, a reference list — but a value the author stated must come out the other side saying the same
thing. **If a stage ever changed one, the artifact would stop meaning what its author wrote and
nothing would notice.** Compilation is verified, attestation is verified, conformance is verified;
the fidelity of the authored declaration itself was not.

Measured when this was written: 420 compiled artifacts, **zero** authored values lost or altered.
That is the invariant, and it was already true — this makes it checkable rather than fortunate.

**Additive, not identical**, and the difference is the whole subtlety. Thirty artifacts do differ:
a workflow's `core.nodes` gains `fqdn_id` on every node, because a design names a bare code and the
compiler resolves it. That is reference resolution and it is exactly what the compiler is for. A
check demanding byte-identity would report all thirty as defects and be deleted within a week, which
is why this one asks the narrower and truer question:

    every key the author wrote is present, and every value the author wrote is unchanged

Nothing is said about what the compiler adds. That is the compiler's business, and other checks —
schema conformance, the governance assertions, S8_VERIFY — are where added material is judged.

Reads the assembled snapshot, so it runs after a build rather than before it. Its sibling
`implementation_closure` reads artifacts as authored and runs before one; the two ask different
questions at different moments on purpose.

Usage:  python .github/process/frontmatter_fidelity.py
Exit:   0 if every authored value survived, 1 otherwise.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

WORKSPACE = Path(__file__).resolve().parents[2]
SNAPSHOT = WORKSPACE / "snapshot" / "canonical"

# Where authored protocol source lives. The composition, as `release.sh` means it — every repo that
# contributes artifacts to a build. A repo absent here contributes nothing and is not searched.
SOURCE_ROOTS = (
    "software_governance",
    "business_domains",
    "conformance_workloads",
    "snapshot_inspector",
    "transformation",
)

MACHINE_BLOCK = re.compile(r"```yaml\n(.*?)\n```", re.S)


def authored_blocks() -> dict[str, tuple[Path, dict]]:
    """Every authored Machine Block in the composition, keyed by the identity it declares."""
    out: dict[str, tuple[Path, dict]] = {}
    for root in SOURCE_ROOTS:
        for md in sorted((WORKSPACE / root).rglob("*.md")):
            # Compiled output lives under `snapshot/` inside each source repo; it is the thing being
            # checked, not a source of truth about what was authored.
            if "snapshot" in md.parts:
                continue
            match = MACHINE_BLOCK.search(md.read_text(encoding="utf-8", errors="ignore"))
            if not match:
                continue
            try:
                block = yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                # A block that will not parse is the compiler's finding, not this one's. Reporting it
                # here would blame the author twice for one defect.
                continue
            if isinstance(block, dict) and block.get("fqdn"):
                out.setdefault(str(block["fqdn"]), (md, block))
    return out


def lost(authored: Any, compiled: Any, path: str = "") -> list[str]:
    """Every authored value that did not survive, described by where it was.

    Recursive because the loss that matters is not at the top level. A whole register vanishing would
    be obvious; one routing outcome inside one node of one workflow quietly changing is the failure
    this exists for, and it is eleven levels down.
    """
    where = path or "(root)"
    if isinstance(authored, dict):
        if not isinstance(compiled, dict):
            return [f"{where} is no longer a mapping"]
        out: list[str] = []
        for key, value in authored.items():
            if key not in compiled:
                out.append(f"{path}.{key} — dropped")
            else:
                out += lost(value, compiled[key], f"{path}.{key}")
        return out
    if isinstance(authored, list):
        if not isinstance(compiled, list):
            return [f"{where} is no longer a list"]
        if len(authored) != len(compiled):
            return [f"{where} — {len(authored)} entries authored, {len(compiled)} compiled"]
        return [d for i, (a, c) in enumerate(zip(authored, compiled))
                for d in lost(a, c, f"{path}[{i}]")]
    return [] if authored == compiled else [f"{where} — changed"]


def main() -> int:
    if not SNAPSHOT.is_dir():
        print(f"no assembled snapshot at {SNAPSHOT} — build before checking fidelity", file=sys.stderr)
        return 1

    authored = authored_blocks()
    seen: set[str] = set()
    derived = 0
    failures = 0

    for path in sorted(SNAPSHOT.rglob("*.json")):
        try:
            compiled = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(compiled, dict):
            continue
        fqdn = compiled.get("fqdn_id")
        if not fqdn:
            continue
        if fqdn not in authored:
            # An artifact the compiler synthesized — a derived ASSERT has no authored block, by
            # construction. Counted rather than ignored: a jump in this number means something
            # started being generated that used to be written.
            derived += 1
            continue
        seen.add(fqdn)
        differences = lost(authored[fqdn][1], compiled.get("frontmatter") or {})
        if differences:
            failures += 1
            print(f"  ALTERED  {fqdn}")
            print(f"           authored in {authored[fqdn][0].relative_to(WORKSPACE)}")
            for difference in differences[:8]:
                print(f"           {difference}")

    print(f"  {len(seen)} authored artifact(s) compared, {derived} compiler-synthesized, "
          f"{len(authored) - len(seen)} authored but not in the snapshot")

    if failures:
        print(f"\nFRONTMATTER FIDELITY FAILED — {failures} artifact(s) no longer say what "
              f"their author wrote")
        return 1
    print("\nFRONTMATTER FIDELITY PASSED — every authored value survived compilation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""The live transformation artifacts the genesis dossier describes: every one not stood down.

Shared by the genesis generators. Reads the registry; decides nothing.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[4] / "transformation_compilers"
MACHINE = re.compile(r"^```yaml\n(.*?)^```$", re.S | re.M)
FAMILY = {"ACTOR": "AC", "INTENT": "IN", "WORKFLOW": "WF", "CAPABILITY_CONTRACT": "CC",
          "CAPABILITY_TRANSFORM": "CT", "RUNTIME_BINDING": "RB", "VOCABULARY": "VOCAB",
          "STRUCTURE": "STRUCTURE", "EVENT": "EV"}


def subdomain(path: Path, machine: dict) -> str:
    """The subdomain an artifact belongs to: its registry folder, design or build. A structure at
    the registry root serves the phases, so it belongs to design."""
    parts = path.relative_to(REPO / "registry").parts
    return parts[0] if parts[0] in ("design", "build") else "design"


def live() -> list[dict]:
    out = []
    for path in sorted((REPO / "registry").rglob("*.md")):
        machine = yaml.safe_load(MACHINE.search(path.read_text(encoding="utf-8")).group(1)) or {}
        # A stood-down artifact is history; a vector is stated by the design as its transform's test
        # cases, not as an artifact of its own.
        if machine.get("superseded_by") or machine["artifact_kind"] == "TEST_DATA":
            continue
        out.append({"path": path, "machine": machine, "code": machine["fqdn"].split("::")[1],
                    "family": FAMILY[machine["artifact_kind"]], "subdomain": subdomain(path, machine)})
    return out


def vectors() -> list[dict]:
    """The live TEST_DATA artifacts, each with the transform it targets."""
    out = []
    for path in sorted((REPO / "registry").rglob("TEST_DATA_*.md")):
        machine = yaml.safe_load(MACHINE.search(path.read_text(encoding="utf-8")).group(1)) or {}
        if not machine.get("superseded_by"):
            out.append(machine)
    return out

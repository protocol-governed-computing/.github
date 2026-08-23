#!/usr/bin/env python3
"""Human-block fidelity — the prose beside a machine block declares nothing.

The policy is `vocabulary::VOCAB_HUMAN_BLOCK_CONSTRAINTS_V0`, read from the sealed composition.
This module is a mechanism and carries no copy of it: adding a forbidden section name is an
authoring act on that artifact, sealed and attested, never an edit here.

  1. no section whose name is in `forbidden_section_names`
  2. no prose line restating a VALUE the machine block declares, for a label in
     `restated_machine_keys`

What it does not check is whether a sentence is a citation or a restatement. That is a reading
rather than a pattern, and it is a review obligation — see the artifact's own bound, and the
Field Manual section `The human block` for the reasoning.

Exit 0 when every artifact's prose declares nothing, 1 otherwise.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOTS = ("software_governance", "conformance_workloads", "business_domains",
         "transformation", "snapshot_inspector")

ARTIFACT = re.compile(r"^[A-Z]{2,}[A-Z_]*_.*_V\d+\.md$")
YAML_BLOCK = re.compile(r"```yaml.*?```", re.S)
SECTION = re.compile(r"^##+\s+(.+?)\s*$", re.M)
BOLD_FIELD = re.compile(r"^\s*[-*]\s*\*\*([^:*]+):\*\*", re.M)

VOCAB_FQDN = "vocabulary::VOCAB_HUMAN_BLOCK_CONSTRAINTS_V0"
SNAPSHOT = Path(os.environ.get("PGC_SNAPSHOT_ROOT", "snapshot"))


def _policy() -> tuple[set[str], set[str]]:
    """The two closed sets, from the sealed composition. No fallback: a missing policy refuses."""
    for path in (SNAPSHOT / "canonical").rglob("*.json"):
        if path.name == "metadata.json":
            continue
        data = json.loads(path.read_text())
        if data.get("fqdn_id") != VOCAB_FQDN:
            continue
        fm = data.get("frontmatter") or {}
        forbidden = {e.lower() for e in fm["forbidden_section_names"]["entries"]}
        restated = {e.lower() for e in fm["restated_machine_keys"]["entries"]}
        return forbidden, restated
    raise SystemExit(
        f"{VOCAB_FQDN} is not in the composition at {SNAPSHOT} — the policy this check enforces "
        f"is not in force. Build and assemble before running it."
    )


BOLD_FIELD_VALUE = re.compile(r"^\s*[-*]\s*\*\*([^:*]+):\*\*\s*(.*)$", re.M)


def artifacts() -> list[Path]:
    out: list[Path] = []
    for root in ROOTS:
        base = Path(root)
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            if "snapshot" in p.parts or not ARTIFACT.match(p.name):
                continue
            if not re.search(r"^fqdn:", p.read_text(), re.M):
                continue
            out.append(p)
    return sorted(out)


def _machine_scalars(text: str) -> list[str]:
    """Every scalar the machine block declares, for comparison against prose."""
    out: list[str] = []
    for block in YAML_BLOCK.findall(text):
        for line in block.splitlines():
            m = re.match(r"^\s*[-\w_]+:\s*(\S.*)$", line)
            if m:
                out.append(m.group(1).strip().strip("'\""))
            m2 = re.match(r"^\s*-\s+(\S.*)$", line)
            if m2:
                out.append(m2.group(1).strip())
    return out


def prose_of(text: str) -> str:
    """Everything outside the fenced yaml. The machine block is not this check's subject."""
    return YAML_BLOCK.sub("", text)


def main() -> int:
    FORBIDDEN_SECTIONS, RESTATED = _policy()
    findings: list[tuple[Path, str, str]] = []
    files = artifacts()

    for p in files:
        prose = prose_of(p.read_text())

        for m in SECTION.finditer(prose):
            name = re.sub(r"^\d+[.)]\s*", "", m.group(1)).strip().lower()
            if name in FORBIDDEN_SECTIONS:
                findings.append((p, "SECTION", m.group(1).strip()))

        machine_values = {str(v).strip() for v in _machine_scalars(p.read_text())}
        for m in BOLD_FIELD_VALUE.finditer(prose):
            key, value = m.group(1).strip(), m.group(2).strip()
            if key.lower() not in RESTATED:
                continue
            bare = value.split("(")[0].strip().rstrip(".")
            if bare and (bare in machine_values
                         or any(bare == v.split("::")[-1] for v in machine_values)
                         or bare.upper() in {"NONE", "DRAFT", "ACTIVE"}):
                findings.append((p, "RESTATED", f"{key}: {value[:44]}"))

    if not findings:
        print(f"HUMAN BLOCK FIDELITY PASSED — {len(files)} artifacts, prose declares nothing")
        return 0

    by_file: dict[Path, list[tuple[str, str]]] = {}
    for p, kind, detail in findings:
        by_file.setdefault(p, []).append((kind, detail))

    for p, items in sorted(by_file.items()):
        print(f"\n{p}")
        for kind, detail in items:
            if kind == "SECTION":
                print(f"   SECTION   '{detail}' — a realization document states no rules")
            else:
                print(f"   RESTATED  '{detail}' — already declared in the machine block")

    print(f"\nHUMAN BLOCK FIDELITY FAILED — {len(findings)} finding(s) "
          f"across {len(by_file)} of {len(files)} artifacts")
    print(f"Policy: {VOCAB_FQDN} — add a forbidden name there, not here.")
    print("Reasoning: Field Manual, 'The human block'.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

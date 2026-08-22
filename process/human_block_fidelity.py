#!/usr/bin/env python3
"""Human-block fidelity — the prose beside a machine block declares nothing.

Enforces what is mechanically checkable in `software_governance/doc/HUMAN_BLOCK_TEMPLATE.md`:

  1. no `## Header` block                       — every fact in it is in the machine block
  2. no prose line restating a machine-block key — two copies can disagree; one cannot
  3. no normative-sounding section name          — a realization document states no rules

What it does not check is whether a sentence is a citation or a restatement (template §3.1). That
is a reading rather than a pattern, and it is a review obligation. Saying so is the template's own
§3.3 applied to this check.

Exit 0 when every artifact's prose declares nothing, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOTS = ("software_governance", "conformance_workloads", "business_domains",
         "transformation", "snapshot_inspector")

ARTIFACT = re.compile(r"^[A-Z]{2,}[A-Z_]*_.*_V\d+\.md$")
YAML_BLOCK = re.compile(r"```yaml.*?```", re.S)
SECTION = re.compile(r"^##+\s+(.+?)\s*$", re.M)
BOLD_FIELD = re.compile(r"^\s*[-*]\s*\*\*([^:*]+):\*\*", re.M)

# Section names that announce a rule is being stated. A realization document states none.
FORBIDDEN_SECTIONS = {
    "header", "header (mandatory)", "rule", "rule statement", "rules",
    "requirements", "validation rules", "enforcement scope", "version history",
    "status",
}

# Prose field labels that name a machine-block key. A label alone is not a finding — a glossary
# entry may legitimately define "Namespace". What makes it one is the prose carrying the same VALUE
# the machine block declares, which is the thing that can drift out of agreement.
RESTATED = {
    "artifact code", "artifact kind", "governed by", "version", "status",
    "supersedes", "superseded by", "fqdn", "authority", "concern", "namespace",
}
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
    print("See software_governance/doc/HUMAN_BLOCK_TEMPLATE.md §3, §4.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

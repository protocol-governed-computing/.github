"""Genesis P8: the authoring mandate, derived from the genesis P7 alone.

A mandate orders the build and decides nothing, so every row here is read from a P7 register: what
is scheduled is P7's `new_artifacts`, what each depends on is what P7's topology, compositions and
runtime bindings name, and the waves are the longest path over those dependencies. A generator is
not a design authority (v5 ruling C1): the rules judge every row it writes.

    python p8_authoring_mandate.py P7.md OUT.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

MACHINE = re.compile(r"^```yaml\n(.*?)^```$", re.S | re.M)
FULL = re.compile(r"^[a-z_][a-z0-9_.]*::[A-Z][A-Z0-9_]*_V\d+$")
ORDER = ["STRUCTURE", "VOCAB", "AC", "EV", "CT", "CC", "IN", "WF", "RB"]


class Plain(yaml.SafeDumper):
    """Writes every row out in full: a reader of the mandate never resolves an anchor."""

    def ignore_aliases(self, data):
        return True


def names(value) -> list[str]:
    """Every full name a P7 value holds, in the order it holds them."""
    if isinstance(value, str):
        return [value] if FULL.match(value) else []
    if isinstance(value, dict):
        return [n for v in value.values() for n in names(v)]
    if isinstance(value, list):
        return [n for v in value for n in names(v)]
    return []


def fields(interface: list[dict], code: str, direction: str) -> str:
    return ", ".join(f"{f['field']}:{f['type']}" for f in interface
                     if f["artifact"] == code and f["direction"] == direction)


def main(p7_path: str, out_path: str) -> None:
    p7 = yaml.safe_load(MACHINE.search(Path(p7_path).read_text(encoding="utf-8")).group(1))
    reg = p7["registers"]
    new = reg["new_artifacts"]
    declared = [a["code"] for a in new]
    family = {a["code"]: a["family"] for a in new}
    owner = {a["code"]: a["owner_subdomain"] for a in new}
    summary = {a["code"]: a["summary"] for a in new}

    deps: dict[str, list[str]] = {c: [] for c in declared}

    def add(code: str, named: list[str]) -> None:
        for n in named:
            if code in deps and n != code and n not in deps[code]:
                deps[code].append(n)

    for row in reg["execution_topology"]:
        add(row["workflow"], names(row["node"]) + names(row["routing"]))
    for row in reg["cc_composition"]:
        add(row["cc_code"], names(row["capability"]))
    for row in reg["rb_declarations"]:
        add(row["rb_code"], names(row["binds_wf"]) + names(row["cs_bindings"])
            + names(row["storage_structure"]))

    wave: dict[str, int] = {}

    def depth(code: str) -> int:
        if code not in wave:
            wave[code] = 1 + max((depth(d) for d in deps[code] if d in deps), default=0)
        return wave[code]

    for code in declared:
        depth(code)
    ordered = sorted(declared, key=lambda c: (wave[c], ORDER.index(family[c]), declared.index(c)))

    tail = max(ordered, key=lambda c: (wave[c], -ordered.index(c)))
    path = [tail]
    while authored := [d for d in deps[path[-1]] if d in deps]:
        path.append(max(authored, key=lambda d: (wave[d], -declared.index(d))))
    path.reverse()

    counts = {f: sum(1 for c in declared if family[c] == f) for f in ORDER}
    workflow_of = {row["node"]: row["workflow"] for row in reg["execution_topology"]
                   if row["node_type"] == "IN"}
    interface = reg["interface_fields"]

    notes = []
    for row in reg["cc_composition"]:
        cc, cap = row["cc_code"], row["capability"]
        if cap in owner and owner[cap] != owner[cc]:
            note = (f"Composes {cap}, which {owner[cap]} owns. {owner[cc].capitalize()} uses "
                    f"{owner[cap]} for that step only and amends nothing it owns.")
            if {"code": cc, "note": note} not in notes:
                notes.append({"code": cc, "note": note})

    registers = {
        "build_order": [{"wave": str(wave[c]), "step": str(i), "code": c, "action": "NEW",
                         "subdomain": owner[c], "depends_on": deps[c] or None}
                        for i, c in enumerate(ordered, 1)],
        "critical_path": [{"position": str(i), "code": c} for i, c in enumerate(path, 1)],
        "mandate_artifact_summary": [{
            "action": "NEW", "count": str(len(declared)),
            "description": ", ".join(f"{n} {f}" for f, n in counts.items() if n)
            + " — every identity Stage 7 assigned"}],
        "field_declarations": [{"code": c, "subdomain_field": owner[c]} for c in ordered],
        "new_capabilities": [{"code": c, "purpose": summary[c],
                              "inputs": fields(interface, c, "INPUT"),
                              "outputs": fields(interface, c, "OUTPUT")}
                             for c in ordered if family[c] == "CT"],
        "new_intents": [{"code": c, "purpose": summary[c], "workflow": workflow_of[c],
                         "inputs": fields(interface, c, "INPUT")}
                        for c in ordered if family[c] == "IN"],
        "cross_subdomain_notes": notes,
    }
    header = {**p7["document"], "phase": "p8",
              "rule_set": "transformation.schemas.REGISTER_SCHEMA_P8_V0"}
    header.pop("approval", None)
    block = yaml.dump({"document": header, "registers": registers}, Dumper=Plain,
                      sort_keys=False, allow_unicode=True, width=100)
    last = max(wave.values())
    Path(out_path).write_text(TITLE + "\n\n## Machine\n\n```yaml\n" + block + "```\n" + PROSE.format(
        count=len(declared), waves=last, path=len(path)), encoding="utf-8")


TITLE = "# Authoring Mandate — transformation / design, build"
PROSE = """
The {count} artifacts Stage 7 designed, scheduled in dependency order over {waves} waves. Every row was
derived from the Stage 7 registers by `.github/process/notes/genesis-generators/p8_authoring_mandate.py`.
Nothing is added here and nothing is dropped: the mandate orders the build, it does not decide it.

---

## 1. Build Dependency Order

A wave depends only on earlier waves. Structures, vocabularies, actors and transforms depend on
nothing the change authors. Contracts compose the transforms; workflows run over their entry points
and contracts; runtime bindings bind the workflows.

## 2. Critical Path

The longest chain of authored dependencies, {path} steps.

## 3. Artifact Summary

## 4. Subdomain Field Declarations

## 5. New Capabilities

## 6. New Intents

## 7. Cross-Subdomain Notes

Build reads a phase document with the reader design owns. That is the one place the two
subdomains meet.
"""

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

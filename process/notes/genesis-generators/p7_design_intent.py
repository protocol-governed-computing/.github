"""Genesis P7: the design intent of the transformation module, read from the live registry.

Every artifact-describing register is the inverse of construction: what `render.py` would read to
write the artifact, read back from the artifact. The design decisions, the refusals and their
deferrals are stated by hand below. A generator is not a design authority (v5 ruling C1): the rules
judge every row it writes.

    python p7_design_intent.py OUT.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

import live_inventory

NS = "transformation::"
REUSED = {
    "capability_side_effects::CS_SNAPSHOT_QUERY_V0": "Observes an assembled composition read-only through the inspection surface",
    "capability_side_effects::CS_TEXT_ARTIFACT_V0": "Persists rendered artifacts as text documents beneath a declared root",
    "execution::STRUCTURE_RUNTIME_EXECUTION_V0": "Runtime execution configuration",
    "lifecycle::CONSTITUTION_CHANGE_MGMT_V1": "States the pipeline as phases and names the invariants the design compiler enforces",
    "lifecycle::CONSTITUTION_CONSTRUCTION_V1": "States the invariants construction enforces",
}
# Inputs whose value, where stated outright rather than bound to a path, the generator its owner
# names supplies: the sealed rule set, and the observations the judging contract hands the evaluator.
GENERATED_INPUTS = {"rule_set", "observed"}
GENERATED_BY = "transformation.design.emit:emit_rule_sets"

ACTOR_CAPABILITY = "The author of record and the reviewer"
CAPABILITY = [
    ("CT_PURE_PARSE_REGISTERS", "Read a phase document into its registers"),
    ("CT_PURE_PARSE_PRIOR_PHASES", "Read the earlier phase documents a phase must agree with"),
    ("CT_PURE_EVALUATE_RULES", "Apply every rule of a phase and report each failure"),
    ("CC_JUDGE_", "Judge a phase document, with and without the composition and earlier documents"),
    ("CT_PURE_RENDER", "Render, measure and attribute the artifacts a mandate schedules"),
    ("CT_PURE_MEASURE", "Render, measure and attribute the artifacts a mandate schedules"),
    ("CT_PURE_ATTRIBUTE", "Render, measure and attribute the artifacts a mandate schedules"),
]


def capability(a: dict) -> str:
    if a["family"] == "AC":
        return ACTOR_CAPABILITY
    for prefix, name in CAPABILITY:
        if a["code"].startswith(prefix):
            return name
    return "Build an approved mandate" if a["subdomain"] == "build" else \
        "The nine phases, each with its rules and its entry point"


def cite_capability(a: dict) -> dict:
    return {"phase": "p6", "register": "governance_outcome", "key": capability(a)}


def cite_new(code: str) -> dict:
    return {"phase": "p7", "register": "new_artifacts", "key": code.split("::")[-1]}


def full(code: str) -> str:
    return code if "::" in code else NS + code


def bound(field: str, value):
    """A binding as the design states it: a path without the runtime's root, a literal, or a value
    the owner's generator supplies."""
    if field in GENERATED_INPUTS and value and not (isinstance(value, str) and value.startswith("$.")):
        return {"generated": True}
    if isinstance(value, str) and value.startswith("$."):
        return value[2:]
    return {"literal": value}


def summary(a: dict) -> str:
    core = a["machine"].get("core") or {}
    return (core.get("summary") or {
        "VOCAB_DESIGN_REGISTER_TERMS_V0": "The controlled terms the phase registers are written in",
        "VOCAB_FACT_PROVENANCE_V0": "Where a value construction wrote came from"}[a["code"]]).strip()


def fields(a: dict) -> list[dict]:
    core = a["machine"].get("core") or {}
    out = []
    sides = [("INPUT", "inputs"), ("OUTPUT", "outputs")] if a["family"] != "AC" else [("ATTRIBUTE", "attributes")]
    for direction, side in sides:
        for name, spec in (core.get(side) or {}).items():
            spec = spec or {}
            row = {"artifact": full(a["code"]), "direction": direction, "field": name,
                   "type": spec.get("type"), "required": "YES" if spec.get("required") else "NO",
                   "default": spec.get("default", spec.get("value")),
                   "meaning": " ".join(str(spec.get("description") or name.replace("_", " ")).split())}
            if spec.get("format"):
                row["format"] = spec["format"]
            out.append(row)
    return out


def topology(a: dict, rows: list, bindings: list) -> None:
    wf = full(a["code"])
    for key, node in a["machine"]["core"]["nodes"].items():
        node_type = node["type"]
        if node_type == "EXIT":
            node_type = "EXIT_SUCCESS" if node.get("status") == "SUCCESS" else "EXIT"
            rows.append({"workflow": wf, "node": key, "node_type": node_type, "routing": None,
                         "source_finding": cite_new(wf)})
            continue
        target = lambda t: t if t.startswith("EXIT") else full(t)
        row = {"workflow": wf, "node": full(key), "node_type": node_type,
               "routing": {k: target(v) for k, v in (node.get("next") or {}).items()},
               "source_finding": cite_new(wf)}
        if node.get("code") and node["code"] != key:
            row["runs"] = full(node["code"])
        rows.append(row)
        for field, value in (node.get("inputs") or {}).items():
            bindings.append({"owner": wf, "step": full(key), "direction": "INPUT", "field": field,
                             "bound_to": bound(field, value), "source_finding": cite_new(wf)})


def composition(a: dict, transforms: dict, rows: list, bindings: list) -> None:
    cc = full(a["code"])
    for index, step in enumerate(a["machine"]["core"]["pipeline"], start=1):
        is_cs = "side_effect" in step
        capability_code = step.get("side_effect") or step.get("transform")
        operation = step.get("op") if is_cs else \
            (transforms.get(capability_code, {}).get("machine") or {}).get("operation")
        consumes = list((step.get("inputs") or {}).keys())
        produces = list((step.get("outputs") or {}).keys())
        rows.append({
            "cc_code": cc, "step": str(index), "step_name": step["step"],
            "capability": capability_code, "kind": "CS" if is_cs else "CT", "operation": operation,
            "store": step.get("store"), "consumes": consumes, "produces": produces,
            "routing": step.get("on_result") or {}, "interpreted_by": None,
            "semantic_status": "SUCCESS",
            "interface": {"in": {f: f for f in consumes}, "out": {f: f for f in produces}},
        })
        for direction, side in (("INPUT", "inputs"), ("OUTPUT", "outputs")):
            for field, value in (step.get(side) or {}).items():
                bindings.append({"owner": cc, "step": step["step"], "direction": direction,
                                 "field": field, "bound_to": bound(field, value),
                                 "source_finding": cite_new(cc)})


def vocabulary(a: dict) -> list[dict]:
    out = []
    for group, spec in a["machine"].items():
        if not isinstance(spec, dict) or "entries" not in spec:
            continue
        meanings = spec.get("meanings") or {}
        for value in spec["entries"]:
            out.append({"vocabulary_code": full(a["code"]), "extends": None, "group": group,
                        "casing": spec.get("casing"), "value": value,
                        "meaning": " ".join(str(meanings.get(value) or value).split()),
                        "source_finding": cite_new(a["code"])})
    return out


def properties(a: dict) -> list[dict]:
    core = a["machine"].get("core") or {}
    out = []
    if a["family"] == "STRUCTURE":
        for key, value in core.items():
            if key in ("summary", "description"):
                continue
            out.append({"artifact": full(a["code"]), "property": key, "value": value,
                        "source_finding": cite_new(a["code"])})
    if a["family"] == "AC":
        out.append({"artifact": full(a["code"]), "property": "type", "value": core.get("type"),
                    "source_finding": cite_new(a["code"])})
    return out


def main(out_path: str) -> None:
    live = live_inventory.live()
    by_family = lambda f: [a for a in live if a["family"] == f]
    transforms = {full(a["code"]): a for a in by_family("CT")}

    topo, cc_rows, bindings, interface, impl, vocab, props = [], [], [], [], [], [], []
    for a in by_family("WF"):
        topology(a, topo, bindings)
    for a in by_family("CC"):
        composition(a, transforms, cc_rows, bindings)
    for a in live:
        if a["family"] in ("CT", "CC", "IN", "AC"):
            interface.extend(fields(a))
        if a["family"] == "VOCAB":
            vocab.extend(vocabulary(a))
        props.extend(properties(a))
    for a in by_family("CT"):
        m = a["machine"]
        impl.append({"ct_code": full(a["code"]), "callable": m["machine"]["implementation"]["callable"],
                     "operation": m["machine"]["operation"], "kind": m["machine"]["ct_kind"],
                     "purity": m["machine"]["ct_purity"], "refusal": m["core"]["refusal"],
                     "source_finding": cite_new(a["code"])})

    rb_rows, policies = [], []
    for rb in by_family("RB"):
        bindings_of = rb["machine"]["core"]["bindings"]
        bound_wfs = [w for w in by_family("WF") if w["machine"].get("runtime_binding") == full(rb["code"])]
        storage = "execution::STRUCTURE_RUNTIME_EXECUTION_V0" if rb["subdomain"] == "design" \
            else NS + "STRUCTURE_BUILD_TRANSFORMATION_CONFIG_V1"
        for w in bound_wfs:
            rb_rows.append({"rb_code": full(rb["code"]), "binds_wf": full(w["code"]),
                            "cs_bindings": list(bindings_of), "storage_structure": storage,
                            "source_finding": cite_new(rb["code"])})
        for cs, spec in bindings_of.items():
            for key, value in (spec.get("policy") or {}).items():
                policies.append({"rb_code": full(rb["code"]), "capability": cs, "key": key,
                                 "value": value, "source_finding": cite_new(rb["code"])})

    generated = [{"artifact": full(a["code"]), "generator": GENERATED_BY,
                  "generator_sources": ["registry/structures/STRUCTURE_REGISTER_SCHEMA_DISPATCH_V0.md",
                                        "registry/schema/"],
                  "source_finding": {"phase": "p4", "register": "design_decisions", "row": 2}}
                 for a in live if a["family"] == "WF" and a["code"].startswith("WF_P")
                 or a["code"].startswith("CC_JUDGE_AGAINST_")]

    cases, values = [], []
    for vector in live_inventory.vectors():
        for case in vector["cases"]:
            cite = {"phase": "p6", "register": "governance_outcome", "key": capability(
                next(a for a in live if full(a["code"]) == vector["target"]))}
            cases.append({"ct_code": vector["target"], "case": case["case_id"],
                          "expected_outcome": case["expected_outcome"], "source_finding": cite})
            for role, side in (("INPUT", "bindings"), ("EXPECTED", "expected"), ("ASSERT", "assertions")):
                for field, value in (case.get(side) or {}).items():
                    values.append({"ct_code": vector["target"], "case": case["case_id"], "role": role,
                                   "field": field, "value": value, "source_finding": cite})

    registers = {
        "design_resolution": DESIGN_RESOLUTION,
        "existing_inventory": [{"fqdn": f, "action": "REUSE", "summary": s,
                                "reason": "Reused as it stands; read, never modified.",
                                "source_finding": {"phase": "p6", "register": "pps_artifacts_requiring_action", "key": f}}
                               for f, s in REUSED.items()],
        "new_artifacts": [{"capability": capability(a), "family": a["family"], "code": full(a["code"]),
                           "summary": summary(a), "owner_subdomain": a["subdomain"], "status": "NEW",
                           "source_finding": cite_capability(a)} for a in live],
        "rb_declarations": rb_rows,
        "execution_topology": topo,
        "cc_composition": cc_rows,
        "step_bindings": bindings,
        "interface_fields": interface,
        "implementation_bindings": impl,
        "vocabulary_extensions": vocab,
        "runtime_policies": policies,
        "artifact_properties": props,
        "structure_stores": [],
        "transport_bindings": [],
        "artifact_summary": [
            {"action": "NEW", "subdomain": sub, "count": str(len(codes)), "artifacts": ", ".join(codes)}
            for sub in ("design", "build")
            for codes in [[full(a["code"]) for a in live if a["subdomain"] == sub]]],
        "generation_provenance": generated,
        "declared_reach": [],
        "refusal_discharge": [],
        "refusal_deferrals": REFUSAL_DEFERRALS,
        "refusal_governance_discharge": [],
        "molecule_steps": [],
        "molecule_step_bindings": [],
        "test_cases": cases,
        "test_case_values": values,
        "withdrawn_facts": None,
    }
    header = {"phase": "p7", "domain": "transformation", "subdomain": ["design", "build"],
              "cr": "genesis", "rule_set": "transformation.schemas.REGISTER_SCHEMA_P7_V0"}
    block = yaml.safe_dump({"document": header, "registers": registers}, sort_keys=False,
                           allow_unicode=True, width=100)
    Path(out_path).write_text(TITLE + "\n\n## Machine\n\n```yaml\n" + block + "```\n" + PROSE)


DESIGN_RESOLUTION = [
    {"decision": "Two subdomains", "business_fact": "The phases and construction fail differently and are fixed by different people.",
     "resolution": "Design holds the phases, their reading and evaluating capabilities and their rules; build holds construction and uses design only to read a document.",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 1}},
    {"decision": "One mechanism, nine rule sets", "business_fact": "The phases differ only by their rules.",
     "resolution": "One reading capability, one evaluating capability and three judging contracts serve all nine phases. Each phase workflow carries its rule set, generated from its register schema.",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 2}},
    {"decision": "The founding change is judged by its own rules", "business_fact": "The composition it is designed against holds none of the pipeline.",
     "resolution": "This design is judged by the rules it declares, each naming the platform invariant it realises.",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 3}},
    {"decision": "Construction writes through the platform", "business_fact": "Writing carries no pipeline meaning.",
     "resolution": "Construction reuses the platform's text persistence beneath a root its binding declares.",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 4}},
]

REFUSAL_DEFERRALS = [
    {"operation": "Continue past a gate", "refused_when": "The document is inadmissible or not approved.",
     "deferred_to": "The reviewer at each gate",
     "until": "A governed approval step is designed. Today an approval is recorded on the document and reported by every check, and nothing in the composition refuses to continue without it.",
     "source_finding": {"phase": "p0", "register": "operation_refusals", "row": 1}},
    {"operation": "Build a mandate", "refused_when": "The mandate has not been approved.",
     "deferred_to": "The person driving the change",
     "until": "Construction reads the mandate's approval. Today it refuses a mandate that does not determine its artifacts, and not one that is unapproved.",
     "source_finding": {"phase": "p0", "register": "operation_refusals", "row": 2}},
    {"operation": "Judge a document", "refused_when": "The composition it is designed against is not the one it names.",
     "deferred_to": "The person driving the change, through the baseline check",
     "until": "The pin is checked inside the composition. Today `tc baseline verify` checks it before a phase is run, outside any governed workflow.",
     "source_finding": {"phase": "p0", "register": "operation_refusals", "row": 3}},
]

TITLE = "# Design Intent — transformation / design, build"
PROSE = """
HOW the change is built — identities, topology, compositions, bindings and interfaces. Every register
that describes an artifact was read from the live registry by
`.github/process/notes/genesis-generators/p7_design_intent.py`; the design decisions and the refusal
deferrals are stated by hand.

---

## 1. Design Decisions Resolution

## 2. Existing Inventory

## 3. New Artifacts

## 4. Runtime Bindings

## 5. Execution Topology

## 6. Capability Contract Composition

### Step Bindings

## 7. Interface Fields

## 8. Implementation Bindings

## 9. Vocabulary Extensions

## 10. Runtime Policies

## 11. Artifact Properties

## 12. Structure Stores

## 13. Transport Bindings

## 14. Artifact Summary

## 15. Generation Provenance

## 16. Declared Reach

## 17. Refusal Discharge

### Refusal Deferrals

### Refusal Governance Discharge

## 18. Molecule Steps

### Molecule Step Bindings

## 19. Test Cases

### Test Case Values

## 20. Withdrawn Facts
"""

if __name__ == "__main__":
    main(sys.argv[1])

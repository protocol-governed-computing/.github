"""Generate book_library_mgmt cr_05_catalog P7 design intent. Writes the dossier file.

Kept as evidence under ruling C1: this dossier's P7 was written by this script, not by hand. It reads
the 26 catalog artifacts the change redeclares, as the pinned composition holds them, states each one
whole as P7 rows, and applies exactly the decisions P3 committed — nothing else. Every departure from
the artifact as it stands is in `apply_decisions`, where a reviewer can read the design by itself.

Do not run it after P7 is approved: it writes over the dossier file in place.
"""
from __future__ import annotations

import copy
import re
from pathlib import Path

import yaml

W = Path("/Users/bp/protocol-governed-computing")
D = "book_library_mgmt"
REG = W / "business_domains" / D / "registry" / "catalog"
OUT = W / "business_domains" / D / "cr_dossiers" / "cr_05_catalog" / "p7_design_intent_book_library_mgmt_catalog_v0.md"
PIN = "34c8a0e8a3f2f1b90956edd08d0d878a10347fbc058348049f8348ce0d5b8a95"


def q(code: str) -> str:
    return code if "::" in code else f"{D}::{code}"


def bare(code: str) -> str:
    return code.split("::")[-1]


WFS = ["WF_REGISTER_BOOK_V0", "WF_REGISTER_ADDITIONAL_EDITION_V0", "WF_REGISTER_PHYSICAL_COPY_V0",
       "WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V1", "WF_RETIRE_BOOK_RECORD_V0", "WF_REINSTATE_BOOK_RECORD_V0",
       "WF_RETIRE_PHYSICAL_COPY_V0", "WF_REINSTATE_PHYSICAL_COPY_V0", "WF_RETRIEVE_BOOK_DETAILS_V0",
       "WF_SEARCH_CATALOG_V0"]
INS = ["IN_" + w[3:] for w in WFS]
CCS = ["CC_CONFIRM_STAFF_AUTHORIZED_V0", "CC_VALIDATE_BOOK_SUBMISSION_V0", "CC_REGISTER_BOOK_V0",
       "CC_REGISTER_ADDITIONAL_EDITION_V0", "CC_REGISTER_PHYSICAL_COPY_V0",
       "CC_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0"]
REUSED_CCS = ["CC_APPEND_CATALOG_OPERATION_V0", "CC_ASSEMBLE_BOOK_DETAILS_V0", "CC_CLAIM_BOOK_IDENTITY_V0",
              "CC_CLAIM_COPY_BARCODE_V0", "CC_CLAIM_WORK_IDENTITY_V0", "CC_REINSTATE_BOOK_RECORD_V0",
              "CC_REINSTATE_PHYSICAL_COPY_V0", "CC_RESOLVE_BOOK_IDENTITY_V0", "CC_RESOLVE_WORK_V0",
              "CC_RETIRE_BOOK_RECORD_V0", "CC_RETIRE_PHYSICAL_COPY_V0", "CC_SEARCH_CATALOG_V0"]
DIRS = {"WF": "workflows", "IN": "intents", "CC": "capability_contracts"}

# The library's rules, as every caller in its own exercise states them today.
AUTH_RULES = [{"field": "staff_id", "op": "not_null"}, {"field": "authorized", "op": "eq", "value": True}]
BOOK = {"title": {"required": True, "type": "string"}, "author": {"required": True, "type": "string"},
        "publication_year": {"required": True, "type": "integer"},
        "subject": {"required": True, "type": "array"}}
WORK = {"title": {"required": True, "type": "string"}, "author": {"required": True, "type": "string"}}

RULES_CT = "capability_transforms::CT_PURE_VALIDATE_PARAMETER_RULES_V0"
STRUCT_CT = "capability_transforms::CT_PURE_VALIDATE_RECORD_STRUCTURE_V0"
STEP_ROUTING = {"SUCCESS": "continue", "VIOLATION": "exit"}


def machine(short: str) -> dict:
    text = (REG / DIRS[short[:2]] / f"{short}.md").read_text()
    return yaml.safe_load(re.search(r"```yaml\n(.*?)```", text, re.S).group(1))


def rule_step(name: str, parameters: dict, rules: list, last: bool = False) -> dict:
    return {"step": name, "transform": RULES_CT, "inputs": {"parameters": parameters, "rules": rules},
            "outputs": {"valid": "$.capability_result.valid"}, "result_surface": ["SUCCESS", "VIOLATION"],
            "on_result": {"SUCCESS": "exit" if last else "continue", "VIOLATION": "exit"}}


def insert_after(pipeline: list, after: str, step: dict) -> None:
    i = next(n for n, s in enumerate(pipeline) if s["step"] == after)
    pipeline.insert(i + 1, step)


def apply_decisions(art: dict[str, dict]) -> list[tuple[str, str, str, str]]:
    """The P3 decisions, applied to the artifacts as they stand. Returns the withdrawals."""
    withdrawn: list[tuple[str, str, str, str]] = []

    def withdraw(short, place, reason, finding):
        withdrawn.append((q(short), place, reason, finding))

    # Q1 — the confirming step holds the library's rules; no act passes them, no gate requires them.
    cc = art["CC_CONFIRM_STAFF_AUTHORIZED_V0"]["core"]
    del cc["inputs"]["authorization_rules"]
    cc["pipeline"][0]["inputs"]["rules"] = copy.deepcopy(AUTH_RULES)
    withdraw("CC_CONFIRM_STAFF_AUTHORIZED_V0", ".core.inputs.authorization_rules",
             "The contract holds the library's rules itself.", "S6 boundary_rules #1")
    for wf in WFS:
        del art[wf]["core"]["nodes"]["CC_CONFIRM_STAFF_AUTHORIZED_V0"]["inputs"]["authorization_rules"]
        withdraw(wf, ".core.nodes.CC_CONFIRM_STAFF_AUTHORIZED_V0.inputs.authorization_rules",
                 "The confirming contract no longer takes the rules.", "S6 boundary_rules #1")
    for gate in INS:
        del art[gate]["core"]["inputs"]["authorization_rules"]
        withdraw(gate, ".core.inputs.authorization_rules",
                 "The gate no longer requires what the catalog holds.", "S6 boundary_rules #6")

    # Q2, Q3 — the submission check holds its descriptions and refuses on what it finds.
    v = art["CC_VALIDATE_BOOK_SUBMISSION_V0"]["core"]
    for field in ("book_schema", "work_schema"):
        del v["inputs"][field]
        withdraw("CC_VALIDATE_BOOK_SUBMISSION_V0", f".core.inputs.{field}",
                 "The contract holds its description itself.", "S6 boundary_rules #1")
    for step in v["pipeline"]:
        if step["step"] == "validate_book_fields":
            step["inputs"]["schema"] = copy.deepcopy(BOOK)
        if step["step"] == "validate_work_fields":
            step["inputs"]["schema"] = copy.deepcopy(WORK)
        if step["step"] == "require_submission_complete":
            step["inputs"]["parameters"]["book_violations"] = "$.results.validate_book_fields.violations"
            step["inputs"]["parameters"]["work_violations"] = "$.results.validate_work_fields.violations"
            step["inputs"]["rules"] += [{"field": "book_violations", "op": "eq", "value": []},
                                        {"field": "work_violations", "op": "eq", "value": []}]

    # Q2, Q3 — the book and edition records hold their descriptions and refuse on what they find.
    for short, field, check in (("CC_REGISTER_BOOK_V0", "book_schema", "validate_book_fields"),
                                ("CC_REGISTER_ADDITIONAL_EDITION_V0", "edition_schema", "validate_edition_fields")):
        c = art[short]["core"]
        del c["inputs"][field]
        withdraw(short, f".core.inputs.{field}", "The contract holds its description itself.",
                 "S6 boundary_rules #1")
        next(s for s in c["pipeline"] if s["step"] == check)["inputs"]["schema"] = copy.deepcopy(BOOK)
        insert_after(c["pipeline"], check, rule_step(
            "refuse_incomplete_record", {"violations": f"$.results.{check}.violations"},
            [{"field": "violations", "op": "eq", "value": []}]))

    # Q6 — a copy is registered as registered.
    pc = art["CC_REGISTER_PHYSICAL_COPY_V0"]["core"]
    next(s for s in pc["pipeline"] if s["step"] == "assemble_copy_record")["inputs"]["fields"]["state"] = "REGISTERED"

    # Q7 — a correction keeps the record's state and meets the book description.
    up = art["CC_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0"]["core"]
    assemble = next(s for s in up["pipeline"] if s["step"] == "assemble_updated_record")
    assemble["inputs"]["fields"]["state"] = "$.results.read_book_record.book_record.state"
    insert_after(up["pipeline"], "assemble_updated_record", {
        "step": "check_corrected_record", "transform": STRUCT_CT,
        "inputs": {"record": "$.results.assemble_updated_record.updated_record", "schema": copy.deepcopy(BOOK)},
        "outputs": {"violations": "$.capability_result.violations"},
        "result_surface": ["SUCCESS", "VIOLATION"], "on_result": dict(STEP_ROUTING)})
    insert_after(up["pipeline"], "check_corrected_record", rule_step(
        "refuse_incomplete_correction",
        {"violations": "$.results.check_corrected_record.violations",
         "subject": "$.results.assemble_updated_record.updated_record.subject"},
        [{"field": "violations", "op": "eq", "value": []}, {"field": "subject", "op": "neq", "value": []}]))

    # Q4, Q5 — the register act checks and records the book it writes, with the supplied subject.
    rb = art["WF_REGISTER_BOOK_V0"]["core"]["nodes"]
    record = {"title": "$.payload.title", "author": "$.payload.author",
              "publication_year": "$.payload.publication_year", "subject": "$.payload.book_fields.subject"}
    val = rb["CC_VALIDATE_BOOK_SUBMISSION_V0"]["inputs"]
    val["book_fields"] = dict(record)
    for field in ("book_schema", "work_schema"):
        del val[field]
        withdraw("WF_REGISTER_BOOK_V0", f".core.nodes.CC_VALIDATE_BOOK_SUBMISSION_V0.inputs.{field}",
                 "The check holds its description itself.", "S6 boundary_rules #1")
    reg = rb["CC_REGISTER_BOOK_V0"]["inputs"]
    reg["book_fields"]["subject"] = "$.payload.book_fields.subject"
    del reg["book_schema"]
    withdraw("WF_REGISTER_BOOK_V0", ".core.nodes.CC_REGISTER_BOOK_V0.inputs.book_schema",
             "The contract holds its description itself.", "S6 boundary_rules #1")
    del art["IN_REGISTER_BOOK_V0"]["core"]["inputs"]["book_schema"]
    withdraw("IN_REGISTER_BOOK_V0", ".core.inputs.book_schema",
             "The gate no longer requires what the catalog holds.", "S6 boundary_rules #6")

    # Q4 — the edition act checks the edition and work it records, not supplied copies.
    ed = art["WF_REGISTER_ADDITIONAL_EDITION_V0"]["core"]["nodes"]
    val = ed["CC_VALIDATE_BOOK_SUBMISSION_V0"]["inputs"]
    val["book_fields"] = {"title": "$.payload.title", "author": "$.payload.author",
                          "publication_year": "$.payload.publication_year", "subject": "$.payload.subject"}
    val["work_fields"] = {"title": "$.payload.title", "author": "$.payload.author"}
    for field in ("book_schema", "work_schema"):
        del val[field]
        withdraw("WF_REGISTER_ADDITIONAL_EDITION_V0", f".core.nodes.CC_VALIDATE_BOOK_SUBMISSION_V0.inputs.{field}",
                 "The check holds its description itself.", "S6 boundary_rules #1")
    del ed["CC_REGISTER_ADDITIONAL_EDITION_V0"]["inputs"]["edition_schema"]
    withdraw("WF_REGISTER_ADDITIONAL_EDITION_V0", ".core.nodes.CC_REGISTER_ADDITIONAL_EDITION_V0.inputs.edition_schema",
             "The contract holds its description itself.", "S6 boundary_rules #1")
    for field in ("edition_schema", "work_schema", "edition_fields", "work_fields"):
        del art["IN_REGISTER_ADDITIONAL_EDITION_V0"]["core"]["inputs"][field]
        withdraw("IN_REGISTER_ADDITIONAL_EDITION_V0", f".core.inputs.{field}",
                 "The gate no longer requires what the catalog holds or no act reads.", "S6 boundary_rules #6")
    return withdrawn


# ---------------------------------------------------------------------------------------------------
# Reverse rendering: an artifact stated as the P7 rows construction renders it from.

def source(value) -> str:
    if isinstance(value, (dict, list)):
        return repr(value)
    if isinstance(value, str) and value.startswith("$."):
        return value[2:]
    return str(value)


def routing(nexts: dict) -> str:
    return "; ".join(f"{k} -> {q(v) if v.startswith(('CC_', 'IN_')) else v}" for k, v in nexts.items())


def ct_operation(capability: str) -> str:
    return re.sub(r"^CT_(PURE|IMPURE)_|_V\d+$", "", bare(capability))


def table(register, header, rows, flags="optional"):
    head = f"<!-- register:{register}{(' ' + flags) if flags else ''} -->"
    lines = [head, "| " + " | ".join(header) + " |", "|" + "|".join("-" * (len(h) + 2) for h in header) + "|"]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(lines) + "\n"


def main() -> None:
    art = {s: machine(s) for s in CCS + WFS + INS}
    reused = {s: machine(s) for s in REUSED_CCS}
    before = copy.deepcopy(art)
    withdrawn = apply_decisions(art)

    pps = {s: i for i, s in enumerate(CCS + WFS + INS + REUSED_CCS, 1)}
    cite = lambda s: f"S6 pps_artifacts_requiring_action #{pps[s]}"

    topo, bindings, comp, fields, props, discharge = [], [], [], [], [], []
    emitted, cts = set(), {RULES_CT, STRUCT_CT}
    for wf in WFS:
        core = art[wf]["core"]
        for node, spec in core["nodes"].items():
            if spec["type"] == "EXIT":
                emit = spec.get("emit")
                kind = "EXIT_SUCCESS" if emit else "EXIT"
                topo.append((q(wf), node, "", kind, f"emit {emit}" if emit else "—", cite(wf)))
                for ev in ([emit] if isinstance(emit, str) else emit or []):
                    props.append((q(wf), f"emit.{node}", ev, cite(wf)))
                    emitted.add(ev)
                continue
            topo.append((q(wf), q(node), "", spec["type"], routing(spec["next"]), cite(wf)))
            for field, value in (spec.get("inputs") or {}).items():
                bindings.append((q(wf), q(node), "INPUT", field, source(value),
                                 f"S7 execution_topology {q(node)}"))
        if art[wf].get("supersedes"):
            props.append((q(wf), "supersedes", art[wf]["supersedes"], cite(wf)))
    for gate in INS:
        if art[gate].get("supersedes"):
            props.append((q(gate), "supersedes", art[gate]["supersedes"], cite(gate)))
        for field, spec in art[gate]["core"]["inputs"].items():
            fields.append((q(gate), "INPUT", field, spec.get("type", "string"),
                           "YES" if spec.get("required") else "NO", "", field.replace("_", " ")))

    for cc in CCS:
        core = art[cc]["core"]
        for direction, key in (("INPUT", "inputs"), ("OUTPUT", "outputs")):
            for field, spec in core[key].items():
                fields.append((q(cc), direction, field, spec.get("type", "string"),
                               "YES" if spec.get("required") else "NO", "", field.replace("_", " ")))
        for n, step in enumerate(core["pipeline"], 1):
            cap = step.get("side_effect") or step.get("transform")
            kind = "CS" if "side_effect" in step else "CT"
            if kind == "CT":
                cts.add(cap)
            ins, outs = step.get("inputs") or {}, step.get("outputs") or {}
            iface = "in: " + ", ".join(f"{k}={k}" for k in ins)
            if outs:
                iface += "; out: " + ", ".join(
                    f"{str(v).rsplit('.', 1)[-1]}={k}" for k, v in outs.items())
            comp.append((q(cc), n, step["step"], cap, kind, step.get("op") or ct_operation(cap),
                         step.get("store", "—"), ", ".join(ins) or "—", ", ".join(outs) or "—",
                         routing(step["on_result"]).replace(" -> ", " -> "), "—", "SUCCESS", iface))
            for field, value in ins.items():
                bindings.append((q(cc), step["step"], "INPUT", field, source(value),
                                 f"S7 cc_composition {step['step']}"))
            for field, value in outs.items():
                bindings.append((q(cc), step["step"], "OUTPUT", field, source(value),
                                 f"S7 cc_composition {step['step']}"))

    for wf in WFS:
        for gate_refusal in ("VIOLATION",):
            discharge.append(("Any catalog operation", "The person performing it is not authorized staff",
                              q(wf), q("CC_CONFIRM_STAFF_AUTHORIZED_V0"), gate_refusal, "S0 operation_refusals #1"))
    discharge.append(("Registering a book", "It lacks what the library says a book must contain",
                      q("WF_REGISTER_BOOK_V0"), q("CC_VALIDATE_BOOK_SUBMISSION_V0"), "VIOLATION",
                      "S0 operation_refusals #2"))
    discharge.append(("Registering a further edition", "It lacks what the library says an edition must contain",
                      q("WF_REGISTER_ADDITIONAL_EDITION_V0"), q("CC_VALIDATE_BOOK_SUBMISSION_V0"), "VIOLATION",
                      "S0 operation_refusals #3"))

    rb = machine_rb()
    cs = ", ".join(rb["core"]["bindings"])
    rb_rows = [(q("RB_CATALOG_BINDINGS_V0"), q(wf), cs, rb["core"]["storage_structure"], cite(wf)) for wf in WFS]

    inv = []
    reasons = {
        "CC_CONFIRM_STAFF_AUTHORIZED_V0": "It takes its rules from the request.",
        "CC_VALIDATE_BOOK_SUBMISSION_V0": "It takes its descriptions from the request and refuses nothing its checks find.",
        "CC_REGISTER_BOOK_V0": "It takes its description from the request and ignores what its check finds.",
        "CC_REGISTER_ADDITIONAL_EDITION_V0": "It takes its description from the request and ignores what its check finds.",
        "CC_REGISTER_PHYSICAL_COPY_V0": "It records the copy in the state the request gives.",
        "CC_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0": "It writes the state the request gives and checks no description.",
    }
    for s in CCS + WFS + INS:
        reason = reasons.get(s) or ("It binds the rules from the request." if s.startswith("WF_")
                                    else "It requires the rules the catalog now holds.")
        inv.append((q(s), "EXTEND", art[s]["core"]["summary"], reason, cite(s)))
    for s in REUSED_CCS:
        inv.append((q(s), "REUSE", "", "Run by an act this change redeclares, unchanged.", cite(s)))
    for s in ("WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0", "IN_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0"):
        inv.append((q(s), "REUSE", "", "Superseded and not in force; named by its successor, unchanged.",
                    cite("WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V1")))
    inv.append((q("RB_CATALOG_BINDINGS_V0"), "REUSE", "", "Binds every catalog act, unchanged.",
                cite("WF_REGISTER_BOOK_V0")))
    inv.append((q("AC_LIBRARY_STAFF_V0"), "REUSE", "", "The actor every catalog act runs as, unchanged.",
                cite("WF_REGISTER_BOOK_V0")))
    for ev in sorted(emitted):
        inv.append((ev, "REUSE", "", "Announced by an act this change redeclares, unchanged.",
                    cite("WF_REGISTER_BOOK_V0")))
    deps = {RULES_CT: 1, STRUCT_CT: 2, "capability_transforms::CT_PURE_ASSEMBLE_RECORD_V0": 3}
    for ct in sorted(cts):
        where = f"S6 cross_subdomain_deps #{deps[ct]}" if ct in deps else cite("CC_REGISTER_BOOK_V0")
        inv.append((ct, "REUSE", "", "Run by a contract this change redeclares, unchanged.", where))
    for side in rb["core"]["bindings"]:
        inv.append((side, "REUSE", "", "Holds the catalog's records, unchanged.", "S6 storage_governance #1"))

    design = [
        ("Each rule is held by the step that applies it", "A rule the caller supplies is a rule the caller can widen",
         "The confirming contract holds the library's authorization rules; the checking contracts hold the book, work and edition descriptions", "S4 design_decisions #1"),
        ("Each check is followed by a rule refusing when it found anything", "An incomplete registration is refused",
         "The submission check refuses on both its checks' violations; the book record, the edition record and the correction each gain a rule step requiring none", "S4 design_decisions #2"),
        ("What each registration checks is the record it writes", "A check of a supplied copy judges nothing that is written",
         "Each registration act hands its submission check the fields it records", "S4 design_decisions #3"),
        ("The register act records the subject where callers send it", "Every present caller sends it inside the book details",
         "The recorded book's subject is bound from the supplied book details", "S4 design_decisions #4"),
        ("A copy's registered state and a correction's state are the catalog's own", "A copy is registered as registered; a correction does not change state",
         "The copy contract writes REGISTERED; the correction writes the state it read and checks the corrected record", "S4 design_decisions #5"),
        ("The gates stop requiring what the catalog holds and what no act reads", "A gate requiring an unread field refuses a correct request",
         "Every gate drops the rules; the book gate its description; the edition gate its descriptions and supplied details", "S4 design_decisions #6"),
        ("Records made before this change are left as they are", "The record is added to and never rewritten",
         "No migration, backfill or repair step is designed", "S4 design_decisions #7"),
    ]

    empty = lambda register, header: table(register, header, [])
    parts = [f"""# Stage 7 — Design Intent: book_library_mgmt / catalog

**Stage:** 7 — Design Intent
**CR:** cr_05_catalog
**Status:** DRAFT
**Feeds:** Stage 8 — Authoring Mandate

Every binding names a field the capability declares, read from the pinned baseline
`{PIN}`.

Nothing new is authored. Twenty-six artifacts the catalog already holds are redeclared whole: six
contracts hold their rules and descriptions and refuse on what they find, ten acts stop passing rules
along and check what they record, and ten gates stop requiring what the catalog holds.

---

## 1. Design Decisions Resolution

""", table("design_resolution", ["Decision", "Business Fact", "Resolution", "Source Finding"], design),
        "\n---\n\n## 2. Artifact Inventory — Existing Artifacts\n\n",
        table("existing_inventory", ["FQDN", "Action (REPLACE, REUSE, EXTEND, REVIEW)", "Summary", "Reason", "Source Finding"], inv, flags=""),
        "\n---\n\n## 3. Artifact Family Mapping — New Artifacts\n\n",
        table("new_artifacts", ["Capability", "Family (AC, IN, WF, RB, CC, CT, EV, VOCAB, STRUCTURE, TI, TE)", "Code", "Summary", "Owner Subdomain", "Status", "Source Finding"], [], flags="optional business_language=capability"),
        "\n---\n\n## 4. Runtime Binding (RB) Declarations\n\n",
        table("rb_declarations", ["RB Code", "Binds WF", "CS Bindings", "Storage Structure", "Source Finding"], rb_rows, flags=""),
        "\n---\n\n## 5. Execution Topology\n\nThe routing of every act is unchanged. What changes is what each node is handed, in §7.\n\n",
        table("execution_topology", ["Workflow", "Node", "Runs", "Node Type (IN, CC, EXIT, EXIT_SUCCESS)", "Routing", "Source Finding"], topo, flags="optional_columns=runs"),
        "\n---\n\n## 6. Capability Composition\n\n",
        table("cc_composition", ["CC Code", "Step", "Step Name", "Capability", "Kind (CT, CS)", "Operation", "Store", "Consumes", "Produces", "Routing", "Interpreted By", "Semantic Status", "Interface"], comp),
        "\n---\n\n## 7. Step Bindings\n\n",
        table("step_bindings", ["Owner", "Step", "Direction (INPUT, OUTPUT)", "Field", "Bound To", "Source Finding"], bindings),
        "\n---\n\n## 8. Interface Fields\n\n",
        table("interface_fields", ["Artifact", "Direction (INPUT, OUTPUT, ATTRIBUTE)", "Field", "Type", "Required (YES, NO)", "Default", "Meaning"], fields),
        "\n---\n\n## 9. Implementation Bindings\n\n",
        empty("implementation_bindings", ["CT Code", "Module", "Callable", "Operation", "Kind (atom, molecule)", "Purity (ct_pure, ct_impure)", "Refusal (raises, returns, never)", "Source Finding"]),
        "\n---\n\n## 10. Vocabulary Extensions\n\n",
        empty("vocabulary_extensions", ["Vocabulary Code", "Extends", "Group", "Casing", "Value", "Meaning", "Source Finding"]),
        "\n---\n\n## 11. Runtime Policies\n\n",
        empty("runtime_policies", ["RB Code", "Capability", "Key", "Value", "Source Finding"]),
        "\n---\n\n## 12. Artifact Properties\n\n",
        table("artifact_properties", ["Artifact", "Property", "Value", "Source Finding"], props),
        "\n---\n\n## 13. STRUCTURE Stores\n\n",
        empty("structure_stores", ["Store Name", "Storage Type (CS_APPENDONLY_JSONL_V0, CS_MUTABLE_JSON_V0, CS_REGISTRY_V0)", "Proposed Path", "Used By", "Source Finding"]),
        "\n---\n\n## 14. Transport Bindings\n\n",
        empty("transport_bindings", ["Artifact", "Direction (INGRESS, EGRESS)", "Operation", "Handler Kind (WF_INVOCATION, SNAPSHOT_READ)", "Handler Target", "Field", "Bound To", "Source Finding"]),
        "\n---\n\n## 15. Artifact Summary\n\n",
        table("artifact_summary", ["Action (REPLACE, EXTEND, NEW)", "Subdomain", "Count", "Artifacts"],
              [("EXTEND", "catalog", len(CCS + WFS + INS), ", ".join(q(s) for s in CCS + WFS + INS))], flags=""),
        "\n---\n\n## 16. Generation Provenance\n\n",
        empty("generation_provenance", ["Artifact", "Generator", "Generator Sources", "Source Finding"]),
        "\n---\n\n## 17. Declared Reach\n\n",
        empty("declared_reach", ["Act", "Consults", "Source Finding"]),
        "\n---\n\n## 18. Refusal Discharge\n\n",
        table("refusal_discharge", ["Operation", "Refused When", "Act", "Step", "Outcome", "Source Finding"], discharge),
        "\n---\n\n## 19. Refusal Deferrals\n\n",
        empty("refusal_deferrals", ["Operation", "Refused When", "Deferred To", "Until", "Source Finding"]),
        "\n---\n\n## 20. Refusal — Governance-Surface Discharge\n\n",
        empty("refusal_governance_discharge", ["Operation", "Refused When", "Phase", "Governing Rule", "Source Finding"]),
        "\n---\n\n## 21. Molecule Steps\n\n",
        empty("molecule_steps", ["CT Code", "Step", "Kind (atom, molecule, loop)", "Target", "Over", "Iterator", "Emits", "Source Finding"]),
        "\n---\n\n## 22. Molecule Step Bindings\n\n",
        empty("molecule_step_bindings", ["CT Code", "Step", "Role (INPUT, CARRY, UPDATE)", "Field", "Bound To", "Source Finding"]),
        "\n---\n\n## 23. Test Cases\n\n",
        empty("test_cases", ["CT Code", "Case", "Expected Outcome (SUCCESS, VIOLATION)", "Source Finding"]),
        "\n---\n\n## 24. Test Case Values\n\n",
        empty("test_case_values", ["CT Code", "Case", "Role (INPUT, EXPECTED, ASSERT, RECORDED)", "Field", "Value", "Source Finding"]),
        "\n---\n\n## 25. Withdrawn Facts\n\n",
        table("withdrawn_facts", ["Artifact", "Fact", "Reason", "Source Finding"], withdrawn),
        """
---

## gov_projection — Governed Handoff to Stage 8

| Direction | Fields |
|-----------|--------|
| **Consumes** ← Stage 6 | ownership · storage_governance · cross_subdomain_deps · pps_artifacts_requiring_action · boundary_rules · governance_outcome |
| **Emits** → Stage 8 | design_resolution · existing_inventory · new_artifacts · rb_declarations · execution_topology · cc_composition · step_bindings · interface_fields · implementation_bindings · vocabulary_extensions · runtime_policies · artifact_properties · structure_stores · artifact_summary · generation_provenance |
"""]
    OUT.write_text("".join(parts))
    print(f"wrote {OUT} — {len(topo)} topology, {len(comp)} composition, {len(bindings)} binding, "
          f"{len(withdrawn)} withdrawal rows")


def machine_rb() -> dict:
    text = (REG / "runtime_bindings" / "RB_CATALOG_BINDINGS_V0.md").read_text()
    return yaml.safe_load(re.search(r"```yaml\n(.*?)```", text, re.S).group(1))


if __name__ == "__main__":
    main()

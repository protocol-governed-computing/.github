"""Generate rule_effectivity's P7 rows from the declarations it replaces.

Every replaced workflow and contract is redeclared whole, so its topology and composition are read
from the artifact in the composition and renamed, never retyped. What the change adds — the
rule-set identity carried in and named back out — is stated here, once.

Run from the workspace root:
    python .github/process/notes/rule-effectivity-generators/p7_design_intent.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path("transformation")
REG = ROOT / "registry"
OUT = ROOT / "dossiers/rule_effectivity/p7_design_intent_transformation_design_v0.md"
D = "transformation::"

CT = [("CT_PURE_PARSE_REGISTERS_V0", "CT_PURE_PARSE_REGISTERS_V1"),
      ("CT_PURE_PARSE_PRIOR_PHASES_V0", "CT_PURE_PARSE_PRIOR_PHASES_V1"),
      ("CT_PURE_EVALUATE_RULES_V0", "CT_PURE_EVALUATE_RULES_V1")]
CC = [("CC_JUDGE_DOCUMENT_V0", "CC_JUDGE_DOCUMENT_V1"),
      ("CC_JUDGE_AGAINST_SNAPSHOT_V1", "CC_JUDGE_AGAINST_SNAPSHOT_V2"),
      ("CC_JUDGE_AGAINST_COMPOSITION_V1", "CC_JUDGE_AGAINST_COMPOSITION_V2")]
WF = [("P0", "SEED", "V0", "V1", "p0_change_seed", "p0_change_seed_template_v0", "a seed"),
      ("P1", "CHANGE_REQUEST", "V0", "V1", "p1_change_request", "p1_change_request_template_v0", "a change request"),
      ("P2", "DOMAIN_MODEL", "V1", "V2", "p2_domain_model", "p2_domain_model_template_v0", "a domain model"),
      ("P3", "ANALYSIS_LOOP", "V1", "V2", "p3_analysis_loop", "p3_analysis_loop_template_v0", "an analysis loop"),
      ("P4", "BUSINESS_MODEL", "V1", "V2", "p4_business_model", "p4_business_model_template_v0", "a business model"),
      ("P5", "BUSINESS_INTENT", "V1", "V2", "p5_business_intent", "p5_business_intent_template_v0", "a business intent"),
      ("P6", "GOVERNANCE_INTENT", "V1", "V2", "p6_governance_intent", "p6_governance_intent_template_v0", "a governance intent"),
      ("P7", "DESIGN_INTENT", "V2", "V3", "p7_design_intent", "p7_design_intent_template_v0", "a design intent"),
      ("P8", "AUTHORING_MANDATE", "V1", "V2", "p8_authoring_mandate", "p8_authoring_mandate_template_v0", "an authoring mandate")]
INTENT = {"P0": "IN_SEED_SUBMITTED_V0", "P1": "IN_CHANGE_REQUEST_SUBMITTED_V0",
          "P2": "IN_DOMAIN_MODEL_SUBMITTED_V0", "P3": "IN_ANALYSIS_LOOP_SUBMITTED_V0",
          "P4": "IN_BUSINESS_MODEL_SUBMITTED_V0", "P5": "IN_BUSINESS_INTENT_SUBMITTED_V0",
          "P6": "IN_GOVERNANCE_INTENT_SUBMITTED_V0", "P7": "IN_DESIGN_INTENT_SUBMITTED_V0",
          "P8": "IN_AUTHORING_MANDATE_SUBMITTED_V0"}
VOCAB = [("VOCAB_DOCUMENT_STANDING_V0", "document_standing", "S6 governance_outcome #6",
          "Recording the standing of a phase document", "The standings a phase document may hold: approved, migrated or re-confirmed",
          [("approved", "A person closed the document's gate under the rule set it names."),
           ("migrated", "The document was amended to satisfy a later rule set, and nobody has re-confirmed it."),
           ("reconfirmed", "A person judged the document whole under a later rule set and closed its gate again.")]),
         ("VOCAB_APPROVAL_STANDING_V0", "approval_standing", "S6 governance_outcome #5",
          "Reporting whether an approval holds under the rule set judging it", "The standings an approval may hold under a rule set: confirmed or unconfirmed",
          [("confirmed", "The approval was given under the rule set the document is judged against."),
           ("unconfirmed", "The document is judged against a rule set other than the one its approval was given under, and no person has re-confirmed it.")]),
         ("VOCAB_CORRECTION_EFFECTIVITY_V0", "correction_effectivity", "S6 governance_outcome #7",
          "Declaring whether a correction applies to documents approved before it", "Whether a correction applies to documents approved before it: retroactive or not",
          [("retroactive", "The correction can alter a prior document's admissibility. It takes a new rule-set identity and names the documents it affects."),
           ("not_retroactive", "The correction cannot alter a prior document's admissibility. It is recorded as a revision under the same identity.")])]

RENAME = {o: n for o, n in CT + CC} | {f"WF_{p}_{n}_ADMISSIBILITY_{o}": f"WF_{p}_{n}_ADMISSIBILITY_{v}" for p, n, o, v, *_ in WF}


def machine(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(re.search(r"```yaml\n(.*?)```", text, re.S).group(1))


def find(code: str) -> Path:
    return next(REG.rglob(f"{code}.md"))


def cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def row(*cells) -> str:
    return "| " + " | ".join(cell(c) for c in cells) + " |"


def flow(v) -> str:
    return yaml.safe_dump(v, default_flow_style=True, sort_keys=False, width=10_000).strip()


SCHEMA = {p: f"transformation.schemas.SCHEMA_REGISTERS_{p}_{n}_V0" for p, n, *_ in WF}


def wf_code(p, n, v):
    return f"WF_{p}_{n}_ADMISSIBILITY_{v}"


# --- registers -------------------------------------------------------------------------------

def design_resolution():
    rows = [
        ("Where a document carries its registers",
         "The judging receives the same data in either form.",
         "One YAML Machine block per phase document, the first fenced yaml block, holds a header mapping and a registers mapping. Each register is a list of rows, each row a mapping from column name to string value, columns in declared order; a narrative register is a string. The reader takes a register's columns from its first row, so an empty register keeps the one-row sentinel, its first column reading NONE IDENTIFIED and the others empty. Prose stays Markdown around the block, and the reader returns the header, sections and registers the table reader returned. Values inside cells stay strings.",
         "S4 design_decisions #1"),
        ("What construction reads",
         "Construction meets this change only through the shared reading.",
         "The construction contract runs the new reading in place of the old and keeps its own splitting of values inside cells. It keeps its identity; only the name of the reading it runs changes.",
         "S4 design_decisions #2"),
        ("What a rule-set identity is",
         "The identity follows the rules themselves, not the phase's workflow version.",
         "Each phase has a register schema, a JSON file whose $id is the identity, such as transformation.schemas.SCHEMA_REGISTERS_P3_ANALYSIS_LOOP_V0. In this change it holds the $id, a digest of the rule set sealed in its workflow, and its revision history; its shape is filled in by the change that moves the rules out of the code. The workflow seals the $id as a literal input beside the rule set. Emission refuses a sealed rule set whose digest the schema does not record.",
         "S4 design_decisions #3"),
        ("How a document is judged under the rule set it names",
         "A superseded rule set stays available in the composition.",
         "The check selects the phase workflow whose sealed identity equals the rule set the document names, and the current workflow. It reports both verdicts, each naming its rule set. A document naming a rule set no workflow seals is refused, never judged by a substitute.",
         "S4 design_decisions #4"),
        ("What happens to v5 dossiers",
         "Dossiers approved under v5 stay as published.",
         "Nothing reads them. The table reader is the converter for the test documents only, and is deleted once the two forms are shown to receive the same findings.",
         "S4 design_decisions #5"),
        ("How a document, an approval and its standing are recorded",
         "A document is judged against both the rules it was authored under and the current rules.",
         "The header names the rule set the document was authored under (rule_set), the rule set its approval was given under (approved_under) and its standing (standing), a value of the document-standing vocabulary. The gate reviewer writes approved_under and standing. Whether an approval holds is derived, never stored: the judging reports it confirmed when approved_under equals the rule set judging, and unconfirmed otherwise.",
         "S4 design_decisions #6"),
        ("How a migration is recorded",
         "A document amended to satisfy a later rule set says so.",
         "Its standing reads migrated and migrated_from names the rule set it was approved under. A person re-confirming it sets standing to reconfirmed and approved_under to the later rule set.",
         "S4 gap_register GAP-6"),
        ("How a correction declares its effectivity",
         "A correction declares its own effectivity, and the rule set records the declaration as governed history.",
         "A correction adds a revision to the phase's schema: the new digest, its effectivity from the correction-effectivity vocabulary, and for a retroactive correction the documents it affects. A retroactive correction takes a new $id and so a new workflow version; a correction that is not retroactive keeps the $id.",
         "S4 gap_register GAP-7"),
        ("How identical verdicts are proven",
         "Different findings can produce the same count.",
         "Each test document is converted mechanically by the table reader and judged in both forms by the same rule set. The findings are compared by rule, register, row and detail. Any difference is a regression, and the table reader is deleted only when there is none.",
         "S4 gap_register GAP-8"),
    ]
    return [row(*r) for r in rows]


def existing_inventory():
    out = []
    for i, (old, new) in enumerate(CT + CC, start=1):
        s = machine(find(old))["core"]["summary"]
        out.append(row(D + old, "REPLACE", s, f"Its meaning changes, so {new} supersedes it.", f"S6 pps_artifacts_requiring_action #{i}"))
    for i, (p, n, o, v, *_ ) in enumerate(WF, start=7):
        s = machine(find(wf_code(p, n, o)))["core"]["summary"]
        out.append(row(D + wf_code(p, n, o), "REPLACE", s, f"It gains a sealed rule-set identity, so {wf_code(p, n, v)} supersedes it.", f"S6 pps_artifacts_requiring_action #{i}"))
    for i, (p, n, o, v, *_ ) in enumerate(WF, start=7):
        s = machine(find(INTENT[p]))["core"]["summary"]
        out.append(row(D + INTENT[p], "REPOINT", s, f"Starts {wf_code(p, n, o)}; it names the successor and keeps its identity.", f"S6 pps_artifacts_requiring_action #{i}"))
    out.append(row(D + "CC_CONSTRUCT_ARTIFACTS_V0", "REPOINT", machine(find("CC_CONSTRUCT_ARTIFACTS_V0"))["core"]["summary"],
                   "Runs the reading this change replaces; it names the successor and keeps its identity.", "S6 pps_artifacts_requiring_action #16"))
    out.append(row(D + "AC_GATE_REVIEWER_V0", "REUSE", "", "Closes a gate, and re-confirms an approval under a later rule set.", "S6 pps_artifacts_requiring_action #17"))
    out.append(row(D + "RB_TRANSFORMATION_BINDINGS_V0", "REUSE", "", "Binds read-only observation for every phase workflow. Unchanged; the new workflows bind it.", "transformation::RB_TRANSFORMATION_BINDINGS_V0"))
    out.append(row("capability_side_effects::CS_SNAPSHOT_QUERY_V0", "REUSE", "", "The observation the later phases' contracts compose. Unchanged.", "capability_side_effects::CS_SNAPSHOT_QUERY_V0"))
    out.append(row(D + "CC_PERSIST_ARTIFACTS_V0", "REVIEW", "", "Names a replaced contract in its explanation only. Unchanged.", "transformation::CC_PERSIST_ARTIFACTS_V0"))
    out.append(row(D + "STRUCTURE_BUILD_TRANSFORMATION_CONFIG_V0", "REVIEW", "", "Declares what the domain compiles. Unchanged; named because the authored artifacts are compiled under it.", "S6 pps_artifacts_requiring_action #18"))
    return out


NEW_CAP = {
    "CT_PURE_PARSE_REGISTERS_V1": ("Reading a phase document's registers from its structured block", "S6 governance_outcome #1"),
    "CT_PURE_PARSE_PRIOR_PHASES_V1": ("Reading a prior phase's registers from its structured block", "S6 governance_outcome #1"),
    "CT_PURE_EVALUATE_RULES_V1": ("Judging a document and naming the rule set that judged it", "S6 governance_outcome #4"),
    "CC_JUDGE_DOCUMENT_V1": ("Judging a seed or change request under a named rule set", "S6 governance_outcome #4"),
    "CC_JUDGE_AGAINST_SNAPSHOT_V2": ("Judging a later phase against the composition under a named rule set", "S6 governance_outcome #4"),
    "CC_JUDGE_AGAINST_COMPOSITION_V2": ("Judging the analysis loop against the composition under a named rule set", "S6 governance_outcome #4"),
}
NEW_SUMMARY = {
    "CT_PURE_PARSE_REGISTERS_V1": "Read a phase document's header and registers from its Machine block, and its sections from its prose",
    "CT_PURE_PARSE_PRIOR_PHASES_V1": "Read the upstream phase documents a phase is judged against, each from its Machine block",
    "CT_PURE_EVALUATE_RULES_V1": "Evaluate a declared rule set against a parsed document, naming the rule set and whether the document's approval holds under it",
    "CC_JUDGE_DOCUMENT_V1": "Parse a phase document and judge it against a declared rule set, naming that rule set in the verdict",
    "CC_JUDGE_AGAINST_SNAPSHOT_V2": "Parse a phase document and its priors, observe the composition, and judge them together under a named rule set",
    "CC_JUDGE_AGAINST_COMPOSITION_V2": "Parse an analysis loop and its priors, observe the composition's declarations, and judge them together under a named rule set",
}


def new_artifacts():
    out = []
    for _, new in CT + CC:
        cap, src = NEW_CAP[new]
        out.append(row(cap, new[:2], D + new, NEW_SUMMARY[new], "design", "NEW", src))
    for p, n, o, v, _, _, what in WF:
        out.append(row(f"Deciding whether {what} is admissible under a named rule set", "WF", D + wf_code(p, n, v),
                       f"Decide whether {what} is admissible, under a rule set with an identity", "design", "NEW", "S6 governance_outcome #2"))
    for code, _, src, cap, summary, _ in VOCAB:
        out.append(row(cap, "VOCAB", D + code, summary, "design", "NEW", src))
    return out


def rb_declarations():
    return [row(D + "RB_TRANSFORMATION_BINDINGS_V0", D + wf_code(p, n, v), "capability_side_effects::CS_SNAPSHOT_QUERY_V0",
                "execution::STRUCTURE_RUNTIME_EXECUTION_V0", f"S6 pps_artifacts_requiring_action #{i}")
            for i, (p, n, o, v, *_ ) in enumerate(WF, start=7)]


def execution_topology():
    out = []
    for i, (p, n, o, v, *_ ) in enumerate(WF, start=7):
        wf = machine(find(wf_code(p, n, o)))
        nodes = wf["core"]["nodes"]
        key_to_code = {k: (k if nd["type"] == "EXIT" else D + RENAME.get(nd.get("code", k), nd.get("code", k)))
                       for k, nd in nodes.items()}
        for k, nd in nodes.items():
            code = key_to_code[k]
            if nd["type"] == "EXIT":
                kind = "EXIT_SUCCESS" if nd.get("status") == "SUCCESS" or k == "EXIT_JUDGED" else "EXIT"
                routing = "—"
            else:
                kind = nd["type"]
                routing = "; ".join(f"{s} -> {key_to_code.get(t, t)}" for s, t in nd["next"].items())
            out.append(row(D + wf_code(p, n, v), code, "", kind, routing, f"S6 pps_artifacts_requiring_action #{i}"))
    return out


def cc_composition():
    out = []
    for i, (old, new) in enumerate(CC, start=4):
        cc = machine(find(old))
        for n_step, s in enumerate(cc["core"]["pipeline"], start=1):
            cap = s.get("transform") or s.get("side_effect")
            bare = cap.split("::")[1]
            cap = cap.split("::")[0] + "::" + RENAME.get(bare, bare)
            kind = "CT" if s.get("transform") else "CS"
            inputs = list((s.get("inputs") or {}).keys())
            if s["step"] == "evaluate_rules":
                inputs.append("rule_set_id")
                produces = "verdict, findings, rules_evaluated, rule_set, approval_standing"
            elif s["step"].startswith("parse_registers"):
                produces = "header, sections, registers"
            elif s["step"] == "parse_priors":
                produces = "priors"
            else:
                produces = "observation"
            op = (s.get("op") or "QUERY") if kind == "CS" else machine(find(RENAME.get(bare, bare) if False else bare))["machine"]["operation"]
            routing = "; ".join(f"{k} -> {t}" for k, t in s["on_result"].items())
            iface = "" if kind == "CS" else ("in: " + ", ".join(f"{x}={x}" for x in inputs) + "; out: " + ", ".join(f"{x}={x}" for x in produces.split(", ")))
            out.append(row(D + new, n_step, s["step"], cap, kind, op, "—", ", ".join(inputs), produces, routing, "—", "SUCCESS", iface))
    return out


def step_bindings():
    out = []
    for i, (p, n, o, v, *_ ) in enumerate(WF, start=7):
        wf = machine(find(wf_code(p, n, o)))
        for k, nd in wf["core"]["nodes"].items():
            if nd["type"] != "CC":
                continue
            node = D + RENAME[nd["code"]]
            for field, value in nd["inputs"].items():
                if field == "rule_set":
                    bound = "generated"
                elif isinstance(value, str) and value.startswith("$.payload."):
                    bound = "payload." + value[len("$.payload."):]
                else:
                    bound = flow(value)
                out.append(row(D + wf_code(p, n, v), node, "INPUT", field, bound, f"S6 pps_artifacts_requiring_action #{i}"))
            out.append(row(D + wf_code(p, n, v), node, "INPUT", "rule_set_id", json.dumps(SCHEMA[p]), "S7 design_resolution #3"))
    for i, (old, new) in enumerate(CC, start=4):
        for s in machine(find(old))["core"]["pipeline"]:
            if s.get("side_effect"):
                for field, value in (s.get("inputs") or {}).items():
                    out.append(row(D + new, s["step"], "INPUT", field, json.dumps(value) if isinstance(value, str) else flow(value),
                                   f"S6 pps_artifacts_requiring_action #{i}"))
        for field in ("verdict", "findings", "rules_evaluated", "rule_set", "approval_standing"):
            out.append(row(D + new, "evaluate_rules", "OUTPUT", field, f"capability_result.{field}", f"S6 pps_artifacts_requiring_action #{i}"))
    return out


def refusal_governance_discharge():
    return [row("Judging a document", "The document is in the old form, after this change", p.lower(), "REGISTER_MISSING", "S0 operation_refusals #1")
            for p, *_ in WF]


def interface_fields():
    out = []
    for old, new in CT + CC:
        core = machine(find(old))["core"]
        for direction, fields in (("INPUT", core.get("inputs") or {}), ("OUTPUT", core.get("outputs") or {})):
            for f, spec in fields.items():
                req = "YES" if spec.get("required", direction == "OUTPUT") else "NO"
                out.append(row(D + new, direction, f, spec.get("type", "object"), req, "", (spec.get("description") or f).split("\n")[0].strip()))
        if new == "CT_PURE_EVALUATE_RULES_V1" or new.startswith("CC_"):
            out.append(row(D + new, "INPUT", "rule_set_id", "string", "YES", "", "The identity of the rule set supplied, as its phase's register schema declares it"))
            out.append(row(D + new, "OUTPUT", "rule_set", "string", "YES", "", "The identity of the rule set that rendered the verdict"))
            out.append(row(D + new, "OUTPUT", "approval_standing", "string", "NO", "", "Whether the document's approval holds under that rule set: confirmed or unconfirmed; absent when the document names no approval"))
    return out


def implementation_bindings():
    out = []
    for old, new in CT:
        m = machine(find(old))
        refusal = m["core"].get("refusal", "never")
        module = m["machine"]["implementation"]["module"].replace("_v0", "_v1")
        out.append(row(D + new, module, "execute", m["machine"]["operation"], "atom", "ct_pure", refusal, f"S7 new_artifacts {new}"))
    return out


def vocabulary_extensions():
    return [row(D + code, "NONE", group, "lower_snake", value, meaning, f"S7 new_artifacts {code}")
            for code, group, _, _, _, values in VOCAB for value, meaning in values]


def artifact_properties():
    out = []
    for old, new in CT + CC:
        out.append(row(D + new, "supersedes", D + old, f"S7 existing_inventory {old}"))
    for p, n, o, v, *_ in WF:
        out.append(row(D + wf_code(p, n, v), "supersedes", D + wf_code(p, n, o), f"S7 existing_inventory {wf_code(p, n, o)}"))
    for code, *_ in VOCAB:
        out.append(row(D + code, "governed_by", "vocabulary::CONSTITUTION_VOCABULARY_V0", f"S7 new_artifacts {code}"))
    return out


DOC = "# Stage 1\n\n```yaml\nheader: {CR: rule_effectivity, rule_set: transformation.schemas.SCHEMA_REGISTERS_P1_CHANGE_REQUEST_V0}\nregisters:\n  known_facts:\n  - {Fact: An approval names its rule set., Certainty: HIGH}\n```\n"
PARSED = {"header": {"CR": "rule_effectivity", "rule_set": SCHEMA["P1"]}, "sections": [],
          "registers": [{"id": "known_facts", "columns": ["Fact", "Certainty"],
                         "rows": [{"Fact": "An approval names its rule set.", "Certainty": "HIGH"}], "text": ""}]}
RS = SCHEMA["P3"]


def tests():
    cases = [
        ("CT_PURE_PARSE_REGISTERS_V1", "reads_header_and_registers_from_the_machine_block", "SUCCESS",
         [("INPUT", "document_text", json.dumps(DOC))] + [("EXPECTED", k, flow(v)) for k, v in PARSED.items()]),
        ("CT_PURE_PARSE_PRIOR_PHASES_V1", "reads_each_prior_from_its_machine_block", "SUCCESS",
         [("INPUT", "prior_texts", flow({"p1": DOC})), ("EXPECTED", "priors", flow({"p1": PARSED}))]),
        ("CT_PURE_EVALUATE_RULES_V1", "reports_an_approval_under_the_judging_rule_set_confirmed", "SUCCESS",
         [("INPUT", "header", flow({"rule_set": RS, "approved_under": RS})), ("INPUT", "sections", "[]"), ("INPUT", "registers", "[]"),
          ("INPUT", "document_text", '""'), ("INPUT", "rule_set", "[]"), ("INPUT", "rule_set_id", RS), ("INPUT", "observed", "{}"), ("INPUT", "priors", "{}"),
          ("EXPECTED", "verdict", "ADMISSIBLE"), ("EXPECTED", "findings", "[]"), ("EXPECTED", "rules_evaluated", "0"),
          ("EXPECTED", "rule_set", RS), ("EXPECTED", "approval_standing", "confirmed")]),
        ("CT_PURE_EVALUATE_RULES_V1", "reports_an_approval_under_another_rule_set_unconfirmed", "SUCCESS",
         [("INPUT", "header", flow({"rule_set": RS, "approved_under": RS.replace("_V0", "_V1")})), ("INPUT", "sections", "[]"), ("INPUT", "registers", "[]"),
          ("INPUT", "document_text", '""'), ("INPUT", "rule_set", "[]"), ("INPUT", "rule_set_id", RS), ("INPUT", "observed", "{}"), ("INPUT", "priors", "{}"),
          ("EXPECTED", "verdict", "ADMISSIBLE"), ("EXPECTED", "findings", "[]"), ("EXPECTED", "rules_evaluated", "0"),
          ("EXPECTED", "rule_set", RS), ("EXPECTED", "approval_standing", "unconfirmed")]),
    ]
    tc = [row(D + c, case, outcome, "human decision") for c, case, outcome, _ in cases]
    tv = [row(D + c, case, role, field, value, "human decision") for c, case, _, values in cases for role, field, value in values]
    return tc, tv


def artifact_summary():
    replaced = [D + o for o, _ in CT + CC] + [D + wf_code(p, n, o) for p, n, o, *_ in WF]
    new = [D + n for _, n in CT + CC] + [D + wf_code(p, n, v) for p, n, o, v, *_ in WF] + [D + c for c, *_ in VOCAB]
    return [row("REPLACE", "design", len(replaced), ", ".join(replaced)),
            row("EXTEND", "design", 0, ""),
            row("NEW", "design", len(new), ", ".join(new))]


def generation_provenance():
    out = []
    # The two observing contracts carry steps and an observation map the generator writes, as their
    # predecessors did; the generator, not construction, produces them.
    rule_modules = ["transformation/design/meta.py"] + [f"transformation/design/{mod}/rules.py" for *_, mod, _, _ in WF]
    for _, new in CC[1:]:
        out.append(row(D + new, "transformation.design.emit:emit_rule_sets", ", ".join(rule_modules), "S7 design_resolution #3"))
    for p, n, o, v, mod, tmpl, _ in WF:
        cc = "CC_JUDGE_DOCUMENT_V1" if p in ("P0", "P1") else ("CC_JUDGE_AGAINST_COMPOSITION_V2" if p == "P3" else "CC_JUDGE_AGAINST_SNAPSHOT_V2")
        sources = [f"templates/{tmpl}.md", f"transformation/design/{mod}/rules.py",
                   f"registry/design/capability_contracts/{cc}.md", f"registry/schema/SCHEMA_REGISTERS_{p}_{n}_V0.json"]
        out.append(row(D + wf_code(p, n, v), "transformation.design.emit:emit_rule_sets", ", ".join(sources), "S7 design_resolution #3"))
    return out


# --- document --------------------------------------------------------------------------------

def table(register: str, header: list[str], rows: list[str], flags: str = "") -> str:
    marker = f"<!-- register:{register}{(' ' + flags) if flags else ''} -->"
    sep = "|" + "|".join("-" * (len(h) + 2) for h in header) + "|"
    body = [] if rows is None else (rows or ["| NONE IDENTIFIED |"])
    return "\n".join([marker, "| " + " | ".join(header) + " |", sep, *body])


def main() -> None:
    tc, tv = tests()
    sections = [
        ("1. Design Decisions Resolution", table("design_resolution", ["Decision", "Business Fact", "Resolution", "Source Finding"], design_resolution(), "optional")),
        ("2. Artifact Inventory — Existing Artifacts", table("existing_inventory", ["FQDN", "Action (REPLACE, REUSE, EXTEND, REPOINT, REVIEW)", "Summary", "Reason", "Source Finding"], existing_inventory())),
        ("3. Artifact Family Mapping — New Artifacts", table("new_artifacts", ["Capability", "Family (AC, IN, WF, RB, CC, CT, EV, VOCAB, STRUCTURE, TI, TE)", "Code", "Summary", "Owner Subdomain", "Status", "Source Finding"], new_artifacts(), "optional business_language=capability")),
        ("4. Runtime Binding (RB) Declarations", table("rb_declarations", ["RB Code", "Binds WF", "CS Bindings", "Storage Structure", "Source Finding"], rb_declarations())),
        ("5. Execution Topology", table("execution_topology", ["Workflow", "Node", "Runs", "Node Type (IN, CC, EXIT, EXIT_SUCCESS)", "Routing", "Source Finding"], execution_topology(), "optional_columns=runs")),
        ("6. Capability Composition", table("cc_composition", ["CC Code", "Step", "Step Name", "Capability", "Kind (CT, CS)", "Operation", "Store", "Consumes", "Produces", "Routing", "Interpreted By", "Semantic Status", "Interface"], cc_composition(), "optional")),
        ("7. Step Bindings", table("step_bindings", ["Owner", "Step", "Direction (INPUT, OUTPUT)", "Field", "Bound To", "Source Finding"], step_bindings(), "optional")),
        ("8. Interface Fields", table("interface_fields", ["Artifact", "Direction (INPUT, OUTPUT, ATTRIBUTE)", "Field", "Type", "Required (YES, NO)", "Default", "Meaning"], interface_fields(), "optional")),
        ("9. Implementation Bindings", table("implementation_bindings", ["CT Code", "Module", "Callable", "Operation", "Kind (atom, molecule)", "Purity (ct_pure, ct_impure)", "Refusal (raises, returns, never)", "Source Finding"], implementation_bindings(), "optional")),
        ("10. Vocabulary Extensions", table("vocabulary_extensions", ["Vocabulary Code", "Extends", "Group", "Casing", "Value", "Meaning", "Source Finding"], vocabulary_extensions(), "optional")),
        ("11. Runtime Policies", table("runtime_policies", ["RB Code", "Capability", "Key", "Value", "Source Finding"], [], "optional")),
        ("12. Artifact Properties", table("artifact_properties", ["Artifact", "Property", "Value", "Source Finding"], artifact_properties(), "optional")),
        ("13. STRUCTURE Stores", table("structure_stores", ["Store Name", "Storage Type (CS_APPENDONLY_JSONL_V0, CS_MUTABLE_JSON_V0, CS_REGISTRY_V0)", "Proposed Path", "Used By", "Source Finding"], [], "optional")),
        ("14. Transport Bindings", table("transport_bindings", ["Artifact", "Direction (INGRESS, EGRESS)", "Operation", "Handler Kind (WF_INVOCATION, SNAPSHOT_READ)", "Handler Target", "Field", "Bound To", "Source Finding"], [], "optional")),
        ("15. Artifact Summary", table("artifact_summary", ["Action (REPLACE, EXTEND, NEW)", "Subdomain", "Count", "Artifacts"], artifact_summary())),
        ("16. Generation Provenance", table("generation_provenance", ["Artifact", "Generator", "Generator Sources", "Source Finding"], generation_provenance(), "optional")),
        ("17. Declared Reach", table("declared_reach", ["Act", "Consults", "Source Finding"], [], "optional")),
        ("18. Refusal Discharge", table("refusal_discharge", ["Operation", "Refused When", "Act", "Step", "Outcome", "Source Finding"], [], "optional")),
        ("19. Refusal Deferrals", table("refusal_deferrals", ["Operation", "Refused When", "Deferred To", "Until", "Source Finding"], [], "optional")),
        ("20. Refusal — Governance-Surface Discharge", table("refusal_governance_discharge", ["Operation", "Refused When", "Phase", "Governing Rule", "Source Finding"], refusal_governance_discharge(), "optional")),
        ("21. Molecule Steps", table("molecule_steps", ["CT Code", "Step", "Kind (atom, molecule, loop)", "Target", "Over", "Iterator", "Emits", "Source Finding"], [], "optional")),
        ("22. Molecule Step Bindings", table("molecule_step_bindings", ["CT Code", "Step", "Role (INPUT, CARRY, UPDATE)", "Field", "Bound To", "Source Finding"], [], "optional")),
        ("23. Test Cases", table("test_cases", ["CT Code", "Case", "Expected Outcome (SUCCESS, VIOLATION)", "Source Finding"], tc, "optional")),
        ("24. Test Case Values", table("test_case_values", ["CT Code", "Case", "Role (INPUT, EXPECTED, ASSERT, RECORDED)", "Field", "Value", "Source Finding"], tv, "optional")),
        ("25. Withdrawn Facts", table("withdrawn_facts", ["Artifact", "Fact", "Reason", "Source Finding"], None, "optional")),
    ]
    head = """# Stage 7 — Design Intent: transformation / design
**Stage:** 7 — Design Intent
**CR:** rule_effectivity
**Status:** DRAFT
**Feeds:** Stage 8 — Authoring Mandate

HOW: the binding identities and the declarations they carry. Every artifact this change acts on
changes meaning, so each is replaced by a new version, redeclared whole.
"""
    body = "\n\n---\n\n".join(f"## {t}\n\n{tbl}" for t, tbl in sections)
    tail = """

---

## Gate 1 — Design Approval

**Gate 1 closes here.** The full dossier (Stages 0–7) is presented for review as a body.

---

## Pipeline Provenance

| Stage | Output | Status |
|-------|--------|--------|
| Stage 6 — Governance Intent | Ownership, artifacts requiring action, boundary rules | COMPLETE |
| Stage 7 — Design Intent | This document | PENDING GATE 1 APPROVAL |
"""
    OUT.write_text(head + "\n---\n\n" + body + tail, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

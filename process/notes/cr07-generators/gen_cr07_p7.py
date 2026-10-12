"""cr_07_own_values P7: the design intent, carried from the designs of record and changed where cr_07 says.

The four acts were last designed by cr_06_routing_closure, whose P7 construction reproduced fact for
fact. Their rows are carried from it under their next versions, and only the bindings cr_07 decides
are changed. The three entrances and the wallet entry point are read back from the registry, as
construction would write them, less what cr_07 removes. A generator is not a design authority (v5
ruling C1): the rules judge every row it writes, and construction completeness must reach 100%.

    python gen_cr07_p7.py CR06_P7.md REGISTRY OUT.md
"""
from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

import yaml

MACHINE = re.compile(r"^```yaml\n(.*?)^```$", re.S | re.M)
FULL = re.compile(r"\bblockchain::[A-Z][A-Z0-9_]*_V\d+\b")
NS = "blockchain::"

ACTS = {"WF_REGISTER_ACTOR_V1": "WF_REGISTER_ACTOR_V2", "WF_ACCEPT_ACTOR_V1": "WF_ACCEPT_ACTOR_V2",
        "WF_REJECT_ACTOR_V1": "WF_REJECT_ACTOR_V2", "WF_CREATE_WALLET_V1": "WF_CREATE_WALLET_V2"}
ENTRANCES = {"TI_REGISTER_ACTOR_V0": "TI_REGISTER_ACTOR_V1", "TI_ACCEPT_ACTOR_V0": "TI_ACCEPT_ACTOR_V1",
             "TI_REJECT_ACTOR_V0": "TI_REJECT_ACTOR_V1"}
ENTRY = {"IN_WALLET_CREATION_V0": "IN_WALLET_CREATION_V1"}
REPLACED = {**ACTS, **ENTRANCES, **ENTRY}
REPOINTED = ["IN_ACTOR_REGISTERED_V0", "IN_ACTOR_ACCEPTANCE_V0", "IN_ACTOR_REJECTION_V0"]
REMOVED_FROM_ENTRANCES = {"address_path", "address_type", "stream_id", "occurrence_fields"}
REMOVED_FROM_ENTRY = {"wallet_id_prefix"}

HOLDER = "$.results.CC_RESOLVE_ACTOR_V0.value.contact_address"
# What each act now states, by (act, place, field). Every other binding is carried as it was.
STATED = {
    ("WF_REGISTER_ACTOR_V2", "CC_CLAIM_CONTACT_ADDRESS_V0", "address_path"): {"literal": "contact_address"},
    ("WF_REGISTER_ACTOR_V2", "CC_CLAIM_CONTACT_ADDRESS_V0", "address_type"): {"literal": "string"},
    ("WF_REGISTER_ACTOR_V2", "CC_APPEND_ACTOR_OCCURRENCE_V0", "occurrence_fields"):
        {"literal": {"occurrence": "ACTOR_REGISTERED_UNVERIFIED"}},
    ("WF_REGISTER_ACTOR_V2", "CC_APPEND_ACTOR_OCCURRENCE_V0", "stream_id"): {"literal": "ACTOR_OCCURRENCES"},
    ("WF_ACCEPT_ACTOR_V2", "CC_APPEND_ACTOR_OCCURRENCE_V0", "occurrence_fields"):
        {"literal": {"occurrence": "ACTOR_ACCEPTED", "verifying_authority": "$.payload.verifying_authority",
                     "grounds": "$.payload.grounds"}},
    ("WF_ACCEPT_ACTOR_V2", "CC_APPEND_ACTOR_OCCURRENCE_V0", "stream_id"): {"literal": "ACTOR_OCCURRENCES"},
    ("WF_REJECT_ACTOR_V2", "CC_APPEND_ACTOR_OCCURRENCE_V0", "occurrence_fields"):
        {"literal": {"occurrence": "ACTOR_REJECTED", "verifying_authority": "$.payload.verifying_authority",
                     "grounds": "$.payload.grounds"}},
    ("WF_REJECT_ACTOR_V2", "CC_APPEND_ACTOR_OCCURRENCE_V0", "stream_id"): {"literal": "ACTOR_OCCURRENCES"},
    ("WF_CREATE_WALLET_V2", "CC_DETERMINE_WALLET_IDENTITY_V0", "wallet_id_prefix"): {"literal": "wal"},
    ("WF_CREATE_WALLET_V2", "CC_CREATE_WALLET_RECORD_V0", "wallet_fields"):
        {"literal": {"holder": HOLDER, "balance": 0, "denomination": "BACHI", "classification": "DEFAULT",
                     "state": "ACTIVE"}},
    ("WF_CREATE_WALLET_V2", "CC_APPEND_WALLET_OCCURRENCE_V0", "occurrence_fields"):
        {"literal": {"occurrence": "WALLET_CREATED", "holder": HOLDER}},
}
# Which design decision (P4) and which governed capability (P6) each change answers.
DECISION_OF = {"WF_REGISTER_ACTOR_V2": 1, "WF_ACCEPT_ACTOR_V2": 1, "WF_REJECT_ACTOR_V2": 1,
               "WF_CREATE_WALLET_V2": 2}
CAPABILITY = {
    "WF_REGISTER_ACTOR_V2": ("Register a person", "State the moment and the trail of each identity act"),
    "WF_ACCEPT_ACTOR_V2": ("Accept a person", "State the moment and the trail of each identity act"),
    "WF_REJECT_ACTOR_V2": ("Reject a person", "State the moment and the trail of each identity act"),
    "WF_CREATE_WALLET_V2": ("Create a wallet", "State a new wallet's record, prefix and moment"),
    "TI_REGISTER_ACTOR_V1": ("Offer registering an actor to a caller outside the business",
                             "Stop the entrances sending what the acts state"),
    "TI_ACCEPT_ACTOR_V1": ("Offer accepting an actor to a caller outside the business",
                           "Stop the entrances sending what the acts state"),
    "TI_REJECT_ACTOR_V1": ("Offer rejecting an actor to a caller outside the business",
                           "Stop the entrances sending what the acts state"),
    "IN_WALLET_CREATION_V1": ("Admit a request for a wallet", "State a new wallet's record, prefix and moment"),
}
SUMMARY = {
    "WF_REGISTER_ACTOR_V2": "The governed sequence that admits a person as an unverified actor, records that moment as its own, and announces it",
    "WF_ACCEPT_ACTOR_V2": "The governed sequence that records an acceptance, records that moment as its own, and announces it",
    "WF_REJECT_ACTOR_V2": "The governed sequence that records a rejection, with grounds required, records that moment as its own, and announces it",
    "WF_CREATE_WALLET_V2": "The governed sequence that gives an accepted person a wallet holding nothing, and records that it did",
    "TI_REGISTER_ACTOR_V1": "Admits a request to register an actor, and sends the act only what the caller supplies and the person's preferences",
    "TI_ACCEPT_ACTOR_V1": "Admits a request to accept a registered actor, and sends the act only what the caller supplies",
    "TI_REJECT_ACTOR_V1": "Admits a request to reject a registered actor, and sends the act only what the caller supplies",
    "IN_WALLET_CREATION_V1": "Admits a request naming the person a wallet is for and the key it is made from, and refuses one that names nobody",
}
SUBDOMAIN = {c: ("wallet" if "WALLET" in c else "identity") for c in SUMMARY}
P6_ROW = {"WF_REGISTER_ACTOR_V1": 1, "WF_ACCEPT_ACTOR_V1": 2, "WF_REJECT_ACTOR_V1": 3,
          "WF_CREATE_WALLET_V1": 4, "TI_REGISTER_ACTOR_V0": 5, "TI_ACCEPT_ACTOR_V0": 6,
          "TI_REJECT_ACTOR_V0": 7, "IN_WALLET_CREATION_V0": 8, "IN_ACTOR_REGISTERED_V0": 9,
          "IN_ACTOR_ACCEPTANCE_V0": 10, "IN_ACTOR_REJECTION_V0": 11}


class Plain(yaml.SafeDumper):
    """Writes every row out in full: a reader of the design never resolves an anchor."""

    def ignore_aliases(self, data):
        return True


def machine(path: Path) -> dict:
    return yaml.safe_load(MACHINE.search(path.read_text(encoding="utf-8")).group(1))


def bare(fqdn: str) -> str:
    return fqdn.split("::")[-1]


def rename(value):
    """Every name of a replaced act, carried under its next version."""
    if isinstance(value, str):
        for old, new in {**ACTS, **ENTRY}.items():
            value = re.sub(rf"\b{old}\b", new, value)
        return value
    if isinstance(value, dict):
        return {k: rename(v) for k, v in value.items()}
    if isinstance(value, list):
        return [rename(v) for v in value]
    return value


def pps(code: str) -> dict:
    return {"phase": "p6", "register": "pps_artifacts_requiring_action", "row": P6_ROW[code]}


def flatten(template: dict, prefix: str = "") -> list[tuple[str, object]]:
    """A payload template as the design states it: one row per leaf, at its dotted field."""
    out = []
    for key, value in template.items():
        field = f"{prefix}{key}"
        if isinstance(value, dict):
            out.extend(flatten(value, field + "."))
        else:
            out.append((field, value))
    return out


def registry_artifact(registry: Path, code: str) -> dict:
    hits = [p for p in registry.rglob(f"{code}.md")]
    assert len(hits) == 1, (code, hits)
    return machine(hits[0])


def main(cr06_path: str, registry_path: str, out_path: str) -> None:
    registry = Path(registry_path)
    cr06 = machine(Path(cr06_path))["registers"]
    acts = {NS + a for a in ACTS}

    topology = [rename(r) for r in cr06["execution_topology"] if r["workflow"] in acts]
    bindings = []
    for r in cr06["step_bindings"]:
        if r["owner"] not in acts:
            continue
        r = rename(copy.deepcopy(r))
        key = (bare(r["owner"]), bare(r["step"]), r["field"])
        if key in STATED:
            r["bound_to"] = STATED[key]
            r["source_finding"] = {"phase": "p4", "register": "design_decisions",
                                   "row": DECISION_OF[key[0]]}
        bindings.append(r)
    stated = {(bare(r["owner"]), bare(r["step"]), r["field"]) for r in bindings}
    assert set(STATED) <= stated, set(STATED) - stated

    properties = []
    for r in cr06["artifact_properties"]:
        if r["artifact"] not in acts:
            continue
        r = copy.deepcopy(r)
        if r["property"] == "supersedes":
            r["value"] = [r["artifact"]]
            r["artifact"] = rename(r["artifact"])
            r["source_finding"] = {"phase": "p4", "register": "design_decisions", "row": 5}
        else:
            r = rename(r)
        properties.append(r)
    for old, new in {**ENTRANCES, **ENTRY}.items():
        properties.append({"artifact": NS + new, "property": "supersedes", "value": [NS + old],
                           "source_finding": {"phase": "p4", "register": "design_decisions", "row": 5}})

    rb_rows = [rename(r) for r in cr06["rb_declarations"] if r["binds_wf"] in acts]
    reach = [rename(r) for r in (cr06.get("declared_reach") or []) if r["act"] in acts]

    interface, transport = [], []
    for old, new in ENTRANCES.items():
        ti = registry_artifact(registry, old)
        for field, spec in ti["input_contract"].items():
            interface.append({"artifact": NS + new, "direction": "INPUT", "field": field,
                              "type": spec["type"], "required": "YES" if spec.get("required") else "NO",
                              "default": "", "meaning": field.replace("_", " ").capitalize() + " the caller sends."})
        for field, value in flatten(ti["handler"]["payload_template"]):
            if field.split(".")[0] in REMOVED_FROM_ENTRANCES:
                continue
            caller = isinstance(value, str) and value.startswith("${input.")
            transport.append({"artifact": NS + new, "direction": "INGRESS", "operation": ti["operation"],
                              "handler_kind": ti["handler"]["kind"],
                              "handler_target": rename(ti["handler"]["workflow"]), "field": field,
                              "bound_to": value if caller else {"literal": value},
                              "source_finding": pps(old)})
    for old, new in ENTRY.items():
        entry = registry_artifact(registry, old)
        for field, spec in entry["core"]["inputs"].items():
            if field in REMOVED_FROM_ENTRY:
                continue
            interface.append({"artifact": NS + new, "direction": "INPUT", "field": field,
                              "type": spec["type"], "required": "YES" if spec.get("required") else "NO",
                              "default": "", "meaning": {
                                  "contact_address": "The person the wallet is for.",
                                  "key_material": "The key material the address is worked out from."}[field]})

    new = [{"capability": CAPABILITY[c][0], "family": c.split("_")[0], "code": NS + c,
            "summary": SUMMARY[c], "owner_subdomain": SUBDOMAIN[c], "status": "NEW",
            "source_finding": {"phase": "p6", "register": "governance_outcome",
                               "key": CAPABILITY[c][1]}} for c in REPLACED.values()]

    # The actor each act runs for is read from the inventory, so it is named there.
    actors = [registry_artifact(registry, act)["core"]["actor_context"] for act in ACTS]
    named = sorted(set(FULL.findall(yaml.safe_dump([topology, bindings, properties, rb_rows, reach,
                                                     transport, actors]))))
    new_codes = {NS + c for c in REPLACED.values()}
    inventory = []
    for old in REPLACED:
        inventory.append({"fqdn": NS + old, "action": "REPLACE",
                          "summary": registry_artifact(registry, old)["core"]["summary"],
                          "reason": "Takes from the request what only the business may decide. Retired by record for its next version.",
                          "source_finding": pps(old)})
    for code in REPOINTED:
        inventory.append({"fqdn": NS + code, "action": "REPOINT",
                          "summary": registry_artifact(registry, code)["core"]["summary"],
                          "reason": "Names the act this change replaces; it names the act's next version, and nothing else in it changes.",
                          "source_finding": pps(code)})
    accounted = new_codes | {r["fqdn"] for r in inventory}
    for fqdn in named:
        if fqdn in accounted:
            continue
        inventory.append({"fqdn": fqdn, "action": "REUSE",
                          "summary": " ".join(registry_artifact(registry, bare(fqdn))["core"]["summary"].split()),
                          "reason": "Reused as it stands; the act decides what it is handed.",
                          "source_finding": {"phase": "p4", "register": "dependency_graph", "key": fqdn}
                          if fqdn in DEPENDENCIES else {"phase": "p2", "register": "pps_baseline_fqdns", "key": fqdn}})
        accounted.add(fqdn)

    summary = []
    for action, codes in (("NEW", list(REPLACED.values())), ("REPLACE", list(REPLACED))):
        for sub in ("identity", "wallet"):
            members = [NS + c for c in codes if ("WALLET" in c) == (sub == "wallet")]
            summary.append({"action": action, "subdomain": sub, "count": str(len(members)),
                            "artifacts": ", ".join(members)})

    registers = {
        "design_resolution": DESIGN_RESOLUTION,
        "existing_inventory": inventory,
        "new_artifacts": new,
        "rb_declarations": rb_rows,
        "execution_topology": topology,
        "cc_composition": [],
        "step_bindings": bindings,
        "interface_fields": interface,
        "artifact_properties": properties,
        "structure_stores": [],
        "artifact_summary": summary,
        "declared_reach": reach,
        "implementation_bindings": None,
        "vocabulary_extensions": None,
        "runtime_policies": None,
        "transport_bindings": transport,
        "generation_provenance": None,
        "refusal_discharge": [],
        "refusal_deferrals": None,
        "refusal_governance_discharge": None,
        "molecule_steps": None,
        "molecule_step_bindings": None,
        "test_cases": None,
        "test_case_values": None,
        "withdrawn_facts": None,
    }
    header = {"phase": "p7", "domain": "blockchain", "subdomain": ["identity", "wallet"],
              "cr": "cr_07_own_values", "rule_set": "transformation.schemas.REGISTER_SCHEMA_P7_V0"}
    block = yaml.dump({"document": header, "registers": registers}, Dumper=Plain, sort_keys=False,
                      allow_unicode=True, width=100)
    Path(out_path).write_text(TITLE + "\n\n## Machine\n\n```yaml\n" + block + "```\n" + PROSE,
                              encoding="utf-8")


DEPENDENCIES = {NS + c for c in ("CC_APPEND_ACTOR_OCCURRENCE_V0", "CC_CLAIM_CONTACT_ADDRESS_V0",
                                 "CC_DETERMINE_WALLET_IDENTITY_V0", "CC_CREATE_WALLET_RECORD_V1",
                                 "CC_APPEND_WALLET_OCCURRENCE_V1")}

DESIGN_RESOLUTION = [
    {"decision": "Each act states, in its bindings, every value only the business may decide",
     "business_fact": "A value only the business may decide is never taken from a request",
     "resolution": "blockchain::WF_REGISTER_ACTOR_V2, blockchain::WF_ACCEPT_ACTOR_V2 and "
                   "blockchain::WF_REJECT_ACTOR_V2 state their moment and ACTOR_OCCURRENCES; "
                   "registration states contact_address as a string; blockchain::WF_CREATE_WALLET_V2 "
                   "states the prefix wal, the wallet's record and WALLET_CREATED",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 1}},
    {"decision": "The wallet's holder is read from the person the act resolved",
     "business_fact": "A wallet's holder is the person identity accepted",
     "resolution": "The wallet's record and its moment take the holder from what "
                   "blockchain::CC_RESOLVE_ACTOR_V1 resolved, as the wallet's identity already does",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 2}},
    {"decision": "The wallet entry point stops declaring the prefix",
     "business_fact": "The prefix of a wallet's identity is the business's",
     "resolution": "blockchain::IN_WALLET_CREATION_V1 declares the contact address and the key material only",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 3}},
    {"decision": "Each identity entrance keeps its input contract and stops sending what its act states",
     "business_fact": "Callers send the same inputs through each entrance as before",
     "resolution": "blockchain::TI_REGISTER_ACTOR_V1, blockchain::TI_ACCEPT_ACTOR_V1 and "
                   "blockchain::TI_REJECT_ACTOR_V1 send no moment, trail or address place",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 4}},
    {"decision": "Each act, entrance and entry point whose meaning changes is stated under its next version",
     "business_fact": "A change of meaning is a new identity",
     "resolution": "The eight successors each supersede their predecessor, which is retired by record",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 5}},
    {"decision": "The identity entry points are re-pointed",
     "business_fact": "Every caller starts the same act as today",
     "resolution": "blockchain::IN_ACTOR_REGISTERED_V0, blockchain::IN_ACTOR_ACCEPTANCE_V0 and "
                   "blockchain::IN_ACTOR_REJECTION_V0 name the next version of the act they start",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 6}},
    {"decision": "Records made before this change are left as they are",
     "business_fact": "The record is added to and never rewritten",
     "resolution": "No backfill or repair step is designed",
     "source_finding": {"phase": "p4", "register": "design_decisions", "row": 7}},
]

TITLE = "# Stage 7 — Design Intent: blockchain / identity and wallet"
PROSE = """
The four acts are carried from cr_06_routing_closure's design under their next versions, and each
binding that took a value only the business may decide now states it. The three entrances and the
wallet entry point are restated as they stand, less what this change removes. Every row was written by
`.github/process/notes/cr07-generators/gen_cr07_p7.py`.

---

## 1. Design Resolution

## 2. Existing Inventory

## 3. New Artifacts

## 4. Execution Topology

## 5. Step Bindings

## 6. Interface Fields

## 7. Artifact Properties

## 8. Transport Bindings

## 9. Artifact Summary
"""

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

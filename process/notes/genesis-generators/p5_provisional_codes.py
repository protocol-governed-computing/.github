"""Genesis P5 `provisional_codes`: one row per live artifact, cited to the P4 capability it serves.

    python p5_provisional_codes.py > rows.yaml
"""
from __future__ import annotations

import sys

import yaml

import live_inventory

ACTORS = {"AC_SEED_AUTHOR_V0": "Problem statement author", "AC_REGISTER_AUTHOR_V0": "Author of record",
          "AC_GATE_REVIEWER_V0": "Reviewer"}
PHASES = "The nine phases, each with its rules and its entry point"
BUILD = "Build an approved mandate"
CAPABILITY = {
    "CT_PURE_PARSE_REGISTERS": "Read a phase document into its registers",
    "CT_PURE_PARSE_PRIOR_PHASES": "Read the earlier phase documents a phase must agree with",
    "CT_PURE_EVALUATE_RULES": "Apply every rule of a phase and report each failure",
    "CC_JUDGE_": "Judge a phase document, with and without the composition and earlier documents",
    "CT_PURE_RENDER": "Render, measure and attribute the artifacts a mandate schedules",
    "CT_PURE_MEASURE": "Render, measure and attribute the artifacts a mandate schedules",
    "CT_PURE_ATTRIBUTE": "Render, measure and attribute the artifacts a mandate schedules",
}


def source(artifact: dict) -> dict:
    code = artifact["code"]
    if code in ACTORS:
        return {"phase": "p4", "register": "actors", "key": ACTORS[code]}
    for prefix, capability in CAPABILITY.items():
        if code.startswith(prefix):
            return {"phase": "p4", "register": "capability_graph", "key": capability}
    if code == "STRUCTURE_BUILD_TRANSFORMATION_CONFIG_V1":
        return {"phase": "p4", "register": "design_decisions", "row": 1}
    return {"phase": "p4", "register": "capability_graph",
            "key": BUILD if artifact["subdomain"] == "build" else PHASES}


def summary(artifact: dict) -> str:
    core = artifact["machine"].get("core") or {}
    if core.get("summary"):
        return core["summary"].strip()
    # A vocabulary carries no summary of its own; these state what each one is for.
    return {"VOCAB_DESIGN_REGISTER_TERMS_V0": "The controlled terms the phase registers are written in",
            "VOCAB_FACT_PROVENANCE_V0": "Where a value construction wrote came from"}[artifact["code"]]


rows = [{"subdomain": a["subdomain"], "provisional_code": a["code"], "family": a["family"],
         "summary": summary(a), "source_finding": source(a)} for a in live_inventory.live()]
yaml.safe_dump(rows, sys.stdout, sort_keys=False, allow_unicode=True, width=100)

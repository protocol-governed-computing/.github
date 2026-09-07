"""G4 transformation and runtime for the NPP-E lending-library need."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import npp_e


BASELINE_SNAPSHOT_ID = "snapshot:70dd9deaa723fa3d808d1bcc9d9171244a8e22378a7719961aadde3339dd80cb"
BASELINE_FAMILY_REVISION = npp_e.FAMILY_REVISION
CHECK_KINDS = {"non_empty", "exact", "baseline_artifact_exists", "contains"}


def _refuse(reason: str, proposal: Any, *, rules: list[str]) -> npp_e.Refusal:
    return npp_e.Refusal(cause="rule_refusal", reason=reason, proposal=proposal, subject="transformation", rules=rules)


def sufficient_design() -> dict[str, Any]:
    return {
        "need": {
            "entries": [{
                "address": "need:library-lending",
                "statement": "A copy may be lent to a member and a copy already on loan must not be lent again.",
                "acceptance": "A named copy's current loan status is established from the recorded loan state.",
            }],
            "empty": False,
            "rung": "business",
        },
        "grounding": {
            "entries": [{
                "address": "grounding:baseline",
                "baseline_snapshot_id": BASELINE_SNAPSHOT_ID,
                "artifacts": [
                    "artifact:93386f38c741419fb48f2109a330ae57b399e3f575397616be5159bf6fc4800f",
                    "artifact:caa3ca8237644e5f8e27613d6b2cbb6f24966d6254d0c76be6f434528f00f237",
                ],
            }],
            "empty": False,
            "rung": "bound",
        },
        "design": {
            "entries": [{
                "address": "capability:lending",
                "name": "lend-copy-to-member",
                "inputs": ["copy_id", "member_id"],
                "outputs": ["loan_record"],
                "outcomes": ["completed", "failed"],
                "effect": "record_loan",
                "refusal": "copy_already_on_loan",
            }, {
                "address": "workflow:lending",
                "steps": [{
                    "id": "lend-copy-to-member",
                    "capability": "record_loan",
                    "routes": {"completed": "loan-recorded", "failed": "loan-rejected"},
                }],
                "start": "lend-copy-to-member",
            }, {
                "address": "read:loan-status",
                "class": "read",
                "answer": "current loan record for named copy",
                "refusal": "malformed or absent copy identity",
            }],
            "empty": False,
            "rung": "artifact",
        },
        "schedule": {
            "entries": [
                {"address": "schedule:capability", "target": "capability:lending", "depends_on": []},
                {"address": "schedule:workflow", "target": "workflow:lending", "depends_on": ["capability:lending"]},
                {"address": "schedule:read", "target": "read:loan-status", "depends_on": []},
            ],
            "empty": False,
            "rung": "artifact",
        },
        "rules": [
            {"id": "TR-L1", "register": "need", "check": "non_empty", "field": "statement"},
            {"id": "TR-L2", "register": "grounding", "check": "exact", "field": "baseline_snapshot_id", "value": BASELINE_SNAPSHOT_ID},
            {"id": "TR-L3", "register": "grounding", "check": "baseline_artifact_exists", "field": "artifacts"},
            {"id": "TR-L4", "register": "design", "check": "contains", "field": "inputs", "value": "copy_id"},
            {"id": "TR-L5", "register": "design", "check": "contains", "field": "inputs", "value": "member_id"},
            {"id": "TR-L6", "register": "schedule", "check": "non_empty", "field": "target"},
        ],
    }


def insufficient_design() -> dict[str, Any]:
    design = sufficient_design()
    design["design"]["entries"][0]["inputs"] = ["member_id"]
    return design


def _entry(register: dict[str, Any], address: str) -> dict[str, Any]:
    for entry in register["entries"]:
        if entry["address"] == address:
            return entry
    raise KeyError(address)


def evaluate_design(design: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    if baseline.get("id") != BASELINE_SNAPSHOT_ID or baseline.get("family_revision") != BASELINE_FAMILY_REVISION:
        raise _refuse("baseline_identity_mismatch", baseline, rules=["TR-15"])
    inspection = npp_e.Inspection(baseline)
    results: dict[str, bool] = {}
    findings: list[dict[str, Any]] = []
    for rule in design.get("rules", []):
        rule_id = rule["id"]
        check = rule["check"]
        register_name = rule["register"]
        register = design.get(register_name, {})
        entry = register.get("entries", [{}])[0]
        field = rule["field"]
        location = {"register": register_name, "entry": entry.get("address", "missing"), "field": field}
        if check not in CHECK_KINDS:
            raise _refuse("unknown_check_kind", rule, rules=[rule_id])
        value = entry.get(field)
        if check == "baseline_artifact_exists":
            try:
                passed = all(inspection.get_artifact(expected) for expected in value)
            except npp_e.Refusal:
                passed = False
        else:
            passed = (
            value not in (None, "") if check == "non_empty" else
            value == rule["value"] if check == "exact" else
            rule["value"] in value
            )
        results[rule_id] = passed
        if not passed:
            findings.append({"rule": rule_id, "location": location, "result": False})
    verdict = {"admissible": not findings, "predicate_results": results, "findings": findings}
    if findings:
        raise _refuse("insufficient_design", {"design": design, "verdict": verdict}, rules=[finding["rule"] for finding in findings])
    return verdict


def _realize(design: dict[str, Any]) -> list[dict[str, Any]]:
    capability = _entry(design["design"], "capability:lending")
    workflow = _entry(design["design"], "workflow:lending")
    read = _entry(design["design"], "read:loan-status")
    return [
        npp_e.make_artifact("capability-contract", {key: capability[key] for key in ("inputs", "outputs", "outcomes", "effect")}),
        npp_e.make_artifact("workflow", {key: workflow[key] for key in ("steps", "start")}),
        npp_e.make_artifact("read-operation", {key: read[key] for key in ("class", "answer", "refusal")}),
    ]


def transform(baseline: dict[str, Any], design: dict[str, Any]) -> dict[str, Any]:
    """Ground, determine sufficiency, then realize and seal the next baseline."""
    evaluate_design(design, baseline)
    realized = _realize(deepcopy(design))
    next_snapshot = npp_e.build_snapshot(baseline["artifacts"] + realized, genesis=True)
    if next_snapshot["id"] == baseline["id"]:
        raise _refuse("baseline_did_not_change", design, rules=["TR-1"])
    return next_snapshot


class LibraryRuntime:
    """Small stateful execution surface derived from the realized snapshot."""

    def __init__(self, snapshot: dict[str, Any]) -> None:
        self.inspection = npp_e.Inspection(snapshot)
        self.loans: dict[str, dict[str, str]] = {}
        artifacts = self.inspection.enumerate_artifacts()
        if not any(item["kind"] == "workflow" for item in artifacts):
            raise npp_e.Refusal(cause="rule_refusal", reason="missing_workflow", proposal=snapshot, subject="execution", rules=["EX-1"])
        if not any(item["kind"] == "capability-contract" and item["declaration"]["effect"] == "record_loan" for item in artifacts):
            raise ValueError("snapshot has no lending capability")
        if not any(item["kind"] == "read-operation" and item["declaration"]["answer"] == "current loan record for named copy" for item in artifacts):
            raise ValueError("snapshot has no loan-status read operation")

    def _dispatch(self, capability: dict[str, Any], copy_id: str, member_id: str) -> tuple[str, dict[str, str] | None]:
        if capability["declaration"]["effect"] != "record_loan":
            raise npp_e.Refusal(cause="rule_refusal", reason="unresolved_capability_binding", proposal=capability, subject="execution", rules=["EX-7"])
        if not copy_id or not member_id:
            return "failed", None
        if copy_id in self.loans:
            return "failed", None
        record = {"copy_id": copy_id, "member_id": member_id}
        self.loans[copy_id] = record
        return "completed", deepcopy(record)

    def execute(self, copy_id: str, member_id: str) -> dict[str, Any]:
        artifacts = self.inspection.enumerate_artifacts()
        workflow = next(item for item in artifacts if item["kind"] == "workflow")
        capabilities = {item["declaration"]["effect"]: item for item in artifacts if item["kind"] == "capability-contract"}
        steps = {step["id"]: step for step in workflow["declaration"]["steps"]}
        current = workflow["declaration"]["start"]
        path: list[str] = []
        while current in steps:
            step = steps[current]
            path.append(current)
            capability = capabilities.get(step["capability"])
            if capability is None:
                raise npp_e.Refusal(cause="rule_refusal", reason="unresolved_capability_binding", proposal=step, subject="execution", rules=["EX-7"])
            outcome, output = self._dispatch(capability, copy_id, member_id)
            if outcome not in capability["declaration"]["outcomes"]:
                raise npp_e.Refusal(cause="rule_refusal", reason="undeclared_outcome", proposal={"step": current, "outcome": outcome}, subject="execution", rules=["EX-5"])
            if outcome not in step["routes"]:
                raise npp_e.Refusal(cause="rule_refusal", reason="unrouted_outcome", proposal={"step": current, "outcome": outcome}, subject="execution", rules=["EX-5"])
            current = step["routes"][outcome]
        if current != "loan-recorded" and current != "loan-rejected":
            raise npp_e.Refusal(cause="rule_refusal", reason="unresolved_route_target", proposal={"target": current}, subject="execution", rules=["EX-7"])
        return {"outcome": "completed" if current == "loan-recorded" else "failed", "output": output, "path": path, "terminal": current}

    def lend(self, copy_id: str, member_id: str) -> dict[str, str]:
        result = self.execute(copy_id, member_id)
        if result["outcome"] == "failed":
            reason = "malformed_lend_request" if not copy_id or not member_id else "copy_already_on_loan"
            rule = "LIB-1" if reason == "malformed_lend_request" else "LIB-2"
            raise npp_e.Refusal(cause="rule_refusal", reason=reason, proposal={"copy_id": copy_id, "member_id": member_id}, subject="loan", rules=[rule])
        return result["output"]

    def loan_status(self, copy_id: str) -> dict[str, Any]:
        if not copy_id:
            raise npp_e.Refusal(cause="rule_refusal", reason="malformed_or_absent_copy_identity", proposal={"copy_id": copy_id}, subject="inspection", rules=["LIB-3"])
        record = self.loans.get(copy_id)
        return {"copy_id": copy_id, "on_loan": record is not None, "loan": deepcopy(record)}
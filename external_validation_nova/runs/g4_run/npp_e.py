"""Minimal offline NPP-E realization for vocabulary and declaration claims."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

PROFILE_ID = "NPP-E"
FAMILY_REVISION = "f476ea5c06506a3efba1d773a5d42818c9190601"
ARTIFACT_KINDS = {
    "constitution": {"governance_required": False, "fields": {"purpose", "vocabulary"}},
    "governance-element": {"governance_required": True, "fields": {"category", "governs", "rules"}},
    "workflow": {"governance_required": True, "fields": {"steps", "start"}},
    "capability-contract": {"governance_required": True, "fields": {"inputs", "outputs", "outcomes", "effect"}},
    "read-operation": {"governance_required": True, "fields": {"class", "answer", "refusal"}},
}
ENVELOPE_KEYS = {"id", "kind", "version", "governance", "declaration"}


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def artifact_id(kind: str, version: str, governance: Any, declaration: Any) -> str:
    return "artifact:" + digest({"kind": kind, "version": version, "governance": governance, "declaration": declaration})


def make_artifact(kind: str, declaration: dict[str, Any], *, version: str = "1", governance: Any = None) -> dict[str, Any]:
    if kind not in ARTIFACT_KINDS:
        raise ValueError(f"unknown artifact kind: {kind}")
    if governance is None and ARTIFACT_KINDS[kind]["governance_required"]:
        governance = {"authority": "constitution", "scope": "NPP-E.system"}
    artifact = {"id": "", "kind": kind, "version": version, "governance": governance, "declaration": declaration}
    artifact["id"] = artifact_id(kind, version, governance, declaration)
    return artifact


class Refusal(Exception):
    def __init__(self, *, cause: str, reason: str, proposal: Any, subject: str, rules: list[str] | None = None):
        self.evidence = {
            "evidence_id": "evidence:" + digest({"cause": cause, "reason": reason, "proposal": proposal, "subject": subject}),
            "subject": subject,
            "reason": reason,
            "proposal": proposal,
            "closure": {"status": "established" if cause == "rule_refusal" else "failed", "authority": "NPP-E"},
            "rules": rules or [],
            "predicate_results": {reason: False},
            "consequence": "refuse",
            "cause": cause,
            "nothing_proceeded": True,
            "determinative_fields": ["subject", "proposal", "closure", "rules", "predicate_results", "consequence", "cause", "nothing_proceeded"],
            "observational_fields": [],
        }
        super().__init__(reason)


def validate_artifact(artifact: Any, *, genesis: bool = False) -> None:
    if not isinstance(artifact, dict):
        raise Refusal(cause="closure_failure", reason="unreadable_artifact", proposal=artifact, subject="artifact")
    if set(artifact) != ENVELOPE_KEYS:
        raise Refusal(cause="rule_refusal", reason="unrecognized_or_missing_envelope_element", proposal=artifact, subject="artifact", rules=["MB-5", "MB-11"])
    kind = artifact["kind"]
    if kind not in ARTIFACT_KINDS:
        raise Refusal(cause="rule_refusal", reason="unregistered_kind", proposal=artifact, subject="artifact", rules=["KV-2", "MB-9"])
    declaration = artifact["declaration"]
    contract = ARTIFACT_KINDS[kind]
    if not isinstance(declaration, dict) or set(declaration) != contract["fields"]:
        raise Refusal(cause="rule_refusal", reason="closed_kind_surface_violation", proposal=artifact, subject="artifact", rules=["MB-11"])
    if not isinstance(artifact["id"], str) or artifact["id"] != artifact_id(kind, artifact["version"], artifact["governance"], declaration):
        raise Refusal(cause="rule_refusal", reason="identity_integrity_mismatch", proposal=artifact, subject="artifact", rules=["MB-3", "MB-6"])
    if contract["governance_required"] and artifact["governance"] is None:
        raise Refusal(cause="rule_refusal", reason="unmet_governance_requirement", proposal=artifact, subject="artifact", rules=["MB-10"])
    if kind == "constitution" and artifact["governance"] is None and not genesis:
        raise Refusal(cause="rule_refusal", reason="governance_omitted_outside_genesis", proposal=artifact, subject="artifact", rules=["MB-10"])


def admit(artifacts: list[dict[str, Any]], *, genesis: bool = False) -> list[dict[str, Any]]:
    seen: set[str] = set()
    evidence: list[dict[str, Any]] = []
    for artifact in artifacts:
        validate_artifact(artifact, genesis=genesis)
        if artifact["id"] in seen:
            raise Refusal(cause="rule_refusal", reason="duplicate_identity", proposal=artifact, subject="artifact", rules=["MB-6", "ID-4"])
        seen.add(artifact["id"])
        evidence.append({
            "evidence_id": "evidence:" + digest({"subject": artifact["id"], "result": "admit"}),
            "subject": artifact["id"],
            "proposal": artifact,
            "closure": {"status": "established", "authority": "NPP-E", "scope": "NPP-E.system"},
            "rules": ["KV-2", "KV-4", "MB-5", "MB-8", "MB-11"],
            "predicate_results": {"kind_registered": True, "envelope_closed": True, "kind_surface_closed": True},
            "consequence": "admit",
            "cause": "rule_evaluation",
            "nothing_proceeded": False,
            "determinative_fields": ["subject", "proposal", "closure", "rules", "predicate_results", "consequence", "cause", "nothing_proceeded"],
            "observational_fields": [],
        })
    return evidence


def build_snapshot(artifacts: list[dict[str, Any]], *, genesis: bool = True) -> dict[str, Any]:
    admission_evidence = admit(artifacts, genesis=genesis)
    ordered = sorted((deepcopy(item) for item in artifacts), key=lambda item: item["id"])
    constituents = [{"id": item["id"], "integrity": digest(item)} for item in ordered]
    content = {
        "profile": PROFILE_ID,
        "family_revision": FAMILY_REVISION,
        "artifacts": ordered,
        "constituents": constituents,
        "provenance": {"source": "declared_machine_blocks", "derivation": "npp_e_standard_library_constructor"},
        "evidence": admission_evidence,
        "whole_integrity_covers": ["profile", "family_revision", "artifacts", "constituents", "provenance", "evidence", "whole_integrity_covers"],
    }
    whole_integrity = digest(content)
    snapshot_id = "snapshot:" + digest(content)
    return {"id": snapshot_id, **content, "whole_integrity": whole_integrity}


def verify_snapshot(snapshot: dict[str, Any]) -> None:
    required = {"id", "profile", "family_revision", "artifacts", "constituents", "provenance", "evidence", "whole_integrity_covers", "whole_integrity"}
    if set(snapshot) != required:
        raise Refusal(cause="rule_refusal", reason="snapshot_surface_violation", proposal=snapshot, subject="snapshot", rules=["SN-5", "SN-14"])
    if snapshot["profile"] != PROFILE_ID or snapshot["family_revision"] != FAMILY_REVISION:
        raise Refusal(cause="rule_refusal", reason="profile_or_revision_mismatch", proposal=snapshot, subject="snapshot", rules=["CF-1", "SN-5"])
    content = {key: snapshot[key] for key in snapshot["whole_integrity_covers"]}
    if digest(content) != snapshot["whole_integrity"]:
        raise Refusal(cause="rule_refusal", reason="whole_integrity_mismatch", proposal=snapshot, subject="snapshot", rules=["SN-2", "SN-14"])
    if "whole_integrity" in snapshot["whole_integrity_covers"]:
        raise Refusal(cause="rule_refusal", reason="whole_integrity_self_coverage", proposal=snapshot, subject="snapshot", rules=["SN-14"])
    for item in snapshot["artifacts"]:
        validate_artifact(item, genesis=item["kind"] == "constitution")
    expected = [{"id": item["id"], "integrity": digest(item)} for item in sorted(snapshot["artifacts"], key=lambda item: item["id"])]
    if snapshot["constituents"] != expected:
        raise Refusal(cause="rule_refusal", reason="constituent_integrity_mismatch", proposal=snapshot, subject="snapshot", rules=["SN-5", "SN-8"])
    if "snapshot:" + digest(content) != snapshot["id"]:
        raise Refusal(cause="rule_refusal", reason="snapshot_identity_mismatch", proposal=snapshot, subject="snapshot", rules=["SN-2", "SN-8"])


@dataclass(frozen=True)
class Inspection:
    snapshot: dict[str, Any]

    def __post_init__(self) -> None:
        verify_snapshot(self.snapshot)

    def enumerate_artifacts(self) -> list[dict[str, Any]]:
        return deepcopy(self.snapshot["artifacts"])

    def get_artifact(self, identity: str) -> dict[str, Any]:
        for artifact in self.snapshot["artifacts"]:
            if artifact["id"] == identity:
                return deepcopy(artifact)
        raise Refusal(cause="rule_refusal", reason="absent_named_artifact", proposal={"id": identity}, subject="inspection", rules=["IN-6", "IN-9"])

    def snapshot_identity(self) -> str:
        return self.snapshot["id"]


def sample_artifacts() -> list[dict[str, Any]]:
    constitution = make_artifact("constitution", {"purpose": "demonstrate NPP-E vocabulary and inspection", "vocabulary": "NPP-E.artifacts"}, governance=None)
    read = make_artifact("read-operation", {"class": "read", "answer": "named artifact", "refusal": "malformed or absent request"})
    return [constitution, read]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("demo", "inspect"))
    parser.add_argument("identity", nargs="?")
    args = parser.parse_args()
    snapshot = build_snapshot(sample_artifacts())
    if args.command == "demo":
        verify_snapshot(snapshot)
        print(json.dumps({"profile": PROFILE_ID, "family_revision": FAMILY_REVISION, "snapshot": snapshot["id"], "artifacts": [item["id"] for item in snapshot["artifacts"]]}, indent=2, sort_keys=True))
        return 0
    try:
        print(json.dumps(Inspection(snapshot).get_artifact(args.identity or ""), indent=2, sort_keys=True))
        return 0
    except Refusal as refusal:
        print(json.dumps({"refusal": refusal.evidence}, indent=2, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

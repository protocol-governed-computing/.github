# Determinations

Family revision for all entries: `f476ea5c06506a3efba1d773a5d42818c9190601`.

## 1. Implementation choices

**Matter:** implementation language and dependency set.

**Source basis:** `task_build_a_realization.md` §4; `NPP-E-scope.md` Working assumption 5; `NPP-E.md` §1.

**Claim type:** chosen by author.

**Reasoning:** The task permits stack choice and the profile selects SHA-256. Python 3.12.10 and the standard library provide the required structured encoding, hashing, CLI, and test mechanisms without external dependencies.

**Confidence:** high.

**Matter:** canonical encoding for semantic objects.

**Source basis:** `spec/2c_machine_block.md` §3; `spec/4c_identity_and_addressing.md` §2.2; `NPP-E.md` §§5-6.

**Claim type:** chosen by author.

**Reasoning:** The archive requires a canonical form but leaves its scheme open. The realization uses JSON with sorted keys, compact separators, and ASCII escaping.

**Confidence:** high.

**Matter:** artifact identity formula.

**Source basis:** `spec/2c_machine_block.md` §6.1; `spec/4c_identity_and_addressing.md` §2.2; `NPP-E.md` §6.

**Claim type:** chosen by author.

**Reasoning:** Identity must be derived from canonical semantic content, but the family does not prescribe a syntax. Artifact identity is SHA-256 over kind, version, governance, and declaration, with the `artifact:` representation prefix.

**Confidence:** high.

**Matter:** snapshot whole-integrity coverage.

**Source basis:** `spec/3b_snapshot.md` §§6-7; `NPP-E.md` §7.

**Claim type:** chosen by author.

**Reasoning:** The profile selects SHA-256 and the standard requires the covered set to be declared and to exclude the whole-integrity value. The implementation covers profile, family revision, artifacts, constituent digests, provenance, evidence, and the declared coverage set itself.

**Confidence:** high.

**Matter:** supported conformance claim.

**Source basis:** `task_build_a_realization.md` §§1, 7-9; `NPP-E.md` §11; `spec/7a_conformance_model.md` §§2-8.

**Claim type:** chosen by author.

**Reasoning:** The realization claims only NPP-E vocabulary/declaration surface and the narrower snapshot/inspection demonstrations explicitly listed in `conformance_evidence.md`; it does not claim the broader system-instance, runtime, transformation, or genesis claims.

**Confidence:** high.

**Matter:** refusal representation.

**Source basis:** `spec/2f_enforcement_and_refusal.md` §§6.1-6.3; `spec/3e_evidence_attestation_provenance.md` §§3-5; `NPP-E.md` §7.

**Claim type:** inferred from source.

**Reasoning:** Refusal evidence includes proposal, subject, closure status, rules, predicate results, dominant consequence, cause, and no-progress assertion. Rule refusal and closure failure are separate values. The field names are an implementation representation of the required semantic content.

**Confidence:** high.

**Matter:** read-surface API shape.

**Source basis:** `spec/5b_governed_inspection.md` §§2-11; `NPP-E.md` §8.

**Claim type:** chosen by author.

**Reasoning:** The profile requires an in-process inspection interface and names lookup, enumeration, and snapshot lookup. The realization exposes `Inspection.enumerate_artifacts`, `Inspection.get_artifact`, and `Inspection.snapshot_identity`; the interface returns the answer and refuses absent subjects.

**Confidence:** high.

**Matter:** sample artifact declaration surfaces.

**Source basis:** `NPP-E.md` §3; `spec/2c_machine_block.md` §§4-12.

**Claim type:** chosen by author.

**Reasoning:** NPP-E closes the five canonical kinds and requires closed kind declarations. The realization supplies a constitution and read-operation sample with explicit fields, while the other three kind contracts are registered and validated even though they are not needed by the narrow sample.

**Confidence:** high.

**Matter:** genesis constitution governance omission.

**Source basis:** `spec/1b_semantic_model.md` §11; `spec/2a_governance_standard.md` §6.1; `NPP-E.md` §§3, 9.

**Claim type:** inferred from source.

**Reasoning:** The sample constitution omits its governance assertion only when `genesis=True`; ordinary admitted kinds require governance. This realizes the profile's stated genesis distinction without claiming the full genesis conformance claim.

**Confidence:** medium.

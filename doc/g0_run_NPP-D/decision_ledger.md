# Determinations Register

Each entry uses the required provenance shape. These are determinations made by NPP-D or inferred from an expressly delegated profile decision. Commission-fixed scope is recorded separately in `list_assumptions.md`; unresolved matters are recorded in `findings_register.md`.

## Determination D-1

**Matter:** Profile identity and governing revision.

**Source basis:** Normative Platform Profile §9; Conformance Model §2; commission §§1-3; `REVISION`.

**Claim type:** expressly required by source for identity and revision; chosen by author for the identity `NPP-D` as the commission's run identity.

**Reasoning:** A profile must have an identity and a claim must name the family revision. The commission identifies this run as NPP-D through the new run designation and supplies the revision file. The identity is not inherited from any earlier work.

**Confidence:** high

## Determination D-2

**Matter:** One accepted snapshot, one governed state, and one active closure for the supported system-instance scope.

**Source basis:** Conceptual Model §§3.3, 7, 8; Semantic Model §§3, 4, 8, 10; Snapshot §§1, 3, 9; Runtime §§2-3; Architectural Invariants AI-1, AI-6, AI-10, AI-12, AI-15; commission §2.

**Claim type:** expressly permitted by source; chosen by author as the profile narrowing.

**Reasoning:** The family defines sealed snapshot execution and permits a profile to select and constrain facilities. NPP-D narrows the claim to one active instance and excludes concurrent or ambient governing inputs.

**Confidence:** high

## Determination D-3

**Matter:** No interaction boundary, no external protocol binding, and no interaction-result claim.

**Source basis:** Governed Interaction Boundary §§2, 5-10, 16; Normative Platform Profile §7; commission §2.

**Claim type:** expressly permitted by source; fixed by commission scope and recorded as a profile selection.

**Reasoning:** The commission explicitly fixes no external protocol boundary. The family distinguishes interaction from inspection, so selecting no interaction does not remove inspection.

**Confidence:** high

## Determination D-4

**Matter:** Means by which inspection is reached.

**Source basis:** Governed Inspection §2.1; Normative Platform Profile §7; commission §2.

**Claim type:** expressly required by source that the profile decide; chosen by author as direct in-process invocation or direct access to sealed representation.

**Reasoning:** The family expressly says a profile selecting no interaction boundary must state how its read surface is reached. Direct reach is selected because it fits the no-wire-boundary scope without introducing a new protocol facility.

**Confidence:** high

## Determination D-5

**Matter:** Read-surface openness policy.

**Source basis:** Governed Inspection §11; Normative Platform Profile §7.

**Claim type:** expressly required by source that the profile decide; chosen by author as open to every caller class, while retaining per-read governed determination.

**Reasoning:** The standard makes policy and determination distinct. NPP-D chooses the most permissive policy available without permitting an ungoverned read.

**Confidence:** high

## Determination D-6

**Matter:** Evidence trust root.

**Source basis:** Evidence, Attestation & Provenance §§6.2, 10, 12; Normative Platform Profile §7.

**Claim type:** expressly required by source that the profile decide; chosen by author as the externally authored, identity- and revision-identified NPP-D profile document.

**Reasoning:** The family supplies no trust root and expressly assigns this matter to the profile and checking party. NPP-D names one root rather than deferring acceptance to the claimant.

**Confidence:** medium

## Determination D-7

**Matter:** Evidence retention period.

**Source basis:** Evidence, Attestation & Provenance §§11-12; Normative Platform Profile §7.

**Claim type:** expressly required by source that the profile decide; chosen by author as retention for the instance lifetime and thereafter for as long as the claim remains withdrawn or superseded but checkable.

**Reasoning:** Retention is expressly left to profiles. The selected period prevents a profile claim from becoming uncheckable merely because the instance ended.

**Confidence:** medium

## Determination D-8

**Matter:** Namespace arrangement.

**Source basis:** Identity & Addressing §§5, 6, 8; Normative Platform Profile §7.

**Claim type:** expressly required by source that the profile decide; chosen by author as one flat namespace named `npp-d` with no fallback.

**Reasoning:** The family delegates namespace existence and arrangement. A flat namespace is sufficient for the single-system scope and carries no authority semantics.

**Confidence:** high

## Determination D-9

**Matter:** Projections carried by the supported system.

**Source basis:** Projection §§2, 3, 9-12; Governed Inspection §7; Normative Platform Profile §7.

**Claim type:** expressly required by source that the profile decide; chosen by author as canonical form and evidence view only.

**Reasoning:** These projections support the selected sealed execution and independent inspection claims. The profile does not require other projections.

**Confidence:** high

## Determination D-10

**Matter:** Capability outcome vocabulary.

**Source basis:** Capability §§3, 3.2, 4; Execution Model §§4-5; Normative Platform Profile §7.

**Claim type:** expressly required by source that the profile decide; chosen by author as the closed set `success`, `failure`, `refusal`.

**Reasoning:** A capability contract must enumerate outcomes, and the family delegates which outcomes contracts may declare. The selected names are profile labels; `refusal` is not redefined as governance refusal.

**Confidence:** medium

## Determination D-11

**Matter:** Sufficiency criterion before realization.

**Source basis:** Governed Transformation §§13, 16; TR-5, TR-8, TR-9, TR-17, TR-18, TR-21; Machine Block §§4-11; Capability §3; Governed Inspection §4; Projection §3; Normative Platform Profile §7.

**Claim type:** expressly required by source that the profile decide; chosen by author as total declaration of every fact required by each selected facility, with refusal on omission or ambiguity.

**Reasoning:** The family requires sufficiency and delegates its criterion. NPP-D enumerates the selected facility facts and does not allow realization to supply missing semantics.

**Confidence:** high

## Determination D-12

**Matter:** Closed admissible kind vocabulary and governance-assertion disposition.

**Source basis:** Kind Vocabulary §§2, 5, 9-11; Machine Block §§4-11; Governance Semantic Ontology §8; Governed Transformation §5; Normative Platform Profile §7.

**Claim type:** expressly permitted by source; chosen by author as the four named NPP-D kinds, each requiring a governance assertion.

**Reasoning:** The family requires a closed profile-owned vocabulary but enumerates no family-wide kinds. The selected set is therefore an author choice over the open declaration language, recorded explicitly rather than presented as family-required.

**Confidence:** medium

## Determination D-13

**Matter:** Genesis is outside the supported claim scope.

**Source basis:** Normative Platform Profile §7; Governed Transformation §12; Conformance Test Specification §9; commission §2.

**Claim type:** expressly permitted by source; chosen by author as a scope narrowing.

**Reasoning:** The profile may exclude a class of systems. Excluding genesis avoids supporting a claim whose profile-specific fixtures have not been authored and named.

**Confidence:** high

## Determination D-14

**Matter:** Additional obligations under Part VI §5.

**Source basis:** Normative Platform Profile §§3.1, 5; EN-1; NP-6; commission §5.3.

**Claim type:** expressly permitted by source; chosen by author to declare none.

**Reasoning:** The profile's decisions are selections and parameterizations. Repeating them as additional obligations would not add a distinct breach condition and would violate §5's distinction.

**Confidence:** high

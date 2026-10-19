# List of Assumptions

This file records the assumptions required to proceed when the standard delegated a decision to a profile but did not supply a concrete mechanism. These are not family-established facts; they are explicit working assumptions used to author NPP-C under the instructions of the task.

1. Single-system means one closure and one accepted baseline
   - Assumption: The profile applies to one governed system, one accepted snapshot, and one closure at a time.
   - Basis: 1a §3.3; Semantic Model §3 and §10; 6a §1.
   - Why needed: The profile scope explicitly specifies a single-system platform and the family distinguishes single-system governance from multi-system composition.

2. Inspection means a declared read surface that does not execute the subject
   - Assumption: A required inspection boundary must be reachable by a checking party without entering execution or mutating state.
   - Basis: 5b; 1c AI-11; 6a §1.
   - Why needed: The profile's scope requires inspection, but the family does not specify a standard means of inspection in a general implementation.

3. “No external protocol boundary” is interpreted strictly for the supported scope
   - Assumption: The system may not present an externally reached protocol boundary that acts as an execution or invocation surface under the profile.
   - Basis: 5a; 6a §1; 6a §7.
   - Why needed: The task expressly states no external protocol boundary, so the profile is narrower than a general platform and excludes remote invocation.

4. Trust is limited to family-defined evidence and attestation
   - Assumption: The profile accepts no additional non-family trust-root or attestation regime.
   - Basis: 3e; 6a §7; 7a §4.
   - Why needed: The standard names evidence and attestation but does not define a concrete external trust-root model. This assumption prevents adding an undeclared external authority.

5. One tenant is a governance-scope condition, not a deployment artifact
   - Assumption: “One tenant” means a single governance authority and no additional subject-level tenant separation within the profile's supported class.
   - Basis: 1a §5, §6; 2e; 6a §7.
   - Why needed: The family defines authority, concern, and domain but not a universal tenant concept, so the profile must define tenant scope locally for the supported claim.

6. The profile closes a minimal kind vocabulary, not the family
   - Assumption: A profile may close a vocabulary of the few kinds needed for the supported scope without claiming to enumerate all possible PGC kinds.
   - Basis: 2d §2, §5, §10; 2c §7; 6a §7.
   - Why needed: The family says the set of admissible kinds is a profile decision, and the profile must fix a closed set for the supported claims.

7. The profile's claim list is intentionally narrow
   - Assumption: The profile supports only the claims it can evaluate under the family's discharge classes and refuses broader implicit claims.
   - Basis: 6a §7; 7a §7; 7b §3.
   - Why needed: The task requires exactness. A wider claim set would exceed what the profile can support without inventing new discharge instruments.

8. The profile is a blocked but reviewable result rather than a universal generalization
   - Assumption: This profile is not asserted to be a general-purpose platform or a universal implementation class; it is a narrow, strict profile for the task's scope.
   - Basis: 6a §1; 0z §7; task commission.
   - Why needed: The family clearly says a profile should narrow its scope and not pretend to be minimal or universal.

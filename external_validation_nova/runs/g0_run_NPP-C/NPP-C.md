# Normative Platform Profile NPP-C

## 1. Identity and scope

- Profile identity: NPP-C
- Revision cited: e736800df3388dfb4ed403a494089e1320064017
- What it profiles: a single governed system constituted as one sealed snapshot, executed against a governed state, with inspection required, no external protocol boundary, no replication, one tenant, and no attestation beyond the standard's own evidence and attestation semantics.
- Purpose: To support a narrow, reviewable conformance claim for a single-system platform intended for governed inspection and sealed execution, not for general-purpose multi-tenant or externally reached deployment.

This profile is a narrowing selection under Part VI. It does not redefine any core facility, widen any permission, or convert a family requirement into a local preference. It exists to make the family's delegated choices concrete for the class of systems in scope and to refuse systems outside that class.

## 2. The selection and constraints this profile makes

This profile selects the following determinations from the family and narrows them to the stated scope:

1. Single governed system, one closure, one baseline
   - The system claims exactly one governed baseline, one accepted snapshot, and one closure applicable to that baseline at a time.
   - Basis: Conceptual Model §3.3; Semantic Model §3, §8, §10; Snapshot and Runtime documents; 6a §1 and §7.
   - Why: A platform whose baseline is multiple or whose closure is non-unique does not satisfy the scope of this profile and is not reviewable as a single-system profile.

2. Sealed execution input only
   - Execution consumes a sealed snapshot and governed state only; no runtime-resolved ambient authority may effect a governing determination.
   - Basis: Conceptual Model §7, §8; Semantic Model §4, §7.1, §8, §10; Architectural Invariants AI-1, AI-6, AI-10, AI-12.
   - Why: The profile's purpose is to support a sealed, inspectable governed system; a runtime that derives behavior from undeclared context would fall outside the class this profile supports.

3. Inspection is required
   - The system must expose a governed inspection boundary sufficient to answer questions about its own declarations, state, and evidence without changing the governed state.
   - Basis: Governed Inspection and 6a §7; 5b §2.1, §10, and §11; 6a §1 and §6.
   - Why: The profile's scope declares inspection as a required property, because the platform is intended to be reviewable by a checking party.

4. No external protocol boundary
   - This profile excludes any externally reached wire protocol within the profile's claimed scope; the system may expose a read surface, but not a remote runtime boundary that acts as an external protocol gateway.
   - Basis: 5a; 6a §1; 6a §7; Conceptual Model §6, *surface*.
   - Why: The profile is deliberately narrower than a general platform; a remote protocol boundary would be a different platform with different obligations and would fail the profile's no-external-boundary selection.

5. No attestation beyond what the standard requires
   - The system may rely only on the evidence and attestation concepts defined by the family; it may not introduce a non-standard trust-root or external attestation regime as a condition of profile satisfaction.
   - Basis: 3e; 6a §7; 7a §4; 7b §3 and §9.
   - Why: The profile narrows the scope to the family-defined evidence model and rejects any non-standard trust assumption as a profile-invented authority.

6. One tenant, no replication
   - The system has one tenant, one authority boundary, and no replicated governed state or multi-node same-identity copies in the profile's supported scope.
   - Basis: 1a §6 and §8; 3a and 3b; 6a §7; 2e and 2d as the identity and authority semantics of composition.
   - Why: Replication and multi-tenant composition create additional authority and closure questions that the profile intentionally excludes.

7. Closed kind vocabulary for the supported profile
   - This profile closes a vocabulary containing the kinds required for the single-system profile: a root-of-governance kind, a sealed snapshot kind, an inspection surface kind, and an evidence-record kind. The vocabulary is closed within this profile revision.
   - Basis: 2d §2, §5, §10; 2c §7, §9, §11; 2b §8; 6a §7.
   - Why: A profile is where a system's admissible kinds are selected; this profile fixes the set so that unrecognized kinds are refused and the profile's claims remain reviewable.

## 3. Additional obligations imposed by this profile

The profile adds no new semantics. It adds enforceable narrowing obligations on systems claiming it. Each one is enforceable as a profile-level governance obligation and is measurable against the family's own rules.

| ID | Additional obligation | What establishes breach | Source of delegation |
|---|---|---|---|
| NPP-C-1 | The system SHALL accept exactly one baseline and one snapshot at a time. | Evidence of a second accepted baseline, or a second concurrently valid snapshot, without a governed transformation. | 1a §7; 3b; 6a §7 |
| NPP-C-2 | The system SHALL expose no external protocol boundary within the profile scope. | Any admitted remote protocol entry path or externally reached execution surface. | 5a; 6a §7; 1a §6 |
| NPP-C-3 | The system SHALL provide a read surface for inspection that is not itself executable. | A read operation that reaches executable behavior or mutates state. | 5b; 1c AI-11; 6a §7 |
| NPP-C-4 | The system SHALL not depend on non-standard attestation as a precondition of conformance. | A claim whose checking party requires a trust root or attestation mechanism not defined by the family. | 3e; 7a; 6a §7 |
| NPP-C-5 | The system SHALL operate under a single tenant and no replication. | More than one tenant, replicated storage, or same-identity copies in different locations. | 1a §6; 2e; 6a §7 |
| NPP-C-6 | The system SHALL close its kind vocabulary under the profile and refuse unregistered kinds. | Admission of an unregistered kind or an artifact whose kind is inferable from location or naming instead of declaration. | 2d; 2c; 6a §7 |

## 4. Conformance claims supported by this profile

This profile supports only the claims below. Each claim is tied to a discharge class or classes that can establish it. Where the profile does not define a discharge instrument, it says so and does not invent one.

| Claim | What it states | Discharge class | Basis |
|---|---|---|---|
| NPP-C-claim-1 | The system is a single governed system under one closure and one accepted snapshot. | Structural + derivational | 1a §3.3; 3b; 6a §7 |
| NPP-C-claim-2 | The system's behavior is determined by the sealed snapshot and not by ambient execution context. | Comparative + derivational | 1c AI-12; 3c; 6a §7 |
| NPP-C-claim-3 | An inspection boundary is required and reachable, and it does not trigger execution. | Structural + observational | 5b; 1c AI-11; 6a §7 |
| NPP-C-claim-4 | No external protocol boundary is admitted under this profile. | Structural | 5a; 6a §7 |
| NPP-C-claim-5 | The system uses no replication and one tenant only. | Structural + comparative | 1a §6; 2e; 6a §7 |
| NPP-C-claim-6 | The profile's closed kind vocabulary is the only admissible one for the system. | Structural + derivational | 2d; 2c; 6a §7 |

These are the only claims the profile supports. All other claims are excluded as outside the profile's scope.

## 5. What this profile excludes

This profile excludes systems that:

- have multiple simultaneously active snapshots or multiple accepted baselines;
- support replication, sharding, or multi-node same-identity copies;
- accept remote protocol-bound external invocation within the claimed scope;
- require a non-family trust root or non-standard attestation to establish conformance;
- define governance by ambient execution context rather than declared governance;
- claim additional domain-specific or execution-environment obligations without a separate profile that names them and is itself conformant under Part VI;
- support a wider platform than the profile's scope, including multi-tenant or general-purpose composition.

## 6. Kind vocabulary and closure

This profile closes a vocabulary within its own revision and states the admissible kinds for the supported scope. The vocabulary is not a family-wide enumeration; it is a profile-owned closure over the family's open declaration language.

The closed vocabulary for this profile is:

1. `platform-root` — the governing root of the system; carries the governance assertion for the system as a whole.
2. `snapshot` — the sealed, total representation accepted for execution.
3. `inspection-surface` — the declared read surface used to answer questions about the system.
4. `evidence-record` — the material record by which determinations are established.

Each admitted kind declares what it carries and its category under the ontology; the kind contract for each is profile-defined and evaluated under the profile's closure. A kind not listed is refused rather than silently passed through.

This is consistent with the family because the Family's kind vocabulary requirement is delegated to profiles, and the profile is where a closed selection is fixed. It is also consistent with 2d §5, because the vocabulary is closed and the profile states the governance-assertion disposition for each admitted kind.

## 7. Why this profile is written this way

The key reason is that the family requires a profile to decide every deferred item that bears on the claims it supports, but it does not specify a general-purpose system. The profile therefore narrows to the exact use-case in the task: one sealed system, one tenant, no replication, no external protocol, required inspection, and evidence-only attestation.

This does not claim to be minimal or universal. It is a profile for a specific class of governed systems under the family. That is exactly what Part VI requires a profile to do.

## 8. Conclusion

This profile is a valid narrowing profile under Part VI only for the stated class. It is deliberately not a general-purpose platform profile, and it refuses everything outside the narrow supported scope. The profile's value lies not in its breadth, but in the fact that every selection it makes is a choice the family delegates to profiles rather than a claim about a particular implementation.

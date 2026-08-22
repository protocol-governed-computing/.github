# REFERENCE_PLATFORM_PROFILE_V1

A **snapshot profile** is a conformance contract over an assembled snapshot. It states the
properties a snapshot SHALL satisfy — not an inventory of what any particular build contains.

A **Profiled Normative Platform (PNP)** is what results when a governance surface, a set of
workloads, and optionally a business domain are compiled and assembled against a profile. There are
as many PNPs as there are profiles, and **no platform is minimal by nature** — minimality is
relative to a profile (6a §8).

This is the **reference** profile: the one the reference realization is developed and demonstrated
against. It selects a single-node, unsigned, locally-stored configuration exercising the full
governed path from interaction admission through constructed invocation to executed workflow and
emitted evidence.

**It is not privileged.** No profile is (6a §11). It is not a base that other profiles derive from —
derivation is declared by the deriving profile, naming its base by identity (6a §10), and this
profile makes no claim on profiles that have not named it.

**Supersession.** This profile supersedes `NORMATIVE_PLATFORM_PROFILE_BASELINE_V0` by that exact
identity (4e §2). The predecessor is retained and remains readable; nothing may reference it
(SU-5, SU-7). The differing names are immaterial — supersession is a declared relation between
identities, never derived from a naming convention (SU-2, ID-6).

---

## 1. Profile

```yaml
snapshot_profile:
  identity: REFERENCE_PLATFORM_PROFILE_V1
  supersedes: NORMATIVE_PLATFORM_PROFILE_BASELINE_V0

  description: >
    Baseline normative platform profile. Defines the minimum set of governance artifacts,
    component capabilities, workloads, and conformance claims a snapshot SHALL provide in order
    to demonstrate protocol-governed execution end to end.

  declared_vocabulary:
    # The closed set of artifact kinds admissible under this profile (KV-1, KV-2).
    # A kind absent from this set is unregistered and MUST be refused.
    # Membership is this profile's selection; no kind is required by the family (KV-9).
    kinds:
      - CONSTITUTION
      - INVARIANT
      - ASSERT
      - STRUCTURE
      - VOCABULARY
      - SURFACE_CONTRACT
      - CAPABILITY_CONTRACT
      - CAPABILITY_TRANSFORM
      - CAPABILITY_SIDE_EFFECT
      - RUNTIME_BINDING
      - WORKFLOW
      - INTENT
      - ACTOR
      - EVENT
      - TRANSPORT_INGRESS
      - TRANSPORT_EGRESS

  required_governance:
    artifact_kinds:
      - CONSTITUTION
      - INVARIANT
      - STRUCTURE
      - VOCABULARY
      - SURFACE_CONTRACT
      - CAPABILITY_TRANSFORM
      - CAPABILITY_SIDE_EFFECT
    artifacts:
      # Constitutional core — the authority chain a governed artifact resolves against.
      - governance::CONSTITUTION_GOVERNANCE_V0
      - structure::CONSTITUTION_STRUCTURE_V0
      - governance::CONSTITUTION_INVARIANTS_V0
      - conformance::CONSTITUTION_ASSERT_V0
      - compiler::CONSTITUTION_COMPILER_V0
      - federation::CONSTITUTION_FEDERATION_BOUNDARY_V0
      - vocabulary::CONSTITUTION_VOCABULARY_V0
      - authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0
      # Execution semantics — what a workflow is and how it is bound and run.
      - workflow::CONSTITUTION_WORKFLOW_V0
      - execution::CONSTITUTION_EXECUTION_V0
      - execution_topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
      - capability_contracts::CONSTITUTION_CAPABILITY_CONTRACT_V0
      - capability_transforms::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
      - capability_side_effects::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
      - runtime_binding::CONSTITUTION_RUNTIME_BINDING_V0
      - trace::CONSTITUTION_TRACE_EXECUTION_V0
      # Governed boundary — admission and egress as first-class contracts.
      - transport::CONSTITUTION_ADMISSION_V0
      - transport::CONSTITUTION_TRANSPORT_ENVELOPE_V0
      - transport::CONSTITUTION_TRANSPORT_INGRESS_V0
      - transport::CONSTITUTION_TRANSPORT_EGRESS_V0
      # Structural bootstrap — how the surface is discovered, identified, and dispatched.
      - structure::STRUCTURE_DISCOVERY_V0
      - structure::STRUCTURE_IDENTITY_V0
      - structure::STRUCTURE_ARTIFACT_IDENTITY_V0
      - structure::STRUCTURE_FQDN_TREE_V0
      - structure::STRUCTURE_SCHEMA_DISPATCH_V0
      - execution::STRUCTURE_RUNTIME_EXECUTION_V0
      - capability_transforms::STRUCTURE_CT_IR_CONTRACT_V0
      - conformance::STRUCTURE_CONFORMANCE_POLICY_V0

  required_compiler:
    capabilities:
      - artifact_discovery
      - schema_validation
      - invariant_assertion
      - topology_compilation
      - semantic_addressing
      - deterministic_projection
      - trust_attestation

  required_assembler:
    capabilities:
      - domain_composition
      - hash_verification
      - manifest_emission

  required_runtime:
    capabilities:
      - snapshot_loading
      - workflow_execution
      - trace_generation

  required_transport:
    capabilities:
      - ingress
      - admission
      - egress

  required_workloads:
    entry_workflows:
      - workload::WF_COLLATZ_CONJECTURE_V0

  required_claims:
    - TRANSPORT_PROTOCOL_INDEPENDENCE
    - COMPILED_INVOCATION_RESOLUTION
    - SNAPSHOT_IMMUTABILITY
    - DETERMINISTIC_EXECUTION
```

---

## 2. Claims and their discharge

A claim is a property the snapshot asserts about itself. A claim with no stated discharge is
decorative — each one below names what settles it.

| Claim | Asserts | Discharged by |
|---|---|---|
| `TRANSPORT_PROTOCOL_INDEPENDENCE` | An Operation Identity is stable across wire protocols; no protocol detail reaches workflow semantics. | `transport::INVARIANT_TRANSPORT_OPERATION_IDENTITY_INDEPENDENCE_V0`, `transport::INVARIANT_TRANSPORT_RESULT_CLASS_PROTOCOL_INDEPENDENCE_V0`, `execution_topology::INVARIANT_TOPOLOGY_TRANSPORT_ORTHOGONAL_V0` |
| `COMPILED_INVOCATION_RESOLUTION` | Operation identity resolves to a governed executable target at compile time; nothing is routed at runtime. | `transport::INVARIANT_TRANSPORT_TARGET_EXISTS_V0`, `transport::INVARIANT_TRANSPORT_NO_DYNAMIC_ROUTING_V0` |
| `SNAPSHOT_IMMUTABILITY` | The assembled snapshot is sealed; no behavior enters at execution time that was not present at build time. | `execution_topology::INVARIANT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0`; manifest `composite_hash` round-trip verification at assembly |
| `DETERMINISTIC_EXECUTION` | The same snapshot and payload always produce the same result and the same graph addresses. | Compiler verify stage (round-trip + determinism check); per-domain `graph_address_hash` stability across recompiles; runtime determinism tests |

---

## 3. Verification status

The profile is checked against `manifest.json` and the compiled projections of an assembled
snapshot. Not every axis is machine-verifiable today.

| Axis | Verifiable now | Against |
|---|---|---|
| `required_governance.artifacts` | Yes | Canonical projection FQDNs |
| `required_governance.artifact_kinds` | Yes, with normalization (§4) | Canonical projection discriminators |
| `required_workloads.entry_workflows` | Yes | Canonical projection FQDNs; manifest domain list |
| `required_claims` | Yes, indirectly | Presence of the discharging invariants above |
| `required_compiler.capabilities` | **No** | — |
| `required_assembler.capabilities` | **No** | — |
| `required_runtime.capabilities` | **No** | — |
| `required_transport.capabilities` | **No** | — |

The manifest records `provenance.source_commits`, `provenance.compiler_versions`, and per-domain
`graph_address_hash`, but **no component declares its capabilities into the snapshot**. Until each
component emits a capability declaration that assembly records in the manifest, the four component
axes are *declared but unverified* — they state intent for a conformance checker that cannot yet
enforce them. Closing this gap is what makes those axes real contract terms rather than commentary.

---

## 4. Known vocabulary discrepancies

Two mismatches a conformance checker must handle rather than assume away.

**Canonical vs compiled kind names.** This profile uses the canonical `artifact_kind` vocabulary.
The compiled projection currently carries legacy short forms for three of them:

| Canonical (used here) | Compiled projection emits |
|---|---|
| `VOCABULARY` | `VOCAB` |
| `SURFACE_CONTRACT` | `SURFACE` |
| `CAPABILITY_TRANSFORM` / `CAPABILITY_SIDE_EFFECT` | `CT` / `CS` |

A checker MUST normalize to canonical form before comparing. The profile does not adopt the legacy
forms — a standard references canonical vocabulary.

**Component capability names are new vocabulary.** Of the capability identifiers above, only
`ingress`, `admission`, and `egress` are grounded in an existing standard (the transport standard's
TI/TE contracts and admission semantics). The compiler, assembler, and runtime capability names are
minted here and have no declared definition elsewhere. They are deliberately named for observable
functions rather than internal stage names, so they remain stable if a component reorganizes
internally — but they are a second vocabulary until each component adopts them.

---

## 5. The declared vocabulary

`declared_vocabulary.kinds` in §1 is the **closed set of artifact kinds admissible under this
profile**. A kind outside it is unregistered and is refused (KV-2).

Three properties follow, and each is a property of *this profile* rather than of the family:

- **Membership is a selection.** No kind is required of a governed system by the standard family
  (KV-9). Another profile may admit a different set and conform equally.
- **The set is closed within this profile's identity.** Admitting a kind is a change to this
  profile's obligations, and therefore a new profile identity (NP-9) — not an edit to this one.
- **Admission is the vocabulary's act.** A domain may propose a kind; it does not create one, and
  holds no private vocabulary (DP-9).

`required_governance.artifact_kinds` is a different statement: those are the kinds a conforming
snapshot's governance artifacts **must exercise**. The declared vocabulary bounds what may exist;
the required kinds state what must be present. A kind may be admissible and absent from a given
build.

**Naming conventions carry no classification.** Where an identifier bears a prefix corresponding to
a kind, the prefix is convention; kind is established by declaration and never derived from a name
(KV-5, MB-6).

## 6. Scope rules

- A profile references **governed identities only** — FQDNs and artifact codes. Never filesystem
  paths, repository names, branch names, or module paths. Those are deployment facts; they change
  independently of conformance, and a profile that encodes them is invalidated by a rename.
- A profile states requirements, never an inventory. A snapshot may contain more than the profile
  requires and still conform.
- Profile scope changes are new versions (`_V0` → `_V1`), never in-place edits.

---

## 7. Version history

- **V1**: Reissued against the namespace rename. Every FQDN this profile pins was re-expressed in
  the post-rename namespace set; the required properties, claims, and capability names are
  unchanged. The rename retired the `fb.constitution` and `fb.topology` composites and split them
  across concern-owned namespaces, so no artifact this profile references carries its former
  namespace. All 35 pinned FQDNs were verified to resolve against the assembled snapshot.
- **V0**: Original baseline, written against the pre-rename namespace set. Retained immutable as
  provenance; its FQDNs no longer resolve and it MUST NOT be used to check a current snapshot.

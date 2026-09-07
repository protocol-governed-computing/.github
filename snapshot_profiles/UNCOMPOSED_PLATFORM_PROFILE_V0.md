# UNCOMPOSED_PLATFORM_PROFILE_V0

A **snapshot profile** is a conformance contract over an assembled snapshot. It states the
properties a snapshot SHALL satisfy — not an inventory of what any particular build contains.

This profile selects the **uncomposed platform**: a governance surface and one conformance workload,
with no business domain. It exercises the full governed path from declaration through construction,
sealing and execution to emitted evidence, and it selects no interaction boundary.

**Relation to other profiles.** This profile supersedes nothing and derives from nothing. It is not
a reduction of `REFERENCE_PLATFORM_PROFILE_V1` and makes no claim on it; the two are peers over
different compositions, and a snapshot conforming to one is not thereby judged against the other.
Derivation is declared by the deriving profile, naming its base by identity (`6a` §10), and this
profile declares none. **No profile is privileged** (`6a` §11), and minimality is relative to a
profile (`6a` §8) — this is not a floor.

---

## 1. Profile

```yaml
snapshot_profile:
  identity: UNCOMPOSED_PLATFORM_PROFILE_V0
  supersedes: null
  derives_from: null

  description: >
    Governance surface and one conformance workload, assembled without business domains.
    Single-node, unsigned, locally-stored. Declares the governed boundary contracts and
    exercises no boundary.

  required_domains:
    - platform
    - workload
    - inspection
    - transformation

  excluded_domains:
    - ai_governance
    - blockchain
    - book_library_mgmt

  namespaces:
    # What namespaces this system has (4c §8). A namespace carries identity and nothing else;
    # it MUST NOT encode authority or concern (4c §5, ID-12, GO-11). That a namespace name
    # coincides with a concern name is an arrangement of this system, not a derivation: concern
    # and authority are declared in the machine block and are never read from the namespace.
    form: "<namespace>::<ARTIFACT_IDENTITY>"
    declared:
      - actor
      - artifact
      - authority
      - capability_contracts
      - capability_side_effects
      - capability_transforms
      - compiler
      - conformance
      - cryptographic_trust
      - event
      - execution
      - execution_placement
      - execution_scheduling
      - execution_topology
      - federation
      - governance
      - intent
      - lifecycle
      - runtime_binding
      - security_domain
      - structure
      - surface_contract
      - trace
      - transport
      - vocabulary
      - workflow
      - workload
    closed: true          # a reference into an undeclared namespace is refused
    derives_concern: false
    derives_authority: false

  declared_vocabulary:
    # The closed set of kinds admissible under this profile (KV-1, KV-2). Each states whether a
    # governance assertion is required for its ordinary admission (KV-10, MB-10).
    kinds:
      - kind: CONSTITUTION,          governance_assertion: required
      - kind: INVARIANT,             governance_assertion: required
      - kind: ASSERT,                governance_assertion: required
      - kind: STRUCTURE,             governance_assertion: required
      - kind: VOCABULARY,            governance_assertion: required
      - kind: SURFACE_CONTRACT,      governance_assertion: required
      - kind: CAPABILITY_CONTRACT,   governance_assertion: required
      - kind: CAPABILITY_TRANSFORM,  governance_assertion: required
      - kind: CAPABILITY_SIDE_EFFECT, governance_assertion: required
      - kind: RUNTIME_BINDING,       governance_assertion: required
      - kind: WORKFLOW,              governance_assertion: required
      - kind: INTENT,                governance_assertion: required
      - kind: ACTOR,                 governance_assertion: required
      - kind: EVENT,                 governance_assertion: required
      - kind: TRANSPORT_INGRESS,     governance_assertion: required
      - kind: TRANSPORT_EGRESS,      governance_assertion: required
    aliases_accepted: false
    # KV-7: an alias is never carried or emitted as an authoritative classification. This profile
    # accepts none, so a projection emitting a short form is refused rather than normalized.

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
      # Constitutional core
      - governance::CONSTITUTION_GOVERNANCE_V0
      - structure::CONSTITUTION_STRUCTURE_V0
      - governance::CONSTITUTION_INVARIANTS_V0
      - conformance::CONSTITUTION_ASSERT_V0
      - compiler::CONSTITUTION_COMPILER_V0
      - federation::CONSTITUTION_FEDERATION_BOUNDARY_V0
      - vocabulary::CONSTITUTION_VOCABULARY_V0
      - authority::CONSTITUTION_AUTHORITY_GOVERNANCE_V0
      # Execution semantics
      - workflow::CONSTITUTION_WORKFLOW_V0
      - execution::CONSTITUTION_EXECUTION_V0
      - execution_topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0
      - capability_contracts::CONSTITUTION_CAPABILITY_CONTRACT_V0
      - capability_transforms::CONSTITUTION_CAPABILITY_TRANSFORMS_V0
      - capability_side_effects::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0
      - runtime_binding::CONSTITUTION_RUNTIME_BINDING_V0
      - trace::CONSTITUTION_TRACE_EXECUTION_V0
      # Governed boundary — declared, not exercised (§7)
      - transport::CONSTITUTION_ADMISSION_V0
      - transport::CONSTITUTION_TRANSPORT_ENVELOPE_V0
      - transport::CONSTITUTION_TRANSPORT_INGRESS_V0
      - transport::CONSTITUTION_TRANSPORT_EGRESS_V0
      # Structural bootstrap
      - structure::STRUCTURE_DISCOVERY_V0
      - structure::STRUCTURE_IDENTITY_V0
      - structure::STRUCTURE_ARTIFACT_IDENTITY_V0
      - structure::STRUCTURE_FQDN_TREE_V0
      - structure::STRUCTURE_SCHEMA_DISPATCH_V0
      - execution::STRUCTURE_RUNTIME_EXECUTION_V0
      - capability_transforms::STRUCTURE_CT_IR_CONTRACT_V0
      - conformance::STRUCTURE_CONFORMANCE_POLICY_V0

  required_domain_profiles:
    # DP-4: each domain states whether it claims to be an authority or is a concern.
    - domain: platform,       claims: authority
    - domain: workload,       claims: concern
    - domain: inspection,     claims: concern
    - domain: transformation, claims: authority

  required_self_description:
    # SN-7, SN-14, CF-14. The snapshot names the profile it is judged against; the claimant does
    # not enumerate its own subject classes.
    manifest_declares_profile: true
    manifest_declares_identity_coverage: true
    covered_set_excludes_the_value: true

  required_workloads:
    entry_workflows:
      - workload::WF_COLLATZ_CONJECTURE_V0

  required_claims:
    - SNAPSHOT_IMMUTABILITY
    - DETERMINISTIC_EXECUTION
    - COMPILED_INVOCATION_RESOLUTION
```

---

## 2. Claims and their discharge

A claim with no stated discharge is decorative. Each names what settles it, and the discharge class
`7a` §7 requires of it.

| Claim | Asserts | Discharged by | Class |
|---|---|---|---|
| `SNAPSHOT_IMMUTABILITY` | The sealed snapshot admits no behavior at execution that was not present at build. | `execution_topology::INVARIANT_TOPOLOGY_IMMUTABLE_AFTER_COMPILATION_V0`; integrity recomputed from constituent bytes at acceptance, not compared to a recorded value | derivational |
| `DETERMINISTIC_EXECUTION` | The same snapshot and payload yield the same result and the same graph addresses. | round-trip and determinism checks at construction; per-domain `graph_address_hash` stability across rebuilds | comparative |
| `COMPILED_INVOCATION_RESOLUTION` | An operation identity resolves to a governed target at construction; nothing is routed at execution. | `transport::INVARIANT_TRANSPORT_TARGET_EXISTS_V0`, `transport::INVARIANT_TRANSPORT_NO_DYNAMIC_ROUTING_V0` | structural |

`TRANSPORT_PROTOCOL_INDEPENDENCE` is **not claimed**. It asserts stability across wire protocols, and
this profile exercises no wire protocol; a claim discharged by a substitution that cannot be
performed is not discharged (`CF-8`, `7a` §7.3).

## 3. What reads this profile

**A profile nothing reads adjudicates nothing.** A profile may rot silently — its identities may
cease to resolve while it continues to be cited — and the only thing that prevents it is something
that reads it against a snapshot and fails.

This profile is checked against an assembled snapshot's `manifest.json` and canonical projections.
The check MUST establish, and MUST fail on any of:

1. every identity in `required_governance.artifacts` resolves;
2. every kind in `required_governance.artifact_kinds` is exercised by at least one artifact;
3. no artifact carries a kind outside `declared_vocabulary.kinds`, **without normalization** — an
   emitted alias is a failure, not a form to be canonicalized (`KV-7`);
4. no reference names a namespace outside `namespaces.declared`;
5. the manifest declares this profile by identity, and declares what its integrity value covers;
6. `required_workloads.entry_workflows` resolve and are reachable.

**A profile that has not been read against a candidate snapshot MUST NOT be handed to anyone as a
target.** Running the check is a precondition of use, not a step in verification.

`NORMATIVE_PLATFORM_PROFILE_BASELINE_V0` is superseded and unreferenced; nothing in this profile
names it, and it is not a base of this one.

## 4. Namespace arrangement

`4c` §8 assigns to a profile the question of what namespaces a system has. This profile answers it in
§1 rather than leaving it to be discovered during construction, because a namespace set settled
after artifacts exist is settled by rename.

Three properties, each a requirement rather than a description:

- **A namespace carries identity and nothing else.** It does not carry authority, concern, or
  federation (`4c` §5, `GO-11`).
- **Coincidence is not derivation.** Several namespace names coincide with concern names. That is an
  arrangement of this system; concern and authority are declared in the machine block, and a
  conforming construction never reads either from a namespace (`ID-12`, `MB-6`).
- **The set is closed.** A reference into an undeclared namespace is refused rather than resolved.
  Adding a namespace changes this profile's obligations and is therefore a new profile identity
  (`NP-9`).

## 5. The declared vocabulary

`declared_vocabulary.kinds` is the closed set of kinds admissible here. A kind outside it is
unregistered and MUST be refused (`KV-2`).

**Each kind states whether a governance assertion is required for ordinary admission** (`KV-10`,
`MB-10`). All sixteen require one. That is this profile's selection and not a property of the
family — a profile admitting a kind that requires none conforms equally.

**No alias is accepted.** `2d` §7 permits a system to accept an alias at a boundary provided it is
normalized before the artifact is treated as conformant, and forbids carrying or emitting one as the
authoritative classification. This profile takes the simpler position: none is accepted, so a short
form in a declaration or a projection is a refusal rather than a normalization. An alias set that is
both accepted and emitted is a second vocabulary, and two names for one kind that both remain
authoritative will eventually stop agreeing.

## 6. Externality

`NP-7` requires a profile to be external to what it governs. **Externality is authorship, not
storage.** A profile held in a different directory, repository, or organization, but written by the
same authority that writes the platform, through the same process, is not external — it is the same
act performed twice, and no change of location closes it.

This profile therefore states its own status rather than asserting a property it may not have:

- **For a realization whose authority also authored this profile, `NP-7` is not satisfied**, and a
  conformance claim made under it must record that. This is a finding against that realization's
  claim, not against the profile.
- **For a realization built by an authority that did not author this profile, `NP-7` is satisfied**,
  and the profile is external in the sense the invariant means.

`CM-5` adds a second obligation with the same shape: a profile MUST NOT alter the meaning of a term
defined by the Conceptual Model. Nothing mechanically checks an authored profile against those
definitions. Until something does, that obligation is discharged by reading, and a claim resting on
it should say so.

## 7. The governed boundary

The four transport constitutions and the two transport kinds are **required and not exercised**, and
this is a ruling rather than an oversight.

A boundary contract states what admission and egress mean for a governed system. A platform that
declares them without anything crossing them is coherent: the contracts exist, nothing is admitted
through them, and a later composition that does admit something finds the contracts already
governing rather than authored under pressure. Dropping them would produce a platform that cannot
admit anything without a new profile identity, which is the wrong shape for a surface intended to
host domains it has not yet seen.

What follows from requiring them:

- `TRANSPORT_INGRESS` and `TRANSPORT_EGRESS` are in the declared vocabulary and require a governance
  assertion like every other kind;
- **a closed schema is required for each** (`MB-11`). A kind admitted by a vocabulary and validated
  by no closed surface is admitted on trust;
- no claim is made that depends on exercising the boundary (§2).

## 8. Domain profiles

`DP-4` requires each domain to state whether it claims to be an authority or is a concern, and a
domain that has not stated it is undeclared rather than defaulted. §1 states it for the four selected
domains.

**A domain admitted later must arrive with its own domain profile.** A governance surface intended to
host domains it has not seen cannot derive a newcomer's authority claim from anything — not from its
namespace, not from its position, not from what it contains. The domain declares it, or it is not
admissible.

## 9. Known non-conformance of the reference realization against this profile

Recorded because a profile that quietly accommodates its author's realization is not a contract.

- **`TRANSPORT_INGRESS` and `TRANSPORT_EGRESS` have no closed schema.** §7 requires one. The
  reference realization does not currently satisfy this profile on that point.
- **The compiled projection emits short-form kinds.** §5 accepts no alias; the reference emits `CT`,
  `CS`, `CC`, `WF`, `IN`, `EV`, `TI`, `TE` alongside canonical names. The reference does not
  currently satisfy §3.3.
- **`NP-7` is not satisfied** for a claim by the authority that authored this profile (§6).

Each is a finding against the realization. None is a reason to relax the profile: a requirement
weakened to fit what exists has stopped being a requirement.

## 10. Scope rules

- A profile references **governed identities only** — namespaces and artifact identities. Never
  filesystem paths, repository names, branch names, or module paths. Those are deployment facts that
  change independently of conformance.
- A profile states requirements, never an inventory. **A snapshot may contain more than this profile
  requires and still conform**, and a conformance check that fails a larger snapshot for being larger
  is testing resemblance (`CF-5`).
- Profile scope changes are new identities (`_V0` → `_V1`), never in-place edits (`NP-9`).

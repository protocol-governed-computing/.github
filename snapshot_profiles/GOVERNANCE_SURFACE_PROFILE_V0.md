# GOVERNANCE_SURFACE_PROFILE_V0

```yaml
completion:
  status: complete
  generated_from: scope sheet
  open_gaps: 0
  usable_as_a_target: true    # gaps closed; read against a candidate snapshot, and satisfied by it
```

A snapshot profile is a conformance contract over an assembled snapshot. It states the properties a
snapshot SHALL satisfy — not an inventory of what any particular build contains. A snapshot may
contain more than this profile requires and still conform.

**Supersession.** This profile supersedes `REFERENCE_PLATFORM_PROFILE_V1` by that exact identity
(`4e` §2). The predecessor is retained and remains readable; a snapshot already sealed under it keeps
whatever it claimed, because a claim is evaluated against the profile it named and no later profile
reaches back.

What changes is the obligation on a workload. `REFERENCE_PLATFORM_PROFILE_V1` required
`workload::WF_COLLATZ_CONJECTURE_V0` as an entry workflow, so no composition could satisfy it without
that workload composed. This profile requires none: a workload assembles like any other domain, and a
governance surface is a conforming composition on its own. The obligation this profile keeps is that
the surface be **able** to govern a workflow — the execution-semantics constitutions of §2 — not that
one be present.

Generated from a scope sheet, then completed by hand: the required identities (§2), the additional
obligations (§3), and the discharge of each claim (§4) name things that do not exist until the
artifacts are authored, and cannot be generated from a scope description.

## 1. Profile

```yaml
snapshot_profile:
  identity: GOVERNANCE_SURFACE_PROFILE_V0
  supersedes: REFERENCE_PLATFORM_PROFILE_V1
  derives_from: null
  description: 'A governance surface with its two tool domains — inspection and transformation
    — assembled with no conformance workload and no business domain. One machine,
    unsigned, locally stored. The governed boundary contracts are declared and none
    is exercised.

    '
  required_domains:
  - platform
  - inspection
  excluded_domains: []
  declared_domains:
  - platform
  - inspection
  - transformation
  namespaces:
    form: <namespace>::<ARTIFACT_IDENTITY>
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
    - inspection
    - intent
    - lifecycle
    - runtime_binding
    - security_domain
    - structure
    - surface_contract
    - trace
    - transformation
    - transport
    - vocabulary
    - workflow
    closed: true
    derives_concern: false
    derives_authority: false
  declared_vocabulary:
    kinds:
    - kind: CONSTITUTION
      governance_assertion: required
    - kind: INVARIANT
      governance_assertion: required
    - kind: ASSERT
      governance_assertion: required
    - kind: STRUCTURE
      governance_assertion: required
    - kind: VOCABULARY
      governance_assertion: required
    - kind: SURFACE_CONTRACT
      governance_assertion: required
    - kind: CAPABILITY_CONTRACT
      governance_assertion: required
    - kind: CAPABILITY_TRANSFORM
      governance_assertion: required
    - kind: CAPABILITY_SIDE_EFFECT
      governance_assertion: required
    - kind: RUNTIME_BINDING
      governance_assertion: required
    - kind: WORKFLOW
      governance_assertion: required
    - kind: INTENT
      governance_assertion: required
    - kind: ACTOR
      governance_assertion: required
    - kind: EVENT
      governance_assertion: required
    - kind: TRANSPORT_INGRESS
      governance_assertion: required
    - kind: TRANSPORT_EGRESS
      governance_assertion: required
    aliases_accepted: false
  declared_outcomes:
  - succeeded
  - refused
  - not_applicable
  - failed
  result_classes: none — no boundary is exercised
  projections:
  - canonical_form
  - kind_index
  - identity_index
  - store_index
  trust_root: 'None. Evidence is self-asserted, and integrity is recomputed from constituent
    bytes at acceptance rather than compared against a recorded value. A checking
    party requiring more than self-assertion is not served by this platform. A derived
    profile may name a real root; this one does not, so that it does not oblige every
    derivation to have one.

    '
  evidence_retention: 'Indefinite. Evidence is written into the sealed snapshot and
    into per-run traces, and nothing removes either.

    '
  read_surface:
    openness: 'Nobody outside the system. Reads are issued by an operator tool on
      the same host; there is no caller class to admit because there is no caller.

      '
    reads_attributed: false
    reach: 'A local read tool run by an operator against the assembled snapshot on
      the same host. It reads projections and never internals.

      '
  sufficiency_criterion: 'A design is sufficient when every fact construction needs
    is fixed by a declaration rather than supplied at build time. Construction refuses
    — it does not fill, default, or infer — where a required field is unfixed, and
    the refusal names the field and the phase that should have fixed it.

    '
  interaction_forms_governed: not_applicable — no boundary is exercised
  protocol_bindings_governed: not_applicable — no boundary is exercised
  genesis_discharge: 'Recomputing the snapshot''s integrity from constituent bytes,
    and the composition conformance rules passing over the whole. The externality
    demonstration is NOT discharged: this profile was authored by the same authority
    that built the system it governs, so the genesis claim fails on that point and
    is recorded as failing.

    '
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
      # Execution semantics — what a workflow is and how it is bound and run. Required
      # even with no workload composed: the surface must be able to govern one.
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
      # Inspection boundary — inspection is a required domain (§1), so the operations
      # that make a snapshot answerable about itself are named here rather than left to
      # an unenforced key. Each is an ingress/egress pair; absence of either half means
      # the operation is not composed.
      - inspection::TI_SI_CATALOG_V0
      - inspection::TE_SI_CATALOG_V0
      - inspection::TI_SI_SNAPSHOT_SUMMARY_V0
      - inspection::TE_SI_SNAPSHOT_SUMMARY_V0
      - inspection::TI_SI_SNAPSHOT_VALIDATE_V0
      - inspection::TE_SI_SNAPSHOT_VALIDATE_V0
      - inspection::TI_SI_ARTIFACT_SHOW_V0
      - inspection::TE_SI_ARTIFACT_SHOW_V0
  required_domain_profiles:
  - domain: platform
    claims: authority
  - domain: inspection
    claims: concern
  - domain: transformation
    claims: authority
  required_self_description:
    manifest_declares_profile: true
    manifest_declares_identity_coverage: true
    covered_set_excludes_the_value: true
  required_workloads:
    entry_workflows: []
  required_claims:
  - SNAPSHOT_IMMUTABILITY
  - DETERMINISTIC_EXECUTION
  - COMPILED_INVOCATION_RESOLUTION
```

## 2. Required governance artifacts

A profile references governed identities — namespaces and artifact identities — and never filesystem
paths, repository names, or module paths.

§1 names thirty-six identities in four platform groups and one inspection group. The test applied to
each was not "is it present in the current build" but **would its absence mean this is not a
governance surface**.

**Constitutional core** — the authority chain a governed artifact resolves against. Without these
nothing in the snapshot can say what authorizes it.

**Execution semantics** — what a workflow is, how a capability is contracted, bound and traced. These
are required even though this profile composes no workload. A governance surface that cannot govern a
workflow is not this platform; the obligation is on the surface, not on any workload being present.
This is the substantive difference from a profile that requires an entry workflow: the *capacity* is
required, the *instance* is not.

**Governed boundary** — admission and egress as first-class contracts, declared whether or not any
boundary is exercised.

**Structural bootstrap** — how the surface is discovered, identified and dispatched. `STRUCTURE_DISCOVERY_V0`
is the one artifact whose absence halts a build before any other check can run.

**Inspection boundary** — `inspection` is a required domain in §1, and `required_domains` is not a key
any assembler verifies today. Naming four inspection operations here puts that requirement somewhere
that is checked. Each is named as an ingress/egress pair, because a half-composed operation is not a
composed operation. The four are the ones that make a snapshot answerable about itself: what it can
answer, what it contains, whether it is internally sound, and what a given identity resolves to.

What is deliberately **not** required: the remaining fourteen inspection operations, every workload
identity, and every business-domain identity. A snapshot may carry any of them and still conform — a
profile states what a snapshot SHALL satisfy, not an inventory of what a build contains.

## 3. Additional obligations

Three obligations beyond §1's selections. Each names what would establish a breach, so that none of
them is satisfied by construction.

**GS-1 — Governance closure agreement.** Every domain in the snapshot other than `platform` records
the governance closure it compiled against, and that closure resolves to the platform composed in the
same snapshot.

*Breach:* a domain whose recorded closure names a governance set absent from, or differing from, the
platform in this snapshot. A domain compiled against one governance surface and sealed beside another
is the failure this obligation exists to catch, and it is not visible from artifact counts.

**GS-2 — One authored copy per identity.** An identity published in more than one domain SHALL NOT
diverge in authored content. A domain carrying an imported capability carries its execution binding;
that binding is not a second authoring of the identity, and the identity resolves to the authoring
copy.

*Breach:* two canonical artifacts sharing an `fqdn_id` whose authored content differs, or an index
entry resolving an identity to a copy that is not the authoring one.

**A composition satisfying this profile satisfies GS-1 through GS-3.** A composition that admits a
capability-consuming domain does not: each such domain emits its own execution binding beside the
platform's authoring copy, and the index resolves the identity to whichever sorts last. The reference
composition breaches GS-2 on every one of its six side effects. This profile's own composition does
not, because inspection declares boundary contracts and consumes no capability — so the obligation is
in force and currently met, rather than in force and quietly failing.

The distinction matters for anyone deriving from this profile: adding a workload or a business domain
puts GS-2 at risk, and the profile is where that consequence is recorded.

**GS-3 — No dependency on what is not composed.** No artifact in a required domain SHALL reference an
identity in a namespace this profile does not declare. A governance surface that composes no workload
must not presuppose one.

*Breach:* an outgoing reference from a `platform` or `inspection` artifact to a workload or
business-domain namespace. This is the obligation that gives the composition its meaning: without it,
"assembled with no conformance workload" describes a build rather than a property.

## 4. Claims and their discharge

§1 names three claims. Each is stated below with its discharge class from `7a` §7, what discharges
it, and a demonstration capable of failing (CD-4).

**SNAPSHOT_IMMUTABILITY** — no behavior enters at execution time that was not present at build time.

*Class:* **structural**, with a derivational component. The claim is of the form *X cannot occur*, and
`7a` §7.2 is explicit that observation cannot substitute: a snapshot that admits ungoverned content is
satisfied on every run that does not exercise the path.

*Discharge:* examine the sealed representation for any admitted path by which behavior enters after
sealing, and re-derive the manifest `composite_hash` from the constituents it covers.

*Demonstration capable of failing:* place a constituent in the snapshot that the manifest does not
enumerate, and require refusal at acceptance. A realization that boots regardless has failed the
claim. This demonstration does fail as intended in the reference realization — an unenumerated file
is refused under 3b §6.

**DETERMINISTIC_EXECUTION** — the same snapshot and payload produce the same result and the same
graph addresses.

*Class:* **derivational** for the addresses, **comparative** for the execution.

*Discharge:* re-derive each domain's `graph_address_hash` from its constituents and compare with the
recorded value; and substitute what must not matter — a second environment, a second runtime — and
compare governed consequences.

*Demonstration capable of failing:* recompile from unchanged sources and compare addresses; a
nondeterministic projection yields a different hash. **The comparative half is not discharged.** Per
`7a` §7.3, a subject exercised in one configuration has not been comparatively discharged however
thoroughly that configuration was tested, and the reference realization has been exercised on one
operating system, one interpreter version and one runtime. This is a limit of the evidence, not a
finding against the system.

**COMPILED_INVOCATION_RESOLUTION** — operation identity resolves to a governed executable target at
compile time; nothing is routed at runtime.

*Class:* **structural.** The claim is that dynamic routing *cannot* occur.

*Discharge:* examine the compiled representation for any path from an operation identity to a target
resolved after sealing.

*Demonstration capable of failing:* declare an operation whose target identity is absent from the
composition, and require the failure to occur at compile or assembly. A realization that seals such a
snapshot and fails only when the operation is invoked has routed at runtime, and has failed the claim
irrespective of the error it eventually produced.

## 5. Externality

NP-7 requires a profile to be external to what it governs, and **externality is authorship, not
storage**. A profile written by the authority that builds the system is not external, whatever
directory it is kept in.

**This profile is not external to what it governs.** It was written by the authority that builds the
reference realization, and moving it between repositories does not change that. A conformance claim
made under this profile by that same authority therefore carries an unmet externality condition, and
must record it as a finding against the claim (`7b` CD-14).

This does not weaken the obligations in §§2-4, which are stated in terms a second party can evaluate
without the author's cooperation: identities resolve or they do not, references cross a namespace
boundary or they do not, a re-derived hash matches or it does not. What externality is missing from
is the *claim*, not the *contract* — and the remedy is a profile authored by a party that did not
build the system, not a rewording of this one.

## 6. Scope rules

- Profile scope changes are new identities (`_V0` → `_V1`), never in-place edits (NP-9).
- A profile that has not been read against a candidate snapshot MUST NOT be handed to anyone as a
  target. Running the check is a precondition of use.

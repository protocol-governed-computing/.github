# Normative Platform Profile NPP-D

## 1. Identity and purpose

- Profile identity: `NPP-D`
- Governing family revision: `14d54013494da27e43362d29ce15059c6fce5f21`
- Profile subject: a single governed system that accepts one sealed snapshot and executes it against governed state.
- Intended use: an independently reviewable, single-tenant, non-replicated system with required governed inspection and no external protocol boundary during the claimed profile scope.

This profile is a narrowing selection under Part VI. It is not a platform inventory, a reference realization, or a general-purpose platform description. Its commission-fixed scope is recorded separately in `list_assumptions.md`.

## 2. Selections and constraints

### 2.1 Governed system and execution

NPP-D selects one governed system, one active accepted snapshot, one governed state, and one applicable closure at a time. A second snapshot ends the first system instance rather than becoming concurrent state for the same claim. Execution is permitted only against the accepted sealed snapshot and governed state; ambient environment, prior evidence, and undeclared inputs are outside the governed input set.

**Source basis:** Conceptual Model §§3.3, 7, 8; Semantic Model §§3, 4, 8, 10; Snapshot §§1, 3, 9; Runtime §§2, 3; Architectural Invariants AI-1, AI-6, AI-10, AI-12, AI-15.

**Reason:** The profile's scope is a single sealed execution. Treating multiple active snapshots or ambient inputs as part of that claim would enlarge the subject rather than narrow it.

### 2.2 Interaction boundary

NPP-D selects no governed interaction boundary. No ingress, egress, external protocol adapter, or external protocol binding is part of the supported profile claim. This selection does not remove the governed inspection boundary.

Because no interaction boundary is selected, NPP-D supports no claim about interaction result classes, interaction-form elements, or external protocol bindings. Those deferred decisions do not bear on a claim this profile supports.

**Source basis:** Governed Interaction Boundary §§2, 5-10, 16; Normative Platform Profile §7; commission §2.

**Reason:** The commission fixes no external protocol boundary. The profile records that exclusion without treating it as permission to bypass obligations that remain, especially inspection.

### 2.3 Governed inspection

Inspection is selected and required. The read surface is reached by direct in-process invocation by the evaluator or by direct read access to the sealed representation and its governed projections. It is not reached through an interaction boundary or a wire protocol.

NPP-D selects an open read policy: every caller class may issue every declared read operation, subject to the system's per-read governed determination. Openness is a policy selection, not a waiver of authorization, refusal, evidence, or malformed/unreadable-input handling.

Every system under NPP-D must be able to answer what it contains, what governs a named subject, what it determined, and what it is. A read operation must answer about a named artifact and must not execute, mutate state, fall back, or return a client-computed answer as the system's answer.

**Source basis:** Governed Inspection §§2.1, 3, 4, 6, 8-11; Normative Platform Profile §7; commission §2.

**Reason:** Direct reach is the narrowest declared means compatible with a system having no interaction boundary, while the open policy makes the profile decision explicit without removing the determination required for each read.

### 2.4 Evidence trust root and retention

For claims under NPP-D, the evaluator accepts as the sole profile trust root the externally authored NPP-D document identified by the profile identity and the named family revision. An attestation chain that does not terminate in that identified profile document, or in a trust assertion explicitly made by the evaluator from it, is not accepted for an NPP-D claim.

Evidence for every determination and execution must be retained for the entire lifetime of the relevant system instance and until the instance's profile claim is withdrawn or superseded. Evidence for a withdrawn or superseded claim remains retained for later checking; NPP-D does not authorize deletion of evidence produced for a claimed instance.

**Source basis:** Evidence, Attestation & Provenance §§3, 6.2, 10, 11, 12; Normative Platform Profile §7.

**Reason:** The family deliberately leaves trust roots and retention to profiles. NPP-D chooses one externally identifiable root and indefinite claim-level retention so a past profile claim remains checkable.

### 2.5 Namespace

NPP-D selects one flat namespace, named `npp-d`, for resolving identities in the profile scope. It has no hierarchy and no implicit namespace fallback. Namespace membership carries identity resolution only; it does not establish authority, concern, ownership, or federation.

**Source basis:** Identity & Addressing §§5, 6, 8; Normative Platform Profile §7.

**Reason:** A single flat namespace is a narrower, deterministic arrangement for this single-system profile and avoids treating namespace structure as governance.

### 2.6 Projections

NPP-D selects the following projections only: a canonical form of the accepted snapshot and an evidence view derived from the evidence record. Neither is an authoring surface. No other projection is required by NPP-D, and a system may carry no additional profile-selected projection.

**Source basis:** Projection §§2, 3, 9-12; Governed Inspection §7; Normative Platform Profile §7.

**Reason:** These two projections are directly relevant to sealed execution and independent inspection. The profile does not require an index, structural rendering, or address-resolved form merely because those projections could be useful.

### 2.7 Capability outcomes

For capability contracts admitted under NPP-D, the profile selects the closed outcome vocabulary `success`, `failure`, and `refusal`. Each contract must enumerate which of these outcomes it admits and must declare outputs for each admitted outcome. `refusal` is a capability result only and is not a governance refusal.

NPP-D admits no outcome outside this vocabulary. A contract that needs a different domain result is outside this profile unless a successor profile with a new identity narrows and names that result vocabulary.

**Source basis:** Capability §§3, 3.2, 4; Execution Model §§4, 5; Normative Platform Profile §7.

**Reason:** Capability outcomes are a profile-deferred interface choice. This finite vocabulary supports both successful and unsuccessful execution without redefining the family distinction between capability results and governance refusals.

### 2.8 Sufficiency

For NPP-D, a design is sufficient only when it fixes, before realization, every fact required to realize the admitted system: identity and version; exactly one admitted kind and its contract; governance assertion; closed references; snapshot constituents; profile identity; governed state inputs; capability inputs, outputs, outcomes, and effect dispositions; selected read operations and their answer shapes; projection sources and derivations; and evidence subjects and closure information.

Any missing, ambiguous, unresolved, or fallback-resolved item makes the design insufficient. Realization must refuse it and must produce nothing from it.

**Source basis:** Governed Transformation §§13, 16; TR-5, TR-8, TR-9, TR-17, TR-18, TR-21; Machine Block §§4-11; Capability §3; Governed Inspection §4; Projection §3; Normative Platform Profile §7.

**Reason:** The family delegates the sufficiency criterion to the applicable profile. NPP-D chooses a total criterion aligned with the facts the selected facilities require and makes absence a refusal rather than a default.

### 2.9 Kind vocabulary

NPP-D closes the following profile vocabulary. These names are profile selections, not kinds required by the family:

| Kind | Declares | Semantic category | Governance assertion |
|---|---|---|---|
| `npp-d-snapshot` | the sealed snapshot representation, its constituents, profile identity, and snapshot identity | governed representation | required for ordinary admission |
| `npp-d-read-operation` | one named inspection operation, its class, inputs, answer shape, and governed target | declaration of a governed boundary | required for ordinary admission |
| `npp-d-evidence-record` | the evidence of one determination or execution, including closure, rules, result, subject, and snapshot identity | governed representation | required for ordinary admission |
| `npp-d-governance-root` | the profile-scoped governance assertion identifying the applicable external governing selection | governance declaration | required for ordinary admission |

Every machine block must carry exactly one of these canonical kind discriminators. The vocabulary has no aliases, no implicit kinds, and no unregistered-kind pass-through. Each admitted kind must have a declared kind contract and registry binding; the table states the governance-assertion disposition required by KV-10. Rules, registers, and check kinds are not artifact kinds and are not added to this vocabulary.

**Source basis:** Kind Vocabulary §§2-6, 9-11; Machine Block §§4-11; Governance Semantic Ontology §8; Governed Transformation §5; Normative Platform Profile §7.

**Reason:** The family leaves enumeration to profiles and requires closure. NPP-D uses only artifact roles named by the family and gives each a separate contract and governance disposition; it does not claim that these are family-wide required kinds.

### 2.10 Genesis

NPP-D excludes genesis and supports only systems whose claimed snapshot is inherited from a named prior governed baseline. Consequently, the profile supports no genesis claim and does not select genesis fixtures or a genesis discharge.

**Source basis:** Normative Platform Profile §7; Governed Transformation §12; Conformance Test Specification §9; commission §2.

**Reason:** Excluding first-snapshot constitution keeps the profile's supported claim set evaluable without inventing proposal, authorship, and baseline fixtures that this profile does not possess.

## 3. Additional obligations

NPP-D declares no obligations under Part VI §5 beyond the selections and parameterizations above. The profile's retention, trust-root, namespace, outcome, projection, reachability, openness, sufficiency, and vocabulary requirements are profile decisions, not additional requirements. Declaring them again as additional obligations would merely restate the profile contract and would not identify a new breach condition.

## 4. Supported claims and discharges

NPP-D supports the following claims:

| Claim | Subject | Discharge class | Required demonstration |
|---|---|---|---|
| NPP-D-P | this named profile | structural and derivational | Establish the identity, revision, selections, closed vocabulary, and absence of widening or redefinition from the profile text and its source bases. Failure is any missing identity, open deferred item bearing on the claim, incompatible meaning, or family-forbidden permission. |
| NPP-D-S | one system instance under NPP-D | all applicable subject classes plus composition obligations | Discharge each class represented by the accepted snapshot and the composition as required by Conformance Model §§3.1, 7, and 8. The claim must include structural absence demonstrations for forbidden paths, observational demonstrations for applicable refusals and executions, comparative demonstrations only where the obligation requires invariance, and derivational demonstrations for identities, closures, paths, projections, and evidence. |
| NPP-D-I | the inspection boundary of one NPP-D system instance | structural and observational | Establish direct reachability of the declared read surface, named-artifact answering, non-execution, no mutation, no fallback, and governed determination of reads. Failure is any executable path from reading, any ungoverned read, an empty success for malformed/unreadable material, or an answer assembled by the caller and held out as the system's. |
| NPP-D-E | evidence and attestation supplied for one NPP-D system instance | derivational and structural | Re-derive the determinative content from supplied evidence, verify its snapshot and subject identity, verify provenance, and verify that every attestation chain terminates in the selected NPP-D trust root. Failure is an unestablishable closure, missing subject/snapshot, non-terminating chain, or determinative mismatch. |

Every demonstration must state one obligation, subject, discharge class, showing condition, failure condition, and identified fixture. Negative claims require violating fixtures and absence claims require a stated total search space. NPP-D does not invent a test harness or an oracle; where the family does not supply enough detail to construct a demonstration, the corresponding matter remains in the findings register and the affected claim is not claimed as independently dischargeable.

## 5. Exclusions

NPP-D excludes systems with multiple active snapshots, replicated governed state, more than one tenant or authority boundary within the claimed scope, an external protocol boundary, a non-family trust root, undeclared environmental or historical inputs, an open or fallback kind vocabulary, an interaction-boundary claim, a genesis claim, or a read surface that cannot be reached directly as specified above.

It also excludes any system that relies on a namespace to establish authority, uses a profile decision to relax a family refusal or invariant, or introduces a facility without a home in the family.

## 6. Conformance boundary

NPP-D is external to any system claiming it. A claiming system may carry or read the profile, but it may not author, alter, or control the profile obligations. A change to any obligation, selection, parameter, vocabulary entry, or supported claim requires a new profile identity under Part VI §9.

The profile is a narrowing document. It does not claim that the family requires its selected kinds, outcome names, namespace, retention period, trust root, projections, or sufficiency criterion. Those are profile decisions, and their provenance is recorded in `decision_ledger.md`; unresolved source gaps are recorded in `findings_register.md`.

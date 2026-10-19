# NPP-E - Normative Platform Profile

## 1. Identity and purpose

- **Profile identity:** `NPP-E`.
- **Family revision:** `14d54013494da27e43362d29ce15059c6fce5f21`.
- **Profiled system:** one sealed, executable governed system with one tenant, no replication, no
  external protocol boundary, and a required inspection surface.
- **Purpose:** to constitute and operate a single-tenant, non-replicated governed system whose
  sealed snapshot, declarations, execution, transformation history, and inspection answers can be
  independently checked.

This is a platform profile, not an inventory of one realization. It selects facilities and
constraints under which a system may claim this profile. The profile is authored outside any system
that claims it, as required by `6a` §6 and `SN-7`.

## 2. Selected facilities and exclusions

The profile selects governed construction, sealing, execution against one accepted snapshot,
governed transformation, supersession, evidence, and governed inspection. It selects no governed
interaction boundary and no external protocol binding. Selecting no interaction boundary does not
remove inspection; the read surface is reached independently as required by `5b` §2.1.

The profile excludes replication, multi-tenant composition, federation, and any external protocol
boundary within the profiled system. It also excludes any system that requires an ambient source of
behavior, an unsealed or partially accepted snapshot, an undeclared effect path, or an inspection
path that invokes execution.

These are selections and scope limits, not exemptions from family obligations. All selected
facilities remain subject to the family invariants.

## 3. Closed artifact-kind vocabulary

NPP-E closes the following vocabulary for the system. The canonical kind names below are the sole
authoritative discriminators. The vocabulary is named `NPP-E.artifacts`, and its revision is tied
to this profile identity and family revision.

| Canonical kind | What the artifact declares | Semantic category | Ordinary governance assertion |
| --- | --- | --- | --- |
| `constitution` | root governance that constitutes the system | Normative | omitted only at genesis; required otherwise |
| `governance-element` | a governing element and its declared relations | Normative | required |
| `workflow` | workflow, steps, outcomes, and routing | Operational | required |
| `capability-contract` | inputs, outputs, outcomes, and effect disposition | Contractual | required |
| `read-operation` | an inspection question, class, answer, and refusal behavior | Contractual | required |

The set is derived from artifact-bearing subjects expressly named by the family: a constitution and
capability contract are artifacts (`1a` §3.1 and §6), workflows and capability contracts are
artifacts (`1a` §3.1), and every read operation is a declared artifact (`5b` §4). A declaration
element such as a register, rule, or outcome is not given a kind merely because it is structured
(`2c` §7.1 and `4d` §5); it remains part of its owning artifact.

No alias is accepted. Every block carries exactly one canonical kind name. Unknown, duplicate, or
unregistered kinds are refused. Each kind contract is closed, every element has one owner, role,
and construction disposition, and every kind-specific contract is bound in the declared registry.
The vocabulary states the governance-assertion disposition for every admitted kind; no kind may
omit it outside genesis.

NPP-E does not admit interaction-boundary kinds, domain-specific kinds, environment-specific kinds,
replication kinds, federation kinds, or attestation-authority kinds. A future addition requires a
governed vocabulary revision and a new profile identity; it is not admitted by discovery.

## 4. Outcomes and capabilities

Every admitted capability contract uses the closed outcome vocabulary:

- `completed` - the declared operation completed and its declared outputs are available;
- `failed` - the declared operation completed with its declared failure outputs or failure state.

Neither name is a governance refusal. An undeclared result or an unrouted outcome produces a
governance refusal and is never routed as an outcome. Capability contracts are either `effecting`
or `non-effecting`; a non-effecting capability has no direct or transitive effecting path.

The two-outcome selection keeps failure explicit while leaving governance refusal distinct. It
narrows the open outcome vocabulary; it does not alter outcome semantics (`3a` §4 and `3d` §3.2).

## 5. Projections carried by the snapshot

NPP-E requires these projections, each with a declared source, selection, deterministic derivation,
and provenance (`4b` §3.1 and §13):

1. **Canonical form:** normalized semantic objects of all admitted artifacts and the profile claim.
2. **Identity index:** every admitted artifact identity, including individually addressable reads.
3. **Address-resolved form:** all references required by construction and execution resolved before
   execution.
4. **Structural rendering:** complete executable workflow structures, routing, bindings, state
   transitions, and effect surfaces.
5. **Vocabulary view:** the closed vocabulary, registry bindings, categories, provenance, and
   governance-assertion dispositions.
6. **Evidence view:** retained evidence and provenance information arranged for inspection.

These are the projection realizations named by `4b` §10. No projection is authoritative over its
source, no projection is edited, and regeneration from the named source must produce the same
determinative content.

## 6. Identity, namespace, and addressing

NPP-E selects one system-wide namespace, `NPP-E.system`, for all admitted artifact identities. It
has no subordinate or ambient namespaces. Identities are declared on artifacts and are globally
unique within the admitted system; references use declared identity only. Addresses used to reach
representations are not identities, are not authority, and do not affect identity.

The profile selects canonical semantic-object normalization for identity and integrity. The exact
identity value is recomputed from the canonical semantic object; it is never assigned, inherited,
or derived from a path, filename, location, or prefix. No alias or short-name fallback is used.

## 7. Evidence, attestation, and retention

NPP-E requires evidence for every determination, including admissions, refusals, closure failures,
construction, transformation, snapshot acceptance, execution, and inspection. Evidence identifies
the sealed snapshot and determination subject, carries the applicable closure and rules, records
predicate results and the dominant consequence, and distinguishes determinative from observational
content.

For this profile, the integrity value over canonical semantic content is a SHA-256 digest. The
whole-integrity value covers the declared constituent set excluding the value itself. This is a
profile parameterization of the integrity mechanism left open by `3b` §6 and §13; it does not make
the digest an authority.

The profile's trust root is the externally published artifact identified as profile `NPP-E` at this
family revision. A checking party accepts that exact profile artifact as the root for evaluating
profile obligations. No attestation beyond the family requirements is required. An optional
attestation is usable only when its chain terminates at that named root.

Evidence and retained canonical records are retained for the lifetime of the system and for ten
years after system retirement or supersession of the final snapshot. Mechanism deletion does not
occur on supersession.

## 8. Inspection policy and reachability

The read policy is open to every caller for every declared read operation. This is an intentional
policy selection, not permission to skip a determination: each read still undergoes the applicable
governance determination and produces evidence (`5b` §11).

Reads are attributed to the identified caller. Attribution is observational and must not become an
authority or alter the answer. The surface provides named-artifact lookup, artifact enumeration,
closure lookup for a named subject, determination/evidence lookup, and snapshot identity,
constituent, and profile lookup (`5b` §10).

Because NPP-E selects no interaction boundary, the read surface is reached by a declared in-process
inspection interface directly over the accepted sealed representation and retained evidence. It is
not reached through an operation identity or capability. The interface returns the system's answer,
not raw material requiring the caller to derive it. Malformed, unreadable, absent, or unanswerable
requests are refused rather than answered empty. Inspection changes no governed state, invokes no
executable target, and reads no construction or runtime internals.

## 9. Transformation sufficiency and genesis

NPP-E selects a binary sufficiency criterion. A transformation is sufficient only if, before
realization:

- every fact required by the declared realization schedule is fixed in addressed register fields;
- every blocking question is resolved and no question is guessed or hedged;
- claims about the existing system are grounded against the named frozen baseline;
- every requested artifact is realized exactly once, every realized artifact traces to a request,
  and dependency ordering is gapless;
- amendments are whole redeclarations that do not narrow what they replace; and
- human semantic content is preserved in both directions.

If any item is absent, unresolved, contradictory, ungrounded, duplicated, omitted, or not
addressable, realization refuses before writing a usable artifact. Quality scores never gate this
criterion. A design that passes may still be inadequate to business intent; that is a separate
determination.

For genesis, NPP-E fixes the discharge fixtures as: the identified genesis proposal, the sealed
`NPP-E` profile artifact, the external authorship/control record for that profile, the resulting
first snapshot, and its acceptance evidence. The genesis claim must establish both self-consistency
of the proposed baseline and satisfaction of NPP-E; the profile authorship check must establish
that the claimant did not author or control the profile.

## 10. Additional obligations

NPP-E adds no independent additional obligation under `6a` §5. Its narrower selections and
parameterizations are sufficient to distinguish systems claiming this profile. Every family
obligation remains in force.

## 11. Supported claims and discharge

Every claim must identify its claimant, subject, profile identity, and family revision (`7a` §2).

| Claim | Subject | Required discharge |
| --- | --- | --- |
| Profile conformance | this profile | derivational review against `6a` and the registers, plus structural narrowing check |
| Vocabulary and declaration surface | vocabulary and machine blocks | derivational and observational checks, including unknown-kind and duplicate-identity refusals |
| Snapshot conformance | snapshot and acceptance | derivational identity/integrity checks and observational refusal of corrupted or incomplete snapshots |
| Construction and transformation | dossier and result | derivation, refusal fixtures, reproduction, preservation, grounding, sufficiency, and real-state proof |
| Runtime and execution | runtime and executions | observational refusals, structural absence checks, and independent-runtime comparison |
| Evidence | evidence records and history | derivational re-evaluation and structural authority/input checks |
| Inspection | read surface and operations | structural absence checks, refusal tests, and independent-client comparison |
| System instance | whole one-tenant system | all applicable constituent classes plus composition-wide demonstrations |

The profile supports no claim about external protocol neutrality, multi-environment equivalence,
replication, federation, domain authority, or business adequacy.

## 12. Excluded systems

A system cannot claim NPP-E if it has more than one tenant, replicates governed state, exposes an
external protocol boundary within this scope, uses a kind outside the closed vocabulary, accepts an
alias as authoritative, relies on an ambient input, lacks an independently reachable read surface,
derives answers in callers, permits inspection to execute, retains evidence for less than the
selected period, or cannot supply the stated genesis fixtures.

These exclusions are consequences of selected scope and parameters. They do not relax family
prohibitions.

## 13. Conformance of NPP-E

NPP-E has an identity, names the family revision, keeps commission scope separate in its scope
register, decides every deferred item bearing on its supported claims, introduces no facility with
no family home, and adds no unenforceable obligation. Its unresolved standard questions are listed
in `findings_register.md`; none is silently represented as settled by this profile.

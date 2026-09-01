# NOVA2 — Independent realization from the standard and a profile

NOVA1 asked whether a *minimal* profile could be authored and realized from the spec alone, across
three runs. NOVA2 asks the adoption question: **given the standard and a profile naming the target,
can a second party build a realization capable of governing arbitrary domains — without ever seeing
the reference?**

The worker receives no authored artifacts and no reference code. Kind vocabulary, constitutions,
invariants, capability declarations, the workload registry, and the entire toolchain are what the
worker produces. Where the standard does not determine them, that is the finding.

NOVA2 runs in phases, each gated on something that can fail. This document states the full scope,
then specifies **NOVA2A** — phase 1 — in full. NOVA2B and later are named here and specified
just in time, because the journey cannot be predicted and specifying it in advance would only
encode a guess.

## 1. The result the program is built to produce

The headline outcome is not conformance and is not snapshot identity. It is generality:

> **Given a governed domain the implementer has never seen, does their realization admit, compile,
> and execute it without any change to their toolchain?**

That is the claim "a realization of this standard hosts arbitrary domains" reduced to a one-shot
test. It is reached in the final phase; every earlier phase exists to get there with something worth
testing.

Two subordinate results are decided along the way:

> **R1 — Conformance.** Does the worker's snapshot exercise the profile's `required_governance`
> kinds, and do all its pinned identities resolve?

> **R2 — Behavioral equivalence.** Over the shared collatz payloads, does the worker's platform
> produce identical declared outcomes and equivalent emitted evidence?

**R1 is a requirements test, not a comparison.** The profile states that *"a profile states
requirements, never an inventory. A snapshot may contain more than the profile requires and still
conform"* (`§6`). A worker snapshot larger than the reference's, or differently partitioned,
conforms. The sealed reference commitment is context for adjudication, never the pass bar.

**Snapshot-id equality is explicitly not a test anywhere in this program.** Two parties who
independently author their declarations differ in naming and ordering long before they differ in
governance, and content-derived identity is sensitive to both. Requiring it would force the
reference registry into the worker's hands as an answer key, collapsing the program into a
canonicalization exercise and leaving authoring — the larger half of the standard — untested.
Convergence on canonical form is a separate question deserving its own trial and its own package.

## 2. Why the reference is withheld

Not to prevent cheating. To prevent anchoring.

The program's value is architectural independence: a realization that satisfies the profile with a
structurally different design proves the standard specifies governed behavior rather than the
reference's shape. Nothing else in the validation program can establish that.

This is a counterfactual regime and should be recorded as one. The reference realization is
published under a DOI; a real third-party implementer would read it. NOVA2 deliberately answers
*"is the standard sufficient?"* rather than *"is the standard plus the published reference
sufficient?"* — the second is the adoption question and is worth a later trial, but it cannot be run
first, because it cannot be un-run.

## 3. The phases

| | Phase | Deliverable | Gate |
|---|---|---|---|
| **2A** | Declaration surface and constitutional core | Declarations only. No code. | Authorable from standard + profile at all? |
| 2B | Determination | Declarations → validated projections | Does refusal actually refuse? |
| 2C | Sealing and identity | A sealed representation that identifies itself | Reproducible across their own rebuilds |
| 2D | Execution | Runtime + collatz | R2 — trace equivalence |
| 2E | Attestation and inspection | Evidence and a read surface | Claims discharge; removal test passes |
| 2F | **Generality** | A sealed domain the worker has never held | Admits with no toolchain change |

Each gate is a stopping point. A phase that fails ends the program with a finding rather than
proceeding on a defective foundation — that is the reason for phasing, and the reason a phase's
scope is drawn where something can fail.

**Each handover is self-contained.** If the worker is an AI instance, context does not survive
between phases. Phase N's package therefore consists of the original Package A *plus the worker's
own phase N−1 output* — the surface they designed, the artifacts they authored. Their prior work is
an input they must be able to read cold. This differs structurally from NOVA1's instruments, where
one run's context carried forward.

## 4. Roles

**Operator.** Assembles packages, seals commitments, records the regime in force, adjudicates gates.
Does not design.

**Virtual architect.** The standard's `8a_implementation_guidance` annex *is* the architect's brief.
It is written for an anonymous future implementer, not at this worker — a doc written to make this
worker succeed tests its own curation rather than the standard.

One rule governs its content and is auditable line by line:

> **It may name problems. It may not name solutions.**

Allowed: *a kind vocabulary must be resolvable before any artifact is classified — you have a
bootstrap ordering problem.* Forbidden: *the reference resolves this with `X`, which does `Y`.*

**Standing rulings during a run.** The architect answers a worker's questions without redesigning:
clarifying what a normative document requires, ruling on a misreading, unblocking. Every ruling is
recorded as a run-log entry against the frozen revision. **No ruling amends `8a` mid-run** — that
would move the family's revision identity while the trial's input is supposed to be fixed, and
findings could no longer be attributed to a revision. Rulings are folded into `8a` at the *next*
revision, after the run. That is the program's feedback loop: NOVA2A's questions become the next
revision's guidance.

## 5. Prerequisites — before NOVA2A

The order here is forced; steps 1 and 2 gate everything after.

1. **Augment `8a`.** Five additions: the declaration surface as the implementer's first decision;
   the problem inventory; the order of construction; the scope floor; falsification discipline.
   Worked on `draft/5`, per the working-name convention `revisions.md` records — a branch may not
   assert a revision identity that has not been declared (`4e §9`).
2. **Freeze and declare the revision.** `draft-5` → `v1` in `revisions.md`, tagged. NOVA2 hands over
   **v1**, not v0: v0's `8a` lacks the additions, and phase 2A is entirely authoring.
3. **Amend the profile to the uncomposed selection.** `platform`, `workload`, `inspection`,
   `transformation`; `ai_governance`, `blockchain`, `book_library_mgmt` excluded. Either an
   amendment or a successor superseding by declared identity (`4e §2`).
4. **Build the uncomposed PNP.** It does not exist. The working `snapshot/` and `pgc_release/
   snapshot` are both the composed 7-domain build (`REFERENCE_PLATFORM_PROFILE_V1`, snapshot id
   `72404ce4…` / release `4a1e8896…`).
5. **Seal the commitment.** Snapshot id, per-domain graph addresses, kind coverage, reference
   collatz traces. Context for adjudication. Not shared.
6. **Rule on the open questions** (§8).
7. **Reserve the phase 2F domain now.** A domain the worker will never see, sealed before 2A begins,
   so it cannot be shaped by what the worker turns out to find easy.
8. **Publish the findings taxonomy** (§7) before handover.

## 6. NOVA2A — phase 1

### 6.1 The task

Design a declaration surface, then author on it:

- **the kind vocabulary** — the profile's `declared_vocabulary.kinds`, declared as a closed set
- **the constitutional core** — the eight constitutional identities the profile pins under that
  heading, and whatever the standard requires to make them resolve

No compiler. No runtime. No code of any kind. The phase ends with declarations on disk and a
document explaining the surface.

The reason for drawing it here: the standard specifies the envelope semantically and declines to
encode it (`2c §3`, `2c §6.1` — *"not specified by this revision"*). No field name appears anywhere
in the normative set. So the very first thing the worker must do is invent something the standard
deliberately does not supply, and if that cannot be done from the standard plus `8a §4`, nothing
downstream is worth running.

### 6.2 Package A

**A1 — Standard.** `standards/spec/` at `v1`, all documents including the augmented `8a`. `VERSION`
and `revisions.md`.

**A2 — Profile.** The uncomposed profile. It names the target: admissible kinds, required kinds,
pinned identities. It does not say how to author anything that satisfies it.

**A3 — Instruments.** The phase 2A charter; run conditions naming the regime in force and the
honour-based input firewall (per NOVA1's `g0_handover.md §1`); the §7 taxonomy.

Nothing else. The collatz statement and payloads are phase 2D's package and are not handed over
now — they would invite the worker to design the surface around one workload.

### 6.3 Package B — withheld

| Withheld | Why |
|---|---|
| `software_governance/registry/` — 27 categories, constitutions and invariants | This is the authored platform. Handing it over is handing over the answer. |
| `software_governance/capability_transforms/`, `capability_side_effects/` | Declarations and behavior alike must derive from the standard. |
| `conformance_workloads/` in full | Out of phase scope; withheld entirely until 2D. |
| `**/snapshot/determinations/` | An admitted determination is a compiled result, not an input. |
| `ARCHITECTURE.md`, `README.md`, `VERSION` in the platform repos | These describe the reference's chosen arrangement, which `8a §2` says establishes nothing. |
| `protocol_compiler/`, `snapshot_assembler/`, `protocol_runtime/`, `snapshot_inspector/` | The toolchain is the worker's to produce — and its four-way split appears in no normative document. |
| `snapshot/`, `pgc_release/`, manifests, hashes, traces | Anchoring, and contamination of R1/R2. |
| **The Realization Map** | A direct normative-document → reference mapping. The sharpest anchoring vector in the dossier, and `8a §11` already holds it outside the family. |
| `.github/process/*.py` closure checks | These encode conformance judgments the standard should carry. Withholding tests whether it does. |
| `business_domains/`, `protocol_transport/` | Out of profile scope; `business_domains` also holds phase 2F's reserve. |
| Papers, NOVA1 materials, this document | Not standard; would leak intent and prior findings. |

### 6.4 Gates

Phase 2A passes if all four hold. None is a resemblance test; none can be satisfied by matching the
reference.

**G1 — The surface exists and is constrained correctly.** Identity, authority and concern are
separately expressible (`GO-11`). The envelope is closed against unrecognized elements (`2c §6`,
`§11`). Classification is declared, never derived from a name (`GO-3`, `MB-6`). Declared identity is
authoritative over filename, folder and position (`AI-2`). References are by declared identity
alone.

**G2 — The vocabulary is expressible and closed.** Every kind in `declared_vocabulary.kinds` can be
written on the surface, and the set is declared closed. Closure is *declared* here, not enforced —
enforcement is phase 2B.

**G3 — The constitutional core resolves.** The eight pinned constitutional identities exist as
declarations and resolve to one another by declared identity, with no unresolved reference and no
short-name or positional resolution anywhere.

**G4 — The bootstrap is answered.** The worker states how the first artifact is classified without
that classification requiring what it establishes, and the answer is not discovery, scanning,
convention, or reflection (`AI-12`).

### 6.5 Deliverables

1. The declaration surface, as a document: what it carries, what it forbids, and how each `8a §4`
   constraint is met.
2. The authored kind vocabulary and constitutional core.
3. A decision log: each choice the standard left open, what was chosen, and what bounded it.
4. A questions log: everything the worker could not resolve from the standard, whether or not it was
   ruled on.
5. A statement of what was not claimed and why.

### 6.6 Abort

If G1 fails, the program stops. A standard from which a declaration surface cannot be designed
cannot be implemented from, and phases 2B–2F would only elaborate the failure. That outcome is a
finding of the first order and is worth more than a partial run.

G2–G4 failing individually localizes to a document and may be ruled on rather than aborted — but a
ruling that supplies content rather than clarifying it is itself a finding against `8a`.

## 7. Findings taxonomy — published before handover

NOVA1 raised seventeen candidate findings and classified none as an undeclared gap. On this surface
that classification will be contested unless the rule is fixed in advance:

- **spec defect** — the worker could not proceed, or proceeded differently, because the standard does
  not determine the answer;
- **deliberately open** — the standard names the decision as the implementer's, `8a §4` and `§5`
  included;
- **permitted architectural variance** — the standard determines the governed property, the worker
  obtained it by another mechanism, and the divergence is confined to mechanism;
- **worker error** — the standard determines it and the worker read it wrong.

The third class will do the most work and is the easiest to abuse after the fact. Its boundary is
fixed before the run, against the standard — never against the worker's output.

## 8. Rulings required before handover

**Transport.** The profile's `declared_vocabulary` admits `TRANSPORT_INGRESS` and `TRANSPORT_EGRESS`
and its `required_governance.artifacts` pins four transport constitutions — while this program
exercises no external effect and withholds `protocol_transport/`. The uncomposed amendment must rule:
declare the boundary contracts without exercising a boundary, or drop them from the required set.
Unruled, phase 2A has the worker authoring constitutions for a surface no later phase reaches.

**Self-reference.** The uncomposed selection includes `transformation` — the machinery by which the
platform changes itself. A profile may not be authored by the system it governs. Decide explicitly
whether the profile is authored outside that surface, and record the reasoning. Cheaper to settle
now than to defend afterward.

**Variance boundary.** Which properties of an authored declaration are identity-bearing for R1, and
which are permitted variance. If the standard does not already answer this, record that as a pre-run
finding rather than settling it by fiat.

## 9. Known limits

- **Single worker.** Use a different model than NOVA1's, or the single-worker limitation is
  unchanged and no cross-worker comparison exists.
- **Honour-based firewall** for an external party. Record which regime was actually in force, not
  which was requested.
- **Cross-revision incomparability.** NOVA1 ran against `v0`; NOVA2 runs against `v1`. Findings from
  the two are against different revisions and are not directly comparable. They answer different
  questions, so this is a limit on aggregation, not on either result.
- **Counterfactual regime.** Withholding a published reference is not how adoption happens (§2).
  This program answers sufficiency of the standard, not sufficiency of the standard in the world.
- **No external effect** is exercised anywhere in the program; the profile selects no interaction
  boundary.
- **Phase 2F proves generality over one unseen domain**, not over all domains. A pass is strong
  evidence and not a proof; a failure is decisive.

## 10. Revision policy

The standard is developed against real use. NOVA2's design has already functioned that way: `8a` was
augmented because specifying phase 2A exposed that the annex named no problems an implementer would
actually face. That loop is legitimate and should continue. It is legitimate only in one of the
three windows below.

| Window | What may change | Why |
|---|---|---|
| **Before freeze** | Anything. Normative documents included. | The program's design is itself a use case, and a defect found now costs nothing. |
| **During a run** | Nothing. Rulings only. | Amending in response to what the worker hits erases the finding: close the gap and you can no longer say the standard was insufficient. `8a §2` — *"the disagreement is resolved by ruling — never by editing the document to match what was built."* |
| **Between phases** | Nothing. | See below. |

**One revision for all of NOVA2.** Phases 2A–2F run against a single frozen revision. Fixing findings
between phases would run each phase against a different revision, and the program's results would
stop aggregating into one statement about one standard — the headline result at 2F depends on every
phase before it, and would become uninterpretable. Findings accumulate and become the *next*
revision. The cost is running later phases against text already known to be defective; that cost is
accepted deliberately.

The one exception is an abort. If a gate fails at abort level (§6.6), the program ends. Fixing the
findings, declaring a new revision, and running again is a new run — not a mid-run amendment.

**Normative and non-normative move differently.** `8a` is non-normative and says outright that it
will age; it may be reworked freely between runs. A normative document changes what conformance
means, and prior results were obtained against prior revisions — those changes take `4e`'s
supersession discipline and a declared revision identity, never an in-place edit.

### 10.1 What makes this checkable by someone else

Each element below is an artifact an outside party can inspect directly, without relying on the
operator's account of it. The point is not to answer a challenge; it is that a process whose
integrity rests on the operator's own testimony has not established it.

- **The revision is tagged before handover.** The tag's commit precedes the run's first exchange.
  Anyone can compare the two.
- **The handover package is recorded by content hash.** What the worker received is then verifiable
  rather than described. This matters more than any other item here, because every claim about what
  was withheld reduces to it.
- **The ruling log is append-only**, entry by entry: what was asked, what was answered, which
  document it concerned. An auditor reads it and forms their own view on whether any ruling supplied
  content rather than clarifying it — which §6.6 already classifies as a finding against `8a` rather
  than a normal unblock.
- **The revision diff is published when the run closes.** A change to any normative document dated
  inside the run window is a contamination event, visible in the diff whether or not anyone declares
  it. Publishing the diff is what makes concealment require an act rather than a silence.
- **Findings are dated after the run and against the frozen revision**, so a finding cannot be
  quietly reclassified once its fix is known.

### 10.2 The part this policy does not fix

The input firewall is honour-based. No tagging, hashing, or logging establishes that an external
worker did not consult the published reference — which is public under a DOI and findable by name.
The regime in force is recorded (§9), and the recording is a statement about intent, not a control.

It is stated here because it is true, not to pre-empt the objection. Where the firewall matters
most is phase 2F, where the reserved domain is withheld from every party until the phase opens —
that one *is* enforceable, because it is withheld rather than merely not-consulted.

**If contamination occurs, it is declared and the affected result is withdrawn.** A run continued
after known contamination produces a claim about nothing, which is worth less than the phase it
would have cost to drop.

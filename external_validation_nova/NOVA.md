# NOVA — a realization of PGC standard

**Codename NOVA.** An independent PGC realization built from the published standard by a worker with
no knowledge of the reference implementation, to answer two questions at once: *is the standard
sufficient to build from*, and *can a PGC system govern its own evolution*.

NOVA is not a rewrite. The reference realization is the control; NOVA is the second sample. Their
disagreement is the evidence.

## What is under test

| | Proposition |
|---|---|
| **G0** | An independent author can produce a valid `6a` profile from the standard alone. |
| **G1** | The experiment itself can be governed before it is run. |
| **G2** | An independent realization can be built from standard + profile alone. |
| **G3** | Two independent realizations can discharge the same conformance claim. |
| **G4** | A PGC realization can govern its own evolution by transformation, not rebuild. |

## Gates

Each gate produces an artifact and a finding set. **No gate starts until the one before it has
both** — otherwise the next gate silently converts a finding into a design decision.

- **G0 — Independent Profile Authoring Commission.** The clean `6a` profile is an unproven
  prerequisite, not preparation. Neither existing candidate qualifies: one is self-described as
  what the reference realization is developed against, which `6c` §1 forbids; the other is written
  in vocabulary the standard does not have. Output: an authored profile at a named revision,
  committed as an independent artifact, plus the ledgers below.
- **Revision freeze.** After G2's findings are dispositioned and repaired, before G3. See *The
  revision target* below.
- **G1 — Independent Realization Experiment Protocol.** **Written**, at
  `external_validation_nova/instruments/g1_realization_protocol.md`. Permitted inputs, firewall, provenance record,
  classification, success and failure criteria — fixed before G2 begins, so the validation exercise
  is not itself ungoverned. Its hard exit criterion is discharged: the normative basis for G2's
  claim is **disposition C**, and the claim is discharged as `7a` and `7b` specify — demonstrations
  with declared fixtures, including negative ones, obtainable by a party that did not build it.
- **G2 — NOVA.** Independent realization. Output: the system, its conformance evidence, and the
  registers.
- **G3 — Comparative conformance.** Reference and NOVA against the same profile and revision. Not
  source equivalence: `7a` §10 makes equivalence relative to profile and revision, never
  architecture. `7a` §7.3's comparative discharge classes and RT-12 are stated over exactly this and
  are currently unexercised. **The standard and the profile are the oracle. The reference and NOVA
  are two observations against it** — see *Reading a disagreement*.
- **G4 — Governed transformation.** NOVA's own baseline snapshot plus a purpose — add a business
  domain — through its own transformation semantics. The snapshot is the correct input *here* and
  contamination anywhere earlier. **Recorded, not required for this claim:** a later transformation
  performed by an operator who did not build NOVA would test the premise harder. G4 asks whether a
  realization can govern its own evolution, and the premise is that behavior travels in the snapshot
  while the runtime is replaceable. If a transformation needs the builder's memory, the governed
  state did not carry what evolution required — and only a different operator can show that. It is a
  stronger follow-on, not a condition of the current claim.

## Finding classes

Every decision a worker makes is classified after the run. This is what keeps the exercise from
degenerating into *the model made choices, therefore the standard is incomplete*.

| Class | The entry shows | Finding? |
|---|---|---|
| **0 — commissioner scope** | the commission fixed it, not the family | no, and no evidence either way |
| **1 — realization freedom** | the standard deliberately leaves it open | no |
| **2 — profile decision, specified** | the family delegated it and supplied enough | no |
| **3 — profile decision, underspecified** | delegated without enough to decide it | **yes** |
| **4 — ambiguity** | two readings, incompatible results | **yes** |
| **5 — omission** | no normative source at all | **yes**, serious |
| **6 — reference-shaped assumption** | needed something knowable only from a realization | **yes**, the most valuable |

**The worker does not classify; the commissioning side does, after the run.** A commission that
hands over the taxonomy answers Finding **A** in advance — the log then shows the commission works
and says nothing about the family. The one exception is the worker's own mark for an assumption it
could not trace, which is a different question and worth prompting for.

**Class 0 exists because run `NPP-C` lacked it.** Seven of that run's twelve class 2 entries cited
the commission as their authority. Without a class of their own, decisions the commission made read
as evidence the family delegates well, and the commission ends up measuring itself.

**The rule that makes it work:** every assumption affecting externally observable PGC semantics must
trace to a permitted input or be reported. Every choice that does not affect them must be explicitly
classified as realization freedom.

## The revision target

`7a` CF-1 requires a claim to name a revision, so NOVA needs an immutable target. It does not need
one yet.

**`draft-4` is the candidate fixed input for G0 — fixed for the trial, not yet frozen.** Freezing
before G0 risks discovering a G0-invalidating defect immediately after the revision is sealed;
leaving it open through G2 makes NOVA chase a moving standard. So:

```
draft-4 pinned  →  G0  →  G1  →  G2  →  repairs  →  freeze and tag  →  G3 claims against it
```

**The freeze comes after G2, not before G1.** CF-1 binds the *claim* — *"a conformance claim MUST
name its subject, its profile, its revision, and its claimant"* — and the claim is made at G3.
G1 and G2 need an immutable target, and a pinned commit already is one; all three G0 runs ran
against a pinned commit with no freeze. Freezing earlier would send every defect G2 finds into a
successor revision, when absorbing exactly those is what `draft-4` was opened for: its own record
lists **a second independent realization** among the things it is waiting for.

A finding that proves a normative defect is repaired in `draft-4` while it is open, and whatever
gate work it invalidates is repeated. A finding that turns out to be a profile-authoring or
realization matter occasions no repair.

**The rule, stated so the name is not what matters:** NOVA's target is *the first frozen revision
incorporating the terminology and ownership repairs, plus any G0 finding that proves a normative
defect.* That is very likely `draft-4`.

`draft-3` is a poor target and not because of its semantics — Change 1 altered no obligation, and
`1a` §14 binds documents rather than implementations, so a realization conforming to `draft-3`
conforms to `draft-4` unchanged. It is a poor target because NOVA consumes the standard as **build
input**, and `draft-3` is known to carry twelve untrue declarations, a term `1a` uses and does not
define, and one term defined twice. A cold worker meets those directly.

## Reading a disagreement

The reference realization is **not** the oracle. Where NOVA and the reference differ:

```
NOVA ≠ reference
   └─ within permitted realization freedom?
        ├── yes → not a conformance disagreement; record as Class 1
        └── no  → does the standard determine one result?
                   ├── yes → one realization has a defect
                   └── no  → specification ambiguity or omission (Class 3 / Class 4)
```

Disagreement triggers investigation. It is never by itself evidence that either system is wrong.

## Firewall

Permitted: the frozen `spec/` at a named revision; the normative conformance material; general
technical knowledge unrelated to the reference.

Prohibited: reference source, repo history, snapshots, architecture papers, prior implementation
discussion, existing profile candidates, and prior agent memory.

Contamination routes that have already bitten, and are guarded explicitly:

- a commissioning reply quoted back as normative text;
- the worker patching its own copy of the standard;
- profile *shape* leaking architecture even when it names nothing.

**One route is structural and no commission wording closes it.** The standard names its own subject,
so a worker that has read `1a` §4 can find an existing realization by searching for that name. The
prohibitions cover what is *offered* to a worker; they do not cover curiosity.

**Settled: network restriction, by the cheapest mechanism each gate allows.** The mechanism differs
because what the worker needs differs, and a single regime would either fail to bind G0 or make G2
impossible.

| Gate | The worker needs | Regime |
|---|---|---|
| **G0** authoring | to read `spec/` and write documents | **tool restriction.** No `Bash`, no web tools, no subagents. Reading and writing files is the whole task, so the network-capable surface can be removed outright rather than policed. |
| **G2** realization | to write, build, and run code | **environment isolation.** A worker that can execute can reach the network; nothing at tool level binds it. An offline container or VM, with dependencies staged in advance. |
| **G3, G4** | — | none. Run by the commissioning side with full context; there is nothing to protect. |

**G0 carries no residual worth stating.** A worker with no execution and no web tools has no route
to an existing realization, whatever it is curious about.

**G2's residual is the staging step.** Dependencies have to enter the isolated environment somehow,
and whatever carries them in is a channel. Stage them before the worker starts, from a manifest
fixed in advance, and record what was staged as part of the run.

What must not happen is assuming G0's guarantee covers G2. It does not: the gate that most needs
isolation is the one where tool restriction stops working.

## Who must be independent of whom

Independence is required at the boundaries a claim rests on, and nowhere else. Rotating workers
between gates for its own sake buys nothing and is not how any standards programme runs.

**Two boundaries, and only two:**

- **`NPP-E`'s author must not build NOVA.** `6a` §6 — externality is a property of authorship, and a
  system claiming a profile it wrote is the collapse the standard forbids.
- **NOVA's builder must not have had access to G0's findings**, nor to any excluded PGC material.
  G0's registers map the terrain G2 surveys; a builder told in advance where the standard's edges
  are will route around them rather than discover them.

**A single worker may perform G2 and G4.** No fresh-worker requirement stands between them. G4
transforms the system G2 built, and asking someone who has never seen it to do so tests nothing G4
is about.

**G3 is not a worker task.** It is a commissioning-side comparative evaluation — two systems'
discharge against one profile, read by the party that commissioned both. Like the classification of
G0's registers, it is done with full context because there is nothing to protect.

The real-world separation this mirrors is **standard author ≠ profile author ≠ implementer ≠
certifier**, which is how every standards body works. An implementer building a system and then
evolving it is not a separation anyone requires; it is the ordinary case.

## Open before G0 closes

- **Which revision does NOVA claim against?** `7a` CF-1 requires a named revision. `draft-4` is open
  with one change declared; `draft-3` is frozen and tagged but carries the twelve untrue
  declarations Change 1 repaired. Freezing `draft-4` first is the clean answer and is a decision,
  not a formality.
- **There is no conformance suite.** `7b` specifies demonstrations; Finding **B** records that it
  specifies none for the *specification* subject class, and no executable suite exists. A worker
  required to produce conformance evidence currently has nothing to run. **G0 exposes this boundary
  and does not solve it; G1 must dispose of it** in exactly one of three ways:

  | | Disposition | Consequence |
  |---|---|---|
  | **A** | existing normative demonstrations suffice | name them, and state how NOVA uses them |
  | **B** | the standard requires an instrument it does not let you build | specification finding; repair before G2 |
  | **C** | a suite is deliberately outside the family | G1 redefines G2's discharge method; it does not pretend a suite exists |

  What must not happen is *"build NOVA and demonstrate conformance"* with the worker inventing the
  test oracle. That creates precisely the second undeclared authority the experiment exists to
  detect.

## Gate contract

| Gate | Cannot close without |
|---|---|
| **G0** | profile artifact · three registers · classification · disposition |
| **freeze** | G2's findings dispositioned · repairs made · named and tagged revision |
| **G1** | protocol · firewall · permitted inputs · conformance discharge basis |
| **G2** | realization · assumption register · findings · evidence |
| **G3** | comparative results · disagreement dispositions |
| **G4** | baseline · transformation evidence · resulting governed state |

## What NOVA is not

Not a competitor to the reference. Not a migration. Not a judgement on the reference's quality — a
realization may be excellent and still reveal that the standard did not determine it.

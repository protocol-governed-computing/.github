# NOVA cycle 1 — what it established

A programme to test whether the Open PGC Standard is sufficient to build from. Independent parties
authored a profile against the standard alone, built a system claiming that profile, drove its
execution from sealed declarations, and evolved it through its own transformation semantics.

> **NOVA cycle 1 found no undeclared semantic gap within the exercised surface.** Three
> profile-authoring runs, an independent realization, declaration-driven execution, and a governed
> transformation produced **no determination with source basis `none`** and **no class-6 instance**
> requiring reconstruction of knowledge available only from an existing realization. **Three of
> `NPP-E`'s eight claims are discharged.** The execution claim is supported by discriminating
> mutation evidence: replacing declared routing with behaviourally equivalent hard-coded routing
> fails, as do mutations removing required routing and refusal behaviour.

Every word of that summary is load-bearing, and one word carries the whole result: **within the
exercised surface.** Three of eight claims, one profile, one model, no external effect path. It is
evidence of sufficiency where the standard was pressed, and no evidence at all where it was not.

## Claim ledger

`NPP-E` supports eight claims. What this cycle did with each:

| # | Claim | State | Evidence |
|---|---|---|---|
| 1 | Profile conformance | not claimed | — |
| 2 | Vocabulary and declaration surface | **discharged** | `conformance_evidence.md` |
| 3 | Snapshot conformance | exercised, not claimed | sealing and integrity demonstrated under claim 2 |
| 4 | Construction and transformation | **discharged** | `transformation_evidence.md` |
| 5 | Runtime and execution | **discharged** | `execution_evidence.md` |
| 6 | Evidence | exercised, not claimed | refusal evidence emitted throughout |
| 7 | Inspection | exercised, not claimed | read surface used for grounding and status |
| 8 | System instance | not claimed | requires all applicable constituent classes |

**Discharged** means an evidence document names the claim and supplies demonstrations that fail when
the behaviour is removed. **Exercised** means the machinery was built and used but no claim was
made for it — the builder declined to claim rather than assert, which is the correct behaviour and
not the same as discharge.

An earlier draft of this summary said *two* claims. It was wrong: the transformation is a claimed
and discharged claim, not evidence supporting another. The correction came from the builder.

**Four gates of five ran. The cycle is at a natural stop, not complete.**

| Gate | | |
|---|---|---|
| **G0** profile authoring | **run three times** | `NPP-C`, `NPP-D`, `NPP-E` |
| **G1** experiment protocol | **written** | governs G2 |
| **G2** independent realization | **run** | a system claiming `NPP-E`, discharging one of its eight claims |
| **G3** comparative conformance | **blocked** | structurally, see below |
| **G4** governed transformation | **run** | a lending domain added to G2's own baseline |

## The headline: the standard needed no repair

**Seventeen candidate findings across three authoring runs, and none was an undeclared gap.** Every
one landed on something the family had already marked — `6a` §7 and §11, `4c` §8, `2d` §1, `2b` §10,
`3e` §12, `3d` §7, `7b` §6, `2c`. Three authors probing for the standard's edges found only edges it
had already drawn.

G2 added nine determinations, **none with source basis `none`**. G4 added a transformation that
grounds by querying the baseline rather than assuming it. **Neither produced a finding against the
standard.**

**No class 6 anywhere** — nothing showed a worker unable to proceed without reconstructing something
knowable only from an existing realization.

## Two findings answered

**A — `6a` supports the distinction, and it took three runs to establish.** A records that `6a`
gives
an author the list of what to decide and no way to tell a deliberate silence from an omission. Run 1
was handed a taxonomy naming that distinction. Run 2 ran under a repaired commission but in the same
worker's context and carried the withdrawn vocabulary forward — provably: a phrase absent from its
own commission and present in the previous one. Run 3 ran fresh and drew the line from the text
alone: eleven determinations *expressly permitted by source*, eight *unresolved by family*.

**What rules out recall** is that run 3 extended the claim-type vocabulary as run 2 had, but with
different constructions for the same distinction. Recall reproduces phrasing; derivation reproduces
structure.

**F — the standard determines no vocabulary, and must not.** Three closures from byte-identical text
under one scope. `NPP-C` and `NPP-D` closed four kinds each and match one another, which is the
carry-over rather than agreement. `NPP-E`, the run that could not remember, closed **five** and
diverged from both, reaching **workflow** and **capability contract** — concepts neither earlier run
touched.

So the result is not *four rather than nine*. It is that the family declines to determine the set,
and `2d` §1 says it must: *"a family that named its kinds would admit exactly one platform, and PGC
admits as many as there are profiles."* **A set the standard deliberately declines to determine
cannot be a canonical axis of its ontology. Not carried into `2b`.**

## The instrument failed three times, and each failure was informative

**The experiment kept measuring itself.** Every repair is now in the commissions.

1. **The taxonomy answered the question it measured.** Handing a worker six classes including
   *deliberate silence* against *omission* answers Finding A in advance. Withdrawn: the worker now
   records **provenance** — source basis, claim type — and the commissioning side classifies after
   the run.
2. **Commissioner scope was counted as family delegation.** Seven of run 1's twelve class-2 entries
   cited the commission as their authority. **Class 0** added, and a third register for scope the
   commission fixed.
3. **A worker's memory is not covered by a rule about handed-over material.** Run 2 inherited run
   1's vocabulary through shared context. The rule now names the worker, not just the inputs.

**The rule that outlives the programme:** *an experiment may constrain the task, but it must not
supply the distinction whose derivability it is measuring.*

## Execution: the claim that had to be asked for twice

The transformation's first delivery declared a workflow carrying `["completed", "failed"]` and
**nothing in the system read it.** The lending rule lived in the body of a method; deleting the
workflow artifact left behaviour unchanged. `3a` §3.2 is the rule it missed: *"Execution performs no
routing logic of its own. It does not decide where to go; it reads where to go."*

It was not a defect in what was claimed — Runtime and execution was not claimed, and a system need
not discharge a claim it does not make. It was the boundary of what had been demonstrated.

Asked to discharge the claim, the builder drove traversal from the sealed declarations. **The
decisive check is a mutation that a well-formed fixture cannot distinguish:** replacing
`step["routes"][outcome]` with the behaviourally equivalent hard-coded branch **fails a test**. So
does emptying the declared routes map, and so does removing either refusal path.

That is `3a`'s central claim demonstrated rather than asserted — **behaviour carried by what was
sealed, not by the method that runs it.**

## Two evidence gaps, same shape, both found only by mutation

At G2, `NPP-E` mandates a SHA-256 digest and **substituting MD5 passed all six demonstrations.** At
G4, the baseline-grounding guard was correct and **disabling it entirely passed all fifteen.**

Both times: a property the profile requires, implemented correctly, asserted *about*, and never
demonstrated by anything that could fail. `7b` is explicit that a fixture set of only well-formed
material cannot exhibit a refusal.

**A passing suite is not evidence a demonstration could fail.** Neither gap was visible to the
tests, the author, or a reading of the evidence. Both closed on the first pass after being named,
without
the fix being specified — so it is a blind spot about what a demonstration is for, not a capability
gap.

## An implementation limitation, recorded

`3d` CP-9: *"A binding MUST be declared, MUST resolve before dispatch, and MUST NOT alter what the
contract declares."* The realization dispatches on `capability["declaration"]["effect"]`, using the
effect value as an implicit binding to its handler. There is no declared binding artifact.

The dispatch does refuse an unresolved binding, and the execution claim holds for the demonstrated
workflow. **What is not demonstrated is CP-9's declared binding**, and the claim should be read with
that boundary. Recorded as a limitation of the realization, not a finding against the standard.
Identified by the builder.

## Candidate findings against the standard — the first this programme has produced

None arose from being blocked. All three arose from the builder's reflection on what the cycle had
made visible, and `0z` §3 holds that a finding is recorded whatever its source and its source
decides nothing. **Recorded, not carried.**

**C-1 — a demonstration capable of failing is required; showing which one fails is not.** `7b` CD-4
requires that a demonstration could fail if the system were non-conforming. This cycle found two
guards, correctly implemented, whose removal broke no test — invisible to a passing suite, to the
author, and to a reading of the evidence. A clarification requiring each claimed normative guard to
carry a **documented counterfactual** — which demonstration fails when this guard is removed or
bypassed — would close it without prescribing tooling.

**C-2 — `3a`'s conformance section does not distinguish four cases that differ in what they
establish.** A declared route followed; a route absent; a route changed to an invalid target; and
**hard-coded routing ignoring a changed declaration.** The fourth is the decisive architectural test
— it is the only one a well-formed fixture cannot separate — and nothing in the text names it.

**C-3 — `7a` §10 says systems under different profiles are not comparable. It does not say a profile
exclusion prevents comparability.** `NPP-E` §12 excludes the reference realization by construction,
which is why G3 is blocked. Stating that an exclusion bars comparison, rather than merely barring
one candidate's conformance, would make the "differences establish nothing" result harder to
misread.

## Why G3 is blocked

`7a` §10: *"Two systems under different profiles are not comparable by this relation, and finding
that they differ establishes nothing."* NOVA claims `NPP-E`. The reference realization cannot —
`NPP-E` §12 excludes any system with more than one tenant, replicated governed state, or an exposed
interaction boundary, and the reference has a transport boundary. **The profile excludes the
reference by construction.**

G3 needs a third profile both can claim, drawn narrow enough for NOVA and permissive enough for the
reference. That is a design question, not a run.

## What the cycle did not test

**`3a` has since been built against and produced no finding.** What remains untested is narrower and
worth stating exactly:

- **`3d`'s effecting path.** A capability contract exists, declares an outcome vocabulary, and its
  outcomes are routed on. No capability with an **external effect** was exercised — and `NPP-E` §2
  selects no interaction boundary, so it may not be reachable under this profile at all. That is a
  scope limit of the profile, not an omission by the builder.
- **Five of `NPP-E`'s eight claims remain undischarged.** Three of those five — snapshot
  conformance, evidence, inspection — were *exercised* without being claimed; profile conformance
  and system instance were neither. See the claim ledger.

The defensible statement is therefore narrower than *the standard supports building a conforming
system*. It is: **the standard supports building the construction, identity, canonicalization,
refusal and inspection surface of one, driving its execution from sealed declarations, and evolving
it through governed transformation — and the builder declined to claim the rest rather than assert
it.** The second half is worth as much as the first.

All runs share one model. A different reader would strengthen every line above. It would not change
the divergence at G0, which was observed within one reader.

## Collateral: what changed outside the programme

**No change to the standard follows from NOVA.** The spec did change this cycle, from two other
instruments:

- **`draft-4` Change 1**, from a terminology projection pointed at the family's own vocabulary:
  twelve untrue declarations repaired, four terms struck, `step` moved to Part I, **five refinements
  declared — the first in the family**, and **CM-8** added, stating that a term belongs to the
  document whose subject matter principally establishes it.
- **`0d`** rewritten for orientation, with a figure.
- **`0z` §2's `1a` row** now reads `CM-1 … CM-8`.

**The instrument that found defects was pointed at internal consistency. The instrument pointed at
sufficiency found none.** The family was self-inconsistent in places nobody had checked, and
sufficient in every place three authors and one builder pressed on it.

Also produced: `tools/requirement_index.py` and a count guard reading `0z` §2 rather than
re-deriving — closing a projection that had reported **317 requirements across 24 documents** when
the family carries **356 across 26**, short by two whole documents because the extractor knew only
one of the two invariant forms.

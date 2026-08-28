# NOVA cycle 1 — what it established

A programme to test whether the Open PGC Standard is sufficient to build from. Independent parties
authored a profile against the standard alone, built a system claiming that profile, and evolved
that system through its own transformation semantics.

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

## Why G3 is blocked

`7a` §10: *"Two systems under different profiles are not comparable by this relation, and finding
that they differ establishes nothing."* NOVA claims `NPP-E`. The reference realization cannot —
`NPP-E` §12 excludes any system with more than one tenant, replicated governed state, or an exposed
interaction boundary, and the reference has a transport boundary. **The profile excludes the
reference by construction.**

G3 needs a third profile both can claim, drawn narrow enough for NOVA and permissive enough for the
reference. That is a design question, not a run.

## What the cycle did not test

**`3a` execution and `3d` capability have been read and never built against.** G2 discharged one of
`NPP-E`'s eight claims — vocabulary and declaration surface, with the sealed snapshot and in-process
read surface — and implemented no execution and no capability effect path. G4 exercised `4d`.

The defensible statement is therefore narrower than *the standard supports building a conforming
system*. It is: **the standard supports building the construction, identity, canonicalization,
refusal, inspection and evidence surface of one, and supports evolving it — and the builder declined
to claim the rest rather than assert it.** The second half is worth as much as the first.

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

release 12 — a passing suite is not evidence a demonstration could fail

This cycle's work is validation, not construction. Release 10 measured the realization against the
standard. Release 11 turned the same kind of instrument on the standard's own vocabulary. This one
runs the instrument the previous two were building toward: **independent parties authoring against
the standard alone, building a system from it, driving that system from what it sealed, and evolving
it through its own transformation semantics.**

Four gates of five ran. The standard needed no repair. That is the result, and the reason it is
stated carefully below is that a result of this shape is very easy to over-read.

## What NOVA cycle 1 established

Three profile-authoring runs, one independent realization, declaration-driven execution, and a
governed transformation produced **no determination with source basis `none`** and **no instance of
a worker unable to proceed without reconstructing something knowable only from an existing
realization.** Seventeen candidate findings arose across the three authoring runs and **not one was
an undeclared gap** — every one landed on something the family had already marked: `6a` §7 and §11,
`4c` §8, `2d` §1, `2b` §10, `3e` §12, `3d` §7, `7b` §6, `2c`. Three authors probing for the
standard's edges found only edges it had already drawn.

**Three of the claimed profile's eight claims are discharged** — vocabulary and declaration surface,
construction and transformation, runtime and execution. Three more were exercised and deliberately
not claimed; two were neither. The builder declining to claim rather than asserting is the correct
behaviour and is worth as much as the discharges.

So the defensible statement is narrower than *the standard supports building a conforming system*.
It is: the standard supports building the construction, identity, canonicalization, refusal and
inspection surface of one, driving its execution from sealed declarations, and evolving it through
governed transformation. **Within the exercised surface** is the load-bearing phrase. One profile,
one model, no external effect path.

## The finding this release is named for

At G2 the profile mandates a SHA-256 digest, and **substituting MD5 passed all six demonstrations.**
At G4 the baseline-grounding guard was correct, and **disabling it entirely passed all fifteen.**

Same shape both times: a property the profile requires, implemented correctly, asserted *about*, and
never demonstrated by anything that could fail. Neither gap was visible to the tests, to the author,
or to a reading of the evidence. Both were found only by mutation, and both closed on the first pass
after being named, without the fix being specified — so it is a blind spot about what a demonstration
is *for*, not a capability gap.

`7b` CD-4 already requires that a demonstration could fail if the system were non-conforming. It
does not require showing **which** demonstration fails. That is the gap, recorded as candidate
finding **C-1**, and it continues release 10's line directly: `declared ≠ implemented ≠ enforced ≠
demonstrated` ends at *demonstrated*, and this release finds that demonstrated has an inside.

## Execution, asked for twice

The transformation's first delivery declared a workflow carrying `["completed", "failed"]` and
**nothing in the system read it.** The lending rule lived in the body of a method; deleting the
workflow artifact left behaviour unchanged. `3a` §3.2: *"Execution performs no routing logic of its
own. It does not decide where to go; it reads where to go."*

This was not a defect in what was claimed — runtime and execution had not been claimed, and a system
need not discharge a claim it does not make. It was the boundary of what had been demonstrated.
Asked to discharge it, the builder drove traversal from the sealed declarations, and **the decisive
check is a mutation a well-formed fixture cannot distinguish**: replacing `step["routes"][outcome]`
with a behaviourally equivalent hard-coded branch fails a test. So does emptying the routes map, and
so does removing either refusal path.

That is `3a`'s central claim demonstrated rather than asserted — behaviour carried by what was
sealed, not by the method that runs it. It also produced candidate finding **C-2**: `3a`'s
conformance section does not name the fourth case, hard-coded routing that ignores a changed
declaration, which is the only one a well-formed fixture cannot separate.

## The instrument failed three times, and each failure was informative

The experiment kept measuring itself.

1. **The taxonomy answered the question it measured.** Handing a worker six finding classes, among
   them *deliberate silence* against *omission*, answers in advance the very question of whether an
   author can draw that line from the text. Withdrawn: the worker now records provenance, and the
   commissioning side classifies after the run.
2. **Commissioner scope was counted as family delegation.** Seven of run 1's twelve entries in one
   class cited the commission itself as their authority. A separate class and a third register were
   added for scope the commission fixed.
3. **A worker's memory is not covered by a rule about handed-over material.** Run 2 inherited run 1's
   withdrawn vocabulary through shared context — provably, by a phrase absent from its own
   commission and present in the previous one. The rule now names the worker, not just the inputs.

**The rule that outlives the programme:** an experiment may constrain the task, but it must not
supply the distinction whose derivability it is measuring.

Run 3, the run that could not remember, is what makes finding A hold: it drew the same distinction
from the text alone, and extended the claim-type vocabulary as run 2 had but with different
constructions for the same distinction. Recall reproduces phrasing; derivation reproduces structure.

## What three authors did with one text

Byte-identical source, one scope, three closures of the admissible kind set. The two runs sharing a
context closed four kinds each and agree with one another — which is carry-over, not agreement. The
run that could not remember closed **five**, and diverged from both, reaching workflow and capability
contract, concepts neither earlier run touched.

The result is therefore not *four rather than five*. It is that the family declines to determine the
set and `2d` §1 says it must: *"a family that named its kinds would admit exactly one platform, and
PGC admits as many as there are profiles."* **A set the standard deliberately declines to determine
cannot be a canonical axis of its ontology**, and it was not carried into `2b`.

## Why the fifth gate did not run

`7a` §10: two systems under different profiles are not comparable, and finding that they differ
establishes nothing. NOVA claims a profile whose §12 excludes any system with more than one tenant,
replicated governed state, or an exposed interaction boundary — and the reference realization has a
transport boundary. **The profile excludes the reference by construction.**

Comparative conformance needs a third profile both systems can claim, narrow enough for NOVA and
permissive enough for the reference. That is a design question, not a run. It also produced candidate
finding **C-3**: `7a` §10 says systems under different profiles are not comparable, and does not say
that a profile *exclusion* bars comparability.

## What was not tested, stated exactly

- **The effecting path.** A capability contract exists, declares an outcome vocabulary, and its
  outcomes are routed on. No capability with an **external effect** was exercised — and the claimed
  profile selects no interaction boundary, so it may not be reachable under that profile at all. A
  scope limit of the profile, not an omission by the builder.
- **A declared binding artifact.** The realization dispatches on a capability's effect value, using
  it as an implicit binding. `3d` CP-9 requires a binding be declared. The dispatch does refuse an
  unresolved binding and the execution claim holds for the demonstrated workflow; what is not
  demonstrated is CP-9's *declared* binding. Recorded as a limitation of the realization, identified
  by the builder, not a finding against the standard.
- **A second reader.** All runs share one model. A different reader would strengthen every line
  above. It would not change the divergence observed at the authoring gate, which occurred within
  one reader.

## Collateral

**No change to the standard follows from NOVA.** The specification did change this cycle, from two
other instruments entirely: a terminology projection pointed at the family's own vocabulary, which
produced twelve repaired declarations, four terms struck, the first five declared refinements in the
family, and a new consistency rule; and a requirement projection with a count guard reading the
family's declared invariant ranges rather than re-deriving them — closing a projection that had
reported 317 requirements across 24 documents when the family carries **356 across 26**, short by two
whole documents because the extractor knew only one of the two forms an invariant is written in.

**The instrument pointed at internal consistency found defects. The instrument pointed at sufficiency
found none.** The family was self-inconsistent in places nobody had checked, and sufficient in every
place three authors and one builder pressed on it.

The specification left draft this cycle and is declared at `v0`, carrying five findings published
with it — the three above and two from the previous cycle. Two of them, if carried, would change what
conformance costs. Systems claiming `v0` keep their claims; a successor may ask more.

## What this release is for

Nothing here is a repair. The standard needed none, and the one red check in the workspace is red
deliberately and recorded as such.

What this release does is close the last thing the project could do to itself. Every remaining
instrument requires someone who was not part of building it.

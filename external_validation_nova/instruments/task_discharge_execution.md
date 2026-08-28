# Task — discharge the runtime and execution claim

**For the builder of the system claiming `NPP-E`.** Same gate, another claim. Keep everything you
have.

`NPP-E` supports eight claims. You discharge two: the vocabulary and declaration surface, and the
transformation. **This asks for one more: Runtime and execution.**

## 1. The observation that prompts it

Your transformation declares a workflow carrying an outcome vocabulary — `["completed", "failed"]`.
**Nothing in the system reads it.** The lending rule lives in the body of `lend()`, which raises a
refusal directly. The declared outcomes are never selected, never routed on, never consulted.

That is not a defect in what you claim. You do not claim Runtime and execution, and a system is not
obliged to discharge a claim it does not make. **It is the boundary of what has been demonstrated**,
and the standard's execution model is on the far side of it.

## 2. What the claim requires

`3a` is the document, and its central rule is one sentence:

> **Execution performs no routing logic of its own.** It does not decide where to go; it reads where
> to go.

With EX-1: *execution MUST NOT originate behavior; every step MUST realize behavior the sealed
representation determines.*

So the question this claim answers is: **is the lending rule in the snapshot, or in the method?**
Today a reader can delete the workflow artifact and `lend()` behaves identically. That is the test —
not whether the system works, but whether its behaviour is carried by what it sealed.

`3d` governs what a capability is and what its contract declares. `NPP-E`'s vocabulary already
admits `capability-contract` and `workflow`; you have both as artifacts.

## 3. What to produce

Whatever `3a`, `3d` and `NPP-E` require of a discharge — that is yours to determine. What the claim
is judged on:

- a workflow **traversed** by reading declared routing, not by executing a hand-written procedure;
- a capability that **reports one of its contract's enumerated outcomes**, and a traversal that
  advances on that outcome and nothing else;
- **an unrouted outcome refusing** (`3a` §4.3: where a step reports an outcome for which the
  traversal declares no routing, execution refuses — it does not default, halt silently, or treat
  absence of routing as completion);
- **evidence** of the above that a party who did not build the system can obtain and check.

Registers as before: `determinations.md`, `unresolved.md`, and the provenance shape.

## 4. Demonstrations, and what has gone wrong twice

Two gaps have been found in your evidence, both by mutation testing rather than by reading it:
substituting MD5 for the profile's SHA-256 passed every demonstration, and disabling the
baseline-grounding guard passed every demonstration. Both times the property was implemented
correctly and nothing would have failed if it were not.

**Assume this set will be mutation-tested too.** For each behaviour the claim rests on, ask: *if I
removed this, which demonstration fails?* If the answer is none, the behaviour is asserted rather
than demonstrated.

The one most likely to be missed here: **if routing were hard-coded rather than read, would anything
fail?** A traversal that reads declared routing and one that ignores it produce identical results on
a well-formed fixture. Only an ill-formed one separates them.

## 5. If it cannot be done

`NPP-E` may not support the claim, or the standard may not supply what a discharge requires. **Say
so, precisely, and stop.** That is a more valuable result than a discharge, and it would be the
first finding in this programme against the standard rather than against evidence.

The standard and `NPP-E` are pinned and are not adjusted to make this easier. A defect you find in
`NPP-E` is recorded, not repaired.

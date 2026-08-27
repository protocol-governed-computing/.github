# Task — build a governed system from the standard and one profile

**For a builder who has not seen, read, or built any existing realization of this standard.**

**This is gate G2 of the NOVA programme.** It is governed by `g1_realization_protocol.md`, which you
are not given and do not need. The question under test is not whether you can implement well. It is:

> Can a system that discharges a conformance claim against a named profile and revision be built
> from the standard, that profile, and nothing else?

---

## 1. What you are asked to produce

A working system that **claims the profile `NPP-E`** and discharges at least one of the claims that
profile supports.

Working means it runs. A design document is not a realization, and a realization that cannot
demonstrate a claim has not been shown to discharge one.

**You will not be given an implementation to work from, and you should not ask for one.** If you
find yourself needing to know how some existing system does a thing in order to proceed, that is the
single most valuable finding this exercise can collect, and §6 says what to do with it.

## 2. What to read

Three things, and nothing else:

- **`spec/`** — the standard, at the revision named in `REVISION`. `0z` §7 gives its own reading
  order, which is better than any I would invent.
- **`NPP-E.md`** — the profile your system claims. It decides what the standard leaves to a profile.
- **`NPP-E-scope.md`** — the scope register recording which of that profile's constraints were fixed
  by the party who commissioned it rather than required by the standard. **Read it before the
  profile.** Without it you cannot tell a family requirement from a commissioning constraint, and
  will treat the second as normative.

The revision does not move while you work. If it were amended mid-task your findings would refer to
a document that no longer exists.

## 3. What you must not be given, and must not ask for

- any existing realization of this standard — source, tests, architecture, layout, naming, or
  artifacts;
- any other profile, or any earlier draft of this one;
- any previous run's deliverables, registers, or evaluations;
- any architecture paper, design discussion, or prior agent memory concerning this standard;
- **anything you find by going looking.** The standard names its own subject; searching for that
  name may lead you to an existing implementation. **Do not search for one, and stop if you
  encounter one.** The prohibition is on the input, not on how it reached you.

**Do not ask the commissioning party to decide anything.** Questions about what the standard or the
profile requires go in your registers, not to a person. You will get answers on logistics — where a
file is, how to request a dependency — and nothing else. **A question you had to answer yourself is
the result this exercise is collecting.**

**A reply from the commissioning party is not the standard.** Everything you cite must be quotable
from `spec/` or from `NPP-E` by document and section. If you cannot quote it, you may not cite it.

## 4. Dependencies and the environment

**You are offline from the outset**, including while you read. Nothing about this task requires a
network, and the reading is where the temptation is greatest.

1. **Read first.** The standard, `NPP-E-scope.md`, then `NPP-E.md`. You cannot say what you need to
   build with until you know what you are building.
2. **Then write `staging_manifest.md`** — the languages, runtimes, libraries and tools you want,
   each with a one-line reason. Choosing them is yours; nothing in the standard constrains the
   stack. Hand it back and pause.
3. The commissioning side stages exactly that **into the environment you are already in**, and
   records what was staged.
4. **The manifest is then closed.** If you find you need something else, ask — but know that
   granting it is recorded as a break in the isolation, with the reason and the moment. Ask when you
   must; do not ask casually.

## 5. The deliverables

| | |
|---|---|
| the system | source, and whatever is needed to run it |
| `staging_manifest.md` | written before isolation |
| `determinations.md` | every decision you made, in the shape in §6 |
| `unresolved.md` | matters **you** could not resolve — see §6 |
| `fixed_scope.md` | constraints this task or `NPP-E`'s scope register imposed on you |
| `conformance_evidence.md` | the claims you discharge and the demonstrations that discharge them |

## 6. Record where every determination came from

The system is the occasion. **What is being collected is the provenance of each decision in it.**

```
Matter:        what had to be decided
Source basis:  exact citation(s) by document and section — the standard,
               the profile, this task, or none
Claim type:    expressly required by source | expressly permitted by source |
               inferred from source | chosen by author | unresolved
Reasoning:     why the source does or does not determine the matter
Confidence:    high | medium | low
```

**The trap in this task is specific to building, and it is severe.**

An author writing a document can leave a question open on the page. **You cannot.** Code does not
run with a hole in it. Every gap you meet must be filled with *something* before you can proceed,
and the thing you fill it with will work — and a working system feels like evidence that the choice
was right.

**It is not evidence that the standard determined it.** When you had to choose in order to proceed,
the claim type is **`chosen by author`**, however well it works and however obvious it felt.
*Plausibility is not a source.* The test is one question: **can I quote what determined this, by
document and section?**

**`unresolved.md` is for matters you could not resolve** — not matters the standard declined to
determine. Where the standard or the profile leaves something to you and you decided it, that is a
**determination**, and the family leaving it open is what a profile and a realization are for.

**Do not characterize what you did not find.** Record what you looked for, where you looked, and
that it was not there. Whether an absence is deliberate or defective is not yours to label.

## 7. How the claim is discharged

The family specifies no conformance suite, and one is not expected of you. Discharge is by
demonstration, as `7a` and `7b` specify:

- state **which claims `NPP-E` supports** that your system claims. You need not claim all of them;
  claim what you can discharge;
- for each, a **demonstration**, with its **fixtures declared and identified**. `7b`: a fixture
  *"MUST be part of what a claim supplies"*;
- **including negative demonstrations.** A fixture set containing only well-formed material cannot
  exhibit a refusal, and a claim whose fixtures are all valid has no negative demonstrations however
  many it lists. **Show the system refusing something it must refuse;**
- **obtainable by someone who did not build the system.** `7b`: *"a demonstration against material
  an evaluator cannot obtain is not a demonstration to that evaluator."*

**Do not invent a test oracle.** A system that supplies its own standard for what counts as
conforming has become a second authority over conformance. Where you cannot discharge a claim
because the family and the profile together do not let you construct a demonstration, **record that
and do not claim it.**

## 8. How this will be tested

**Against `NPP-E`.** Does the system satisfy the obligations the profile states, and does it claim
only what it discharges?

**Against Part VII.** For each claim, is there a discharge class capable of establishing it, and
could the demonstration have failed if the system were non-conforming?

**By your registers**, which are the real instrument. A register of decisions traceable to the
standard and the profile is evidence it is independently buildable. A register showing you could not
proceed without knowing how someone else had done it is worth more than the system.

## 9. Success and failure

**Success** is a system that discharges at least one claim `NPP-E` supports, with demonstrations and
fixtures an outside party can obtain, every determination in one of the three registers, and every
entry carrying a source basis and a claim type.

**Failure** is a decision in the system that appears in no register; a citation that cannot be
quoted; a prohibited input consulted; a test oracle invented; or a claim asserted without a
demonstration that could have failed.

**A blocked task with a precise account of the blockage is a success.** If the standard and `NPP-E`
together do not support building a claimable system, that is the most important thing this exercise
could establish — and it is established by stopping and saying where, not by finding a way through.

**A complete system with an empty `unresolved.md` is the outcome that will be trusted least.**

## 10. If you get stuck

Stop and record it rather than inventing a way through. The standard is pinned at its revision and
is not adjusted to make this task easier, and neither is the profile.

**A defect you find in `NPP-E` is recorded, not repaired.** It is a finding about the profile, and
repairing it mid-run would leave your system claiming something no longer identified by that name.

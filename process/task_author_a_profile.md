# Task — author a Normative Platform Profile from the standard alone

**For an author who has not built, read, or seen the reference realization.**

**This is gate G0 of the NOVA programme.** Its output is an input to everything after it: the
profile a second, independent realization will be built against and will attempt to claim. The
question under test is not whether a good profile can be written. It is:

> Can an independent author create a valid `6a` profile using only the published standard, and can
> the result distinguish every decision the standard requires from every choice it deliberately
> leaves free?

Those are different questions from *can PGC be implemented*, and this task answers only the first.

---

## 1. What you are asked to produce

One document: a **Normative Platform Profile** conforming to Part VI of the Open PGC Standard.

**Identity:** the one given to you for this run. **Never one a previous run used** — `6a` §9 makes a
change of obligations a new identity, and two trials producing different obligations under one name
make both unverifiable after the fact.

A profile is a conformance contract over a system. It states the properties a system **shall**
satisfy in order to claim it. **It is not an inventory of what any particular system contains**, and
you should not be able to write one by describing something — only by deciding things.

**You will not be given an implementation, and you should not ask for one.** If you find yourself
needing to know how some existing system works in order to decide something, that is a finding about
the standard, and §6 tells you what to do with it.

## 2. Scope of this profile

Profile a class of systems with these characteristics, and decide everything else the standard leaves
to you:

- **a single governed system**, sealed and executed — one snapshot, accepted whole, executed against
  governed state;
- **inspection is required** — the system must be able to answer questions about itself;
- **no external protocol boundary** — nothing outside the system reaches it over a wire protocol
  during the scope of this profile;
- **no attestation beyond what the standard requires** — you decide what a checking party accepts;
- **one tenant, no replication.**

**This scope is deliberately narrower than a general-purpose platform.** Narrowness is a profile's
job. What matters is that every decision you make is one the standard delegates to you, and that you
make **all** of the ones bearing on the claims you support.

**Do not name the scope "minimal."** The standard is explicit that no platform is minimal by nature
and minimality is relative to a profile. Say what the profile is *for*.

## 3. What to read

**The standard at one named revision, frozen for the duration of this task, and nothing else.** The
revision identity is given to you with this commission. It does not move while you work: if it were
amended mid-task, your findings would refer to a document that no longer exists, and `7a` CF-1 makes
a claim meaningless without a revision to name.

`0z` §7 gives its own reading order, which is better than any I would invent:

| To understand | Read |
|---|---|
| why this exists | Part 0 |
| what the terms mean | `1a`, then `1b` |
| what must be true of any realization | `1c` |
| how governance works | Part II, beginning at `2a` |
| what a running system does | Part III, beginning at `3a` |
| how a system is built and changed | Part IV |
| how a system is reached | Part V |
| **how a concrete platform is specified** | **Part VI — `6a` is your document** |
| how any of it is established | Part VII |

**Read Part I in full first.** Everything derives from it, and `0z` §3 states the derivation rule
that governs how.

**Then `6a` in full.** §7 is the list of decisions the family hands to profiles — that list is the
core of your deliverable. §3 and §4 bound what you may and may not do. §6 is the externality
requirement and explains why it exists. §9 governs identity. NP-1 … NP-12 are what your document will
be judged against.

**Also read:** `6b` (execution environment profiles) and `6c` (domain profiles) — not to write them,
but so you can tell when a decision belongs to one of those rather than to you. `7a` and `7b` — a
profile that supports no evaluable claim is decorative, and NP-8 makes that concrete.

**The standard is read, never written.** Do not edit, patch, renumber, or "improve" any document of
the family — not in the copy you are given, not anywhere, and not even to fix something you are
certain is wrong. The family is frozen at its current revision for the duration of this task, a copy
you have amended is no longer the thing you are being tested against, and renumbering a section
breaks every cross-reference in the family at once. **Every change you would make goes in the
questions log as a finding against a named document** — what is wrong, and what it prevented you
from deciding. Proposing a fix there is the most valuable thing you can produce; applying one
destroys the run.

## 4. What you must not be given, and must not ask for

This list exists because the value of this exercise depends on it:

- **any existing profile, in whole or in part** — including any candidate carrying a name like
  *baseline*, *reference*, or *normative platform*, and including its shape, its field names, and
  its file format. A profile's *structure* leaks an architecture even when it names nothing;
- **any taxonomy of semantic spaces, concerns, artifact families, or identifier prefixes drawn from
  an existing realization** — how many there are, what they are called, or that any such set was
  arrived at. Whether the standard determines such a set, and what it contains, is among the things
  this task exists to find out;
- **any prior agent memory, session transcript, or architecture paper** describing how PGC has been
  built;
- **anything you find by going looking.** The standard names its own subject, so searching for that
  name — in a code host, a package index, a search engine — may lead you to an existing realization
  of it. **Do not search for one, and stop if you encounter one.** The prohibition is on the input,
  not on how it reached you: nobody has to hand you a realization for it to spoil the result, and a
  profile written after glancing at one is the failure Part VI's §6 exists to prevent, whether or
  not the glance was invited;
- any implementation's source, architecture, artifact inventory, directory layout, or naming
  conventions;
- any evidence about how a particular system realizes the standard;
- any answer to "how does the existing system do it?";
- **the deliverables, questions log, or evaluation of any previous run of this task.**

**If you are offered any of these, decline them.** A profile written by consulting a realization is
the failure mode Part VI's §6 exists to prevent, and it makes the result worthless for its purpose.
The same is true of one written by consulting a previous attempt: the trial measures what the
standard alone supports, and a run that inherits another run's answers measures nothing.

**Do not ask the commissioning party to decide anything.** Questions about what the standard
requires go in the log, not to a person. You will receive answers on logistics — where the documents
are, what identity to use — and nothing else, and you should not expect more. **A question you had
to answer yourself is the result this exercise is collecting.**

**A ruling from the commissioning party is not the standard.** Anything told to you in reply is an
instruction about how to work, not normative text. **Everything you cite must be quotable from a
document of the family, by document and section** — if you cannot quote it, you may not cite it, and
if you believe it should be there but is not, that is a finding.

## 5. The deliverable

**This commission does not tell you what a profile looks like.** Everything below is quoted or cited
from the family; where it is not, it is not binding on you. If this task supplied structure the
standard does not require, it would have become a second, undeclared specification — which is the
failure the whole exercise exists to detect.

A single document declaring, at minimum:

1. **Its identity** (§9, ID-1) and what it profiles.
2. **Its selections and constraints** — the decisions of `6a` §7 that bear on the claims it supports.
   NP-8: *"A profile MUST decide every deferred item bearing on a conformance claim it supports."*
   For each, state the decision and the family document that delegates it.
3. **Any additional obligations** it imposes (§5), each **enforceable** — NP-6 forbids an
   unenforceable obligation from being declared as one. State, for each, what would establish a
   breach.
4. **The conformance claims it supports**, and for each, what discharges it (`7a` §7's discharge
   classes; `7b` on demonstrations).
5. **What it excludes** — systems whose requirements this profile does not admit.
6. **Its kind vocabulary, closed** — `2d` requires an admissible set of artifact kinds to be closed
   within a revision, and `6a` requires a profile that closes one to state what each admitted kind
   declares. Decide whether this profile closes one; if it does, close it, and if it does not, say
   which authority does and why that is consistent with the claims you support. **Derive the set
   from the family, not from what a platform would plausibly need.**

**Say why, not only what.** Where a decision could reasonably have gone the other way, one sentence
on why it went this way is worth more than the decision alone, and it is what makes the profile
reviewable rather than merely followed.

## 6. Keep a questions log — this is half the deliverable

Record **every question you had to answer that the standard did not answer for you.** For each:

| Record | |
|---|---|
| the question | as you asked it |
| where you looked | which documents and sections |
| what you did | the decision you made, and on what basis |

**Classify each one into exactly one of the classes below.** The classification is the instrument.
Without
it, every choice you made looks like evidence the standard was incomplete, and the exercise
degenerates into *the author made decisions, therefore the standard has holes.*

| Class | You encountered | Finding? |
|---|---|---|
| **1 — realization freedom** | a choice the standard deliberately leaves open: encoding, file format, tooling, internal structure | **No.** Record it and say which text leaves it open. |
| **2 — profile decision, specified** | the standard delegated it to you and gave you what you needed to decide | **No.** That is this task. |
| **3 — profile decision, underspecified** | the standard delegated it to you and did not give you enough to decide it | **Yes.** A profile-authoring finding. |
| **4 — ambiguity** | two defensible readings of the text produce incompatible profiles | **Yes.** Name both readings and the sections. |
| **5 — omission** | a determination you were required to make has no normative source at all | **Yes**, and serious. |
| **6 — reference-shaped assumption** | you could not proceed without reconstructing something apparently knowable only from an existing realization | **Yes — the most valuable result this task can produce.** |

**Do not smooth over classes 3 to 6.** A question you resolved by picking something sensible is
still a finding if the standard should have decided it.

**Class 6 is what you are really hunting.** It is also the hardest to notice, because a capable
author fills such a gap from general engineering instinct without registering that it happened. The
test: *can I trace this to a document and section?* If not, it is a finding, whatever its
plausibility. **Plausibility is not a normative source.**

Keep these as **separate registers**, not one list — a decision ledger for classes 1 and 2, and a
findings register for classes 3 to 6. They are read by different people for different purposes.

## 7. Where you cannot discharge a claim, say so

`6a` NP-8 requires you to decide every deferred item bearing on a conformance claim you support, and
item 4 of the deliverable above asks what discharges each claim. You may find that the family
specifies demonstrations without supplying enough to construct one for some subject class.

**If so, record it and do not invent the instrument.** A profile that supplies its own oracle for
what counts as conforming has become a second authority over conformance, which is the same defect
as inventing a semantic decision. Name the claim, name the discharge class, and state precisely what
is missing.

## 8. How this will be tested

**Against `6a`, by reading.** Every one of NP-1 … NP-12 is a property of your document:

| | |
|---|---|
| NP-1, NP-2 | permits nothing the family forbids; requires nothing less |
| NP-3, NP-4 | redefines no term, weakens no invariant |
| NP-5 | introduces no facility the family has no home for |
| NP-6 | every additional obligation is enforceable |
| NP-8 | every deferred item bearing on a supported claim is decided |
| NP-9 | has an identity; a change of obligations is a new identity |
| NP-11 | no selection or parameterization makes a prohibited behaviour appear permitted |

**Against Part VII.** For each claim the profile supports, is there a discharge class capable of
establishing it (CF-8), and could a demonstration exist that would fail if the system were
non-conforming (CD-4)?

**By a claim attempt.** A system built independently of this profile will attempt to claim it. **The
profile passing or failing that attempt are both informative** — what is not informative is a profile
written so that some particular system passes.

**By the questions log**, which is the real instrument. A log containing only implementation and
profile choices is strong evidence the standard is independently usable. A log containing missing
semantic decisions is more valuable still, and each one becomes a finding against a named document.

## 9. What this exercise does and does not establish

**Stated plainly so the result is not over-read.**

It **does** establish whether a competent reader can decide the family's delegated questions from the
standard alone — the cheapest available test of independent usability, and one that costs a document
review rather than an implementation.

It **does not** by itself satisfy the standard's externality requirement. `6a` §6: *"Externality is a
property of authorship, not of storage… what matters is that changing it is not within the authority
of the system that claims it."* If the party commissioning this work can change the resulting
profile at will, the form is satisfied and the substance is not. **Whether this profile is external
to any system that later claims it is a question about authority, decided separately from how well it
is written.**

## 10. What counts as success and failure

**Success is not a profile that looks good.** This task succeeds when the profile is testable
against NP-1 … NP-12 by reading, every decision is classified, and every class 3–6 finding is
traceable to a named document and section.

**It fails** if a decision appears in the profile that appears in no register; if a citation cannot
be quoted from the family by document and section; if any prohibited input was consulted; or if a
class 3–6 finding was resolved silently rather than recorded.

**A blocked task with a precise account of the blockage is a success.** A complete profile with an
empty findings register is the outcome to be most suspicious of.

## 11. If you get stuck

Stop and record it rather than inventing a way through. The standard is frozen at its current
revision and is not adjusted to make this task easier. **A blocked task with a precise account of the
blockage is a successful outcome of this exercise.**

# Task — author an Execution Environment Profile from the standard alone

**For an author who has not built, read, or seen any realization of this standard.**

---

## 1. What you are asked to produce

One document: an **Execution Environment Profile** conforming to Part VI of the Open PGC Standard.

**Identity:** the one given to you for this run. **Never one a previous run used** — `6a` §9 makes a
change of obligations a new identity, and two trials producing different obligations under one name
make both unverifiable after the fact.

An environment profile is a conformance contract over an environment and the systems that run in it.
It states what the environment must provide and what a system claiming it must satisfy. **It is not a
description of any particular substrate**, and you should not be able to write one by describing a
platform you know — only by deciding things.

**You will not be given an implementation, a substrate, or a product, and you should not ask for
one.** If you find yourself needing to know how some existing orchestrator, cloud, or runtime works
in order to decide something, that is a finding about the standard, and §6 tells you what to do with
it.

## 2. The environment to profile

Profile an environment with these characteristics, and decide everything else the standard leaves to
you:

- **multiple nodes, geographically separated**, executing one governed system;
- **nodes become unreachable, and the network partitions** — not as an exception but as an expected
  operating condition;
- **no synchronized clock across nodes**, and no bound you may assume on clock skew;
- **no instant at which every node is guaranteed to hold the same snapshot** — propagation takes
  time;
- **the substrate offers a hardware attestation device on some nodes and not others**, and which
  nodes have one may change;
- **work carries deadlines**, and exceeding one has operational consequences;
- **one tenant.**

This is a hard environment on purpose. It is not a trick, and there is no hidden correct answer —
but **some systems will not be able to run in it**, and deciding which is part of the work.

## 3. What to read

The standard, and nothing else.

| To understand | Read |
|---|---|
| why this exists | Part 0 |
| what the terms mean | `1a`, then `1b` |
| what must be true of any realization | `1c` — **AI-12 in particular** |
| how governance works | Part II, beginning at `2a` |
| what a running system does | Part III — `3a`, `3b`, `3c` are directly load-bearing here |
| what a profile is, and what one may do | **`6a` in full — every rule in it applies to your document unchanged** |
| **your document** | **`6b`** |
| how any claim is established | `7a`, `7b` |

**Read Part I in full first.** Everything derives from it, and `0z` §3 states the derivation rule
that governs how.

**Then `6a`, then `6b`.** `6b` §1 says an environment profile *"is a profile in the sense the
Normative Platform Profile specifies, and every rule there applies here unchanged."* That means
NP-1 … NP-12 are properties of your document as much as EE-1 … EE-8 are. A document that satisfies
`6b` and violates `6a` has not conformed.

**Also read** `6a` and `6c` well enough to tell when a decision belongs to one of those rather than
to you. Deciding something that is a platform profile's or a domain profile's is as much an error as
leaving your own undecided.

**The standard is read, never written.** Do not edit, patch, renumber, or "improve" any document of
the family — not in the copy you are given, not anywhere, and not even to fix something you are
certain is wrong. The family is frozen at its current revision for the duration of this task, a copy
you have amended is no longer the thing you are being tested against, and renumbering a section
breaks every cross-reference in the family at once. **Every change you would make goes in the
questions log as a finding against a named document.** Proposing a fix there is the most valuable
thing you can produce; applying one destroys the run.

## 4. What you must not be given, and must not ask for

- any existing profile of any kind, in whole or in part;
- any implementation's source, architecture, or artifact inventory;
- any product, platform, or orchestrator documentation;
- any answer to "how does an existing system handle this?";
- **the deliverables, questions log, or evaluation of any previous run of this or any related task.**

**If you are offered any of these, decline them.** A profile written by consulting a realization is
the failure mode `6a` §6 exists to prevent.

**Do not ask the commissioning party to decide anything.** Questions about what the standard requires
go in the log, not to a person. You will receive answers on logistics — where the documents are, what
identity to use — and nothing else.

**A ruling from the commissioning party is not the standard.** Anything told to you in reply is an
instruction about how to work, not normative text. **Everything you cite must be quotable from a
document of the family, by document and section** — if you cannot quote it, you may not cite it, and
if you believe it should be there but is not, that is a finding.

## 5. The deliverable

A single document declaring, at minimum, what `6b` §9 requires:

1. **Its identity**, and the environment it profiles — *"bounded well enough that a system can
   determine whether it is in one."*
2. **The execution constraints it requires** (`6b` §3), and the obligations each places on a system
   claiming it. For each, state what would establish a breach — NP-6 forbids declaring an obligation
   nothing can refuse.
3. **What it excludes** — systems whose requirements this environment cannot meet.
4. **The conformance claims it supports**, and for each, what discharges it (`7a` §7's discharge
   classes; `7b` on demonstrations). Note what `6b` §12 says about how a system's conformance under
   an environment profile is established.

And, because `6b` §1 makes every rule of `6a` apply to you: **any decision `6a` delegates to a
profile that bears on a claim you support** (NP-8), each stated as your own decision rather than
deferred to the system that claims you (NP-12).

**Say why, not only what.** Where a decision could reasonably have gone the other way, one sentence
on why it went this way is worth more than the decision alone.

## 6. Keep a questions log — this is half the deliverable

Record **every question you had to answer that the standard did not answer for you.** For each: the
question as you asked it; where you looked, by document and section; what you decided, and on what
basis.

**Classify each one:**

- **an implementation choice** — encoding, format, tooling. *Fine; deliberately left open.*
- **a profile choice** — the standard delegated it to you and you decided it. *Fine; that is this
  task.*
- **a missing semantic decision** — you had to invent something the standard should have told you,
  and no profile is the right home for it. **This is a defect in the standard, and finding one is a
  more valuable result than the profile.**

**Do not smooth over the third category.** A question you resolved by picking something sensible is
still a finding if the standard should have decided it. **A log that walks a list in the standard row
by row and contains nothing else has recorded the questions the documents named, not the questions
you had** — record the terms you needed and did not find, the boundaries the family did not draw, and
the points where you could not tell whether a silence was deliberate.

## 7. How this will be tested

**Against `6b`.** EE-1 … EE-8 are properties of your document.

**Against `6a`.** NP-1 … NP-12 apply unchanged. In particular NP-4 — a profile may not weaken, exempt
from, or relax any invariant — and NP-12, which forbids deciding an item by deferring it to the
system that claims the profile.

**Against Part VII.** For each claim you support, is there a discharge class capable of establishing
it (CF-8), and could a demonstration exist that would fail if the system were non-conforming (CD-4)?
`6b` §12 is specific about how conformance under an environment profile is established — a profile
supporting a claim that cannot be discharged supports a claim nobody can evaluate (`6a` §7).

**By the questions log**, which is the real instrument.

## 8. What this exercise does and does not establish

It **does** establish whether a competent reader can decide the family's delegated questions from the
standard alone.

It **does not** by itself satisfy the standard's externality requirement. `6a` §6: *"Externality is a
property of authorship, not of storage… what matters is that changing it is not within the authority
of the system that claims it."* Whether this profile is external to any system that later claims it
is a question about authority, decided separately from how well it is written.

## 9. If you get stuck

Stop and record it rather than inventing a way through. The standard is frozen at its current
revision and is not adjusted to make this task easier. **A blocked task with a precise account of the
blockage is a successful outcome of this exercise.**

release 5 — correcting a governed system, and explaining it

dev/4 established that a business problem can be compiled into artifacts. dev/5 asks the question
that comes next and is harder: **what happens when something built that way turns out to be wrong?**

Every change in release 4 authored something. A lifecycle that can only describe creation cannot
describe maintenance, which is most of what happens to software. This release drives a defect
correction through the same nine phases and out the other side, and the machinery it broke on the way
is what the release consists of.

## The change that authors nothing

A governed change was raised against `blockchain::identity` for a defect: recording a verification
decision replaced the participant's whole record, silently erasing the name and preferences they
registered with — and succeeding every time. The rule saying otherwise had been written a change
earlier.

The dossier is complete, P0 through P8, every phase admissible, pinned to the composition its
predecessor produced. **The emitted diff is two lines.** An operation declared as *write this value*
became one declared as *update these fields*.

Nothing about that was ordinary. Getting a two-line correction through the pipeline required four
changes elsewhere, each the same defect at a different level.

**The registers assumed authorship.** Four registers naming what a change creates each demanded at
least one row, so a change that amends rather than authors was literally inexpressible. They are now
optional. The biconditionals binding the phases to each other still hold in both directions.

**The platform could not express the operation.** The mutable store offered a whole-value write at a
key, and a merge across a filter, and nothing that merged fields at a key. Without it the domain
would have leaned on its own uniqueness rule to make a set operation behave as a point operation —
an unstated promise that travels wherever it is copied. **When a domain needs a neutral mechanism the
substrate lacks, the substrate gains it.** That is the second time: first a clock, now an update.

**A dead field was hiding a missing one.** The renderer wrote a field on every workflow exit that no
constitution declares, no assertion checks and no runtime reads — its value derived from whether a
node's name ended in `COMPLETED`. It never wrote the one key the platform actually reads there. The
renderer now writes it, and the dead field is gone from the renderer and from all 18 artifacts that
carried it. Acceptance reported zero field differences after the removal, which is the evidence that
nothing had been reading it.

**Two refusals still share one result class.** "The details cannot be read" and "the act ran and
refused" both classify as a violation, because the closed governed set has no kind for the second.
That one is recorded, not fixed — a distinct class is a change to the transport egress constitution.

## Two ways the system could be confidently wrong

Both were found by using the system rather than by testing it, and both answered cleanly while
answering falsely.

**Inspection answered "nothing uses this" for fourteen of fifteen stores.** The join read only a
binding's concrete path, so every store reached through a structure or a top-level declaration came
back unused. Nothing failed; the answer was empty, well-formed and wrong. It now resolves all three
forms and answers for 15/15. **An inspection answer that is empty and confident is the characteristic
failure of an inspector**, and this is now the first thing its architecture document tells a reader
to distrust.

**Disagreeing copies of one identity assembled successfully.** A governance artifact is compiled into
every domain's output, so one identity exists N times, and nothing checked that the copies matched.
Editing one and recompiling a single domain left five copies of the mutable-store capability in two
versions — and that composition assembled, round-trip verified, and reported conformance while the
capability surface answered from a stale copy. Copies are now compared by content hash during
snapshot verification, proved against a deliberately tampered snapshot.

## Identity is complete, and not fully enforced

Registration, decision, records that keep what a participant was admitted with, reachable over both
transport and the command line, idempotent registration, every declared refusal refused.

Three rules the domain declares are enforced at its boundary but not within it, and are deliberately
carried forward rather than fixed speculatively: a rejection must state grounds, the moments of
registration and decision must be announced, and a repeated registration must record its differing
details. The next function to name an actor is the first consumer able to test them against real
data. One change closes all three — splitting the deciding workflow into accept and reject, which
gives the reject path an unconditional grounds check and each path an exit to announce from.

The module reports 12 of 14 criteria holding, and that number is the honest state of it. It should
not be read as green.

## The documentation set

Three papers now publish together: what evolution must be, what execution must be, and — new in this
release — what it takes to make both real. The third carries a formal definition of construction
completeness and a three-move device (obligation, realization, incidental) with an ageing test:
delete the latter two and a usable specification must remain. Two foundation documents were revised
to v1; neither alters a claim.

Every repository in the composition now carries an **`ARCHITECTURE.md`**: frozen per release, written
for a reader with no prior familiarity, self-contained, and figure-led. They are not duplicates of the
working documents. One is a release snapshot and the other a working state, and drift between them is
signal rather than decay. Each opens with a claim a reader can execute — the transport engine's is
`grep` the resolver and adapters for any workload name and find nothing.

## Architectural notes

**Write what does not exist; update what does.** A whole-value write is correct where a record is
created and wrong where one is changed.

**A workflow input must be the caller's own data or a constant, never a derivation of it.** The test
when it bites: would the business name this as its own act? Yes, split it. No, the derivation belongs
inside the workflow.

**A rule stated in a document and realised in no artifact is checked by nothing.** Two such rules
were found in one subdomain. No phase rule catches it; only executing the function and reading what
it left behind.

**Correct where exercised, unverified elsewhere.** Defect discovery in a governed system is a
coverage property, not a maturity one. The cheapest instrument that would have caught four of this
release's five defects in one run is a maximal admissible corpus case exercising every register and
every artifact family. The testbed has inadmissible cases and no maximal admissible one.

## Operational

The composition is 369 indexed artifacts across 7 domains — ai_governance, blockchain,
book_library_mgmt, inspection, platform, transformation, workload — and composition conformance
passes over the 376 artifacts it judges. Per-phase rule counts are P0 83 · P1 189 · P2 74 ·
P3 51 · P4 79 · P5 69 · P6 52 · P7 122 · P8 32, totalling 751 rules resolving against 42 check kinds.

Standing checks at the cut: 37 end-to-end phase cases; 37 documents agreeing between the tool and the
running system across 9 phases; construction acceptance at 51/52 artifacts with zero field
differences; rule sets sealed 9/9; the workload executing with all sequences terminating; inspection
answering for 15/15 stores; and every copy of every identity in the snapshot agreeing.

A completed change keeps the baseline pin it was approved against. A mismatch against today's
composition is the pin working, not a defect — approving a register against the post-build state
asserts a re-reading of facts the build already falsified.

The `dev/5` branch history has the working detail — every defect, and the change that closed it.

release 6 — when domains stop being independent

dev/4 established that a business problem can be compiled into artifacts. dev/5 asked what happens
when something built that way turns out to be wrong. **dev/6 asks what happens when one part of the
business needs another part.**

Every change through release 5 acted on a domain that could be reasoned about alone. That is not how
businesses work. A wallet belongs to a person the identity function accepted. Registering a book
completes three things at once. A rule the business states in one sentence has to be carried out
somewhere specific, and somebody has to be able to point at where. This release is the machinery for
all three, and a new business function that exercises the first.

## An act may read what another subdomain owns, and may never write it

A subdomain owns its records. Nothing else writes them — that is what ownership means, and it is the
property that lets a domain be reasoned about without reading the rest of the system.

But a wallet cannot be created for a person the business has not accepted, and the record of that
acceptance belongs to identity. The act needs to *look*.

So an act now **declares its reach**: the bindings it consults, named in its design, read and never
written. The declaration is not documentation. It travels through the whole toolchain:

- the design language has a register for it, and rules that hold an act to what it declared;
- the compiler composes an act's storage from the bindings it operates under, marking which are
  reached rather than owned;
- **the runtime refuses a write through a reach at execution.**

The refusal at the end is the point. A declaration that only a compiler checks is a promise; one the
runtime enforces is a boundary. An act that declares it consults identity's records, and then writes
one, is stopped — not reviewed, not warned, stopped.

The validation states the property directly: *identity's records are consulted and never written —
byte for byte what they were.*

## A new function: the wallet

`blockchain` gained a second subdomain. An accepted person is given exactly one wallet; a person the
business never registered is refused; an unverified person is refused; a person who already holds one
does not get a second. The creation of a wallet is recorded as a moment on its own trail.

It is the first adopter of declared reach, which is why it exists in this release rather than a later
one: a capability nobody has used is a capability nobody has tested.

Nine validated criteria hold. One is not exercised and says so — a write through a consulted binding,
which no act is authored to attempt. **The platform refuses it at run time and proving that needs an
act written to try**, which would be an act authored to fail. The skip is honest rather than pending.

## One act, several announcements

An act that completes says so by announcing a business moment. Until this release it could announce
one.

Registering a book completes three things: the work, the book, and the physical copy. Six acts in the
library catalog completed moments the business had declared and announced none of them, because the
platform could not express more than one ending announcement.

Now an act announces **several moments at one ending, in the order the business completes them**. The
compiler seals the sequence and refuses a repeat; the runtime announces each as sealed and reports one
it cannot make. Six acts now announce eight moments between them.

The moments were not new. They had been declared long before and referenced by nothing — the design
could say a moment existed and could not say which act completed it.

## The catalog learned what it holds and what it completed

`book_library_mgmt` gained two changes. The first separated a **work** from an **edition**: a title
is not the same thing as a printing of it, and a library that conflates them cannot register a second
edition without inventing a second work. The second gave six of its ten acts the announcements above.

The second change is worth reading for how it failed rather than what it added. The design was
admissible at all nine phases across 793 rules and would still have rendered six acts **without the
actor they run as** — the authorization context every catalog operation carries. The design had
inventoried the six acts and the six moments and not the actor. Construction measured it at 98.2%
complete and named the missing fact six times, before anything was written.

This is why there are two compilers and not one. A design compiler asks whether a design is complete
and consistent as a design. A construction compiler asks whether it determines the artifact. Those
questions differ in kind, and passing the first establishes nothing about the second.

## The storage capability learned to select

A domain needed to search what it held. Answering a question about a collection means seeing the
records and choosing among them by content; the capability could list a collection and could not
select within one.

It can now. The change had already been made when the boundary governing such changes was written, so
this release also carries the dossier it should have had — retrospective by construction and by
admission. **When a domain needs a neutral mechanism the substrate lacks, the substrate gains it, and
the change is recorded as a platform change rather than a domain's private extension.** That is now
the third time: a clock, an update, and a select.

## A declared refusal has to be carried out somewhere

A business states operations it refuses and the conditions under which it refuses them. *We will not
register a book whose title, author and year match one we already hold.*

Twelve rules across the first two phases guarded the arrival of those statements. **None guarded their
consequence.** A refusal could be declared by the business, restated by the change request, and
carried unread through six more phases into a system where nothing performed it.

A design must now account for every refusal the business declared, and there turn out to be three
places a refusal can be carried out:

- **a step of an act** — the operation is attempted, a step detects the condition, and the act stops
  at an ending that refuses;
- **absence** — the business refuses something the system simply does not offer;
- **the governance surface** — a rule of the pipeline makes the offending design inadmissible before
  anything runs.

The first is fully checkable: the design already states its acts, their steps, the outcomes each
reports and the type of each ending, so a rule can verify that the named step exists, reports the
named outcome, and that the outcome reaches an ending that refuses rather than one that completes.
The third is checkable for existence but not for coverage — a cited rule can be shown to be in force,
never to be the right rule — and that judgement stays with the person at the gate. The second has no
form yet, and the release says so rather than pretending otherwise.

## What the composition now checks about itself

Four checks were added, and each exists because something had already gone wrong quietly:

- **every generator agrees with what it produces** — three generators now report drift instead of
  being discovered stale by hand;
- **the compiler enriches and never overwrites** — every authored declaration survives compilation
  unchanged, which was true, unstated and unchecked;
- **no layer of the registry is declared two ways** — three artifacts claimed authority over where
  the registry lives while contradicting the one that is actually read;
- **a superseded artifact is unreachable**, asserted over the whole composition rather than trusted.

One discipline governs all four, and it is worth stating for anyone adopting this architecture: **a
check that has never been observed to fail is evidence of nothing.** Each was proved by breaking the
thing it guards and watching it refuse.

## The composition

Seven domains: the platform, a conformance workload, inspection, transformation, and the business
domains `ai_governance`, `blockchain` and `book_library_mgmt`. 399 artifacts, composition conformance
passing, an independently reproduced snapshot identity. The design language stands at 820 rules across
nine phases; the inspection surface publishes eighteen operations; every domain validates its own
behaviour against criteria its change requests declared.

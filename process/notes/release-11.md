release 11 — a declaration is not a definition

Release 10 measured the realization against the standard. This release turns the same instrument on
the standard itself, and finds that the family had been failing its own vocabulary rules for as long
as it had stated them.

Twenty-four of the thirty-two documents open by declaring the terms they introduce. **Twelve of those
declarations were not true.** The rule requiring a document that introduces a term to define it has
been in force since Part I was written; nothing could see it was being broken, because nothing read
the declaration sentences against the documents carrying them.

## What the declarations said, and what the documents did

Seven terms were named in a declaration and never defined anywhere. `4b` introduced **faithfulness**
and the word never reappeared. `3a` introduced **traversal**, **step** and **routing**, and each
appeared only inside a bolded sentence — *"Execution includes traversal."* — never marked as a term.
`2d` declared **kind registry** and marked `registry`. `3b` declared **self-description** and marked
`self-describing`.

Four terms should not have been declared at all. `3c` introduced **execution agent** while Part I
already defines **Runtime** as *the agent that performs execution*: a second name for one concept,
which the family names as a defect outright. `4a` introduced **admissibility determination**, a
compound of two terms already defined elsewhere. `6c` introduced **platform-owned governance** and
**domain-owned governance**, then drew the distinction in a table and never used either phrase.

The most consequential was **step**. Part I defines a workflow as *"a declared structure of governed
steps"* — resting a Part I definition on a term Part III owned. It now sits in Part I, and Part III
refines it.

## Refinement, exercised for the first time

The family has always required a document needing more of an inherited concept to refine it and say
what it is refining. **No document had ever done so.** Five now do: over **step**, **snapshot**,
**provenance**, **resolution** and **candidate**.

Four of those five were refinements already. `3b` adds five properties to Part I's snapshot; `2b`
adds an origin vocabulary to its provenance; `4c` states what resolution must do when an identity is
what is resolved. None restated what the concept *is*. What each got wrong was the declaration
sentence, which claimed to *introduce* a term Part I defines — the opposite of the relation the rule
requires. Only `4a`'s **candidate** was a real second definition, near-verbatim with Part I's, and
the duplicate clause is gone while what construction adds remains.

## The rule nobody had written down

Deciding where **candidate** belonged could not be settled by wording. Near-verbatim duplication is
evidence of an accident, not of ownership. It was settled by use: **candidate** appears in ten
documents, and the Semantic Model defines **proposal** as *"a candidate change presented to a
governed state"* — a Part I document using the term to define one of its own. Had construction owned
it, Part I would rest on a Part IV term, which is the defect just repaired for **step**.

That determination had to be made four times and the family stated the rule nowhere. It is now
**CM-8**: a term belongs to the document whose subject matter principally establishes it, never to
Part I by order of appearance. The contrary reading would make the Conceptual Model a warehouse for
whatever was written down earliest.

CM-8 is the only requirement this release adds. It invalidates no existing definition — all four
determinations left their term where the rule puts it — and it binds documents rather than
implementations, so a realization conforming to the previous revision conforms to this one unchanged.

## The instrument was wrong before the documents were

The first harvest reported **124 defects. One hundred and eleven were its own blindness.**

The family sites a definition five ways: a paragraph opening with the bolded term, a copula sentence,
a numbered section named for the term, a table row, and the term bolded at first substantive use. The
extractor knew two of them. Every document using the other three read as a document that had defined
nothing.

Three further conventions were learned by getting them wrong. A definition may share a line with the
declaration that introduces it. A mark may carry its article inside the bold. A bolded term must not
straddle a line break — a rewrap during this cycle split one across two lines and silently unmade a
definition the extractor had been reading.

This is the characteristic failure of a derived index, and the guard is the same one release 10
required elsewhere: the term count is verified by a script sharing no code with the extractor. The
contract now states the conventions the derivation depends on, so that a change to any of them
breaks loudly.

## The family projects itself

The index and its findings are a projection in the standard's own sense — derived, deterministic,
faithful, regenerable — and are governed as one, with a declared contract stating source, selection
and derivation. They live outside the family they derive from: a file identifier confers membership,
and a regenerated file inside a family built on declared supersession would contradict it.

The contract declares what the projection does **not** carry, and the first exclusion is the meaning
of any term. That is the whole distinction between an index and a glossary. A glossary would be a
second statement of the vocabulary, and the family would then have two.

CM-8 is not among its checks and cannot be. Ownership is a semantic determination — settling it for
**candidate** meant reading the Semantic Model — and a clean run says only that declarations and
definitions agree, never that a term sits where it belongs.

## What was found and not carried

**Nothing says when a word must become a term.** A document introducing one must define it, and the
term must sit where its subject matter puts it, but nothing says a word must be introduced at all.
Six terms are declared, defined, and then used nowhere.

The obvious rule would be wrong. Thirty-one terms appear in no document but the one defining them,
and **fifteen carry a requirement in that document's own invariants**. A rule that family vocabulary
must span documents would break every one of them.

This also gives the first measurement of a concern carried unclosed for two revisions — that one
document holds more vocabulary of its own than any other. It owns eleven terms, four are local to it,
and **all four are cited by its own invariants.** It did not invent vocabulary nothing uses. What
survives is whether its subject requires that much, which is a different question and still open. Two
other documents carry five local terms each and have never been the subject of a finding.

**Whether the domain-neutral semantic spaces a runtime recognizes belong in the ontology** is
recorded and not carried. The ontology already defines what is *not* an axis, already rejects axes
that restate a category as a verb, and states the criterion that decides it: whether admitting a
genuinely new kind requires changing the ontology. A set derived from one realization's kinds is the
named failure. The evidence that would settle it does not exist yet.

## What comes next

Both open findings are answerable by the same exercise, now specified: an independent author,
working from the standard alone, closing a vocabulary for a profile with no sight of what any
realization arrived at. Convergence is evidence the spaces are canonical; divergence is evidence they
were one realization's artifacts. Asserting them into the ontology first would destroy the experiment
that could justify them.

That trial is the first gate of a programme to build a second realization from the standard and
nothing else — and then to have the two of them discharge the same claim. The standard and a profile
are the oracle. The existing realization is not one of them; it is one observation against it.

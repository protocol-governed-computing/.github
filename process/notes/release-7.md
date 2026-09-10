release 7 — a rule set is not evidence that its rules can fail

dev/6 asked what happens when one part of the business needs another. **dev/7 asks a question about
the machinery itself: how do you know a governance surface governs anything?**

Every check in this composition reported clean at the start of this cycle, as they had for several
before it. The build was green. What that established was that the surface is well-formed — every
reference resolves, every schema validates, every handler is registered. It established nothing about
whether a single rule in it had ever refused anything.

It turns out that four of them could not.

## A field that governed nothing, and contradicted the one that did

An invariant declares where it is enforced. It turned out to declare it twice.

`core.enforcement_stage` is read by four mechanisms, one of which decides whether an invariant is
compiler-enforced at all. `assert_projection.enforcement.phase` is declared on fourteen of
eighty-eight invariants, never alone, canonicalized by the compiler, copied into the derived
assertion — and **read by nothing**.

The two disagreed on seven of the fourteen. One disagreement was a contradiction inside a single
machine block: the authoritative field excluded the invariant from compile-time assertion while the
second asserted it ran there. Both statements sat in one declaration and could not both be acted on.

They were moot, because nothing read the field. That is precisely why they had accumulated.

**The repair is removal, not reconciliation.** Enforcing agreement between an authoritative field and
an unread restatement enforces a derived copy. The schema already refuses undeclared keys, so
deleting the property makes its reappearance a hard build failure rather than a review miss — the
constraint becomes structural instead of vigilant.

A second finding was corrected on the way. The dimension itself was said to be an unconstrained
string wanting an enum. It already had one, a closed six-value set, and the probe that proves it
would have passed before the work started. Coarse consequence and absent constraint are different
defects, and only the first was true.

## A check scoped away from the builds where its subjects live

One invariant verifies that every runtime-enforced business rule is bound to a real enforcement path.
It declared a scope field, and the compiler's import filter excludes scope-bearing invariants from a
domain build — correctly, because that field names *the allow-list a constraint carries*, and
importing one surface's allow-list into a domain would assert the wrong rule entirely.

Three of the four invariants carrying that field carry an allow-list. The fourth did not. It had
borrowed the field to mean *this is a platform concern*, and the filter read it as what it means.

So the check ran only in the build where its subjects cannot exist, and was absent from every build
where they can. Runtime business rules are authored in domains.

The repair is one field, three lines. What makes it evidence is that the same probe was run twice:

    an unwired runtime invariant, authored in a domain

      before   the domain build fails on an unrelated check; the wiring check is silent
      after    the domain build fails on the wiring check

The same document, the same defect, judged twice. What changed is not a check's strictness but
whether the check was there at all.

The general fix — make scope select applicability rather than admission — was also run, against a
genuine surface-closure invariant. It produces seven violations in the first domain tried: one
surface's allow-list asserted against a domain that never declared it. **The exclusion rule is
load-bearing and the defect was never in the rule.**

## A domain may state a rule about what it owns, and nothing can check that it did

A domain is the authority for the subjects it introduces. If it cannot state a constraint over them,
the platform ends up owning rules about subjects it does not own.

That capability is not missing — a conformance workload already authored an invariant, and it
compiled. What is missing is the chain that makes an authored invariant *governed*. The two rules
that close it — every invariant is declared by a constitution, every invariant is paired with its
assertion — govern artifact kinds that are not domain-instantiated, so **neither is ever imported
into a domain build.** The one domain invariant in the composition was an orphan by the platform's
own definition, and the mechanism that exists to say so was structurally absent from the only build
that could see it.

The ruling is yes, and not yet: authorship is granted together with the chain that governs it, never
before. Granting it first is one line per domain and yields ungoverned invariants — the defect this
release spent itself deleting.

A check now proves the chain by name, and the workload's authorship is withdrawn until the governance
exists to back it. **That withdrawal costs something and the release says so:** the invariant carried
the workload's capability allow-list, and nothing now refuses a third transform. The platform's own
surface closure cannot substitute — it carries the platform's list, which is the seven-violation
counterfactual above.

## The measurement that found the rest

The design language stands at 820 rules over 229 distinct identifiers. Before this cycle, **63 had
ever been observed to fail.** Roughly seven in ten had been authored, resolved, sealed into the
composition, and never once seen to refuse anything.

Thirty-one negative documents later, **222 have.** Every phase from P0 to P5 and P8 is complete; P6
is one short and P7 nine short, and both remainders are named rather than rounded away.

No rule was authored and no design construct added. Forty-five lines of behaviour changed. What the
pass produced is evidence, and the evidence is what found everything below.

**Two rules could not fire at all.** A template may scope a business-language constraint to named
columns, and the author writes those names in the spelling authors use. Parsed rows are keyed by the
literal column headers. The lookup was a case-sensitive prefix match, so every lookup returned empty,
every cell appeared to contain nothing, and every rule so scoped reported clean on every document
always — twenty-five column declarations across four phases. The unscoped form reads the headers
directly and worked, which is why it survived: the mechanism was demonstrably functional in the
configuration nobody had broken.

**Nine registers could lose a column undetectably.** A required column was matched by prefix against
any header, and `Source Finding` begins with `Source`. Matches are now consumed once, exact before
prefix. The rule was correct throughout; the defect was in how a correct rule resolved its subject.

**One fixture had carried a real defect since it was written.** Repairing the first of those turned
it red on a design identity sitting in a business-language column. The document did not change. The
rule started working.

**Five rules have no subject anywhere.** Cross-subdomain reach — that a subdomain owns what it holds
and another may read it and never write it — is governed by five rules and exercised by nothing. Every
business-intent document in the workspace declares the register empty. The rules are correct,
admitted, reachable, and have never had a subject to judge. That is a change to author, not a test to
write, and the release records it as such.

One discipline runs through all of it, and it is the sentence this release is named for. It is the
older guardrail — *a check that has never been observed to fail is evidence of nothing* — turned on
the rule set itself.

## A fork that was two-thirds delivered and did not know it

`register_coverage` asked whether a design can state, for an artifact it amends, every fact that
artifact carries. It was carried for several cycles as scope-collapsed.

Checked against the language as it stands: an amended artifact **can** state its subdomain — the
mandate carries it, the renderer reads it there, and a rule refuses an amended artifact missing from
it. A vocabulary that extends nothing **can** say so, through a declared-emptiness sentinel the
renderer distinguishes from an unfilled cell.

Both were fixed by work done since, and **neither fix was recorded against the fork.** That is why it
read as parked rather than as two-thirds delivered.

What remains is a different question from the one it asks: whether an artifact every field of which
is compiler configuration belongs in the design language at all, or to the generator that derives it.
No change has yet amended a build configuration, so there is nothing to rule on. The dossier closes
unbuilt on that record.

A related claim was retired the same way. `tc construction emit` had been carried as the last
generator without an agreement check. It was not — everything it writes is already compared, the
generated build manifest included. What was unchecked sat one level up: the list of domains the
acceptance corpus reads is hand-kept, and a base-code domain's dossiers cannot enter it at all. The
harness now asks that question of the workspace rather than of a second list.

## The specification learned two things about its own realization

The transformation fragment carries a comparison method and records its answers rather than asserting
their absence. It had been run once. Running it again against this composition:

**Two of the three recorded realization gaps have closed**, and neither closure had been recorded.
Preservation is enforced at every handoff, not two. And *a rule that passes because a value is absent
has not passed* is no longer enforced nowhere — it is what the corpus pass did, and the run learned
that the principle has **two mechanisms**, only one of which is about the document.

**One gap in the model, found and closed.** The realization carries a governance mechanism the
fragment had no home for: a refusal the business declares and the design must discharge. The fragment
used *refuse* only of documents and rules. It now carries §15.23, stated as a property rather than an
enumeration of forms — enumerating them would specify one realization's taxonomy as the model, and
would make the reference realization non-conformant against a fragment written from it.

## The composition

Unchanged in shape: seven domains, 398 artifacts — one fewer than release 6, and the difference is
the withdrawn invariant rather than anything lost. Composition conformance passes over five rules.
Every domain validates its own behaviour against criteria its change requests declared.

What changed is what the composition can say about itself. Two governance closure relations are now
proved by name rather than assumed. 222 of 229 rule identifiers have been seen to refuse a document
written to violate them. And the ten that have not are listed, with the reason each is a change to
author rather than a document to cut.

release 4 — the design and construction compilers

dev/4 implements two compilers that turn a business problem into governed artifacts. They conform to
the PGC rule that behaviour is declared and separated from implementation, they are rules-driven and
deterministic, and **who does the work does not change the result**: a human, an interactive AI, or an
API-driven LLM produce functionally the same artifacts, because none of them decides anything the
rules do not admit.

## What the two compilers do

**The Design Compiler** takes a problem statement written by a business author and drives it through
nine gated phases (P0–P8) into an authoring mandate. Each phase produces one document made of
*registers* — tables with declared columns — and each phase has a rule set that decides whether that
document may proceed. A document that passes is ADMISSIBLE; one that does not names exactly which
rule it broke and where.

    P0 seed          what the business said, reorganised
    P1 change request  the seed restated with a citation per row
    P2 domain model  what already exists, verified against the composition
    P3 analysis loop the decisions: reuse it, extend it, or author it new
    P4 business model the decisions consolidated
    P5 business intent what the subdomain will be
    P6 governance intent who owns what
    P7 design intent  the artifacts, their identities, their wiring
    P8 mandate       the order to build them in

**The Construction Compiler** takes P7 and P8 and renders the artifacts themselves. Before it runs it
measures *construction completeness*: every fact an artifact needs, counted against what the design
states. Below 100% it refuses, because a fact the design does not state is one the generator would
have to invent — and a generator that invents design is a second, ungoverned design authority.

The two are separate because they fail differently. A design failure is "the register is incomplete".
A construction failure is "the design is valid and still does not determine an artifact". Different
people fix those, and merging the compilers would blur them.

## Why the worker does not matter

This is the property the release exists to establish, and it rests on three separations.

**Rules are data, not code.** A rule says which register it governs, which check evaluates it, and
with what parameters. The checks are mechanisms — "is this cell empty", "does this citation resolve",
"does this identity exist in the composition" — and know nothing about why they matter. Adding a
governance rule never requires new code.

**The rule sets are sealed into the composition.** Each phase's rules are compiled into that phase's
workflow artifact, so the command-line tool and the running system judge the same document by the
same rules. When the two drift apart, a check reports it rather than letting them disagree quietly.

**The gates are human and the drafting is not.** A worker may draft the prose that fills a register.
It may not decide admissibility — that is the rule set — and it may not answer a question the business
has not answered, because an unanswered question is now inadmissible rather than something to fill in.
Given the same business answers, any worker yields the same admissible registers, and the renderer
turns those into the same artifacts byte for byte.

So the pipeline is assistive where it is drafting and deterministic where it decides. Swapping the
worker changes the wording of a rationale. It cannot change what is built.

## What dev/4 added

The phases existed before this release. What they could not yet do was govern a change that *extends*
a domain someone already built — and every business change after the first one is that. Driving such
a change end to end exposed the gaps, each closed in the compiler rather than worked around:

- **A phase can no longer hedge.** A cell reading `UNRESOLVED` used to satisfy every rule that asked
  whether a cell was filled, because none asked whether what filled it was an answer. A question the
  business has not answered is now refused, and belongs in the register that exists for asking.
- **A question cannot be handed forward unanswered.** A change request carrying a blocking
  clarification is refused. Otherwise the next phase answers it by invention.
- **The subdomain purpose survives.** The one paragraph no artifact can derive is written once by the
  business author. It used to disappear between phases and get rewritten later by someone else; a
  phase that changes it must now say it is changing it, and say what it adds.
- **Both directions of "was it asked for" are checked.** Nothing the business asked for goes unbuilt,
  *and* nothing gets built that the business never asked for.
- **P1 became a compiler pass.** Once blocking questions had to be resolved before it, P1 decided
  nothing — it is the seed's rows plus a citation each. So it is now generated rather than written,
  and a question found while writing it goes back to the seed instead of entering there.
- **Extending an artifact is a first-class act.** Construction now renders amended artifacts, not only
  new ones, and refuses an amendment that would quietly delete what it does not restate.

## Architecture nuances worth seeing

**An extension redeclares the artifact whole; it is not a patch.** Construction renders an amended
artifact from the design alone, and the result replaces what was there. The alternative — merging a
change into whatever is currently on disk — would make the built artifact a function of the design
*and* the current system, so the same dossier would build differently against two systems and
"the design determines the artifact" would stop being true. The cost is that a design must restate
what it is not changing, so a check compares each amendment against what it replaces and refuses one
that narrows it.

**Admission and quality are different axes.** Whether a document may proceed is decided by its rule
set and nothing else. How good it is gets a separate score, which may be poor for an admissible
document that carries declared open questions. Collapsing them would make the score a second, softer
gate. It follows that anything admission refuses must not also be scored — otherwise one defect is
counted twice — and that rule is now written into the scoring policy itself.

**Dossiers are evidence, not artifacts.** The nine documents describe a change to a system; they are
never part of one, and never enter the compiled snapshot.

**Documents passing proves less than it looks like.** Every defect this release closed was admissible
over the full rule set and complete at 100% when it was written. Document checks prove a design
determines its artifacts. Only running the system proves the artifacts do anything, which is why a
change request is not finished until something has run against real stores.

## Operational

The composition is 345 artifacts. Per-phase rule counts are P0 82 · P1 169 · P2 65 · P3 49 · P4 69 ·
P5 62 · P6 46 · P7 97 · P8 34; after changing any rule set, re-seal it and recompile, or the tool and
the system judge differently. A dossier is validated against a named, frozen baseline, re-derived when
a source domain is recompiled rather than copied from a manifest.

Standing checks: 37 end-to-end phase cases, 37 documents compared between the tool and the running
system, 5 projection cases, and construction acceptance at 51/52 artifacts with zero field differences
— the one exception being a hand-authored file no design renders.

Naming: this repo's own dossiers live under `transformation/dossiers/`. `cr_` is reserved for business
domains, where a change request is raised against a governed system; a change to platform or base code
is managed by git.

The `dev/4` branch history has the working detail — every rule, and the failure that produced it.

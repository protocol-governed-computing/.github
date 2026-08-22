# Parked Rulings & Items — Open PGC Standard

Rulings made about the standard family, and items considered for it and deliberately not admitted
yet. An item is here because it is not driven by a use case, not because it is wrong.

## Spec → reference-implementation roadmap — DELIVERED

**Unparked and delivered** as `standards/doc/realization_map.md`: complete over all twenty-five
normative documents, ~280 invariants, 43 findings, four probes. It went to `doc/` rather than `spec/`
so that a change in a codebase cannot move the standard's revision identity, and it is stated against
a named subject — snapshot `7b6f2699…`, `draft-1` — so it does not age into being wrong. `8a` §6 was
rewritten to name it. The original parking note follows, unedited, because its stated reason for
parking is the reason it could be unparked.

**What it is.** A mapping from each normative document to where the reference realization
demonstrates it — which artifacts, which compile path, which snapshot region, which trace.
Not a tutorial and not an on-ramp: a demonstration that the specification is satisfiable, and
by what.

**Why it is worth having.** An implementer reconstructs this mapping anyway, by reading the
code. Supplying it costs the family nothing it does not already know and saves every
implementer the same rediscovery. It also has a second use: a normative document with no
demonstration is either unimplemented or unimplementable, and the mapping makes which one
visible.

**Why it is parked.** It describes documents that do not exist yet. Twenty-one of twenty-six
are unwritten, so the mapping would be mostly empty and would set the shape of documents
before they are drafted. Write it when there is something on both sides to connect.

**Where it goes when unparked.** The non-normative annex (Implementation Guidance), not a
profile and not a part. It is evidence about the realization, and §4 bars the realization from
supplying authority.

## Canonical kind enumeration

**Ruled.** The Kind Vocabulary's normative subject is the mechanism and semantics of kind
vocabularies, not the membership of any particular vocabulary. Canonical kind enumeration belongs
to the applicable platform profile.

The existing canonical-kind list remains working material in `kind_vocabulary.md`, alongside this file until
the Normative Platform Profile is developed, at which point it is the candidate content for that
profile's declared vocabulary.

## Conformance sections in normative documents

**Ruled.** Each normative document keeps its conformance section, naming its conformance subject
and the obligations that subject must satisfy. Revisit as a family-wide pass when the Conformance
Model is drafted — not per document.

The division is:

```
Parts I–VI documents    what must be true of the subject
Part VII                how conformance to those truths is claimed, demonstrated,
                        measured, and classified
```

Removing the sections before Part VII exists would make the individual documents incomplete against
the root standard's own requirement that a document state its conformance obligations in terms an
independent implementation could discharge.

**When the Conformance Model is written, do not move the existing sections into it wholesale.** They
answer a different question. Compare:

| Document says | Conformance Model should say |
|---|---|
| *obligation* — a runtime conforms when it consumes only permitted inputs, verifies before execution, makes no governed decisions, produces required evidence, and refuses where declarations do not answer | *evaluation* — conformance requires evidence that acceptance occurred before execution, that no prohibited decision affected a governed consequence, that refusal occurred for uncovered cases, and that substitution testing demonstrates no hidden authority |

The first is a normative obligation; the second is an evaluation method. The pass should derive the
second from the first, leaving the first in place.

**Carry into that pass: some obligations cannot be discharged by observing runs.** Effect
disposition is the clearest case — a non-effecting declaration is satisfied on every run in which
the effect path is not taken, so no number of successful executions establishes it. What establishes
it is the absence of any reachable path, direct or transitive, from realization to effect. The
Conformance Test Specification will therefore need structural analysis and not only execution
testing, and the obligations requiring it should be identified rather than discovered late.


## Governed Transformation — comparison run records

Carried forward from the transformation specification fragment when that fragment was subsumed into
the Governed Transformation standard. The standard itself excludes review history; these records are
kept because a recorded gap that later closes is evidence about the method, and deleting it would
leave the method unfalsifiable.

Section references below are to the **retired fragment**, not to the current standard. The mapping
for the two that still matter: fragment §12 grounding → standard §11.1–§11.2; fragment §14 "a rule
that passes because a value is absent has not passed" → standard §5.1 and TR-3a; fragment §15.23
declared refusal and discharge → standard TR-23.

**One realization gap remains open across both runs**: nothing checks that a contract preserves
state another contract wrote.

### First run

**Gaps in the realization, not in this model.** Nothing checks that a contract preserves state
another contract wrote (§13). Human content entering once (§10) is enforced at two handoffs and not
at the rest. "A rule that passes because a value is absent has not passed" (§14) is stated by this
fragment and enforced nowhere — a live instance was found the day it was written.

**A gap this model had, now closed.** Grounding was specified as an interface without saying what it
must answer. A realization able only to enumerate cannot express a rule that compares a design
against one named existing artifact, and will migrate such rules to later, weaker checks while
remaining formally conformant. §12 now requires it.

**Correctly absent, and deliberately so.** How a realization derives its test fixtures, where a
dossier is stored relative to the system it changes, and how change requests are named are method and
convention. They belong to a realization and would not survive contact with a second one.

### Second run

**Two of the first run's three realization gaps have closed, and neither closure was recorded until
this run.** Preservation is now enforced at every handoff, not two: each of the eight carries at
least one rule reconciling what it received against what it passes on. And §14 is no longer enforced
nowhere — the realization made every rule identifier it declares fail on a document written to
violate it, and the pass found two rules that could not fire at all, nine registers whose missing
column was undetectable, and one live defect in a fixture that had never been reported.

**A gap in the realization, unchanged.** Nothing checks that a contract preserves state another
contract wrote (§13). It was the first run's first finding and is the only one still open.

**What §14 turned out to mean, which the first run did not know.** A rule passes because a value is
absent in more than one way, and only one of them is about the document. A rule whose parameters name
a column the register does not have reads every cell as empty and reports clean; a check that
resolves a column name by prefix is satisfied by a longer sibling, so a register can lose a column and
report clean. Both were live, in a realization that reported green, and neither was reachable by
reading the rule. **A rule set is not evidence that its rules can fail.** §14 states the principle;
what a realization must do about it is demonstrate refusal, not declare intent.

**A gap in this model, found by this run and closed by it — §15.23.** The realization carries a
governance mechanism this fragment had no home for: **a refusal the business declares and the design
must discharge.** A business states an operation the system must refuse; the design carries the
refusal out. Until now this fragment used "refuse" only of documents and rules, and said nothing
about a refusal that is *subject matter*, travelling from a business statement to a design that must
account for it. It is not realization detail: any transformation whose business can say *"the system
must never do X"* faces it, and it presumes no host capability beyond the three §16 already requires.

**What §15.23 deliberately does not say.** It does not enumerate the forms a discharge may take. The
realization admits three — performed by a step, deferred to a named owner under a stated condition,
or discharged by the governance surface — and a fourth, prohibition by absence, is designed and
unbuilt. Enumerating them would specify one realization's taxonomy as though it were the model, and
would make the reference realization non-conformant against a fragment written from it, which is not
how an invariant should arrive.

**Why the second clause is there.** A discharge can be declared, accurate in every cell, and still
not discharge anything: the realization's sharpest probe names an outcome the step really reports and
routes it to the ending that *completes* the act. Nothing that reads the declaration alone can see
it. So the invariant requires the discharge to be checked against what it does — the same distinction
§14 draws for rules, applied to a design's own statements.

**Correctly absent, confirmed against a second body of evidence.** Register identity — which
registers exist, what each is called, what a phase names them — remains realization detail; a
comparison by register name finds fourteen concepts with no home here and every one of them is a
register name. So is the quality score's shape (§8 governs its use, not its scale), so is how a
realization decides a phase has said enough. And **cross-subdomain reach** — that a subdomain owns
what it holds and another may read it and never write it — is correctly absent too, but for a
different reason worth stating: it presumes a host with subdomains and stores, and §16 requires only
three host capabilities, none of which is that.


## Supersession — realization migration state

Carried forward from `SUPERSESSION_MODEL.md` when its semantics were subsumed into the Supersession
standard. The standard states what supersession is; the realization work below is what applying it
to the current composition requires, and it was still outstanding when the file was retired.

**The live finding**: the `blockchain` composition carries three references to a superseded workflow.
Under referential closure (SU-5) it does not compile. That is the correct first casualty — the rule
finds a real defect on its first run.

Two existing version pairs are *not* affected, because nothing declares them superseded:
`STRUCTURE_BUILD_PLATFORM_CONFIG_V0` and `STRUCTURE_FIGURE_OF_MERIT_POLICY_V0`. Whether they should
be declared so is a separate, smaller act.

## What must change, and what it invalidates

| layer | change |
|---|---|
| `software_governance` | `INVARIANT_SUPERSEDED_NOT_REFERENCED_V0` and its assertion; the artifact constitution states that `Supersedes` is a governed relation and that a superseded artifact is unreachable |
| `protocol_compiler` | read `Supersedes` as a compiled fact; assert closure; omit superseded artifacts from the dispatch and intent projections while keeping them canonical |
| `protocol_runtime` | nothing — an artifact absent from dispatch is already unreachable |
| `transformation` | nothing further; P7 states it and construction writes both headers today |

**What it invalidates immediately:** the `blockchain` composition, which carries three references to a
superseded workflow. cr_04 must re-point `IN_ACTOR_VERIFIED_V0` — or retire it too — and re-point both
transport ingresses at the accept and reject workflows, before the domain will compile under the new
invariant. That is the correct first casualty: the rule finds a real defect on its first run.

**What it does not invalidate:** the two existing version pairs. `STRUCTURE_BUILD_PLATFORM_CONFIG_V0`
and `STRUCTURE_FIGURE_OF_MERIT_POLICY_V0` are not declared superseded by anything the compiler reads,
so the invariant does not fire on them. Deciding whether they *should* be is a separate, smaller act —
and once declared, the closure check will name every reference that has to move.

**Recompile:** every domain, because the assertion set changes.



## Specification plan — residue

The planning artifact `specification_plan.md` was retired when the specification it planned was
written. It carried twelve unresolved questions (U-01 … U-12). Every question it raised at
*specification* level is now answered:

| Was | Answered by |
|---|---|
| U-02 where canonicalization lives | required to exist, scheme unspecified — `4c` §2.2, MB-3 |
| U-03 what a snapshot address means | identity derived from content — `3b` §4, `4c` |
| U-04 conformance model and tiers | `7a` — and **tiers refused**, CF-11 |
| U-05 the snapshot boundary | constituents and construction obligations — `3b` §2, `4a` §5 |
| U-06 when transformation is specified | `4d` |
| U-07 inspection and assembly as tooling | inspection is a first-class boundary (`5b`); assembly is construction (`4a`) |
| U-09 numbering scheme | `0z` §2 |
| U-11 house style | `0z` §4 |
| U-12 conformance test kit | `7b` |

What remains from that list is not specification: U-01 (which components a platform has), U-08 and
U-10 (repository naming and staging). Those are arrangement questions a profile or an organization
answers, and the family declines to (`6a` §7, `6c` §11).


## Charter — two contradictions, resolved in the family's favour

`RFC-0000-charter.md` was retired. It predated the specification family and conflicted with it on
two load-bearing points; both are resolved **for** the family, and the charter's positions are
recorded here so the question is not reopened as though it were open.

| Charter position | Family position | Ruling |
|---|---|---|
| §1.1, §2.1 — the more *executable* authority wins; "an RFC never overrides the conformance suite" | `0z` §3 — where a document and a realization disagree, **the document governs**, and the disagreement is resolved by ruling | family. An executable that overrides its specification makes the specification descriptive |
| §5 — conformance is equivalent observable behaviour against a **reference trace** over a normative platform surface | `7a` — conformance is per-subject discharge across four classes; `7a` §5, `8a` §2 — resembling a reference realization establishes nothing | family. Reference-trace equality is one comparative discharge, not the definition of conformance |

Also retired with it, deliberately: the five-authority layer model (architecture, barred from
normative text by `0z` §4), the Conformance Reference as a privileged artifact, and the RFC
lifecycle ceremony. The minimum of the last — that revisions are declared, superseded, and claimed
against — is now `0z` §5.1.

## Rejected framings of the same item

- **"Bootstrap Profile" / "Minimal Conformance Profile."** Proposed as a normative floor: the
  smallest set of declarations that constructs, seals, and executes a governed no-op. Rejected
  as premature — fixing a conformance floor before the Conformance Model exists decides what
  conformance is by accident. A floor is derived from the model, not the other way round.
- **"Getting Started" / "Hello World."** A tutorial. Belongs with the reference realization's
  own documentation, not in the standard family.


---

# Rulings from the realization-map pass

Three findings against the documents were opened by the map and are ruled here. Two are resolved
against the finding; one is narrowed and upheld. Each states what changes and what that invalidates,
per `4e` §9.

## SU-5 vs SU-3 — supersession is impossible as written

**The finding.** SU-3 requires the successor to declare the relation, which necessarily names the
predecessor's identity. SU-5 forbids anything in the governed system referencing the predecessor, and
`4e` §4 forecloses the obvious narrowing: *"The requirement is **strict**: no reference, not no
executable reference. A system that mentions a retired identity has not finished retiring it."* Read
literally, the two cannot both be satisfied and no supersession conforms.

**Ruled: the finding holds. SU-5 is over-broad and is narrowed.**

SU-5's subject is **dependency**, not mention. §4's strictness clause exists to defeat a different
evasion — the claim that a non-executable reference is harmless — and it overshot into forbidding the
declaration SU-3 mandates.

**The decisive evidence is not textual.** The reference realization enforces SU-5 with a handler that
walks an artifact's entire machine block for references — deliberately total, on the stated grounds
that "a handler that looked only where references are *expected* would miss the one place a design put
an identity nobody anticipated." That handler carries:

```python
DECLARATION_KEYS = {"supersedes", "superseded_by"}
...
if key in DECLARATION_KEYS:
    continue
```

An independent implementer, enforcing SU-5 as written, hit the contradiction and carved out exactly
this exception — because without it nothing can ever be superseded. That is `0z` §3's case precisely:
a realization exposing a requirement that could not be met.

**What changes.** SU-5 gains the exception, and §4 states its own scope:

> **SU-5.** Where `X` supersedes `Y`, nothing in the governed system MUST reference `Y` **other than
> the supersession declaration SU-3 requires**, and the closure MUST be determined during
> construction.

§4's strictness paragraph gains a sentence distinguishing a **dependency** on the predecessor from the
**record** of its retirement — the first is what referential closure forbids, the second is what makes
the retirement declarable at all.

**What it invalidates.** Nothing discharged: no conformance claim exists. Blast radius is SU-5's text
and one paragraph of §4. No other invariant cites SU-5. The realization needs no change — it already
implements the corrected rule.

## IN-13's scope — reads by parties, or by any process?

**The finding.** IN-13 requires that no read path exist outside a declared read operation. The
realization has several direct readers of the sealed snapshot. The map recorded the scope as unsettled
and asked whether "read path" reaches the system's own construction and checking tooling.

**Ruled: the finding does not hold. `5b` settles it, and the answer is broad.**

The map read IN-13 in isolation. Read with §2, §12 and IN-14 the document is unambiguous, and it
answers *against* the convenient reading:

- §2 forecloses the tooling exemption by name: inspection "is not a debugging affordance, a developer
  convenience, an administrative back door, or **a tool that happens to read files**," and the reason
  given is that a read path "will be used — **by tooling**, by operators, by other systems."
- §12 closes the observability route: "a side channel opened for observation is an ungoverned read
  path, and §2 applies to it exactly as to any other."

**So tooling is in scope. IN-14 is what bounds it, and cleanly:** *inspection MUST NOT be performed
against a representation that has not been sealed.* A pre-seal read is therefore not inspection at
all — it is construction, governed by Part IV. That gives a criterion needing no judgment call:

| Read | Under | Why |
|---|---|---|
| construction reading its own in-flight state (`s8_verify`) | Part IV | pre-seal; IN-14 puts it outside `5b` |
| acceptance verifying a snapshot (`verify_snapshot`, `warm_boot`) | `3b` §7 | a governed determination *about* a snapshot, not a question asked *of* it |
| anything reading a **sealed** representation | `5b` | inspection, whoever performs it |

**This converts a finding against the document into a finding against the realization**, with two
named instances:

- **`protocol_runtime examine`** — reads the sealed snapshot through its own `locator`/`parser`/
  `reporter` and answers questions about it to a person. No `si.` operation is involved. This is the
  side channel §12 describes.
- **`.github/process/frontmatter_fidelity.py`** — reads `snapshot/` directly.

**And the realization already demonstrates the correct pattern.** `transformation/design/sealed.py`
needed a sealed rule set and went through `inspector.api.query("si.artifact.show", …)` rather than
opening the file; when the observation pipeline could not supply what a check needed, the answer was
to author `si.rule_set.list` — a new declared read operation — rather than to open a side channel.
That is §12's rule followed exactly, by the same codebase that breaks it twice elsewhere.

**What changes.** Nothing in the family. The map's entry is corrected: IN-13 moves from *unsettled*
to **violated by the realization**, and IN-14 from *partial* to demonstrated for the `si.` surface.
Two work items are created, and `runtime examine` is the larger — it is a whole read surface that
should be expressed as `si.` operations.

**Worth stating because it is uncomfortable:** the reading that exonerated the realization was the
one the map reached first, and it was wrong. The document was clearer than the finding claimed.

## Is `4d` over-specified? — narrowed and upheld

**The finding.** `4d` introduces eleven terms, none defined in Part I, all the vocabulary of
`transformation/`; it carries twenty-four invariants, the largest set in the family; several
correspond to specific lessons this workspace learned and recorded. The concern is `0z` §3's
prohibition on describing an implementation and declaring the description to be the standard.

**Ruled: the general finding does not hold. One clause is over-specified and is narrowed.**

**The vocabulary concern does not survive its own test.** `8a` §4.7 asks whether an alternative model
satisfying the semantics can be shown to conform, and for the introduced terms it plainly can:

| Term | The semantic requirement under it | An alternative may |
|---|---|---|
| **register** | governed content lives in a bounded declared surface, never in prose (TR-2) | use typed records, tables, forms — any bounded declared shape |
| **rung** | business-level statements must not name constructed identities (TR-6) | have two levels instead of nine, and call them anything |
| **phase**, **gate** | admissibility and acceptance are distinct determinations (TR-12) | have one phase; TR-14 is then vacuous, not violated |

Each names a real distinction. `0z` §5 permits a document to define its own terms, and renaming is not
an escape from the requirement.

**One clause fails the test.** TR-17, via §13:

> Sufficiency MUST be measured before realization — **as the proportion of required facts the design
> states** — and realization MUST refuse below the declared threshold.

The parenthetical specifies *how* sufficiency is computed (a ratio) and the clause presumes a scalar
with an ordering (a threshold). **Neither is the meaning**, and §13 states the meaning one line
later: *"A generator that supplies a fact the design omits is a second, ungoverned design authority."*

A conforming alternative could discharge that by **per-artifact determinability** — for each artifact
to be realized, does the design fix every field it needs? — refusing on the first that does not, with
no proportion and no threshold anywhere. Under `4d` as written that alternative does not conform,
though it satisfies the requirement more directly than a ratio does.

**The realization is itself the evidence.** `tc construction emit --require` defaults to **100.0** —
the point at which the proportion carries no information and the measure is equivalent to
per-artifact determinability. The scalar is not load-bearing in the only system that implements it.

**What changes.** TR-17 and §13's first bullet are restated over the requirement rather than the
mechanism: *realization MUST NOT proceed from a design that does not fix every fact the realization
needs, and the determination MUST be made before anything is written.* How sufficiency is measured,
and whether it is measured as a proportion at all, becomes a realization's choice.

**What it invalidates.** Nothing discharged. TR-18 (a realized artifact is a function of the design
alone) is unaffected and carries the weight. The realization needs no change; its default already sits
at the semantic reading.

**What is not ruled, and stays open.** Whether `4d` was *derived* from the realization is not settled
by finding one over-specified clause, and it is not a defect on its own — `0z` §5.1 says experience
from a realization may occasion a revision, only that it may not decide one. **`4d` carries the
highest inverse-derivation risk in the family and is the document to re-review clause-by-clause
against `8a` §4.7.** TR-17 is the demonstrated instance; the review is what would establish whether it
is the only one.

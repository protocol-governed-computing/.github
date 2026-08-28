# G1 — Independent Realization Experiment Protocol

**The governing document for NOVA G2.** It fixes what a realization worker may see, what it must
produce, how its decisions are classified, and what counts as success — **before** the realization
begins, so that the validation exercise is not itself ungoverned.

It does not tell anyone how to build a PGC realization. A protocol that supplied architecture would
become the second design authority the whole programme exists to detect.

## 1. The question under test

> Can a system that discharges a conformance claim against a named profile and revision be built
> from the standard, that profile, and nothing else?

Not *can PGC be implemented*. Not *is this a good implementation*. The subject is the **standard's
sufficiency for realization**, and the measurable outcome is a discharged claim.

**G0 answered the adjacent question** and its results are inputs here, not open items: a profile can
be authored from the standard alone (`NPP-E`), the family determines no kind vocabulary (`2d` §1),
and seventeen candidate findings across three runs produced no undeclared gap.

## 2. Permitted inputs

| | |
|---|---|
| the standard | `spec/` at a **pinned commit**, named in the run's `REVISION` |
| the profile | **`NPP-E`** and its scope register — the only G0 run that was uncontaminated |
| general technical knowledge | languages, libraries, storage, tooling, unrelated to any PGC realization |

**A pinned commit, not a frozen revision.** CF-1 binds the *claim*, made at G3. A commit is
immutable already. `draft-4` stays open through G2 so that what this run finds can be repaired in
the revision opened to receive it.

**`NPP-E`'s scope register travels with it.** Without it the worker cannot tell which of the
profile's constraints the family required and which the G0 commission fixed — and would read
commissioner scope as normative.

## 3. Prohibited inputs

Everything G0 prohibited, and it prohibits more, because a realization worker has to search for
ordinary engineering answers and the surface is wider:

- any PGC reference implementation — source, tests, architecture, repository history, snapshots;
- any other profile, including `NPP-C` and `NPP-D`;
- any prior run's deliverables, registers, or evaluations;
- non-normative architecture discussion, papers, or agent memory;
- **anything found by going looking.** The standard names its own subject; searching for that name
  may reach an existing realization. Do not search for one; stop if you encounter one.

**Two independence boundaries apply, and no others:** the author of `NPP-E` must not build the
system, and the builder must not have had access to G0's findings or to any excluded material. G0
run `NPP-D` showed why the second cannot be met by prohibition alone — it inherited its
predecessor's vocabulary through shared context, and a rule about handed-over material does not
reach what a worker remembers.

**No fresh-worker requirement stands between G2 and G4.** The same worker may do both, and normally
should: G4 transforms the system G2 built.

## 4. The firewall is environmental, not tool-level

G0 could remove the network-capable surface outright — authoring needs no execution. **G2 cannot.**
A worker that can build and run can reach the network, and no tool restriction binds it.

**G2 runs in an offline container or VM, from before the worker reads a line.** The reading is the
longest stretch of the run and the one where curiosity most easily reaches for a search box; nothing
in reading, or in writing a manifest, needs a network. Staging dependencies *between* reading and
building would leave that whole period outside the firewall.

Dependencies are staged into the running environment, and the staging is itself governed:

- the worker reads first, then declares what it needs as a manifest — it cannot say what it needs
  to build with until it knows what it is building;
- the manifest is recorded as a realization-freedom decision — *what it chose*, not *what we
  supplied*;
- the commissioning side stages exactly the manifest **into the environment the worker is
  already in**, and records what was staged;
- **a mid-run staging request is a finding about the environment, not a licence.** Grant it, and
  record that the isolation was broken and when.

Choosing the stack is the worker's — specifying it would make this protocol an architecture.

## 5. What the worker records

**Provenance, not interpretation.** Carried forward from G0, where handing the worker an
interpretive taxonomy answered the finding it was meant to measure.

```
Matter:        what had to be decided
Source basis:  exact citation(s) by document and section — the standard,
               the profile, this protocol, or none
Claim type:    expressly required by source | expressly permitted by source |
               inferred from source | chosen by author | unresolved
Reasoning:     why the source does or does not determine the matter
Confidence:    high | medium | low
```

**Three registers, named by who is left holding the question** — G0's third instrument repair:

| Register | Holds |
|---|---|
| **determinations** | decisions the worker made, whatever settled them |
| **matters the worker could not resolve** | *not* matters the family declined to determine — those are determinations |
| **scope this protocol fixed** | constraints from here or from `NPP-E`'s scope register |

**Plausibility is not a source.** An answer that felt obvious carries claim type *chosen by author*
unless the worker can quote what determined it.

## 6. How the claim is discharged — the hard exit criterion

**G1 must identify the normative basis for G2's discharge, or G2 must not start.** It is identified,
and it is **disposition C: a conformance suite is deliberately outside the family.**

That is not a gap. Seventeen G0 candidates converged on one position held across `6a` §7 and §11,
`4c` §8, `2d` §1, `2b` §10, `3e` §12, `3d` §7, `7b` §6 and `2c`: **the family specifies meaning and
declines form.** Encoding, syntax, canonicalization, schema, signature mechanism, publication and
fixtures are each named somewhere as a realization's or a profile's to choose.

So the claim is discharged as `7a` and `7b` specify, and not otherwise:

- the worker states **which claims `NPP-E` supports** that its system claims;
- for each, a **demonstration** with declared, identified **fixtures** — `7b` §6: fixtures *"MUST be
  part of what a claim supplies"*;
- **including negative demonstrations.** `7b`: a fixture set containing only well-formed material
  cannot exhibit a refusal, and a claim whose fixtures are all valid has no negative demonstrations
  however many it lists;
- **obtainable by a party that did not build the system.** `7b` §6: *"a demonstration against
  material an evaluator cannot obtain is not a demonstration to that evaluator."* This is the
  operative constraint on G2 — not a schema.

**The worker does not invent a test oracle.** A realization that supplies its own standard for what
counts as conforming has become a second authority over conformance, which is the defect this
programme exists to detect.

## 7. Classification, after the run

The commissioning side classifies. The worker is given none of this.

| Class | The entry shows | Finding? |
|---|---|---|
| **0 — protocol scope** | this protocol or `NPP-E`'s scope register fixed it | no, and no evidence either way |
| **1 — realization freedom** | the standard deliberately leaves it open | no |
| **2 — determined by source** | the standard or the profile settled it | no |
| **3 — delegated, underspecified** | delegated without enough to decide | **yes** |
| **4 — ambiguity** | two readings, incompatible systems | **yes** |
| **5 — omission** | no normative source at all | **yes**, serious |
| **6 — reference-shaped assumption** | needed something knowable only from an existing realization | **yes**, the most valuable |

**The worker never sees this table.** It records five claim types and a source basis; you assign the
class. Nothing in the worker's commission names a class, and that is deliberate — naming class 6 to
a worker tells it an existing realization exists.

**How a record becomes a class:**

| Claim type recorded | Source basis | Class |
|---|---|---|
| expressly required by source | the standard or `NPP-E` | **2** |
| expressly required by source | this protocol or the scope register | **0** |
| expressly permitted by source | the standard or `NPP-E` | **1** |
| inferred from source | cited, but the text does not say it | **3** or **4** |
| unresolved | cited, and the source delegates without deciding | **3** |
| unresolved | cited, and the readings conflict | **4** |
| unresolved | none | **5** |
| chosen by author | none, *and* proceeding required reconstructing a convention | **6** |

**Class 5 and class 6 are separated by one question**, and the record alone will not answer it: did
the worker choose freely among workable options, or was there a shape it had to arrive at for
anything to fit? The second means something outside the standard was determining the answer. Read
the reasoning, not the label.

**Audit classes 0, 1 and 2 hardest** — the ones about to be recorded as *not* findings. Read claim
type against source basis: *expressly required* citing text that does not require it, or *inferred*
where the text is plain, are the entries that move.

**Class 6 is what G2 exists to find, and G0 produced none of it.** Authoring a profile does not
press on the standard the way building does. If G2 also produces none, that is a strong result about
the standard; if it produces several, they are the most valuable findings the programme can
generate.

## 8. Success and failure

**Success** is a realization that discharges at least one claim `NPP-E` supports, with
demonstrations and fixtures an outside party can obtain, every determination in one of the three
registers, and every entry carrying a source basis and a claim type.

**Failure** is a determination in the system that appears in no register; a citation that cannot be
quoted from the standard or the profile; a prohibited input consulted; a test oracle invented; or a
claim asserted without a demonstration that could have failed.

**A blocked run with a precise account of the blockage is a success.** If the standard and `NPP-E`
together do not support building a claimable system, that is the most important thing G2 could
establish, and it is established by stopping rather than by inventing a way through.

**A complete realization with an empty findings register is the outcome to trust least.**

## 9. What G1 does not decide

- **The architecture.** Language, storage, process topology, module boundaries, interfaces — all
  realization freedom, and specifying any of it would make this protocol a second design authority.
- **Whether `NPP-E` is a good profile.** It is the profile. Defects in it are G2 findings against
  the profile, recorded, not repaired mid-run.
- **What G3 compares.** Comparative conformance is its own gate. G2 produces one realization and its
  evidence; it does not produce a comparison, and it is not evaluated against the reference.

## 10. Closing G2

G2 cannot close without: the realization; its three registers; the conformance evidence; the
staging manifest with a record of what was staged and whether isolation was ever broken; the
commissioning side's classification of every entry; and a **disposition** for each classified 3–6.

Only then are the defects repaired in `draft-4`, the revision frozen and tagged, and G3 permitted to
name it.

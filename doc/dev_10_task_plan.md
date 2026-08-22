# dev/10 — task plan

Three tasks. **They are ordered by dependency, not by appetite.**

```
A  realization map          what the spec requires vs what the RI does
        ↓ tells you what B touches, and what C should say
B  namespace representation fb.* / pgc:: — authority and concern separated
        ↓ settles the identifiers C will describe
C  human text alignment     non-normative block, template-driven, not authoritative
```

Doing B first means migrating 1,407 occurrences before knowing which of them the specification
actually objects to. Doing C first means writing prose about identifiers that are about to change.

---

## Rules that hold across all three

- **Direction is not symmetric.** Validate the **RI against the spec**. A realization "informs this
  family by exposing concepts that were missing, distinctions that were conflated, and requirements
  that could not be met; it never supplies authority" (`0z` §3). Where the two disagree, the document
  governs and the disagreement is resolved by **ruling**.
- **`draft-1` stays marked and unedited.** Spec changes are revisions *superseding* it (`4e` §9),
  declared against a named predecessor, stating what they change and what that invalidates. A
  predecessor that was edited is not a predecessor.
- **Every finding is recorded** in `.github/doc/parked_rulings.md` — including the ones resolved
  against the specification. A ruling that exists only in a commit message will be re-litigated.
- **No governed content changes for convenience.** If a task is blocked by an invariant, that is a
  finding, not an obstacle.

---

## A — Realization map

**Deliverable:** the mapping `8a` §6 describes, one row per normative document.

For each document in `standards/spec/`, record where the reference realization demonstrates it —
which declarations, which construction path, which region of the sealed representation, which
evidence. Where nothing does, classify:

| Finding | Means | Resolution |
|---|---|---|
| **unimplemented** | the RI could satisfy it and does not | RI work item |
| **unimplementable** | the RI cannot satisfy it as specified | **finding against the spec** — ruling, then revision |
| **over-specified** | the document names a mechanism while believing it names a meaning | `8a` §4.7 — finding against the spec |

**Start where correspondence is densest**, to establish the map's shape before the hard ones:

- `3b` Snapshot → `snapshot/` (manifest, canonical, indexes, evidence, trust)
- `4a` Governed Construction → `protocol_compiler/compiler/stages/`
- `5b` Governed Inspection → the `si.*` operation identities

**Known gaps to confirm or refute first** — four architectural invariants have no counterpart in the
RI's own invariant list, and the comparison to date is document-level only:

- **AI-4** determination precedes effect
- **AI-7** refusal dominates
- **AI-14** every determination evidenced, including refusals
- **AI-16** evidence checkable without its producer

**Done when:** every document has a row, every gap is classified, and every spec-side finding has a
ruling.

---

## B — Namespace representation

Follows the ordering `AUTHORITY_VS_CONCERN_RULING` sets for itself. Plan and inventory:
`software_governance/doc/namespace_map.md`.

**1. Ruling — done.** Authority and concern are distinct; a concern may be governed without
constituting a boundary.

**2. Canonical representation.** Give authority and concern **separate declared carriers**. The
requirement is stated — GO-11, MB-7, ID-12, and `4c` §5 — and the *encoding* is deliberately open.
This step precedes enforcement because **a predicate needs a declared field to test**; every current
candidate reads the collapsed identifier and cannot distinguish an unlisted namespace from an
illegitimate one.

**3. Enforcement predicates.** Two, both obligations the ruling created:

- a boundary that cannot demonstrate distinct authority and bounded jurisdiction is **refused**
  (`2e` §3.2 five questions, §3.3 independence);
- a concern classification alone is **refused** as grounds for a boundary (CA-6).

Each must be demonstrated capable of refusing before it counts (CD-4, `7b` §4).

**4. Migration.** 1,407 occurrences, 532 files, 6 repos. Not confined to declarations — assertion
handlers key on invariant FQDNs, so the statically enumerated handler registry is in scope. Sixteen
pinned baselines go stale and each owes a re-pin and re-approval.

**Two things to settle before step 4 starts:**

- **`STRUCTURE_IDENTITY_V0` declares `method: module_path`** while `assert_fqdn_namespace_authorized`
  states path-derivation was replaced by authorization. Which is true determines whether migration
  edits declarations only or moves directories. This is also `4c`'s standing conflict — declared
  identity is authoritative over position (MB-6, ID-1, ID-9) and discovery is filename-driven. The
  settling test is **relocation** (`4c` §10).
- **`blockchain` carries three references to a superseded workflow.** Under SU-5 it will not compile
  once referential closure is enforced. That is the correct first casualty — the rule finding a real
  defect on its first run.

**Done when:** authority and concern are separately determinable, both predicates refuse something,
the composition compiles, and no baseline is stale.

---

## C — Human text alignment

**Deliverable:** a template for the **non-normative** block carried alongside machine blocks, and
the artifacts brought into line with it.

**The constraint that governs this task:** `MB-1` makes the machine block the *sole normative
declaration surface*, and everything outside it "MUST NOT determine anything."

So the template:

- **carries nothing load-bearing.** No value it holds may be read by anything, resolved against
  anything, or relied upon by any determination.
- **is not authoritative and cannot be.** The question "what if the template and the machine block
  disagree?" does not arise — the template declares nothing to disagree with.
- **exists for the reader**, and its job is terminology: an artifact's prose should call things what
  the specification calls them, so that reading an artifact and reading the standard do not require
  translation.

**Where the vocabulary comes from:** Part I. `1a` is the terminology authority, and `1a` §12 makes
its distinctions binding on documents — the template extends the same discipline to artifacts.

**Do this last**, because A tells you which terms the RI is currently using wrongly and B settles the
identifiers the prose refers to.

**Done when:** the template exists, artifacts follow it, and nothing outside a machine block is read
by any mechanism.

---

## Release 10

Scope is A + B + C. Unlike release 9, this one moves governed content: the snapshot id **will**
change, every domain recompiles, and baselines re-pin.

Cut it when B's step 4 is complete and the composition is green — not when A is, since a map with
findings and no remediation is a report rather than a release.

Release 9 is the rollback point.

# G0 run `NPP-D` — disposition of F-1, F-2, F-3

These three survived the run's contamination because they are checkable against the documents
without relying on the author's independence. Checked.

**All three declined. Each is a declared exclusion, not a gap.**

| | Matter | Class | Where the family declares it |
|---|---|---|---|
| **F-1** | no canonical representation of a profile, and no identity-to-document resolution | **1** | `6a` §11: *"**The form a profile takes** — its encoding, structure, or how it is published."* Obtainability is still required — `6a` §9 ID-1 obliges that a checking party can obtain the same profile, and `7b` §6 holds that *"a demonstration against material an evaluator cannot obtain is not a demonstration to that evaluator."* The obligation exists; the mechanism is deliberately unspecified |
| **F-2** | no trust-root verification mechanism | **1** | `3e` §12 names both halves: *"**Integrity or signature mechanisms.** Any serves…"* and *"**The trust root.** Supplied by a profile and by the checking party, never by this family."* |
| **F-3** | no payload grammar for profile-defined kinds | **1** | `2c` treats schema as one realization and not privileged: *"a document schema is one realization and is not privileged."* The kind contract's obligations are specified; its form is not |

The author of `NPP-D` knew this in at least one case — F-1's own reasoning says the standard *"says
the form of a profile is unspecified"* — and filed it as a finding regardless. That is the same
register misplacement dispositioned for run `NPP-E`, and it has the same cause in the commission's
wording.

## Across all three runs: seventeen candidates, no undeclared gap

| Run | Candidates | Undeclared gaps |
|---|---|---|
| `NPP-C` | 9, reclassified to 7 | 0 |
| `NPP-D` | 3 carried for checking | 0 |
| `NPP-E` | 8 | 0 |

**Every candidate landed on something the family had already marked** — `6a` §7 and §11, `4c` §8,
`2d` §1, `2b` §10, `3e` §12, `3d` §7, `7b` §6, `2c`. Three authoring passes probing for the edges
of the standard found only edges the standard had already drawn.

That is what the *does-not-specify* apparatus is for, and it is the strongest positive result G0
produced. It is not a claim that the family has no gaps. It is evidence that the gaps an author
reaches for first are ones the family has already declared.

## The pattern, and what it settles for G1

All seventeen are one position held consistently: **the family specifies meaning and declines
form.** Encoding, syntax, canonicalization, schema, signature mechanism, publication, fixtures —
each is named somewhere as a realization's or a profile's to choose.

The consequence the authors kept reaching is real: **a profile claim cannot be checked mechanically
from the family alone.** That is not a defect. It is the design position, stated in five documents.
Conformance is discharged by demonstration and evidence against declared obligations, not by
schema-checking an artifact.

**This settles G1's hard exit criterion.** Of the three permitted dispositions for the missing
conformance suite, the answer is **C — a suite is deliberately outside the family.** G1 must
define G2's discharge method in those terms rather than pretend an automated instrument exists.

**And it sharpens what G2 must produce.** A realization claiming a profile discharges that claim
with demonstrations and evidence a party who did not build it can obtain and check — `7b` §6's
obtainability rule is the operative constraint, not a schema.

## Disposition

- **F-1, F-2, F-3: declined.** None carried against `draft-4`. No repair to the standard follows.
- **G1 conformance-discharge basis: disposition C**, recorded above, with the reasoning.
- **Commission repair** already recorded under `NPP-E`: rename the registers so *unresolved* means
  unresolved by the author, not by the family.

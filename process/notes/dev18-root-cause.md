# dev/18 — why the work keeps circling

## What happened

The goal was set at the reckoning: a coherent dev/18, ready to merge, no v6 cut. The remaining list
was frozen at eight items. Since then:

| Item | Planned as | Became |
|---|---|---|
| A2 | one platform dossier | one dossier, amended after delivery (`code` added), its figures corrected |
| B | one dossier | one dossier |
| RT-6 | a runtime fix | the fix, plus `cr_03` (a defect the survey found), a CLM fix, a parked transport change |
| Evaluation targets | "none are in use" | a platform dossier, a Collatz dossier with an amended P0 and a failed first emit, a licence-cap dossier that turned out to be a deletion |
| SU-11 re-cut | "re-cut dev/18's semantic changes" | a sweep that found 24 breaches, five restores, one failed option (1a), a platform dossier, then three domain dossiers, the first of which stopped at P3 |

Six dossiers were delivered after the list was frozen, against two planned; a seventh is open. Items
5–8 have not started.

## The pattern

Each round has the same shape: a claim is made, work starts on it, the claim turns out to be wrong
or incomplete, the scope changes, and a new decision goes to you. Counted in this session alone:

- **Four premises were wrong.** "No evaluation targets are in use." "The licence cap is never
  enforced." "Restoring the workflow constitution is enough" (1a). A2's figures counted parts, not
  artifacts.
- **Six tooling gaps were found mid-build.** The design language has no family for a constitution or
  an invariant. P7 assumes `{domain}.implementation`. A workload cannot hold test data. Design does not
  know a step must declare outputs. Construction reads 0 of 0 facts as 0%. A domain build keeps no
  record of which checks ran.
- **Three workarounds became permanent.** Governance artifacts are written by hand and cited as
  REVIEW. `--require 0`. Pinned red-by-design differences.
- **The snapshot was wiped four times** by a failed clean rebuild, and restored by hand each time.

## Root causes

**1. Scope is stated before it is measured.** The frozen list froze names, not sizes. Each item was
sized from memory or from one view of the data, and each time the measurement came after the
commitment. "None are in use" counted nothing; the licence cap was counted from compiled routing
without asking whether anything runs the contract. The reckoning named this ("designing on our
feet"); the fix was a list, and a list does not measure.

**2. Ceremony does not scale with the change.** Every defect, whatever its size, runs P0–P8 with three
gates. A two-line rule change and an eight-artifact domain change cost the same nine documents and
three round trips. For the governance surface the ceremony buys nothing: the design language cannot
express it, so the artifacts are written by hand anyway, and the dossier records a decision already
made. Each gate is a turn in which you approve and I return with the next surprise.

**3. Rules were applied retroactively and absolutely.** SU-11 is now enforced by construction (B). The
re-cut then applied it to changes made before B existed, and to its full depth: every published
identity, every re-point, every test. "Coherent dev/18" turned into "every rule holds for every past
change", which has no natural end, because each fix touches identities that are themselves governed.

**4. Fixing a layer exposes the next.** RT-6 found evaluation targets; they found a constitution that
contradicted itself; replacing it needed re-points; the sweep for those found published rules changed
in place; restoring them broke the governance closure check. Each layer is real. Nothing decided in
advance where to stop, so the stopping point was always "the next layer".

**5. The tooling is being finished while it is being used.** The pipeline was built for domain
changes. Platform and workload changes reached its edges, and each edge cost a workaround or a parked
gap in the middle of a dossier.

The common root: **there is no definition of done for dev/18 that can be tested, and no rule for
what is fixed now versus recorded and parked.** Without both, every finding looks like it blocks the
list, and the list grows from inside.

## Mid-course correction

**A. Define done as checks, not items.** dev/18 is merge-ready when:

1. `regression.sh --all` passes as expected, with every red-by-design step explained.
2. No rule in force contradicts another, and none changes what a v5 rule means. Done:
   `routing_lookup`, `published_rules` and the restores.
3. Construction refuses a change of meaning under an old identity. Done: B.
4. Every known deviation is listed where a reader looks for it: the realization map and the release
   notes.

**B. One rule for findings.** A finding is fixed in dev/18 only if it makes a check in A fail.
Everything else is written down in one line and parked. Under this rule the domain re-cuts are
parked: the 18 remaining breaches predate B, v5's sealed copy is unaffected, and they become an
enumerated exception to SU-11 in the map and the release notes.

**C. Measure before stating scope.** No size, count or "none" goes into the SOTU or a plan unless a
command produced it, and the command is named beside it.

**D. Proportional process.** A domain behaviour change runs the dossier pipeline. A governance-surface
edit, which the design language cannot express, runs as a short change note plus the regression,
with one approval.

**E. Protect the build.** The regression copies the snapshot before a clean rebuild and restores it on
failure.

**F. What is left, in order:**

1. Item 5: the map and the standard. The SU-11 entry records the enumerated exception; RT-6, ID-5,
   EX-18 and CP-13 are corrected; the publication rule is written.
2. Item 6: cleanup. The one unpublished, stood-down identity (`VOCAB_DECLARATION_REPRESENTATION_V0`) is
   deleted; `cr_07` is deleted or kept as a record.
3. Item 7: the SoSyM evidence re-run.
4. Item 8: merge-ready, by the checks in A.

The parked list (transport optional fields, the workload and governance gaps in the design language,
the 18 published breaches, short-code references) goes to the next cycle as one file, not into
dev/18.

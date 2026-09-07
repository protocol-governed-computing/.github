release 8 — the documentation said one thing and the surface declared another

dev/7 asked how you know a governance surface governs anything, and answered it by making rules
demonstrate that they can refuse. **dev/8 started as a documentation pass and turned into the same
question one level up: how do you know the documentation describes the system you have?**

The answer, for two repositories, was that it did not — and one of those mismatches was not a
documentation defect at all.

## What the pass found

`protocol_compiler/README.md` was titled `pgs_compiler`. It described Protocol-Governed Systems,
listed a layer table of `pgs_governance` / `pgs_runtime` / `pgs_capabilities`, and directed new
readers to `bachipeachy/pgs_workspace` — the frozen implementation — as the place to start.
`protocol_runtime/README.md` was the same template with the same links. Both documented CLI flags
that no longer exist and omitted commands that do: the compiler recognizes ten artifact kinds and
its README listed nine, missing `TI_`; the runtime has four subcommands and its README documented
two, missing `boot`, which is the repository's distinguishing act.

Every `ARCHITECTURE.md` in the composition opened with **"Release 5. This document is frozen for this
release."** at a release that is now 8. That banner was removed rather than corrected — it is status
metadata in a deliverable document, and bumping it only defers the same staleness.

None of this changed behavior. All of it changed what a reader would conclude the system is, which
is the only thing documentation does.

## `.github` joined the composition

Two files moved out of `standards` and into `.github`: the snapshot assembly contract, and the
optional domain requirements. `snapshot_assembler` and `protocol_runtime` cite the assembly contract
from module docstrings as the contract they implement, and `standards` is private — a citation a
reader cannot follow is not a contract.

`release.sh` gained `.github` in `REPOS`. Its comment had asserted that `.github` "is deliberately
absent: it is the org profile page, never part of a composition," which stopped being true the moment
it carried surface that sibling repositories cite. The rule that replaced it is narrower and
testable: what a public repository must link to does not belong in a private one.

## The authority/concern finding

`software_governance` documented its namespace as `pgc::`. No artifact declares one. All declare
`fb.<concern>` — and `fb` is a **federation boundary**, which `CONSTITUTION_FEDERATION_BOUNDARY_V0`
defines as "a semantic sovereignty construct, not an implementation packaging construct," under an
anti-sprawl rule forbidding speculative creation.

The surface declares one boundary per concern. Both cannot be right.

Applying the constitution's own test to all twenty-six declared boundaries, reading `applies_to_kinds`
and `enforcement.scope` as declared: nine are kind-mirrors whose name *is* the artifact kind they
govern; six contest a single jurisdiction, three of them declaring the identical four kinds; four
contest the snapshot; two claim all sixteen kinds; two declare no constitution at all; three exercise
no jurisdiction whatsoever.

`fb.governance` appeared to be the one survivor. It fails an independence test in the opposite
direction: `CONSTITUTION_GOVERNANCE_V0` declares itself "the root authority … supreme. All other
constitutions derive authority from this document." It is not a peer boundary. It is the platform
authority, encoded as one boundary among peers.

**One modeling error explains all twenty-six, with no exception.** Governance authority — who may
decide — and governance concern — what is being decided about — are orthogonal, and the surface
expresses both through a single identifier, which makes the distinction unenforceable by any check.

Recorded in `software_governance/doc/AUTHORITY_VS_CONCERN_RULING.md`, unratified. A separate finding
records that `governed_by` forms a literal two-node cycle through the supreme constitution, and that
the relation has two possible meanings the surface does not declare.

`standards/doc/spec/03_governance_ontology.md` gained the distinction as specification: Authority,
Concern, Federation and Namespace are four independent concepts. The fragment's existing rejection of
"authority *level*" as an ontology axis was bounded rather than reversed — it governs how elements are
classified, which is a different question from how a universe is partitioned.

## Nothing was migrated

No namespace changed. `pgc::` and `fb.*` are untouched, as is the legacy handler reference the survey
already classifies. The thread is parked, and the ruling carries its own ordered plan: representation
before predicates, because a predicate needs a declared field to test and today every candidate reads
the collapsed identifier. The migration itself is 1,407 references across 532 files in six
repositories, including constants in the statically enumerated handler registry, and sixteen pinned
baselines that would owe a re-pin and a re-approval.

The finding is worth more than the cleanup would have been. A namespace rename would have moved the
collapse into new identifiers; naming the collapse is what makes it fixable.

## What this release contains

Documentation, one specification fragment, two governance findings, and five citation paths. The
composition is unchanged: the build gate rebuilt every domain, assembled, and passed composition
conformance over 398 artifacts throughout.

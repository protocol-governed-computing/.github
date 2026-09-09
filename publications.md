# Publication Record

The declared public identities of this composition, and what each supersedes.

`VERSION` carries the **composition ordinal** — which composition a repository belongs to, a
monotonic integer, written to all ten repositories by the release process. `PUBLIC_VERSION` carries
the **public identity** — the name under which a composition is published and may be named from
outside. This document carries the relation between successive public identities.

**The two are independent and neither is derived from the other.** `4e` §9 holds that a revision is
declared rather than inferred from a number; a public identity computed from the composition ordinal
would be inferred, and an offset between two counters is the kind of undeclared relation this family
objects to everywhere else. A public identity that appears in `PUBLIC_VERSION` and not here has not
been declared.

**They increment on different occasions.** The composition ordinal advances every release cycle,
whether or not anything is published. The public identity advances only when a composition is
published, which is a deliberate act. Cycles that are cut and not published consume an ordinal and
no public identity.

**The number counts publications and asserts nothing else.** It is not a semantic version and
carries no major, minor or patch. A publication that changes everything and one that changes almost
nothing both advance it by one, and the release note for the cycle says which it was.

---

## `v1` — the first public identity

**Supersedes: nothing.** This is the first public identity of the PGC reference platform under this
scheme. No earlier public identity is superseded, because the identities that preceded it were not
public identities: `release-2` through `release-11` were composition tags on a development remote,
and they were removed rather than superseded when publication moved to a single-commit surface.

**Published at composition ordinal 12.** Ten repositories — `software_governance`,
`conformance_workloads`, `business_domains`, `protocol_compiler`, `protocol_runtime`,
`snapshot_assembler`, `protocol_transport`, `snapshot_inspector`, `transformation`, `.github` — each
carrying one commit on `main` tagged `v1`.

**Why it does not start at zero.** `v0` is reserved and will not be issued from these repositories.
It names **RI-0**, the earlier reference implementation, which is a different system under different
governance. Numbering from one is the declaration that this composition does not claim that
lineage — a point that is unanswerable in five years if it is not written down now.

**Not the same `v0` as the standard's.** `standards` declares its own revision identity in its own
`VERSION`, currently `v0`, counting revisions of the specification. A specification revision and a
platform publication are different subjects and their numbers are unrelated. A system claiming
conformance names the specification revision it claims, never this identity.

---

## `v2` — the first citable publication

**Supersedes `v1`.** Same ten repositories, same composition, same governance surface. What changed
is not what the platform is but whether it can be named from outside.

**Published at composition ordinal 13.** The ordinal advanced when cycle 12 was cut; `v1` was
published at ordinal 12 and the cycle that carried it has since closed. The publication therefore
carries cycle 12's work — the NOVA cycle 1 validation result, recorded in that cycle's release
note — and nothing of cycle 13 beyond the ordinal itself.

**Why it was issued.** `v1` was archivable and not citable. Every repository now declares its own
deposit metadata in `.zenodo.json`, so an archive of this publication is attributed under a stated
identity — title, author, ORCID, licence — rather than under whatever a hosting platform infers from
a repository name. A publication that cannot be named by someone outside the project is not
available to the instruments the project cannot run on itself.

**What it does not assert.** The identity counts publications and nothing else. `v2` does not claim
more conformance than `v1`, does not supersede any specification revision, and stands in no declared
relation to the standard's `v0` — which counts revisions of a different subject and advances on its
own occasions.

---

## `v3` — the first obtainable publication

**Supersedes `v2`.** Same ten repositories and the same governance surface. What changed is not what
the platform determines but whether someone outside the project can obtain it and run it, and
whether its boundary failures are governed outcomes rather than exceptions.

**Published at composition ordinal 15.** `v2` was published at ordinal 13. Cycle 14 was cut and not
published — it prepared the repositories as distributions and recorded why an editable install could
not establish that a wheel works. This publication therefore carries the work of cycles 14 and 15
together, recorded in those cycles' release notes.

**Why it was issued.** Two reasons, and the second is why `v2` could not simply be re-cut.

Nine distributions are published on PyPI at `3.0.0`: eight component packages and
`protocol-governed-computing`, which pins them to one composition, so the toolchain is obtained in
one command. PyPI prohibits the short name `pgc`, so the composition carries the full project name;
the import package and the `pgc` command are unchanged.

And the runtime changed. Loading a sealed handler reference ran code the platform does not own, at
two sites that were unguarded: a missing module or a missing optional dependency escaped as a Python
exception rather than a declared refusal, and a refusal that did reach the caller carried no account
of itself. Both now refuse using codes the trace schema already admits. That is a change to governed
execution, not to packaging.

**Why `v2` was not reused.** The distributions published under `2.0.x` were built from cycle 15 and
carry the refusal guards; the commit tagged `v2` is cycle 13's and does not. The documented relation
between the public identity and the published version had therefore already broken before this cycle
declared anything. Re-publishing different content under `v2` would have left a minted identity
naming material other than what it was minted for, which is the failure that content-derived identity
exists to prevent. A new identity was the only honest option.

**What it does not assert.** The identity counts publications and nothing else. `v3` does not claim
more conformance than `v2`, supersedes no specification revision, and stands in no declared relation
to the standard's own revision identity. The published version `3.0.0` names this publication and is
not a semantic-versioning claim about compatibility.

---

## `v4` — what the composition answers, corrected

**Supersedes `v3`.** The same ten repositories and the same governance surface. What changed is what
a snapshot resolves an identity to, what a wheel contains, and which profile a composition claims.

**Published at composition ordinal 16.** `v3` was published at ordinal 15.

**Why it was issued.** Three reasons. Only the first would have justified a patch release; the second
is why this is a new identity.

*An identity published twice resolved by accident.* A domain that consumes a platform capability
carries it as an execution binding, so one identity is published by more than one domain. The
artifact index kept whichever copy a sorted walk saw last, which made resolution depend on the
alphabetical order of the consuming domain's name: `workload` and `transformation` sort after
`platform` and won; `ai_governance` and `blockchain` sort before it and lost. Three of fifteen
affected identities resolved to an execution binding carrying no authored content, where
`si.artifact.show` promises the artifact as authored. The index now prefers the authoring copy.
**This changes what the composition answers, and renaming a domain could previously have changed it
again.**

*The wheels shipped declarations.* `pgc-governance` carried two nested `registry/` trees and
`pgc-workloads` carried a compiled snapshot, `registry/` and `test_payloads/` — in both cases
contradicting the comment directly above the packaging rule that admitted them. The compiler resolves
declarations from `PGC_PLATFORM_ROOT` and never read them, so nothing behaved differently; but a
registry inside a wheel is a second governance surface, and the distribution asserted it carried none.

*Acceptance evaluated one of two identity claims.* A manifest states its identity twice, as
`snapshot_id` and as `composite_hash`. Only the first was checked, so a manifest could carry two
contradictory identities and be accepted. Both are now evaluated.

**The profile in force changed.** `GOVERNANCE_SURFACE_PROFILE_V0` supersedes
`REFERENCE_PLATFORM_PROFILE_V1` and requires no entry workflow: a conformance workload composes like
any other domain rather than being a condition of conformance. The obligation retained is that the
governance surface be *able* to govern a workflow, not that one be present. `REFERENCE_PLATFORM_PROFILE_V1`
is retained unaltered, because the `v3` snapshot claims it and a superseded profile does not
retroactively alter claims discharged under it.

**Why `v3` could not be reused.** `3.0.0` is published and immutable. Beyond that, the material
differs in what it determines rather than only in how it is packaged, so republishing under `v3`
would name material other than what that identity was minted for.

**What it does not assert.** The identity counts publications and nothing else. `v4` does not claim
more conformance than `v3`, supersedes no specification revision, and stands in no declared relation
to the standard's own revision identity. The published version `4.0.0` names this publication and is
not a semantic-versioning claim about compatibility.


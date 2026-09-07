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


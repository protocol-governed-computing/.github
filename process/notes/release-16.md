release 16 — a claim nothing checks is not a claim

This cycle changes what the composition answers, and that is why it takes a new public identity
rather than a patch. An identity published by more than one domain now resolves to its authoring
copy. Acceptance evaluates both identity claims a manifest carries instead of one. The wheels stop
shipping declarations. Seven domains, 410 protocol artifacts, composition conformance PASSED over
five rules.

The cycle began by installing `v3` from PyPI into an empty directory and following the published
instructions. That does not reach a running snapshot. What the attempt found, repeatedly, was not
broken machinery but **claims nothing was checking** — documentation asserting behaviour the code did
not have, tests that had never been run, and checks that looked only one way. The theme is not that
things were wrong; it is that nothing would have said so.

## What was actually done

**An identity published twice resolved by accident.** A domain consuming a platform capability
carries it as an execution binding, so one identity is published by several domains. The artifact
index kept whichever copy a sorted walk saw last, making resolution depend on the alphabetical order
of the consuming domain's name: `workload` and `transformation` sort after `platform` and won,
`ai_governance` and `blockchain` sort before it and lost. Three of fifteen affected identities
resolved to a binding carrying no authored content, where `si.artifact.show` promises the artifact as
authored. The index now prefers the authoring copy, and two testbed cases pin it — one asserting the
resolution does not track domain naming, which is the property rather than the symptom.

**Acceptance checked one of two identity claims.** A manifest states its identity as `snapshot_id`
and again as `composite_hash`. Only the first was evaluated, so a manifest could carry two
contradictory identities and boot. Measured, not inferred: `composite_hash` set to `deadbeef…` was
accepted while `snapshot_id` and `profile` were both refused. Both are now evaluated. The runtime's
own weaker composite and an unused third copy in the assembler are deleted — one determination, one
implementation.

**The wheels shipped declarations.** `pgc-governance` carried two nested `registry/` trees and
`pgc-workloads` a compiled snapshot, `registry/` and `test_payloads/`, each contradicting the comment
directly above the packaging rule that admitted them. Nothing read them, so nothing behaved
differently — but a registry inside a wheel is a second governance surface, and the distribution
asserted it carried none. `pgc-workloads` drops 84% of its size. Three further repositories carried
the same blanket pattern while matching nothing yet; all are narrowed.

**Five test suites existed and nothing ran them. Two were red.** `test_governance_provenance.py`
perturbed an invariant with a YAML comment, but `content_hash` is taken over the *parsed* machine
block — prose declares nothing — so the closure hash could not move and two of its four properties
reported false. `test_warm_boot.py` asserted the runtime's composite against the manifest using a
helper `boot` had stopped calling. All five are now in the check block, and what they check is stated
in the runbook, including the two things that are red by design.

**A check that looked only one way.** `governance_closure` verified that every registered handler is
named by an invariant, never the reverse, and its extractor read raw file text — harvesting a
`handler:` key out of a *violation example* in one artifact's prose and treating a constitution as an
invariant because the string `artifact_kind: INVARIANT` appeared in its prose. It now reads only the
machine block. A duplicated rule row in `CONSTITUTION_ASSERT_V0` is removed.

**The HTTP boundary had been unable to boot since release 10.** When acceptance moved into the
assembler, `runtime.boot` gained an import that `run_http.sh` never provisioned, so every adapter
request died at `No module named 'assembler'`. The CLI was unaffected because the venv installs the
package; the adapter runs on an env-provisioned path by design. `PGC_ASSEMBLER_ROOT` is now required
and exported by all three client launchers. Two releases in which nobody asked the boundary a
question.

**The profile in force changed.** `GOVERNANCE_SURFACE_PROFILE_V0` supersedes
`REFERENCE_PLATFORM_PROFILE_V1` and requires no entry workflow: a conformance workload composes like
any other domain rather than being a condition of conformance. What is retained is that the surface
be *able* to govern a workflow, not that one be present. The predecessor is kept unaltered because
the `v3` snapshot claims it, and a superseded profile does not retroactively alter claims discharged
under it.

## Why this is not bookkeeping

Every defect above was reachable by reading. None was found that way. They were found by installing
the published artifact and using it, and by running suites that had sat unrun — and the two largest
were introduced by changes that were themselves correct: moving acceptance into the assembler, and
making `content_hash` canonical over the parsed block. A correct change with an unchecked consequence
is the shape this cycle kept finding.

So the durable output is not the fixes. It is that the claims now have checks attached: the
domain-authoring path documented for a domain developer is executed on every regression run rather
than described, `si snapshot validate` runs against the snapshot the build just produced rather than
against fixtures, preflight asserts each pyproject's major against the public identity instead of a
comment asserting the two agree, and the release repository states no fact that is generated
elsewhere.

## What this release is for

`v3` was the first obtainable publication. `v4` is the first whose obtainability was tested from
outside — installed from an index into an empty directory, followed as written, and corrected where
the instructions were wrong rather than where the code was.

Two questions are recorded and deliberately not answered here. Whether a consuming domain should
publish under the authoring identity at all — the duplication whose symptom is fixed and whose cause
is not. And whether anything should read a profile's stated obligations: `GS-1` through `GS-3` are
declared and unchecked, because the verifier reads two keys and those are not among them. Both are in
`.github/doc/parked_rulings.md` and neither is driven by a use case yet.

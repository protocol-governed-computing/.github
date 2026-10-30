# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-29 · A platform change may reuse its own domain's artifacts (P3 revision 2)

### Changes made
Work is on `dev/19`. The last commits are `transformation_compilers` `1e35c7d`, `protocol_runtime`
`2d2b14f`, `protocol_compiler` `72caf69` and `.github` `958d05e`.

**Uncommitted from the two previous sweeps**
- `transformation_compilers`, staged: platform fixtures off business domains (the corpus restored,
  the frozen e2e baseline, the design test on the workload, construction acceptance skipping run
  output).
- `transformation_compilers`, unstaged: a route change judged by the phases (`seal.py`, `cli.py`,
  `route_seals.yaml`, `route_seal_test.py`, `dossiers/route_change_judged_by_phases/`, the 3.6
  readiness row, DESIGN_LANGUAGE §9.5).
- `protocol_runtime`: `testbed/pgc/test_step_outcome.py` on the Collatz workload.

**This sweep**

**`transformation_compilers`**
- `registry/schema/REGISTER_SCHEMA_P3_V0.json`: the `reuse_eligible` rule declares
  `own_domain: true`. `tc phase revise p3` recorded **revision 2**: the change's own domain is
  eligible. It widens the rule and refuses nothing it admitted.
- `transformation/design/evaluate/constructs.py` (`_reuse_candidate_eligible`): with `own_domain`, a
  candidate from the change's own domain is eligible, whatever plane the domain serves.
- `registry/design/workflows/WF_P3_ANALYSIS_LOOP_ADMISSIBILITY_V0.md`: resealed in place by
  `tc phase emit`. Transformation recompiled; the snapshot reassembled (602 artifacts).
- `design/p7_design_intent_transformation_baseline.md`: the design of record carries `own_domain`.
- `scripts/testbed/reuse_own_domain_test.py` (new, 3/3), on the route dossier's P3 with one REUSE row:
  - a transformation change reusing `transformation::WF_P0_SEED_ADMISSIBILITY_V0` is admitted;
  - the same row in a `book_library_mgmt` change is refused (`REUSE_CANDIDATE_NOT_ELIGIBLE`);
  - a transformation change reusing `inspection::TE_SI_ARTIFACT_LIST_V0` is refused.
- `doc/DESIGN_LANGUAGE.md`: the `reuse_eligible` row names `own_domain`.

**`.github`**
- `process/regression.sh`: runs `reuse_own_domain_test` after `repoint_callers_test`.
- `process/expectations.yaml`: `reuse_own_domain_test` expects 3/3.
- `process/RUNBOOK.md`: a row for the new test.
- `doc/SOTU.md`: this file.

### Build & test status
- `regression.sh --all` (2026-10-29, working tree): **PASSED, 99/99 steps as expected.**

### Open issues
- **The rule change has no dossier.** It follows the precedent of P7 revisions 4 and 5: a rule-set
  revision is recorded by `tc phase revise`, not designed through P0–P6.
- **The route dossier's P3 stays as delivered,** with AUTHOR_NEW rows only. It was admissible then
  and is now; it is sealed history.
- **`INVARIANT_REUSE_FROM_PERMITTING_DOMAIN_V0` is unchanged.** Its rationale protects other domains'
  artifacts, which the revision still does.
- **The ruling that an authored change is complete at P6 is not in the composition.** It lives in
  `THE_SHAPE_OF_A_CHANGE_V0.md`; it belongs in `lifecycle::CONSTITUTION_CHANGE_MGMT_V0`.
- **P2 to P6 of a route change are written by hand.** Only P1 is projected.
- **The frozen corpus pin** `36bc62a` must survive any squash or published cut.
- **Caller repointing has not run on a real delivery.**
- **The blockchain web client was not opened in a browser** after its repointing.
- **The prose in the blockchain and ai_governance ledgers is not owner-confirmed.**

### Architectural concerns
- Eligibility now has two grounds: the candidate's domain permits reuse, or it is the change's own
  domain. The second reads the document's `domain` header, so a P3 must name its domain truthfully;
  the P2 prior's header is judged with it.

### Next session should start with
1. Commit (the user's step; this includes the two previous sweeps):
   ```
   cd transformation_compilers && git add -A design doc dossiers registry scripts testbed transformation && git commit -m "P3 revision 2: a change may reuse its own domain's artifacts; route changes judged by P0-P6; platform fixtures off business domains"
   cd ../protocol_runtime && git add testbed/pgc/test_step_outcome.py && git commit -m "step outcome test runs on the conformance workload"
   cd ../.github && git add doc/SOTU.md process && git commit -m "regression: own-domain reuse test; route changes judged by the phases"
   ```
2. Next candidate: carry the complete-at-P6 ruling into the lifecycle constitution.

**Priorities (the user):** fix platform defects and decision gaps first. Keep business-domain
parking-lot items on hold unless the new compiler needs one to be assimilated fully and tested.

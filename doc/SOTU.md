# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-29 · Platform tests no longer depend on a live business domain

### Changes made
Work is on `dev/19`. The last commits are `transformation_compilers` `1e35c7d`, `protocol_runtime`
`2d2b14f`, `protocol_compiler` `8be7322` and `.github` `22cd9e0`. Everything below is uncommitted.

**`protocol_runtime`**
- `testbed/pgc/test_step_outcome.py`: runs on the Collatz workload instead of ai_governance's
  reclaim. 8/8.
  - The cases are an admission, transform steps, and a `CS_MUTABLE_JSON_V0` write whose answer is
    replaced for one run.
  - A termination check that will not load, or that breaks, is a fault and is never routed as a
    verdict.
  - The platform's own `CT_PURE_REQUIRE_TRUE_V0` refuses a sequence that did not terminate, and the
    run routes to `EXIT_CONJECTURE_VIOLATED`.

**`protocol_compiler`**
- `scripts/testbed/test_platform_vectors.py`: the domain compiled against the platform is the
  Collatz workload. It carries `CT_PURE_REQUIRE_TRUE_V0` and `CS_MUTABLE_JSON_V0` from the surface.
  3/3.

**`transformation_compilers`**
- `scripts/testbed/semantic_change_design_test.py`: its fixtures are the workload's artifacts:
  - `CC_STORE_RESULTS_V0` and `WF_COLLATZ_CONJECTURE_V0` for referrer accounting;
  - `CT_PURE_COLLATZ_STEP_V0` and `CC_COMPUTE_SEQUENCES_V0` for the transform and its contract.

  24/24.
- **The phase corpus is frozen on its neighbour (your choice).** The corpus cites a neighbouring
  domain's artifacts as business reuse candidates, and Collatz is `reuse_visibility: internal`.
  - `scripts/testbed/e2e_phases_test.py`: `design_baseline()` builds ai_governance from
    `business_domains` `36bc62a`, the revision CR-1 was designed against. The build comes from git
    into `traces/design_baseline_sources/`, with its own transforms on the import path, and the
    live domain is no longer a source root.
  - `scripts/testbed/corpus_p2`, `corpus_p3`, `corpus_p7`, `fixtures/catalog` and
    `testbed/phases/test_payloads`: restored to their content at `8fb030b`. That undoes cr_04's
    repointing, so the corpus cites ai_governance's artifacts as they were, and its prose is true
    again.
  - Case 84 expects three unbound inputs again.
  - `build_fixtures.py` and `build_payloads.py --check` reproduce the corpus with no diff.
  - `differential`, `effectivity_test` and `projection_test` pass.

- `scripts/testbed/construction_acceptance.py`: does not read the workspace root's run output
  (`data/`, `traces/`). It reported the frozen copy's design of record as uncovered.

**`.github`**
- `process/implementation_closure.py`: does not read the workspace root's run output. It reported
  the frozen copy's two retired transforms as absent.
- `process/RUNBOOK.md`: the design baseline's sources, and `test_step_outcome.py` on the workload.
- `doc/SOTU.md`: this file.

### Build & test status
- `regression.sh --all` (2026-10-29, working tree): **PASSED, 98/98 steps as expected.**
- No platform test or fixture now reads a live business domain. The corpus reads ai_governance
  frozen at a revision, and the regression's own business steps run the domains by design.

### Open issues
- **The frozen neighbour is rebuilt on every regression run,** because `traces/` is cleared. The
  rebuild is one compile.
- **Caller repointing has not run on a real delivery.**
- **A route dossier is `change.md` and a seal,** not a P0–P8 dossier.
- **Book's derived-design criteria were written while book was delivered.**
- **The blockchain web client was not opened in a browser** after its repointing.
- **The prose in the blockchain and ai_governance ledgers is not owner-confirmed.**

### Architectural concerns
- **The corpus is pinned by revision, not by a sealed snapshot.** `36bc62a` must stay reachable in
  `business_domains`' history. A squash or a published cut that drops it from the history would break
  the e2e baseline, so the pin must move to a revision that survives it.
- **The workload now carries the runtime's and the design test's platform properties.** A change to
  Collatz's workflow reaches them, as it should, since Collatz exists to prove the platform.

### Next session should start with
1. Commit (the user's step):
   ```
   cd transformation_compilers && git add -A scripts testbed && git commit -m "platform fixtures: design tests on the workload; the phase corpus frozen on its neighbour at 36bc62a"
   cd ../protocol_runtime && git add testbed/pgc/test_step_outcome.py && git commit -m "step outcome test runs on the conformance workload"
   cd ../protocol_compiler && git add scripts/testbed/test_platform_vectors.py && git commit -m "platform vectors test compiles the conformance workload"
   cd ../.github && git add doc/SOTU.md process && git commit -m "platform tests independent of business domains; closure reads no run output"
   ```
2. Choose the next platform defect or decision gap. Candidates:
   - judging a route change by the phases;
   - running caller repointing on a real delivery.

**Priorities (the user):** fix platform defects and decision gaps first. Keep business-domain
parking-lot items on hold unless the new compiler needs one to be assimilated fully and tested.

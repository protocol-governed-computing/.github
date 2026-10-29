# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-29 · Delivery repoints callers outside the domain, and refuses the ones it cannot

### Changes made
Work is on `dev/19`. The last commits are `transformation_compilers` `0df4017`, `business_domains`
`8410d6a`, `protocol_runtime` `2d2b14f` and `.github` `3098c10`. Everything below is uncommitted.
Only `transformation_compilers` and `.github` changed. No module of the derive route changed, so no
route seal is needed.

**`transformation_compilers`**
- `scripts/repoint_callers.py` (new). It handles callers outside a delivered domain: every source file
  in a workspace repository that names the domain's artifacts.
  - A caller is code, a script, a payload, a fixture under a `testbed/`, or the workspace process
    (the runbook).
  - `check` refuses when a caller names an artifact the change retires with no successor, or another
    domain's declaration names a changed artifact.
  - `apply` repoints every caller of a superseded or replaced artifact to its successor.
  - History is never rewritten: documents, dossiers, designs of record, snapshots, the retirement
    ledger and the route seals.
  - A full name is matched anywhere. A short name is matched only in a file that names the domain.
- `scripts/derive_deliver.sh`:
  - `check` runs right after identities are decided, before anything is written;
  - `apply` runs with the domain's own repointing.
- `scripts/derive_build.sh`: reports what `check` finds, so a rehearsal shows it before delivery.
- `scripts/testbed/repoint_callers_test.py` (new): 6/6 on a temporary workspace.
- `doc/DESIGN_LANGUAGE.md` §9.7: callers outside the domain follow the change.

**`.github`**
- `process/regression.sh` and `expectations.yaml`: the step `repoint_callers_test` (6/6).
- `process/RUNBOOK.md`: delivery repoints every caller outside the domain, plus the test's row.
- `doc/SOTU.md`: this file.

### Build & test status
- `regression.sh --all` (2026-10-29, working tree): **PASSED, 98/98 steps as expected.**
- **Dry run on the real workspace:** with an imaginary supersession, `apply` finds exactly the callers
  that cr_04 and cr_05 needed repointed by hand:
  - `protocol_runtime`'s `test_step_outcome.py`;
  - `semantic_change_design_test.py`;
  - the regression script and the runbook;
  - the phase-test payloads, and the corpus sources they are generated from.

### Open issues
- **The repointing has not run on a real delivery yet.** The test and the dry run cover it.
- **A retired artifact with outside callers needs a person.** Delivery refuses until each caller
  stops naming it. cr_04's e2e fixtures were such a case: each needed a live counterpart chosen.
- **A route dossier is `change.md` and a seal,** not a P0–P8 dossier.
- **Book's derived-design criteria were written while book was delivered.**
- **The blockchain web client was not opened in a browser** after its repointing.
- **The prose in the blockchain and ai_governance ledgers is not owner-confirmed.**

### Architectural concerns
- **Platform tests still use business domains' artifacts as fixtures.** Delivery now keeps them
  current, but each delivery reaches into other repositories' files. Moving those fixtures to the
  conformance workload would remove the reach.
- **Short names are matched by heuristic.** A file that names the domain and uses another domain's
  artifact of the same short name would be repointed wrongly. No such file exists today.

### Next session should start with
1. Commit (the user's step):
   ```
   cd transformation_compilers && git add -A doc scripts && git commit -m "delivery repoints callers outside the domain, and refuses a caller it cannot repoint"
   cd ../.github && git add doc/SOTU.md process && git commit -m "regression: callers outside the domain"
   ```
2. Choose the next platform defect or decision gap. Candidates:
   - judging a route change by the phases;
   - moving platform fixtures to the conformance workload.

**Priorities (the user):** fix platform defects and decision gaps first. Keep business-domain
parking-lot items on hold unless the new compiler needs one to be assimilated fully and tested.

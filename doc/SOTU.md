# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-11-11 · dev/19 prepared as `v7`, the final publication of RI-1

RI-1 closes with `v7`. After it is published, these repositories take no further changes. New work
belongs to RI-2, a separate realization in `~/protocol-governed-computing-ri2` (GitHub org
`protocol-governed-computing-ri2`, packages `pgc-ri2-*`). The standard stays in `standards` and keeps
evolving; it is not frozen.

### Changes Made

**Committed and force-pushed by the user.** `business_domains`, `transformation_compilers` and
`.github` were reset to `checkpoint-dev19-route-frozen` and force-pushed to `origin/dev/19`.

**Uncommitted, for the release commit:**
- **Versions.** Every `pyproject.toml` is `7.0.0` (ten repositories). `PUBLIC_VERSION` is `v7`.
  `pgc_install`'s pins stay at `6.0.0`; `release.sh --publish-composition` regenerates them.
- **`publications.md`.** A `v7` entry: the final publication of RI-1, a genesis with no compatibility
  with `v6`, ten governed changes delivered after the genesis, every distribution at `7.0.0`.
- **Vendored revision.** `transformation_compilers/testbed/frozen/business_domains_36bc62a.tar` holds
  `ai_governance`, `book_library_mgmt` and `blockchain` at `36bc62a`. `scripts/criteria_before.sh` and
  `scripts/testbed/e2e_phases_test.py` extract from it instead of `git archive`, so a clone of the
  published `main` reproduces them. `process/RUNBOOK.md` says so.
- **Docs moved to RI-2** (`~/protocol-governed-computing-ri2/.github/doc/`):
  `AGENT_ARCHITECTURE_COMPARISON.md`, `DECISION_ACCOUNTING_DESIGN.md`, and
  `business_domains/causal_language_model/doc/cr_sequence.md` as `CLM_PARKED_CHANGES.md`.
- **Docs kept:** `BEHAVIOR_OUTSIDE_SNAPSHOT.md` and `DOMAIN_BEHAVIOR_OUTSIDE_SNAPSHOT.md` are findings
  about RI-1 itself. `transformation_compilers/doc/ASSIMILATION_READINESS.md` is cited by a delivered
  dossier, which is never edited.
- `doc/SOTU.md` — this file.

**Decided, not changed:** artifact versions stay as delivered. 47 artifacts carry `_V1`–`_V3` and the
retirement ledger records 99 identities. They are the frozen release's evidence that supersession and
retirement work.

### Build & Test Status
- `regression.sh --all` after the reset (2026-11-11): **PASSED, 99/99 steps as expected.** Snapshot
  `8ad89baa75ce1412bb61dceb5bc5dc11eeba146c96eed600d43c169b2d447982`, 603 artifacts, eight domains.
- `regression.sh --all` after vendoring the revision, frozen sources rebuilt from the tarball:
  **98/99.** `e2e_phases_test` and the three `criteria_before_*` steps pass from the tarball, with the
  expected counts (book 0/8, blockchain 2/9, ai_governance 4/21). The one miss is `demo_script`:
  the demo copies each working tree with `git ls-files | tar`, and `tar` fails on the three moved
  docs while their deletion is uncommitted. With the files restored, `demo_script_check.sh` passed
  12/12. Committing the deletions clears it.
- `release.sh --check`: the build gate passes with the same snapshot id. The preflight fails only on
  the uncommitted changes listed above.

### Open Issues
- **Before publishing:**
  - open the blockchain web client in a browser once; it has not been opened since its repointing;
  - the ledger prose in `blockchain` and `ai_governance` is not owner-confirmed.
- **After publishing:**
  - delete the local `dev/20` that `release.sh` opens; no cycle follows;
  - archive the RI-1 repositories on GitHub as read-only, except `standards`;
  - rebase the standard's realization map onto the `v7` snapshot as its final subject.
- **Left unfinished by design.** These stay as RI-1 leaves them:
  - derive route: the seal requiring `AUTHORED`, mandatory `delivery`, derived seeds declaring
    `CONSTRUCTED`;
  - rules nothing enforces: overlapping in-flight dossiers (`transformation_compilers/CLAUDE.md`),
    validation criteria drawn from P0 on the authored path, governing generation
    (`process/rulings.md`);
  - "caller" is defined nowhere; only a failing regression enforces its meaning.

### Architectural Concerns
- `genesis.yaml` says it is set back to `false` once the cut it declares is sealed. No composition
  follows `v7`, so the reset changes nothing. Leave it `true`, as sealed.

### Next Session Should Start With
1. Commit the release changes, one commit per repository:
   ```
   cd ~/protocol-governed-computing
   for r in software_governance conformance_workloads business_domains protocol_compiler \
            protocol_runtime snapshot_assembler protocol_transport snapshot_inspector \
            transformation_compilers pgc_install .github; do
     git -C $r add -A && git -C $r commit -m "v7: final publication of RI-1"
   done
   ```
2. `bash .github/process/regression.sh --all` — expect 99/99.
3. `bash .github/process/release.sh --check` — expect PREFLIGHT PASSED.
4. `bash .github/process/release.sh --publish`, wait for the Zenodo mints, then
   `bash .github/process/release.sh --publish-composition`, then build and upload `pgc_install`.

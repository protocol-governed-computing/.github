# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-29 · The ledger states where a refused release ends; ai_governance cr_05 delivers cr_02's ending

### Changes made
Work is on `dev/19`. The last commits are `transformation_compilers` `3255262`, `business_domains`
`52fe293`, `protocol_runtime` `8e06ec5` and `.github` `92234cd`. Everything below is uncommitted.

**`transformation_compilers`**: two route changes, each sealed by its own dossier.
- **`dossiers/release_refused_ends_otherwise`** adds a new ledger answer, `release_refused: otherwise`.
  - `ledger_schema.yaml` (rev 7) admits it only on a change that `releases` an identity and has an
    `otherwise` ending. `catalog.yaml` (rev 6) adds the question.
  - `compose.py`: the release step's `VIOLATION` routes to the `otherwise` ending. `BACKEND_ERROR`
    still ends rejected, per `failed_record_ends`.
  - `ledger.py`: two new self-test cases, so the self-test is 25/25.
- **`dossiers/replaces_spent_across_versions`** keeps a delivered `replaces` spent after its
  successor is itself superseded.
  - `compose.delivered()` follows each predecessor's chain of successors through the retirement
    ledger and the design's lineage.
  - `tc phase derive design --retired …` passes the retirement ledger. `derive_build.sh`,
    `derive_deliver.sh` and `tc phase derive seal` all pass it.
  - A `replaces` answer that names nothing held or replaced is still refused; I checked it with a
    misspelled name.
- `route_seals.yaml`: three seals; the last is `replaces_spent_across_versions`. Each re-derived all
  three designs of record unchanged.
- `testbed/ledgers/ai_governance/ledger.yaml`: holds cr_05's answer, and equals cr_05's ledger.
- Docs:
  - `doc/LEDGER_FORMAT_V0.md`: the `release_refused` row;
  - `doc/DESIGN_LANGUAGE.md` §9.7: the spent-`replaces` rule reads the chain.

**`business_domains/ai_governance`**
- `cr_dossiers/cr_05_refused_release_still_active`: the first delivery through the criteria gate.
  - `criteria.yaml` names the routing-closure suite. 3/4 criteria held before the design and 4/4
    after.
  - The full dossier, P0–P8, plus `delivery.md`.
- `WF_RECLAIM_LICENSE_V0` → `_V1`. The registry, the design of record and the testbed are repointed.
- `testbed/routing_closure/execution_validation.py`: criterion 1 is cr_02's own decision again, that
  the reclaim ends at `EXIT_STILL_ACTIVE`. It was written before the delivery.

**`protocol_runtime`**
- `testbed/pgc/test_step_outcome.py`: repointed to `WF_RECLAIM_LICENSE_V1`. 8/8.

**`.github`**
- `process/retired_identities.yaml`: `WF_RECLAIM_LICENSE_V0`.
- `process/expectations.yaml`:
  - self-test 25/25;
  - `derive_meta` names the last seal;
  - the reclaim-closure comment.
  - Supersession stays at 49 relations: `WF_RECLAIM_LICENSE_V1` names one predecessor, as `_V0`
    did.
- `doc/SOTU.md`: this file.

### Build & test status
- `regression.sh --all` (2026-10-29, working tree): **PASSED, 97/97 steps as expected.**
- Re-deriving keeps every artifact: ai_governance 59, blockchain 44, book 57.
- Phase documents are 7/7 admissible for all three.
- ai_governance: owner decisions 21/21, routing closure 4/4.

### Open issues
- **Delivering a domain can reach platform tests** that use its artifacts as fixtures.
  `test_step_outcome.py` was repointed by hand again. Delivery repoints only the domain's testbed and
  client.
- **A route dossier is `change.md` and a seal,** not a P0–P8 dossier.
- **Book's derived-design criteria were written while book was delivered.** They fail 0/8 before and
  hold 8/8 after.
- **The blockchain web client was repointed by text replacement.** It was not opened in a browser.
- **The prose in the blockchain and ai_governance ledgers is not owner-confirmed.**

### Architectural concerns
- **A design of record keeps one predecessor per artifact,** so lineage older than that lives only
  in the retirement ledger. The derive route now reads that ledger. An installed copy without it
  recognizes only the latest replacement.
- **Scripts outside the package are not sealed,** such as `derive_deliver.sh` and
  `criteria_run.py`.

### Next session should start with
1. Commit (the user's step):
   ```
   cd transformation_compilers && git add -A doc dossiers scripts testbed transformation && git commit -m "derive route: release_refused routes a refused release to otherwise; a delivered replaces stays spent across versions"
   cd ../business_domains && git add -A ai_governance && git commit -m "ai_governance cr_05: a reclaim the registry refuses ends as still active"
   cd ../protocol_runtime && git add testbed/pgc/test_step_outcome.py && git commit -m "step outcome test follows the reclaim to V1"
   cd ../.github && git add doc/SOTU.md process && git commit -m "regression: cr_05 delivered, route sealed twice more"
   ```
2. Repoint callers outside a domain at delivery, or move platform fixtures off business domains.
   This is the next platform defect.

**Priorities (the user):** fix platform defects and decision gaps first. Keep business-domain
parking-lot items on hold unless the new compiler needs one to be assimilated fully and tested.

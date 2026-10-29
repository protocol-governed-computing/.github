# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-29 · Derive route: 5.2 holds — book (cr_06–cr_09), blockchain (cr_08–cr_11) and ai_governance (cr_04) delivered through the route

### Changes made
Work is on `dev/19`. The last commits are `transformation_compilers` `8fb030b`,
`business_domains` `36bc62a`, `protocol_runtime` `7a99fe4`, `software_governance` `8801cc8`, `protocol_compiler` `8be7322` and `.github` `6380ada`. Everything
below is uncommitted. The user had staged part of book's cr_06 in `business_domains`. Book's design
files changed after that, so re-stage them.

**`transformation_compilers`**
- `transformation/design/derive/project.py` and `discover.py` (new): project P0 to P6.
  - `project.py` projects P0 from the ledger, P5 from P0 and P6 from P5.
  - `discover.py` projects P2 to P4 from what the derivation observed.
  - `storage()` matches a part's storage structure at any version.
- `transformation/design/derive/cli.py`:
  - `tc phase derive project … [--cr …]`;
  - `identities` drops carried lineage from a successor.
- `transformation/design/derive/compose.py`:
  - **Live versions.** `live_versions`, `as_v0` and `live_names` work in V0 names, then map each
    artifact back to its live version with its lineage. Lineage is now restored for V0-live
    successors too.
  - **A delivered `replaces` is spent.** `delivered()` reads the design of record's lineage. A
    `replaces` answer whose first target the operation's workflow already supersedes is not
    re-applied.
  - **The trail is stable.** `trail_values()` counts a request field as carried when the act's own
    chain binds it. A new act's trail is then the same before the act exists and after.
- `transformation/design/derive/base.py`: `carried_trail` also reads a trail stream bound inside a
  derived recorder.
- `transformation/design/derive/identity.py`: a kept artifact that names a superseded one is
  compared again, with the successors' names in place.
- Sealed files:
  - `ledger_schema.yaml` (rev 6) and `catalog.yaml` (rev 5): the answers `purpose`, `why` and
    `out_of_scope`, and `on_repeat` with optional parts;
  - `ledger.py`: the self-test is 23/23.
- `testbed/ledgers/*/ledger.yaml`: the prose answers, each citing its source.
- Scripts:
  - `scripts/derive_build.sh`: the phase-documents step.
  - `scripts/derive_deliver.sh` (new): delivers one change request.
  - `scripts/derive_suite.py`: a suite's workflow names now follow this run's identities, the
    design's lineage and the retirement ledger, to the last version.
- Tests:
  - `scripts/testbed/semantic_change_design_test.py`: fixtures repointed to ai_governance's live
    artifacts.
  - The phase corpus and the catalog fixtures (12 sources under `scripts/testbed/corpus_p2`, `_p3`,
    `_p7` and `fixtures/catalog/cr_01_catalog`) cite ai_governance's live artifacts: each successor,
    or the live counterpart of a retired contract. `testbed/phases/test_payloads/` are regenerated
    from them (`build_payloads.py`). `e2e_phases_test.py`: case 84 expects two unbound inputs.
- Docs:
  - `DESIGN_LANGUAGE.md` §9.6 and §9.7, including the fixed-point rules and one-change domains;
  - `CONSTRUCTION_MAPPING.md`: `supersedes` adds ACTOR. Input `default` and `format` for CC and IN
    are dropped, because no design of record writes them now.
  - `LEDGER_FORMAT_V0.md`: updated.
  - `ASSIMILATION_READINESS.md`: 3.4 and 5.2 hold.

**`business_domains`**
- book_library_mgmt:
  - `cr_06` to `cr_09`;
  - registry, design and testbed;
  - `execution_validation_owner_decisions.py` (8 criteria).
- blockchain:
  - `cr_08` to `cr_11`;
  - registry, design, testbed and `client/web/*.html`;
  - `execution_validation_owner_decisions.py` (9 criteria).
- ai_governance:
  - `cr_dossiers/cr_04_derived_design`: the whole ledger in one change, with `delivery.md` naming
    each difference.
  - `registry/` and `design/` derived. Two orphaned transform modules are deleted
    (`ct_pure_check_quota_available_v0`, `ct_pure_check_training_status_v0`).
  - `testbed/owner_decisions/execution_validation_owner_decisions.py` (new, 21 criteria);
  - `testbed/routing_closure/execution_validation.py`: rewritten for the derived reclaim, 4/4;
  - `testbed/ai_licensing/test_payloads/`: nine payloads for licensing's acts;
  - `testbed/agent_governance/README.md`: licenses the seed users through those acts.
  - The earlier provisioning payload and `seed_data/license_facts.json` are deleted.

**`protocol_runtime`**
- `testbed/pgc/test_step_outcome.py`: runs on the derived reclaim, with a license that licensing's
  own acts provisioned. 8/8.

**`.github`**
- `process/retired_identities.yaml`: book's, blockchain's and ai_governance's deletions.
- `process/regression.sh`:
  - ai_governance licenses its seed user through four acts before governing an action;
  - new steps `ai_governance_owner_decisions`, `catalog_owner_decisions` and
    `blockchain_owner_decisions`.
- `process/expectations.yaml`:
  - supersession: 49 relations, 49 deleted;
  - human block 588; mapping 191 fields; acceptance 298/298; implementation closure 35;
  - derive fixed points: book 57, blockchain 44, ai_governance 59;
  - the new execution steps.
- `process/RUNBOOK.md`: the derive rows, the ai_governance commands and its suite rows.
- `doc/SOTU.md`: this file.

### Build & test status
- `regression.sh --all` (2026-10-29, working tree): **PASSED, 93/93 steps as expected.**
- Each domain's last ledger equals its test ledger. Re-deriving keeps every artifact: book 57,
  blockchain 44, ai_governance 59.
- Phase documents are 7/7 admissible for all three.
- Owner decisions:
  - book 8/8;
  - blockchain 9/9;
  - ai_governance 21/21, with routing closure 4/4.

### Open issues
- **Delivering a domain reaches outside it.** cr_04 broke three platform tests that used
  ai_governance's artifacts as fixtures: `protocol_runtime`'s `test_step_outcome`,
  `semantic_change_design_test` and the e2e phase payloads. Delivery repoints only the domain's own
  testbed and client. Fixtures outside the domain were repointed by hand.
- **A refused release ends the reclaim at `EXIT_REJECTED`.** The earlier design ended it at
  `EXIT_ACTIVE`. The behavior cr_02 decided holds: the license stays assigned and nothing is
  announced. The ledger has no shape to route a refused release to `otherwise`.
- **The blockchain web client was repointed by text replacement.** It was not opened in a browser.
- **The prose in the blockchain and ai_governance ledgers was drafted from their briefs.** The
  owner has not confirmed it.
- **Book's cr_06 holds three corrections**, each named in its `delivery.md`.
- **The construction mapping now tracks the corpus.** Fields no design of record writes, such as
  input `default`, are not stated. A design that writes one must add its row back.
- 3.6: the rule that a route change runs as its own dossier is enforced only by process.
- 4.4: book's earlier suites predate the method.

### Architectural concerns
- Callers that dispatch by workflow identity must follow `supersedes`. Platform tests should not use
  a business domain's artifacts as fixtures, or a domain's delivery must repoint them.
- The sealed derive documents live in the package, not in a compiled artifact.

### Next session should start with
1. Commit (the user's step):
   ```
   cd transformation_compilers && git add -A doc scripts testbed transformation && git commit -m "derive route: P0-P6 projected (3.4), delivery, fixed points across delivered replacements and new-act trails"
   cd ../business_domains && git add -A book_library_mgmt blockchain ai_governance && git commit -m "book cr_06-cr_09, blockchain cr_08-cr_11 and ai_governance cr_04 delivered through the derive route"
   cd ../protocol_runtime && git add testbed/pgc/test_step_outcome.py && git commit -m "step outcome test runs on the derived reclaim"
   cd ../.github && git add doc/SOTU.md process && git commit -m "regression: owner decisions for three domains, derived domains at their fixed points"
   ```
2. The readiness document's remaining sections (3.6, 4.4), or the decision gaps the deliveries named.

**Priorities (the user):** fix platform defects and decision gaps first. Keep business-domain
parking-lot items on hold unless the new compiler needs one to be assimilated fully and tested.

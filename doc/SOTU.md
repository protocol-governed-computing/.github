# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-29 · Derive route: the route is sealed whole (3.6), and each change's criteria come before its design (4.4)

### Changes made
Work is on `dev/19`. The last commits are `transformation_compilers` `23f0c0d`, `business_domains`
`52fe293`, `protocol_runtime` `8e06ec5` and `.github` `6ed9359`. Everything below is uncommitted.
Only `transformation_compilers` and `.github` changed.

**`transformation_compilers`**
- `transformation/design/derive/seal.py`: seals the route whole.
  - `route_now()` takes the digest of every module of the package and every sealed document.
  - `route_unsealed()` and `route_in_force()` refuse a derivation under a route no seal records.
    `judged_by` names the seal beside the three documents.
  - `unsealed_dossiers()` refuses a seal whose dossier has no `change.md`.
  - `record_seal()` appends to `route_seals.yaml` and refuses a route a seal already records.
- `transformation/design/derive/route_seals.yaml` (new): the first seal, by
  `dossiers/derive_route_sealed`. It covers 13 files, and all three ledgers re-derive unchanged:
  book 57, blockchain 44, ai_governance 59.
- `transformation/design/derive/cli.py`:
  - `tc phase derive seal <dossier> --snapshot … --change …` (new) re-derives every ledger and
    records the seal;
  - `derive meta` refuses an unsealed route and names the seal in force.
- `dossiers/derive_route_sealed/change.md` (new): what the seal changes and covers. The route
  changes made in readiness sections 1 to 5 predate the rule; git and the readiness document
  record them.
- `scripts/derive_deliver.sh`: the criteria gate.
  - The change's `criteria.yaml` names its suites.
  - Delivery runs them before it derives and refuses unless one fails (`criteria_before.txt`).
  - After delivery it requires every criterion to hold (`criteria_after.txt`).
- `scripts/criteria_run.py` (new): dispatches each act a suite names to the version of it the
  composition holds. It can run the domain's transforms from an earlier revision.
- `scripts/criteria_before.sh` (new): runs a domain's criteria against the domain at a git revision,
  compiled and assembled in scratch.
- `scripts/testbed/route_seal_test.py` (new): 5/5.
- Docs:
  - `doc/DESIGN_LANGUAGE.md` §9.5 (the route sealed whole) and §9.7 (the criteria come first);
  - `doc/ASSIMILATION_READINESS.md`: 3.6 and 4.4 hold, and the order list is complete.

**`.github`**
- `process/regression.sh`: the steps `route_seal_test`, `criteria_before_book_library_mgmt`,
  `criteria_before_blockchain` and `criteria_before_ai_governance`.
- `process/expectations.yaml`:
  - route seal 5/5;
  - `derive_meta` names the seal;
  - criteria before the route designed each domain: book 0/8, blockchain 2/9, ai_governance 4/21.
- `process/RUNBOOK.md`: `criteria.yaml` in "A change the derive route designs", a new section "A
  change to the derive route", and two check rows.
- `doc/SOTU.md`: this file.

### Build & test status
- `regression.sh --all` (2026-10-29, working tree): **PASSED, 97/97 steps as expected.**
- Changing a building block by one byte refuses every derivation and fails `derive meta`. Restoring
  it passes both.
- Each delivered domain's owner-decision criteria against the domain before the derive route
  (`business_domains` `36bc62a`):

  | Domain | Before | After | What held before |
  |---|---|---|---|
  | book | 0/8 | 8/8 | nothing |
  | blockchain | 2/9 | 9/9 | behavior the owner kept |
  | ai_governance | 4/21 | 21/21 | the agent-governance denials, which the owner kept |

### Open issues
- **The delivery gate for criteria has not run on a delivery yet.** No change has been delivered
  since it was added. cr_04 to cr_11 predate it, so their dossiers carry no `criteria.yaml`, and
  delivered dossiers are not edited. `criteria_before.sh` shows the same property for them, after
  the fact.
- **Book's derived-design criteria were written while book was delivered,** not before its first
  design. They fail 0/8 before and hold 8/8 after. Book's registration and works suites predate the
  method, and they stay as regression suites.
- **A route dossier is `change.md` and a seal,** not a P0–P8 dossier. Judging a route change by the
  phases is not built.
- **A refused release ends the reclaim at `EXIT_REJECTED`.** The earlier design ended it at
  `EXIT_ACTIVE`. The behavior cr_02 decided holds.
- **Delivering a domain can reach platform tests** that use its artifacts as fixtures.
- **The blockchain web client was repointed by text replacement.** It was not opened in a browser.
- **The prose in the blockchain and ai_governance ledgers is not owner-confirmed.**

### Architectural concerns
- The seal list ships in the package, so an installed copy can verify itself. The dossiers stay in
  the repository, and `derive meta` checks them only there.
- Scripts outside the package, such as `derive_deliver.sh` and `criteria_run.py`, are not sealed.
  They deliver and test a design; they do not derive one.

### Next session should start with
1. Commit (the user's step):
   ```
   cd transformation_compilers && git add -A doc dossiers scripts transformation && git commit -m "derive route sealed whole (3.6); each change's criteria run before and after its design (4.4)"
   cd ../.github && git add doc/SOTU.md process && git commit -m "regression: route seal, criteria before the derive route for three domains"
   ```
2. With the readiness document complete, choose the next platform defect or decision gap. Candidates:
   - a ledger shape to route a refused release to `otherwise`;
   - repointing outside a domain at delivery;
   - judging a route change by the phases.

**Priorities (the user):** fix platform defects and decision gaps first. Keep business-domain
parking-lot items on hold unless the new compiler needs one to be assimilated fully and tested.

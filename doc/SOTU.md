# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-29 · The derive route is frozen; caller repointing is removed

### Why
Caller repointing had never run on a real delivery. Replaying it in scratch over the nine
owner-decided deliveries of 2026-10-29 showed it was wrong. The replay used the workspace as it
stood before them, each change's real map from the retirement ledger, and the fix made by hand as
the oracle.
- **It would have refused 3 of 9 real deliveries.** Book cr_06 had 40 callers, blockchain cr_08 had
  4 and ai_governance cr_04 had 32.
- **Most of the refusals were false.**
  - The flagged files are pinned to an older composition: the catalog fixtures `cr_01`–`cr_05` with
    their own `baseline.json`, and the corpus and payloads judged against the frozen baseline. They
    are history.
  - Two platform declarations name blockchain workflows in prose, as illustrations.
- **`apply` would have rewritten pinned fixtures** to successors their pin does not hold.
- **One refusal was right:** `semantic_change_design_test.py` named a retired ai_governance artifact.
- Root cause: a caller was "any file naming the artifact", where it should be "a file judged against
  the live composition".

The route had grown its own lifecycle: seals, judging its changes, where a change ends, repointing.
The user chose to freeze it rather than retire it. Freezing is reversible, keeps the eleven
delivered changes re-derivable, and stops the growth. `repoint_callers` was the one part both
defective and unused, so it is removed.

### Changes made
Work is on `dev/19`. The last commits are `transformation_compilers` `e6996da` and `.github`
`1b58fb4`.

**`transformation_compilers`**
- Deleted `scripts/repoint_callers.py` and `scripts/testbed/repoint_callers_test.py`.
- `scripts/derive_deliver.sh` and `scripts/derive_build.sh`: the check and apply steps are gone. A
  note says callers outside the domain are repointed by hand, and a pinned file is history.
- `doc/DESIGN_LANGUAGE.md`:
  - §9: the route is frozen, defect fixes only;
  - §9.7: callers are repointed by hand, and the regression names any stale one;
  - §8: an absent register is a finding unless the schema does not require it. This corrects the
    previous sweep.
- `doc/ASSIMILATION_READINESS.md` and `CLAUDE.md`: the freeze, and when the route would be retired.
- The route seal covers only `transformation/design/derive/`, so nothing was resealed.
  `route_unsealed()` is None.

**`.github`**
- `process/regression.sh`, `expectations.yaml` and `RUNBOOK.md`: `repoint_callers_test` removed;
  the delivery paragraph says the domain's testbed and client are repointed.
- `doc/SOTU.md`: this file.

### Build & test status
- `regression.sh --all` (2026-10-29, working tree): **PASSED, 99/99 steps as expected** (one test removed).
- The replay harness is in the session scratchpad and is not in any repository.

### Open issues
- **Parked on dev/19, and off for good while the route is frozen:** the seal requiring `AUTHORED`,
  mandatory `delivery` (a P0_V1 `$id`), and derived seeds declaring `CONSTRUCTED`. Each changes a
  record's wording, not an outcome.
- **Decide whether the route stays.** It stays while owner work through a ledger, such as decision
  accounting, is on the roadmap. If none is, retire it: remove `derive/`, the decision compiler, the
  derive scripts, the seals and the testbed ledgers, and record the six doctrine invariants' retirement
  under a governance dossier. The delivered changes stay as history either way.
- **The frozen corpus pin** `36bc62a` must survive any squash or published cut.
- **The blockchain web client was not opened in a browser** after its repointing.
- **The prose in the blockchain and ai_governance ledgers is not owner-confirmed.**

### Architectural concerns
- What a "caller" is should be stated once: a file judged against the live composition. Files judged
  against a pin are history. The regression enforces this today by failing. Nothing states it as a
  rule.

### Next session should start with
1. Commit (the user's step):
   ```
   cd transformation_compilers && git add -A scripts doc CLAUDE.md && git commit -m "derive route frozen; caller repointing removed after a replay over real deliveries showed false refusals"
   cd ../.github && git add doc/SOTU.md process && git commit -m "regression: caller repointing removed; route frozen"
   ```
2. Next: decide the route's future against the roadmap, or take the next platform defect.

**Priorities (the user):** fix platform defects and decision gaps first. Keep business-domain
parking-lot items on hold unless the new compiler needs one to be assimilated fully and tested.

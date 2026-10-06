# dev/18r — cleanup check, after the replay

Run after step 8, before the map and the standard. It measures dev/18r against what v5 sealed
(`pgc_release/snapshot`) and against the plan's targets (`dev18r-file-ledger.md` §4).

## Verified

- `regression.sh --all`: 69/69 as expected. Four steps are red by design, each with its reason in
  `expectations.yaml`: `admission_contract_fidelity`, `si_snapshot_validate`,
  `construction_acceptance` (two book_library differences) and `blockchain_identity` (the parked
  transport field).
- `pgc_env_check`: no RI-0 dependency is reachable. `implementation_closure`: 36 transforms, every
  module named and present.
- Published identity: none of the 500 identities v5 published changed meaning. One was removed by
  name.
- Disk: no directory without a tracked file, and no stray untracked file.

## Artifacts, against v5

Measured on the compiled compositions: v5 holds 500 artifacts, dev/18r holds 525.

| | Count | What |
|---|---|---|
| New | 27 | 26 compiled identities and `SCHEMA_TRACE_EVENT_V2.json` |
| Stood down | 24 | Published V0s that gained only `superseded_by`; each has a V1 among the new |
| Re-pointed | 36 | Published artifacts whose only change is a reference moved to a declared successor |
| Explanation only | 4 | `WF_P0_…_V0` and `WF_P1_…_V0` gain a generator-source line; `VOCAB_AI_LICENSING_STATES_V0` and `WF_PROVISION_AI_LICENSING_V0` lose the line naming the licence cap |
| Removed | 1 | `ai_governance::CC_ENFORCE_LICENSE_CAP_V0`, by named exception to SU-11 |
| Deletable | 0 | No identity was created and then stood down. Every stood-down artifact was published in v5, so it stays in the record |

**New, by kind.**
- **Platform (7):**
  - `VOCAB_DECLARATION_REPRESENTATION_V0`;
  - the topology constitution V1, and `CONTRACT_CLOSED_V1` and `ROUTING_COMPLETE_V1`;
  - `WF_ROUTING_CLOSED_V0`;
  - the trace constitution V1, and `SCHEMA_TRACE_EVENT_V2`.
- **Transformation (9):** the two judge contracts and `WF_P2`–`WF_P8`.
- **Blockchain (8).**
- **ai_governance (2).**
- **Collatz (1).**

**Re-pointed.**
- 19 platform artifacts name the topology V1 in `governed_by`.
- 7 blockchain entrances and intents, 7 transformation intents, 2 ai_governance workflows and the
  Collatz workflow each name a V1.

## Against the plan

| | Ledger target | dev/18r |
|---|---|---|
| New registry artifacts | 27 | 27 |
| Published artifacts edited beyond stand-down, re-point or explanation | 0 | 0 |
| Unpublished identities stood down before release | 0 | 0 |
| Dossier directories | 4 | 3. Blockchain, ai_governance and Collatz; transformation ran as a change note |
| Platform re-points | 20 | 19. The ledger's twenty was a miscount |
| Published identities removed | 0 | 1. The licence cap; the plan changed at step 7 |

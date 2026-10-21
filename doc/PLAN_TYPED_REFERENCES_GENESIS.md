# Plan — Names Carried as Data Become References, at a Genesis

## Decision

A value that names an artifact is written as a full name and declared a reference by its part.
`artifact::VOCAB_DECLARATION_REPRESENTATION_V0` already decides references by part name (`target`,
`code`, `workflow`). Three parts join its `reference` group: `target_cs`, `event_code`,
`event_type`, `governs`.

- Only a value shaped as a full name (`ns::CODE`) is read as a reference. A constitution's
  `core.governs` holds kind tokens (`CC`, `CS`), so it stays a value. A path (`$.inputs.event_type`)
  stays a binding.
- No part joins `full_name_required`. Its check refuses any value without `::`, which would refuse
  kind tokens, paths and binding descriptions under the same part names.
- The runtime is unchanged: a literal is passed through as written, now as a full name.
- The compiler's closure check then resolves every such name. The two dangling
  `CS_NAME_REGISTRY_V0` names in the storage surface contracts would fail it, so they are removed.

The earlier sketch, a consumer-typed `artifact_ref` input, cannot work alone: the representation
rule refuses a full name outside a reference part before any consumer type is read.

## Genesis

dev/19 is cut as a genesis (`1b` §11), as v6 was.

- `VOCAB_PROTOCOL_KINDS_V1` returns to `_V0`, with no `supersedes`.
- The retirement ledger is emptied.
- `rulings.md`: the v6 baseline ruling is replaced by one for this cut.
- `process/genesis.yaml` declares the genesis. `published_identity_check.py` reads it and compares
  nothing against the sealed composition while it is declared. The ledger rules still hold.

## Values

| Part | Where | Count |
|---|---|---|
| `target_cs` | claim CCs: book_library_mgmt 3, causal_language_model 3, blockchain 1, ai_governance 1 | 8 |
| `event_type` | ai_governance WF node inputs | 4 |
| `event_code` | ai_governance record CCs | 2 |
| `governs` | platform surface contracts (2 dangling names removed) | 9 |

## Files

- `software_governance`: the representation vocabulary; seven surface contracts;
  `VOCAB_PROTOCOL_KINDS_V1` → `_V0`; the invariant prose that names it; the surface map.
- `protocol_compiler`: `_RESERVING` in `assert_vocabulary_symbols_well_formed_v0.py`.
- `business_domains`: eight CCs and three WFs above; each domain's baseline design, regenerated.
- `.github`: `rulings.md`, `genesis.yaml`, `published_identity_check.py`,
  `retired_identities.yaml`, `expectations.yaml`, `SOTU.md`.

## Done when

`regression.sh --all` is green, and every baseline design determines its registry.

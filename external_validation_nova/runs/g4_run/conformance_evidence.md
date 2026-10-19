# Conformance Evidence

## Claim identity

- **Claimant:** this realization, supplied by the builder.
- **Subject:** vocabulary and declaration surface, plus the sealed snapshot and in-process read surface used by the demonstrations.
- **Profile:** `NPP-E`.
- **Family revision:** `f476ea5c06506a3efba1d773a5d42818c9190601`.
- **Baseline snapshot:** `snapshot:70dd9deaa723fa3d808d1bcc9d9171244a8e22378a7719961aadde3339dd80cb`.

The realization does not claim the broader NPP-E claims for profile conformance, construction, evidence, or whole system instance. The G4 transformation and lending-runtime demonstrations are supplied separately in `transformation_evidence.md`; they do not claim full NPP-E transformation/runtime conformance.

## Demonstrations

| ID | Obligation | Subject | Class | Fixture | Demonstration |
| --- | --- | --- | --- | --- | --- |
| D-1 | KV-1, KV-2, KV-4, KV-10 | vocabulary and admitted artifacts | derivational + observational | `sample_artifacts()` in `test_npp_e.py` | `test_valid_snapshot_is_rederivable` constructs the declared vocabulary, verifies the sealed snapshot, and inspects the two admitted artifacts. |
| D-2 | KV-2, MB-8, MB-9 | artifact declaration surface | observational negative refusal | `unknown_kind` created in `test_unknown_kind_is_rule_refusal` | Changes the authoritative kind to `unregistered-kind`; admission refuses with `rule_refusal`, `KV-2`, `MB-9`, consequence `refuse`, and `nothing_proceeded=true`. |
| D-3 | MB-6, ID-4 | admitted artifact set | observational negative refusal | duplicate list in `test_duplicate_identity_is_rule_refusal` | Presents the same identified artifact twice; admission refuses with `duplicate_identity` and no partial admission. |
| D-4 | SN-2, SN-8, SN-9, SN-14 | sealed snapshot | observational negative refusal | mutation in `test_corrupted_snapshot_is_refused_before_inspection` | Mutates a declared artifact after sealing; inspection construction refuses on whole-integrity mismatch before returning material. |
| D-5 | IN-6, IN-9, IN-10 | named-artifact inspection | observational negative refusal | `artifact:absent` in `test_absent_named_artifact_is_refusal_not_empty` | Requests an absent named identity; the read surface refuses rather than returning an empty answer or falling back. |
| D-6 | GC-9, PJ-2, SN-2 | construction and snapshot representation | comparative | two calls over copied `sample_artifacts()` | Reconstructs from equivalent declarations and requires byte-for-byte semantic equality of the resulting snapshot objects and identity. |
| D-7 | SN-2, SN-14, profile integrity parameter | canonical semantic content integrity | derivational algorithm-selection check | fixed semantic object in `test_integrity_algorithm_is_sha256` | Requires the digest of the canonical bytes for `{"a":"NPP-E","z":[1,true]}` to equal the independently computed SHA-256 value; substituting another algorithm fails. |

## Failure capability

Each refusal demonstration uses a fixture that violates the stated obligation. The tests assert the refusal cause, refusal reason, applicable rule identifiers, and `nothing_proceeded`; replacing the violating fixture with valid material makes the same path pass, so each negative demonstration is capable of failing.

## Independent execution

Run from the workspace root:

```text
python3 -m unittest -v
python3 npp_e.py demo
python3 npp_e.py inspect artifact:absent
```

The first command executes all seven demonstrations. The second independently verifies and prints the profile, family revision, snapshot identity, and admitted identities. The third exercises the named-artifact refusal path and exits nonzero with structured refusal evidence.

An evaluator can obtain all fixtures from `test_npp_e.py` and re-derive snapshot identity/integrity with the public functions in `npp_e.py`; no producing process or network service is required.

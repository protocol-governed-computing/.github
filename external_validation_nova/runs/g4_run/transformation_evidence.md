# Transformation Evidence

## Claim identity

- **Subject:** G4 transformation of the NPP-E realization for the lending-library need.
- **Profile:** `NPP-E`.
- **Family revision:** `f476ea5c06506a3efba1d773a5d42818c9190601`.
- **Frozen baseline:** `snapshot:70dd9deaa723fa3d808d1bcc9d9171244a8e22378a7719961aadde3339dd80cb`.
- **Resulting snapshot:** `snapshot:f4220813be0caad738c4d488b46078b2d8704ca533f11c801483cab979b7df43`.

This is a G4 transformation and business-behavior demonstration. It does not claim full NPP-E
transformation, runtime, evidence, or system-instance conformance.

## Governed design

`sufficient_design()` in `transform_npp_e.py` supplies four registers: the business need, exact
baseline grounding by the two actual baseline artifact identities, the artifact design, and a dependency-respecting schedule. Each register
declares `entries`, `empty`, and `rung`; each entry has an address. The design realizes:

- capability contract `lend-copy-to-member`, with `copy_id`, `member_id`, `record_loan`, and the
  refusal `copy_already_on_loan`;
- workflow `lend-copy-to-member`; and
- read operation `current loan record for named copy`.

The result contains the two baseline artifacts plus these three realized artifacts. Artifact
identities and the resulting snapshot identity are derived by `npp_e.py`; no identity is supplied
by the transformation from memory.

## Sufficiency and refusal

Six rules are declared as data and evaluated without short-circuiting. The check-kind set is
closed: `non_empty`, `exact`, `baseline_artifact_exists`, and `contains`. An unknown check kind
refuses hard. Sufficiency is evaluated before `_realize` is called.

The fixture `insufficient_design()` removes `copy_id` from the capability inputs. The transformation
refuses with `insufficient_design`, finding `TR-L4` at the `design` register's
`capability:lending.inputs` location, and `nothing_proceeded=true`. The test
`test_insufficient_design_refuses_before_writing` demonstrates the pre-write behavior. A separate
fixture supplies a baseline whose identity is `snapshot:wrong`; `test_wrong_supplied_baseline_is_refused`
requires the `TR-15` `baseline_identity_mismatch` refusal. The grounding-register fixture changes
the declared baseline identity and fails `TR-L2`.

## Execution proof

`LibraryRuntime` is constructed only from the resulting sealed snapshot and verifies that the
snapshot carries the `record_loan` capability and named status read operation. It records a loan for
`copy-1` and `member-1`, returns the status by looking up that recorded state, and refuses a second
loan of `copy-1` to `member-2` with `copy_already_on_loan`. It also establishes an unloaned status
for `copy-2` from the same record, rather than from an asserted success value.

## Independent execution

From `/Users/bp/g2-nova`:

```text
python3 -m unittest -v test_transform_npp_e
```

The nine tests cover evolution, supplied-baseline refusal, pre-write refusal, exact grounding,
per-rule refusal capability, unknown check-kind rejection, runtime success/refusal, unloaned
status, and same-answer determinism. The fixtures and implementation are local files an evaluator
can inspect and execute without the builder's memory or a network service.
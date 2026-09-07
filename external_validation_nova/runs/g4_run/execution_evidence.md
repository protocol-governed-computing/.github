# Runtime and Execution Evidence

## Claim identity

- **Subject:** execution of the lending workflow from a sealed NPP-E snapshot.
- **Profile:** `NPP-E`.
- **Family revision:** `f476ea5c06506a3efba1d773a5d42818c9190601`.
- **Snapshot consumed:** `snapshot:48fd5a4dcf23cebfe5b993a1d576080857a8a7012c5bfcfb83b468b7f7908d5f`.

This discharges the Runtime and execution claim for the demonstrated lending workflow. It does not
claim full effect-path, substitutability, durable-state, or whole-system conformance.

## Snapshot-driven traversal

The sealed workflow carries one step, its `record_loan` capability binding, and routes for both
enumerated outcomes: `completed -> loan-recorded` and `failed -> loan-rejected`. `LibraryRuntime.execute`
reads the workflow, start step, binding, capability contract, outcome vocabulary, and route from the
snapshot through `Inspection`. It does not select a route from payload, state, or a hard-coded
success/failure branch.

The capability realization reports `completed` when it records a new loan and `failed` when the copy
is already recorded. Execution accepts only outcomes enumerated by the capability contract, then
requires a route for that outcome. An undeclared outcome refuses with `undeclared_outcome`; a missing
route refuses with `unrouted_outcome`; an unknown route target refuses with `unresolved_route_target`.

## Demonstrations

- `test_execution_reports_declared_outcome_and_reads_declared_route` checks the successful outcome,
  path, and terminal.
- `test_execution_routes_declared_failure_outcome` checks the declared negative outcome and route.
- `test_unrouted_declared_outcome_refuses` removes the declared `completed` route, reseals the
  mutated snapshot, and requires refusal.
- `test_routing_mutation_changes_execution_path` changes the declared route to an invalid terminal
  and requires refusal, so hard-coded routing cannot pass the set.
- `test_undeclared_capability_outcome_refuses` supplies a result outside the contract vocabulary and
  requires refusal before routing.
- `test_missing_workflow_refuses_execution` removes the workflow from the sealed representation and
  requires execution refusal rather than fallback behavior.

## Independent execution

From `/Users/bp/g2-nova`:

```text
python3 -m unittest -v
```

The fixtures, sealed snapshot derivation, and execution implementation are local and inspectable by
an evaluator who did not build the system.
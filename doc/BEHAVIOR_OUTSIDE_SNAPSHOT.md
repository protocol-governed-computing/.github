# Behavior Outside the Snapshot

This report lists places where the implementation decides behavior that the sealed snapshot
should decide. It covers `protocol_runtime`, `protocol_transport`, and the platform capability
side effects in `software_governance`. Line numbers refer to `dev/19`.

There are two categories:

- **A: oversight or shortcut.** The snapshot could carry the fact. Code carries it instead.
- **B: cannot live in the snapshot.** The fact belongs to the environment, to the kernel's own
  semantics, or to a bootstrap. The aim is to bound it and declare it, not to move it.

Each entry names the code, the behavior it decides, and the fix.

---

## A. Oversight or shortcut

### A1. Workflow outcome is the last contract's status, not the declared ending
- `protocol_runtime/runtime/scheduler.py:136`, `:265`. `result_status` starts as `"SUCCESS"`.
  The workflow then completes with the status of the last contract that ran.
- The sealed `terminal` entry is `{"exit": key, "type": "EXIT"}`. It names the exit but no
  outcome. Two EXIT nodes reached by `SUCCESS` and by `VIOLATION` look the same to the snapshot.
- `protocol_runtime/runtime/cli.py:196` then hard-codes the successful outcomes:
  `("SUCCESS", "ALREADY_EXISTS")`.
- **Fix:** seal an outcome class on each EXIT node. Complete the workflow with that class. The
  CLI and the TE then read the class rather than keeping their own lists.

### A2. Contract inputs leak into the contract surface
- `dispatcher.py:274–282`. Every `cc_input` that no output maps is copied into the surface. The
  comment says this "restores the expected surface without changing the pipeline contract".
- The surface is meant to be compiler-declared, and `_apply_outputs` says so. This merge adds
  undeclared fields that downstream bindings and the TE can read.
- **Fix:** declare passthrough outputs in the CC (for example, `CC_STORE_RESULTS`). Remove the
  merge, then let the build refuse any binding that reads an undeclared field.

### A3. The reach read-only rule is decided at execution time
- `dispatcher.py:~395–417`. The dispatcher checks "consulted entity + `effect: write`" and
  returns `REACH_IS_READ_ONLY`.
- The operation, the entity, and its reach are all sealed. When `__store__` is a literal
  binding, this is a static fact.
- **Fix:** have the build refuse such a step (as an invariant). Keep the runtime check only as
  defense in depth, and record it as a check, not as a determination.

### A4. Admission checks are a hard-coded subset, and two copies disagree
- `scheduler.py:73`, the `_admit` function. It checks `required` and `type` against a Python type
  table. The sealed admission contracts carry only those two fields (138 of 138 fields).
- Five artifacts state `admission_rules` in prose, such as "each element must be a positive
  integer". The code acknowledges this and ignores them.
- `protocol_transport/.../resolver.py:119`, the `_validate_input` function, is a second
  validator:
  - It checks `min` and `max`, which `_admit` does not.
  - It skips `number`, `array` and `object`, so those declared types go unchecked at ingress.
- **Fix:** compile both IN and TI input contracts to one sealed schema form (JSON Schema is
  already a core dependency). Have both boundaries run the same generic validator. Make the build
  refuse any prose admission rule that has no machine form.

### A5. A workload-specific derivation operator in the domain-neutral resolver
- `resolver.py:43–49`, the `_DERIVE` table. `length_minus_one` exists only for Collatz `steps`
  (`TE_COLLATZ_COMPUTE_V0`).
- The resolver claims "ZERO operation-specific logic". This operator is Collatz logic.
- **Fix:** move it into the workflow surface, where a CT computes `steps`. Alternatively, seal
  the operator set as a governed vocabulary and have the compiler check `op` against it.

### A6. The status-to-condition namespace is guessed
- `scheduler.py:273–291`. The code tries `transition::X`, then `outcome::X`, then falls back
  to `-1`. Every status in the vocabulary exists in both namespaces.
- **Fix:** seal the condition address on each routing and terminal entry, keyed by the status
  string. Remove the lookup chain.

### A7. A side effect's returned status is not checked against its declaration
- `dispatcher.py:501`. The code checks only that a status is present. Each CS operation already
  seals `result_status_values`.
- Today an undeclared status is caught later, as an unlisted continuation. The error then blames
  the contract rather than the capability.
- **Fix:** refuse at the step when the status is not in the declared set. The data is already
  sealed.

### A8. Defaults supplied inside capability code
- `CS_MUTABLE_JSON_V0/impl/executor.py:245`. An absent `filter` becomes `{}`, so
  `UPDATE_WHERE` updates **every** record.
- `executor.py:174`. An absent `keys` list becomes `[]`.
- The operation declares its inputs but not whether each one is required.
- **Fix:** declare required inputs per operation, and have the build check that bindings supply
  them. A capability then refuses on a missing input rather than defaulting it.

### A9. Hop bound is a runtime constant
- `scheduler.py:50`, `_MAX_HOPS = 64`. This fixed number limits how far any workflow can traverse.
- **Fix:** have the compiler prove the routing graph is acyclic and seal its longest path, or
  seal a declared bound per workflow. The runtime then enforces the sealed number.

### A10. Compatibility and alias paths for shapes the compiler no longer emits
- `scheduler.py:189`. A string in `emits` is accepted as a list. `projections/dispatch.py:139`
  always emits a list now.
- `dispatcher.py:191`. Both `step_id` and `step` are accepted.
- `ct_executor.py:230`, `RESERVED_KEYS`. When no `args` are given, step keys are flattened into
  atom inputs. `_execute_loop` (`:284`) still uses that flattened form.
- `ct_executor.py:149`, `:299`. A loop with no declared `iterator` defaults to `"item"`, and a
  loop with no `over` defaults to `[]`.
- **Fix:** let the build refuse these old shapes, and delete the readers. Each one is a rule the
  snapshot does not state.

### A11. Internal key protocol between compiler and capabilities
- `dispatcher.py:279`, `:485`. The compiler emits `__store__`. The runtime renames it to
  `__store_entity__`, strips both from the surface, and injects `workflow_executor` into every
  side effect.
- **Fix:** seal the store entity as a named field of the CS step, rather than a magic input key.
  Inject the executor only where the CS declares that it needs nested invocation.

### A12. Transport registry skips bad files and finds operations by scanning
- `protocol_transport/.../registry.py:50`. An unparsable canonical JSON file is skipped silently.
- Operations are found by `rglob` over `canonical/`, not by a sealed index.
- **Fix:** read the operation list from a sealed transport index, and fail hard on a file it
  cannot read.

---

## B. Cannot live in the snapshot (bound it and declare it)

### B1. Environment binding
- `dispatcher.py:653`, the `{{module_data_root}}` and `{{snapshot_root}}` templates.
- `runtime/federation/defaults.py`: bind address, port, and timeouts.
- `run_http.sh`: `PGC_HTTP_BINDINGS`.
- These are facts about the deployment. One snapshot runs on many deployments, so it cannot
  know them.
- **Keep:** they are correctly gathered and overridable. One gap remains: the **HTTP route →
  operation and namespace table** is an admission decision (`binding.py`), and it is loaded from
  an unsealed file. Either seal it per profile, or record its hash in the trace.

### B2. Kernel execution semantics
- These are the interpreter:
  - the path grammars (`$.inputs`, `$.results`, `$.payload`);
  - ABSENT versus null;
  - the meaning of `continue` and `exit`;
  - CT completion → `SUCCESS` and refusal → `VIOLATION`;
  - fault versus outcome;
  - replay substitution for `ct_impure`.
- A snapshot cannot hold its own interpreter.
- **Keep:** cite these in the standard (`3a`/`3c`), and version them with the runtime contract
  that the manifest names.

### B3. The atom refusal signal is a class name
- `ct_executor.py:26`. A refusal is recognized because the exception class is named
  `CTExecutionError`.
- This follows from atoms being external code that cannot import the runtime.
- **Smaller boundary:** ship a tiny shared `pgc-atom` signal package, or have atoms return a
  declared refusal value instead of raising.

### B4. Capability realization
- Examples:
  - `UPDATE_WHERE` uses AND semantics, and a `None` value removes a field;
  - a `DELETE_MANY` with nothing to delete still succeeds;
  - file locking and JSON storage.
- This is the C1 limit: a rule computed inside a capability is governed only by its contract and
  its test vectors.
- **Keep:** the realization in code. Close the gaps in the contracts: required inputs (A8),
  declared statuses (A7), and conformance vectors for each operation.

### B5. Authority enforcement needs caller identity
- `scheduler.py:126–132`. Every entry seals an `actor` (an `AC_*` artifact). The runtime only
  records it: "No authorization is enforced (authority model TBD)."
- The policy is in the snapshot. Proving that a caller is that actor needs a credential, and
  that exists only at run time. The Canonical Transport Request carries no principal.
- **Split:**
  - Sealed: which principal kinds may invoke each actor-bound workflow.
  - Runtime: verifying the credential.
  - Evidence: record the verified principal next to the sealed actor.
- Until then, sealing an actor gives attribution only. It does not authorize anything.

### B6. Compiler checks and the kind registry are code
- There are 99 assertion handlers in `governance_engine/assertions/handlers/`, and
  `artifact_kinds.py` holds the built-in kind registry.
- Something must check the snapshot, so these are a bootstrap. They are mitigated by the sealed
  ontology and its agreement invariant.
- **Keep:** but make sure every assertion's artifact states its rule, so that a handler can be
  checked against its declaration.

---

## Priority

| # | Item | Why first |
|---|---|---|
| 1 | A1 workflow outcome from the declared EXIT | The terminal determination is undeclared, and two lists of successful outcomes have drifted |
| 2 | A4 one sealed admission schema | Admission is the AI-6 surface, and prose rules go unenforced today |
| 3 | A8 + A7 CS input and status declarations | An empty filter rewrites a whole store |
| 4 | A2 remove the surface merge | Undeclared data reaches egress |
| 5 | B5 principal on the canonical request | Authority is sealed but does nothing |
| 6 | A3, A6, A9, A10–A12 | Cleanup: move static checks to the build and delete compatibility readers |

# Decision Accounting

## 1. Problem

A sealed snapshot states what a workflow does. It does not state who controls the values that
decide it, and it does not show whether its evidence records the values that the decision used.

The domain analysis found three kinds of problem:

- **Hidden authority.** A caller supplies a value that decides a business outcome.
  `WF_PROVISION_AI_LICENSING_V0` takes its license cap from the payload, and
  `WF_AUTO_RECLAIM_V0` takes its inactivity threshold from the payload.
- **Hidden logic.** An atom computes a rule that no declaration states. Three atoms hard-code a
  key limit of 256. Eight atoms declare `refusal: never`, and all eight refuse.
- **Unsubstantiated evidence.** The reclaim audit records `days_inactive` from the payload,
  not the value that the transform computed.

This design makes **complete decision accounting** a construction obligation. The obligation
is split into three parts, and its inspectable output is a sealed **Decision Authority Map**.
The obligation does not list known leaks. It defines what a decision is, what must account for
the decision, and what the compiler can establish soundly.

## 2. Terms

**Decision.** A decision is a node whose outcomes route to different targets. Three kinds of node
qualify:

- an IN admission gate;
- a CC step whose transform can refuse;
- a CS step whose declared statuses route apart.

**Dependency.** A dependency is a value or a computation that can change a decision's outcome.

**Account.** A decision's account is the set of its dependencies. Each dependency carries five
things: its origin, its semantic role, the contract that governs its use, how it was
established, and whether that use is admissible.

## 3. Three obligations

| Obligation | Question | Refused when |
|---|---|---|
| **Provenance** | Which values and computations influence this decision, and where do they come from? | A dependency is missing from the account, or its role is undeclared |
| **Authority conformance** | May these sources decide this decision under the governing declarations? | A source is not admissible for its role at this decision |
| **Evidence integrity** | Does the recorded evidence match the values and computation that occurred? | An evidence field declares no `records:`, or records a source other than the determination it claims |

One compiler stage carries all three. They stay separate as obligations, as invariants, and as
fields in the map, so each one can fail and be reported on its own.

## 4. How a dependency is established

Every dependency in the map carries one status. The statuses never merge, and none of them is
called "verified".

| Status | Meaning | Example |
|---|---|---|
| `static` | The compiler derives it from sealed artifacts | A binding from `$.payload.threshold_days` to a transform input |
| `declared` | An author asserts it, and nothing checks it independently | The input role `policy`; an atom's stated refusal conditions |
| `observed` | A trace recorded it for one execution | The branch a run took, and the atom results it recorded |
| `unknown` | The analysis cannot establish it completely | Logic inside an atom beyond its declared inputs and constants |

`observed` evidences one run. It never upgrades a dependency's status in the map, because a
trace shows which branch ran, not every value that could have changed it.

## 5. Where completeness holds and where it does not

PGC already seals the composition layer:

- the runtime executes only sealed bindings and pipeline steps;
- an absent binding is refused, not defaulted;
- an unrouted outcome is refused.

So at the composition boundary, the account of every transform's and side effect's inputs is
**static and complete by construction**. Every value that reaches an atom arrives through a
sealed path, and the compiler can trace that path to its origin.

Completeness stops at three boundaries:

1. **Inside an atom.** An atom may depend on its inputs, module constants, and any computation
   over them. A syntax-tree scan finds module constants and literals inside comparisons. It
   cannot establish every way that code can turn an input into an outcome.
2. **Atom purity.** Atom inputs are a complete account only if the atom reads nothing else.
   Purity is declared but not checked. Today the import rule in `business_domains/CLAUDE.md`
   is doctrine, and no check enforces it. `implementation_closure.py` checks only that each
   module exists.
3. **Inside a capability side effect.** A side effect's status semantics, such as an empty
   match returning `VIOLATION`, are realization.

The design makes the first two boundaries smaller and reports what remains as `unknown`.

## 6. Declarations

### 6.1 Input role on a capability transform

Every input of a transform declares a `role`. The field is required and has no default.

| Role | Meaning | Example |
|---|---|---|
| `policy` | A rule that the business sets | `quota`, `threshold_days`, `kinds` |
| `fact` | Something true about the world | `assigned_count`, `last_active_date`, `evaluation_date` |
| `subject` | What the request is about | `employee_id`, `title`, `key_material` |

A role is `declared`. The role alone never makes a source admissible (§6.4).

### 6.2 Atom constants

An atom declares every constant that can affect its outcome, including its value:

```yaml
machine:
  constants:
    MAX_KEY_LENGTH: {value: 256, role: policy, source: software_governance::CS_REGISTRY_V0.max_key_length}
```

The compiler scans the module's syntax tree. It refuses any module-level constant, and any
literal used in a comparison, that the artifact does not declare with an equal value. A
declared constant that names a `source` must equal that sealed value. This moves hard-coded
thresholds from `unknown` to `static`. A computed threshold, such as `90 * 2` assembled at run
time, stays `unknown`.

### 6.3 Refusal conditions

An atom that can refuse declares `refusal: raises` and names its conditions. Each condition has
a refusing test vector. The status of the conditions is `declared`; their vectors are
`observed` at build time.

### 6.4 Admissibility

The constitution seals a default table, and every cell is one of three answers:

| Role ↓ Source → | sealed | governed_store | store | clock | caller |
|---|---|---|---|---|---|
| `policy` | admit | admit | refuse | refuse | refuse |
| `fact` | admit | admit | admit | admit | claim |
| `subject` | admit | admit | admit | refuse | admit |

The three answers mean:

- **admit:** the source may decide.
- **refuse:** the build is refused.
- **claim:** the source may decide only if its admission field declares `claim: caller_asserted`.

A decision may narrow the table. It may widen the table only by an explicit override on the
contract, and the map shows every override:

```yaml
admits:
  ceiling: [governed_store]   # set by WF_PLACE_MODEL_IN_SERVICE_V0
```

A `governed_store` source is admissible only if every workflow that writes it is bound to an
actor. Until the runtime enforces authority, the map flags such a source as
`authority: declared_not_enforced`.

### 6.5 Evidence binding

Every evidence or audit field declares what it records:

```yaml
data:
  days_inactive:
    records: $.results.CC_RECLAIM_UNUSED_LICENSE_V0.days_inactive
```

Each field records either a determination or an input. If a field claims to record a
determination, its `records:` path must trace to the node that made it. Field names are never
matched; the binding is the declaration.

## 7. Decision Authority Map

The compiler writes `decision_map/<domain>.json` into the snapshot, and the manifest hashes it.
The inspector exposes it read-only, as `si.decision.map`. Each decision entry carries:

- the decision and its governing declaration;
- each dependency, with its origin path, role, governing contract, status (§4) and
  admissibility (§6.4);
- every override of the default table;
- every `unknown` region, with the reason it is unknown;
- the evidence fields that refer to the decision, each with its `records:` trace.

```json
{
  "decision": "ai_governance::WF_AUTO_RECLAIM_V0#CC_RECLAIM_UNUSED_LICENSE_V0",
  "governed_by": "ai_governance::CC_RECLAIM_UNUSED_LICENSE_V0",
  "dependencies": [
    {"input": "threshold_days", "role": "policy", "role_status": "declared",
     "origin": "$.payload.threshold_days", "source": "caller", "origin_status": "static",
     "admissible": "refuse"},
    {"input": "evaluation_date", "role": "fact", "role_status": "declared",
     "origin": "$.payload.context.evaluation_date", "source": "caller", "origin_status": "static",
     "admissible": "claim", "claim_declared": false}
  ],
  "unknown": [{"region": "CT_PURE_EVALUATE_INACTIVITY_V0", "reason": "computation over inputs"}],
  "evidence": [{"field": "days_inactive", "records": "$.payload.context.days_inactive",
                "claims_determination": true, "traces_to_decision": false}]
}
```

The summary counts each status and each source for every workflow and domain, so successive
snapshots and domains can be compared.

## 8. Invariants

All three invariants sit under `decision_accounting::CONSTITUTION_DECISION_ACCOUNTING_V0`. Each is
a `compiler_assertion` with the response `FAIL_IMMEDIATELY`.

| Invariant | Holds when |
|---|---|
| `INVARIANT_DECISION_ACCOUNT_COMPLETE_V0` | Every decision has an account. Every transform input declares a role. Every atom constant is declared with an equal value. Every atom that can refuse declares its conditions, and each condition has a vector. Every atom imports only what it is permitted to. |
| `INVARIANT_DECISION_SOURCE_ADMISSIBLE_V0` | Every dependency's source is admissible for its role at its decision, under the default table or an override the map shows. |
| `INVARIANT_EVIDENCE_RECORDS_DETERMINATION_V0` | Every evidence field declares `records:`, and every field that claims a determination traces to it. |

`unknown` regions do not refuse the build. A profile may set a ceiling on them.

## 9. Effect on existing domains

| Invariant | Where it fails today |
|---|---|
| Admissible | `cap` and `threshold_days` are policy from the caller. `assigned_count`, `training_completed`, `last_active_date` and `evaluation_date` are caller facts with no declared claim. |
| Evidence | `days_inactive` in the reclaim audit. |
| Complete | The 8 atoms declared `refusal: never`. `MAX_KEY_LENGTH` in the three key atoms. The record outcomes and markers in `causal_language_model`. Every transform input lacks a role. No atom's imports are checked. |

## 10. Evaluation

The test of the design is this: **introduce an undeclared decision dependency, and check that
construction refuses it.** The known leaks motivated the design, so they cannot be the test.
The test uses a mutation suite, seeded into a copy of each domain:

| Mutation | Expected result |
|---|---|
| A hard-coded threshold added to an atom | Refused: undeclared constant |
| A threshold computed at run time inside an atom | Not refused. Reported as `unknown`; this marks the boundary |
| A policy input relabelled as `subject` | Not refused. The map shows `role_status: declared`, and a reviewer must catch it |
| A policy binding moved from sealed to `$.payload` | Refused: inadmissible |
| An indirect dependency: payload → transform A → transform B → decision | Refused if the payload value plays a policy role at B |
| An evidence field rebound to the payload, or to the wrong node | Refused: `records:` does not trace |
| An atom that reads `os.environ` or the clock | Refused: import not permitted |
| A refusal added to an atom declared `never` | Refused: undeclared refusal |
| A side effect whose empty result changes from `SUCCESS` to `VIOLATION` | Not refused. Reported as realization in a side effect |

The results give three measures:

- **detection rate** for each mutation class;
- the share of dependencies in each status (`static` / `declared` / `observed` / `unknown`);
- the classes that are not refused, reported as the stated limits.

## 11. What a passing build supports

A build that passes all three invariants supports this statement:

> For dependencies the compiler can establish statically, which is every value that crosses the
> composition boundary and every declared atom constant, construction refuses a candidate with an
> incomplete account, an inadmissible source, or evidence that does not trace to its
> determination. Dependencies it cannot establish are listed as `declared` or `unknown`, never
> as verified.

It does not support "hidden business logic is eliminated". Three limits remain:

- **Roles are declared.** A relabelled role passes, and a reviewer sees it in the map.
- **Computation inside an atom stays `unknown`.** Only test vectors govern it.
- **Authority over governed stores is declared, not enforced,** until the runtime checks callers.

Three terms keep the claim honest:

- a **detector** finds known violations;
- an **enforced invariant** rejects every violation within its scope;
- a **guarantee** also needs evidence that the scope covers every way a decision can be
  determined.

This design delivers enforced invariants with a stated scope. The mutation suite measures how
much of the problem that scope covers.

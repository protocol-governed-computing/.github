# dev/18 — the D1/D2 cycle, replayed

dev/18 was rebuilt from each repository's "VERSION bump to 18" commit. The first attempt's code was
carried in its final form, and each change of meaning was authored once, under a new identity. The
first attempt is kept as the tag `archive/dev-18-original` in every repository.

## Done-checks

dev/18 is ready to cut when every check passes. No cut is planned.

| # | Check | Command |
|---|---|---|
| D1 | The regression passes as expected, and every red-by-design step has a written reason. | `regression.sh --all` |
| D2 | No identity published in v5 changes meaning. Only stand-down markings, declared re-points and named removals are allowed. | `published_identity_check.py` |
| D3 | Construction refuses a change of meaning under an old identity. | `semantic_change_design_test.py` |
| D4 | No rule in force contradicts another. | the compile, `test_routing_closure` and `test_routing_lookup` |
| D5 | Every known deviation appears in the realization map and the release notes. | read |

**Rules the work kept.**
- A finding is fixed only if it makes a done-check fail; anything else is parked.
- No count is stated unless a command produced it.
- A domain change runs the dossier pipeline. A platform or pipeline change runs a change note plus
  the regression.

## Result after step 8

D1–D4 hold: `regression.sh --all` passes 69/69 as expected. Four steps are red by design, each with
its reason in `expectations.yaml`.

### Artifacts, against v5

Measured on the compiled compositions: v5 holds 500 artifacts, dev/18 holds 525.

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

**Dossiers.** Each is delivered with its own `delivery.md`:
- `blockchain/cr_06_routing_closure`;
- `ai_governance/cr_02_reclaim_and_parameters`;
- `collatz/cr_01_termination_gate`.

## Parked

None of these makes a done-check fail.

- **Optional TE output fields.** `TE_ACCEPT_ACTOR_V0` owes `grounds`, which leaves
  `blockchain_identity` red at 21/22.
- **Design language gaps:**
  - it has no family for a constitution or an invariant;
  - P7 assumes `{domain}.implementation`;
  - P7 refuses with `TRANSFORM_WITHOUT_VECTOR` and `DISCHARGE_NOT_IN_TOPOLOGY`;
  - a step's required outputs are unknown to design.
- **Workloads cannot hold test data.**
- **Construction reads 0 of 0 facts as 0%.**
- **A domain build keeps no record of which checks ran.**
- **Short-code references:** workflow `code` and `start_node`, and RB binding keys.
- **RT-6 stays Partial** for the outcome-namespace fallback (finding 31).
- **No register states an explanation-only `extensions.description` for a new artifact.**
- **Stood-down identities stay in the record** until a rule says when a published identity may leave
  it.

---

## Change notes

One entry per platform or pipeline change, in step order.

## Step 2 — The rebuild keeps the previous build until the new one is assembled

**Problem.** `regression.sh --build` and `--all` deleted every snapshot, `data/` and `traces/` before
they compiled anything. If the build then failed, there was no snapshot left, and every later check
failed because of that rather than for its own reason. In dev/18 this happened four times, and each
time the snapshot was restored by hand.

**Change** (`process/regression.sh`):
- The previous build output is moved to a temporary directory, not deleted. That covers each
  `snapshot/`, `software_governance/snapshot_fed` and `snapshot_mw`, `data/` and `traces/`.
- If any compile or assembly step fails, the partial output is removed and the previous output is
  moved back. The script then exits 1.
- After a successful assembly, the backup is deleted.
- `pgc_release/snapshot` is still excluded, and the check that it survived still runs.

**Verified.**

| Case | Command | Result |
|---|---|---|
| Failed build | `PGC_SNAPSHOT_PROFILE=NO_SUCH_PROFILE_V0 regression.sh --build` | The assembler refuses and the script exits 1. All 1,270 build-output files come back, and the checksums of `snapshot/`, `snapshot_mw/` and the blockchain snapshot match. No backup is left behind. |
| Successful build | `regression.sh --all` | 59/59 as expected. No backup is left behind. |

## Step 3 — The platform declares what a reference is

**Problem.** The platform decided what a reference is in three places, and they disagreed:
- S1's record of references read a fixed list of nine keys;
- the superseded check walked every value shaped like a full name;
- construction had no notion of a reference at all.

So a reference could be missed by one place and seen by another.

**Change.**
- **`software_governance`.** New `artifact::VOCAB_DECLARATION_REPRESENTATION_V0` declares the parts
  that only explain, the unordered lists, the reference parts (`code` included), the keyed reference
  part (`bindings`), the parts that require a full name, the supersession parts and the two sameness
  rules. It is new, so no published identity changes.
- **`protocol_compiler`.**
  - New `compiler/atoms/representation.py` reads the declaration by its exact identity.
  - S1 records references from the declaration and refuses a full name in an undeclared part
    (`E105_UNDECLARED_REFERENCE`).
  - The FQDN-only and superseded handlers read the declaration. The superseded handler reads a
    workflow's own place labels as labels.
  - S4 passes the declaration to every handler.
  - New test: `test_reference_semantics`. `test_vector_build` expects the refusal of a dangling
    target.
- **`snapshot_inspector`.** `si.artifact.refs` reads the composition's record of references.
- **`transformation`.** New `build/sameness.py` compares two declarations by the platform's
  declaration. Only the published-identity check uses it so far; construction uses it from step 4.
- **`.github`.** New `published_identity_check.py`. It compares every identity published in v5 with
  the working composition and fails on a change of meaning or a missing identity. It is added to the
  regression, the RUNBOOK and the README.

**Verified.** `regression.sh --all`: 61/61 as expected.
- 505 artifacts, 7 supersession relations.
- Construction acceptance 167/167.
- `test_reference_semantics` 15/15; `test_vector_build` 4/4; `test_inspector` 152/152.
- Published identity: 500 identities published in v5, none changed meaning.
- **Probe.** On `blockchain::CC_RESOLVE_ACTOR_V0`, the comparison reports an added outcome
  (`core.result_surface`) and ignores a reworded `summary`.

## Step 4 — Construction refuses a change of meaning; a phase rejects when nothing is found

**Problem.** There were two problems.
- **Construction never compared meaning.** It built an amendment that changed what an artifact
  means, under the artifact's old identity. It skipped the comparison when it was not given the
  composition. It let a design withdraw a fact. And it gave a design no way to re-point a reference
  without restating the artifact that holds it.
- **Phases ignored NOT_FOUND.** Seven of the phases ask the composition questions before they judge.
  When an answer was NOT_FOUND, nothing answered it, so the phase judged against an observation that
  never arrived.

**Why a change note.** All nine artifacts this step replaces are written by the generator
(`emit_rule_sets`). A dossier would also have been judged by the P7 rules it replaces.

**Change.**
- **Construction** (`build/sameness.py`, `completeness.py`, `generators.py`, `render.py`, `cli.py`):
  - it compares every amendment with the composition by `VOCAB_DECLARATION_REPRESENTATION_V0`;
  - it refuses a change of meaning under an old identity, and refuses an amendment built without
    `--snapshot`;
  - `REPOINT` moves one reference and nothing else, and only in declared reference parts;
  - a replacement whose live referrer the design does not account for is refused;
  - `render._binding` refuses a step-binding literal that does not parse.
- **P7 rules** (`p7_design_intent/rules.py` and its template): P7 admits `REPOINT` and refuses any
  `withdrawn_facts` row.
- **Generator** (`design/emit.py`):
  - every observing step answers each outcome the observing capability declares;
  - every phase routes every outcome its contract declares other than SUCCESS to `EXIT_REJECTED`;
  - it writes P2–P8 into their V1s, and reads the judge V1s.
- **Generator fix, new in the replay.** The generator found a workflow's contract by the node's place
  label. A re-point moves the node's `code` and keeps the label, so a re-pointed workflow was routed
  by the contract it no longer runs. `emit.judge_contract` now reads `code`, as the compiler does.
  The routing-closure validation reads it the same way.
- **New identities** (`transformation`), each standing down its V0, which gains only `superseded_by`:
  - `CC_JUDGE_AGAINST_SNAPSHOT_V1` and `CC_JUDGE_AGAINST_COMPOSITION_V1`;
  - `WF_P2…P8_…_ADMISSIBILITY_V1`. Each runs its judge V1, and P7 V1's `phase_workflows` names the
    V1s.
- **Re-points.** The seven intents `IN_*_SUBMITTED_V0` for P2–P8 each move `workflow` once.
- **Explanation only.** `WF_P0_…_V0` and `WF_P1_…_V0` gain a generator-source line.
- **Tests.**
  - `semantic_change_design_test` replaces `withdrawal_design_test`.
  - `testbed/routing_closure/execution_validation.py` is new.
  - `e2e_phases_test` and `differential` now name the V1 workflows.
  - `construction_acceptance` adds ai_governance (partial). The Collatz workload joins it in step 8.

**Verified.** `regression.sh --all`: 62/62 as expected.
- 514 artifacts, 16 supersession relations.
- Published identity: 500 identities published in v5, none changed meaning.
- `semantic_change_design_test` 18/18; `keyed_node_design_test` 7/7.
- Routing closure: 4/4 criteria hold (1 not exercised).
- Rule-set emission is consistent.
- **Construction acceptance** reproduces 171/173 across 6 domains and is red by design. The two
  differences are `book_library_mgmt`'s `IN_`/`WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V1`: v5 published
  them with `version: v0`, and the renderer now writes the version from the identity.
- **Match with dev/18.** Each V1 equals dev/18's final text for the same artifact, apart from
  identity names, `version` and `supersedes`.

## Step 7 — Routing is a lookup, and every outcome is answered

**Problem.**
- **Conditions nothing runs.** A contract could route a step's answer to an evaluation condition.
  Execution read any answer but `exit` as going on, so such a contract ended with its last step's
  outcome.
- **Steps narrower than their capability.** A step's answers could be fewer than the outcomes the
  capability it dispatches declares.
- **Unrouted contract outcomes.** A workflow could leave an outcome of the contract a place runs
  without a route.

**Change.**
- **`software_governance`**, from dev/18:
  - `CONSTITUTION_EXECUTION_TOPOLOGY_V1` names both new invariants and `WF_ROUTING_CLOSED`;
  - `INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V1`: routing answers only `continue` or `exit`, and a contract
    declares no `evaluation` block;
  - `INVARIANT_TOPOLOGY_ROUTING_COMPLETE_V1`: a step answers every outcome its capability declares;
  - `workflow::INVARIANT_WF_ROUTING_CLOSED_V0`: a workflow routes every outcome a reachable place can
    end with;
  - the three V0s gain only `superseded_by`;
  - twenty `governed_by` references move to the topology V1, one line each.
- **`protocol_compiler`**, from dev/18:
  - the three handlers, and their registrations;
  - S2's single node resolver, and S4's precomputed workflow routing;
  - `test_routing_closure` and `test_routing_lookup`.
- **New in the replay: the routing-complete V1 handler skips a stood-down contract.** It checked every
  contract, and reported the two judge-contract V0s that step 4 stood down. dev/18 had amended those
  V0s in place, so it never met the case. The handler now skips a contract that is not in force, as
  `INVARIANT_SUPERSEDED_NOT_IN_FORCE_V0` requires and as `CONTRACT_CLOSED_V1` already did.
  `test_routing_lookup` covers it.
- **Licence cap.** `ai_governance::CC_ENFORCE_LICENSE_CAP_V0` carries an evaluation block, and
  nothing runs it.
  - It is deleted, and the two prose lines naming it are trimmed. This is dev/18's commit.
  - `published_identity_check.py` allows this one removal by name, with its reason.
  - It is an exception to SU-11; the realization map and the release notes record it.
- **Order.** The Collatz dossier (step 7a) ran first, because this rule refuses the evaluation block
  `CC_VERIFY_TERMINATION_V0` carries.

**Verified.** `regression.sh --all`: 66/66 as expected.
- 528 artifacts, 30 supersession relations.
- Published identity: 500 identities published in v5, none changed meaning, 1 removed by name.
- `test_routing_closure` 12/12; `test_routing_lookup` 6/6.
- Construction acceptance 182/184 across 7 domains, red by design for the two pinned book_library
  differences.

## Step 8 — No default, a refused fault, and trace format v2

**Problem.** Four problems in the runtime and the transport.
- **Defaults.** Three runtime resolvers gave a binding that reached nothing a value of None. A step
  outcome with no continuation was routed anyway.
- **Faults routed.** A capability fault was routed as VIOLATION, as if it were a business refusal.
- **Traces.** Traces carried neither a step's outcome nor the continuation it selected.
- **Transport.** The egress answered with an absent output field.

**Change.** All from dev/18, final form.
- **`protocol_runtime`** (`dispatcher`, `scheduler`, `memory`, `ct_executor`, `ct_execute`,
  `conformance`, `evidence`, `api`, `examine/`):
  - no resolver supplies a default (RT-6);
  - an unlisted step outcome refuses (EX-18);
  - a fault refuses rather than routing;
  - an unknown continuation refuses;
  - traces are written to `SCHEMA_TRACE_EVENT_V2`, and each refusal is recorded once (EV-19).
  - Tests: `test_step_outcome`, `test_no_default` and `test_unknown_continuation`, with
    `test_reference_collatz` (including the case where the gate fails) and the conformance runner.
- **`software_governance`.** `CONSTITUTION_TRACE_EXECUTION_V1` names `SCHEMA_TRACE_EVENT_V2`, and the
  V0 gains only `superseded_by`. `SCHEMA_TRACE_EVENT_V2.json` and the schema index are added.
- **`snapshot_inspector`.** The test fixtures use trace format v2.
- **`protocol_transport`.** The egress refuses an absent output field by name.
- **`business_domains`.** CLM's choose atom reads `ground_numbers` with `.get`: absent means not
  grounded, as before.
- **`.github`.**
  - `trace_schema_conformance.py` reads V2.
  - `domain_authoring.py` expects a module that cannot be imported to refuse the run as a fault, not
    to report VIOLATION. This file was missing from the replay's file ledger, and the audit at this step
    found it.
- **Surface map.** `software_governance/surface_map/governance_surface_map.yaml` is regenerated with
  `gen_governance_surface_map.py`: 204 governance artifacts. dev/18's copy was never regenerated after
  its rules changed.

**Verified.** `regression.sh --all`: 69/69 as expected.
- 529 artifacts, 31 supersession relations.
- Published identity: none of the 500 changed meaning, 1 removed by name.
- Trace schema conformance: every line of 160 traces conforms to V2.
- `test_step_outcome` 8/8, `test_no_default` 12/12, `test_unknown_continuation` 3/3;
  `test_reference_collatz` 6 tests; conformance runner 11 tests; `domain_authoring` 8/8.
- **Audit.** Every repository's code equals dev/18's except the intentional differences: the
  declaration's name, the V1 targets and the fixes recorded in steps 4, 5 and 7.
- **Red by design.** `blockchain_identity` holds 21 of 22 criteria. An acceptance stating no grounds
  records none, and `TE_ACCEPT_ACTOR_V0` still owes `grounds`. The fix needs an optional transport
  output field, which is parked.

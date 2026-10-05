# SOTU Handoff

## Reckoning: the remaining list is frozen; the goal is a coherent dev/18, not v6 — dev/18 · 2026-10-04

- **Goal changed.** No v6 cut is planned. The goal is a dev/18 that is coherent and ready to merge.
  Publication waits; the SoSyM review sets no pace. The v6 cut, the `pgc_release` DOI, PyPI 6.0.0
  and the SoSyM note leave the closure criteria.
- **Why the reckoning.** Four CRs became six, then a seventh. The M-series was planned from the
  standard's obligation list, one step ahead, not from a design of the whole system. Dossier A
  (M5) declared what carries no meaning without asking what M1 and M2 would need from it. Each gate
  reviews one dossier, so a gap between dossiers passes every gate.
- **Structural cause.** `tc construction emit --root` writes one domain. A concept that spans the
  platform and transformation always costs two dossiers.
- **Dossier B paused after P1** (`transformation/dossiers/semantic_change/`). P2 grounding found:
  - The platform's declaration does not name the keys that hold references, so M1 would read a
    re-point as a change of meaning. Nor does it state that explanation is exempt only as text.
    Both go into **A2**.
  - M1 makes `withdrawn_facts` unsatisfiable: a withdrawal changes meaning. B retires the register,
    and the narrowing check folds into the M1 comparison. Four P7 designs use it today: blockchain
    `cr_05` (39), book_library_mgmt `cr_05` (36) and its fixture copy, CLM `cr_02` (1). They go to
    the re-cut.
  - `tc construction check` without `--snapshot` admits an amendment it never compared. B refuses
    that.
  - B's P0/P1 still name `artifact` MODIFIED. They are rewritten to name it ADJACENT before B
    resumes.
- **The frozen list.** Anything new is parked on dev/18 unless it blocks this list.
  1. **A2**, `software_governance/dossiers/reference_semantics/`: `VOCAB_DECLARATION_REPRESENTATION_V1`
     supersedes V0. It adds the reference-key group and the text-only rule. This is the last
     platform dossier for this concern.
  2. **B**: M1–M3, retiring `withdrawn_facts`, and refusing a design with an amendment when no
     snapshot is passed. Construction reads V1 by its exact identity and never searches for it.
  3. RT-6 and evaluation targets.
  4. The SU-11 re-cut of dev/18's semantic changes.
  5. The map and the standard, including the publication rule below.
  6. **Cleanup**, then regression.
  7. The SoSyM evidence re-run on dev/18 (`omission.sh` O3, `outcome_survey.py`), outputs kept.
  8. dev/18 merge-ready: `--all` green.
- **Cleanup rules.** These keep the cleanup itself conformant.
  - Delete only identities that were never published: in the working snapshot, absent from
    `pgc_release/snapshot` (v5), and superseded during dev/18. VOCAB V0 is one. The list comes from
    a diff of the two snapshots, not from memory.
  - Everything in v5 stays, for example `SCHEMA_TRACE_EVENT_V1` (SU-8).
  - Clean up before any merge to `main`. A version on `main` is cited.
  - The standard has to permit it first. On `work/v1`, add that publication is the boundary of
    identity, and that a version never published may be withdrawn before release. Record it in
    `revisions.md`.
- **A2 at P0, admissible, awaiting Gate 0** (`software_governance/dossiers/reference_semantics/`,
  pinned to `c55dbfd7`). Grounding found that the platform decides what a reference is three ways.
  - **S1's record of references** (`s1_extract._extract_references`) reads a fixed list of nine keys.
    `si.artifact.refs` reports `CONSTITUTION_ASSERT_V0` referred to by 1 artifact, although 138 name
    it in `enforced_by`, and `AC_SEED_AUTHOR_V0` by 0 of 39 (`actor_context`).
  - **`ASSERT_SUPERSEDED_NOT_REFERENCED_V0`** walks every FQDN-shaped value.
  - **Construction** has no notion of a reference.
  - A2 therefore declares the reference keys in VOCAB V1, and has S1 and the superseded check read
    them. A full name in an undeclared key is refused. Short-code references (workflow `code` and
    `start_node`) stay out of scope.
  - M3 depends on this: it reads `si.artifact.refs`.
- **A2 delivered** (`software_governance/dossiers/reference_semantics/delivery.md`).
  - VOCAB V1 (73/73) supersedes V0. `bindings` is keyed but not `full_name_required`: admission
    and test cases key `bindings` by short code or field name. A short-code RB binding key is no
    longer refused; parked with the other short-code references.
  - Compiler: `compiler/atoms/representation.py`; S1 records from the declaration and refuses an
    undeclared full name (`E105_UNDECLARED_REFERENCE`); the FQDN-only and superseded handlers read it.
  - Renderer: `version` comes from the identity's `_V<n>`. book_library `cr_05` re-emitted; two
    `_V1` artifacts now say `v1`.
  - `test_reference_semantics` 14/14; `test_vector_build` expects the dangling-target refusal.
  - `--all` 65/65 as expected: 507 artifacts, 8 supersession relations, acceptance 169/169.
- **Dossier B delivered** (`transformation/dossiers/semantic_change/delivery.md`).
  - M1: construction compares every amendment, rendered or generated (via a generator preview),
    with the composition by VOCAB V1 (`build/sameness.py`); refuses a change of meaning by place, an
    uncompared amendment (no `--snapshot`), and a declaration naming a rule it does not apply.
  - M2: P7 admits `REPOINT`; construction rewrites names of replaced artifacts to their successor.
  - M3: every live referrer of a `REPLACE`d artifact must be REPLACE/EXTEND/REPOINT in the design.
  - P7 refuses any `withdrawn_facts` row (register kept: removing it changed P1–P6's sealed rules).
  - `WF_P7_…_V0` stood down for `_V1` (carried by hand, filled by the generator); the P7 intent
    re-pointed by hand. Narrowing and `withdraw` removed.
  - Inspector: the graph adds the canonical record of references. It missed 342 of 1,008 recorded
    references (e.g. `CONSTITUTION_CAPABILITY_CONTRACT_V0`: 1 of 73).
  - `--all` 65/65: 508 artifacts, 9 supersession relations, `test_inspector` 152/152,
    `semantic_change_design_test` 17/17 (replaces `withdrawal_design_test`).
- **Correction to A2.** A2's P2 and delivery say inspection reported `CONSTITUTION_ASSERT_V0` named by
  1 of 138 and `AC_SEED_AUTHOR_V0` by 0 of 39. Those were counts of the part (`enforced_by`,
  `actor_context`), not of the artifact; each has 2 and 1 referrers. A2's change to the record
  stands; its figures do not. The real gap is above.
- **RT-6 survey (no code yet).** Three runtime resolvers default to None: CT-IR (`ct_executor`),
  step bindings (`dispatcher._nested_get`), workflow bindings (`memory._nested_get`). Measured: 168
  misses, all in step outputs of non-SUCCESS results (66), absent optional inputs (95+4), and one
  synthetic CT-IR case. Plan approved (B): R0 CT-IR absent path refuses; R1 outputs mapped only on
  SUCCESS and must exist there; R2 an absent source is left out, never None; R3 malformed paths refuse.
- **ai_governance cr_03 delivered** (`cr_dossiers/cr_03_parameter_result/delivery.md`): it fixes
  the one real defect the survey found. `CC_VALIDATE_TOOL_PARAMETERS_V1` maps `validation_result`
  from `valid`; V0 stood down; `WF_GOVERN_AGENT_ACTION_V0` re-pointed (one line, `code`).
  - First real REPLACE + REPOINT. Fixed on the way: reach ignores `NODE_NEXT`/`WF_START`; re-point
    rewrites only declared reference parts; `code` added to VOCAB V1's `reference` group in place
    (recorded exception, V1 unpublished; A2's P7 and delivery amended to match); the compiler's
    superseded check reads a workflow's own place labels as labels.
  - ai_governance added to construction acceptance (`whole=False`): 177/177 across 6 domains.
  - `--all` 65/65: 509 artifacts, 10 supersession relations.
  - Carried: a step-binding literal that fails to parse is silently kept as a string
    (`render._binding`); to be refused in the RT-6 pass.
- **RT-6 built (R0–R3), no default left in any resolver.**
  - `ct_executor.py`: both resolvers and the loop accumulators refuse a path that reaches nothing
    (`CTFault`); a value present as null passes.
  - `dispatcher.py`: inputs leave an absent source out (nested too); a list naming one refuses;
    a result maps only on SUCCESS and must carry each field mapped from it; `$.result_status` maps
    the step's outcome; a malformed path or a step not yet run refuses (`BindingFault` →
    `CapabilityFaultError`).
  - `memory.py` + `scheduler.py`: workflow bindings leave an absent source out; a contract not reached
    on this route is absent; a malformed path refuses (`MalformedBindingError`).
  - `transformation/build/render.py`: `_binding` refuses an object or list literal that does not
    parse.
  - Readers that expected the null: CLM's choose atom reads `ground_numbers` with `.get` (absent means
    not grounded, as before). The transport resolver refuses an absent egress field by name.
  - Tests: `test_no_default` 12/12 (new, in regression); the conformance runner 11/11 (the
    null-input case passes nulls; absent inputs fail as a fault); `keyed_node_design_test` 7/7.
  - Map: RT-6's text corrected; it stays Partial for the outcome-namespace fallback (finding 31).
  - `--all` 66/66 as expected.
- **Parked on dev/18: optional TE output fields.** `TE_ACCEPT_ACTOR_V0` owes `grounds`, which an
  acceptance may omit; the entrance now refuses that answer (`EXECUTION_FAILURE`) after the workflow
  has recorded the acceptance. `blockchain_identity` is red by design at 21/22. Needs the TE output
  contract to declare a field optional (transport standard change).
- **Evaluation targets: three dossiers (plan A).** The SOTU's "none are in use" was wrong: two live
  contracts route SUCCESS to a condition nothing runs, so the licence cap is never enforced and the
  Collatz gate cannot fail. The constitution also contradicts itself (§4 two answers; §1, §3 admit
  evaluation targets).
  - Platform `software_governance/dossiers/routing_lookup/`: P0–P8 approved (Gates 1–2). V1
    constitution + V1 `INVARIANT_TOPOLOGY_CONTRACT_CLOSED` by hand (REVIEW); 20 referrers REPOINT
    (dry-run clean); compiler check for V1; runtime refuses an unknown answer. **Built last.**
  - Collatz `conformance_workloads/workloads/collatz/cr_dossiers/cr_01_termination_gate/`: P0–P8
    admissible (option A, P0 amended). `CC_VERIFY_TERMINATION_V1` runs the unchanged check, then the
    platform's `CT_PURE_VALIDATE_SET_MEMBERSHIP_V0` on `all_terminate` against `[True]`; WF re-pointed.
    **Delivered** (`delivery.md`): Gates 1–2 approved, emitted, `--all` 66/66. First emit failed
    the build (`SCHEMA_CC_PIPELINE_STEP_V0` requires step `outputs`; design does not know it): step 2
    now maps `is_member` → `conjecture_holds`. `test_reference_collatz` 6/6 (gate now fails);
    construction acceptance covers the workload: 178/178 across 7 domains.
  - **Parked on dev/18 (design-language gaps for workloads):** P7 `IMPLEMENTATION_MODULE_MISPLACED`
    assumes `{domain}.implementation…`, ignoring a build config's `implementation_namespace`
    (`workloads.collatz…`); the workload build config does not discover `TEST_DATA`, so
    `TRANSFORM_WITHOUT_VECTOR` cannot be met. No new workload transform can pass P7 until both close.
    Also carried: set membership declares `value` a string and is given a boolean; declared input
    types are not checked.
  - ai_governance licence cap: next, after Collatz.
  - **Licence cap: no dossier.** The premise was wrong. `CC_ENFORCE_LICENSE_CAP_V0` was named by
    nothing; the cap is enforced by `CC_VALIDATE_ELIGIBILITY_V0` (quota check refuses at the cap).
    Deleted by hand with the user's approval (v5 keeps it; the one recorded exception to "never delete
    a v5 identity", because unreachable); two prose mentions trimmed. `routing_lookup` P0 statement and
    P2 amended ("Amended before build"). `--all` as expected; 509 artifacts.
  - Build note: the stood-down Collatz V0 still declares `evaluate_conjecture` and is compiled, so the
    V1 contract-closed check judges only contracts in force (`INVARIANT_SUPERSEDED_NOT_IN_FORCE_V0`).
  - **Platform `routing_lookup` delivered** (`delivery.md`). V1 constitution + V1
    `INVARIANT_TOPOLOGY_CONTRACT_CLOSED` by hand; V0s stood down; 20 re-pointed by construction
    (`--require 0`: 0 of 0 facts). Compiler `assert_topology_contract_closed_v1` (in force only):
    refuses a routing answer other than continue/exit and an `evaluation` block — proved by a planted
    probe. Runtime `UnknownContinuationError`. Tests `test_routing_lookup` 5/5,
    `test_unknown_continuation` 3/3. `--all` 68/68; 511 artifacts, 13 supersession relations.
  - **Item 3 (RT-6 and evaluation targets) is closed.**
- **SU-11 re-cut: scope frozen** (`.github/process/notes/su11-recut-sweep.md`). 24 published
  identities changed meaning in dev/18; the three withdrawal designs were in v5 and are out of scope.
  - Restored to v5 text (user decision): `CONSTITUTION_WORKFLOW_V0`; stood-down
    `CONSTITUTION_EXECUTION_TOPOLOGY_V0` and `WF_P7_…_V0` (v5 + stand-down marking); book_library
    `IN_`/`WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V1` (published `version: v0` kept; construction
    acceptance red by design at 176/178, 2 pinned differences).
  - 1a failed: every invariant must be named by a constitution rule. 1c taken:
    `CONSTITUTION_EXECUTION_TOPOLOGY_V1` (unpublished) names `INVARIANT_WF_ROUTING_CLOSED_V0`
    (unpublished), which it now governs. `--all` 68/68 as expected.
  - **Platform `published_rules` delivered** (`delivery.md`): `ROUTING_COMPLETE_V1` (CP-13, today's
    check as `_v1`) and `CONSTITUTION_TRACE_EXECUTION_V1` (schema V2); both V0s = v5 + stand-down;
    v0 handler = v5. Probe: narrowed surface refused by V1. `--all` 68/68; 513 artifacts, 15 relations.
    `ROUTING_COMPLETE_V1` and `CONSTITUTION_TRACE_EXECUTION_V1`; V0s restored to v5 and stood down.
  - Then three domain dossiers: blockchain (8), ai_governance (1), transformation (9).
- **First action next session.** Blockchain re-cut dossier P0 (8 published identities, `cr_06` routes).

## D1 and D2 closed in every layer; 8 gaps found — dev/18 · 2026-10-04

- **SoSyM submitted.** On the site, no DOI. The abstract was rewritten from the expert review.
- **Standards (`work/v1`).** Changes 3 and 4 add EX-18, CP-13 and EV-19 (nested composition) and
  GC-15 (construction refuses an unrouted reachable outcome). All four are core. The realization map
  now records all four as **Demonstrated**.
- **Domains, one CR each, all committed:**
  - blockchain `cr_06_routing_closure`: 4 CCs and 4 WFs answer and route BACKEND_ERROR.
  - transformation `dossiers/routing_closure`: the generator (`design/emit.py`) owns the query
    answers and the phase routing. NOT_FOUND ends a phase as EXIT_REJECTED.
  - ai_governance `cr_02_reclaim_closure`: the reclaim's DEREGISTER answers VIOLATION, which routes
    to EXIT_ACTIVE. The defect was latent, because the removal is the last step. The renderer gained
    `string (date-time)` formats and carry-forward of `extensions.description`.
- **Platform `software_governance/dossiers/routing_closure`, committed:**
  - CP-13: `ROUTING_COMPLETE` checks a step against its capability's declared outcomes, reading the
    imported platform surface in a domain build.
  - GC-15: new `workflow::INVARIANT_WF_ROUTING_CLOSED_V0`. It skips workflows not in force (SU-7).
  - EX-18: the dispatcher refuses an unlisted step outcome (`UnlistedStepOutcomeError`).
  - EV-19: `CC_STEP` requires `outcome` and `continuation`.
  - The dossier is pinned to v5 `f8356d9c`, because the working snapshot already held the change.
- **Regression.** `--all` runs 64/64 as expected. New suites: `test_routing_closure` (11),
  `test_step_outcome` (3), and the three validations (6/6, 4/4, 4/4). The artifact count is 505.
- **Correction recorded.** The superseded `WF_RECORD_VERIFICATION_DECISION_V0` is unreachable: it has
  no dispatch entry. SU-8 forbids deleting it, so it keeps its 3 gaps and no `cr_07` was needed.
- **Gaps found, not closed:**
  1. ~~`generated_discharge`~~ **Dropped, by the separation-of-concerns review.** Grounding a
     discharge against a composition the design does not own would have the design judge it, and
     whether an ending refuses is a design concept the platform does not seal and need not. The two
     deferrals (transformation generator, ai_governance reused act) are honest. Root cause: #2.
  2. Design language: no register restates workflow admission, renamed nodes or nested literal
     inputs, and there is no INVARIANT family. Held for v6.
  3. Doctrine: how to pin a platform change already in the working snapshot.
  4. The P6 checker admitted a malformed one-cell row.
  5. ~~Runtime: a fault is routed as a refusal~~ **Closed, no dossier.** A `CTFault` (module or
     IR failure, atom bug, None return, missing output), a `CSExecutionError`, or a CS result with
     no status now refuses (`CapabilityFaultError` plus an ERROR). Only an atom's own
     `CTExecutionError` routes, and it is recognised by name, because 14 atoms define their own
     class and 4 use a vendored one; one canonical class is v6. Found along the way: a CT-IR path
     that resolves to nothing yields None (RT-6, still open). `test_step_outcome` 8/8; `--all`
     64/64.
  6. The runtime proceeds past evaluation targets in `on_result`; none are in use.
  7. ai_governance is not in `construction_acceptance`.
- **SoC clean-up, done:** the dispatcher no longer writes `wf_complete` (the scheduler does);
  GC-15 reads `wf_routing`, which S4 precomputes with S2's `resolve_wf_node_keys`, so there is one
  resolver; the phase-workflow generator observes the QUERY outcomes through `si.capability.surface`
  (`emit --snapshot` is now required) rather than holding a copy. `--all` runs 64/64.
- **v6 queue:**
  - The design language restates every sealed workflow (#2). This dissolves the deferrals.
  - One declared CT refusal signal, probably refusal by return; it replaces recognition by name.
  - A Format column in `interface_fields`, replacing `string (date-time)`.
- **Committed and pushed** to `dev/18` (standards to `work/v1`) in every repo touched.
- **Process-check concerns, resolved:**
  1. **Trace schema versioned (done).** `SCHEMA_TRACE_EVENT_V1` is restored to exactly what v5
     published. `SCHEMA_TRACE_EVENT_V2` (`trace_schema_version: v2`) requires `outcome` and
     `continuation` on `CC_STEP`, and the runtime writes v2.
     - The examiner and `trace_schema_conformance` read v2; a v5 trace is refused by name.
     - The trace constitution now names V2 and states that a schema requiring more is a new
       identity.
     - `routing_closure/delivery.md` still says V1 was restated; it is delivered and not edited, and
       this entry supersedes it.
  2. **In-place semantic amendments (SU-11): the gate on cutting v6.** This is not a policy
     question. `4e` §7 and SU-11 already rule that a change of declared semantics is a new
     identity. Every change this cycle amended meaning in place, and v6 would be cited with
     identities whose meaning differs from v5's. The program:
     (a) a transformation dossier, in which an EXTEND declares whether it changes meaning; a change
         of meaning becomes `_V(n+1)`, supersedes the old identity, and has its references rewritten
         by construction;
     (b) a determination of which dev/18 changes alter meaning, re-cut through the pipeline;
     (c) cut v6.
  3. **Double ERROR (done).** `RecordedRefusal` (in `evidence.py`) is the base of
     `UnroutedOutcomeError`, `UnlistedStepOutcomeError` and `CapabilityFaultError`.
     `api.run_workflow` does not record those again. `test_step_outcome` asserts exactly one ERROR
     per refusal.
  4. **Process order: noted.** The platform dossier was written after the code; its criteria came
     from obligations the standard fixed first.
  - `--all` runs 64/64 as expected. The surface map is regenerated: V2, and the GC-15 invariant it
    had missed.
- **Committed and pushed:** V2 trace schema and the single-record refusal, to `dev/18`, with
  standards on `work/v1`.
- **SU-11 diagnosis (step a).** Already present: P7 REPLACE plus `supersedes`, construction marking
  the predecessor, and the compiler's `ASSERT_SUPERSEDED_NOT_REFERENCED_V0`. Missing:
  - **M1.** Nothing tells an amendment from a semantic change. Fix: construction compares an
    EXTEND's governed facts with the existing artifact, and a release gate diffs against the last
    cited composition.
  - **M2.** A re-point requires restating the whole referrer. Fix: a P7 `reference_repoints`
    register, with construction rewriting the reference in place.
  - **M3.** The design does not state the blast radius. Fix: a rule checks every live referrer
    against `si.artifact.refs`.
  - **M4.** External callers move by hand. Fix: list them in the delivery.
  - **M5.** No declared documentation-key vocabulary.
  - Map correction: ID-5 is Partial, not Demonstrated.
- **Closure criteria for the D1/D2 journey.**
  - **Must:**
    - M1–M5;
    - the SU-11 re-cut of dev/18's semantic changes;
    - the map corrected (ID-5, SU-11);
    - Changes 3 and 4 settled on `work/v1`, with their realization recorded in `revisions.md`;
    - the SoSyM evidence re-run on v6 (`omission.sh` O3, `outcome_survey.py`, outputs kept);
    - v6 cut: `--all`, `release.sh --check`, the `pgc_release` DOI, PyPI 6.0.0, `release-18` notes.
  - **Should:**
    - RT-6: a CT-IR path resolving to None must refuse;
    - evaluation targets in `on_result`: refuse at compile until they are executed;
    - a SoSyM reviewer-response note.
  - **Not needed to close:** the CT refusal signal, the Format column, design-language
    completeness, and ai_governance in construction acceptance.
  - **Order:** M5 → M1 → M2/M3 → RT-6 and evaluation targets → re-cut → map and standard →
    evidence → v6 → note.
- **M5 delivered:** `software_governance/dossiers/identity_semantics/` (P0–P8, Gates 0, 1 and 2),
  emitting `artifact::VOCAB_DECLARATION_REPRESENTATION_V0`. Its groups are `documentation` (9 keys)
  and `unordered` (12 keys).
  - It found a renderer defect, now fixed: a multi-group vocabulary was sealed as one group, and the
    measure still read 100%.
  - `--all` runs 64/64, with 506 artifacts and construction acceptance at 168/168.
- **First action next session.** Dossier B (`transformation/dossiers/semantic_change/`, M1–M3) at
  P0.

## v5 published; dev/18 open — 2026-10-03

- **Published.** Cycle 17 is published as `v5`. Ten repos carry one commit on `main` and the tag
  `v5`. `history-17` keeps the full cycle locally.
  - **Composition:** `pgc_release` @ `9aec833`, sealing snapshot `f8356d9c…`: 8 domains, 515
    artifacts. Version DOI **10.5281/zenodo.23129879** (concept 22184747).
  - **Components:** nine version DOIs, 10.5281/zenodo.23129781 through 23129792.
  - **PyPI:** nine packages at `5.0.0`. A clean `pip install protocol-governed-computing==5.0.0`
    resolves all nine, and `pgc` reports them. `pgc_install` is pushed at `9c1f9f1`.
  - **Release record:** `process/notes/release-17.md`; the `v5` entry in `publications.md`.
- **Verified before publishing.** A clean `regression.sh --all` ran 59 of 59 steps as expected and
  reproduced `f8356d9c…`. `release.sh --check` passed. No wheel ships declarations.
- **A finding for the next version.** The SoSyM paper's evaluation found D2. When a step omits an
  outcome its operation declares, the runtime continues past it (`dispatcher.py:182`), and the trace
  does not record the step's outcome.
  - With a corrupted contact-address registry, a failed lookup let a person be accepted.
  - A static survey finds 14 of 73 operation steps listing fewer outcomes than their operation, and
    11 act outcomes that no workflow routes, all storage failures in blockchain.
  - v5 states this as a limit. The fix is deliberately not in v5: a runtime that refuses an unlisted
    step outcome, a trace that records step outcomes, and later construction checks at both levels.
  - Evidence is in `~/omnibachi-site/sosym_doc/experiments/` (`omission.sh` case O3,
    `outcome_survey.py`).
  - The domain dossiers drafted for these gaps were dropped by the author's decision: domain gaps are
    test cases, not architecture. They are not in any repo.
- **Cleanup done.** The editable installs reported stale `3.0.0` metadata. They are reinstalled and
  report `5.0.0`. `pgc_env_check` passes.
- **Left for the author.** The remote `dev/17` backup branches are redundant with `history-17`.
  Delete them if the remotes should carry only `main` and `v5`.
- **First action next session.** Finish the SoSyM paper. It already cites v5. The supplement deposit
  and the reference check remain.

## Paused — everything committed and backed up — dev/17 · 2026-10-03

- **State.** Every repo is clean. `dev/17` now exists on GitHub as a backup in all ten dev repos
  (not merged to `main`). `standards` is on `work/v1`, in sync with its remote. `pgc_release` is in sync.
- **Last regression.** `regression.sh --all`: 59/59, every step as expected.
- **Deferred on purpose.**
  - Why a capability refused: parked in the entry below; only if an investigation stalls on it.
  - EN-12 in the realization map: worth re-checking when the standards work resumes.
  - `pgc_install` is 3 commits ahead of `origin/main`: a release decision, not cleanup.
- **First action next session.** None scheduled.

## Decision explanation graph: closed — delivered via `si.execution.explain` and the PNG — dev/17 · 2026-10-03

- **Query.** `si.execution.explain <trace>` in `snapshot_inspector` (`inspector/queries/execution_explain.py`,
  `inspector/trace.py`, contracts `TI_`/`TE_SI_EXECUTION_EXPLAIN_V0`). The trace is named by the
  runtime's own reference, read under a provisioned trace root (transport: data root; CLI:
  `--trace-root` / `$PGC_DATA_ROOT`), and refused unless it names the snapshot being read. Recorded
  facts and snapshot-joined facts stay apart (`snapshot` keys).
- **Phase 2 — why.** The runtime now records every admission check it evaluated, held or not
  (`scheduler._admit` → `CC_STEP` ADMIT `detail.checks`; declared in `SCHEMA_TRACE_EVENT_V1`). The
  query reports per node a `determination` (gate: the checks and which failed; capability: its
  outcome, explicitly *not* its reasons) and an `ending`: `declared_ending` (decided at which node,
  by which outcome), `no_declared_answer` (ERROR records — the declarations had no answer, no rule
  refused), or `incomplete`. Traces from before the change say "not recorded".
- **Correction.** EV-17 was never a phase-2 dependency: it concerns `snapshot/evidence/*`, not run
  traces. Finding 10 was already CLOSED in the map.
- **Bears on the standard (not edited — standards paused).** Admission now evidences refusals as
  fully as admissions at the gate: the map's EN-12 row (Unimplemented) is worth re-assessing.
- **Closed (KISS).** Reviewed against real collatz and blockchain runs. The picture answers which
  path, which outcome chose each route, where the run was decided, and which capability decided it;
  that one pointer is the deep-dive entry (`si artifact show` on it). Rejected as complexity without
  value: a per-node `governed_by` inventory and an artifact table in the PNG — the text answer
  already carries `artifacts`.
- **Parked, only if an investigation stalls on it.** Why a capability refused: record the refusing
  capability's result values for a non-SUCCESS outcome and draw one line at the deciding node. A
  runtime + trace-schema change — a decision about which values are determinative.
- **PNG rewired.** `protocol_runtime/runtime/trace_viz.py` now draws `si.execution.explain` over
  `si.behavior_logic.show` and reads no trace itself: recorded facts red (path, outcomes, failed
  checks, captured inputs, errors), joined capability grey, undeclared routes dashed, the deciding
  node double-bordered; refused traces are reported, not drawn. The runtime imports the inspector
  only there (optional extra `pgc-runtime[render]`); execution never does.
- **Repos touched.** `snapshot_inspector`, `protocol_transport` (`resolver.py`: data root → trace
  root), `protocol_runtime` (`scheduler.py`, `evidence.py`, `trace_viz.py`, `cli.py`, `pyproject.toml`, test, docs), `software_governance` (trace schema),
  `.github` (RUNBOOK count, `expectations.yaml`).

### Original parked idea — 2026-10-01

Not started, not scheduled. Prototype on a feature branch off `dev/17` before any merge.

- **Idea.** Extend the on-demand redlined execution-path PNG (`protocol_runtime/runtime/trace_viz.py`,
  `run --behavior-logic` / `behavior-logic <trace>`) into a decision explanation graph: for each
  node and edge, *what caused this path and which artifacts were involved*. Origin: an expert's list
  of ten next-step directions (#1, "a system that can explain every decision"), weighed in the
  standards session.
- **Shape.** A declared `si.` **query** operation (e.g. `si.execution.explain`) returns the graph as
  data; the PNG is one client rendering of it. Reads the sealed snapshot plus the trace, never
  runtime internals — `runtime examine` is the side channel ruling A.2 flagged; do not repeat it.
  An LLM narration stays client-side and is never the system's answer (IN-8).
- **Phase 1 — supported by today's data.** Route taken and the declared outcome that selected it
  (`WF_ROUTE`); per node the contract, capability FQDN and kind, projected steps, bindings (all
  already in `<WF>.graph.json`); captured non-deterministic values (`CT_STEP`). Draw inferred links
  (trace joined to snapshot) differently from recorded ones.
- **Phase 2 — needs evidence work first.** *Why admitted or refused*: closure, rules, predicate
  results, rule refusal vs closure failure. Blocked on determination records in evidence (map
  finding 10) and evidence naming its snapshot (EV-17); both are `protocol_runtime` changes.
- **Repos (checked, not guessed).** `snapshot_inspector` — the operation's declaration and generated
  `TI_`/`TE_` pair (`scripts/author_transport_contracts.py`), a `inspector/queries/` module, a
  `registry.py` entry, optionally a `client/web` view. `.github` — `RUNBOOK.md:643` "eighteen
  operations sharing one route" becomes nineteen; check the regression too. `protocol_runtime` only
  if `trace_viz` is rewired as a client. No change expected to `protocol_compiler`,
  `snapshot_assembler`, `software_governance` or `standards`; confirm by a build.
- **Trace-to-snapshot tie — already present.** The trace's first record (`trace_classification`)
  carries `snapshot_id`, verified at boot (`protocol_runtime/runtime/evidence.py:120`,
  `boot.py:104`). EV-17's Violated row concerns `snapshot/evidence/*/evidence.json`, not the trace.
  Rules for the query:
  - The trace arrives as a declared input (identity or path), never by scanning `data/traces/` (AI-12).
  - Require an exact `snapshot_id` match with the snapshot being read; refuse on mismatch or on a
    trace with no first record (IN-9). Trace addresses (`wf_addr`, `cc_code`) mean nothing elsewhere.
  - The trace is unsealed, so the tie is *claimed*, not proven; the graph labels it so.
  - The working `snapshot/` is rebuilt each time, so old traces will mismatch: regenerate the trace,
    or let the query take the snapshot root as input (e.g. a `pgc_release` copy).
  - Phase 1 needs no `protocol_runtime` change.

## CLM governs a hosted model, numbers grounded: Qwen3 8B through Ollama — work/clm · 2026-09-29

- **`cr_02_hosted_model` redone from P0 and delivered.** The first delivery was withdrawn after Qwen
  leaked a read account number digit by digit and then invented one. P0 now adds grounding: a time in
  service may require every number to be one the model read, matched on digits. P0–P8 admissible
  against `b8dd7145…`; 17 artifacts; no existing artifact changed. P7 `step_bindings` changed after
  its approval (the opening carries `ground_numbers`); the recorded approvals are by name and stand.
- **Merged:** squashed into `dev/17` (`business_domains` 2c5d5bf, `.github` a0c08be); `work/clm`
  deleted. README and ARCHITECTURE for the domain written.
- **Choice transform:** judges NFKC text; won't begin a forbidden number the model read; with
  grounding, won't begin or end a number that isn't in the reading (`numbers_from_the_reading`).
- **Host:** `host/driver.py --model qwen3:8b [--ungrounded]`. ~45 ms a token.
- **Validation:** hosted suite 15/15 in regression, 16/16 with `--qwen`; regression 59/59.
- **Open:** grounded is not true — Qwen gave the customer's own number as the spouse's. An
  evaluation harness (leak rate vs baselines) if a paper is wanted.

## Runtime performance done: a governed run in ~5 ms — dev/17 · 2026-09-29

- **Boot once, run many.** `runtime.api` keeps a booted snapshot resident per process, keyed by
  the manifest file, trust anchor and profile root; a rewritten manifest is verified afresh, and
  `boot()` itself is never cached. The HTTP server, the federation worker and coordinator, and the
  suites all run through it.
- **Pictures on demand.** A run writes its `.jsonl` only; `run --behavior-logic` or
  `behavior-logic <trace>` draws the path. It reverses "every trace has a picture"; ruled in
  `rulings.md`.
- **Measured:** ~330 ms → ~5 ms per run after the first in a process (~133 ms). The regression's
  execution block ran 189 governed runs in 2.5 s, where the runs alone used to take about a minute.
- `test_resident_boot.py` 4/4; `regression.sh --all` 58/58. No artifact or snapshot identity
  changed, so no dossier. Snapshot verification itself (item 3 below) is no longer worth doing.

## Scoped next: runtime performance on dev/17; a real model for CLM on work/clm — 2026-09-29

### Platform, dev/17 — worth doing whether or not CLM moves

Measured: one in-process governed run takes ~330 ms. Boot and snapshot verification take ~195 ms,
drawing the trace PNG ~128 ms, and the execution itself ~8 ms.

1. **Boot once, run many.** `runtime.api` boots and hash-verifies the whole snapshot on every call.
   Keep it resident, keyed by root and snapshot id, and re-verify only when the id changes. First
   confirm whether the HTTP server and the coordinator already boot once.
2. **Trace pictures on demand.** A run writes its `.jsonl` evidence only; `behavior-logic` draws the
   PNG when asked. This reverses "every execution trace has a picture", so it needs a ruling, and the
   tests and expectations that look for a PNG need updating.
3. Optional, after (1): snapshot verification itself (`pathlib` comparisons, repeated JSON reads).

Expected: under ~10 ms per governed run, and a faster regression; before-and-after timings are the
evidence. Plan to be approved before any edit.

### CLM, work/clm — a separate issue, not started

A locally hosted pretrained model (qwen3 through Ollama, thinking off; a small variant for
development) governed token by token. Model composability is a different dimension and is out.
The shape discussed: **invert control.** A driver outside PGC asks the model for its top-k offers
and submits each offer to a governed workflow that chooses a permitted token and appends it to the
record; only a release workflow releases, and only what the record holds. It needs no platform
change: no outbound side effect, no side effect inside a molecule (a molecule is a transform), no
cyclic workflow (workflows are acyclic). Limits: the platform cannot prove that offers came from the
model, and this is a new CR rather than a second realization of CR-1's offer step. It depends on the
platform items above for its performance.

## B21–B24 — dev/17 · 2026-09-28

The A batch is complete; wave 4 and B21–B24 are on dev/17, uncommitted. `regression.sh --all`:
55/55.

- **B21 — `examine` reads PGC traces.** It read RI-0's format and could not read one line PGC
  writes. It is now a `SCHEMA_TRACE_EVENT_V1` reader: path by node, contracts and results, events,
  recorded non-deterministic results, errors. It exits 1 on a structural failure — an ERROR, or a
  run that never completed — and 0 on a completed run, refusals included. It refuses any other
  format. The RI-0 classifier, hint engine and `structure.*` locator are gone.
  `test_examine.py`: 5/5, and it reads every trace under `data/`.
- **B22 — events are schema-checked.** `SCHEMA_EVENT_V1` was written from what the 25 events
  declare: a constitution named by FQDN, `subdomain`, `moment`, integer fields, `enum`. EVENT is now
  dispatched, and its `description_pending` row is gone. Four kinds remain pending: ACTOR, INTENT,
  TI and TE.
- **B23 — the blockchain web page.** Its explainer named the superseded
  `WF_RECORD_VERIFICATION_DECISION_V0`. It now names and draws `WF_ACCEPT_ACTOR_V0` and
  `WF_REJECT_ACTOR_V0`, with CR-04's reason for the split.
- **B24 — the dead platform build config.** `STRUCTURE_BUILD_PLATFORM_CONFIG_V0` is deleted, not
  superseded; `STRUCTURE_ARTIFACT_IDENTITY_V0` and the compiler's comments name V2. The compiler's
  no-argument default and `--all-structures`, both of which selected it, are removed. `compile` now
  requires `--structure`. The surface map has 197 artifacts, and human-block fidelity counts 482.
- **Noticed, not changed:** the other dispatched schemas still carry a `pgs_governance.schemas…`
  `$id`.

### B8–B10 ruled; three CRs follow

The rulings are in `process/rulings.md`. Each changes a domain's behaviour, so each lands as a CR
through P0–P8, not by hand.

- **B8 — a validator reports, and the contract refuses.** It is wider than recorded. Four contracts
  validate a record and never act on the result: book's `VALIDATE_BOOK_SUBMISSION`, `REGISTER_BOOK`
  and `REGISTER_ADDITIONAL_EDITION`, and blockchain's `VALIDATE_REGISTRATION`. Each gains CLM's
  follow-up rule, `violations == []`. The platform transform stays a reporter.
- **B9 — identity's rules become literals.** The TIs fix them as constants, but the workflows admit
  them from the payload, so a direct caller can widen them. There are three:
  - `states_admitting_a_decision`;
  - `admitted_outcomes`;
  - `registration_schema`, found while diagnosing.
- **B10 — refuse.** ai_governance's three checks keep their declared refusal. Refusal vectors
  replace the stale RI-0 ones.
- **The CRs, in order:**
  1. blockchain `cr_05_identity` (B8 and B9). Its P0 problem statement is drafted, with three
     clarifications for Gate 0.
  2. book `cr_05_catalog` (B8).
  3. ai_governance `cr_01` (B10). It is that domain's first dossier.

- **`cr_05_identity`, Gate 0 passed.** The author accepted all three recommendations: an
  incomplete registration is refused; rules a request states are ignored, not refused; a refused
  decision records nothing. The seed is ADMISSIBLE at P0, 5/5 over 83 rules. The baseline is pinned
  to `4d366cca…`, the v5 working composition: 478 artifacts, 8 domains.

- **`cr_05_identity` P1, projected.** It is the seed's registers, each row cited: 73 citations.
  ADMISSIBLE at P1, 5/5 over 189 rules, judged against its P0 prior. `tc baseline verify`:
  BASELINE OK, and no register approved yet.

- **`cr_05_identity` P2–P8, designed.** Each phase ADMISSIBLE at 5/5. P7 redeclares ten identity
  artifacts whole and creates nothing:
  - the contracts hold the schema, the sets and the rules as literals;
  - a rule step refuses an incomplete registration;
  - a comparison and a rule refuse self-decision;
  - the decided record is built from the checked decision;
  - each act fixes its decision, and registration writes UNVERIFIED itself;
  - the entrances drop the constants;
  - the acceptance gate declares optional grounds.

  P8 schedules nothing, since nothing is new.
- **A P7 rule fixed along the way.** `NODE_INPUT_UNBOUND` joined a contract's pinned inputs to the
  design's, so an input a redeclared contract withdrew still read as required. Refined in
  `transformation/design/checks.py`, re-sealed and proven in `keyed_node_design_test` (6/6), with
  a ruling in `rulings.md`. Re-sealing moved the working snapshot to `08800223…`; the baseline was
  re-pinned and p2–p7 re-approved against it.

- **Construction refused, then admitted by declaration.** `tc construction check` found 78 facts
  lost. Every loss was intended, but nothing in the design language could say so. P7 now has a
  `withdrawn_facts` register, and cr_05 declares 38 withdrawals. Construction check reaches 100%
  with nothing narrowed. The fix also covers a list refinement the guard misread; the ruling is in
  `rulings.md`. The re-seal moved the snapshot to `dcfed76f…`.

- **`cr_05_identity` delivered.** The first execution run found every registration through the
  entrance refused: the registration gate still required the schema the entrance stopped sending,
  and P3 had missed that gate. Re-authored from P3, the gate became an eleventh artifact. Emitted, and
  identity holds 22/22 criteria (3 not exercised), wallet 9/9; full `regression.sh --all` 56/56 on a
  clean rebuild, composition `61952a22…`. Admission fidelity dropped from 26 findings to 12. B25
  recorded: no rule checks that an entrance supplies what its gate requires. `delivery.md` written.

- **B25 done.** P7 holds an entrance to the gate it reaches (`ENTRANCE_UNDERSUPPLIES_GATE`, 242
  rules); the inspector publishes intents. It fires on cr_05's first-pass shape and on no current
  document. `regression.sh --all` 57/57, composition `34c8a0e8…`.

- **`cr_05_catalog` delivered.** Measuring book found worse than B8: every catalog act confirmed
  staff against rules the request sent, so an unauthorized caller registered a book by sending none.
  The author widened the scope to identity's pattern. The catalog now holds its authorization rules
  and descriptions, refuses on what its checks find, checks what it records and records the subject
  callers send (every book registered before had none). A copy is registered as registered, and a
  correction keeps its state and meets the description. 26 artifacts redeclared, 36 facts withdrawn;
  P7 and P8 generated under C1, generators kept in `.github/process/notes/cr05-catalog-generators/`.
  Catalog 23/23 and 27/27; `regression.sh --all` 57/57, composition `25009fed…`. Carried: credentials
  are self-asserted (authentication is outside the catalog).

- **`cr_01_licensing` delivered (B10).** ai_governance's three checks are proven: each is
  redeclared whole with its cases, 7 in all (the earlier RI-0 values under PGC names, each no case
  now expecting a refusal, plus the inactivity boundary). Conformance: ai_governance 3 proven. The seed
  first listed the checks' refusals as operation refusals, which obliged P7 to restate both acts and
  to discharge provisioning's denial at an ending that completes. The author ruled them the checks'
  own, proven by their cases, and dropped them from the seed. Two construction fixes came with it:
  the manifest generator now runs for an amendment and names every subdomain the domain holds, and
  `emit` carries a replaced document's descriptions forward as `check` already measured them.
  `vector_design_test` 8/8; `regression.sh --all` 57/57, composition `b8dd7145…`.

- **Testbeds cleaned.** RI-0 licensing replay and scenarios deleted; payloads that nothing ran, or
  that targeted a superseded workflow, deleted; the rest carry only what the acts read.
- **Group F done** except what the cut writes. Noticed, not changed:
  `compiler/diagnostics/determination.py` still reads `PGC_SNAPSHOT_ROOT`, and the execution paper
  states determinism without the non-deterministic atom (a published paper; the author's call).

- **`v5_readiness.md` retired.** Every A and B item is done, deferred or frozen; what the cut still
  needs is carried below.

### Carried to the v5 cut

The cut is not scheduled; one more cycle of checks comes first.

- **The cut writes:** `release-17.md`; `pgc_release/MANIFEST.md` and its README's domain count (eight);
  `pgc_install/README.md`'s version paragraph (its v5 body is committed only when v5 is published);
  a final clean regression; one re-pin of every dossier baseline that still runs phases.
- **Stated limits for the release notes:**
  - C1: a generated dossier is admitted on what it says, and keeps its generator as evidence in its
    `delivery.md`. Governed generation is v6.
  - C5: after a dropped connection, a caller cannot tell whether it was admitted. A unit idempotency
    key with an admission-status query is v6 design work.
- **Deployment and operations (D), recorded, not blocking:** the SSH exception to EO-4;
  `EVIDENCE_EXPIRY` not exercised over the shared store; cross-node concurrency only lightly
  exercised; two orphaned barcode claims kept as evidence; the evidence store is not external to
  every node; `shuttle` LXD start/stop priorities not set; the stale `/etc/hosts` line on the Mac.
- **Only someone else can close (E):** a second reader (§6 externality); the profile read-back by
  hand for the signed federated profile, which the author can do but which is still one reader.
- **Deferred or frozen:** B17, the signed federated profile existing twice, waits for the next
  standards revision. B18, 13 domain transforms unproven and implementation source not sealed by
  hash, is recorded, not fixed. Both are in `standards/doc/parkinglot/todo.md`.

## A batch complete — wave 4: the identity covers the profile's content — dev/17 · 2026-09-28

Waves 1–3 are committed. Wave 4 and the batch's close are on dev/17, uncommitted.
`regression.sh --all`: 54/54.

- **A1 — the profile's content is in the identity.** The manifest carries `profile_sha256`, a
  digest of the claimed profile's `snapshot_profile` declaration, and `identity_covers` names it.
  Acceptance recomputes it from the profile as it now reads. A profile changed after sealing is
  refused, and so is a manifest that does not cover its profile. Profiles stay in `.github`, per the
  A1 ruling.
  - `test_warm_boot.py` is now 8/8. The two new cases change a copy of the claimed profile after
    sealing, and delete `profile_sha256`.
  - A snapshot sealed before v5 carries no `profile_sha256` and is refused by this acceptance. That
    includes `pgc_release/snapshot`, which v4's tooling still verifies.
- **The batch's close.**
  - **Surface map regenerated:** 198 artifacts, up from 195 — the transform-wide constitution, the
    signed-snapshot structure and the not-in-force invariant.
  - **No dossier was re-pinned.** Every CR with a dossier is delivered, and a delivered dossier's pin
    records the composition it was designed against. The next CR pins the v5 composition.
  - **Docs:** the `snapshot_assembler` README and ARCHITECTURE now state the profile rule and the
    declared output root.

**Next:** the B items still open (B8–B10 await rulings; B21–B24), then group F, the documentation
refresh, before the v5 seal.

## A batch, wave 3: the governance surface — dev/17 · 2026-09-28

Waves 1 and 2 are committed. Wave 3 is on dev/17, uncommitted. `regression.sh --all`: 54/54.

- **A2 — handler keys.** 94 registry keys, three prefix constants and seven invariants now say
  `pgc_governance.handlers.*`. It is behaviour-neutral: the same assertions run on the same inputs.
- **A6 — transform-wide rules.** `CONSTITUTION_CAPABILITY_TRANSFORMS_V1` carries surface closure,
  derived closure and implementation admissibility; `DETERMINISTIC_ATOMS_V0` no longer does. No
  transform is `governed_by` it.
- **A8 — record locks.** `FEDERATED_NODE` declares `shared_store_requirement: posix_record_locks`,
  and says why an object store cannot carry a node group's store.
- **A7 — `cryptographic_trust` V1**, the way placement went to V1: V0 deleted, not superseded.
  - `LOCAL_DEV_UNSIGNED` and `SIGNED_SNAPSHOT` are authorized; the build configuration selects one.
  - The federated build now declares `SIGNED_SNAPSHOT`. Before, it claimed `LOCAL_DEV_UNSIGNED`
    against V0's own rule that unsigned snapshots stay local.
  - The runtime still does not branch on the mode; a node holding an anchor verifies.
- **A11 — presence is not force.** `INVARIANT_SUPERSEDED_NOT_IN_FORCE_V0` declares one predicate,
  realized once in `compiler/atoms/force.py`, and asked at selection, assertion derivation,
  dispatch entry and admission. S8 checks the outputs: anything superseded that still confers effect
  fails the build.
  - **The exposure was not nil.** Two superseded workflows were dispatchable, and the book catalog's
    CR-01 validation ran one. It now runs V1, the act in force.
  - `admission_contract_fidelity` drops to 26 findings over 34 gates. The five findings that went
    were all on the superseded `WF_RECORD_VERIFICATION_DECISION_V0`'s gate.
- **A10 — output roots.** Each build configuration declares `output_configuration.root`; the
  compiler no longer reads `PGC_SNAPSHOT_ROOT`. Two in-force configurations of one repository naming
  one root are refused, and a configuration naming none cannot be built. `compiler.cli output-root`
  prints where a configuration writes; `compile.sh` asks it.
- **Tests.** `test_force_and_output_root.py`, 8/8, in `regression.sh`.
- **Findings.**
  - **B23:** the blockchain web client's explainer describes the superseded workflow.
  - **B24:** `STRUCTURE_BUILD_PLATFORM_CONFIG_V0` is dead but still named.
  - **F:** `pgc_install`'s README, the SU-7 realization entry, and three landed design notes.

**Next:** wave 4, A1 — where profiles live, still to be ruled. Then the batch's end: re-pin the
dossier baselines, regenerate the surface map, SOTU.

## A batch, waves 1–2: traces name places; evidence says what to ignore; routes resolve against the composition — dev/17 · 2026-09-28

The A batch changes identity, so it lands whole before the v5 seal, in four waves (plan in
`v5_readiness.md`). Wave 1, evidence, is committed. `regression.sh --all`: 53/53.

- **A9 — traces name the node.** `CC_START`/`CC_COMPLETE` carry `node`, and `WF_ROUTE` carries
  `from_node` and `to_node`: the ending reached, or null where an outcome reached neither. One
  contract at two places is now two places in the evidence. The PNG path is read from these.
- **A5 — the trace schema is the trace.** `SCHEMA_TRACE_EVENT_V1` replaces a V0 that described
  RI-0's format and shared no field with PGC's. The file is a header, then events with a fixed
  envelope. `trace_schema_conformance.py` is a regression step: 84 traces, 2292 lines, all conform.
- **A3/A4 — what a replay ignores is declared.** `VOCAB_EVIDENCE_CONTENT_CLASSIFICATION_V1` adds
  `observational_keys: [record_id]`, stripped wherever it appears. The trace header carries it, and
  `runtime.replay` reads it from there. CLM's validation lost its `STORE_ASSIGNED` exception: a
  replay agrees on every determinative event.
- **B7 — events carry ATTRIBUTE fields.** The event renderer merges ATTRIBUTE into the schema and
  sets `core.moment`. The machine blocks of six events were patched to match.
- **A defect, found and fixed.** S5 sealed an atom that a contract runs directly without its
  `ct_purity`, so a non-deterministic one was neither recorded nor replayed. It now is.
- **Findings.**
  - **B21:** `pgc_runtime examine` still parses RI-0 traces.
  - **B22:** `SCHEMA_EVENT_V0` is stale and not in the schema dispatch.

**Wave 2, B6 — done.** `si.behavior_logic.list` rows now carry `nodes`, the workflow's node keys.
P7 declares the observation, and `tc phase emit` generated the judging step and re-sealed P7.
`TOPOLOGY_ROUTE_RESOLVES` now accepts a route to a place the composed workflow already has.
Blockchain cr_03 row 3 no longer fires. Test counts: inspector 122/122, `keyed_node_design_test`
5/5. Regression: 53/53.

**Next:** wave 3, the governance surface — A2, A6, A8, A7, A11, A10. Ask again where profiles live
(A1) before wave 4.

## v5 parking lot opened; every trace draws its path — dev/17 · 2026-09-28

v5 is planned, not scheduled. Every item left open since v4 is triaged in
`.github/doc/v5_readiness.md`.
- **A — identity-changing:** one batch, landing before the v5 seal.
- **B — defects.**
- **C — decisions.**
- **D — deployment limits.**
- **E — needs a second reader.**
- **F — documentation.**

Rulings now have a versioned home, `.github/process/rulings.md`. Each repository's `CLAUDE.md` is
gitignored, so a ruling kept only there was neither versioned nor backed up.

### Every execution trace has a picture again

- **What it does.** Every `run_workflow` writes `<trace_id>.png` beside `<trace_id>.jsonl`: the
  workflow's behavior-logic graph with the path the run took drawn in red. RI-0 had this; PGC had
  lost it.
- **It is a projection.** The JSONL is the evidence and nothing reads the picture back, so rendering
  never fails a run. Without graphviz, or for a workflow with no published graph, there is simply no
  picture. `PGC_TRACE_PNG=0` turns it off; that is deployment configuration under ruling C2/C3.
- **What it costs.** About 0.25 s per run. The full clean regression went from about 1m 24s to about
  1m 51s, and every one of its 167 traces has a picture.
- **The path is walked by routing, not matched by contract.** The drawing follows the recorded
  `WF_ROUTE` outcomes, in order, over the graph's node-keyed edges. The old walk matched
  `CC_COMPLETE` events to nodes by contract code. It lost the path at the first node whose key isn't
  its contract's code, so CLM's submission was drawn only halfway. Every CLM path now draws to its
  own record node and exit. Test: `test_trace_path.py`, 4/4, in `regression.sh`.
- **`behavior-logic` works again.** Both `pgc_runtime behavior-logic` and `run --behavior-logic`
  looked for graphs in the RI-0 layout (`<workspace>/protocol_snapshot/…`, `PGS_WORKSPACE`). They
  now read `snapshot/behavior_logic/<domain>/<WF>/`, from `--snapshot` or `PGC_SNAPSHOT_ROOT`.

### Also done since the rename

- **C rulings.** They are recorded in `rulings.md`:
  - **C1:** a generated dossier is a stated limit. CLM's `delivery.md` now says its P7 and P8 were
    generated.
  - **C2/C3:** deployment configuration is not branching. The runtime's defaults are gathered in
    `runtime/federation/defaults.py`.
  - **C4:** record locks are declared in the FEDERATED_NODE placement. It is pending, as A8.
  - **C5:** EO-2 is a stated limit.
- **B fixes:**
  - B1: the surface map is regenerated (195 artifacts) and a stale generator case removed.
  - B2: `software_governance/CLAUDE.md` is corrected. The file is gitignored.
  - B3: the runtime workflow-execution test passes, 7/7.
  - B4: the `emit --help` text is corrected.
  - B5: the new P7 rule `TEST_VALUE_UNPARSEABLE` brings P7 to 235 rules, sealed.
  - B16: `rulings.md`.
  - B19: `behavior-logic`, as above.
- **Re-diagnosed into batch A:**
  - **B6** is a false positive in `TOPOLOGY_ROUTE_RESOLVES`. The rule doesn't resolve an
    amendment's route against the workflow's existing nodes; blockchain's artifact is correct.
  - **B7** is confirmed and wider. Event fields declared as ATTRIBUTE were dropped:
    `EV_WALLET_CREATED_V0` was sealed with only `timestamp`, and blockchain cr_01's identity events
    follow the same pattern.
- **New findings:**
  - **A9.** A trace records which contract ran, not which node. The picture is right because the
    graph names nodes; the evidence still doesn't.
  - **B20.** `regression.sh` exits 0 when a test script fails.
- **Deferred:** B17 waits for the next `standards` revision.

### The regression now has a verdict (B13, B20)

The RUNBOOK's expected results used to be prose nothing evaluated, and `regression.sh` exited 0
whatever its steps did.

**What the run does now:**
- **Every step through a wrapper.** Every check and execution step runs through `step`, which keeps
  its output and exit code in `traces/regression/` (or `$PGC_REGRESSION_OUT`).
- **Expectations as data.** `.github/process/expectations.yaml` is the "## Expected" table as data,
  52 steps with exit codes and exact counts.
- **A verdict.** `regression_verdict.py` compares the run against those expectations, and the script
  exits with the verdict.

**The run fails on any of these:**
- a failing step, or a count that moves;
- an **unexpected pass** — admission fidelity's 31 findings, or the inspector's two advisories
  (15 and 1), coming back green;
- a step expected and not run, or run with no expectation;
- a unittest suite that skipped everything.

**Tests and results.** `test_regression_verdict.py` passes 8/8 and runs as a step itself.
`--all`: **52/52 steps as expected, exit 0**. Execution only: 8/8.

**RUNBOOK "## Expected" now points at the data.** The stale rows are corrected: construction 150/150
across 5 domains, molecule 5/5, conformance evidence 36/36, runner 10 tests. The cycle's new tests
and the CLM suite are added.

**The new habit:** a count that changes on purpose is changed in `expectations.yaml` and the RUNBOOK
in the same commit, with the reason.

### B14, B15 done; B11, B12 moved to batch A

- **B14 — `publish_component_releases.sh` is back in `.github/process/`.** It is rewritten, because
  the staged copy was lost with an old scratchpad.
  - It refuses to publish unless Zenodo answers and every component has its release webhook.
  - It skips components already released.
  - It reads the component list from `compose_release.py`.
  - `--verify` checked against v4: 9/9 components have a record. The publish path first runs at v5.
- **B15 — `pgc_install/README.md` (`main`) documents the `⚠ Machine-block health` advisory.** The
  second newcomer gap, compile writing into the clone, was already covered in §4. The README's V1
  build-configuration names are right for the published v4 and change with v5 (F).
- **B11 (output root) and B12 (supersession in force) moved to batch A.** Each fix declares something
  in a governed artifact: the output root in each build configuration, and an `in_force` predicate
  with an invariant that every effect path consults it.

### Next

- **The A batch first, by decision:** A1–A9, with B6, B7, B11 and B12 folded in. A plan is being
  drawn; then one clean regression and one re-pin.
- **B8, B9, B10 wait for business rulings:**
  - B8: should the catalog's structure validation refuse?
  - B9: should identity take its admitted states as a literal, as wallet does?
  - B10: for ai_governance's three vectors, answer or refuse? That one is its own CR.

---

Older entries: `process/notes/sotu-archive-to-v5.md`.

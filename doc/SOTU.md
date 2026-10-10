# SOTU Handoff

## SOTU Handoff — 2026-10-10 · transformation rebuild chartered; checkpoint before the oracle tag

### Changes Made
- `transformation/doc/REBUILD_CHARTER.md` — new. Freezes transformation as the oracle and rebuilds the module on a branch, designed once from the unravel. Scope, acceptance against the oracle, identity at the swap, the governance exception, sequence, open decisions.
- `transformation/doc/TRANSFORMATION_UNRAVEL.md` — §10 vehicle: the charter replaces the dossier-per-change plan.
- `transformation/dossiers/version_retirement/` — P0–P6 ADMISSIBLE, terminal at P6. Parked as evidence and not delivered.
- `transformation/dossiers/register_format/` — P0–P7 ADMISSIBLE. Parked as evidence and not delivered.
- `.github/process/retention.yaml` — new. Development is open; nothing is retained for its own sake; no stable baseline.
- `.github/process/retired_identities.yaml` — new ledger (`4e` SU-12). One entry, the deletion that `REMOVED` used to hold in code.
- `.github/process/retirement.py` — new shared reader: validates both files and finds the retired identities a live artifact names (`supersedes`, keys and `next` targets excluded).
- `.github/process/published_identity_check.py` — `REMOVED` dict gone. A missing published identity needs a ledger entry. A ledgered identity present, or named by a live artifact other than its successor, is a finding.
- `.github/process/supersession_agreement.py` — a successor may name an absent predecessor only if the ledger records it.
- `.github/process/expectations.yaml`, `RUNBOOK.md` — new pass lines for both checks.

### Build & Test Status
PASSING. `regression.sh --all`: 71/71 as expected.

### Open Issues
- The trial deletion of the 11 dead transformation artifacts failed at S4: `ASSERT_PROTOCOL_SURFACE_CLOSED_V0` refuses a successor's `supersedes` naming an absent identity (10 violations). The files are restored. Decided fix (option B): exempt `supersedes` from surface closure, as a `software_governance` change judged by the oracle. The 11 ledger entries are drafted in `.github/process/notes/rebuild-retirements.yaml`, and they go into the ledger at the swap.
- P3 of `version_retirement` missed the compiler blocker. Its beliefs came only from what P0 named.
- `standards/doc/realization_map.md` SU-12 row still says nothing records a deletion. That is out of date, and it lives in the standards repo (`work/v1`).
- Earlier open issues stand: `emit.sources()` template path; the `generated` gate is case-insensitive.

### Architectural Concerns
- The charter re-opens the "last exception" ruling. Record it in `.github/process/rulings.md` once the charter is approved, before the branch opens.

### Next Session Should Start With
The human approves `transformation/doc/REBUILD_CHARTER.md` and its open decisions (§11), commits the checkpoint, and tags the oracle. Then write the ruling, then `REBUILD_DESIGN.md`.

## SOTU Handoff — 2026-10-10 · transformation unravel: rule_effectivity parked, binding_literals + quoted_literals built

### Changes Made
- `transformation/doc/TRANSFORMATION_UNRAVEL.md` — §9 checklist: carrier (A), rule identity = schema `$id`, effectivity in the schema's revision history, schema file arrives with the format change carrying identity only (committed in 446b0cb).
- `transformation/dossiers/rule_effectivity/` — re-authored as change 1 (format): p0–p6 ADMISSIBLE; p3 gains Q7 and the missing `CC_JUDGE_AGAINST_COMPOSITION_V1`; p5/p6 REPLACE 15 artifacts + 3 VOCABs; p7 drafted, INADMISSIBLE (26 findings, all the binding-literal defect). **Parked at P6.**
- `.github/process/notes/rule-effectivity-generators/p7_design_intent.py` — generator for rule_effectivity's p7 (v5 ruling C1 evidence).
- `transformation/dossiers/binding_literals/` — new dossier p0–p8, all ADMISSIBLE 5/5, Gates 0–2 taken.
- `transformation/transformation/design/p7_design_intent/rules.py` — `LITERAL_FORMS` shared by `BINDING_SOURCE_MALFORMED` and `MOLECULE_BINDING_SOURCE_MALFORMED`; new rule `GENERATED_SOURCE_WITHOUT_GENERATOR` (reserved source `generated`).
- `transformation/transformation/templates/p7_design_intent_template_v0.md` — §7 states what a literal is and that `generated` is reserved.
- `transformation/registry/design/workflows/WF_P7_DESIGN_INTENT_ADMISSIBILITY_V2.md` — new, emitted, 243 rules; V1 gains `superseded_by`.
- `transformation/transformation/design/emit.py`, `registry/design/intents/IN_DESIGN_INTENT_SUBMITTED_V0.md` — sealing target and intent point at V2.
- `transformation/scripts/testbed/binding_literal_design_test.py` — 7 probes.
- `transformation/scripts/testbed/e2e_phases_test.py`, `differential.py` — P7 workflow V2, 243 rules.
- `transformation/scripts/testbed/construction_acceptance.py` — a dossier with no p8 determines nothing (the parked rule_effectivity crashed it).
- `transformation/scripts/testbed/differential.py`, `e2e_phases_test.py` — workflow identities from `emit.workflow_fqdn`, rule counts from the declared phases; no version or count is restated.
- `transformation/doc/TRANSFORMATION_UNRAVEL.md` — §9 "Obligations carried into later changes": typed `generated` marker (change 2), one literal specification (change 3), render vectors (change 4).
- `transformation/CLAUDE.md` (gitignored, local only) — doctrine: a defect blocking an in-flight dossier is fixed in sequence, not as a child.
- `.github/process/regression.sh`, `expectations.yaml` — adds the probes; supersession 34→35, artifacts 535→536, p7 242→243.
- `transformation/dossiers/quoted_literals/` — new build dossier p0–p8, all ADMISSIBLE 5/5, pinned `ba9000fa…` (the composition with binding_literals); Gates 0–2 taken. Authors no artifact.
- `transformation/transformation/build/render.py` — `_binding` renders a quoted literal as the text between its quotes and a decimal as a number; the shared `_literal` (defaults, properties) is unchanged.
- `transformation/scripts/testbed/keyed_node_design_test.py` — expects each reason as its value, not quoted text.
- `transformation/scripts/testbed/binding_literal_design_test.py` — 8th probe: construction renders a literal as its value.

### Build & Test Status
PASSING. `regression.sh --all` (after quoted_literals): 71/71 as expected; construction acceptance unchanged at 183/185. Red by design, unchanged: `admission_contract_fidelity`, `construction_acceptance` 183/185, `si_snapshot_validate`, `blockchain_identity`. Every existing P7 corpus document keeps its verdict and findings; only the rule count moved.

### Open Issues
- Nothing committed since 446b0cb; the binding_literals implementation is partly staged in `transformation` and `.github`.
- binding_literals and quoted_literals have no `delivery.md`; their p7s were hand-written (no generator to keep).
- The new rule's gate is case-insensitive: `Generated` also reads as the reserved source.
- `transformation/design/emit.py` `sources()` writes `templates/<template>` into every generated artifact's provenance; the templates live at `transformation/templates/`. Designs mirror emit's spelling until it is corrected by a designed change.
- rule_effectivity re-pinned to `ba9000fa…`; p0–p8 ADMISSIBLE (p8 by `p8_authoring_mandate.py`). Stopped before Gate 2: change 1 had drifted into two concerns. Re-cut decided in `transformation/doc/TRANSFORMATION_UNRAVEL.md` §9.10 (R1 re-cut, R2 re-author, R3 (b) convert test copies, R4 withdraw placeholder). Cut design committed; dossier renamed `register_format` with a narrowed p0; the rule-effectivity p0 kept for the later change.

### Architectural Concerns
- rule_effectivity resumes against the composition binding_literals produces (quoted_literals changes no artifact): re-pin, and its codes shift by one (`WF_P7_DESIGN_INTENT_ADMISSIBILITY_V3`).
- A design cannot discharge a refusal with a rule its own change adds; binding_literals defers its one refusal to the rule it adds.
- The step-binding form rules and the renderer each define a literal; `LITERAL_FORMS` is the design side only.

### Next Session Should Start With
Gate 0 on `transformation/dossiers/version_retirement/p0_business_problem_statement.md` (retention policy + recorded deletion; blocks register_format). `register_format` is parked at P7 (P0–P7 ADMISSIBLE, Gate 1 taken) until it is delivered.

## SOTU Handoff — 2026-10-05 · typed step inputs (dev/18 step 9)

### Changes Made
- `software_governance/capability_transforms/registry/capability_transforms/CT_PURE_REQUIRE_TRUE_V0.md` — new atom: boolean in; SUCCESS when true, VIOLATION when false.
- `software_governance/capability_transforms/implementation/ct_pure_require_true_v0.py` — its implementation.
- `software_governance/capability_transforms/registry/test_data/TEST_DATA_CT_PURE_REQUIRE_TRUE_V0.md` — two vectors.
- `software_governance/registry/capability_transforms/invariants/INVARIANT_CT_SURFACE_CLOSED_V2.md` — closed list adds the atom; V1 gains `superseded_by`.
- `software_governance/registry/capability_transforms/invariants/INVARIANT_CT_INPUT_TYPED_V0.md` — new rule: a step input has the type its transform declares.
- `software_governance/registry/capability_transforms/constitutions/CONSTITUTION_CAPABILITY_TRANSFORMS_V2.md` — names SURFACE_CLOSED_V2 and CT_INPUT_TYPED_V0; V1 stood down and still names SURFACE_CLOSED_V1.
- `software_governance/registry/{capability_transforms,governance}/constitutions/*` — prose names the transform constitution V2 (deterministic, non-deterministic, molecules, governance).
- `software_governance/surface_map/governance_surface_map.yaml` — regenerated, 207 artifacts.
- `protocol_compiler/compiler/governance_engine/assertions/handlers/assert_ct_input_typed_v0.py` + `__init__.py` — new handler, registered.
- `protocol_compiler/scripts/testbed/test_input_typed.py` — 7 tests; `test_platform_vectors.py` counts 13 platform transforms.
- `conformance_workloads/workloads/collatz/cr_dossiers/cr_02_typed_decision/` — P0–P8 + delivery.
- `conformance_workloads/workloads/collatz/registry/collatz/capability_contracts/CC_VERIFY_TERMINATION_V2.md` — decides with the new atom; V1 stood down; `WF_COLLATZ_CONJECTURE_V0` re-pointed.
- `.github/process/published_identity_check.py` — follows a successor chain to its end.
- `.github/process/regression.sh`, `expectations.yaml` — adds `test_input_typed`; counts 535 / 34 / 37 / 183/185 / 16 advisory copies.
- `.github/process/notes/dev18-changes.md` — step 9 and the updated result table.
- `standards/doc/realization_map.md` — CP-2 records the rule.

### Build & Test Status
PASSING. `regression.sh --all`: 70/70 as expected. Red by design, each with its reason: `admission_contract_fidelity`, `construction_acceptance` (183/185), `si_snapshot_validate` (16 advisory copies), `blockchain_identity` (21/22). Published identity: none of 500 changed meaning, 1 removed by name. The planted V1 step fails the Collatz build on `ASSERT_CT_INPUT_TYPED_V0`.

### Open Issues
- All five repos are committed, each 1 ahead of origin: push pending.
- Commit subjects carry wrapped-line double spaces (cosmetic).
- cr_02 has no `baseline.json` approvals; Gates 1 and 2 were taken under the author's sweep go-ahead.
- `CC_VERIFY_TERMINATION_V1` is deletable by a recorded human act (SU-12): created and stood down this cycle, never published.

### Architectural Concerns
- The type rule checks transform steps only; side-effect step inputs and `$.` paths other than `$.inputs` and `$.results` are not compared.
- The runtime still does not check step inputs (`protocol_runtime/runtime/ct_executor.py:238-253`); build refusal is the only guard.
- Adding any platform atom forces a new version of the closed surface invariant and of its constitution.
- The architecture items in the park list of `dev18-changes.md` are unchanged.

### Next Session Should Start With
Push the five repos (`software_governance`, `protocol_compiler`, `conformance_workloads`, `.github` on `dev/18`; `standards` on `work/v1`). Then decide whether to remove `CC_VERIFY_TERMINATION_V1`.

## dev/18 replayed and renamed; no cut planned — dev/18 · 2026-10-05

- **State.** The D1/D2 work was rebuilt from each "VERSION bump to 18" commit and is now `dev/18` in
  all ten dev repositories. The first attempt is the tag `archive/dev-18-original`. Every repository is
  clean and pushed. No cut is planned; further work continues on `dev/18`.
- **Done-checks D1–D4 hold.**
  - `regression.sh --all` passes 69/69 as expected.
  - Published identity: none of the 500 identities v5 published changed meaning. One,
    `CC_ENFORCE_LICENSE_CAP_V0`, was removed by name.
  - The record is in `process/notes/dev18-changes.md`: the done-checks, the result, the park list
    and one change note per platform step.
- **Against v5:** 27 new artifacts, 24 stood down, 36 re-pointed, 4 changed in explanation only, 1
  removed, 0 deletable.
- **Delivered dossiers:**
  - `blockchain/cr_06_routing_closure` (8 V1s);
  - `ai_governance/cr_02_reclaim_and_parameters` (2 V1s);
  - `collatz/cr_01_termination_gate` (1 V1).
- **Realization map updated** on `standards` `work/v1`: SU-11 moves to Partial, ID-5 and CP-13 name
  what the replay built, and SU-12 records the licence-cap deletion. EX-18, EV-19, GC-15 and RT-6 were
  checked and are unchanged. The spec is unchanged, so no revision is declared. The publication rule
  was dropped: the replay authored every identity once, so ID-5 and SU-11 hold as written.
- **Closed.** D1–D5 hold, except the release notes, which wait for a cut. The SoSyM re-run waits for
  Springer.
- **Ideas the author is holding, not documented on purpose:**
  - retirement of stood-down identities;
  - a per-platform coherency declaration in place of one version number across the repositories.

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

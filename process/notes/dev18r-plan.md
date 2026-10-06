# dev/18r — replay plan

dev/18r restarts the D1/D2 work from each repository's "VERSION bump to 18" commit. It carries
dev/18's code in its final form and authors each change of meaning once, under a new identity.
`dev18r-file-ledger.md` lists what each dev/18 file becomes. `dev18-root-cause.md` explains why.

## 1. Baseline

| Repo | Bump commit |
|---|---|
| software_governance | `4773012` |
| business_domains | `9636160` |
| transformation | `5916228` |
| protocol_compiler | `8273568` |
| protocol_runtime | `50d5106` |
| conformance_workloads | `bc9ff15` |
| snapshot_inspector | `816a977` |
| protocol_transport | `7d235b3` |
| snapshot_assembler | `380d2a9` |
| .github | `0ac0321` |

`standards` is not branched. Its map and standard changes stay on `work/v1`.

The bump's expectations hold: 504 artifacts and 7 supersession relations. Construction acceptance
reproduces 167/167 across 5 domains. Step 1 confirms this before any change.

## 2. Done-checks

dev/18r is merge-ready when every check below passes. Each step ends by running the checks that
apply to it so far.

| # | Check | Command |
|---|---|---|
| D1 | The regression passes as expected, and every red-by-design step has a written reason. | `regression.sh --all` |
| D2 | No identity published in v5 changes meaning. Only stand-down markings and declared re-points are allowed. | `published_identity_check.py` (step 3), expected 0 |
| D3 | Construction refuses a change of meaning under an old identity. | `semantic_change_design_test.py` |
| D4 | No rule in force contradicts another. | the compile, plus `test_routing_closure` and `test_routing_lookup` |
| D5 | Every known deviation appears in the realization map and the release notes. | read, at step 9 |

**Rules for the work.**
- A finding is fixed in dev/18r only if it makes a done-check fail. Anything else gets one line in
  the park list (§6).
- No count goes into a note or the SOTU unless a command produced it, and that command is named.
- A domain change runs the dossier pipeline. A platform change runs a change note plus the regression,
  with one approval.
- The regression keeps a copy of the snapshot and restores it if the build fails.

## 3. How code is carried

Code is carried by **file, in its final form**, not by cherry-picking commits. In each step:

```
git checkout dev/18 -- <paths>
```

This drops dev/18's edit-then-restore pairs. For example, `assert_topology_routing_complete_v0.py`
was edited, then restored, so it is never touched.

- A file lands whole in the first step that needs it. If it also carries a later step's change, that
  change must be dormant until the later step, and the regression proves it.
- Where dev/18 code names an identity that dev/18r spells differently, the step edits that name.
  Each such edit is listed in its step.
- `.github` files (`regression.sh`, `expectations.yaml`) are edited step by step, not checked out.
  A test joins the regression in the step that brings it.

**Why this order.** A compiler handler is dormant until an invariant names it: S4 looks up handlers
through the invariant's `enforced_by`. So compiler checks can land before their rules. Runtime
changes are not gated this way: they take effect on landing. So every domain has to route its
outcomes before the runtime step.

## 4. Steps

### Step 1 — Branch and baseline (git only)

- Create `dev/18r` from each bump commit.
- Run `regression.sh --all` and confirm it matches the bump's expectations.

### Step 2 — Protect the build (.github; change note)

- `regression.sh` copies `snapshot/` before a clean rebuild and restores it if the rebuild fails.
- Check: D1.

### Step 3 — Reference declaration (platform; change note)

- **Artifact.** `artifact::VOCAB_DECLARATION_REPRESENTATION_V0`, with dev/18's final V1 content. It
  includes the `code` reference key and keyed `bindings`.
- **Compiler** (from `f2110b9` and `49f8a2c`):
  - `representation.py`, `error_codes.py` (E105) and `s1_extract.py`;
  - the FQDN-only and superseded handlers;
  - `test_reference_semantics.py` and `test_vector_build.py`.
- **Name edits.** In `representation.py` and `error_codes.py`, `DECLARATION` and the hint name V0.
- **Inspector** (`4bfeb43`): `graph.py` reads the record of references.
- **.github.**
  - Bring `su11_sweep.py` in from the scratchpad as `process/published_identity_check.py`, with the
    declaration read as V0.
  - Expected result: 0 breaches.
  - It reads `transformation.build.sameness`, so this step also brings `sameness.py`.
- **Watch for.** `s4_govern.py` changes in both this step and step 7. Check it out here and confirm
  the step 7 changes stay dormant.
- **Checks:** D1, D2.

### Step 4 — Transformation: semantic change and routing (change note)

Every artifact this step replaces is written by the generator (`emit_rule_sets`), and a dossier
would be judged by the P7 rules it replaces. It runs as a change note.

- **Code** (all transformation tooling at dev/18's head):
  - `render.py`, `completeness.py`, `generators.py`, `sameness.py`, `cli.py`, `emit.py`;
  - `p7_design_intent/rules.py` and the P7 template;
  - `emit_rule_sets.py`;
  - `differential.py`, `e2e_phases_test.py`, `keyed_node_design_test.py` and
    `construction_acceptance.py`.
- **Name edits** in `emit.py`:
  - `SEALED_IN` names V1 for P2–P8;
  - the judge-contract paths name V1.
- **New artifacts:**
  - `CC_JUDGE_AGAINST_SNAPSHOT_V1` and `CC_JUDGE_AGAINST_COMPOSITION_V1`;
  - `WF_P2…P6_…_V1` and `WF_P8_…_V1`;
  - `WF_P7_…_V1`, which carries B's rules and the NOT_FOUND route.
- **Predecessors.** The 2 judge contracts and 7 phase workflows (P2–P8) each gain `superseded_by`
  and nothing else.
- **Re-points.** `IN_DESIGN_INTENT_SUBMITTED_V0`, plus every referrer the dossier's P2 measures.
- **Tests:**
  - `semantic_change_design_test.py` replaces `withdrawal_design_test.py`;
  - `testbed/routing_closure/execution_validation.py`.
- **Book library.** The renderer takes `version` from the identity, which leaves two book differences
  pinned red by design. Both are sealed in v5.
- **Checks:** D1, D2, D3.

### Step 5 — Blockchain dossier

This ports `cr_06_routing_closure`'s design as REPLACE.

- **New artifacts:** V1s of `CC_RESOLVE_ACTOR`, `CC_CLAIM_WALLET_IDENTITY`, `CC_CREATE_WALLET_RECORD`,
  `CC_APPEND_WALLET_OCCURRENCE`, `WF_REGISTER_ACTOR`, `WF_ACCEPT_ACTOR`, `WF_REJECT_ACTOR` and
  `WF_CREATE_WALLET`.
- **Predecessors.** The 8 V0s gain `superseded_by` only.
- **Re-points:**
  - `TI_REGISTER_ACTOR_V0`, `TI_ACCEPT_ACTOR_V0` and `TI_REJECT_ACTOR_V0` (`handler.workflow`);
  - the four `IN_ACTOR_*` and `IN_WALLET_CREATION_V0` intents (`workflow`, by short code).
- **Tests.**
  - `blockchain/testbed/routing_closure/execution_validation.py`.
  - Every test that runs the workflows by full name:
    - the identity, wallet and routing-closure validations;
    - the runtime determinism test.
- **Checks:** D1, D2, D3.

### Step 6 — ai_governance dossier

This replaces `cr_02_reclaim_closure` and `cr_03_parameter_result`.

- **New artifacts:** `CC_RECLAIM_UNUSED_LICENSE_V1` and `CC_VALIDATE_TOOL_PARAMETERS_V1`. Both V0s
  gain `superseded_by`.
- **Re-points:**
  - `WF_GOVERN_AGENT_ACTION_V0` (`code`);
  - the reclaim contract's one referrer.
- **Not deleted.** `CC_ENFORCE_LICENSE_CAP_V0` stays as v5 published it (parked, §6).
- **Tests:** `ai_governance/testbed/routing_closure/execution_validation.py`.
- **Checks:** D1, D2, D3.

### Step 7 — Platform routing rules (change note)

- **New artifacts:**
  - `CONSTITUTION_EXECUTION_TOPOLOGY_V1`, which names both new invariants and `WF_ROUTING_CLOSED`;
  - `INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V1` and `INVARIANT_TOPOLOGY_ROUTING_COMPLETE_V1`;
  - `INVARIANT_WF_ROUTING_CLOSED_V0`, governed by topology V1.
- **Predecessors.** The topology constitution V0 and both invariant V0s gain `superseded_by` only.
  `CONSTITUTION_WORKFLOW_V0` is untouched.
- **Re-points.** The 20 `governed_by` references move to topology V1, once each.
- **Compiler** (from `2519642`, `48003b1`, `85c0c6f` and `d063c3f`, final form):
  - `assert_wf_routing_closed_v0.py`, `assert_topology_contract_closed_v1.py` and
    `assert_topology_routing_complete_v1.py`;
  - `__init__` registrations, `s2_canonicalize.py` and `author_invariant_scope.py`;
  - `test_routing_closure.py` and `test_routing_lookup.py`.
- **Arming.** The compile now checks routing in every domain, so steps 4–6 must already route every
  outcome.
- **Checks:** D1, D2, D4.

### Step 8 — Runtime, trace and Collatz

**Platform part (change note).**
- **Artifacts.** `CONSTITUTION_TRACE_EXECUTION_V1` and `SCHEMA_TRACE_EVENT_V2.json`. The trace
  constitution V0 gains `superseded_by` only.
- **Runtime.** All six dev/18 commits, final form:
  - `dispatcher`, `scheduler`, `memory`, `ct_executor`, `ct_execute`, `conformance`, `evidence`,
    `api` and `examine/`, plus the README and architecture notes;
  - their tests, including `test_step_outcome`, `test_no_default` and `test_unknown_continuation`.
- **Inspector:** the v2 trace fixtures (`2fe44df`).
- **Transport:** the egress refuses an absent field (`52c67dd`).
- **CLM:** the choose atom reads `ground_numbers` with `.get`.
- **.github:** `trace_schema_conformance.py` reads V2.

**Collatz dossier.** This replaces `cr_01_termination_gate`.
- **Artifact.** `CC_VERIFY_TERMINATION_V1`; the V0 gains `superseded_by`.
- **Re-point.** `WF_COLLATZ_CONJECTURE_V0`.
- **Test.** `test_reference_collatz`, including the case where the gate fails.

**Pinned red by design:** `blockchain_identity` at 21/22, because the TE output fields are parked.

**Checks:** D1–D4.

### Step 9 — Map, standard and release notes

- **`standards` `work/v1`:**
  - the realization map entries for RT-6, ID-5, EX-18, CP-13 and SU-11;
  - the publication rule, recorded in `revisions.md`.
- **Release notes** for the cycle.
- **Check:** D5.

### Step 10 — SoSyM evidence re-run

- `omission.sh` O3 and `outcome_survey.py` run on dev/18r. Keep the outputs.

### Step 11 — Merge-ready

- D1–D5 pass, and the SOTU is updated.
- You run the squash merges.

## 5. What dev/18r does not do

- **No cleanup step.** No identity is created and then stood down before release.
- **No sweep.** The published-identity check runs at every step from step 3 on.
- **No platform dossiers.** Each platform change is a change note.

## 6. Parked

None of these makes a done-check fail. They go to the next cycle as one file.

- **Optional TE output fields.** `TE_ACCEPT_ACTOR_V0` owes `grounds`, which leaves
  `blockchain_identity` red at 21/22.
- **Design language gaps:**
  - it has no family for a constitution or an invariant, so governance artifacts are written by hand
    and cited as REVIEW;
  - P7 assumes `{domain}.implementation`;
  - P7 also refuses with `TRANSFORM_WITHOUT_VECTOR` and `DISCHARGE_NOT_IN_TOPOLOGY`.
- **Workloads cannot hold test data.**
- **Construction reads 0 of 0 facts as 0%** (`--require 0`).
- **A domain build keeps no record of which checks ran.**
- **Short-code references:** workflow `code` and `start_node`, and RB binding keys.
- **RT-6 stays Partial** for the outcome-namespace fallback (finding 31).
- **`CC_ENFORCE_LICENSE_CAP_V0`.** It is published in v5 and nothing runs it. It stays as published;
  removing a published identity needs a rule for it first.

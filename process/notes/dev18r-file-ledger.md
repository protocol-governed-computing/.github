# dev/18 → dev/18r — what each changed file becomes

Measured with `git diff --name-status <bump>` and `git ls-files --others` in each repo, where `<bump>`
is the "VERSION bump to 18" commit. dev/18 adds 157 files, deletes 2, and modifies 103. `standards` and
`snapshot_assembler` have no dev/18 change.

dev/18r starts from the bump commit, so **nothing has to be deleted from it**: a file dev/18 added
simply never exists there unless the replay creates it. The tables below say which ones it creates.

---

## 1. Gone — never created in dev/18r

They stay only in the dev/18 branch, as history.

### Dossiers (11 directories, about 130 files)

| Repo | Dossier | Why it goes |
|---|---|---|
| software_governance | `dossiers/routing_closure/` | Platform changes become change notes |
| software_governance | `dossiers/identity_semantics/` | The reference declaration is authored once |
| software_governance | `dossiers/reference_semantics/` | Same |
| software_governance | `dossiers/routing_lookup/` | Platform changes become change notes |
| software_governance | `dossiers/published_rules/` | Nothing published is edited, so nothing needs restoring |
| business_domains | `blockchain/cr_dossiers/cr_06_routing_closure/` | Replaced by one dossier authoring the V1s |
| business_domains | `blockchain/cr_dossiers/cr_07_published_identities/` (untracked) | The re-cut does not exist |
| business_domains | `ai_governance/cr_dossiers/cr_02_reclaim_closure/` | Replaced by one ai_governance dossier |
| business_domains | `ai_governance/cr_dossiers/cr_03_parameter_result/` | Same |
| transformation | `dossiers/routing_closure/`, `dossiers/semantic_change/` | Replaced by one transformation dossier |
| conformance_workloads | `workloads/collatz/cr_dossiers/cr_01_termination_gate/` | Replaced by one Collatz dossier |

dev/18r writes its own dossiers: one per domain that changes (blockchain, ai_governance,
transformation, Collatz).

### Registry artifacts (1)

| Repo | Artifact | Why it goes |
|---|---|---|
| software_governance | `artifact::VOCAB_DECLARATION_REPRESENTATION_V1` | The declaration is authored once, as V0, with V1's content |

### In-place edits to v5 artifacts (51 files)

Every registry file dev/18 modified keeps its v5 text in dev/18r. The only edits made to these files
are stand-down markings and deliberate re-points, and only where a successor exists:

- **software_governance (24).** Twenty `governed_by` re-points to the execution topology V1, and four
  rules edited in place: `CONSTITUTION_EXECUTION_TOPOLOGY_V0`, `INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V0`,
  `INVARIANT_TOPOLOGY_ROUTING_COMPLETE_V0`, `CONSTITUTION_TRACE_EXECUTION_V0`. In dev/18r the twenty
  are re-pointed once, and the four only gain `superseded_by`.
- **business_domains (13).** Blockchain's 8 and ai_governance's reclaim contract are not edited; their
  V1s are new files. `CC_VALIDATE_TOOL_PARAMETERS_V0` gains `superseded_by`. `WF_GOVERN_AGENT_ACTION_V0`
  is re-pointed once. `VOCAB_AI_LICENSING_STATES_V0` and `WF_PROVISION_AI_LICENSING_V0` lose the prose
  naming the deleted cap contract.
- **transformation (12).** The judge contracts and phase workflows are not edited; their V1s are new
  files. `IN_DESIGN_INTENT_SUBMITTED_V0` is re-pointed once.
- **conformance_workloads (2).** `CC_VERIFY_TERMINATION_V0` gains `superseded_by`;
  `WF_COLLATZ_CONJECTURE_V0` is re-pointed once.

### Notes (1)

`.github/process/notes/su11-recut-sweep.md` describes dev/18's drift and stays with it.

---

## 2. Carried — created again in dev/18r, final form only

### Registry artifacts (10)

| Repo | Artifact | How |
|---|---|---|
| software_governance | `artifact::VOCAB_DECLARATION_REPRESENTATION_V0` | V1's content, under V0 |
| software_governance | `execution_topology::CONSTITUTION_EXECUTION_TOPOLOGY_V1` | Final form, naming both new invariants and the WF routing rule |
| software_governance | `execution_topology::INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V1` | As is |
| software_governance | `execution_topology::INVARIANT_TOPOLOGY_ROUTING_COMPLETE_V1` | As is |
| software_governance | `trace::CONSTITUTION_TRACE_EXECUTION_V1` | As is |
| software_governance | `workflow::INVARIANT_WF_ROUTING_CLOSED_V0` | Governed by the topology V1 from the start |
| software_governance | `schema/SCHEMA_TRACE_EVENT_V2.json` | As is |
| business_domains | `ai_governance::CC_VALIDATE_TOOL_PARAMETERS_V1` | As is |
| transformation | `transformation::WF_P7_DESIGN_INTENT_ADMISSIBILITY_V1` | Carries B's rules and the NOT_FOUND route together |
| conformance_workloads | `workload::CC_VERIFY_TERMINATION_V1` | As is |

### Deletions (2)

| Repo | File | Why |
|---|---|---|
| business_domains | `CC_ENFORCE_LICENSE_CAP_V0.md` | Unreachable; the same decision |
| transformation | `scripts/testbed/withdrawal_design_test.py` | Replaced by B's test |

### Code (about 60 files, by cherry-pick)

All runtime, inspector, transport and compiler code, and transformation's tooling, as they stand at
dev/18's head:

- **New modules:** `representation.py`, `sameness.py`, `assert_topology_contract_closed_v1.py`,
  `assert_topology_routing_complete_v1.py`, `assert_wf_routing_closed_v0.py`.
- **New tests:** `test_reference_semantics`, `test_routing_closure`, `test_routing_lookup`,
  `test_no_default`, `test_step_outcome`, `test_unknown_continuation`, `semantic_change_design_test`,
  and three `routing_closure` execution validations.

Two code changes go away because the edits they undo are never made:
`assert_topology_routing_complete_v0.py` is never touched, so it needs no restore; and the code naming
`VOCAB_DECLARATION_REPRESENTATION_V1` names V0.

---

## 3. New in dev/18r — not in dev/18

These are the successors dev/18 never wrote, because it edited in place:

| Repo | Artifacts |
|---|---|
| business_domains | 8 blockchain V1s (4 contracts, 4 workflows); `CC_RECLAIM_UNUSED_LICENSE_V1` |
| transformation | `CC_JUDGE_AGAINST_SNAPSHOT_V1`, `CC_JUDGE_AGAINST_COMPOSITION_V1`; phase workflows P2–P6 and P8 as V1 |

Plus one change note per platform change, and one dossier per changed domain.

---

## 4. Net effect

| | dev/18 | dev/18r |
|---|---|---|
| Dossier directories | 11 (+1 untracked) | 4 |
| New registry artifacts | 11 | 27 |
| Published artifacts edited beyond stand-down or re-point | 18, then restored or left as breaches | 0 |
| Unpublished versions stood down before release | 1 (`VOCAB` V0) | 0 |
| Pinned red-by-design construction differences | 2 (book_library) | 2 (book_library, sealed in v5 either way) |

---

## 5. What stays on disk after switching branches

Switching a repo to dev/18r removes every tracked file dev/18 added. These do not move with a
branch, and are cleared by hand once dev/18 is archived:

- untracked work: `blockchain/cr_dossiers/cr_07_published_identities/` (commit it to dev/18 first, or
  delete it);
- build output, all gitignored: `snapshot/` and `data/` at the root, each domain's `snapshot/` or
  `snapshot_mw/`, `traces/`, `__pycache__/`; a clean rebuild regenerates them.

In git, dev/18's history stays on the `dev/18` branch only. A squash-merge of dev/18r into `main`
carries none of it.

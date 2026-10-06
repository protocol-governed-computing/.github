# SU-11 re-cut sweep — dev/18 against v5

Measured on the working snapshot after `routing_lookup`, against `pgc_release/snapshot` (v5).

## Method

- **Lens 1, declarations.** Every identity present in both, compared by `sameness.differences` under
  `artifact::VOCAB_DECLARATION_REPRESENTATION_V1`, with each stood-down artifact's one successor
  excused as a re-point.
- **Lens 2, published text.** Every identity whose canonical text differs once supersession markings
  and re-points are set aside.
- **Lens 3, realization.** Compiler handlers, transform implementations and design checks changed
  since the `v5` tag.
- **Scope rule.** Identity is fixed at publication. Only identities published in v5 whose meaning
  changed in dev/18 are breaches. An identity added in dev/18 is unpublished and may change or be
  withdrawn before release.

v5 holds 500 identities, the working snapshot 507: 499 shared, 8 added, 1 removed (the unreachable
licence cap contract, deleted by hand).

## Out of scope

- **The three withdrawal designs.** Blockchain `cr_05`, book_library_mgmt `cr_05` and CLM `cr_02` were
  all delivered before v5. What v5 published is what those identities mean.
- **The 23 re-points of this cycle.** Each moves only a reference to a declared successor, which keeps
  identity by rule.
- **Explanation-only text.** The licence cap prose trims; the generator-source line added to
  `WF_P0_…` and `WF_P1_…`.
- **Realization of an unchanged rule.** `assert_fqdn_only_references_v0` and
  `assert_superseded_not_referenced_v0` read the reference declaration; their invariants' text is
  unchanged. CLM's `ct_pure_choose_permitted_token_v0` reads an absent field as false, as before.

## Breaches — published identities whose meaning changed in dev/18

| # | Identity | Changed | Referrers | Origin |
|---|---|---|---|---|
| 1 | `blockchain::CC_RESOLVE_ACTOR_V0` | BACKEND_ERROR surfaced, routed, allowed | 4 | `cr_06_routing_closure` |
| 2 | `blockchain::CC_CLAIM_WALLET_IDENTITY_V0` | same | 1 | same |
| 3 | `blockchain::CC_CREATE_WALLET_RECORD_V0` | BACKEND_ERROR surfaced, routed | 1 | same |
| 4 | `blockchain::CC_APPEND_WALLET_OCCURRENCE_V0` | same | 1 | same |
| 5 | `blockchain::WF_REGISTER_ACTOR_V0` | BACKEND_ERROR routes | 1 | same |
| 6 | `blockchain::WF_ACCEPT_ACTOR_V0` | same | 1 | same |
| 7 | `blockchain::WF_REJECT_ACTOR_V0` | same | 1 | same |
| 8 | `blockchain::WF_CREATE_WALLET_V0` | same | 0 | same |
| 9 | `ai_governance::CC_RECLAIM_UNUSED_LICENSE_V0` | VIOLATION surfaced and routed; store named | 1 | `cr_02_reclaim_closure` |
| 10 | `transformation::CC_JUDGE_AGAINST_SNAPSHOT_V0` | NOT_FOUND surfaced, routed | 7 | the generator, `routing_closure` |
| 11 | `transformation::CC_JUDGE_AGAINST_COMPOSITION_V0` | same | 1 | same |
| 12–17 | `transformation::WF_P2…P6, P8_…_V0` | NOT_FOUND routes | 2 each | same |
| 18 | `transformation::WF_P7_DESIGN_INTENT_ADMISSIBILITY_V0` | NOT_FOUND route; stood down by V1 | 0 | same |
| 19 | `workflow::CONSTITUTION_WORKFLOW_V0` | names `INVARIANT_WF_ROUTING_CLOSED_V0` | 42, in 7 domains | `routing_closure` |
| 20 | `execution_topology::INVARIANT_TOPOLOGY_ROUTING_COMPLETE_V0` | rule text and check widened (CP-13) | 2 | `routing_closure` |
| 21 | `execution_topology::CONSTITUTION_EXECUTION_TOPOLOGY_V0` | routing constraint restated (CP-13); stood down by V1 | 1 | `routing_closure` |
| 22 | `trace::CONSTITUTION_TRACE_EXECUTION_V0` | names `SCHEMA_TRACE_EVENT_V2` | 0 | trace schema v2 |
| 23–24 | `book_library_mgmt::IN_/WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V1` | `version` v0 → v1 | 1, 0 | renderer fix |

## Cleanup candidates (item 6)

Added in dev/18 and already stood down: `artifact::VOCAB_DECLARATION_REPRESENTATION_V0`.

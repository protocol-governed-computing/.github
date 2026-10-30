# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-29 · Route frozen, docs cleaned; dev/19 is cut-ready

### Changes Made
Work is on `dev/19`. The session's work is committed in `transformation_compilers` `59902f3`,
`software_governance` `5aaee8c`, `protocol_runtime` `2e494d7` and `.github` `8c88fbc`. Uncommitted
in `.github` only:
- `external_validation_nova/` (59 files) — deleted. The study is closed; the standard's revisions cite
  its results, and published tags keep it.
- `doc/PLAN_TYPED_REFERENCES_GENESIS.md` — deleted; the plan is done.
- `doc/FINDINGS_DESIGN_REDUNDANCY.md` — deleted; shelved, and the result is in memory.
- `process/RUNBOOK.md` — the row naming the missing `test_trace_path.py` now names only
  `test_node_keyed_routing.py`.
- `profile/README.md` — the public link to the standard's revisions now points to
  `standards/blob/main/revisions.md`.
- `doc/SOTU.md` — this file.

**What the session delivered, all committed:**
- **P3 revision 2:** a change may reuse its own domain's artifacts (`own_domain`).
- **The complete-at-P6 ruling** is in `lifecycle::CONSTITUTION_CHANGE_MGMT_V0`, under the dossier
  `software_governance/dossiers/complete_at_governance_intent/`.
- **The seed declares delivery** (P0 revision 2, optional register).
  - An authored change ends at P6, and its verdict reads `Complete at P6`.
  - P7 revision 6 refuses it (`AUTHORED_CHANGE_HAS_DESIGN`), realising
    `lifecycle::INVARIANT_AUTHORED_CHANGE_HAS_NO_DESIGN_V0`.
  - The design language honours a register schema's `required` list.
- **The derive route is frozen:** defect fixes only.
  - `repoint_callers` is removed. A replay over the nine real deliveries showed it would have refused
    3 of 9 on false positives, and rewritten pinned fixtures.
  - Callers outside a domain are repointed by hand.
- **Broken doc references fixed** in `software_governance`, `protocol_runtime` and
  `transformation_compilers`.

### Build & Test Status
- `regression.sh --all` (2026-10-29, working tree): **PASSED, 99/99 steps as expected.**
- `release.sh --check` (run earlier this session, before the doc edits): PREFLIGHT PASSED.
  - All 10 repos are on `dev/19`, with no tag collisions.
  - A clean rebuild and composition conformance passed (603 artifacts).

### Open Issues
- **Kept pending the user's call:**
  - `.github/doc/AGENT_ARCHITECTURE_COMPARISON.md`, `BEHAVIOR_OUTSIDE_SNAPSHOT.md` and
    `DOMAIN_BEHAVIOR_OUTSIDE_SNAPSHOT.md` (keep if the Inversion paper v2 is live);
  - `.github/doc/DECISION_ACCOUNTING_DESIGN.md`;
  - `business_domains/causal_language_model/doc/cr_sequence.md`.
- **The derive route's future:** keep it frozen while work through a ledger (decision accounting) is on
  the roadmap; otherwise retire it and keep the delivered changes (`transformation_compilers/CLAUDE.md`,
  "The derive route is frozen").
- **Parked while the route is frozen:**
  - the seal requiring `AUTHORED`;
  - mandatory `delivery`, which would need a `REGISTER_SCHEMA_P0_V1`;
  - derived seeds declaring `CONSTRUCTED`.
- **Before any publish, not a cut:**
  - **the frozen e2e baseline needs `business_domains` `36bc62a`.** A fresh clone of the published
    `main` lacks it (`transformation_compilers/scripts/testbed/e2e_phases_test.py:796`). Vendor the
    frozen sources first.
  - the blockchain web client has not been opened in a browser since its repointing;
  - the ledger prose in blockchain and ai_governance is not owner-confirmed.
- **Gaps in rules that nothing enforces**, none with current exposure:
  - overlapping in-flight dossiers (`transformation_compilers/CLAUDE.md:372`);
  - validation criteria drawn from P0 on the authored path (`CLAUDE.md:271`);
  - governing generation (`.github/process/rulings.md:53`).

### Architectural Concerns
- **"Caller" is not defined anywhere.** It should mean a file judged against the live composition;
  files judged against a pin are history. Only a failing regression enforces this today.
- **Optional registers are now a language feature.** Keep it for declarations whose absence has a
  stated meaning, as `delivery` has: "judged as before".
- **The constitution was edited in place on V0**, prose and one rule line. This follows the precedent
  of `8801cc8`.

### Next Session Should Start With
1. Commit `.github`:
   `cd .github && git add -A doc external_validation_nova process profile && git commit -m "docs cleanup: NOVA study, done plan and shelved finding removed; broken references fixed"`
2. Decide the kept docs and the derive route's future against the roadmap. The code needs no work
   before a cut (`bash .github/process/release.sh`, local only).

**Priorities (the user):** fix platform defects and decision gaps first. Keep business-domain
parking-lot items on hold unless the new compiler needs one to be assimilated fully and tested.

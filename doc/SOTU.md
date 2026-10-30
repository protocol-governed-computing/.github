# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-29 · The seed declares where a change ends; an authored change is complete at P6

### Changes made
Work is on `dev/19`. The last commits are `transformation_compilers` `c614abc`, `software_governance`
`8801cc8` and `.github` `048a5fa`. Everything below is uncommitted. It includes the previous sweep's
complete-at-P6 clause, which this sweep extends.

**The root cause.** Where a change ends was doctrine, not data. The phase catalog was one straight
line from P0 to P8, and no dossier said it ends at P6. So every admissible P6 printed "Ready for P7".

**`transformation_compilers`**
- **The design language:** a register the schema's `required` list leaves out may be absent
  (`design/schema.py` `Register.mandatory`; `design/expand.py` emits `REGISTER_MISSING` only for a
  mandatory register). Every register before this one is required, so no rule set changed by it.
- **P0 revision 2** (`REGISTER_SCHEMA_P0_V0.json`, template §20): an optional `delivery` register of
  one row, `mode` `AUTHORED` or `CONSTRUCTED` (vocabulary group `delivery_mode`), with
  `DELIVERY_NOT_SINGULAR` holding it to one row. A seed without it is judged as before.
- **P7 revision 6:** `AUTHORED_CHANGE_HAS_DESIGN`, the procedure
  `evaluate/procedures/authored_change_has_no_design.py`, reading the seed. It realises
  `lifecycle::INVARIANT_AUTHORED_CHANGE_HAS_NO_DESIGN_V0`.
- **P1–P6 revisions** (P3 to 3, the rest to 2): each phase's citation rule lists every register a
  citation may name, and the seed now has one more. Each widens and refuses nothing.
- **The verdict:** `design/catalog.py` `next_phase(phase, delivery)` ends an authored change at P6.
  `cli.py` reads the seed's delivery: an authored P6 prints `Complete at P6`, and other P6 verdicts
  print `Ready for P7`, saying so when the seed declares no delivery or was not supplied. `--json`
  carries `delivery` and `next_phase`.
- All nine phase workflows resealed by `tc phase emit`. The transformation design of record was
  regenerated.
- `scripts/testbed/delivery_declared_test.py` (new, 5/5):
  - an authored seed makes P6 complete;
  - a constructed or silent seed goes on to P7;
  - two delivery rows are refused;
  - P7 refuses an authored change, and only it.
- Docs:
  - DESIGN_LANGUAGE §7.1 "Where a change ends", a §6.1 row, and §9.5 (a route dossier declares
    `AUTHORED`);
  - THE_SHAPE_OF_A_CHANGE §5 cites the constitution.

**`software_governance`**
- `registry/lifecycle/invariants/INVARIANT_AUTHORED_CHANGE_HAS_NO_DESIGN_V0.md` (new). The
  constitution names it in its rules.
- `CONSTITUTION_CHANGE_MGMT_V0.md`, prose:
  - §2: an authored change is reviewed as a body at P6;
  - §3: "An authored change is complete at P6", and its seed declares it authored.
- `dossiers/complete_at_governance_intent/`: re-authored as the child it is, because the invariant
  falls under the constitution this in-flight dossier extends. It gains outcome 4, gap 3, an
  AUTHOR_NEW decision and the ownership row. Its out-of-scope item now hands the rule and the seed
  declaration to the transformation repository.
  - It was re-judged against its exact pin (`4c065cf2…`), reproduced from `git archive HEAD` of
    `software_governance` and `transformation_compilers`. All seven are admissible.
  - Its seed declares no delivery: its pinned P0 rule set predates the register.
- The platform recompiled. Every domain was recompiled against it, and the snapshot was reassembled
  (603 artifacts).

**`.github`**
- `process/regression.sh`, `expectations.yaml` and `RUNBOOK.md`: `delivery_declared_test`.
- `doc/SOTU.md`: this file.

### Build & test status
- `regression.sh --all` (2026-10-29, working tree): **PASSED, 100/100 steps as expected.** The first run missed two counts the change
  moves on purpose: human block fidelity 588 → 589 artifacts (the invariant), and P7 284 → 285 rules
  (the refusal). Both are updated in `expectations.yaml`.
- `tc phase meta`: CONSISTENT, 1001 rules across 9 phases, 58 check kinds. `emit --check` OK.
  `write_baseline_designs --check` 6/6. Implementation closure passed.

### Open issues
Parked on dev/19, none blocking: the first three below. Each changes a record's wording, not an
outcome — a route seal never runs P7, and P7 cannot design a constitution or an invariant anyway.

- **`delivery` is optional.** A seed that declares nothing reads as today, Ready for P7. Making it
  mandatory is retroactive: a new `$id`, `REGISTER_SCHEMA_P0_V1`, with fixtures and payloads updated
  and V0 approvals unconfirmed. It is the user's call.
- **The derive-route seal does not yet require `AUTHORED`.** `derive/` is sealed, so that
  requirement is a route change with its own dossier. The derive route's projected business seeds
  could declare `CONSTRUCTED` in the same change.
- **The two delivered route dossiers and this governance dossier declare no delivery.** Their pinned
  rule sets predate the register, and delivered dossiers are never edited.
- **The constitution is edited in place on V0, prose and one rule line.** This follows the precedent
  of `8801cc8`.
- **The frozen corpus pin** `36bc62a` must survive any squash or published cut.
- **Caller repointing has not run on a real delivery.**
- **The blockchain web client was not opened in a browser** after its repointing.
- **The prose in the blockchain and ai_governance ledgers is not owner-confirmed.**

### Architectural concerns
- Optional registers are now a language feature. A register left out of `required` is judged only
  where it is present, so it can be skipped silently. Keep it for declarations whose absence has a
  meaning stated in the language: for `delivery`, "judged as before".

### Next session should start with
1. Commit (the user's step):
   ```
   cd software_governance && git add dossiers registry/lifecycle && git commit -m "lifecycle: an authored change is complete at P6 and has no design intent, under its own dossier"
   cd ../transformation_compilers && git add THE_SHAPE_OF_A_CHANGE_V0.md design doc registry scripts transformation && git commit -m "the seed declares delivery; an authored change ends at P6 and P7 refuses it; optional registers"
   cd ../.github && git add doc/SOTU.md process && git commit -m "regression: delivery declared test"
   ```
2. Next: the derive-route seal requires `AUTHORED`, as a route change with its own dossier. Or
   decide whether `delivery` becomes mandatory.

**Priorities (the user):** fix platform defects and decision gaps first. Keep business-domain
parking-lot items on hold unless the new compiler needs one to be assimilated fully and tested.

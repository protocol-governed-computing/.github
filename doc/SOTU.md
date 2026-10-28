# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-28 · Decision compiler: block composer, closed ledger, moved into `transformation/decision`; readiness 1, 2 and 4 done but for two gaps

### Changes made
Work is on `dev/19`. The user committed `transformation_compilers` `7b8a334`, `8512527` and
`2a400d2`, and `.github` `9d2674b`. **`2a400d2` is incomplete:** it holds the new
`transformation/decision/` and `scripts/decision_build.sh` only. Uncommitted:
`transformation/cli.py` (registers `tc decision`), `pyproject.toml` (`jsonschema`),
`scripts/decision_suite.py`, and the prototype's moved and edited files. A clean checkout of HEAD
has no `tc decision`, so the regression's `decision_*` steps fail there.

**`transformation_compilers`**
- `transformation/decision/base.py` — the composer's shared base (was `engine/generate_domain.py`):
  several actors, a node key that `runs` another CC, `_ends` emits, and only invoked transforms
  carried. Reads a design with `machine_block`.
- `transformation/decision/compose.py` — the block composer (was `engine/compose.py`). It adds
  named `checks` with denial nodes for `on_refusal`, a fixed identity, `sets`/`holds`, a
  `when`/`otherwise` condition, `releases`, ids from several fields, trails scoped to the part, and
  `replaces`. `derive()` refuses an unsealed rule set or a refused ledger.
- `transformation/decision/ledger.py` — the shape check, references and self-test (was
  `engine/check_ledger.py`).
- `transformation/decision/splice.py` — the splice, `OWNER` and identity rows (EXTEND, REPLACE,
  `supersedes`).
- `transformation/decision/identity.py` (new) — decides each artifact's identity by `sameness`
  against the pinned composition. It gives a changed artifact the next unused version, and
  renumbers the derived rows.
- `transformation/decision/seal.py` (new) — `$id`, `x-revisions` and digests for the doctrine, the
  schema and the catalog; `judged_by`; the doctrine closure.
- `transformation/decision/cli.py` (new) — `tc decision check|meta|selftest|derive|identities|splice|revise`.
- `transformation/decision/doctrine.yaml` (rev 2) — each rule cites `realizes`, or `none` with a reason.
- `transformation/decision/catalog.yaml` (rev 2) — 31 questions.
- `transformation/decision/ledger_schema.yaml` (rev 2) — the closed ledger shape, with an
  `x-question` per answer.
- `transformation/cli.py` — `main.add_command(decision)`.
- `pyproject.toml` — the `jsonschema` dependency.
- `scripts/decision_build.sh` (was `engine/run_pipeline.sh`) — runs derive → identities → splice
  → construction check → emit `--snapshot` → retirement record → compile → assemble → suites.
- `scripts/decision_suite.py` (new) — runs a domain suite, dispatching each workflow's declared
  successor.
- `decision_authoring_prototype/engine/{census,compare,p7_slice}.py` — analysis only; they import
  from `transformation.decision`.
- `decision_authoring_prototype/domains/ai_governance/ledger.yaml` — the whole domain in closed
  shape, with `replaces` answers.
- `decision_authoring_prototype/domains/ai_governance/FINDINGS_COMPOSER_RUN.md` (new) — derives
  with no new block. The run passed 17/21, and 21/21 with the cap count stood in.
- `decision_authoring_prototype/domains/*/generated.json` — rederived, with `_judged_by` and `_identity`.
- `decision_authoring_prototype/doc/ASSIMILATION_READINESS.md`, `BUILDING_BLOCKS.md` and
  `LEDGER_FORMAT_V0.md` — the readiness status, the "as built" section, and the catalog for the
  third domain plus the closed ledger.

**`.github`** (committed `9d2674b`)
- `process/regression.sh` — steps `decision_ledgers`, `decision_meta`, `decision_selftest` and
  `decision_<domain>`.
- `process/expectations.yaml` — rows for those steps. `decision_ai_governance` is red by design.
- `process/RUNBOOK.md` — two rows in "Expected".

### Build & test status
- `regression.sh --all` (2026-10-28, working tree): **PASSED, 87/87 steps as expected.**
  `decision_ai_governance` is RED BY DESIGN, as declared.
- **Decision builds** (in that run):
  - **book:** kept 23, superseded 18, new 16, retired 10. Construction is at 100% and emit is
    accepted by construction's meaning check. The suites pass 23/23 and 27/27.
  - **blockchain:** kept 13, superseded 9, new 22, retired 16. Construction is at 100%. The suites
    pass 26/26, 6/6 and 12/12; the owner checks pass 8/9 (empty list, a parked platform gap).
  - **ai_governance:** construction is at 100%, but construction refuses the identities (see
    open issues).
- `tc decision meta`: PASSED. 3 of 9 doctrine rules cite an invariant.
- `tc decision selftest`: 16/16 answers outside their shapes are refused.

### Open issues
- **Commit gap:** see "Changes made". The user still has to commit the remaining
  `transformation_compilers` files.
- **ai_governance identities (readiness 2.5).** Construction refuses because three artifacts the
  ledger no longer derives still name artifacts it replaces: `CC_RECORD_GOVERNED_ACTION_V0`,
  `CC_RECORD_DENIED_ACTION_V0` and `RB_LICENSE_BINDINGS_V0`.
  - `replaces` names operations only, and no answer can name a component.
  - The design language's inventory has no retirement without a successor: REPLACE requires
    `superseded by`.
  - The fix is a design-language and construction change, made in its own dossier.
- **Doctrine citations (readiness 2.4, partial):** order, storage, interface, reuse, own_values and
  rules_held realize no platform invariant. They are stated with the standard text (3.3–3.6).
- **Platform gaps, parked:**
  - `CT_PURE_FILTER_RECORDS_V0` refuses an empty answer (plan in git history);
  - the registry declares no COUNT, so the license cap is unrealized.
- **The composer:**
  - `change_identity` is still fitted;
  - the RB name is not carried, which is why `RB_LICENSE_BINDINGS_V0` is retired;
  - ai_governance's entrance is renamed (`IN_AGENT_ACTION_REQUESTED_V0` → `IN_GOVERN_AGENT_ACTION_V0`);
  - `request_identity` is formed and never recorded.
- **The closed ledger** has no `open: true` and no cases.
- **Readiness 4.4:** book's suites predate the method. That stays a stated limit.
- **Defects in today's designs** (book, blockchain, ai_governance), parked as before, are in git
  history.

### Architectural concerns
- **Identity by meaning versions most workflows.** A derived design changes how operations are
  composed, so book supersedes 18 and blockchain 9. Callers that dispatch by workflow identity
  must follow `supersedes`. Today only the test harness does (`decision_suite.py`).
- **The sealed documents live in the package**, not in a compiled artifact. Phase rule sets are
  sealed into their workflows; the doctrine is not.
- **`tc` now imports `transformation.decision` at start-up**, which pulls in `inspector` and
  `jsonschema`. The decision compiler ships in `pgc-transformation`.
- **The carried-surface rule** is still a prototype rule (readiness 3.5). Store matching is
  heuristic, and RB names are not carried.
- **The ledgers and checks stay in `decision_authoring_prototype/domains/`.** Behavior reaches the
  domains only as numbered change requests (5.2).

### Next session should start with
Commit the rest of `transformation_compilers`, then confirm `tc decision --help` works from the
committed tree:
```
cd transformation_compilers
git add transformation/cli.py pyproject.toml scripts/decision_suite.py decision_authoring_prototype
git commit -m "decision compiler: register tc decision, jsonschema dependency, suite harness, prototype moved"
```
**Priorities (the user, 2026-10-28):** after the normalization, fix platform defects and
decision-related gaps first. Keep business-domain parking-lot items on hold unless the new compiler
needs one to be assimilated fully and tested. In order:
1. Platform: the design language's retirement without a successor (unblocks ai_governance, 2.5).
   Then `CT_PURE_SELECT_RECORDS_V0` (empty answer) and a declared registry COUNT (license cap).
2. Decision gaps: carry RB names, carry entrance names, record `request_identity`, generalize
   `change_identity`, add `open`/cases to the closed ledger, and doctrine invariants (2.4).
3. On hold: the parked defects in book, blockchain and ai_governance's today-designs, and the
   owner rulings (tier names, reclaim "still active").

# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-26 · behavior outside the snapshot analysed, platform and domains; decision accounting designed

### This session
No code changed in any repository. The session produced three documents in `.github/doc/`. All
three are new and uncommitted. The 2026-10-24 handoff below is also uncommitted, so it is kept here
rather than left to git history.

**1. Platform: behavior outside the snapshot** (`doc/BEHAVIOR_OUTSIDE_SNAPSHOT.md`)
- This report covers `protocol_runtime`, `protocol_transport`, and the side effects in
  `software_governance`.
- It finds 12 oversights (A1–A12), where code holds a fact the snapshot could carry. The main ones:
  - A workflow ends with the last contract's status. The sealed EXIT carries no outcome, and
    `cli.py:196` hard-codes `("SUCCESS","ALREADY_EXISTS")`.
  - `dispatcher.py:274–282` merges undeclared inputs into the surface.
  - Two admission validators disagree: `scheduler._admit` and the transport `_validate_input`.
  - `length_minus_one` is a Collatz-only operator inside the domain-neutral resolver.
  - In `CS_MUTABLE_JSON_V0`, an absent `filter` updates every record.
- It finds 6 bounded necessities (B1–B6): the environment, kernel semantics, the class name that
  signals a refusal, capability realization, the bootstrap, and authority. On authority, the actor
  is sealed but not enforced, because the canonical request carries no principal.

**2. Business domains: behavior outside the snapshot** (`doc/DOMAIN_BEHAVIOR_OUTSIDE_SNAPSHOT.md`)
- **Policy from the caller:** ai_governance takes `cap` and `threshold_days` from the payload, so
  the caller sets the rule that judges it.
- **Facts from the caller:** `assigned_count`, `training_completed`, `last_active_date` and
  `evaluation_date` all come from the payload.
- **Evidence from the caller:** the reclaim audit records `days_inactive` from the payload. It does
  not record the transform's result.
- **False declarations:** 8 atoms declare `refusal: never`, and all 8 raise.
- **Smaller findings:**
  - `MAX_KEY_LENGTH = 256` is copied from the CS config into three atoms.
  - A literal kinds list duplicates `VOCAB_KIND_OF_INFORMATION_V0`.
  - Identity normalization is undeclared.
  - The hosted-record outcomes are hard-coded in `CT_PURE_READ_HOSTED_STATE_V0`.
- **Not ours to move:** Keccak, the choose algorithm, time-in-service as governed data (its
  authority is not enforced), and the host's prompt rendering.

**3. Decision accounting design** (`doc/DECISION_ACCOUNTING_DESIGN.md`)
- The first draft was a provenance map with one leak-specific invariant. It was revised after an
  expert critique, which asked for three separate obligations and for completeness as the central
  requirement.
- **Three obligations:**
  - provenance;
  - authority conformance;
  - evidence integrity.
- **Four ways a dependency is established:** `static`, `declared`, `observed`, `unknown`. None of
  them is called "verified".
- **New declarations:**
  - an input `role` (`policy`, `fact` or `subject`);
  - sealed constants for each atom, checked by a syntax-tree scan;
  - an admissibility table of role × source, with overrides the map shows;
  - `records:` on evidence fields.
- **Outputs:**
  - a sealed Decision Authority Map, `si.decision.map`;
  - three `FAIL_IMMEDIATELY` invariants under `decision_accounting::CONSTITUTION_DECISION_ACCOUNTING_V0`;
  - a mutation suite with 9 classes, 3 of them expected to pass undetected as the stated limits.
- **Claim boundary (§11):** the invariants are enforced within a stated scope. They are not a
  guarantee that hidden logic is eliminated.
- **Correction to the expert:** completeness at the composition boundary already holds by
  construction. The unknowns are inside atoms and side effects, plus atom purity, which is declared
  but not checked.

**4. Other**
- The two reports disappeared from `doc/` mid-session. The cause is not known; I neither moved nor
  deleted them. They were regenerated from the session text.
- I recommended against a general-purpose PGC agent. The suggestion is one read-only closure
  auditor agent, with procedures kept as skills. It was not built.

### Build & test status
- `regression.sh` (execution block) ran on 2026-10-26: **PASSED, 16/16 steps as expected**.
- The `--all` mode (rebuild plus every check) was not run. No code changed.

### Open issues
- Nothing is committed. Commit the three docs with the commands given in session, then
  `doc/SOTU.md` separately.
- The design is parked on dev/19. None of its declarations exist yet: `role`, `constants`,
  `admits`, `records:`, and the three invariants.
- The domain fixes are unscheduled. The ai_governance leaks are the top priority: `cap`,
  `threshold_days` and the audit's `days_inactive`.

### Architectural concerns
- **Where the rules live:** the design proposes a new `decision_accounting` concern. The alternative
  is to put the rules under `CONSTITUTION_EXECUTION_TOPOLOGY_V0`.
- **Atom purity:** the import rule in `business_domains/CLAUDE.md` is doctrine, and no check
  enforces it. `implementation_closure.py` checks only that each module exists.
- **Authority:** `governed_store` admissibility rests on actor binding, which the runtime does not
  enforce. B5 needs a principal on the Canonical Transport Request before the rule means anything.
- **The paper:** the expert's RQ1–3 suggestion bears on the inversion paper v2. Do not promote
  decision accounting to the paper's main claim until the mutation suite has results.

### Next session should start with
Decide whether decision accounting goes ahead on dev/19, and under which concern. If it does,
implement `INVARIANT_DECISION_SOURCE_ADMISSIBLE_V0` first, against the ai_governance `cap` and
`threshold_days` bindings, as the first mutation-suite case.

---

## SOTU Handoff — 2026-10-24 · Architecture Inversion paper rebuilt as a standalone problem-first draft; field manual aligned with dev/19

### This session
No code changed in any repository. The work was on papers and on documentation outside the workspace. The previous handoff (dev/19 items 1–12) is in git history.

**1. Field manual aligned with dev/19** (`omnibachi-site` `a0ccf3a`)
- `content/papers/foundations/pgc_field_manual_v1.md` was edited in place at your direction, so it now describes the dev/19 line, not v6. Where v6 differs, the text says so.
- It covers:
  - the sealed ontology and its agreement invariant;
  - 17 kinds, every one schema-governed;
  - the closed set of actor types;
  - names carried as data are references;
  - the genesis;
  - `INVARIANT_ADMISSION_COVERS_BINDINGS_V0`;
  - no pictures in the snapshot, only `graph.json`;
  - `si kind map --domain`, `si compile trace`, and the `?trace=` page;
  - 21 operations, 15 reads and 6 queries;
  - `author_transport_contracts.py` for adding an inspection operation.
- The Zenodo v1 deposit now differs further from the site.

**2. Architecture Inversion paper, v2 — the plan and two drafts**
- **Decisions:**
  - v2 is a new version of the preprint DOI `10.5281/zenodo.22736531`, not of the foundations paper.
  - The paper stands alone: no PGS/PGC naming history, and no citations to earlier papers in the series.
  - The paper shows 17 kinds. The registry's 21 entries include 4 compiler-bookkeeping entries.
  - The cost problem became the **complexity** problem.
- **First draft, kept but unmodified:** `omnibachi-site/parkinglot/pgc_architectural_inversion_v2.md`, with its outline beside it. `parkinglot/` is gitignored.
- **Working draft:** `omnibachi-site/doc/pgc_architectural_inversion_draft.md` (`34de0a5`), developed one section at a time. It now holds:
  - §1 the two problems. Problem 1 distinguishes *lifecycle-activity authorization* from *behavioral authorization*. It cites Hou et al. 2024 [1] and MacCormack & Sturtevant 2016 [2].
  - §2 the inversion defined. §2.1 uses the same terms as §1.1.
  - §3 the existing controls. Table 1 shows what each class of control authorizes, its scope, and what it does not establish by itself. Its references [3]–[16] were verified by web search. §3.3 gives criteria C1–C6. §3.4 states how PGC is to be compared, and that authorization is not correctness.
  - §4 the five properties. §4.1 states the C1 limit: a rule computed inside a capability is governed only by its contract and test vectors. Table 2 maps properties to criteria and is labelled as design claims.
  - §5 the baseline A1–A6, the derivation rule, Result 1 (execution preserves authority), and Result 2 (workers stay independent of authority). Result 2 is framed as the design answer to Problem 1.
- **Reviewer patches applied:** two rounds of expert comments. The main ones:
  - no "current practice" generalization;
  - possible failures are not presented as established ones;
  - the paper makes no superiority claim; that belongs to the parked comparative-evaluation paper.
- **Memory:** `inversion-paper-v2.md`.

**3. SOTU housekeeping:** the "field manual at the next cut" item is closed.

### Where things stand
v6 is published. dev/19 is declared a genesis, so nothing is measured against it until the cut.

- **Composition `v6`:** DOI `10.5281/zenodo.23485442`. Sealed snapshot
  `13e3c5bb502e2548389f5787caa9438247ee34f9d510ce6a8a3ed980fdf974d1`: 8 domains, 556 artifacts,
  `GOVERNANCE_SURFACE_PROFILE_V0`. `pgc_release/composition.json` names each component's version,
  commit and DOI.
- **PyPI:**
  - The nine components are at `6.0.0`.
  - `protocol-governed-computing` is at `6.0.1`. It pins those nine, and `pgc status` names composition v6.
- **Standard `v1`:** DOI `10.5281/zenodo.23486349` (concept `22150615`). It declares eight new
  obligations against `v0` (`standards/revisions.md`). The v6 reset reads as a genesis (`1b` §11),
  so it needed no spec change. Implementation repos link the concept DOI and cite `v1` in
  `.zenodo.json`.
- **Field manual:** `omnibachi-site/content/papers/foundations/pgc_field_manual_v1.md` now describes
  dev/19, edited in place (2026-10-22): sealed ontology, 17 schema-governed kinds, actor types, names
  as references, genesis, admission-covers-bindings, no pictures in the snapshot, kind map, compile
  trace, 21 operations. It notes where `v6` differs. The Zenodo v1 deposit differs from the site.
- **Git:**
  - Every repo is clean and pushed. Items 1–12 are on `dev/19`. `dev/19` and `main`
    exist locally and on the remote.
  - Every repo's `main` is one orphan commit, tagged `v6`. `pgc_install`'s `main` is `6.0.1`, and its `v6` tag stays on `6.0.0`.
  - Unsquashed history is in the local `history-18` tags.
  - Work happens on `dev/19`, where `VERSION` is 19.
- **Verified:**
  - `regression.sh --all` passes 81/81 on `dev/19` (2026-10-24, committed tree, 3m50s), with the demo script at 12/12 and trace-schema conformance over 167 traces.
    `test_reference_semantics` is 20/20, and `construction_mapping_test` states 186 fields. `test_inspector` is 173/173, and
    `human_block_fidelity` counts 552 artifacts. The working snapshot holds 545.
  - Rebuilds give one identity.
  - A clean `pipx` install runs the demo end to end, in the terminal and in the browser.
  - `README_DEV`'s tour and from-source path both work.

### How the next version is cut
- **One version per distribution (A2).** A repo whose tree changed since the last public tag
  bumps its own version, and `release.sh` refuses it otherwise. A repo that didn't change keeps its
  version.
- **New public identity.** One is issued only when what the composition determines changes, and
  only that mints DOIs.
- **Packaging fix.** One that doesn't change the composition bumps just that distribution,
  as `6.0.1` did. It gets a bare version tag; `v*` tags are for identities only.
- **The sequence:**
  1. `release.sh --check`
  2. Build wheels before `--publish`, because the compiler and assembler package `VERSION`.
  3. `release.sh --publish`
  4. twine
  5. `publish_component_releases.sh`, then `--verify`
  6. `release.sh --publish-composition`
  7. `pgc_install`: build, upload, then orphan `main`
- **The standard.** Each `.zenodo.json` "references" the version DOI of the standard revision the
  composition implements; standard `v1` is `10.5281/zenodo.23486349`. Move it when the standard
  moves. READMEs, `pyproject.toml` and `pgc status` link the concept DOI `22150615`, which always
  resolves to the latest revision.
- **Zenodo matching.** Component records are matched by concept DOI (`COMPONENT_CONCEPTS` in
  `compose_release.py`), not by title. The v6 transformation record is titled `(transformation)`,
  and Zenodo will not let it be edited.
- **At the cut, after sealing:** set `genesis: false` in `process/genesis.yaml` and move the
  `published_identity` expectation back to a comparison with the new identity.

### Open work
- **Unenforced admission in collatz.** `IN_COLLATZ_INPUT_VALIDATED_V0` keeps its rules as prose in
  `extensions.admission_rules`, which construction drops. The enforced bound is in
  `TI_COLLATZ_COMPUTE_V0` (`number`, 1–999999). TI and TE are outside the design language
  (`transport_bindings: []`).
- **Unenforced search rule in book_library_mgmt.** `WF_SEARCH_CATALOG_V0` says it excludes retired
  books. Only the summary says so: `CC_SEARCH_CATALOG_V0` binds the caller's `search_criteria`
  straight into the filter. Execution validation check 14 supplies `state: REGISTERED` itself, so
  it cannot fail. Fix as `cr_01`: a fixed `{state: REGISTERED}` filter step, `CC_`/`WF_SEARCH_CATALOG_V1`,
  and testbed payloads without `state`. Fold in a second gap: no match returns VIOLATION rather than
  an empty result. Same class as the collatz item. Source:
  `transformation_compilers/decision_authoring_prototype/domains/book_library_mgmt/FINDINGS_DECISION_LEDGER_CENSUS.md`.
  Two more, confirmed by a probe (`transformation_compilers/decision_authoring_prototype/domains/book_library_mgmt/FINDINGS_STEP4_COPY_FAMILY.md`):
  - A copy registration refused for an unknown book still claims its barcode, so the barcode is
    lost for good. The claim runs before the book check.
  - Retiring an already-retired copy succeeds and is trailed twice. No state precondition. The
    same holds for books.
  - A book refused for a duplicate barcode loses its identity for good: the book identity is
    claimed before the barcode. Confirmed by `transformation_compilers/decision_authoring_prototype/domains/book_library_mgmt/probes/probe_catalog.py`.
  - Updates refuse any change to title, author or year. cr_01 P0 §3 allows it, refused only on a
    duplicate; the narrowing entered at P7 and no rule caught it. The owner kept P0's rule.
  A ledger-derived design that fixes all of them passes construction and both validations:
  `transformation_compilers/decision_authoring_prototype/domains/book_library_mgmt/FINDINGS_STEP5_WHOLE_DOMAIN.md`.
- **Realization map:** `standards/doc/realization_map.md` is still measured against `72404ce4…`
  under `v0`. Re-survey it against the sealed v6 and standard `v1`. Record v6 as a genesis there,
  and give each new `v1` obligation its status.
- **CLM parked changes:** `business_domains/causal_language_model/doc/cr_sequence.md`, each run
  as a change dossier on its baseline design.
- **`README_DEV` "Known rough edges":**
  - `boot` requires `PGC_SNAPSHOT_PROFILES`;
  - `PGC_BUILD_ROOT` is inert;
  - `pgc` reports readiness for the platform compile only;
  - no serving path is published for an installed platform.
- **Transport:** phases after the frozen standard are not authorized. The HTTP adapter reads
  `PGC_DATA_ROOT` at import, so even the read-only inspector surface needs it set.
- **The demo** fetches `REF=v6`. Move it to the next identity at that cut.
- **Python:** the published packages ran on Python 3.15 under pipx, but the workspace builds and tests on 3.12.

- **Architecture Inversion draft** (`omnibachi-site/doc/pgc_architectural_inversion_draft.md`):
  - §6 the fifteen inversions, in four groups. Adapt them from the parkinglot v2.
  - Problem 2: the Governance Dividend, framed as complexity.
  - PGC scored against C1–C6. Each cell needs evidence that is derived, specified and exercised. Expected C cells: C1 (rules inside capabilities), C2 (impure transforms, external systems), C5 (bounded neighborhoods), and the violations the realization map records.
  - §2.2 repeats §3.4. Trim it.
  - Missing citations for declarative deployment and capability security in §4; take them from the v2 reference list.
  - Check before deposit: the IEEE DOI for [7]; the author lists for [4], [9] and [10]; Cedar's article number; the pages of [6]; and [1], [2].
  - Forward references to Appendix A and to sections not yet written.

### Next Session Should Start With
1. Run `regression.sh --all` on `dev/19` and expect 81/81. It passed on this tree, so this only
   confirms that nothing in the environment moved.
2. Pick the next task from "Open work". The candidates, roughly by readiness:
   - **Architecture Inversion draft:** §6 (the fifteen inversions), then the PGC scoring against C1–C6.
   - **`governance_chain_closure` doctrine** (2026-10-21 handoff, item 11.2): forbid domain-authored invariants, or let
     domain builds import the chain kinds, so the check can become a governed invariant.
   - **Realization map:** re-survey against sealed v6 and standard `v1`, and record v6 and this cut
     as geneses.
   - **CLM parked changes:** `causal_language_model/doc/cr_sequence.md`, each run as a change dossier.
   - **TI/TE in the design language:** they are schema-governed, but still outside P7.
3. At the cut, do the parked steps:
   - the field manual: drop its "where `v6` differs" notes, and name the new identity;
   - `genesis: false`;
   - point the `published_identity` expectation at the new release;
   - move the demo's `REF`.

# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-28 · Decision authoring: blockchain derived whole from a 120-line ledger; book unchanged

### This session
Work is on `dev/19`. The changes are staged in `transformation_compilers`, not committed. The
2026-10-27 handoff, which this replaces, is in git history.

**1. Phase split** (`doc/ANALYSIS_LEDGER_VS_PHASES.md`). The ledger does not force answers up
front: the questions come in rounds and open questions are allowed. But a typed catalog cannot ask
a reframing question. So P1–P3 stay a dialog for conceptual changes, and P4–P7 are generated.

**2. Blockchain, steps 1–5** (`domains/blockchain/`)
- **Census** (`FINDINGS_DECISION_LEDGER_CENSUS.md`): 32 decisions underlie 2,424 P7 values, with
  0 unaccounted. `census.py` now takes a per-domain profile; book's census is unchanged.
- **History:** four of seven deleted change requests (cr_03, cr_05, cr_06, cr_07) only repaired
  hand-written HOW. The seeds were recovered from commit `5d405b8^`.
- **Owner answers** (`LEDGER_OWNER_ANSWERS_BLOCKCHAIN.yaml`): 19 in all.
  - 5 settle disagreements between the seeds and P7.
  - 4 come from the seeds where the brief omitted them.
  - 10 settle decisions today's design made without recording them. The trust model stays
    deferred: whoever the request names as authority is recorded unchecked.
- **Brief and blind author** (`LEDGER_BRIEF_BLOCKCHAIN.md`, `FINDINGS_LEDGER_BRIEF_RUN.md`): the
  author addressed all 32 decisions and needed 12 new question types. 9 of those joined the
  catalog; 3 were doctrine.
- **Checks** (`checks/execution_validation_owner_answers.py`): 9 criteria written before any
  design. Today's design holds 2 of 9. `run_pipeline.sh` now runs `domains/<d>/checks/` too.

**3. Generator** (`engine/`, plan in `doc/PLAN_GENERATOR_SECOND_DOMAIN.md`)
- `doctrine.yaml`: 9 named rules. A citation of a rule the file does not state is refused.
- Ledger `parts`; a participant actor (`authorization: none`); four patterns: `register` with a
  repeat, `decide`, `list`, and `create_held`.
- **Carried surface:** store names and paths, request shapes, trail record keys, and entrances are
  copied from the baseline.
- Reach, offering and vocabulary rendering.
- `splice.py` handles the new registers and adds P8 `new_intents` entries for new requests.
- Plan step 7, a clock on every trail moment, was dropped: the trail store already stamps the
  envelope with its time.

### Build & test status
- `regression.sh --all` (2026-10-28): **PASSED, 81/81 steps as expected.** Nothing outside the
  prototype changed.
- `run_pipeline.sh blockchain <scratch>`: **PARTIAL.**
  - Construction 100% (1332/1332, 46 artifacts); compile 1/1; composition conformance passed.
  - Suites: `identity` 26/26, `routing_closure` 6/6, `wallet` 12/12.
  - Owner-answer checks **8/9**. FAIL: "listing a state no actor is in answers with an empty
    list", which is unrealized (see below).
- `run_pipeline.sh book_library_mgmt <scratch>`: **PASSING.**
  - Construction 100% (2076/2076); `catalog` 23/23, `catalog_works` 27/27.
  - `generated.json` is byte-identical to the 2026-10-27 output.
- Blockchain `generated.json` is deterministic: two runs compare equal.

### Open issues
- **Unrealized**
  - An empty list or search answers empty, in both book and blockchain. The platform's
    `CT_PURE_FILTER_RECORDS_V0` refuses an empty result; one platform transform would fix both.
    **Parked on dev/19, with a plan:**
    - The new transform is `capability_transforms::CT_PURE_SELECT_RECORDS_V0`. It uses the same
      criteria as the filter (exact value or `"present"`) and answers `[]` when nothing matches.
    - It needs its implementation and `TEST_DATA` (exact, presence, multiple criteria, empty,
      malformed input refused).
    - Add it to the closed list in `INVARIANT_CT_SURFACE_CLOSED_V0`. In place is allowed, because
      `genesis: true`.
    - The prototype generator then uses it for blockchain's listing and book's search.
    - Keep the filter: causal_language_model's `CC_RETRIEVE_USER_PROMPT_RECORD_V0` relies on
      its refusal.
    - Book's own `book_library_mgmt::CT_PURE_SELECT_RECORDS_V0` could later be retired in favour
      of the platform one, as a separate book change.
  - Defaults for a request that leaves a field out: preferences default to BACHI and English only
    at the entrance. No transform applies a default.
  - Book: a retitle that creates a work announces no "work registered". Conditional emission
    cannot be stated.
- **Defects in today's designs, parked**
  - Book: the five defects from 2026-10-27, in git history.
  - Blockchain: two holders supplying one key share an address. The vocabulary has 8 wallet
    classifications where the seeds name 4. No listing exists. A repeat registration records none of its
    details, and announces itself as a first one.
- **Versioning:** changed components keep `_V0`, because `sameness` is not wired in. Blockchain
  replaces 15 components and requests with new names.
- **Repo rules the prototype breaks:**
  - it reads P7 files, not `inspector.api`;
  - it uses `sys.path` in `splice.py` and the checks;
  - the ledger is normalized by hand, with no strict schema.
- **Fitted patterns:** `generate_domain.py` still hard-codes book names in `validate`,
  `write_record`, `details` and `update`. The blockchain patterns are fitted to two domains.

### Architectural concerns
- **The carried-surface rule** needs a home in the standard. Data on disk and callers fix names;
  a ledger change to them is a migration. Today the matching is heuristic: an exact name, the
  words of what a registry holds, or the part's single trail.
- **The generator is a design authority.** Doctrine is now data, but it is neither sealed nor
  versioned.
- **Phase split:** P1–P3 remain dialog for discovery changes. Each catalog miss becomes a new
  question type, which is a PGC-owned change.
- **The question catalog** is now 23 types plus a `default`. Records written before a change is
  still missing.

### Next session should start with
Commit the staged prototype work:
`cd transformation_compilers && git commit -m "Decision authoring: blockchain derived whole from its ledger"`.
Then decide the next direction. The platform empty-answer filter is parked (see Open issues). The
other option is a third domain, ai_governance, to test the generator beyond two fitted domains.

Carried, unchanged: decision accounting (`doc/DECISION_ACCOUNTING_DESIGN.md`) is parked on
dev/19. The ai_governance leaks (`cap`, `threshold_days`, `days_inactive`) are the top domain fix.

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

# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-21 · kind map, sealed ontology, genesis declared, names carried as data closed, every kind schema-governed, actor types canonical on dev/19

### This session
Nine pieces of work. Items 1–8 are committed and pushed on `dev/19`. **Item 9 is uncommitted in
`software_governance`, `protocol_compiler`, `business_domains` and `.github`** (see "Next Session
Should Start With").

**9. Actor types are canonical** (uncommitted)
- New `actor::VOCAB_ACTOR_TYPES_V0`: one closed group, `actor_type: [agent, human, system]`. It is
  the "governed actor type vocabulary" that `AC_TYPE_REQUIRED` names, and it did not exist before.
- Rule 1 of `ASSERT_AC_DECLARATION_WELL_FORMED_V0` now requires `core.type` to be one of these.
  A build that has actors but cannot see the vocabulary is refused. Proven: `type: ENDUSER` on
  the blockchain participant fails the compile.
- Six actors normalized:
  - `ENDUSER` → `human`: the blockchain participant, library staff, model staff and requester.
  - `ENDUSER` → `system`: the model host.
  - `person` → `human`: the ai_governance employee.
  - The `agent`, `system` and `human` actors were already canonical.
- No code reads `core.type`, so no behaviour changed. Designs and the surface map were
  regenerated. `human_block_fidelity` now counts 549.

**8. Every artifact kind is schema-governed** (`software_governance` `0f4b9d9`)
- `STRUCTURE_SCHEMA_DISPATCH_V0` recorded four kinds as `description_pending`. Each build now
  validates them, and the `description_pending` block is gone.
  - `SCHEMA_ACTOR_V0`, corrected: all 14 actors failed it. It pinned the wrong constitution,
    required a `role` no actor has, and forbade `attributes`, `type` and `description`.
  - `SCHEMA_INTENT_V0`, corrected: all 37 intents failed it. It pinned a short-code constitution
    and rejected `integer`.
  - `SCHEMA_TRANSPORT_INGRESS_V0` and `SCHEMA_TRANSPORT_EGRESS_V0`, new, written from Transport
    Standard V0 §6–7 and the 48 TI/TE artifacts:
    - Each has a closed surface.
    - A TI's `handler.kind` is `WF_INVOCATION` (needs `workflow`) or `SNAPSHOT_READ`/`SNAPSHOT_QUERY`
      (needs `operation` and `implementation`).
    - A TE's Result Classes are the six that `CONSTITUTION_TRANSPORT_EGRESS_V0` governs.
    - A TE's `op` values and its `evidence_policy` are the ones the transport resolver implements.
- All 99 artifacts of the four kinds pass. Proven negative: a TI with `handler.kind: WF_TELEPORT`
  and an actor declaring `permissions` each fail with `ASSERT_SCHEMA_CONFORMANCE_V0`.
- `domain_authoring` caught that an actor attribute may carry a literal `value`. The schema allows
  it.
- No transport behaviour changed: the schemas describe the existing declarations.
- Actor types were inconsistent. Item 9 made them canonical.

**7. The last names carried as data, closed** (uncommitted)
- **Bare codes are refused under name parts.** `VOCAB_DECLARATION_REPRESENTATION_V0` adds a group,
  `named_in_full`: `bootstrap_exception`, `event_code`, `event_type`, `governs`, `target_cs`.
  `Representation.short_codes` refuses a value under one of these parts that is written as an
  artifact's code (`…_V<n>`, no `::`). A kind token or a `$.` path is still a value.
  Proven: a bare `target_cs` in blockchain fails with `ASSERT_FQDN_ONLY_REFERENCES_V0`.
- **`STRUCTURE_ARTIFACT_IDENTITY_V0.bootstrap_exception`** now holds full names, as a reference
  part. It named `STRUCTURE_BUILD_DOMAINS_CONFIG_V0`, which doesn't exist; the entry and the prose
  naming it are gone.
- **A vocabulary may name artifacts.** `SCHEMA_VOCABULARY_V0` allows `names_kind` on a group.
  Rule 6 of `ASSERT_VOCABULARY_SYMBOLS_WELL_FORMED_V0` refuses an entry that is not the code of an
  artifact of that kind the build can see. `VOCAB_DESIGN_REGISTER_TERMS_V0.storage_type` declares
  `names_kind: CAPABILITY_SIDE_EFFECT`. Proven: adding `CS_GONE_V0` fails the transformation compile.
- The P7 rule params that list CS codes are generated from that vocabulary, and `emit_rule_sets
  --check` gates them, so they needed nothing.
- **The design language carries it.** `REGISTER_SCHEMA_P7_V0.vocabulary_extensions` gains an
  optional `names_kind` column ("Names Kind"). It is in the P7 template, the recorder
  (`record/design.py`), the renderer and `CONSTRUCTION_MAPPING.md`.
- Residual: three `only_when_value` consts in `REGISTER_SCHEMA_P7_V0` name CS codes. They gate rows
  of the Storage Type column, whose values the vocabulary closes, so a stale const makes its rule
  inert rather than wrong.

**6. Names carried as data are references; the cut is a genesis** (uncommitted; plan in `doc/PLAN_TYPED_REFERENCES_GENESIS.md`)
- `VOCAB_DECLARATION_REPRESENTATION_V0` adds four parts to its `reference` group: `target_cs`,
  `event_code`, `event_type`, `governs`. Only a value written as a full name is a reference, so a
  constitution's `core.governs` kind tokens and `$.inputs.*` paths stay values. None joins
  `full_name_required`, because that check refuses any value without `::`.
- 21 values rewritten as full names: 8 `target_cs` in claim CCs, 4 `event_type` in ai_governance
  WFs, 2 `event_code` in ai_governance record CCs, 7 `governs` in platform surface contracts.
- `SURFACE_CONTRACT_STORAGE_READ_V0` and `_WRITE_V0` named a non-existent `CS_NAME_REGISTRY_V0`;
  the name is removed. Putting it back as a full name now fails the platform compile:
  `E104_INVALID_FQDN: Dangling reference … → capability_side_effects::CS_NAME_REGISTRY_V0`.
- The runtime is unchanged: it passes a literal through as written, now a full name.
- Designs of record regenerated. In ai_governance's P8, the two record CCs move after the events
  they now reference.
- **Genesis declared** (`1b` §11), as v6 was:
  - `VOCAB_PROTOCOL_KINDS_V1` is back to `_V0`, with no `supersedes`. The compiler and the invariant
    prose name V0.
  - `retired_identities.yaml` is empty.
  - `process/genesis.yaml` declares `genesis: true`, read by `retirement.genesis()`.
    `published_identity_check.py` then compares nothing with v6; the ledger rules still hold.
  - `rulings.md`: "The cut after v6 is a genesis, built as a baseline" replaces the spent v6 ruling.
    Set `genesis: false` once the cut is sealed.

**1. The kind map: `si.kind.map`** (`snapshot_inspector` `7060f45`)
- The composition read one level up: every artifact kind, its category, provenance and runtime
  disposition, its field shares, its schema status, and how kinds refer to kinds.
- Edges come from the inspector's `SemanticGraph`, aggregated by kind. A number counts distinct
  artifact pairs, not edges.
- New pieces:
  - `TI_SI_KIND_MAP_V0` / `TE_SI_KIND_MAP_V0`, generated by `author_transport_contracts.py`
  - `inspector/queries/kind_map.py`
  - the browser page `client/web/kinds/`, linked from the surface's index
  - the offline export, `scripts/export_kind_map.py --snapshot <dir> --out <file>`
- The inspector now offers 20 operations: 15 reads and 5 queries.
- A snapshot sealed before this change, such as v6, refuses the export with one line.

**2. The Governance Ontology is sealed** (`software_governance` `2a8b006`, `protocol_compiler` `e821fda`)
- `artifact::VOCAB_GOVERNANCE_ONTOLOGY_V0` states each kind's semantic category, its provenance, and
  each category's runtime disposition, in the terms of standard `2b`.
- `artifact::INVARIANT_GOVERNANCE_ONTOLOGY_AGREES_V0` is declared by the new
  `artifact::CONSTITUTION_GOVERNANCE_ONTOLOGY_V0`. Its handler, `assert_governance_ontology_agrees_v0`,
  refuses a platform build in which the vocabulary and the compiler's built-in table
  (`artifact_kinds._DESCRIPTORS`) differ.
- This was proven on the real build: listing EVENT as participatory gave `E701 …
  ASSERT_GOVERNANCE_ONTOLOGY_AGREES_V0 — 2 violation(s)`.
- These are new identities only. Nothing published in v6 changed, and `published_identity` passes.
- The built-in table stays as the compiler's bootstrap, because the compiler needs the
  classification to compile the vocabulary.
- `si.kind.map` reads the ontology and reports `ontology_declared: false` where a snapshot seals none.

**3. `VOCAB_PROTOCOL_KINDS_V0` lists `TEST_DATA`**
- V0 listed sixteen artifact kinds and omitted `TEST_DATA`. It was first fixed as a V1
  supersession; the genesis (item 6) folded it back into V0 in place.

**4. Construction completeness gaps closed** (`transformation_compilers`, `.github`; uncommitted at handoff)
- Both gaps were measurement defects, not design gaps. The designs stated the values; the measure
  counted an empty value as undetermined.
  - ai_governance had 3 facts: literal `''` and `{}` on workflow node inputs.
  - transformation had 6: `gate: null` on phases with no human gate, which its STRUCTURE states
    on purpose.
- `render.py` now applies the existing rule, "an empty value a design wrote is determined", to
  workflow node literals and to STRUCTURE properties. It already applied it to contract steps.
- All six designs measure 100%, and every rendered artifact is byte-identical to before.
- **The gate.** `write_baseline_designs.py --check` now also requires each design of record to
  determine its whole registry. This held as a v6 baseline condition, but nothing measured it.
  Without the fix it reports `INCOMPLETE — 4/6` and exits 1.

**5. Design-redundancy study, shelved** (`.github` `2018890`, `doc/FINDINGS_DESIGN_REDUNDANCY.md`)
- **The question.** Could a smaller human vocabulary, with the machine artifacts fully generated,
  halve what a person authors?
- **The answer is no.** Measured in P7 register cells, what a person writes, 13–20% is
  redundant. Measured in rendered artifact facts, the figure was 35–40%. That figure overstated
  it, because the renderer already turns one register cell into several artifact facts.
- **Why it was shelved:**
  - The largest source is CC interface rows that bind platform capabilities. Deriving them needs
    construction to read the sealed composition while rendering.
  - Every option changes identities published in v6: `REGISTER_SCHEMA_P7_V0`, the rule set in
    `WF_P7_DESIGN_INTENT_ADMISSIBILITY_V0`, and the constitutions.
- **Method.** Count authoring effort in P7 register cells, never in artifact facts.
- **Rules that match by name do not hold.** They failed on every real domain.
- **What reopens it.** The finding names one question: may render read platform specs, as the phase
  checks already do through `si.capability.surface`?
- **Doctrine tension, recorded, not acted on.** `rulings.md` says no change after v6 may claim the
  v6 baseline ruling. `THE_SHAPE_OF_A_CHANGE_V0.md` §5 says a constitution clause needs a dossier.
  An in-place dev-phase simplification would need a ruling that replaces the v6 one.

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
- **Field manual:** `omnibachi-site/content/papers/foundations/pgc_field_manual_v1.md` describes the
  v6 composition. You edited it in place, so the Zenodo v1 deposit differs from the site.
- **Git:**
  - Items 1–8 are committed and pushed. Item 9 is uncommitted in four repos. `dev/19` and `main`
    exist locally and on the remote.
  - Every repo's `main` is one orphan commit, tagged `v6`. `pgc_install`'s `main` is `6.0.1`, and its `v6` tag stays on `6.0.0`.
  - Unsquashed history is in the local `history-18` tags.
  - Work happens on `dev/19`, where `VERSION` is 19.
- **Verified:**
  - `regression.sh --all` passes 82/82 on `dev/19` (2026-10-21, with item 9 in the working tree), on
    a clean rebuild after the negative tests. The 82nd step is `test_governance_ontology` (6/6).
    `test_reference_semantics` is 20/20, and `construction_mapping_test` states 186 fields. `test_inspector` is 167/167, and
    `human_block_fidelity` counts 549 artifacts. The working snapshot holds 545.
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
- **Field manual, at the next cut.** The kind map (`si.kind.map`) is on dev/19, not in v6, so the
  manual (`omnibachi-site/.../pgc_field_manual_v1.md`) stays as it is until a new identity is
  cut. Then:
  - §10 Inspection: add the kind map to the `SNAPSHOT_QUERY` examples.
  - Appendix A "Inspect": add `si kind map` and `scripts/export_kind_map.py`. "Nineteen
    operations: fifteen reads and four queries" becomes twenty: fifteen reads and five queries.
  - Appendix D "Add an inspection operation", step 1: the boundary contracts are generated by
    `snapshot_inspector/scripts/author_transport_contracts.py` from one declaration, not
    hand-authored. That is already true of v6.
  - §4 The artifact ontology: the ontology is now sealed as `artifact::VOCAB_GOVERNANCE_ONTOLOGY_V0`.
    `artifact::INVARIANT_GOVERNANCE_ONTOLOGY_AGREES_V0` refuses a platform build in which it and the
    compiler's built-in table differ.
- **Unenforced admission in collatz.** `IN_COLLATZ_INPUT_VALIDATED_V0` keeps its rules as prose in
  `extensions.admission_rules`, which construction drops. The enforced bound is in
  `TI_COLLATZ_COMPUTE_V0` (`number`, 1–999999). TI and TE are outside the design language
  (`transport_bindings: []`).
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

### Next Session Should Start With
1. **Commit item 9 in four repos, then push:**

   ```bash
   cd ~/protocol-governed-computing
   git -C software_governance add -A registry surface_map
   git -C software_governance commit -m "Govern actor types: VOCAB_ACTOR_TYPES_V0 (agent, human, system)"
   git -C protocol_compiler commit -am "An actor's type must be in the governed actor type vocabulary"
   git -C business_domains commit -am "Canonical actor types; regenerate designs of record"
   git -C .github commit -am "Expectations and SOTU: actor types canonical"
   for r in software_governance protocol_compiler business_domains .github; do git -C $r push origin dev/19; done
   ```
2. Run `regression.sh --all` on `dev/19` and expect 82/82.
3. No gap found this session remains open. Pick the next task from "Open work".

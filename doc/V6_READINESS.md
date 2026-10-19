# v6 Readiness

v6 is a baseline. It is clean, stable and forward-looking. It keeps no compatibility with earlier
versions, no history in the live tree, and no record of how it came to be. It introduces versioning
that is decoupled per component. Then it is cut, tested and locked.

Each item states what done means. Items under **A** are decisions. Order: B6 → C → B2–B5 → B1 with B7
→ D → E → F → G.

## A. Decisions

- **A1. Identity baseline: full reset.**
  - Every artifact is `_V0`, and `supersedes` is dropped everywhere. 549 artifacts: 47 are renamed,
    and 15 groups lose 17 superseded predecessors before their survivor is renamed.
  - Python modules named after a version follow their artifact.
  - The supersession rules and checks stay, because every change after v6 uses them. Only the data
    resets: the retirement ledger starts empty, and identity checks compare against v6, not v5.
  - Done by one rename map, generated from the snapshot and applied to every repository in a
    single pass, with the regression green before and after.
- **A2. Versioning: decoupled, starting at 6.0.0.** Every distribution starts at `6.0.0` and moves
  on its own after v6. A composition is named by a manifest in `pgc_release`, which lists each
  component's version and the snapshot identity. `pgc_install`'s pins are generated from that
  manifest, and the snapshot records the component versions it was built from.
- **A3. History documents: removed.**
  - These leave the live tree, and git history keeps them: the change dossiers and their delivery
    notes, the genesis delivery note, `process/notes/`, `rulings.md`, the swap plan, and the
    `archive/*` tags.
  - Release notes leave too: the `pgc_release` manifest states what a version is (A2).
  - What the dossiers proved moves to a **baseline design of record per domain** (A6).
  - The catalog fixtures (`fixture_dossiers/`) and the bootstrap copies (`delivered_copies/`) are
    test fixtures, not history. They stay, renamed and stripped of history prose.
- **A6. Baseline designs.**
  - Each domain carries one P7/P8 design of record, in `<domain>/design/`, that determines its whole
    v6 registry. It is generated from the registry by the genesis generators, made general.
  - `construction_acceptance` asks whether each domain's design rebuilds its registry.
  - Every change after v6 is a dossier built on that design.
- **A4. G-4: out of scope.** Gate approval, mandate approval and composition identity stay
  enforced by people and `tc baseline verify`. P7 states this as the module's scope, not a
  deferral.
- **A5. Composition content.** All four business domains, transformation, collatz and inspection.

## B. Remove the breadcrumbs

- **B1. Identities. Done.** Apply A1. One landing, together with B7: the reset, the cr_dossiers
  deletion, the baseline designs (A6), and `construction_acceptance` re-pointed at them.
  - Every artifact is `_V0`, none carries `supersedes`, and the ledger is empty.
  - Hard-coded identities in compiler and runtime code are reviewed, not blindly replaced.
  - `standards` names no realization identity. `spec/` cites none, and `doc/realization_map.md` is
    evidence about the snapshot its §0 names, so it keeps that snapshot's identities. Rebasing it is E3.
  - Stage 3 done: 16 predecessors are deleted and 65 identities renamed to `_V0`, with their
    handler and transform modules. No artifact carries `supersedes` and `retired_identities.yaml` is
    empty. Prose that narrated one version against another states the rule instead.
  - Supersession is declared once, on the successor (`4e` SU-3, SU-5). No schema admits
    `superseded_by`; the compiler derives which artifacts are superseded from every `supersedes`.
- **B2. Legacy references. Done.** Zero matches for `pgs_`, `RI-0` and `bachipeachy/pgs` outside
  what must name them: the two guards that refuse a legacy package (`pgc_env_check.py`,
  `verify_release.py`), the frozen `TRANSPORT_STANDARD_V0.md`, the sealed `pgc_release`, and
  `publications.md`, which reserves `v0` for that lineage. The store-entity payload key is
  `__store_entity__`, the platform schemas' `$id`s are `software_governance.schemas.*`, and the RI-0
  path registry, layout artifact, maintenance scripts, legacy runtime suite and web page are deleted.
- **B3. History in prose.** Comments, docs and artifact text describe what is, not what was:
  "previously", "no longer", "before this", "formerly", "used to", "was once". 513 matches today;
  each one is rewritten or removed. **Done.** 362 of the 513 are in dossiers, the corpora, fixtures
  and payloads cut from them, and go with B7. Of the 151 left, about 45 narrated history and are rewritten.
  The rest state present meaning ("a retired copy is no longer held", "used to verify", "before
  this step") or are exempt: the frozen transport standard, `publications.md` (a release record),
  and the external-validation runs (evidence). Left for later items: `construction_acceptance.py`'s
  sequencing comments go with B7, and the RUNBOOK's former-failure notes with B5. Every repo's
  NOTICE now opens "PGC — Protocol-Governed Computing", except the sealed `pgc_release`.
- **B4. Process markers in artifacts.** Zero `**Status:**` lines and zero "cut-#" or "Phase N"
  delivery notes in artifact text. 8 and 6 today. Example: `TI_COLLATZ_COMPUTE_V0`'s "cut-#1
  hand-authored. Promoted… in Phase 3". **Done.** Removed eight `**Status**: CANONICAL` headers
  (seven STRUCTUREs and the collatz build manifest), the four "cut-#1… Phase 3" lines (the collatz
  TI/TE and both transport contracts), and the Status label in `rule_ownership.md`. Kept: the
  `status: active` machine-block fields, which are governed, and the frozen transport standard.
- **B5. Expectations and RUNBOOK.** Comments in `expectations.yaml` and RUNBOOK sections that
  narrate count changes ("34 → 35", "swap:") are reduced to what each step checks. **Done.**
  Every `expectations.yaml` comment states what its step checks, with no count deltas or work
  labels. The RUNBOOK's Expected table states no counts, since `expectations.yaml` holds them and
  the table's copies had drifted. Its former-failure notes state the rule they taught. Left for B7:
  the RUNBOOK's dossier paths, the construction sequence, and the "simple path" costs, which assume
  a domain has no design.
- **B6. Pure history. Done.** Delete what no test reads: `process/notes/` and the genesis dossier's
  delivery note, and the references to them. `rulings.md` stays as present-tense doctrine: its rules
  are in force, and the one spent ruling is dropped. This comes first in B.
- **B7. The dossier corpus. Done.** Delete `*/cr_dossiers` and the genesis dossier, generate the baseline
  designs (A6), and re-point `construction_acceptance`. This lands with B1.
  - Stage 1 done: `python -m transformation.record` writes each designed root's P7 and P8 from its
    registry into `<root>/design/`, and `write_baseline_designs.py --check` keeps them current.
    `construction_acceptance` renders one design per root and reproduces 279 of 280 artifacts; the
    one difference was a predecessor the reset deletes. After the reset it reproduces all 270.
  - The design language gained a store's `Structure`, and a structure with no store and no layer
    renders as a shape. The renderer writes typed property and policy values, every step's
    `outputs`, and a transform's module under the namespace its build manifest declares. Actors are
    governed by `actor::CONSTITUTION_ACTOR_IDENTITY_V0`.
  - Hand-authored artifacts in ai_governance, transformation and collatz were rewritten in the form
    construction writes. Facts nothing reads were removed: EXIT `reason` and `status`, field `enum`,
    binding `host`/`type`/`operation`, a node's `payload_schema`, an attribute's `value`.
  - Stage 2 done: the dossier corpus is deleted — every `cr_dossiers`, the genesis dossier and its
    generators, and the delivered copies. The test fixtures stay as
    `transformation_compilers/scripts/testbed/fixtures/`: the catalog chain and the transformation
    phases' P0–P2. The RUNBOOK, READMEs, architectures and CLAUDE.md files describe designs of record.
  - `WF_AUTO_RECLAIM_V0` declared `core.admission`, an event-log precondition form nothing realized,
    so it was removed. `transport::CONSTITUTION_ADMISSION_V0` now states the admission the runtime
    realizes: the IN gate judges the payload against its declared input contract.
- **B8. RI-0 machinery still in the compiler. Done.** Found by B2:
  - `ASSERT_NO_SMART_EXECUTION_V0`'s handler scans runtime files that do not exist, so it always
    passes; `ASSERT_ATOM_OUTPUT_PURITY_V0` and `ASSERT_CT_OUTPUT_CONTRACT_MATCH_V0` may be the same.
    Each either checks something real or its invariant states it is enforced elsewhere.
  - `ProtocolLoader.load` and `domain_resolver` read RI-0's workspace layout and nothing calls them.
  - `CONSTITUTION_FEDERATION_BOUNDARY_V0` describes `FB_*` directories and `fb.*` namespaces that
    no longer exist.
  - Resolved: the three handlers are deleted, because none could fail. Each invariant is
    `enforced_elsewhere` and states its rule as it stands. No smart execution is held by a new
    runtime test (`test_no_smart_execution.py`). Output contract match is held by conformance, which
    now fails a result whose keys differ from the declared outputs; that found twelve atoms returning
    an undeclared `result_status`, now removed. Atom output purity is held by the CT executor and
    conformance, in the schema's terms for `refusal`. The loader and resolver are deleted. The
    federation constitution follows `AUTHORITY_VS_CONCERN_RULING.md`: a boundary is an authority,
    `pgc.platform` is the only one, and namespaces are concerns.

## C. Close known defects, so nothing is red by design

- **C1. `blockchain_identity`. Done.** A TE output field is owed unless it declares
  `required: false`, and the response omits an optional field the result does not carry. P7's
  `transport_bindings` states it in a `Required` column, so construction writes it. `grounds` on
  `TE_ACCEPT_ACTOR_V0` is optional, and the step holds 26/26.
- **C2. `construction_acceptance`. Done.** Book library's two `_V1` artifacts carry `version: v0`.
  The reset in A1 resolves it, and B7 resolves blockchain's undesigned vector (C10); done when
  the step is green.
- **C3. `si snapshot validate` advisories. Done.**
  - A domain that runs a platform capability carries a copy that records exactly what the platform
    records.
  - ai_governance declares its action registry as a store.
  - The regression runs the check with `--strict`.
- **C4. Genesis G-8. Done.** `transformation.build.provenance` is the one place a leaf is addressed
  and its origin derived. The measure reads the provenance it is handed, and a new vector case
  proves a renderer-supplied value is refused. Carried values were recorded under a path no leaf
  had, and are now attributed correctly.
- **C5. Genesis G-3. Done.** P7's `interface_fields` states a field's shape in a `Structure`
  column, and `FIELD_STRUCTURE_UNDECLARED` requires it to name a STRUCTURE the design declares or
  carries over. Genesis is regenerated, re-pinned and admissible P0–P8, and its transforms rebuild
  their structures. The mapping test reads genesis beside the acceptance corpus. Genesis rebuilds
  20 of its 41 artifacts and measures 98.7% complete; the rest is B7's input:
  - `supersedes` on five artifacts (A1 drops it);
  - actors, contracts, bindings and the build manifest, which the design language cannot yet state;
  - STRUCTURE `concern`, `layer` and `entity_stores`, which the renderer supplies;
  - exit-node `status` on `WF_CONSTRUCT_ARTIFACTS_V0`.
- **C6. Genesis G-2. Done.** A workflow's actor is stated as its `actor_context` property, and
  `WORKFLOW_ACTOR_UNDECLARED` requires it to resolve. Unstated, it is determined only when the design
  has one actor to choose; among several, the renderer's choice is recorded as its own and refused
  by the measure. Genesis states all fourteen. The measure found one real defect:
  `WF_SUBMIT_USER_PROMPT_V0` ran as model staff, and the seed says requesters submit prompts. It now
  runs as `AC_REQUESTER_V0`, and CLM's design states every workflow's actor.
- **C7. Genesis G-4. Done.** Genesis P7 states the three refusals as the module's scope: approving a
  gate, approving a mandate and confirming a pin are acts of people, and none is open work. Genesis
  is re-pinned and admissible P0–P8.
- **C8. The flaky first `--all`. Closed on evidence.** Its three failures each read the platform
  surface just after it compiled and found it incomplete; root cause unknown, never reproduced. The
  regression guards it: the platform surface is fingerprinted after its compile and re-checked after
  every later compile, and a failed build's output is kept in `$TMPDIR/pgc_failed_build.*`. Since
  then about fifteen `--all` runs, including three consecutive clean rebuilds, gave one snapshot
  identity and identical verdicts on all 366 steps. Neither trap has fired, and no failed build was
  kept. A recurrence is caught and named by the traps, so it reopens with its evidence.
- **C9. `pgc_sloc.py`. Done.** Registry schemas are counted as declared behaviour in a
  `json_schema` column: 16,669 lines, 4,532 in the platform and 12,137 in transformation.
- **C10. Every transform proven. Done.** Every domain's conformance line reports 0 unproven. The
  book catalog's four vectors are the ones its designs already stated. Two findings carry forward:
  - blockchain's designs state no vector for `CT_PURE_DERIVE_WALLET_ADDRESS_V0`, so
    `construction_acceptance` reports it as a miss until B7 generates the baseline design;
  - `CT_PURE_FORM_BOOK_IDENTITY_KEY_V0` declares `refusal: never`, and its designed vector expects a
    refusal of a blank title. Settled by B8: neither is wrong. `SCHEMA_CAPABILITY_TRANSFORM_V0`
    makes refusal a judgement about the subject, and every transform raises on malformed input.

Done for C as a whole: `expectations.yaml` holds no `red_by_design` except `published_identity`.
That one is red by ruling while the baseline is built, and it returns to a plain pass at the cut
(F1).

## D. Versioning — Done

- **D1.** Each distribution carries its own version per A2, and every one starts at `6.0.0`:
  - `pgc-governance`, `pgc-compiler`, `pgc-assembler`, `pgc-runtime`, `pgc-inspector`;
  - `pgc-transport`, new in v6;
  - `pgc-transformation`, `pgc-workloads`, `pgc-domains`.
- **D2.** `release.sh` enforces A2 instead of lockstep. A repo whose tree changed since the previous
  public tag must declare a version that tag did not, and `--publish` refuses a version PyPI already
  holds. The previous version is read from the previous public tag, because the v5 manifest records
  no versions. The release-notes requirement is gone.
- **D3.** `compose_release.py` writes `pgc_release/composition.json`: each component's distribution,
  version, commit and DOI, and the snapshot identity. `MANIFEST.md`, `pgc_install`'s pins and
  `pgc/composition.py` are generated from it. The snapshot's provenance records
  `component_versions`: each contributing repo's version, and the assembler's own.
- **D4.** `pgc status` names the composition it was installed as, and flags a package whose version
  differs from its pin. A source install reports that it has no composition.

## E. Code and repository hygiene

- **E1. Done.** `to_canonical_request` is in `pgc_transport/request.py`, which knows no protocol.
  Both adapters import it from there, and the CLI adapter no longer imports from the HTTP adapter.
- **E2. Done.** `workflow_diagram.js` lives once, in the inspector's client. The Collatz client
  loads it from `/diagram/`, which `serve.sh`, `pgc-demo.sh` and `README_DEV.md` mount from the
  inspector.
- **E3. Done, no change.** The realization map names one transport path, `protocol_transport/CLAUDE.md`,
  and that file exists. The map does not take part in revision (§0), so `revisions.md` declares
  nothing.
- **E4. Done.** Each `README`, `ARCHITECTURE` and `CLAUDE.md` states only what is true of v6. Wrong
  paths, version claims, the RI-0 fidelity criterion and rebuild history are gone. One sentence
  of RI-0 provenance stays where a repo began as a fork. A domain's design of record is in
  `design/`, and a change is authored in `cr_dossiers/`.
- **E5.** Each repository is clean on `dev/18`, and `pgc_install` `dev/18` is backed up.

## F. Cut — Done

- **F1.** `regression.sh --all` passes 81/81 with no `red_by_design`, and a second run is identical.
  `published_identity` passes against the sealed v6: 540 identities, none changed meaning.
- **F2.** Two clean rebuilds, and a rebuild in a second folder, give one snapshot identity,
  `13e3c5bb502e2548389f5787caa9438247ee34f9d510ce6a8a3ed980fdf974d1`. A rebuild on `dev/19`
  differs from it only in the toolchain ordinal and timestamps.
- **F3.** `release.sh` cut v6. All nine distributions and `protocol-governed-computing` are on PyPI
  at `6.0.0`, `pgc-transport` for the first time. `pgc_release` v6 is sealed and tagged, and its
  DOI is `10.5281/zenodo.23485442`.
- **F4.** Zenodo `--verify` passes 9/9. Components are matched by concept DOI, not by title.

## G. Final test, then lock

- **G1.** A clean machine: `pipx install --include-deps protocol-governed-computing`, then
  `pgc-demo.sh` in release mode. Every Demo 1 and Demo 2 step works, including both pages in a real
  browser.
- **G2.** `README_DEV.md`'s developer path runs end to end against the published v6.
- **G3.** Lock:
  - `main` holds one commit for v6, tagged `v6`, in every repository;
  - `dev/18` is retired;
  - the next work opens `dev/19`.

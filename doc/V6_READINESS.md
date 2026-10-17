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

- **B1. Identities.** Apply A1. One landing, together with B7: the reset, the cr_dossiers
  deletion, the baseline designs (A6), and `construction_acceptance` re-pointed at them.
  - Every artifact is `_V0`, none carries `supersedes`, and the ledger is empty.
  - Hard-coded identities in compiler and runtime code are reviewed, not blindly replaced.
  - `standards` applies the same map, declared in `revisions.md`.
- **B2. Legacy references.** Zero matches for `pgs_`, `RI-0` and `bachipeachy/pgs` across the
  repositories. 194 today.
- **B3. History in prose.** Comments, docs and artifact text describe what is, not what was:
  "previously", "no longer", "before this", "formerly", "used to", "was once". 513 matches today;
  each one is rewritten or removed.
- **B4. Process markers in artifacts.** Zero `**Status:**` lines and zero "cut-#" or "Phase N"
  delivery notes in artifact text. 8 and 6 today. Example: `TI_COLLATZ_COMPUTE_V0`'s "cut-#1
  hand-authored. Promoted… in Phase 3".
- **B5. Expectations and RUNBOOK.** Comments in `expectations.yaml` and RUNBOOK sections that
  narrate count changes ("34 → 35", "swap:") are reduced to what each step checks.
- **B6. Pure history.** Delete what no test reads: `process/notes/` and the genesis dossier's
  delivery note, and the references to them. `rulings.md` stays as present-tense doctrine: its rules
  are in force, and the one spent ruling is dropped. This comes first in B.
- **B7. The dossier corpus.** Delete `*/cr_dossiers` and the genesis dossier, generate the baseline
  designs (A6), and re-point `construction_acceptance`. This lands with B1.

## C. Close known defects, so nothing is red by design

- **C1. `blockchain_identity` 25/26.** The TE output contract can declare a field optional, and
  `grounds` is declared optional. Done when the step is green and loses `red_by_design`.
- **C2. `construction_acceptance`.** Book library's two `_V1` artifacts carry `version: v0`.
  The reset in A1 resolves it; done when the step is green.
- **C3. `si snapshot validate` advisories. Done.**
  - A domain that runs a platform capability carries a copy that records exactly what the platform
    records.
  - ai_governance declares its action registry as a store.
  - The regression runs the check with `--strict`.
- **C4. Genesis G-8. Done.** `transformation.build.provenance` is the one place a leaf is addressed
  and its origin derived. The measure reads the provenance it is handed, and a new vector case
  proves a renderer-supplied value is refused. Carried values were recorded under a path no leaf
  had, and are now attributed correctly.
- **C5. Genesis G-3.** The design language states a field's `structure`. Through the lifecycle.
- **C6. Genesis G-2.** The design language states which actor each workflow runs under. Through
  the lifecycle.
- **C7. Genesis G-4.** P7 states the three refusals as out of scope (A4).
- **C8. The flaky first `--all`.** Reproduce it or close it with evidence.
- **C9. `pgc_sloc.py`.** It counts `registry/schema/*.json`.
- **C10. Every transform proven.** Eight transforms carry no vectors:
  - `capability_transforms::CT_PURE_COMPARE_EQUAL_V0`;
  - collatz's `CT_PURE_COLLATZ_STEP_V0` and `CT_PURE_TERMINATION_CHECK_V0`;
  - book_library_mgmt's four;
  - blockchain's `CT_PURE_DERIVE_WALLET_ADDRESS_V0`.

  Done when every domain's conformance line reports 0 unproven.

Done for C as a whole: `expectations.yaml` holds no `red_by_design` except `published_identity`.
That one is red by ruling while the baseline is built, and it returns to a plain pass at the cut
(F1).

## D. Versioning

- **D1.** Each distribution carries its own version per A2:
  - `pgc-governance`, `pgc-compiler`, `pgc-assembler`, `pgc-runtime`, `pgc-inspector`;
  - `pgc-transport`, new in v6;
  - `pgc-transformation`, `pgc-workloads`, `pgc-domains`.
- **D2.** `release.sh` enforces the A2 rule instead of lockstep. It reads what a version is from the
  `pgc_release` manifest, not from `process/notes/release-<N>.md`, which B6 removes, and
  `pgc_install`'s pins are generated from that manifest.
- **D3.** The composition record names every component version and the snapshot identity, and
  `pgc_release/MANIFEST.md` is generated from it.
- **D4.** `pgc` reports the composition it was installed as.

## E. Code and repository hygiene

- **E1.** `to_canonical_request` moves to a protocol-neutral module in `pgc_transport`, so the CLI
  adapter no longer imports from the HTTP adapter.
- **E2.** `workflow_diagram.js` lives once. Both clients load the same file, or one client owns it
  and the other is served it.
- **E3.** `standards/doc/realization_map.md` points at `pgc_transport/…` paths. This is declared in
  `revisions.md`.
- **E4.** Every repository's `README`, `ARCHITECTURE` and `CLAUDE.md` describes the v6 layout and
  nothing earlier.
- **E5.** Each repository is clean on `dev/18`, and `pgc_install` `dev/18` is backed up.

## F. Cut

- **F1.** `regression.sh --all` is green with no `red_by_design`, and a second run is identical.
  `published_identity` passes against the sealed v6, and its expectation is restored to a plain pass.
- **F2.** Two clean rebuilds, and a rebuild in a second folder, give one snapshot identity.
- **F3.** `release.sh` cuts v6. Every distribution is built and uploaded, `pgc-transport` for the
  first time. `pgc_release` v6 is sealed and tagged, and its DOI is minted.
- **F4.** Zenodo `--verify` passes.

## G. Final test, then lock

- **G1.** A clean machine: `pipx install --include-deps protocol-governed-computing`, then
  `pgc-demo.sh` in release mode. Every Demo 1 and Demo 2 step works, including both pages in a real
  browser.
- **G2.** `README_DEV.md`'s developer path runs end to end against the published v6.
- **G3.** Lock:
  - `main` holds one commit for v6, tagged `v6`, in every repository;
  - `dev/18` is retired;
  - the next work opens `dev/19`.

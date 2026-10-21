# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-21 · design-redundancy study shelved; dev/19 unchanged

### This session
A study of whether construction can derive what a design restates. It was measured, then
shelved. The only change is `doc/FINDINGS_DESIGN_REDUNDANCY.md`, committed on `.github` `dev/19`
(`2018890`). No other repository changed.

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
v6 is published. Every later change is measured against it.

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
  - Every repo is clean and pushed. `dev/19` and `main` exist locally and on the remote.
  - Every repo's `main` is one orphan commit, tagged `v6`. `pgc_install`'s `main` is `6.0.1`, and its `v6` tag stays on `6.0.0`.
  - Unsquashed history is in the local `history-18` tags.
  - Work happens on `dev/19`, where `VERSION` is 19.
- **Verified:**
  - `regression.sh --all` passes 81/81 on `dev/19` (re-run 2026-10-21, twice this session).
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

### Open work
- **Construction completeness gaps, found this session.** Both predate it, and the regression does
  not catch them.
  - `ai_governance` is 99.75% (1218/1221). Three node inputs in `WF_PROVISION_AI_LICENSING_V0` are
    not determined by its design: `CC_APPEND_AUDIT_EVENT_SUCCESS.inputs.reason_code` and `.data`,
    and `CC_APPEND_AUDIT_EVENT_DENIED.inputs.data`.
  - `transformation` is 99.53% (1282/1288): six `core.phases[].gate` facts.
  - Reproduce with `python -m transformation construction check <root>/design --root <root>`.
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
Read this, then run `regression.sh --all` on `dev/19`. Next, decide whether the two construction
completeness gaps are defects to close or limits to record. They are the only measured defects open,
and a design below 100% means construction cannot rebuild that registry from it.

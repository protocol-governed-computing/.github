# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-19 · v6 is the baseline; dev/19 is open

### Where things stand
v6 is published. Every later change is measured against it.

- **Composition `v6`:** DOI `10.5281/zenodo.23485442`. Sealed snapshot
  `13e3c5bb502e2548389f5787caa9438247ee34f9d510ce6a8a3ed980fdf974d1`: 8 domains, 556 artifacts,
  `GOVERNANCE_SURFACE_PROFILE_V0`. `pgc_release/composition.json` names each component's version,
  commit and DOI.
- **PyPI:**
  - The nine components are at `6.0.0`.
  - `protocol-governed-computing` is at `6.0.1`. It pins those nine, and `pgc status` names composition v6.
- **Git:**
  - Every repo's `main` is one orphan commit, tagged `v6`. `pgc_install`'s `main` is `6.0.1`, and its `v6` tag stays on `6.0.0`.
  - Unsquashed history is in the local `history-18` tags.
  - Work happens on `dev/19`, where `VERSION` is 19.
- **Verified:**
  - `regression.sh --all` passes 81/81, twice, with no `red_by_design`.
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
- **Zenodo matching.** Component records are matched by concept DOI (`COMPONENT_CONCEPTS` in
  `compose_release.py`), not by title. The v6 transformation record is titled `(transformation)`,
  and Zenodo will not let it be edited.

### Open work
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
Read this, run `regression.sh --all` on `dev/19`, and pick the first change from the open work.

# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-12 · swap step A done; awaiting the user's squash (step B)

### Changes Made
- All on the rebuild branches (`transformation`, `.github`, `software_governance`) plus `protocol_runtime` on `dev/18`. Plan and outcome: `.github/process/notes/swap-plan.md` §3–3a. All six decisions D1–D6 were approved as recommended.
- Deleted: 28 identities by record (25 transformation, 2 lifecycle constitutions, `VOCAB_DECLARATION_REPRESENTATION_V0`); 4 V0 transform modules; `dossiers/` except genesis; `scripts/rebuild/`; the 5 working docs (charter, design, unravel, coverage verification, genesis triage).
- `.github/process/retired_identities.yaml` — 29 entries; `notes/rebuild-retirements.yaml` deleted (staged with `git rm`).
- `transformation/CLAUDE.md` — rulings restated: phase document, declared rules, one live version, vectors, platform governance, genesis. `README.md` and `ARCHITECTURE.md` corrected.
- `regression.sh` — pristine and leak-detecting: per-run `TMPDIR` checked empty (`temp_hygiene`), bytecode cleared, the `single_instance` step (transformation, artifact, lifecycle). `e2e_phases_test.py` keeps the design baseline in `traces/`. `construction_acceptance.py` reports RETIRED BY RECORD. `differential.py` uses the V1 modules. 3 corpus docs and 4 payloads cite the live identities. `test_examine.py` no longer leaks.
- `software_governance/surface_map/governance_surface_map.yaml` regenerated; `INVARIANT_RENDER_INVENTS_NOTHING_V0` names the V1 transform.
- Genesis re-pinned to `37968c3e…` (503); P0–P8 ADMISSIBLE, 0 findings.
- Cleanup before step B: `.github` ephemera removed (rule-effectivity generators, SOTU archive, trial instruments; SOTU trimmed to this entry); `doc/parked_rulings.md` moved to `standards/doc/`; all 10 `software_governance/dossiers/` deleted (table form, unjudgeable by the rebuilt module; 9 held at tag v5, `data_parts` on the archived rebuild branch); test docstrings point at the tag. The 17 business/workload dossiers were converted in place to the Machine form by the oracle's reader (153 documents; P7/P8 byte-identical to the corpus; all parse), the testbed reads them in place, and `delivered_copies/` keeps only the two base-code roots. Ruling in `transformation/CLAUDE.md`; note in `business_domains/README.md`. Regression `--all` clean: 77/77.
- Found, not fixed: `business_domains/CLAUDE.md` still describes RI-0 (`pgs_*`).

### Build & Test Status
PASSING. `regression.sh --all` from a clean workspace: 77/77, exit 0; no build failure, the platform surface unchanged, `temp_hygiene` passes. Final oracle comparisons before `scripts/rebuild/` was deleted: 193 / 884 / 189 identical. The oracle can no longer be run.

### Open Issues
- Step B (the user's): commit and push the rebuild branches; squash into `dev/18` in the order software_governance, transformation, .github; regression on `dev/18`; push; archive the branches; remove the `~/pgc-oracle` worktree.
- Step C: the rename to `transformation_compilers`, as a separate change.
- The flaky first `--all` is still unreproduced; the traps stay.
- `dist/` and `build/` in several repos hold v5 release packages. They are gitignored and were not cleaned.

### Architectural Concerns
- Delivered-dossier test copies are now corpus fixtures that follow the live composition (D2). The originals are held by the oracle tag.

### Next Session Should Start With
Run `regression.sh --all` on `dev/18` after the user's squash (swap-plan §4), then step C.

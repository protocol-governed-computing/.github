# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-13 · dev/18 green; demo prototyped; comparative paper planned

### Changes Made
- **Rebuild swap closed.** `rebuild/transformation` was squashed into `dev/18` in software_governance, transformation_compilers and .github. The branch tips are tagged `archive/rebuild-transformation`, and the branches are deleted. The tag holds the `data_parts` dossier that genesis G-11 cites.
- **Genesis G-12.** `transformation::IN_BUSINESS_INTENT_SUBMITTED_V1` declares the `prior_texts` that P5 reads. V0 is retired by record.
- **blockchain `cr_07_own_values`, delivered.**
  - The identity and wallet acts now state the values only the business may decide. Before, those values came from the request.
  - 8 successors were emitted, and 14 identities were retired by record. The ledger holds 44 entries.
  - The admission contract fidelity check now passes: 0 findings over 37 gates.
  - Delivery notes and what was corrected at delivery: `business_domains/blockchain/cr_dossiers/cr_07_own_values/delivery.md`.
- **Generators.** The generators of delivered dossiers were removed from `.github/process/notes`; git holds them.
  - The genesis generators moved to `transformation_compilers/scripts/genesis/`, the repo they read. Regenerating from there reproduces genesis P7 and P8 byte for byte.
  - Ruling C1 was amended to match, in `rulings.md` and `transformation_compilers/CLAUDE.md`.
  - Genesis was re-pinned to `72ff39c8…` (497 artifacts) after cr_07. P0–P8 are admissible with 0 findings.
- **`pgc_install`** has a local `dev/18` branch (2 commits) and a local `v5` tag on `9c1f9f1`.
  - `README.md` is now a short introduction.
  - `README_DEV.md` holds the former developer guide.
  - `README_DEMO.md` is the spec for Demo 1 (the Collatz game) and Demo 2 (look inside the game, change a rule).
- **Demo prototype**, in the session scratchpad only, not in any repo: `scratchpad/pgc_demo/`.
  - Wheel: `protocol-governed-computing-demo` 0.1.0.dev0, 9.7 MB.
  - `scripts/stage_assets.py` pulls the snapshot, profiles, transport and client bindings from the `v5` tags.
  - The demo owns its Collatz web page: no check in the browser, and a run-path view drawn from the trace plus the sealed `graph.json`.
  - The `pgc-demo` commands are `collatz`, `collatz N` (sent through the entrance) and `where`.
- **Paper plan.** `~/omnibachi-site/parkinglot/comparative_evaluation_proposal.md`: a research question with four measured parts, three systems compared, defect injection, and a related-work map.

### Build & Test Status
PASSING. A clean `regression.sh --all` on `dev/18` gives 77/77, exit 0.
- The demo wheel was installed into a clean Python 3.12 venv, with its dependencies from PyPI 5.0.0.
- Terminal: 27 succeeds in 111 steps, peaking at 9,232. -5, 0, 1000000 and `abc` are refused at the entrance (`INPUT_OUT_OF_RANGE`, `INPUT_TYPE`).
- HTTP: the page, the PNG, the trace and the path view all serve.
- Not yet checked: the user has not tried the page in a browser.

### Open Issues
- **`pgc_install` git steps not yet run (the user's):**
  - local `main` and remote `main` are still at `3dd64ef`;
  - `git branch -f main 9c1f9f1`, a `--force-with-lease` push of `main`, and pushing `v5` and `dev/18` are pending.
- **`standards`** has 1 unpushed commit on `work/v1`.
- **`parkinglot/` is gitignored** in omnibachi-site, so the paper plan is neither versioned nor backed up.
- **Demo:**
  - The `pgc_demo` repo does not exist yet.
  - Demo 2 is unbuilt: `pgc-demo inspect`, a diagram-first inspector page, `show` and `code`.
  - Demo 2's `set-limit`, `reset` and `tamper` need a rebuild on the user's machine. That means shipping the Collatz declarations at v5, the compiled platform and inspection roots, and the profile, all unproven.
- **The `dev/18` runtime refuses the v5 snapshot on Collatz.** This was found during the demo prototype (`check_termination` routing, INVARIANT_TOPOLOGY_CONTRACT_CLOSED_V1). Decide before v6 whether that is intended or a compatibility break.
- **Carried from before:**
  - the TE output contract cannot declare `grounds` optional, so blockchain_identity is at 25/26;
  - 16 republished copies have drifted (advisory only);
  - 4 blockchain V0 contracts are stood down, plus the sweep in other domains;
  - genesis G-2, G-3, G-4 and G-8 are open;
  - Zenodo `--verify` must run before v6;
  - the flaky first `--all` is still unreproduced.
- **`pgc_sloc.py`** does not count `registry/schema/*.json` (12,057 lines of declared rules), so it understates declared behaviour.

### Architectural Concerns
- **Versioning is parked.** The plan is per-repo package versions, plus a composition manifest that `pgc_install`'s pins could become.
  - It reverses `release.sh`'s lockstep ruling.
  - `pgc_install` must either join `REPOS` and carry a `VERSION`, or become the manifest. Decide before the v6 cut.
- **Where a rule lives.** The Collatz range is enforced only at the entrance (`TI_COLLATZ_COMPUTE_V0`). A direct runtime call skips it. The demo must call through the entrance. This is also a candidate topic for Demo 3.
- **Construction cannot withdraw an artifact.** A retirement with no successor is done by hand and recorded in the ledger.

### Next Session Should Start With
Get the user's browser check of the Demo 1 prototype. Then build Demo 2's read-only inspector path (`pgc-demo inspect`, `show`, `code`) before attempting the `set-limit` rebuild.

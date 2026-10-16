# SOTU Handoff

Only the current handoff is kept here. Earlier handoffs are in git history: `git log -p -- doc/SOTU.md`.

## SOTU Handoff — 2026-10-16 · demo is a script on v6; transport CLI; reproducible snapshot identity

### Changes Made
The demo runs on v6 only. v6 is a forward-only baseline. The demo adds no code: every step runs a PGC command, and each gap was fixed in the repo that owns it.

- **`pgc_install`** (committed `5dc8777` on local `dev/18`, not pushed):
  - `demo/pgc-demo.sh` — new. It runs only `pgc_transport`, `protocol_compiler`, `protocol_runtime`, `snapshot_assembler`, `si` and `python -m inspect`.
    - On first run it downloads the `v6` tag archives into `~/pgc-demo/v6/`.
    - `PGC_DEMO_WORKSPACE` points it at the workspace working trees and working snapshot instead.
    - Commands: `collatz [N | set-limit N | reset | tamper]`, `inspect [show FQDN | code MODULE]`, `where`.
  - `README_DEMO.md` — install is now `pipx install --include-deps protocol-governed-computing` plus `curl` of the script. Demo 2 uses the v6 facts: verify runs `CC_VERIFY_TERMINATION_V2`, 56 lines of code, about 490 lines of declarations.
  - `README_DEV.md` — the HTTP and command-line examples use `pgc_transport`. The passage saying transport is unpublished is gone.
  - `pyproject.toml`, `pgc/cli.py` — add `pgc-transport==5.0.0` to the family.
- **`protocol_transport`** (uncommitted):
  - `adapters/cli/__init__.py`, `adapters/cli/main.py` — new CLI adapter.
    - `pgc_transport call <operation> '<json>'` prints the canonical response. Exit status: 0 SUCCESS, 1 VIOLATION, 2 usage, 3 UNAUTHORIZED, 4 NOT_FOUND, 5 OPERATION_NOT_FOUND, 6 EXECUTION_FAILURE.
    - `pgc_transport http` serves the HTTP adapter.
    - The acid-test grep finds no domain names.
  - `pyproject.toml` — the distribution is now `pgc-transport`, with a static `version = "5.0.0"` and the console script `pgc_transport`.
  - `README.md` — gains a CLI section. `CLAUDE.md` (untracked) gains the layout and environment notes.
- **`protocol_compiler`** (uncommitted): `compiler/stages/s7_materialize.py` — new `_recorded()` helper.
  - Evidence `output_path`, `output_dir` and `files_written` are now relative to the declared output root.
  - Before, absolute build paths were sealed into `evidence_graph.json`, so the build folder changed the snapshot identity.
- **`conformance_workloads`** (uncommitted, Collatz client):
  - `web/collatz/index.html`, `js/collatz_bridge.js`, `css/collatz.css` — a text input with no browser check. A live diagram, with the trace's routes marked, replaces the PNG. `?n=27` plays a number on arrival.
  - `js/workflow_diagram.js` — new.
  - `client/README.md` — describes the new page.
- **`snapshot_inspector`** (uncommitted):
  - `client/web/workflow/` — new workflow map page (`index.html`, `js/workflow_map.js`, `js/workflow_diagram.js`, `css/workflow.css`).
    - It reads only through `si.behavior_logic.show`, `si.artifact.refs`, `si.artifact.show`, `si.artifact.list` and `si.snapshot.summary`, and builds no FQDN itself.
  - `client/web/index.html` — adds a card for the map.
  - `README.md` — gains a paragraph on the map.
- **`.github`** (pushed): `process/release.sh` — the comment now says transport publishes `pgc-transport`.
- **Deleted:** the workspace folder `pgc_demo/` and the `protocol-governed-computing-demo` wheel plan.

### Build & Test Status
PASSING.
- `regression.sh --all` on `dev/18`: 77/77, exit 0, run at the end of this session.
- The working snapshot is `bc46e17d…` and holds no absolute paths.
- Two rebuilds of the working snapshot gave the same identity.
- The same sources built in two different folders gave one identity (`a11f84d7…`).
- `pgc_env_check.py` passes, and transport is still not installed in the workspace venv.
- The demo script was run in workspace mode on every step:
  - 27 returns steps 111 and peak 9232; -5, 1000000 and `abc` are refused.
  - `set-limit 9999999` takes about 7.6 s the first time. 1000000 is then admitted, and a repeat build gives the same identity.
  - `reset`, `tamper` (refused at acceptance, naming the file), `show` and `code` all work.
  - Both pages were checked as headless Chrome screenshots.
- The `pgc-transport` wheel builds, and `entry_points.txt` names `pgc_transport`.
- Not tested:
  - Release mode, because the `v6` tags don't exist yet.
  - The regression after the transport and client changes. Those changes aren't covered by it.
  - The pages in a real browser.

### Open Issues
- **Uncommitted** on `dev/18`: `protocol_transport`, `protocol_compiler`, `conformance_workloads` and `snapshot_inspector`, as listed above.
- **`pgc_install`:**
  - Local `dev/18` has no remote branch.
  - Local and remote `main` are still `3dd64ef`. The earlier steps are still pending: `git branch -f main 9c1f9f1`, a `--force-with-lease` push of `main`, and pushing `v5`.
- **At the v6 cut:**
  - Upload `pgc-transport` to PyPI by hand.
  - Bump every `5.0.0`, including `pgc_install`'s pins.
  - Name `pgc-transport` in `process/notes/release-18.md`, which doesn't exist yet.
  - Run Zenodo `--verify`.
- **`workflow_diagram.js`** has two copies, `conformance_workloads/workloads/collatz/client/web/collatz/js/` and `snapshot_inspector/client/web/workflow/js/`. Change both together.
- **`README_DEMO.md` says verify reuses a platform transform.** That is true on dev/18 (`CT_PURE_REQUIRE_TRUE_V0`), but only while v6 keeps `CC_VERIFY_TERMINATION_V2`.
- **Carried from before:**
  - the TE output contract cannot declare `grounds` optional, so blockchain_identity is at 25/26;
  - 16 republished copies have drifted (advisory only);
  - 4 blockchain V0 contracts are stood down;
  - genesis G-2, G-3, G-4 and G-8 are open;
  - the flaky first `--all` is still unreproduced;
  - `pgc_sloc.py` skips `registry/schema/*.json`;
  - `parkinglot/` is gitignored in omnibachi-site.

### Architectural Concerns
- **Transport is now published but stays uninstalled in the workspace.** Its top-level packages, `adapters` and `resolver`, are generic names in site-packages. Decide before v6 whether to keep them or move them under a `pgc_transport` namespace.
- **The CLI adapter imports `to_canonical_request` from `adapters.http.binding`.** That function is protocol-neutral and could move to a shared module.
- **The demo's rebuilt snapshot is narrower:** platform, collatz and inspection only, under `GOVERNANCE_SURFACE_PROFILE_V0`. The published one carries every domain.
- **Versioning is still parked:** per-repo versions against `release.sh`'s lockstep, and whether `pgc_install` joins `REPOS`.
- **Where a rule lives:** the Collatz range is enforced only at the entrance. This is a candidate for Demo 3.

### Next Session Should Start With
Review and commit the four uncommitted repos on `dev/18`. Then open `bash pgc_install/demo/pgc-demo.sh collatz` and `inspect` in a real browser, in workspace mode (`PGC_DEMO_WORKSPACE`, plus a `pgc_transport` shim or an editable install of `protocol_transport` in a scratch venv).

# v5 readiness — the parking lot, triaged

v5 carries three things v4 did not have:
- the signed federated profile, run on a node group;
- composable molecules with visible internal state, including non-deterministic atoms that are
  recorded and replayed;
- `causal_language_model` as a fourth business domain.

There is no rush to publish. This is every item left open since v4, sorted by what it would cost to
leave it until later.

**The sorting rule.** Some items change what a snapshot's identity covers, or change many
artifacts. Each of those changes every composition id. A release is cited by its id, so those items
should all land before v5 is sealed and together, or wait for v6 together. Doing them one at a time
after v5 means a second round of re-pinning and a second deposit for each one.

---

## A. Identity-changing — decide for v5 or v6, as one batch

| # | Item | Source | Why it changes ids |
|---|---|---|---|
| A1 | **Profile content in the identity.** Today the snapshot id covers the profile's *name* only, so a profile can be weakened without changing the id of any snapshot claiming it. Move profiles out of `.github` into their own repo, require `PGC_SNAPSHOT_PROFILES`, and hash the profile's content into the identity. | SOTU, v4 "Queued for dev/18" | changes what the identity covers |
| A2 | **Handler namespace rename.** 89 handler-registry keys name `pgs_governance`, the retired namespace. It is behaviour-neutral but misleads readers, and it was explicitly deferred to v5. About 96 edits in one commit. | `doc/handler_namespace_rename.md` | every artifact carrying a key |
| A3 | **Replay classification.** An append-only store's clock-assigned `record_id` sits inside `detail`, which is classified determinative, so no replay of an appending act agrees on it. The CLM suite carries a named exception. Declare store-assigned content observational. | CLM CR-1 delivery | evidence classification vocabulary |
| A4 | **`moment: refusal` into the event artifact.** It is checked at P7 and rendered nowhere, so a sealed EV does not say it is a refusal. | CLM CR-1 | CLM's refusal events, renderer |
| A5 | **`SCHEMA_TRACE_EVENT_V0` lags the runtime.** The event enum does not list what the runtime writes. | SOTU, carried since dev/17 | schema artifact |
| A6 | **A common home for the three transform-wide rules.** Surface closure, derived closure and implementation admissibility sit in `CONSTITUTION_DETERMINISTIC_ATOMS_V0` for history's sake. This is option (b) of the rename. | this session | constitution artifacts |
| A8 | **The FEDERATED_NODE placement requires a store honouring POSIX record locks.** Capability correctness across workers depends on it; NFSv4 and local filesystems honour them, an object store does not. Ruled C4: declare it in the placement. | ruling C4 | placement declaration |
| A9 | **A trace records which contract ran, not which node.** CC and route events carry the CC address, never the node key. With one contract at several places, evidence does not say which place ran; it is recoverable only by replaying the routing. The execution-path overlay stops at the first reused contract for the same reason. Record the node key in `CC_START` and `WF_ROUTE`, then walk the overlay by key. Changes the trace schema, with A5. | found in B19 | trace schema, determinative content |
| A7 | **`cryptographic_trust` V1.** Signing is selected by the composition, not carried by the surface. Declarations only; the selector is pre-wired. | SOTU "Still owed" | trust declarations |

**Recommendation:** take A1–A5 into v5, and A6–A7 too if they stay small. A1 is the one that matters
for a citable release: a deposit whose id does not cover the profile it claims can have its
profile weakened without anyone seeing it.

---

## B. Defects and gaps — fix before v5, none changes the platform's identity alone

| # | Item | Size |
|---|---|---|
| B1 | ~~`governance_surface_map.yaml` is stale~~ — **done**: regenerated, 195 artifacts; the generator's leftover `execution/<envelope|semantics>` special case is removed | small |
| B2 | ~~`software_governance/CLAUDE.md` says the repo holds no implementation code~~ — **done**; the file is gitignored, so the correction is on disk only | trivial |
| B3 | ~~`test_workflow_execution.py`: 2 failures, `TraceWriter` without its snapshot args~~ — **done**, 7/7; still not in the regression | trivial |
| B4 | ~~`tc construction emit --help` is stale about manifest creation~~ — **done** | trivial |
| B5 | ~~P7 does not check that vector-case YAML parses~~ — **done**: `TEST_VALUE_UNPARSEABLE` (P7 now 235 rules), sealed; `vector_value_design_test` 3/3, `vector_design_test` 6/6 | small |
| B6 | ~~False positive in `TOPOLOGY_ROUTE_RESOLVES`~~ — **done** (wave 2): `si.behavior_logic.list` rows carry `nodes`; P7 observes them, and a route to a place the composed workflow already has resolves. cr_03 row 3 no longer fires. **Not a blockchain defect: a false positive in `TOPOLOGY_ROUTE_RESOLVES`.** The rule resolves a routing target only against the dossier's own rows, so an amendment that routes to an existing, unchanged node is flagged (blockchain cr_03 row 3; the workflow artifact is correct). Fix: resolve also against the workflow's nodes in the pinned composition. The published graphs carry node keys, but no observation exposes them yet: it needs a node list on `si.behavior_logic.list` (a governed inspection surface) and a P7 observation. Changes the transformation and inspection domains, so it joins batch A. | medium |
| B7 | **Confirmed, and wider.** Dossiers declaring event fields as ATTRIBUTE have them silently dropped by the renderer: `EV_WALLET_CREATED_V0` is sealed with only a default `timestamp`, not `wallet_id`, `holder`, `occurred_at`; blockchain cr_01's identity events follow the same pattern. The fix is a renderer or rule change plus re-rendering delivered events, and possibly what the runtime validates on announcement. Changes domain artifacts, so it joins batch A. | medium |
| B8 | book catalog's `VALIDATE_RECORD_STRUCTURE` never refuses | small, needs a ruling |
| B9 | blockchain identity takes its admitted states from the caller, the hole cr_04 closed for wallet | small CR |
| B10 | ai_governance's inherited vectors disagree with PGC (`CHECK_QUOTA_AVAILABLE`, `CHECK_TRAINING_STATUS`, `EVALUATE_INACTIVITY`) | needs a business ruling, own CR |
| B11 | **Two compositions can overwrite each other's output:** the output root is not declared by the build. Its fix declares the root in each build configuration, a governed artifact, so it **moves to batch A**. | medium, `doc/composition_output_root.md` |
| B12 | **A superseded artifact stays in force.** The full fix is an `in_force` predicate declared in the surface plus an invariant that every effect-conferring path consults it, so it **moves to batch A**. A code-only first step — no assertion derived from a superseded invariant — changes nothing today, because none exists. | medium, `doc/supersession_and_force.md` |
| B13 | ~~Runbook expectations as data, with an unexpected-pass check~~ — **done**: `expectations.yaml` (52 steps, counts exact), `regression_verdict.py`, `test_regression_verdict.py` 8/8; RUNBOOK "## Expected" brought up to date and pointed at the data | small–medium |
| B14 | ~~`publish_component_releases.sh` adopted into `.github/process/`~~ — **done**, rewritten (the staged copy was lost). Refuses unless Zenodo answers and every component has a release webhook; skips components already released; reads the component list from `compose_release.py`. `--verify` checked against v4: 9/9. The publish path runs for the first time at v5. | small |
| B15 | ~~Two `pgc_install/README.md` gaps~~ — **done**: the Machine-block health advisory is documented; the second gap, compile writing into the clone, was already covered in §4. Its V1 build-configuration names are right for the published v4 install and change with v5 (F). | small |
| B16 | ~~Rulings and doctrine live only in gitignored `CLAUDE.md` files~~ — **done**: rulings are mirrored into `.github/process/rulings.md`, which is versioned | trivial |
| B17 | `SIGNED_FEDERATED_MULTINODE_PROFILE_V0` exists twice: operational in `.github`, illustrative in `standards`. **Deferred** to the next standards revision; `standards` is frozen. | trivial |
| B19 | ~~`behavior-logic` reads `PGS_WORKSPACE`~~ — **done, and it was broken, not just misnamed**: it looked for graphs in the RI-0 layout. It now takes `--snapshot` / `PGC_SNAPSHOT_ROOT` and reads `behavior_logic/<domain>/<WF>/`; `run --behavior-logic` was fixed with it. | trivial |
| B20 | ~~`regression.sh` exits 0 on a failing test script~~ — **done**: every check and execution step runs through `step`, and the script exits with the verdict | small–medium |
| B21 | `pgc_runtime examine` parses RI-0's trace format (`execution_start`, `node_start`, `sequence`, …) and pins `TRACE_SCHEMA_V0`. It cannot read a PGC trace, the way `behavior-logic` could not (B19). | small–medium |
| B22 | `SCHEMA_EVENT_V0` is never applied — EVENT is `described` in `STRUCTURE_SCHEMA_DISPATCH_V0` but absent from its dispatch — and it is stale: its `governed_by` constant and `$id` (`pgs_governance.schemas…`) match no event. Rewrite it from what events carry (with `core.moment`) and dispatch it, or record the disposition truthfully. Changes a governed artifact, so it goes with batch A. | small–medium |
| B18 | Transform conformance: 16 domain transforms unproven, and implementation source not sealed by hash. **Frozen by decision**, so record it, don't fix it. | none |

---

## C. Decisions — ruled

Each ruling is recorded in `.github/process/rulings.md`.

| # | Item | Ruling |
|---|---|---|
| C1 | P7 is generated by a script outside governance (lesson 3) | **Stated limit for v5.** A dossier is admitted on what it says. A generated dossier keeps its generator as evidence and says so in its `delivery.md`; CLM's now does. Governed generation is v6. Written into `transformation/CLAUDE.md`. |
| C2 | `runtime.api` reads `PGC_COORDINATOR_URL` | **Conforming: deployment configuration.** The sealed placement decides; the environment supplies only an address. Written into `protocol_runtime/CLAUDE.md`. |
| C3 | Runtime built-in defaults: bind, port, connect timeout, poll interval | **Conforming: deployment configuration.** They are gathered, documented and overridable in `runtime/federation/defaults.py`; loopback by default is a safety property. Federation tests 11/11. |
| C4 | Capability correctness depends on POSIX record locks | **Declare it in the FEDERATED_NODE placement.** Moved into batch A as A8. |
| C5 | The EO-2 residual: admission unknown after a dropped connection | **Stated limit for v5.** A unit idempotency key with an admission-status query is v6 design work. Record it in the release notes. |

---

## D. Deployment and operations — record in the release notes, not blocking

- The SSH exception to EO-4.
- `EVIDENCE_EXPIRY` not exercised over the shared store.
- Cross-node concurrency only lightly exercised.
- Two orphaned barcode claims kept as evidence.
- The evidence store is not external to every node.
- `shuttle` LXD start/stop priorities not set.
- The stale `/etc/hosts` line on the Mac.

---

## E. Only someone else can close these

- **A second reader** (§6 externality). No read-back by the author mends it.
- **The profile read-back by hand** for the signed federated profile. The author can do it, but it
  is still one reader.

---

## F. Documentation refresh for v5

- **Org profile** (`.github/profile/README.md`): four business domains, the signed federated
  profile, molecules and non-deterministic atoms, CLM.
- **Every repo's `README.md` and `ARCHITECTURE.md`.** `business_domains` and `snapshot_assembler`
  are done. The rest need a pass for:
  - domain counts;
  - the constitution rename;
  - keyed nodes and node-keyed routing;
  - S8 dispatch fidelity;
  - the signed federated profile.
- **Canonical docs:** the three transform constitutions, and the placement and profile docs.
- **`.github/process/notes/release-17.md`,** and a `pgc_release/MANIFEST.md` for v5.
- **The papers:** anything citing v4 behaviour that v5 changes. Molecules, the constitution rename
  and routing by node are the likely ones.

---

## Suggested order

1. **Rule on C1–C5.** Some rulings move items into A or B.
2. **Do B, the cheap ones first.** They change no platform identity, and each is visible in the
   regression.
3. **Take the A batch in one pass,** then one clean regression and one re-pin of every dossier
   baseline that still runs phases.
4. **Refresh the documentation (F)** against the final composition.
5. **Write the release notes,** record D and E as stated limits, and cut v5.

---

## The A batch — plan

**Wave 2 done:** B6. **Wave 1 done, with B7:** A9, A5, A3, A4 and the ATTRIBUTE fix; `regression.sh --all` 53/53. Rulings: handler keys → `pgc_governance.handlers.*`; the renderer honours ATTRIBUTE on events; the transform-wide rules → `CONSTITUTION_CAPABILITY_TRANSFORMS_V1`. A1's home is still to be ruled.

Everything that changes a composition id lands here, together, then one clean regression and one
re-pin. It runs in four waves, each ending with a green `regression.sh --all`, so a failure is
traced to one wave rather than to the batch.

| Wave | Items | Repos | What changes |
|---|---|---|---|
| **1 — evidence** | A5, A9, A3, A4 | protocol_runtime, software_governance, transformation, business_domains | **A9:** `CC_START` and `WF_ROUTE` carry the node key. **A5:** `SCHEMA_TRACE_EVENT` lists what the runtime writes. **A3:** store-assigned content (`record_id` and the store's timestamp) is declared observational in the evidence classification, and replay honours it, so CLM's named exception is dropped. **A4:** `moment: refusal` is rendered into the EV artifact. |
| **2 — design and construction** | B6, B7 | snapshot_inspector, transformation, business_domains | **B6:** `si.behavior_logic.list` publishes node keys; P7 observes them; `TOPOLOGY_ROUTE_RESOLVES` accepts a route to an existing node. **B7:** event fields declared ATTRIBUTE reach the sealed event — approach to be ruled; blockchain's events re-rendered. |
| **3 — governance surface** | A2, A6, A8, A7, A11 (B12), A10 (B11) | software_governance, protocol_compiler, all domains' build configs | **A2:** the 89 handler keys renamed. **A6:** the three transform-wide rules move to a common home. **A8:** FEDERATED_NODE declares the record-lock requirement. **A7:** `cryptographic_trust` V1, signing selected by composition. **A11:** an `in_force` predicate, applied where presence confers effect, and the invariant that checks it. **A10:** each build configuration declares its output root; two naming one root are refused. |
| **4 — identity** | A1 | snapshot_assembler, .github (or a new profiles repo), protocol_runtime | The snapshot identity covers the profile's **content**, not only its name. `PGC_SNAPSHOT_PROFILES` becomes required. Last, because every earlier wave changes ids anyway and this one changes what an id means. |

**Then:** one clean regression, `expectations.yaml` updated for every count that moved (with
reasons), every dossier baseline that still runs phases re-pinned by the side-assembly recipe, and
the SOTU.

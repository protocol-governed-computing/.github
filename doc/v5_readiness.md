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
| A7 | **`cryptographic_trust` V1.** Signing is selected by the composition, not carried by the surface. Declarations only; the selector is pre-wired. | SOTU "Still owed" | trust declarations |

**Recommendation:** take A1–A5 into v5, and A6–A7 too if they stay small. A1 is the one that matters
for a citable release: a deposit whose id does not cover the profile it claims can have its
profile weakened without anyone seeing it.

---

## B. Defects and gaps — fix before v5, none changes the platform's identity alone

| # | Item | Size |
|---|---|---|
| B1 | `software_governance/surface_map/governance_surface_map.yaml` is stale throughout | small–medium |
| B2 | ~~`software_governance/CLAUDE.md` says the repo holds no implementation code~~ — **done**; the file is gitignored, so the correction is on disk only | trivial |
| B3 | ~~`test_workflow_execution.py`: 2 failures, `TraceWriter` without its snapshot args~~ — **done**, 7/7; still not in the regression | trivial |
| B4 | ~~`tc construction emit --help` is stale about manifest creation~~ — **done** | trivial |
| B5 | P7 does not check that vector-case YAML parses | small (one rule) |
| B6 | blockchain cr_03's delivered route defect | small |
| B7 | blockchain cr_04's EV fields declared as ATTRIBUTE, which the renderer ignores | small |
| B8 | book catalog's `VALIDATE_RECORD_STRUCTURE` never refuses | small, needs a ruling |
| B9 | blockchain identity takes its admitted states from the caller, the hole cr_04 closed for wallet | small CR |
| B10 | ai_governance's inherited vectors disagree with PGC (`CHECK_QUOTA_AVAILABLE`, `CHECK_TRAINING_STATUS`, `EVALUATE_INACTIVITY`) | needs a business ruling, own CR |
| B11 | **Two compositions can overwrite each other's output:** the output root is not declared by the build | medium, `doc/composition_output_root.md` |
| B12 | **A superseded artifact stays in force:** a defect in the family's model | medium, `doc/supersession_and_force.md` |
| B13 | Runbook expectations as data, with an unexpected-pass check | small–medium |
| B14 | `publish_component_releases.sh` adopted into `.github/process/` | small |
| B15 | Two `pgc_install/README.md` gaps from the newcomer install test, and it still names V1 platform build declarations | small |
| B16 | `transformation/CLAUDE.md` is gitignored, so lessons 2 and 4 are unversioned | trivial, decide where they live |
| B17 | `SIGNED_FEDERATED_MULTINODE_PROFILE_V0` exists twice: operational in `.github`, illustrative in `standards`. The illustrative copy should say so. | trivial |
| B19 | `runtime/cli.py` `behavior-logic` reads `PGS_WORKSPACE`, a legacy RI-0 environment name | trivial |
| B18 | Transform conformance: 16 domain transforms unproven, and implementation source not sealed by hash. **Frozen by decision**, so record it, don't fix it. | none |

---

## C. Decisions — ruled

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

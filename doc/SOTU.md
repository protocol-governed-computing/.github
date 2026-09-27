# SOTU Handoff

## Conformance frozen: kept, no backfill; CLM merge next — dev/17 · 2026-09-27

`platform_test_data` is delivered and closed: the platform proves its own transforms in each of its
three builds. Then transform conformance was **frozen by decision, not left open**. All repos are
committed.

### The decision: keep and freeze

After two platform dossiers and the start of a third, the business author asked whether conformance
was worth its cost. No vector has caught a bug in a transform's code; the defects it found were in
the conformance machinery itself, and the execution validations already exercise every transform
through real workflows. So:

- **Kept, and not rolled back.**
  - Every build runs its vectors after the compile.
  - The platform's 12 transforms are checked on every build: 11 proven and 1 unproven,
    `COMPARE_EQUAL`.
  - P7 requires cases for every transform a design authors or amends.
  - Molecules are proven from recorded results, which CLM needs.
  - The rules over vectors no longer report PASSED while judging nothing.
  - The net cost is about 1,100 lines of code and tests across 6 repos.
- **Rolling back was rejected.** Back to dormant restores rules that report PASSED over nothing.
  Removing conformance entirely is a bigger change, and leaves no check per transform.
- **Skipped, by decision and not as open items:**
  - backfilling domain vectors: 16 domain transforms stay unproven until their domain next changes
    them, as P7 already requires;
  - the `vector_backfill` path. Today a domain can give vectors only to a transform its design
    authors or amends, and constitution V2 §5 says so;
  - the ai_governance CR. Its inherited vectors were stale, not a drift in behaviour: the three
    transforms declare `refusal: raises` on purpose;
  - a vector for `COMPARE_EQUAL`;
  - sealing the implementation's source by hash;
  - the Collatz declared-iteration dossier. CLM's `model_response` supplies the in-composition
    evidence for a molecule. That relaxes the earlier ruling that the evidence must not come from a
    domain that needs it.
- **If P7's vector rule ever feels bureaucratic,** downgrade that one rule to a warning. Do not roll
  back.

### What `platform_test_data` delivered

- **Governance:** `CONSTITUTION_TEST_DATA_V2`, `SCHEMA_TEST_DATA_V1` and
  `STRUCTURE_BUILD_PLATFORM_{,FEDERATED_,MULTIWORKER_}CONFIG_V2`. The V1s, and schema V0, were deleted.
- **Vectors:** 11 in `capability_transforms/registry/test_data/`. All 49 inherited cases were kept.
- **Compiler:**
  - vectors are written as canonical declarations: the snapshot grew from 421 to 432 artifacts, and
    `si artifact list --kind TEST_DATA` lists them;
  - the attestation records `imported_capabilities`;
  - `compile.sh` runs the platform's conformance.
- **Runner:**
  - a build's own and carried transforms are read from its attestation, never from a name;
  - any failed case refuses its build;
  - it takes `--snapshot-root` and `--structure`.

### Build & Test Status

**PASSING.** Regression `--all` is green except `admission_contract_fidelity` (31, expected). Every
build prints its `[conformance]` line: the RUNBOOK has the platform line, three times, and every
domain's.

### Open Issues

1. **Three documents still name the V1 platform build declarations:**
   - `pgc_install/README.md`, which is main-only;
   - `standards/profile_authoring/README.md`, frozen with draft-3;
   - `governance_surface_map.yaml`, which is stale throughout.
2. **Still carried from earlier:**
   - the `SCHEMA_TRACE_EVENT_V0` enum lags the runtime;
   - the CLM CR-1 rebaseline notes: overturn P3 #2, move GAP-09 to REUSE, revisit the trace
     constraint.

### Next Session Should Start With

1. Merge dev/17 → work/clm.
2. The CLM CR-1 rebaseline: re-pin against the merged composition, overturn P3 #2, move GAP-09 to
   REUSE, and revisit the trace constraint.
3. Resume CLM at P7. P7 now requires cases for each transform it authors, with recorded results for
   the non-deterministic step.

---

## Transform conformance delivered; platform test data next — dev/17 · 2026-09-26

`transform_conformance` is delivered in six steps. Steps 1–5 are committed. **Uncommitted:**
- `transformation`, step 6: P7 `test_cases` and `test_case_values` registers, the vector rules (P7
  has 232 rules), the TEST_DATA companion family and renderer, fixture and corpus cases, and
  `vector_design_test`.
- `.github`: the RUNBOOK conformance section and test rows, plus `vector_design_test` in the regression.
- `software_governance`: `dossiers/transform_conformance/{delivery,closure}.md`, and the new
  `dossiers/platform_test_data/p0_business_problem_statement.md`.

### Build & Test Status

**PASSING.** Regression `--all` is green except `admission_contract_fidelity` (31, expected).
Construction acceptance reproduces 99/99 and lists 4 vectors as NOT YET DELIVERED.

Every domain build now runs conformance after its compile succeeds. The baseline, as proven /
unproven / refused / carried:

| Domain | Proven | Unproven | Refused | Carried |
|---|---|---|---|---|
| workload | 0 | 2 | 0 | 0 |
| transformation | 0 | 6 | 0 | 0 |
| inspection | 0 | 0 | 0 | 0 |
| ai_governance | 0 | 3 | 0 | 4 |
| book_library_mgmt | 0 | 4 | 0 | 5 |
| blockchain | 0 | 1 | 0 | 6 |

### Open Issues

1. **No transform is proven yet.** The platform transforms that domains carry are proven nowhere.
2. **The implementation's source is not sealed by a hash.** Two P7 refinements are also missing:
   a value's case is matched per register rather than per transform, and cell normalization reaches
   values.
3. **The ai_governance vectors inherited from RI-0 disagree with PGC.** This covers
   `CHECK_QUOTA_AVAILABLE`, `CHECK_TRAINING_STATUS` and `EVALUATE_INACTIVITY`: RI-0 answered "no"
   where PGC refuses, and one output was renamed. It needs a business ruling in its own CR.
4. **Still carried from earlier:**
   - the `SCHEMA_TRACE_EVENT_V0` enum lags the runtime;
   - `governance_surface_map.yaml` is stale;
   - the CLM CR-1 rebaseline notes: overturn P3 #2, move GAP-09 to REUSE, revisit the trace constraint.

### Next Session Should Start With

1. **Gate 0 for `software_governance/dossiers/platform_test_data`.** The P0 is written and has four
   clarifications with recommended answers. It lifts RI-0's vectors for 11 platform transforms
   into the Machine-block format and runs them in a new workload in `conformance_workloads`.
   - A read-only drift check found 10 of the 11 match on every case.
   - `PASSTHROUGH` is unconfirmed until the first compile.
2. Then the `ai_governance` CR for its 3 vectors.
3. Then Collatz declared iteration: the first molecule proven in a composition.
4. Then merge dev/17 → work/clm, run the CLM CR-1 rebaseline, and resume CLM at P7.

---

## Session close: shuttle powered off — dev/17 · 2026-09-25

No code changed after the previous entry. All four repos are committed and clean:
`.github` `bfb459c`, `software_governance` `3819279`, `protocol_runtime` `1a4112b`,
`protocol_transport` `bcc1871`.

### Build & Test Status

**PASSING.** Regression `--all` re-run at close: exit 0, 135 OK, `test_federation` 11/11,
`test_capability_concurrency` 3/3.

### Open Issues

1. **`shuttle` is powered off, with the node group on it.** Whether UC221–UC224 were stopped before
   UC220 is not recorded. If they were not, the host's shutdown could have waited on their `hard`
   NFS mounts; check the next boot came up cleanly.
2. **Power-up ordering is not set.** LXD restarts instances without order. A node that starts before
   the UC220 VM serves NFS fails `srv-pgc-data.mount`, and its `pgc-<role>` service fails with it
   and is not retried. After power-up, check `findmnt /srv/pgc/data` and `systemctl is-active pgc-*`
   on each node; if either failed, `sudo systemctl restart srv-pgc-data.mount pgc-<role>` in the
   start order coordinator → workers → boundary. The lasting fix is two `lxc config set` lines:
   `boot.autostart.priority=100` and `boot.autostart.delay=30` on UC220, and `boot.stop.priority=10`
   on UC221–UC224.
3. The open issues of the two entries below stand.

### Architectural Concerns

None beyond those recorded below.

### Next Session Should Start With

If the node group is needed again: power on `shuttle`, set the LXD start/stop priorities, and check
each node's mount and service. Otherwise the signed federated testing is wrapped and nothing
waits on the testbed.

---

## A stateful domain on the node group; signed federated testing wrapped — dev/17 · 2026-09-25

The stateful run the previous entry named as next is done, and with it the testbed work on
`SIGNED_FEDERATED_MULTINODE_PROFILE_V0` is wrapped. The profile did what it was built for: every
demonstration could fail, and three found real defects, each now fixed.

```
snapshot     641dc40e465b7885…  (platform, workload, inspection, book_library_mgmt; 274 artifacts)
catalog      23/23 criteria through the node group, units alternating workers
concurrency  20 concurrent copy registrations → 20 records (was 18 of 20 reported SUCCESS)
regression   exit=0, 135 OK, test_federation 11/11, test_capability_concurrency 3/3
```

### Changes Made

- `software_governance/capability_side_effects/implementation/store_lock.py` — new: one writer per
  store across threads, processes and hosts; POSIX record lock on a hidden sidecar (`.<store>.lock`)
- `…/CS_MUTABLE_JSON_V0/impl/executor.py` — thread lock replaced by `store_lock` on every mutation
- `…/CS_REGISTRY_V0/impl/backend.py` — `register`, `deregister` check-and-append under `store_lock`
- `…/CS_APPENDONLY_JSONL_V0/impl/executor.py` — count-and-append under `store_lock`
- `protocol_runtime/testbed/pgc/test_capability_concurrency.py` — eight separate processes race
  each store; fails on the old code (148 of 200 updates lost, duplicate sequence numbers)
- `.github/process/regression.sh` — runs it
- `.github/process/deploy/NODE_CONFIG.md` — store mount `hard,_netdev,lookupcache=none,actimeo=0`
- `.github/doc/profile_readback_signed_federated.md` — section on the stateful domain; conclusion
  now records three defects
- On the nodes: the book snapshot, `pgc-domains` and the new `pgc-governance` wheel installed;
  mount options changed; previous snapshot kept at `/opt/pgc/snapshot.347be174`

### Build & Test Status

**PASSING.** Regression `--all` exit 0, 135 OK, every domain's criteria hold (catalog 23/23),
`test_federation` 11/11, `test_capability_concurrency` 3/3.

### Open Issues

1. **§6 externality** — unchanged; only a second reader closes it.
2. **Cross-node concurrency on the group was lightly exercised** — the final race placed 19 of 20
   units on one worker. The eight-process race is the stronger evidence.
3. **The store holds two orphaned claims** — `BC-UNI-08`, `BC-UNI-14` are in the barcode registry
   with no copy record, left by the lost-update run and kept as its evidence. A fresh catalog run
   needs a fresh store.
4. **`software_governance/CLAUDE.md` says the repo holds no implementation code**; it holds the
   capability implementations the workers run. The doctrine file is stale.
5. From the previous entry, still open: the SSH exception to EO-4, the EO-2 ambiguous-admission
   case, `EVIDENCE_EXPIRY` over the shared store, the runtime's built-in defaults, the stale
   `/etc/hosts` line on the Mac.

### Architectural Concerns

- **A capability's correctness now depends on the store honouring POSIX record locks.** NFSv4 and
  local filesystems do; an object store would not. That constraint belongs in the placement or
  capability declarations rather than only in code.

### Next Session Should Start With

Testing is wrapped. Decide what to record of the three defects outside this repo — the stale-read
and lost-update findings apply to any multi-writer placement, not only this deployment.

---

## The federated node group runs, configured by hand — dev/17 · 2026-09-25

`FEDERATED_NODE` has a realization, a deployment, and a read-back against it. The composition built
from `STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V1` runs on four LXC nodes on `shuttle`, its evidence
in a VM none of them is, signed on the Mac and nowhere else. Every node was configured by hand.

```
snapshot_id  347be1741d7a1191bf7863462d4ec41340a33e2de7375c8c51145a59a3b201d4
signed under e5f15d7a0173e70a    ~/.pgc/federated/sign.pem — Mac only, mode 600
UC221 boundary :8000 · UC222 coordinator :8100 · UC223, UC224 workers · UC220 VM store (NFSv4)
read-back    OB-1…5 hold · EO-1…6 hold · OB-5/EO-4 with an SSH exception · §6 not satisfied
regression   exit=0, 135 OK, test_federation 11/11, closures passing
```

### Changes Made

**protocol_runtime** — `4b8aa51`, `4dd9889`
- `runtime/federation/{store,coordinator,worker,client}.py` — the `FEDERATED_NODE` realization: a
  coordinator that queues and never executes, workers that claim by exclusive creation and run
  `run_workflow` unchanged, all meeting only at the store
- `runtime/api.py` — `invoke_workflow`: submits to `PGC_COORDINATOR_URL` under `FEDERATED_NODE`,
  runs in place otherwise; no timeout
- `runtime/cli.py` — `coordinator`, `worker` subcommands
- `runtime/federation/client.py` (EO-2) — connect bounded, answer unbounded; after admission the
  outcome is awaited without limit, through coordinator restarts; failure only when nothing was admitted
- `testbed/pgc/test_federation.py` — 11 cases, three of them for EO-2

**protocol_transport** — `bcc1871`
- `resolver/resolver.py` calls `runtime.api.invoke_workflow`; `adapters/http/server.py` gains
  `PGC_HTTP_BIND`; `run_http.sh`, `README.md` document both

**.github** — `1046e43`, `f59f329`
- `process/deploy/PLAN.md` — topology, phases, the §5 checks, risks
- `process/deploy/NODE_CONFIG.md` — the end configuration of every machine and the manual recipe
- `process/regression.sh` runs `test_federation.py`; `process/RUNBOOK.md` gains the third composition
- `doc/profile_readback_signed_federated.md` — read back against this deployment

**Outside git**
- `shuttle`: UC220 is an LXD VM (MAC `…:02:20`) exporting `/srv/pgc/data`; UC221–224 rebuilt fresh
  and configured by hand; all five have `bp` with the Mac's and shuttle's keys, `sudo` on UC221–224
- Mac: `~/.pgc/federated/{sign.pem,trust.pub}`; `/etc/hosts` still has a stale `192.168.1.200 shuttle`
- Deploy scripts were written, used, and deleted in favour of manual configuration; they are not in git

### Build & Test Status

**PASSING.** Regression `--all` exit 0, 135 OK, governance and implementation closures passing,
`test_federation` 11/11. On the live group, every §5 check was run by hand:

| Check | Result |
|---|---|
| OB-1 | altered signature refused at authentication |
| OB-2 | signing key absent everywhere, by hash; signing code present, key withheld |
| OB-3 | UC223 stopped; its traces intact on UC220; UC224 served alone; UC223 rejoined unaided |
| OB-4 / EO-5 | a begun unit never re-run, also after a worker restart; unstarted work moved |
| EO-1 | four addresses, one role each, one `snapshot_id` everywhere |
| EO-2 | worker refuses without coordinator or store; a request during a store outage waited and returned SUCCESS |
| EO-4 | from outside only UC221:8000 and admin SSH answer; all else dropped |
| EO-6 | eight runs of one payload, both workers, one surface hash `21488c857a130358` |

### Open Issues

1. **§6 externality** — a read-back by the author. Only a second reader closes it.
2. **SSH exception to EO-4** — the Mac (`.75`) and shuttle (`.201`) reach port 22 on all five
   machines. A non-admin LAN host was not probed.
3. **EO-2 residual** — a connection lost after a unit is sent and before the coordinator answers
   leaves admission unknown; the error says so, and nothing resolves it.
4. **`EVIDENCE_EXPIRY`** has not been exercised over the shared store.
5. **Stateful domains** — two workers share one `data_root`; concurrent units against the same
   capability state are serialized only by what each capability does. Only `collatz` has run.
6. **Stale `/etc/hosts` line** on the Mac (`192.168.1.200 shuttle`) makes `ping shuttle` fail.
7. **Built-in defaults** in the runtime (coordinator port 8100, loopback bind, 10 s connect bound)
   against the runtime doctrine's "no magic constants" — flagged, not decided.

### Architectural Concerns

- **`runtime.api` consults placement.** `invoke_workflow` branches on the sealed placement mode and
  reads `PGC_COORDINATOR_URL`. It decides where `run_workflow` is called, not how execution proceeds,
  so placement §4 holds — but it is the first runtime entry point to consult placement, and the
  runtime doctrine forbids environment-driven branching. It reads an address, not a branch. Worth a ruling.
- **The boundary authenticates per request**, not at start, so its boot log has no trust-root line.
- **Privileged nodes share the host kernel.** Node isolation from the host is not claimed; abrupt
  node loss wedges the host's NFS client. Nodes are stopped, never force-deleted, while mounted.

### Next Session Should Start With

Decide whether to run a stateful domain on the node group — it is the first thing that can break a
determination across workers, and only `collatz`, which holds no state, has run. Read how
`book_library_mgmt`'s capabilities write under `{{module_data_root}}` before sending it a unit.

---

## FEDERATED_NODE authorized — the deployment has a composition — dev/17

Declarations and one deletion. No compiler change, which is what the selector generalization was
for.

### What was added

`CONSTITUTION_EXECUTION_PLACEMENT_V1` §1 now authorizes three modes, and §5a says what the third
permits: several separately addressable nodes under **one** authority, work reaching a node across a
network, and a node executing a topology it did not receive from a caller. It does not permit a
second authority — *a node is where execution happens; it is not a party that determines anything,
and its refusal is the one authority refusing, reached on that node.*

```
single-node    LOCAL_SINGLE_NODE    cross_node=False
multi-worker   LOCAL_MULTI_WORKER   cross_node=False
federated      FEDERATED_NODE       cross_node=True
```

Three compositions from one surface, each carrying the arrangement its build named.
`STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V1` assembles, signs and boots:

```
snapshot_id  347be1741d7a1191bf7863462d4ec41340a33e2de7375c8c51145a59a3b201d4
composition  PASSED (5 rules over 212 artifacts)
boot         Authenticated under trust root, healthy
regression   exit=0, 135 OK, governance closure passing
```

### The line that decides the deployment

**The distinction from `LOCAL_MULTI_WORKER` is reachability, not count.** Workers in processes are
not addressable at any host count, and the mode forbids cross-node dispatch outright — so a
`LOCAL_MULTI_WORKER` composition can never satisfy EO-1, on any number of hosts. That is sharper
than the read-back's "not satisfied", which recorded the deployment rather than the impossibility.

`FEDERATED_NODE` is what an environment profile requiring addressable nodes can be met under. The
LXC work now has a composition to deploy.

### Three judgments

**V1 was amended in place, not superseded by a V2.** Governance §3.3 makes versions immutable *once
ratified*; nothing on `dev/17` is ratified. V1 ships once carrying three modes rather than shipping
as V1 and immediately again as V2.

**`REMOTE_WORKER_POOL` was skipped, and §6 says so rather than jumping silently.** A pool is a set of
interchangeable executors behind one address; a node group is addressable participants with declared
roles. The profile names roles, so the pool is not on the path to it. The cost is recorded: nothing
here has been demonstrated against an arrangement where executors are anonymous.

**The duplicated authorization was removed.** Generalizing the selector argued that stating the
authorized set twice creates two places for it to disagree, and then left `AUTHORIZED_MODES` in the
placement handler. There is now no copy anywhere in the compiler. The set exists in the constitution
and in the structures declaring it, and authorization is enforced where it can only be stated once —
a mode no structure declares resolves to nothing at selection and the build refuses.

### Two things now stale

1. **The read-back is against the multi-worker snapshot.** `doc/profile_readback_signed_federated.md`
   records EO-1 as not satisfied by that deployment; against a federated composition the entry
   should be re-read, and it remains not satisfied until there are hosts.
2. **The RUNBOOK table lists two compositions**, not three.

Neither is wrong, both are behind.

### Where this leaves the platform

Everything the profile says about meaning holds. Everything it says about placement now has a
composition that *can* satisfy it and a deployment that does not yet exist. The next move is
`shuttle`: four nodes, an evidence store held by none of them, a build machine outside the group.
That closes OB-2, OB-3, EO-1, EO-3 and EO-4 together, because they have one cause.

The item nothing here can close remains a second reader.

---

## The read-back — the profile answered its own question

The work the whole exercise was set up to produce, and the one piece no tool performs. Recorded in
`doc/profile_readback_signed_federated.md` against snapshot
`f899c0d8ba6ff6e0b2fa76eb43cfb3010e2095ab44b696d0c37f456aacaa3466`.

### Result

```
§1 selections          Holds — 7 of 7
§2 required artifacts  Holds — 11 of 11
§3 obligations         2 Hold · 2 Not satisfied · 1 Not testable here
§4 claims              5 of 5 discharged
§5 derivation          Holds
§6 externality         Not satisfied
EO-1 … EO-6            2 Hold · 1 Partial · 2 Not satisfied · 1 Not testable here
```

**Five unmet obligations, one cause.** OB-2, OB-3, EO-1, EO-3 and EO-4 are about a deployment of
several nodes, and there is one host. Nothing about the platform prevents meeting them and nothing
about this deployment meets them. The composition satisfies what the platform *means*; the
deployment does not satisfy where it *runs*. That split is the finding, and it is the expected one.

### Every claim was demonstrated, and one demonstration was invalid

All five ran against the composition and all five could have failed.

- `SNAPSHOT_IMMUTABILITY` — a constituent altered; refused at acceptance naming the file and both
  hashes.
- `DETERMINISTIC_EXECUTION` — one workflow and payload across four worker processes; four identical
  determinations. This tests SM-10 *across workers*, which a single-process platform cannot exercise
  at all.
- `COMPILED_INVOCATION_RESOLUTION` — a workflow the dispatch table does not name refused with
  `WF FQDN not in vocab`.
- `SIGNED_SNAPSHOT_VERIFICATION` — an anchored node refused an unverifiable signature; an unanchored
  node booted the same snapshot.
- `EVIDENCE_EXPIRY` — evidence past the window ended with its attestation, evidence within it
  survived, the deletion recorded to an append-only stream.

**The first attempt at the signature demonstration was invalid, and the read-back records it.** It
corrupted a signature on an already-tampered snapshot, so acceptance refused before authentication
ran — a signature refusal would have been reported that never happened. A demonstration that cannot
isolate what it claims to test establishes nothing. Re-run on an intact snapshot.

### What the reading found beyond the verdicts

**§2 is prose the assembler does not read.** Eleven identities are required by §2 and none by
`required_governance.artifacts`, which is `[]`. A profile whose §2 emptied tomorrow would still
assemble. That is a finding about the profile's machinery rather than about the platform.

**The domain authority claims are checked by nothing.** `platform` and `transformation` each name a
decision no other domain may make — admission, sufficiency. No mechanism establishes that no other
domain makes it. Recorded as asserted rather than established, which is what the generated text said
before the tables were filled.

**The read-back does not improve externality; it repeats it.** Performed by the same party that
wrote the profile, the platform, and the surface it derives from. A profile read against a
composition by its own author establishes that the author believes it holds, which is weaker than
what a read-back is for.

### The thing worth carrying forward

The profile **refused a composition for lacking an artifact nobody had written** — the evidence
expiry side effect — and the artifact was written in response. That is the strongest evidence in the
exercise that the profile does work rather than describes it, and it happened because §2 named a
requirement its own author could not yet meet.

### Status of the profile

`usable_as_a_target: false`, and correctly. §7 makes being read against a candidate snapshot the
precondition of use; that reading has now happened, and it found five unmet obligations and an unmet
externality requirement. The precondition is satisfied and the target is not met.

**What would change the verdict is a deployment, not code**: nodes that are separately addressable,
an evidence store held by none of them, and a build machine that is not one of them.

### Still owed

The five-gap list that opened this line of work is closed. What replaces it is shorter and is not
all code.

1. **A deployment.** Four addressable nodes, an evidence store external to all of them, and a build
   machine that is not one of them. That closes OB-2, OB-3, EO-1, EO-3 and EO-4 together, because
   they have one cause. Until then the profile is read and not met.
2. **A second reader.** Externality is unmet and a read-back by the author does not mend it. This is
   the only item nothing in this workspace can do.
3. **`cryptographic_trust` V1** — its mode is `LOCAL_DEV_UNSIGNED`, and signing should be selected
   by a composition rather than carried by the surface. The selector generalization already
   pre-wired it; it needs declarations only.
4. Four notes in `doc/` awaiting a decision rather than work: the handler namespace rename,
   supersession-and-force, the composition output root, and the regulated-model domain.

### Where the platform stands

Everything the profile says about *meaning* holds against a sealed, signed, multi-worker composition
that boots, authenticates and executes. Everything it says about *placement* awaits hosts. No part
of it is unexamined.

---

## Placement made composable, and a coordinator that uses it — dev/17

Still nothing on GitHub. Every remote carries `main` alone.

### What this was for

`SIGNED_FEDERATED_MULTINODE_PROFILE_V0` obliges four node roles. The governance surface forbade
them: `CONSTITUTION_EXECUTION_PLACEMENT_V0` §1 authorized `LOCAL_SINGLE_NODE` only — *no remote
dispatch, no worker pool consulted, no distribution layer involved.* Dispatch was never an
implementation task; it was a governed prohibition, and writing a coordinator first would have built
something the surface refuses.

### Placement is now a property of a composition

V0 held that a surface carries one placement structure marked `status: active`. That is adequate
while a surface serves one composition and incoherent once it serves two: **an inventory cannot hold
two answers to where execution runs.** V0 §2 already said the compiler finds *"the active placement
contract in this boundary"* — a boundary is a build, and V0 read it as a repository because for one
composition the two could not be told apart.

| | |
|---|---|
| surface | declares what is **available** — one structure per authorized mode, none claiming activity |
| build configuration | declares what is **active** — naming exactly one |
| snapshot | records what **was** active, so a composition's permissions are recoverable from it |

`CONSTITUTION_EXECUTION_PLACEMENT_V1` authorizes `LOCAL_SINGLE_NODE` and `LOCAL_MULTI_WORKER`. Its
§8 records that V0 was **deleted, not superseded**, and argues it: a superseded structure stays in
the composition, so two would declare one mode; a superseded invariant is still enforced, so V0's
check would go on demanding a `status: active` V1 deliberately drops; and a successor naming an
excluded predecessor dangles. All three were observed, not predicted.

### The selector is generalized, and three more boundaries are pre-wired

`STRUCTURE_BOUNDARY_SELECTION_V0` declares which boundaries a build selects and where each side of
the selection is written. The compiler loads it as it loads `STRUCTURE_DISCOVERY_V0`. Four
boundaries are declared — placement, scheduling, security domain, cryptographic trust — and **all
four already declared their mode in exactly the field the table names**, so the build configuration
now selects all of them. Three have one candidate today, making selection a no-op; when any of them
gets its own V1, multiple candidates become selectable with no compiler change.

Authorization is stated once. The compiler holds no list of authorized modes: a mode no structure
declares resolves to nothing and is refused, because a surface carries a structure only for a mode
its constitution admits.

### Scheduling does not need a V1, and I was wrong to say it did

`execution_scheduling` governs *how execution units **within a topology** coordinate* — parallel
branches, non-blocking dispatch, deterministic joins. Four workers each running a whole workflow is
several serial topologies side by side, and inside each worker scheduling remains
`SERIAL_SINGLE_WORKER`. Changing it would have authorized parallel branch execution inside
workflows, which nothing asks for — the exact widening the placement work existed to avoid, for no
reason.

`cryptographic_trust` **does** need the same treatment eventually: its mode is `LOCAL_DEV_UNSIGNED`,
and signing has to become profile-conditional rather than surface-wide.

### Two compositions from one surface

```
single-node   sealed LOCAL_SINGLE_NODE    from ..._LOCAL_SINGLE_NODE_V1
multi-worker  sealed LOCAL_MULTI_WORKER   from ..._LOCAL_MULTI_WORKER_V1
```

Both 190 artifacts, same surface, one line different.
`STRUCTURE_BUILD_PLATFORM_MULTIWORKER_CONFIG_V1` says so in its own header: a configuration *is* the
definition of a composition, and where the two diverge in anything but placement, that divergence is
a defect.

The multi-worker composition assembles, signs and boots:

```
snapshot_id  f899c0d8ba6ff6e0b2fa76eb43cfb3010e2095ab44b696d0c37f456aacaa3466
composition  PASSED (5 rules over 211 artifacts)
boot         Authenticated under trust root 70c5f1e7129766a3, healthy
```

### The coordinator

`protocol_runtime/runtime/coordinator.py` — a coordinating party that runs several runtimes. Not
part of the runtime and unknown to it: placement §4 obliges a runtime to execute *without consulting
placement mode for branching*, so each worker calls `run_workflow` exactly as a lone runtime would.
What the coordinator adds is which runtime receives which unit, which is a placement question.

Tested, three workers, six units:

```
all six executed, spread across workers 0/1/2, one claim recorded per unit
re-dispatch of the same units    all claimed_elsewhere, executed again: 0
coordinating a single-node snapshot    REFUSED
```

**Placement now governs something.** The mode is read from the sealed composition, not from
configuration — *a coordinator cannot grant itself an arrangement the composition does not carry.*

**OB-4 and EO-5 hold by construction.** A claim is taken by exclusive file creation, so the
filesystem decides once and the loser of a race learns it lost rather than discovering it later in
the evidence. A claim that checked and then wrote would leave a window where two workers both
believed they held it.

**The over-refusal is stated, not discovered.** A worker that claims and dies before its first
effect leaves work nobody retries. Inferring *begun* from effects means reading state a worker may
be mid-write on — the condition it is trying to detect. SM-7a obliges a realization that can apply a
transition partly to determine the resulting state; declining to resume is how this platform
declines to be in that position, and the profile said so before the code did.

### The surface refused three times, and each refusal taught something

- **`ASSERT_CS_SURFACE_CLOSED_V1`** — a capability is not admitted by existing on disk.
- **`ASSERT_SCHEMA_CONFORMANCE_V0`** — the machine block schema is **closed**. `ratified`, `status`
  on a constitution, `multi_worker_allowed`, `selection_check` were all invented and all refused. I
  had been authoring against the shape of examples rather than against the schema.
- **`composition_check` expresses cardinality over snapshot artifacts only** — which killed the
  design I had written and produced a better one needing no schema change: the compiler selects and
  materializes one, the invariant verifies the result. *A snapshot carrying every available mode so
  an invariant could pick between them would be carrying permissions it was not granted.*

The schema also settled a naming question — `multi_worker_allowed` was refused, and rightly:
`placement_mode: LOCAL_MULTI_WORKER` already says it, and a boolean beside it is a second place for
one fact to disagree with itself.

### Held in `doc/`

- `supersession_and_force.md` — a superseded artifact stays in force. `SU-7` requires exclusion from
  *every* projection execution consumes; the realization satisfies only the retention half. The
  existing hygiene check assumes artifacts are reached by **reference**; invariants are reached by
  **presence**. Five superseded artifacts exist, all reference-reached, so exposure is nil and
  nothing prevents the sixth. The map's `SU-7` entry was scoped to the projection it was tested
  against.
- `composition_output_root.md` — two compositions can overwrite each other's output. The root is
  supplied by `PGC_SNAPSHOT_ROOT`; the build configuration declares every path *within* it and not
  the root. New today, for the same reason placement was: one surface, two compositions.
- `handler_namespace_rename.md`, `regulated_llm.md` — unchanged.

### Still owed

1. **Nothing read back against the profile by hand.** Unchanged, and now the largest remaining item:
   the trust root, the five-day window, the five obligations, the six environment obligations, the
   claim discharges. No tool does this.
2. **The evidence store is not yet external to every node.** Claims and traces sit under one
   `data_root`. On one host that is a directory; OB-3 wants it held by no node, which on four
   containers is a mount. Nothing in the code decides that.
3. `cryptographic_trust` V1, when signing becomes profile-conditional.
4. `snapshot_mw/` is a name invented when an output root was needed — see the `doc/` note.

---

## Signing, evidence expiry, and a midcourse correction — dev/17

Nothing here is on GitHub. Every remote carries `main` alone; `dev/17` is local, and stays local
until it is cut. That is the point of working this way and it is why the correction below cost
nothing.

### What was built

**Snapshot authentication.** `snapshot_assembler/assembler/signing.py` signs a sealed snapshot's
identity and verifies it against a key the verifying party holds. `--signing-key` on `assemble`, a
`keygen` subcommand, a report on `verify`, and `protocol_runtime boot` calling the same verify —
one determination, two callers, for the reason acceptance already gave: *a second implementation of
one determination is two things that can disagree.*

Three separations are kept apart, and conflating any two defeats the exercise:

| | |
|---|---|
| snapshot identity | `snapshot_id`, derived from what was sealed |
| snapshot authentication | a signature over that identity |
| trust anchor | a public key the verifying party holds, **from outside the snapshot** |

`Verify(K, I, sigma)` with `K` from the node. The `key_id` in a signature record is read only to
report which failure occurred and **must not** select a key — a snapshot carrying the key that
authenticates it authenticates nothing.

Five outcomes are distinguished, each tested: authenticated · `TrustRootMismatch` · `IdentityMismatch`
· `SignatureInvalid` · `SignatureMalformed`. A valid snapshot carrying a valid signature over a
*different* identity is refused as `IdentityMismatch`, checked before the cryptography, because
calling it a bad signature names the wrong fault.

**Signing is a profile's selection, not a platform property.** `cryptography` is an extra,
`signing = ["cryptography>=42"]`, and the core dependency contract is unchanged. A node holding no
anchor boots an unsigned snapshot exactly as before, so the reference composition is untouched —
tested explicitly, because that is what keeps this a superset rather than a fork.

**Evidence expiry.** `CS_EVIDENCE_EXPIRY_V0`, the artifact `SIGNED_FEDERATED_MULTINODE_PROFILE_V0`
§2 required and nobody had written. It decides three things not at all: not the window
(`retention_window_days` comes from the artifact, so from the snapshot, with no default — absent, it
refuses), not the time (`as_of` arrives from the governed clock; a host reading its own would let
anyone who moved the host clock expire anything), and not what is exempt (the deletion record is
appended to a store that admits no deletion, so **the exemption is structural and no flag could
clear it**).

Tested: `SURVEY` removes nothing; `EXPIRE` ends an attestation together with its subject; evidence
carrying no `closed_at` is left alone rather than expired on mtime, which says when bytes were
written and not when a determination was made.

**Admission is a governed act.** The first compile refused it — `ASSERT_CS_SURFACE_CLOSED_V1`. A
capability is not admitted by existing on disk; it is declared into
`allowed_capability_side_effects`. Added in place, the invariant's own text being *"baseline closed;
extension open."*

### The midcourse correction

`~/signed-federated-pgc` was an external sandbox pinned to the published `v4` and the `4.0.0` wheel.
It proved what it was built to prove — that `pip install` reaches about a third of a working
platform, that `protocol_transport` is unpublished, and that no serving path exists for an installed
platform. All three are recorded and two are fixed.

Then it became the wrong shape. **A platform whose obligations require signing cannot be developed
against a release that has none.** Signing and expiry both landed on `dev/17`, which the sandbox is
pinned away from, and pinning it to `dev/17` was not available either: `dev/17` is not pushed, so a
branch or SHA there is exactly the unresolvable pin that `history-16` already was.

So the profile moved into the workspace. `.github/snapshot_profiles/` now carries all six documents
beside the two that were there.

**They coexist; nothing is superseded.** `4e` obliges a superseding profile to state what it
invalidates, and this one invalidates nothing about the composition claiming the profile in force —
that composition still requires it, and superseding would orphan a live claim. The directory already
held a superseded profile beside a current one, so the arrangement is the existing one, not a new
one. Assembly decides: `--profile` selects which contract a snapshot claims, and the same three
domains compose under either. What differs is what is required of them, not what they are.

`regression.sh` needed no change — `PGC_SNAPSHOT_PROFILE` already parameterizes this, and the
RUNBOOK already called such a thing a candidate profile. Both now name it.

**§5.1 was rewritten because it had become false.** It pinned a toolchain unable to meet the profile
it introduces. It now records that, and where reproduction actually lives: content-derived identity
covering the compiler, plus the deposited composition — *a development profile asserting
reproducibility would be claiming a property of a release it is not.*

### First build of the merged arrangement

```
snapshot_id  36ff116e9f48ef5e4972c44b915f9670c55620aebe111be925465d65beb93c64
profile      SIGNED_FEDERATED_MULTINODE_PROFILE_V0
composition  PASSED (5 rules over 209 artifacts)      208 before; the new capability
signing      signed under key 70c5f1e7129766a3
boot         Authenticated under trust root, resident, hash-verified, healthy
```

Signing and evidence expiry are in a real snapshot for the first time. Neither could ever have
reached the sandbox.

### Held in `doc/`, not decided

Neither is parked in the gitignored sense — `doc/parkinglot/` is scratch that gets cleaned, and both
of these are things looking for a final home rather than things being discarded.

- `.github/doc/handler_namespace_rename.md` — 89 handler-registry keys name
  `pgs_governance`, the retired namespace. **Not a stale reference: the naming convention**, with
  zero Python imports behind it and `pgc_env_check` passing. It was misread as a defect once, from
  the artifact, which is the evidence that the name misleads. A partial rename does not degrade — it
  stops the build, the registry's own comment making an unknown handler a compile failure by design.
  96 edits in one commit, behaviour-neutral, or not at all.
- `.github/doc/regulated_llm.md` — a regulated language model as a governed domain. Phase 1 worth
  testing; phase 2 as proposed claims what this architecture cannot govern. After the platform.

### Still owed

1. **Coordinator and worker dispatch.** `boot` and `run --wf` exist; the four node roles the
   environment profile requires are implemented by nothing.
2. **Nothing read back against the profile by hand** — the trust root, the window, the five
   obligations, the six environment obligations, the claim discharges. Unchanged, and still the
   piece no tool can do.
3. `~/signed-federated-pgc` is dormant, not deleted. Its profiles and parked note are copied out;
   nothing else in it is worth keeping.
4. `SIGNED_FEDERATED_MULTINODE_PROFILE_V0` now exists in two places — here, operational, and in
   `standards/profile_authoring/worked_example/`, illustrative. They can drift, and the worked
   example's copy is the one that should say which it is.

---

## v4 composition deposited — the release cycle is closed — 2026-09-11

`release.sh --publish-composition` ran. **The composition version DOI is
[10.5281/zenodo.22714911](https://doi.org/10.5281/zenodo.22714911)** (concept `10.5281/zenodo.22184747`).
Cite the version DOI, never the concept. `pgc_release` is clean on `main`, tagged `v4`, pushed —
the three commits that had been sitting ahead of origin went up with it.

### The deposit

| | |
|---|---|
| public identity | `v4` |
| assembler ordinal | **16** |
| sealed snapshot | `d92b447fd39eaf926bb2f4330f9efbb19d744ecfbc3fe9a214ae52945918905d` |
| profile | `GOVERNANCE_SURFACE_PROFILE_V0` |
| composition | 7 domains, 410 artifacts, 595 constituents, 597 snapshot files |

**No ordinal-discrepancy section this time.** v3 carries one because it sealed ordinal 16 over
components declaring 15. This deposit's ordinal matches what its components declare, and the
`MANIFEST.md` accordingly has nothing to explain away.

That did not happen by following the procedure the previous entry recorded. **That procedure was
incomplete**: it set only `.github/VERSION`, which drives the manifest's prose. Two other files
determine the artifact — `protocol_compiler/VERSION` becomes `COMPILER_VERSION`, lands in every
materialized artifact, and therefore *changes the snapshot identity*; `snapshot_assembler/VERSION`
becomes `provenance.assembler_version` and stamps the manifest's ordinal and `pgc_release/VERSION`.
Composing with only the documented edit would have deposited snapshot `41adfd87…` at ordinal 17
while claiming dev/16 — the exact artifact v3 had to apologise for.

What was done instead, and what to do next cycle:

```bash
# Not an edit — a restore of the tagged state. v4..HEAD differs by exactly one
# file in every component repo, and that file is VERSION.
for r in protocol_compiler snapshot_assembler protocol_runtime protocol_transport          snapshot_inspector software_governance conformance_workloads          business_domains transformation .github; do
  ( cd $r && git checkout v4 -- VERSION )
done
bash .github/process/regression.sh --build      # gate: must reproduce the freeze hash
.github/process/release.sh --publish-composition

# Restore. `git checkout <tag> -- FILE` STAGES the change, so `git checkout -- FILE`
# is a silent no-op afterwards. This is the incantation that works:
for r in ...; do ( cd $r && git restore --staged --worktree VERSION ); done
bash .github/process/regression.sh --build
```

The rebuild before composing is a gate, not a formality: if it does not reproduce the hash this
handoff records, stop rather than deposit something unverified.

### Component DOIs at v4

Nine, each unique. `.github` is not among them — it carries no Zenodo webhook and is not in
`compose_release.COMPONENTS`.

| repo | DOI | | repo | DOI |
|---|---|---|---|---|
| `software_governance` | 22714508 | | `snapshot_assembler` | 22714507 |
| `conformance_workloads` | 22714505 | | `protocol_transport` | 22714513 |
| `business_domains` | 22714506 | | `snapshot_inspector` | 22714514 |
| `protocol_compiler` | 22714509 | | `transformation` | 22714518 |
| `protocol_runtime` | 22714512 | | | |

### Three duplicate deposits were minted and deleted — read this before the next cycle

`transformation` was checked for its DOI with a Zenodo title search, `q=title:"(transformation)"`.
Zenodo's tokenizer does not match that, so the query returned nothing **for a record that already
existed**. Read as a failed mint, the release was deleted and recreated three times; each fire
minted another version. Four v4 records existed for one component. Zenodo permits self-deletion
under 30 days, so `22714657`, `22714682` and `22714703` were removed and `22714518` — the one the
release cut produced — was kept.

Three lessons, in order of how much they would have saved:

1. **Never verify a mint with a title search.** Resolve a known prior version by DOI, read its
   `conceptrecid`, and query `conceptrecid:<id>&all_versions=true`. That is exact and cannot
   silently return zero.
2. **Webhook status codes are noise.** `transformation` showed `hookshot_error`/500 on one
   sub-event and had minted anyway; `snapshot_inspector` showed 500 on all three and minted. Zenodo
   is slow enough (16.5 s to first byte during this cycle) that GitHub gives up after one attempt
   while Zenodo still processes the request.
3. **Redelivery needs `admin:repo_hook`,** which the current token lacks — `gh auth refresh -h
   github.com -s admin:repo_hook` if it is ever needed. Without it the only lever is
   delete-and-recreate, which mints. Prefer waiting.

Also unavailable this cycle: `scratchpad/publish_component_releases.sh`, staged by the previous
entry, was gone — the workspace `scratchpad/` no longer exists. The nine releases were created with
a plain `gh release create v4 --verify-tag` loop, guarded by a Zenodo reachability check and a skip
for any repo already released. That loop is worth keeping in `.github/process/` now that the freeze
is over.

### RUNBOOK and SOTU corrections

Four expected-results claims were stale and are fixed, each verified against a run rather than a
reading:

- `test_warm_boot.py` — was "2 failures, both pre-existing"; is `6/6`. One change resolved both:
  `boot()` no longer carries its own acceptance check and delegates to
  `assembler.core.verify_snapshot`. `test_composite_recompute_matches_manifest` was retired with the
  weaker check it tested.
- `test_governance_provenance.py` — was "2 of 4 red, undiagnosed"; is `4/4`.
- the freeze row's snapshot id — was truncated to 16 of 64 characters, which cannot be compared and
  reads as a mismatch against any rebuild. Now full, with the ordinal it was built at.
- `si snapshot validate` — the freeze row said "no advisory", which is false. Both advisory checks
  are red and always have been (`republished_copies_agree` 15, `bound_paths_declared_as_stores` 1).
  Non-advisory violations are zero, which is the pass. This row cost a downstream reader a wrong
  correction; it now states counts, not a verdict.

**The common cause is not any of the four lines.** `RUNBOOK.md`'s expected-results table is a rule
set carried in prose that nothing evaluates, so no rule in it is capable of refusing. Payloads and
boundary contracts each have a `--check` that prints `DRIFTED` on a hand edit; the runbook has none.
Until those expectations are data the script compares against — including an *unexpected pass*, which
is how both of these went unnoticed — the table will drift again.

### State

All twelve repos clean. Ten components on `dev/17` with `VERSION` 17; `pgc_release` and
`pgc_install` on `main`. Working snapshot rebuilt to `41adfd877515544b0277fb843a99cd65efcf79c24579d29a28afa681b64be89e`
at ordinal 17 — that is the dev-cycle build and is *not* the deposited artifact.

Only `main` exists on any remote; `dev/N` is local-only and has no upstream, so "in sync" is not a
question that applies to it. `.github/main` carries one commit past tag `v4` (`5ad8a62`, the RUNBOOK
fix) so the correction is publicly readable now; the next `release.sh --publish` will force-push an
orphan over it, which is harmless since the fix is already on `dev/17` and rides the squash.

### Queued for `dev/18`

- Runbook expectations as data, with an unexpected-pass check (above).
- `publish_component_releases.sh` adopted into `.github/process/`.
- Two `pgc_install/README.md` documentation gaps from the newcomer install test, carried from the
  previous entry.
- Profiles out of `.github` into their own repo, not on PyPI, with `PGC_SNAPSHOT_PROFILES` required
  and the profile's *content hash* covered by the snapshot identity. Today the identity covers the
  profile's name only, so a profile can be weakened without changing the identity of any snapshot
  claiming it. This is a v5 change: it alters what the identity covers, and therefore every id.

---

## v4 published to PyPI and tagged across ten repos — composition deposit still pending — 2026-09-09

`dev/16` closed. All ten component repos carry tag `v4` on `main`, are clean on `dev/17`, and
`protocol-governed-computing 4.0.0` is live on PyPI. The newcomer install path was executed
end-to-end from an empty directory by the author and reached a booted snapshot. **The workspace is
frozen**: no repo is to be modified. Known rough edges are deferred to JIT fixes, listed below.

### The one unfinished step — blocked on two things, not one

`release.sh --publish-composition` has **not** run. The first attempt died before staging anything:

```
compose_release: cannot reach Zenodo: The read operation timed out
```

`pgc_release` was never touched, carries no `v4` tag, and sits **3 commits ahead of origin** — those
commits belong to the pending deposit, not stragglers to push separately.

**Blocker 1 — Zenodo is down.** Not a defect and not our network: `zenodo.org/` itself returned 504,
then stopped answering entirely. Check `https://status.zenodo.org` before doing anything else.

**Blocker 2 — the ten component releases were never created, and this is the real gap.**
`release.sh:178` creates a GitHub release for exactly one repo, `pgc_release`, inside the COMPOSE
branch. The ten component repos receive only a **tag**. The script's own comment at that line states
the consequence: *"Publishing the RELEASE is what fires the webhook; pushing the tag alone does
not."* Zenodo mints on the `release` event, never on a tag push.

Confirmed: `software_governance` has releases at `v2` and `v3` but **none at `v4`**, and its Zenodo
webhook reports `"status": "unused"` — it has never fired. So the ten component DOIs for `v4` do not
exist, and `compose_release.py` would have failed on ten missing DOIs even with Zenodo up. The
outage masked it.

**Those ten releases were made by hand in every prior cycle.** That manual step lived only in the
author's memory, which is why its absence read as a network error. A script that supplies it is
staged but deliberately **not** in `.github/process/` — writing it there would modify a frozen repo:

```
scratchpad/publish_component_releases.sh    # chmod +x before use; adopt into .github/process/ on unfreeze
```

It refuses to publish anything unless Zenodo answers first (a release published during an outage
mints no DOI and needs a per-repo webhook redelivery afterwards), skips repos already released so a
partial run is safe to repeat, and takes `--verify` to list which of the ten have deposits.

**The ordinal edit must be re-applied on every attempt, and it now serves two purposes.**
`.github/VERSION` is read by `compose_release.py:149` for the composition ordinal *and* by the
release-notes lookup. The cut advanced it to **17**; the ten components declare **16** and the notes
file is `release-16.md`. Composing at 17 stamps a deposit whose components claim a different ordinal
— precisely the labelling artifact `pgc_release/MANIFEST.md:13` documents for v3. The fix is a
temporary, never-committed edit:

```bash
cd ~/protocol-governed-computing && source .venv/bin/activate
echo 16 > .github/VERSION

scratchpad/publish_component_releases.sh             # ten component releases → ten DOIs
sleep 90
scratchpad/publish_component_releases.sh --verify    # all ten must show a timestamp

.github/process/release.sh --publish-composition     # prompts before it commits
echo 17 > .github/VERSION
git -C .github status --porcelain                    # only doc/SOTU.md
```

Then verify `head -6 pgc_release/MANIFEST.md` reads public identity `v4`, assembler ordinal `16`.
The compose aborts on its own if the `pgc_release` webhook is missing (it is present — one hook
confirmed) or if `pgc_release` already bears the tag.

### Verified state at freeze

| check | result |
|---|---|
| workspace snapshot | `d92b447fd39eaf926bb2f4330f9efbb19d744ecfbc3fe9a214ae52945918905d` — the full id, because a truncation cannot be compared and reads as a mismatch against a rebuild. `snapshot_id` and `composite_hash` identical, profile `GOVERNANCE_SURFACE_PROFILE_V0`, 7 domains, 595 constituents. **Built at ordinal 16.** `COMPILER_VERSION` comes from `protocol_compiler/VERSION`, is written into every materialized artifact, and materialized artifacts are constituents — so the same governed content seals a different identity once the cycle advances the counter. At `dev/17` the same tree seals `41adfd877515544b0277fb843a99cd65efcf79c24579d29a28afa681b64be89e`; the seven graph addresses and all 595 constituents are unchanged between them. To reproduce this row, `echo 16 > protocol_compiler/VERSION` before building |
| `si snapshot validate` | `valid: true`, 10 checks, **0 non-advisory violations** — which is the pass. Both advisory checks are red and always have been: `republished_copies_agree` 15, `bound_paths_declared_as_stores` 1. Advisory failures exit 0; `--strict` turns them red. An earlier version of this row read "no advisory", which is false and cost a downstream reader a wrong correction — state the counts, not a verdict |
| runtime warm-boot testbed | 6/6 passed |
| release build gate (on the tagged tree) | clean rebuild + assemble + composition conformance, 410 passed / 5 skipped |
| ten component repos | clean, `dev/17`, `main` tagged `v4` |
| `pgc_install` | clean, `main`, pushed |
| `pgc_release` | clean, `main`, **3 unpushed** — the pending deposit |

### Cleanup queued from the newcomer install test

Two documentation gaps the clean-environment run surfaced. Both are in `pgc_install/README.md`, both
are cosmetic against a path that otherwise worked end-to-end, and neither is worth breaking the
freeze for — do them in the first `dev/18` commit.

1. **The `⚠ Machine-block health` advisory is undocumented.** A correct run prints it, the README's
   rough-edges section does not mention it, and a newcomer has no way to tell an expected advisory
   from a symptom. Say what it means and that it is expected.
2. **The platform compile writes into the cloned repo.** `compiled/` lands inside the clone rather
   than under a build root. The README never says so, so a reader who expects a read-only source
   tree is surprised by a dirty checkout. State it, and note that `PGC_BUILD_ROOT` does *not* change
   it — `build_root()` still has no callers.

### Deferred — do not open the repos for these

- `bound_paths_declared_as_stores` remains undiagnosed.
- Whether anything should read profile §3 obligations — `GS-1`..`GS-3` are declared and unchecked.
- Whether a consuming domain should publish under the authoring identity at all.
- Canonical kind-vocabulary enumeration trigger has fired; parked in `.github/doc/parked_rulings.md`.
- **Fold component-release publication into `release.sh`.** It is the missing half of the release
  procedure and the direct cause of this cycle's stall; the staged script is the starting point.
- **Split `release.sh` publish from ordinal advance.** A publish that fails leaves `.github/VERSION`
  ahead of the identity it names, and the correction is a manual edit someone must remember. This
  session is the motivating case, and the double duty that file now serves — ordinal *and*
  release-notes selection — makes it worse, since both want the pre-advance value.

### Next session should start with

Check `https://status.zenodo.org`. When it is up, run the block above **in full** — the two component
release commands are not optional, and skipping them is what failed this time. Nothing else in the
workspace is to change. The author has moved to `~/omnibachi-site` to write a new paper; `standards/`
is the only tree not frozen.


## Install path validated from a clean environment — `dev/16` reopened for the v4 mop-up — 2026-09-08

The previous entry closed this file at the `v3` freeze. It reopens because installing `v3` from
PyPI into an empty directory does not reach a running snapshot by following the published
instructions, and the gap is large enough to need a cycle of its own. **`dev/16` is dedicated to
mop-up**; nothing here is a new capability.

### What was proven

A clean venv, wheels built from `dev/16`, four cloned repositories and six anchors reach a sealed,
executing platform: compile platform + workload + inspection → assemble → composition conformance
PASSED → warm boot hash-verified → workflow SUCCESS, and the NACK payload correctly returns
VIOLATION. The counts match the workspace exactly, so the trimmed wheels lose nothing.

Every blocker met along the way was a **discovery** problem, not a code defect. No compiler,
assembler or runtime change was needed to reach a conformant PNP.

### What is wrong

**Packaging.** `pgc-governance` shipped `capability_transforms/registry/` and
`capability_side_effects/registry/`; `pgc-workloads` shipped a compiled snapshot, `registry/` and
`test_payloads/`. Both from over-broad `package-data` globs, and both contradicting the comments
directly above them. `.DS_Store` shipped too. The leaked registries are inert — the compiler resolves
declarations from `PGC_PLATFORM_ROOT` — but they are a second governance surface sitting in a wheel.

**Documentation.** Reaching a snapshot needs four repositories and six anchors. The published
instructions name one repository and three anchors, one of which does nothing.

- `PGC_BUILD_ROOT` is inert. `build_root()` is defined and never called; `PGC_SNAPSHOT_ROOT` is the
  anchor that controls compiled output, and it is documented nowhere.
- `PGC_SNAPSHOT_ROOT` means two different things — compiled output root to the compiler, assembled
  snapshot root to the runtime.
- `PGC_SNAPSHOT_PROFILES` is required by both the assembler and the runtime, and is named in neither
  `--help` nor any install document. The profiles live in `.github`, which nothing tells a user to clone.
- `PGC_DOMAIN_ROOTS` must name the directory holding `registry/structures/`, not the repository above
  it. Pointing one level too high is a silent no-op.
- Each domain build needs its own `PGC_SNAPSHOT_ROOT`. Two domains sharing one output root cannot both
  pass S8, which reports the other domain's artifacts as undeclared.
- `--all-structures` and `STRUCTURE_BUILD_PLATFORM_CONFIG_V0` do not build; only `_V1` does.
- `pgc` reports "Ready" once the governance surface resolves, which is readiness for the platform
  compile only, not for assembly or execution.

**The ergonomics already exist, and are not distributed.** `protocol_compiler/compile_domain.sh` sets
all three compile anchors per domain — including `PGC_SNAPSHOT_ROOT=<domain>/snapshot`, the separation
whose absence produced the E402 deadlock — and auto-discovers the build STRUCTURE. `snapshot_assembler/assemble.sh`
auto-discovers every compiled root and refuses to assemble when a domain declares source but has no
compiled output, precisely so a skipped compile cannot silently narrow a composition. Neither ships:
`packages.find` includes `compiler*` and `assembler*`, and both runners sit at their repo roots,
outside those trees. A PyPI user therefore performs by hand what the workspace has automated since
before `v3`. Whether the fix is to package the runners or to document the sequence is a decision, not
a defect — but the current state is the worst of both, since the sequence was documented nowhere either.

**Two anchors differ by one letter.** `PGC_SNAPSHOT_PROFILE` (singular) names the profile identity a
snapshot claims and is read by `assemble.sh`; `PGC_SNAPSHOT_PROFILES` (plural) names the directory
profiles are read from and is read by the assembler and runtime. Neither is documented.

**A real defect, wider than one artifact.** `si artifact show capability_side_effects::CS_MUTABLE_JSON_V0` returns an
execution-binding stub — empty `content`, empty `references`, `layer_code: WORKLOAD` — instead of the
platform authoring copy. Two copies exist by design: `s1_extract._inject_imported_capabilities` lifts
consumed CS/CT into the consuming domain carrying only the execution binding. But the compiler's
`metadata.imported` marker does not survive into the sealed artifact, so
`snapshot_assembler/assembler/indexes.py:44-51` cannot tell them apart and keeps whichever sorts last —
`canonical/workload/` after `canonical/platform/`, by alphabetical accident. `si snapshot validate`
flags it as `republished_copies_agree`, advisory. Fixing it changes content hashes and therefore
snapshot identity.

**Scope, measured against the full seven-domain snapshot: fifteen violations, not one — six side
effects and nine capability transforms.** Every consumed capability is duplicated, each diverging on
the same four fields, `content`, `layer_code`, `references`, `version`. The count scales with the
composition, because every domain that consumes a capability emits its own execution binding beside
the platform's authoring copy. A one-artifact finding was an artifact of the narrow composition it
was found in, and it was not confined to side effects.

**Only three of the fifteen actually resolve wrongly, and which three is decided by alphabetical
order.** `indexed_copy` is the platform's authoring copy for twelve of them. It is the consuming
domain's execution binding for exactly the three whose consumer sorts after `platform`:
`CS_MUTABLE_JSON_V0` → `canonical/workload/`, `CS_SNAPSHOT_QUERY_V0` and `CS_TEXT_ARTIFACT_V0` →
`canonical/transformation/`. Consumers sorting before it — `ai_governance`, `blockchain`,
`book_library_mgmt`, `inspection` — lose to `platform` and the index happens to be right.

This was the last-write-wins in `indexes.py` measured rather than reasoned about, and it was worse
than a wrong resolution: the index was correct for twelve of the fifteen **by coincidence of domain
naming**. Renaming a domain, or adding one whose name sorts late, silently changed which copy
`si artifact show` returned for a capability nobody edited.

**Fixed.** `_load_canonical` now prefers the authoring copy rather than whichever sorted last. The
discriminator is authored `content`: the field-level diff shows `content_hash`, `frontmatter` and the
IR byte-identical across copies, while the execution binding has `content` and `references` emptied
and `layer_code` naming the consuming layer. So the copy still carrying authored content is the
authoring copy, which is what `si.artifact.show` promises. Ties keep the first seen, so the sorted
walk remains the tiebreak and the result is stable. All three indexes share `_load_canonical` and all
three benefit.

The binding copy also carries the `content_hash` of content it does not hold — the sharper tell, and
deliberately **not** the selector: an inconsistent hash is a defect to report, not something to route
on. That reasoning is recorded in `_authoring_rank`.

After the fix, identities resolving to a non-authoring copy: **zero**. `CS_MUTABLE_JSON_V0` returns
10888 characters under `REUSABLE_SIDE_EFFECTS` where it returned an empty stub under `WORKLOAD`;
`CS_SNAPSHOT_QUERY_V0` and `CS_TEXT_ARTIFACT_V0` likewise. Assembler testbed 13/13, inspector 121/121,
warm boot healthy over seven domains, collatz SUCCESS. Two testbed cases pin it —
`artifact_index_resolves_to_authoring_copy` and `artifact_index_ignores_domain_name_order`, the second
asserting the same identity resolves identically whether the consumer is named `blockchain`,
`workload` or `transformation`. Both fail against the previous `indexes.py`, which is what makes them
worth having.

`republished_copies_agree` still reports fifteen, correctly: the copies do diverge. The advisory
reports a fact about the composition; what was defective was the index. **Whether the duplication
should exist at all remains open** and is compiler-side — carrying `metadata.imported` through
materialization would let the assembler select on a declared marker instead of inferring from an
emptied field.

The snapshot identity is now `1194598a…`; index content feeds identity, so the fix moves it.

The inspector's own suite passes `validate_catches_divergent_copies` and `validate_names_divergent_fields`,
so detection is intended and tested. What nothing asserts is **which copy the index resolves to** —
that is the untested behaviour, and it is where the defect lives.

**A second advisory fails on the same snapshot.** `bound_paths_declared_as_stores`, one violation:
`ai_governance::RB_AGENT_GOVERNANCE_BINDINGS_V0` binds `CS_REGISTRY_V0` to
`ai_governance/agent_governance/governance_actions.json`, a path no store declares. Two of two
examined, one failing. Not yet diagnosed.

**Release tooling.** `release.sh:27` claims pyproject versions derive from each repo's `VERSION`.
They do not — all nine are hand-edited literals, and nothing asserts them against `PUBLIC_VERSION`.
That is how `3.0.0` came to name two different byte sets: the published wheels, and anything built
from `dev/16`.

**Environment.** A `.DS_Store` written into a sealed snapshot makes it unbootable — correctly refused
at acceptance under 3b §6, but it means opening a snapshot in Finder breaks it until the file is removed.

### Committed on `dev/16` — ten repositories, working trees clean

All twelve repositories are clean. Ten carry the mop-up under one message,
`v4 mop-up: documentation, packaging, and check corrections`; `pgc_release` was untouched and
`pgc_install` is on `main` and pushed.

**Bumped to `v4` / `4.0.0`.** Eighteen literals across nine pyprojects (nine versions, eight pins,
one optional extra), `.github/PUBLIC_VERSION`, seven component READMEs, the `pgc_install` versioning
section, and a `v4` entry in `publications.md` — which preflight requires by name before it will cut.

It is a new identity rather than a patch because the composition changed what it *answers*: an
identity published by more than one domain now resolves to its authoring copy instead of to whichever
sorted last. The wheels also stopped shipping declarations and acceptance now evaluates both identity
claims a manifest carries, but either alone would have been a patch.

### Build and test status — PASSING

`regression.sh --all` on the committed tree, exit 0, snapshot `d92b447f…`, composition conformance
PASSED over 410 artifacts. The run exercised the new full cleanup for the first time and the sealed
release survived it — `pgc_release/snapshot` intact at 604 files, git clean, boots healthy.

Green: governance closure (95 named / 89 registry, 0 orphans), governance chain, supersession (7),
human block (404), evidence determinism, frontmatter, meta (822 rules), differential (83 documents),
e2e (83 cases), projection, construction acceptance 99/99, implementation closure (28), inspector
121/121, indexes 13/13, compiler atoms 9/9, provenance 4/4, reference collatz, warm boot 6/6,
environment check. Execution: collatz, both `ai_governance` workflows, `book_library_mgmt` 23/23 and
21/21, `blockchain` 15/15 and 9/9.

Red by design, both expected: `admission_contract_fidelity` at 31 findings, and the advisory half of
`si snapshot validate` — `valid: True`, no non-advisory failure, `republished_copies_agree` at 15 and
`bound_paths_declared_as_stores` at 1.

**Determinism was demonstrated rather than asserted**: two consecutive full teardowns and rebuilds
produced byte-identical snapshot identities, and the identity moved only when a declaration actually
changed.

### The skinny profile

`GOVERNANCE_SURFACE_PROFILE_V0` is copied into `.github/snapshot_profiles/` from the standards worked
example and completed. It is the skinny composition: `required_workloads.entry_workflows: []`,
`required_domains: [platform, inspection]` — a workload composes like any other domain, and nothing
requires one to be present.

It arrived as a draft with open gaps and `usable_as_a_target: false`, and adopting it unchanged would
have been worse than `REFERENCE_PLATFORM_PROFILE_V1`: `verify_profile` reads only `required_governance`
and `required_workloads.entry_workflows`, and in the draft the first was empty and the second is `[]` —
a profile that cannot fail. What was written:

**§2, thirty-six required identities.** The twenty-eight platform identities carry over from
`REFERENCE_PLATFORM_PROFILE_V1` — all are platform-domain, none workload-specific, and each was
verified to resolve rather than trusted. Eight inspection identities were added as four ingress/egress
pairs, because `required_domains` is a key nothing verifies: naming inspection operations in §2 puts
that requirement somewhere checked. The execution-semantics constitutions stay required despite no
workload being composed — the surface must be able to govern a workflow; the capacity is required, the
instance is not, and that is the substantive line between this profile and V1.

**§3, three additional obligations**, each with a stated breach. `GS-1` governance closure agreement
across domains; `GS-2` one authored copy per identity — **recorded as breached by the current reference
realization**, since that is the `CS_MUTABLE_JSON_V0` finding above; `GS-3` no artifact in a required
domain may reference a namespace the profile does not declare, which is what makes "composes no
workload" a property rather than a description of one build.

**§4, each claim with its discharge class** from `7a` §7. `SNAPSHOT_IMMUTABILITY` structural, its
failing demonstration being the unenumerated-constituent refusal actually observed. `DETERMINISTIC_EXECUTION`
derivational for addresses and **comparative-not-discharged** for execution — one OS, one interpreter,
one runtime, which `7a` §7.3 says is not a comparative discharge however thorough.
`COMPILED_INVOCATION_RESOLUTION` structural.

**§5 derivation deleted** — `derives_from: null`, and the template directs that an absent section beats
one saying "none". Externality now states its case rather than asking for it: not external, same
authority, recorded as a finding against any claim made under it.

`usable_as_a_target` remains **false**. The gaps are closed, but §6 requires a profile to have been read
against a candidate snapshot before it is handed to anyone, and it has not been. Clearing that is a
concrete prerequisite below, not a formality.

The standards copy at `standards/profile_authoring/worked_example/` is untouched and will now drift.
Which copy is canonical is undecided.

### What the regression does and does not establish

**The business domains are exercised from the workspace, not from a wheel.** This narrows the
`pgc-domains` gap without closing it: nothing says the packaged distribution behaves the same, and
that wheel has had no packaging review.

**`si snapshot validate` was added to the check block.** Without it a fully green run sits on top of
a composition carrying advisory failures — which is how fifteen divergent copies went unreported
through an earlier passing run.

**`regression.sh` claims one profile per run.** It now defaults to `GOVERNANCE_SURFACE_PROFILE_V0`
and accepts `PGC_SNAPSHOT_PROFILE` as an override, which is how a candidate profile is read against
the composition before being put in force.

### The skinny composition assembles, validates clean, and boots

`GOVERNANCE_SURFACE_PROFILE_V0` has been read against two candidate snapshots.

**Satisfiable over the reference composition.** Seven domains under the new profile: assembled,
profile verified, composition conformance PASSED over 410 artifacts. The `snapshot_id` differs from
the same domains under `REFERENCE_PLATFORM_PROFILE_V1` because the claimed profile identity is a
constituent.

**Satisfied by the composition it was written for.** Platform + inspection only, via
`PGC_SOURCE_ROOTS`: two domains, 194 artifacts, conformance PASSED, warm boot hash-verified with
governance provenance bound. `si snapshot validate` reports **every check clean — zero violations,
advisories included.**

That last result sharpens the duplication defect. The reference composition carries fifteen divergent
copies; this one carries none. The cause is not the platform publishing side effects twice — it is
**composing a domain that consumes them**, since each consumer emits its own execution binding beside
the authoring copy. Inspection declares thirty-six boundary contracts and consumes no capability, so
nothing is injected and nothing diverges. `INVARIANT_INSPECTION_BOUNDARY_COMPOSED_V0` is satisfied
with no workload present, which was the open question about whether inspection could stand as the
sole non-platform domain.

The profile is `status: complete`, `open_gaps: 0`, `usable_as_a_target: true` — §6's precondition,
that a profile be read against a candidate snapshot before it is handed to anyone, is met. It is now
the profile in force: it declares `supersedes: REFERENCE_PLATFORM_PROFILE_V1`, `regression.sh`
defaults to it, and the nineteen operational references across eight files that named the predecessor
now name it. Sealed evidence, the SU-3 declarations, and history were left alone.

**Two profiles deleted, one retained under protest of the evidence.**
`NORMATIVE_PLATFORM_PROFILE_BASELINE_V0` and `UNCOMPOSED_PLATFORM_PROFILE_V0` are gone — a deliberate
act, which `4e` §6 distinguishes from supersession, since supersession deletes nothing. No manifest
claimed either.

`REFERENCE_PLATFORM_PROFILE_V1` **cannot be deleted**, and this was tested rather than argued. Moving
it out of the profile root and booting the sealed `v3` release gives:

    snapshot claims profile 'REFERENCE_PLATFORM_PROFILE_V1' and no profile of that identity
    was found — a claim nobody can read is not a claim (3b SN-7)

`pgc_release/snapshot/manifest.json` names that identity and profiles resolve by identity at read
time, so deleting the file makes a published, DOI-cited release unreadable. It is retained for that
reason alone, and its prose now says so. Its own `supersedes` was set to `null` and its supersession
paragraph rewritten, because it had claimed its predecessor "is retained and remains readable" — no
longer true.

### Prerequisites to the v4 bump

Ordered by dependency. Items 1 and 2 both change snapshot identity and must land before anything is
re-validated.

1. **Decide what reads §3.** `GOVERNANCE_SURFACE_PROFILE_V0` is complete and both runs pass, but
   `verify_profile` reads only `required_governance` and `required_workloads.entry_workflows` — so
   `GS-1`, `GS-2` and `GS-3` are stated and unchecked. Either extend the verifier to honour them, or
   record that §3 is documentation. The same applies to `required_domains`, which is why the
   inspection identities had to be named in §2 to be enforced at all.
2. **The duplication itself, now that its symptom is fixed.** The index resolves correctly; the
   composition still publishes fifteen identities twice. Decide whether a consuming domain should
   emit an execution binding under the authoring identity at all, and if it should, carry
   `metadata.imported` through materialization so the assembler selects on a declaration rather than
   on an emptied field. Separately, diagnose `bound_paths_declared_as_stores` — one violation,
   unrelated to the duplication, undiagnosed.
3. ~~Per-repo review.~~ **Done** — all nine wheels inspected, three blanket globs narrowed, the
   `pgc-domains[blockchain]` extra exercised.
4. ~~`pgc-domains` exercised end to end from a wheel.~~ **Done** — `ai_governance` compiled,
   assembled, booted and executed from an offline wheel install with no workspace code on the path.
5. **Documentation.** Fold the anchor set and rough edges into the component READMEs, correct
   `release.sh:27`, and record the `.DS_Store` hazard.
6. **Mock upload.** TestPyPI, with `--extra-index-url` to real PyPI for third-party dependencies, then
   a clean install from it — the upload path itself has never been exercised.
7. **Version bump last.** Nine pyprojects and eight pins to `4.0.0`, `.github/PUBLIC_VERSION` to `v4`,
   and the `publications.md` entry recording what v4 supersedes — `release.sh:264-267` aborts without it.

Still untested and not closable locally: installing from PyPI itself, and any platform or Python other
than macOS/arm64 on 3.12. `requires-python = ">=3.10"` is a claim, not a tested fact.

### Packaging reviewed across all nine wheels — clean

Prerequisite 3 is closed. Every wheel was built and inspected: no `registry/`, `snapshot/`,
`.DS_Store`, `test_payloads`, testbed, scripts, docs or dossiers in any of the nine.

Nothing needed is missing either, checked by installing all nine offline into a throwaway venv and
walking them: **330 submodules imported across 12 packages, one failure** —
`blockchain…ct_pure_derive_wallet_address_v0` needs `Crypto`, which is the `pgc-domains[blockchain]`
optional extra behaving as designed. Installing the extra resolves it and `execute` is callable, so
**the untested optional extra is now tested**. All six console scripts run. `compiler/VERSION` and
`assembler/VERSION` are staged correctly by the `_build_hook` backend those two repos declare;
`assembler.__init__` is the only importer that reads one.

**One preventive change.** Three repos still carried the blanket `package-data` pattern that produced
the two leaks already fixed — `protocol_compiler` and `snapshot_assembler` as
`"*" = ["*.md", "*.yaml", "*.json", …, "VERSION"]`, `business_domains` as `"*" = ["*.json"]`. All
three were clean only because no matching file happened to sit under a packaged tree; a design note
added beside a module would have shipped silently. Narrowed to `"compiler" = ["VERSION"]`,
`"assembler" = ["VERSION"]`, and the `business_domains` block removed. Rebuilt: contents identical —
6, 170 and 17 files — so no behaviour changed and the trap is gone.

`protocol_runtime` is the shape to copy: `include-package-data = false` with an explicit `exclude`.
`snapshot_inspector` declares no package-data and needs none.

### The full pipeline runs from the wheels

Prerequisite 4 is closed. A business domain was compiled, assembled, booted and executed with **no
workspace code on the path** — the toolchain from an offline wheel install, the declarations from
copied repository trees, nothing in the workspace touched.

Setup: `software_governance`, `business_domains` and `snapshot_inspector` copied to a scratch tree
without their `snapshot/` directories, profiles copied beside them, and the nine wheels installed
into a throwaway venv with `--no-index`. The repo `.sh` runners were deliberately **not** used —
they put the workspace `protocol_compiler` on `PYTHONPATH`, which would have defeated the test.

| step | result |
|---|---|
| platform compile | 187 artifacts, verified, attested |
| inspection compile | 49 artifacts, verified, attested |
| `ai_governance` compile | 63 artifacts, verified, attested |
| assemble under `GOVERNANCE_SURFACE_PROFILE_V0` | 3 domains, `c19f8593…`, round-trip OK, conformance PASSED over 245 artifacts |
| warm boot | 3 domains resident and hash-verified, provenance bound |
| `WF_GOVERN_AGENT_ACTION_V0` | SUCCESS |

Module origins were checked rather than assumed: `compiler`, `assembler`, `runtime`,
`capability_transforms`, `ai_governance` and the executed CT all resolve under the test venv's
`site-packages`. The platform capability layout is `capability_transforms.implementation.*` and
`capability_side_effects.implementation.CS_*/runtime` — worth writing down, since the plausible guess
`capability_transforms.atoms.*` is what the *domain* namespaces use, not the platform.

**What this establishes and what it does not.** The packaged distribution can build and run a
composition including a business domain. It still says nothing about installing from PyPI itself, or
about any platform or Python other than macOS/arm64 on 3.12.

### Five test suites existed that nothing ran, and two of them were red

`regression.sh` invoked ten checks and left five test files on disk unrun. Two were failing, and had
been failing unnoticed for exactly that reason. All five are now in the check block.

**`test_governance_provenance.py` — 2 of 4 red, and the system was right.** `content_hash` is taken
over the machine block *parsed and canonically serialised*, so prose declares nothing (MB-1) and a
YAML comment is invisible to it. The test perturbed by appending a comment, so the governance-closure
hash could not move: `SENSITIVITY` failed, and `ENFORCEMENT` failed as a consequence because there
was no drift for assembly to catch. Finding a working perturbation took three attempts and each
failure was informative — an added key is refused by `ASSERT_SCHEMA_CONFORMANCE_V0`
(`additionalProperties: false`), and so is a repeated enum member. **No semantically-inert
perturbation of an invariant exists**, because the schema is closed and every declared field carries
meaning. The test now changes a real declared value, `core.violation_response`
`FAIL_IMMEDIATELY` → `WARN`, restored immediately. 4/4 pass.

**`test_warm_boot.py` — 2 failures, one stale test and one real defect.** The stale one asserted that
`_composite_hash(manifest["domains"])` equals the manifest's claim, using a runtime helper boot had
already stopped calling: the assembler's composite covers constituents and the claimed profile as
well, so the runtime's weaker version could never match. Removed, along with `_identity_view`, and
`assembler.core.compute_composite_hash` which was a third unused duplicate of the same
determination.

The real one: **acceptance evaluated `snapshot_id` and never `composite_hash`**, so a manifest could
carry two contradictory identity claims and boot. Measured, not hypothesised — `composite_hash` set
to `deadbeef…` was accepted, while `snapshot_id` and `profile` were both refused. `verify_snapshot`
now evaluates both. 6/6 pass.

### The closure check had a blind spot, and the first fix for it was wrong

`governance_closure` reported *"89 in the registry, 97 named by an invariant"* and passed, because it
only computes `live − named`. The other direction looked like eight dangling handler names, seven
under `pgs_governance.*` — which read as RI-0 residue surviving the severance.

**It was not.** `pgs_governance.registry.handlers.*` is the live key namespace of the current
compiler: all 89 entries in `HANDLER_REGISTRY` use it. It is a string key, not an import path, and
`pgc_env_check` is right that nothing imports `pgs_*`. Adding the obvious `named − live` check would
have failed eight times, at least five of them false, because the extractor deliberately records both
the `handler:` override and the convention-derived name and only one need resolve.

Two of the eight were real, and both were the same bug: the extractor read raw file text. `workflow:`
came from a **violation example** in `INVARIANT_SUPERSEDED_NOT_REFERENCED_V0` — an illustration of
what not to do — and `constitution_invariants_v0` from a substring match on a constitution's prose.
It now parses the `## Machine` block, as the compiler does. That fix broke the check on first
attempt (orphans 0 → 3): the `handler:` override lives under `assert_projection`, and reading raw
text had made the nesting invisible. 97 → 95 named, orphans 0.

Also removed: a duplicated `rules[]` row in `CONSTITUTION_ASSERT_V0` declaring one obligation twice.
That is a real declaration change, so the snapshot identity moved — `1194598a…` → `d92b447f…`. A
stable identity there would have meant the edit was not reaching the snapshot.

`INVARIANT_ASSERT_CAPABLE_OF_REFUSING_V0` has no handler and needs none: it declares
`enforcement_stage: [declared_not_enforced]` with `enforced_by` naming the constitution that carries
the obligation where the build does not.

### The regression now cleans what it claims to clean

`--build` deleted only `$W/snapshot`, so a domain's stale `compiled/` survived and was reported by S8
as an undeclared output — which reads as a compiler defect rather than as stale state. It now removes
every generated snapshot.

`pgc_release/snapshot` is excluded **and the exclusion is asserted**: the script aborts, naming
`git restore`, if the cleanup ever removes it. That directory was deleted once by a hand-typed
command during this cycle and recovered only because it is committed. It is not reproducible — the
claimed profile changed and the assembler's index changed, both of which feed identity.

`.DS_Store` is now swept workspace-wide. macOS writes one into any directory Finder opens; acceptance
then refuses the snapshot as carrying undeclared content (3b §6), which makes a DOI-cited release look
corrupt when nothing about it changed. It broke a boot three times in one day, twice on
`pgc_release/snapshot`. Thirty-two existed at the time of the sweep and none is tracked in any repo,
so removing them can destroy nothing.

### Documentation aligned, and `doc/` is ephemera only

Seven component READMEs shared one paragraph crediting `PGC_BUILD_ROOT` with keeping the governance
repo read-only. Nothing reads it. Replaced with the anchors that matter, the `PGC_DOMAIN_ROOTS` depth
trap, the per-domain `PGC_SNAPSHOT_ROOT` rule, and a pointer to `pgc_install`.

Documents cited by code moved out of `doc/`: `snapshot_assembler/CONTRACT.md`,
`protocol_transport/TRANSPORT_STANDARD_V0.md`, `transformation/THE_SHAPE_OF_A_CHANGE_V0.md`,
`software_governance/rulings/` and `software_governance/surface_map/`. Twenty-one files had citations
rewritten. Two spent plan addenda were deleted. What remains under `doc/` is pending-decision
analysis — `MACHINE_BLOCK_CLOSURE.md` and `REGISTER_COVERAGE_VERIFICATION.md` — plus `.github/doc/`.

`release.sh` claimed pyproject versions derive from `VERSION`. They never did — all nine are
hand-edited literals, which is how `3.0.0` came to name two byte sets. The comment is corrected and
preflight now **asserts** each pyproject's major against `PUBLIC_VERSION`, so a repo left on the
previous identity's number fails the cut instead of reaching PyPI.

### `doc/` carries only what is still open

`doc/` holds ephemera awaiting disposition — nothing in it is read by code or cited by a paper, and
that was verified rather than assumed for all three files it held.

`parked_rulings.md` had drifted: 545 lines, eighteen entries, of which **thirteen were settled** —
DELIVERED, RATIFIED, SETTLED, RULED, narrowed and upheld. A parking lot and a rulings archive sharing
one filename. The settled thirteen are removed and the file is 176 lines over five open items.

**Each deletion was verified absorbed before it was made**, because a settled ruling can carry a
standing constraint and deleting an unapplied one would destroy the only record that the spec is
wrong. Four needed checking against the standard and all four had shipped: `SU-5`'s narrowing is at
`4e:205` in the exact words the ruling prescribed; `IN-14` sits at `5b:337` as the ruling described;
twenty-six normative documents carry the conformance section the ruling required; and `2d` §1 states
the kind-enumeration ruling verbatim.

`e0_ruling_3_brief.md` is deleted. It was evidence for a ruling that has since been made and recorded,
so it was residue rather than a pending item.

**One live item was rescued from a deleted ruling.** The kind-enumeration ruling carried a
forward-pointer: the canonical-kind list stays working material *until a normative platform profile
exists*. `GOVERNANCE_SURFACE_PROFILE_V0` now exists and declares `required_governance.artifact_kinds`,
so the trigger has fired. It is re-parked in its own right rather than lost inside a deletion.

Deleting also orphaned the `# Rulings from the realization-map pass` header, which introduced three
rulings that no longer exist; it is removed.

### Start here next session

**The mock upload to TestPyPI — prerequisite 6.** It is the only remaining thing testable before a
version number is committed to, and the one path nothing else exercises: metadata acceptance, name
resolution, and whether the nine `==` pins resolve against a live index rather than `--find-links`.
It needs a TestPyPI account and token.

Two items remain decisions rather than work, and both can wait: whether anything should read the
profile's §3 obligations (`GS-1`–`GS-3` are stated and unchecked, because `verify_profile` reads only
`required_governance` and `required_workloads`), and whether a consuming domain should publish under
the authoring identity at all — the duplication whose symptom is fixed and whose cause is not.
`bound_paths_declared_as_stores` is still undiagnosed.

The version bump is last, and preflight now enforces that: it refuses any pyproject whose major
disagrees with `PUBLIC_VERSION`.

### What was published

**Nine distributions on PyPI at 3.0.0** — eight components plus `protocol-governed-computing`, which
pins them into one composition. `pip install protocol-governed-computing` obtains the toolchain in one
command; the governance surface is still a separate step by design.

**Ten repositories published as `v3`**, each carrying one orphan commit on `main` at composition
ordinal 15, snapshot `3e81773b…`. Nine Zenodo component DOIs minted. The composition deposit is
`10.5281/zenodo.22578424`, naming those nine as `hasPart` and referencing the standard at
`10.5281/zenodo.22150616`.

### Three things a later reader will need

**The deposit's ordinal runs one ahead of its components.** `pgc_release` v3 seals ordinal 16;
the component `v3` tags declare 15. All seven graph addresses are byte-identical across the two, over
the same 595 constituents and 410 artifacts — only the embedded ordinal differs, and the ordinal is a
constituent. Cause: `release.sh --publish` increments `VERSION` as its last act, and the workspace was
rebuilt after that and before composing. `pgc_release/MANIFEST.md` records it in full. Avoid it next
time by composing before rebuilding, or from a tree checked out at the tag.

**`v2` could not be reused, and that is recorded in `publications.md`.** The distributions published
under 2.0.x were built from cycle 15 and carry the runtime refusal guards; the commit tagged `v2` is
cycle 13's and does not. The documented mapping had already broken before this cycle declared
anything.

**Two release-tooling fixes were needed and both are on `dev/16` only.** Zenodo now caps an
unauthenticated page at 25 records, so the single 100-record request in `compose_release.py` failed
the whole composition; it pages now. And the standard was located by filtering author-scoped records,
which failed because that deposit carries no ORCID — it is resolved by concept DOI directly. Neither
fix is in the published `v3` tree, which was sealed before they were written.

### Build & Test Status

**PASSING** at the point of freeze. `pgc_env_check` clean · `implementation_closure` 28 transforms ·
G4 suite 22 tests · warm reboot 7 domains hash-verified · composition conformance PASSED, 5 rules over
410 artifacts · `pip install protocol-governed-computing==3.0.0` resolves all nine and runs.

### Where work continues

`~/omnibachi-site` — the paper series, including the ASE submission in `doc/`. Its own handoff.

`standards` — the normative specification, outside this release cycle and on its own revision track.
Its own handoff. Moving it beside `omnibachi-site` is under consideration; nothing in the tooling
references it by path, only by concept DOI.

### State at freeze

Ten repositories on `dev/16` at `VERSION 16` — a cycle cut and deliberately not published, the same
pattern as cycles 12 and 14. `PUBLIC_VERSION` is `v3`. `pgc_install` and `pgc_release` are `main`-only.
The public surface is one commit and one tag per repository.

---

## v3 declared, family renamed and rebuilt at 3.0.0, ASE paper style pass — 2026-09-06

Everything below is committed-ready and **nothing has been published yet**. The nine distributions
are built at 3.0.0 and await upload; `release.sh --publish` awaits the commits.

### Changes Made

**Nine `pyproject.toml` → 3.0.0.** The family had drifted to a 2.0.0/2.0.1 split, which contradicted
the lockstep claim its own READMEs make. One version across all nine restores it.

**`pgc_install` publishes as `protocol-governed-computing`.** PyPI rejects the short name outright —
*"The name 'pgc' isn't allowed"* — so the composition takes the full project name. The import package
and the `pgc` command are unchanged, and this removes the need for the separate alias package that
was previously planned: one name, held by the meta-package itself.

**`.github/PUBLIC_VERSION` → v3.** See below for why v2 could not be reused.

**Collateral swept.** Ten files named the old distribution or the old public identity: seven component
READMEs (`pip install pgc`), `pgc_install/README.md`, the workspace `CLAUDE.md`, and
`process/notes/release-15.md`, which shipped a claim that the meta-package was held by a rate limit.
Eight READMEs also declared *"`v2` is `2.0.0`"* and *"the platform is at `v2`"*. All corrected.
`pgc_release/.zenodo.json` carried `"version": "v2"` — Zenodo reads that when the tag push fires the
mint, so a `v3` deposit would have carried `v2` metadata.

**ASE paper** (`~/omnibachi-site`, separate repo): reconciled against a 15-patch compression review,
converted to Springer decimal headings, name-year citations and a 17-entry alphabetized reference
list, exhibits renumbered to consecutive citation order, mutation-testing lineage cited, AI-tools
disclosure added to §3.3, and a two-pass direct-style edit taking passive voice from 26% to 22%.

### Build & Test Status

**PASSING.** `pgc_env_check` clean · `implementation_closure` 28 transforms · G4 suite 22 tests OK ·
runtime warm reboot 7 domains hash-verified at `3e81773b…` · `twine check` 18/18 artifacts.

`release.sh --check` fails only on uncommitted changes in nine repos — the expected state before
committing.

### Open Issues

1. **Eleven repos uncommitted**, then upload nine to PyPI, then `--publish`. Order matters: publishing
   first would push READMEs advertising 3.0.0 while PyPI still serves 2.0.x.
2. **PyPI 2.0.x remains published** and now names no public identity. Harmless, and cheaper than the
   alternative of reusing v2.
3. **Appendix B.1 of the paper cites dev SHAs that are not publicly reachable.** `release.sh`
   publishes an orphan commit and keeps `history-N` local, so `7848e70` and its nine siblings resolve
   nowhere. After `--publish`, B.1 must be re-pinned to the `v3` tag and the orphan SHAs.
4. Preprint DOI before Springer submission; then the submission itself.

### Architectural Concerns

**v2 could not be reused, and the reason is the project's own doctrine.** The publish guard blocks it
mechanically — the tag exists locally and on origin for every repo. But the substantive reason is
stronger: git `v2` is release 13's orphan and contains no `CSExecutionError`, while PyPI 2.0.1 ships
it. The documented mapping *"`v2` is `2.0.0`"* was **already false** before this cycle. Republishing
different content under `v2` would make a minted DOI resolve to something other than what it named —
the exact integrity failure content-derived identity exists to prevent.

**The reproducibility surface has a gap the paper inherits.** Development SHAs are not publishable by
design, so any document that pins a repository by dev revision cites something no reader can fetch.
The public tag and the orphan commit are the citable pair.

### Next Session Should Start With

**Commit the eleven repos, then `twine upload */dist/*`, then `release.sh --publish`.** After the
mints, `--publish-composition`, then re-pin Appendix B.1 to the published `v3` tag and orphan SHAs.

---

## PyPI family published, four external-boundary defects fixed, ASE paper reconciled and pinned to ordinal 15 — 2026-09-05

Two threads ran together: publishing the `pgc-*` distributions, which exposed real defects at the
boundary where PGC code loads external code; and a full reconciliation of the ASE paper against two
independent reviews.

### Changes Made

**`protocol_runtime`** — `runtime/ct_executor.py`: guarded `importlib.import_module` and `getattr`
on sealed handler_refs; added `CTArtifactNotFound` (`CT_ARTIFACT_NOT_FOUND`). Distinguishes an absent
handler module from an absent *dependency* of one, via `ModuleNotFoundError.name`.
`runtime/dispatcher.py`: same guards for the CS path plus the constructor and `execute()` call, with
`CSExecutionError` (`CS_EXECUTION_FAILED`); added `_violation_payload`; `_execute_ct_step` no longer
returns `VIOLATION, {}` — it had been discarding every CT refusal message. `pyproject.toml` → 2.0.1.

**`snapshot_assembler`** — `pyproject.toml`: `dependencies = ["pyyaml"]` (was `[]` while
`core.py:313` imports yaml on the `verify_snapshot` path); → 2.0.1.

**`business_domains`** — `pyproject.toml`: `pycryptodome` moved to a `blockchain` extra; → 2.0.1.

**`pgc_install`** — `pyproject.toml`: pins moved to 2.0.1 for assembler/runtime/domains; added a
`blockchain` extra passing through to `pgc-domains[blockchain]`. **Uncommitted.**

**`~/omnibachi-site/doc/`** (committed, branch `release/5`) — ASE paper reconciled against
`review_luna_ase_draft.md` and `review_expert_ase_draft.md`; author block and 16-entry References
added; re-pinned to composition ordinal 15 / `3e81773b…`; appendices made free-standing and
renumbered. 14 figure SVG+PDF pairs updated.

### Build & Test Status

**PASSING.**

- `pgc_env_check.py` — PASSED, no RI-0 dependency reachable
- `implementation_closure.py` — PASSED, 28 transforms
- G4 suite (`test_transform_npp_e` + `test_npp_e`) — **22 tests OK**
- Runtime warm reboot — 7 domains resident and hash-verified, `3e81773b…`
- `release.sh --check` — build gate **ok** (clean rebuild + assemble + composition conformance
  PASSED, 5 rules over 410 artifacts). **Preflight FAILS on one item: release notes missing.**

All ten workspace repos on `dev/15`, VERSION 15, clean. `pgc_install` on `main`, one modified file.

### PyPI

Eight component distributions published; three at 2.0.1 (`pgc-assembler`, `pgc-runtime`,
`pgc-domains`), five at 2.0.0. `pgc` meta-package **not yet uploaded** — new-project rate limit, due
when the 24h window opens. Loose `>=` pins between components mean no cascade was needed. Local
`dist/` cleaned in the eight pushed repos; `pgc_install/dist` preserved for the pending upload.

### Open Issues

1. **`.github/process/notes/release-15.md` does not exist** — the only preflight blocker. Content,
   author's to write.
2. **`pgc` upload pending**, then `release.sh --publish`, then wait for Zenodo mints, then
   `release.sh --publish-composition`.
3. **`pgc_release/snapshot` holds `4a1e8896…` at assembler_version 13** — two cycles stale until the
   composition phase runs.
4. **`dispatcher.py` CS lane and `ct_executor.py` are fixed; no other dynamic-import site exists** in
   the five packaged repos. The ~25 unguarded `json.load`/`yaml.safe_load` hits are in `scripts/`,
   which ships in no wheel — verified against the built artifact.
5. **ASE paper**: `zenodo.21879516` unverified before citation; the anchor's v1/v3 label; Zenodo
   affiliation change to *Independent Researcher* across ~22 records.
6. **Reference venue strings unverified** — authors/titles/venues recorded, but page numbers, DOIs and
   proceedings strings need checking against published records at bibliography time.

### Architectural Concerns

**Promotion is not an enforced transition, and the paper now says so.** No `promote` callable exists
anywhere in the toolchain. Admission is enforced by compilation; sealing is enforced against admission
by `assembler/core.py::_domain_identity`. Promotion is the operator's act of running assembly. This
propagated into §5.5, §8.2, §11, Table 4 (split into Admission / Promotion / Sealing rows) and Figs.
3, 4, 8, 10, 12, where every promotion transition is now dashed and labelled *operator adoption*.

**Four count errors were found by reading the implementation rather than the prose.** Table 3 had
P2=10, P4=11, P5=10 registers; the templates carry 8, 7, 8. P7 names four inspection operations, not
three. Separately, the demonstration total was 15→16 in the run's evaluation record but 21→22 in the
retained files; the artifacts won and the discrepancy is documented rather than reconciled.

**The G4 successor identity in `transformation_evidence.md` is stale.** It records `f4220813…`; the
retained code reproduces `48fd5a4d…`. There is no two-snapshot chain — `LibraryRuntime` is constructed
from `transform()`'s return value. The workflow gained routes during the execution work and the
evidence note was never restated.

### Next Session Should Start With

**Write `.github/process/notes/release-15.md`.** It is the only thing standing between the current
state and `release.sh --publish`, and the recommended order is: upload `pgc` → write and commit the
notes → `--publish` → wait for mints → `--publish-composition`. Publishing before the `pgc` upload
would put seven READMEs promising `pip install pgc` onto `main` while that command 404s.

---

## ASE paper — figures and tables drawn, no prose. **14 figures and 5 tables built for *Protocol-Governed Human–AI Software Engineering: Autonomy Without Authority*, targeting Springer ASE. Reading `rules.py` changed the paper's central structure.** Next: six decisions listed below, then prose.

Figure-first authoring, deliberately. Nothing is drafted; the spec says what each section must contain
and the exhibits are built so the prose can be written to them.

### Where it lives

All under `~/omnibachi-site/doc/` — **staged, uncommitted**. Outside the workspace; `release.sh` does
not touch it.

| | |
|---|---|
| `ase_writing_spec.md` | 4,711 w — 11 sections with word targets, figure/table index, seeds, inherited-vs-new |
| `ase_tables.md` | 5 tables built from the implementation; 2 flagged redundant with figures |
| `figures/*.svg` + `.pdf` | 14 figures, portrait, all within 6×9 in (largest 8.65) |

Author in SVG, deliver PDF. The Springer template (`parkinglot/sn-article-template`, v3.1 Dec 2024)
uses `graphicx` under pdflatex — **SVG will not compile on their side**. One `.tex` file, no
`\input{}`, figures attached separately.

### What changed the paper

**P0–P8 is not a ladder.** The declared priors, read from each phase's
`transformation/transformation/design/p*/rules.py`, are two branches from one root:

    P0 → P1 → P2 → P3 → P4          modelling branch — verifies, and terminates
     └──────────→ P5 → P6 → P7 → P8   intent branch — determines
                    ↖ P0 cited directly by P5, P6 and P7

**The intent phases never read the analysis** — P5's prior is P0, not P4. **Nothing declares P4 a
prior at all.** The source gives the reason: carrying the seed forward "would mean a register and a
carry rule in each intermediate phase, restating what the seed already says — and free to drift from
it." Anti-drift by *not restating*. Fig. 6 and §4.2 were rebuilt on this; the earlier ladder sketch
is superseded.

Rule counts locate the weight: 3–12 rules per phase, **70 at P7**. Only P2 declares
`GROUNDING_RULES`.

### The anchor, and two things it settles

***Protocol-Governed Systems: Closed-Loop Governed Evolution***, `10.5281/zenodo.21434335`, v3.
The PGC-titled local draft is its renamed successor and is not separately deposited.

- **The property already has a name.** §11: *"authority invariance with respect to the authoring
  actor."* Use it; do not coin a rival vocabulary. Its formulations — *"Authoring is interchangeable;
  authority is not"* and *"The actor proposes; governance disposes"* — are better than paraphrase.
- **A two-actor demonstration already exists.** One change cycle run by a small local model and a
  frontier model against an identical scaffold: *"The drafts differed… The governance did not."*
  §10 now states worker diversity as three facts — this cycle used one model; prior work used two;
  neither covers an actor operating outside the scaffold.

### Decisions waiting

1. **Fig. 11 vs Table 2** — component mapping is in both; strip one.
2. **Fig. 14 vs Table 6** — mutation ledger is in both; convention puts logic in the figure, data in
   the table.
3. **Table 1's four AI-approach rows** need representative citations; not invented.
4. **The Zenodo record** — the local draft labels `21434335` as v1, Zenodo says v3; and the record
   carries affiliation **Strad Research** against the IEEE byline *Independent Researcher*. The
   constitutional paper's records (`20272695` v1, `20330650` v2) carry it too.
5. **Verify §11's two-actor claim in the source** before §10 relies on it.
6. **IEEE Fig. 1 caption** — "two human acts" undercounts; the SVG marks three (scope, problem,
   promote) and the caption drops the authorizing one. One word, Word-stage, on `release/4`.

### Build and test status

**Not applicable — no code changed.** Workspace repos untouched this session.

### Next session should start with

Reviewing the 14 figures and 5 tables. **No prose until they are settled** — the whole method is that
the text is written to the exhibits. Decisions 1 and 2 come first, since they change what two figures
contain.

---

## PyPI packaging swept, regression clean. **Eight repos packaged as `pgc-*` at 2.0.0 plus a `pgc` meta-package; fifteen wheel defects found and fixed, every one invisible to editable installs. Full clean rebuild reproduces `72404ce4…` bit-for-bit.** Next: a git repo for `pgc_install`, then upload.

### What shipped

| Distribution | Repo | Command |
|---|---|---|
| `pgc-compiler` | `protocol_compiler` | `protocol_compiler` |
| `pgc-transformation` | `transformation` | `tc` |
| `pgc-runtime` | `protocol_runtime` | `protocol_runtime` |
| `pgc-inspector` | `snapshot_inspector` | `si` |
| `pgc-assembler` | `snapshot_assembler` | `snapshot_assembler` |
| `pgc-governance` | `software_governance` | — |
| `pgc-workloads` | `conformance_workloads` | — |
| `pgc` | `pgc_install` (new) | `pgc` |

All eight build, install into isolated venvs, and resolve as a set from the wheel index alone.
`pgc_install` is the composition as installable software, the counterpart to `pgc_release` as sealed
evidence — the parallel is role, not citation, and it takes no DOI.

### Defects found — none visible from the source tree

The acceptance criterion for every package was a **clean green-field wheel install**, not an editable
one. That distinction found fifteen defects:

- **`pgc-compiler` shipped no governance engine.** The hardcoded `packages` list had fallen eight
  behind the tree, omitting `compiler.governance_engine` and every assertion handler under it.
- **Four unreachable-`VERSION` bugs.** `COMPILER_VERSION` and `ASSEMBLER_VERSION` read the repo-root
  `VERSION`, which no wheel has; both failed at import. Package-data globs then missed the
  extensionless file even after the read was fixed.
- **Five undeclared dependencies.** `pgc-transformation` named one of four — `click`, `yaml` and
  `runtime` were satisfied only by the shared dev venv. `pgc-workloads` omitted `runtime` likewise.
- **One dependency named a pre-rename distribution** (`snapshot_inspector`), which after the sweep
  resolves to nothing on PyPI or to a stranger's package.
- **`transformation/templates/` lived outside the package** — nine phase templates the P0–P8 pipeline
  reads at run time, which no wheel would have carried. Moved inside; nothing else referenced them.
- **`.DS_Store` files inside a package**, and the retired **PGS** name in the compiler's CLI banner.

### Versioning — corrected before commit

**Two schemes, not three.** Each repository's `VERSION` is a monotonic composition ordinal, internal,
tagged `release-<N>`, never published. `PUBLIC_VERSION` is the platform's public identity, tagged on
every component repo. **The packages publish the public one: `v2` is `2.0.0`.**

The packages were first cut at `1.0.0` on a mistaken reading — that the published version tracked the
*standard*, which is at `v0`. It does not: the standard is a separate artifact on its own track
(`draft-1`…`draft-3`, then `v0`), while the platform went `v1` then `v2`, and every component repo
carries both tags. Caught before upload; a PyPI version can never be reused or deleted, so `1.0.0`
would have sat there permanently, one release behind the repos it packages.

### The VERSION ruling

`COMPILER_VERSION` is the **composition ordinal**, not a package concept: eleven repos carry it at a
uniform root path and `release.sh` refuses any repo whose `VERSION` disagrees. Moving it package-local
would make `release.sh` learn eleven paths, and four repos have nowhere to put it — `software_governance`
has two top-level packages and no canonical one; `pgc_release` and `standards` are not Python packages.

Resolution: the repo-root `VERSION` stays the single **authored** declaration; `_build_hook.py` stages a
copy into the package at build time; the copy is **gitignored**, regenerated every build, never edited.
One tracked file, nothing to synchronise, `release.sh` untouched. Two packages need the hook
(`pgc-compiler`, `pgc-assembler`); the others never read `VERSION`.

### Green install is two steps, by design

`platform_root.py` resolves the governance surface from **`PGC_PLATFORM_ROOT`** — "fail-hard,
cwd-independent, zero inference" — so declarations come from a repository the operator points at.
**No wheel ships a registry**: one inside a package would be a second governance surface competing with
the repository's. Wheels carry importable implementations; the registry stays repo-side. All eight
READMEs say so, and `pgc` reports both halves and exits non-zero when unanchored.

### Regression — full clean rebuild from deleted `snapshot/`, `data/`, `traces/`

**`snapshot_id 72404ce469c8987efa83d9a68cb3d517e2b9b571204bf7087b696a25abc46c99` — identical to the
pre-packaging composition, and stable across two rebuilds.** Packaging changed no governed behavior.

7 domains compiled, all verified and attested · composition conformance PASSED, 5 rules over 410
artifacts · `governance_closure`, `governance_chain`, `supersession_agreement`, `human_block_fidelity`,
`evidence_determinism` PASSED · `emit_rule_sets`, `build_payloads`, `author_transport_contracts`,
`frontmatter_fidelity` OK · `meta` (822 rules), `differential`, `e2e_phases` (83 cases), `projection`
PASSED · `construction_acceptance` **99/99 reproduced across 4 domains, 0 field differences** ·
`implementation_closure` PASSED, 28 transforms · `test_inspector` 121/121 · `pgc_env_check` PASSED ·
collatz `all_terminate: true` · ai_governance ×2 SUCCESS · catalog 23/23 and 21/21 · identity 15/15
(2 not exercised) · wallet 9/9 (1 not exercised).

`admission_contract_fidelity` FAILED on 31 findings — **the documented expected state**, at exactly the
documented count.

### Tooling added

`process/regression.sh` — the RUNBOOK's own sequence, scripted, because its one-line commands break
under terminal paste in ways that read like test failures rather than shell errors.
`regression.sh` runs the execution block, `--build` prepends a clean rebuild, `--all` adds the
seventeen checks. Expected results remain the table in `RUNBOOK.md` "## Expected".

### Open issues

- ~~**`pgc_install/` is not a git repo.**~~ **Done since.** `protocol-governed-computing/pgc_install`
  exists, `main`, and `d508db3 package for PyPI as pgc-* at 2.0.0` is pushed. Added to the repo table
  in `CLAUDE.md`, which had never named it.
- **Three one-line changes are staged and uncommitted in `pgc_install`** — registering the eighth
  package, `pgc-domains`, in `README.md`, `pgc/cli.py`, and `pyproject.toml`. `HEAD` is already
  pushed, so `git log` looks clean and this is easy to lose.
- **PyPI upload in progress — four of nine live.** `pgc-compiler`, `pgc-assembler`, `pgc-runtime`,
  `pgc-inspector` are published at 2.0.0 and verified. `pgc-governance` hit **HTTP 429** — PyPI's
  rate limit on *creating new projects*, not on upload volume — and nothing partial landed (still
  404). Remaining: `pgc-governance`, `pgc-transformation`, `pgc-workloads`, `pgc-domains`, then
  `pgc` last (it pins `==2.0.0` on all eight), then the `protocol-governed-computing` thin alias.
  **BLOCKED — waiting does not clear this.** Retried after 8 hours and got the same
  `429 Too many new projects created`. This is PyPI's limiter on *new project creation per account*,
  and it is a known obstacle for coordinated multi-package releases: reported cases have had to
  spread creation over weeks. PyPI does not publish the limit value or the reset window.

  **The remedy is to request a lift, not to wait.** Either email the admins (address on
  <https://pypi.org/help/>) or file at <https://github.com/pypi/support> using the *Limit Request*
  issue type — existing ones are titled `Limit Request: <username> — new project creation`. Include:
  the PyPI username; the four already published and verified (`pgc-compiler`, `pgc-assembler`,
  `pgc-runtime`, `pgc-inspector`); the five outstanding (`pgc-governance`, `pgc-transformation`,
  `pgc-workloads`, `pgc-domains`, `pgc`); and the coordination argument — `pgc` pins `==2.0.0` on
  all eight, so the family is unusable until every name exists. This is not nine unrelated uploads.
  Repo: <https://github.com/protocol-governed-computing>.

  Once lifted, resume with one batched command:

      twine upload --skip-existing software_governance/dist/* transformation/dist/* \
        conformance_workloads/dist/* business_domains/dist/*

  then `pgc_install/dist/*` on its own, then the `protocol-governed-computing` thin alias.
  `--skip-existing` makes the batch safely repeatable. Nothing is at risk in the meantime: no
  version numbers were consumed and `pgc-governance` is still 404.
- **Do not rebuild before uploading.** The verified `dist/` artifacts carry composition ordinal 14;
  the repos are now on `dev/15` at ordinal 15, so a rebuild would produce different, unverified
  wheels still labelled 2.0.0. Rebuild only from the `history-14` tag.
- **`si --help` with no snapshot** errors without explaining that a snapshot declares the commands, or
  naming `--snapshot` / `PGC_SNAPSHOT_ROOT`. Correct behavior, poor first-run message.
- **Three domains emit `⚠ Machine-block health: 1 candidate unconsumed key(s)`** — collatz, inspection,
  blockchain. Identical in all three, so structural rather than domain-specific. Not a regression.
- **Repo consolidation deferred** until after upload: moving repos invalidates the `Repository` URLs now
  in eight `pyproject.toml` files and eight READMEs.
- `UNCOMPOSED_PLATFORM_PROFILE_V0` §9 still unresolved — gates the uncomposed PNP build, not packaging.

### Papers

JOSS is closed until roughly March 2027: it requires six months of public history with issues and pull
requests, and every repo's `origin/main` is a single squashed commit from the v1 cut. The mismatch is
structural — JOSS rewards visible process, the release discipline seals finished work and discards
history. The transformation study goes to Springer *Automated Software Engineering* instead; the IEEE
special issue is the same one the architecture paper is already under review at, and two submissions from
one author to one special issue is not defensible.

**Parked — the ASE submission's scope.** The venue is settled: Springer *Automated Software
Engineering*. What is not settled is whether the study covers `transformation` alone or widens to
include `protocol_compiler`. Nothing blocks the decision and nothing waits on it.

**Parked — the ASE topic fit, decided.** Target the *Human-AI collaboration in software development*
topic, not the governance/LLMOps one. The spine: the design and construction compilers are a
collaboration model in which an agent derives every open step while the non-delegable decisions stay
human. The LLM queries the snapshot through the inspector for context — grounding in the literal
sense the call means — and the workers are producer-neutral by construction.

Two corrections to hold onto when drafting. **The shape is bookends, not a taper.** Human at the
start (scope, problem), agent through P0–P8 and construction, human again at the close (promotion,
deliberately not fused to construction). Describing it as oversight decreasing toward the end
contradicts Fig. 1 and undersells the claim: the two ends are exactly the decisions that cannot be
delegated — what to govern, and whether to authorize. **And the LLM angle is motivational and
evidential, not architectural** — PGC does not require a particular kind of producer. The connection
is that the problem exists because production became agent-mediated, and NOVA's workers were LLMs
with `run_conditions.md` recording which model played which role. Open on that, not on P0–P8
internals, or the paper reads as off-topic for an LLM-centric issue.

Leave `protocol_compiler` out for this venue: it strengthens a compilers paper and dilutes a
governance one.

**The Fig. 1 seam — resolved. The figure is right; the caption is wrong.** Read from the SVG
(recovered at `omnibachi-site` commit `e662ea8`), excluding the legend swatch, there are four solid
circles: `(60,170)` profile scope, `(60,356)` business problem, `(542,490)` promote/assemble/seal,
and `(828,666)` interactive actors in the execution band. So the figure marks **three human acts in
the governed lifecycle** — scope, problem, promote — matching the refrain exactly. The caption's
"the two human acts" undercounts, and it drops **promotion**, the authorizing act, which is the one
the whole thesis turns on. A reader counting dots finds three.

**Fix:** one word in the IEEE caption — "Filled circles mark the **three** human acts". The paper is
in Word on `release/4`, so this is a Word-stage edit, not Markdown.

**Also check:** the fourth solid circle marks *interactive actors* — humans using the system at
runtime, not authorizing it. If it shares the filled style incidentally rather than deliberately,
give it a distinct mark; otherwise the count stays ambiguous to anyone counting dots.

**Consequence for the ASE paper:** the collaboration model is **bookends with three acts**, the third
being the authorizing one. Fig. 2 there can now be drawn.

One consideration for whoever takes it up: the IEEE paper's §III-B already frames transformation as
**two** compilation problems — whether a design is admissible, then whether an admissible design can
be rendered into an artifact — and treats protocol compilation as the separate downstream step where
material violating the governing surface is refused. On that framing `transformation` alone is the
coherent unit, and adding `protocol_compiler` makes it three problems and changes the shape of the
argument rather than extending it. Widening may still be right; it is not free.

### Next session should start with

Commit the three staged `pgc-domains` lines in `pgc_install`, then the PyPI upload. The repo now
exists and its `HEAD` is pushed; the packaging work is done and verified, and nothing else blocks it.

---

## Plan change: packaging over validation. **NOVA2 deferred to the parking lot; the next work is PyPI distribution of the toolchain and a green-room install. JOSS ruled out for now; the transformation study redirected to Springer/ASE.** Next: add `pyproject.toml` to `software_governance`, then publish tier-1.

### The plan

- **(a) NOVA2 — deferred.** Setup is complete and parked: `~/nova2` holds the SOW, the transfer register and NOVA-1; `~/standard-build` is staged for a cold worker. `~/nova2/SOTU.md` carries the resume steps. Nothing in this repo depends on it.

- **(b) Tier-1 packages — five, all with `pyproject.toml` and a console script.**

  | Distribution | Repo | LOC | Command |
  |---|---|---|---|
  | `pgc-compiler` | `protocol_compiler` | 26,816 | `protocol_compiler` |
  | `pgc-transformation` | `transformation` | 13,599 | `tc` |
  | `pgc-runtime` | `protocol_runtime` | 5,892 | `protocol_runtime` |
  | `pgc-inspector` | `snapshot_inspector` | 3,174 | `si` |
  | `pgc-assembler` | `snapshot_assembler` | 1,699 | `snapshot_assembler` |

  All eight candidate names are free on PyPI. Namespace as `pgc-*` regardless: distribution name prefixed, import names unchanged.

- **(c) Tier-2 — `pgc-governance` is `software_governance` only.** It has **no `pyproject.toml`**; that is the first packaging task. It carries the governance surface and the capability-transform implementation modules the runtime binds at execution — without it the five tools have nothing to compile or bind.

  **`protocol_transport` is not folded in.** Transport splits: the 12 declarations (constitutions, invariants) live in `software_governance/registry/transport/` and compile into the snapshot; the code in `protocol_transport` is the HTTP adapter and is not required to build, seal, or execute one. It stays unpublished — its import roots are env-provisioned by design, and the transport standard is Phase-1 frozen with adapters unauthorized.

  **`pgc-workloads`** (`conformance_workloads`) is needed for a runnable demo: the profile requires `workload::WF_COLLATZ_CONJECTURE_V0`.

  **`pgc`** — a meta-package depending on the seven, providing one command that compiles, assembles, seals and runs collatz. That command is the green-room test and the developer's first five minutes; it is the deliverable, not a convenience.

- **(d) Papers.** JOSS deferred — see below. The transformation design/construction compiler study goes to Springer *Automated Software Engineering*, possibly widened to include `protocol_compiler`. TBD.

### Why JOSS is out

JOSS requires "at least six months of public history prior to submission, with evidence of releases, public issues and pull requests," and values open development over "private development followed by public release." Every PGC repo's `origin/main` is **a single squashed commit** — the deliberate outcome of the v1 publication cut. Earliest eligibility would be roughly March 2027, and only if development moves into the open from here. The deeper mismatch is structural: JOSS rewards visible process; the release discipline seals finished work and discards history on purpose.

### Versioning nuance

Three version spaces must not be conflated. The **standard** is `v1` with a DOI and is not revised by packaging (`8a` §2, direction of authority). The **repos** carry `VERSION 14`, which is embedded in snapshots as `compiler_version` / `assembler_version`. **PyPI semver** is a third. Publishing wheels as `1.0.0` while emitted manifests read `compiler_version 14` will confuse a reader — either publish at `14.x` or document the mapping.

### Evidence found while scoping

- **22 transformation runs, 14 complete P0–P8, across 4 domains** (`blockchain` 4/4, `book_library_mgmt` 4/4, `software_governance` 3/6, `transformation` 3/8): 209 documents, 415,552 words. Extractor at `scratchpad/extract_dossiers.py`.
- **Register counts track phase completion mechanically** — 9-phase runs carry 84–90 distinct registers, 7-phase runs exactly 63, across unrelated domains.
- **`transformation/testbed/phases/test_payloads/` holds 83 payloads: 69 inadmissible, 14 admissible**, P7 alone carrying 27 negative cases. This is the per-phase verdict evidence the dossiers lack — all 171 phase files record only `Status: DRAFT`.
- **`book_library_mgmt/cr_03_catalog`** documents a full block → resolve → resume cycle across domains.

### Open issues

- `software_governance` has no `pyproject.toml` — blocks tier-2 and therefore the green install.
- No `CONTRIBUTING.md`, issue templates, or CI in any repo.
- `transformation` tests live at `scripts/testbed/*_test.py` with no pytest config; the 83 payloads are not packaged (`packages.find` includes `transformation*` only).
- `UNCOMPOSED_PLATFORM_PROFILE_V0` §9 still unresolved — no closed TI/TE schema, short-form kinds emitted. Gates the uncomposed PNP build, not the packaging work.

### Next session should start with

Adding `pyproject.toml` to `software_governance` and building `pgc-governance`. Everything else in (b) and (c) is blocked behind it, and the green-room install cannot be tested until the governance surface installs.

---

## NOVA-2 separated from the workspace. **All NOVA material moved out of `.github` to a standalone local repo `~/nova2`; `8a` augmented into an architect's brief; the Realization Map rebased from `draft-2`/`94e9b9dd…` to `v0`/`72404ce4…` and extended over the twenty-four invariants `v0` added.** Next: decide whether the reference is fixed to satisfy `UNCOMPOSED_PLATFORM_PROFILE_V0`, or the profile is relaxed — the uncomposed PNP cannot be built until one of those happens.

### Changes made

- `snapshot_profiles/UNCOMPOSED_PLATFORM_PROFILE_V0.md` — **new.** A peer of
  `REFERENCE_PLATFORM_PROFILE_V1`, superseding nothing and deriving from nothing, over the
  uncomposed composition: `platform`, `workload`, `inspection`, `transformation`, no business
  domain. Settles what `4c` §8 assigns to a profile and what the reference profile left open — the
  27-namespace set declared and closed with `derives_concern: false`; a per-kind
  `governance_assertion` statement for all sixteen kinds (`KV-10`), set to `required` throughout
  because every artifact of every kind in both repos carries `governed_by`; `aliases_accepted:
  false`, stricter than `2d` §7 permits; domain profiles declaring authority-or-concern for all four
  domains (`DP-4`); and a `required_self_description` block (`SN-7`, `SN-14`, `CF-14`). §3 states
  the six checks the profile must fail on and the rule that a profile unread against a candidate
  snapshot may not be handed to anyone as a target. §6 declares `NP-7`'s status rather than
  asserting it: externality is authorship, not storage, so the invariant is unsatisfied for a claim
  by the profile's own author and satisfied for a realization built by another authority.
  `TRANSPORT_PROTOCOL_INDEPENDENCE` is not claimed — no wire protocol is exercised, and a claim
  discharged by a substitution that cannot be performed is not discharged (`CF-8`).
- `external_validation_nova/` (57 files) — **removed**, relocated to `~/nova2/nova1/`. NOVA-1 is
  retained as prior art in the new repo; nothing in it changed.
- `external_validation_nova2/SOW_NOVA2.md` — **removed**, relocated to `~/nova2/`. Directory gone.

Outside this repo, on `standards` branch `draft/5` (unpushed, two commits ahead of `origin/main`):

- `spec/8a_implementation_guidance.md` — 1,630 → 3,594 words. Five sections added and the existing
  spine renumbered (old §4→§7, §5→§10, §6→§11, §7→§12): **§4 the declaration surface is yours**,
  which states that `2c` §3's encoding neutrality and `2c` §6.1's *"not specified by this revision"*
  are a decision the implementer owns rather than an omission, with seven binding constraints and an
  explicit list of what is free; **§5 the problem inventory**, fourteen decisions each with what
  bounds an answer and none with an answer; **§6 order of construction**, seven dependency rows
  stated as implications rather than stages; **§8 the scope floor**, six obligations with the
  reference's arrangement excluded; **§9 falsification discipline**, every guard ships with a
  demonstration that fails when the guard is removed. §1 now states the annex's own rule: it names
  problems and declines to name solutions.
- `doc/realization_map.md` — subject restated to `72404ce4…` / `v0` / 7 domains / 410 artifacts /
  PASSED over 5 rules, the third statement of subject. The map had declared itself retired; it is
  un-retired explicitly, on the ground that its findings are now relied on for a second purpose and
  cannot carry that weight against an archived subject. **§0.1 rebasing record** — the coverage
  delta (`v0` added 24 invariants over `draft-2` and retired none, including the whole `CM-1 … CM-8`
  family) and a spot recheck of eleven findings by direct signature: 2 and 4 **closed**, 1 and 3
  **changed** (what sits outside the identity is now declared rather than incidental), 14 and 29
  **re-verify**, 13/24/30/33/39 **stand**, 45 **stands and is larger than recorded**. **§26A** maps
  the 24 additions: `CM-1 … CM-8` bind documents and not realizations and are demonstrated for the
  documents outside this map by `tools/vocab_index.py` (0 defects, 44 warnings); the other sixteen
  yield one Demonstrated entry (`SN-14`) and six new findings, **50–56**. Three of `v0`'s new
  invariants name mechanisms the map had already found (28, 31, 9), which is evidence the additions
  were written against real defects.

### Build & test status

**PASSING.**

- `python .github/process/pgc_env_check.py` → `PGC ENVIRONMENT CHECK PASSED — no RI-0 dependency
  reachable`
- `python .github/process/implementation_closure.py` → `IMPLEMENTATION CLOSURE PASSED — 28
  transform(s), every module named and present`

No code changed this session. The current snapshot is unmodified at `72404ce4…`, assembled against
`REFERENCE_PLATFORM_PROFILE_V1`.

### Open issues

- **The reference realization does not satisfy `UNCOMPOSED_PLATFORM_PROFILE_V0`**, recorded in that
  profile's §9 rather than accommodated. Two failures: `TRANSPORT_INGRESS` and `TRANSPORT_EGRESS`
  have no closed schema, which §7 requires under `MB-11`; and the compiled projection emits
  `CT`/`CS`/`CC`/`WF`/`IN`/`EV`/`TI`/`TE` alongside canonical names, which §5 refuses since the
  profile accepts no alias. The uncomposed PNP cannot be built and sealed until one of these moves.
- **`standards` `draft/5` is unpushed and must stay that way.** Its history carries material
  relocated to `~/nova2`; the current file contents are clean and the commits are not. A publishable
  branch should be built fresh from `main` plus the `8a` change rather than by rewriting this one.
- **Map findings 14 and 29 are marked re-verify**, not closed — `rglob` survives only in
  `protocol_compiler/scripts/`, and the admission text survives only as a comment in
  `protocol_runtime/runtime/trace_viz.py`. Neither may be cited as a closure until the sections are
  read against current code.
- `standards/doc/realization_map.md` §§3–26 remain measured against `94e9b9dd…` under `draft-2`.
  Only §0.1 and §26A are stated against the current subject.

### Architectural concerns

- **`NP-7` has no mechanical closure.** Externality is authorship, and no arrangement of directories
  or repositories establishes it. The uncomposed profile states its own status per claimant rather
  than asserting a property it may not have; whether that is the right shape for a profile is worth
  a ruling.
- **`CM-5` is unchecked.** Nothing compares an authored profile against the Conceptual Model's
  definitions, so that obligation is discharged by reading. Map finding 56.
- **`7a` §10's equivalence relation holds only over a shared snapshot** — *"given the same snapshot,
  inputs, and initial state."* Two systems that independently authored different snapshots under one
  profile have no stated relation in the family. Map finding 57, and genuinely open.
- The registry contains one artifact declaring a `blockchain::` FQDN inside the governance or
  workload surface. Noticed while enumerating namespaces for the profile; not chased.

### Next session should start with

Deciding the `UNCOMPOSED_PLATFORM_PROFILE_V0` §9 pair — fix `protocol_compiler` to emit canonical
kind names and author closed schemas for `TRANSPORT_INGRESS`/`TRANSPORT_EGRESS`, or amend §5/§7 of
the profile. Nothing downstream can proceed until the uncomposed PNP builds, and it cannot build
against a profile it fails.

---

## IEEE paper to submission-ready. **`gold_who_authorizes_software_behavior.md` passed two mock IEEE reviews plus a line-by-line pass; citations [1]–[18] closed and verified. Two items parked by decision, not oversight.**

The paper is the deliverable this session, not code. Nothing in the workspace repos changed except
the NOVA-2 SOW.

### Changes made

- `~/omnibachi-site/doc/gold_who_authorizes_software_behavior.md` (repo `omnibachi-site`, branch
  `release/4`, HEAD `ed0f0c5`) — all seven sections reviewed. Table I added (comparative matrix,
  five mechanism families x five dimensions); mutations table renumbered to Table II. `[17]` was
  orphaned when §V-B was removed and was deleted; `[17]`/`[18]` re-added as Jia & Harman (IEEE TSE
  2011) and Andrews et al. (ICSE 2005), the paper's first non-self citations past `[9]`. Defects
  fixed: PGC used before definition in Table I, a logic inversion in §VI ("unvalidated rather than
  untested" for a path never exercised), §V heading still saying "Beyond the Target" after §V-B's
  removal, "Four consequences" where only three follow from the property, `[Section IV-C]` as a
  bracketed non-numeric reference, two sentence fragments in §IV-C, unspaced em dashes, and
  `sealed` used 25 times without a definition.
- `.github/external_validation_nova/` — **restored, 57 files, byte-exact from `9db39f7^`.** Commit
  `9db39f7` had moved all NOVA material out to the `nova2` repo; the IEEE paper's §IV evidence
  depends on this tree, so NOVA 1 was put back where the paper expects it. Restored from git rather
  than from the preserved `~/g2-nova` copy, which is the G2 worker's flattened sandbox (with its own
  32-document `spec/`), not this folder structure. Staged, not committed.
- NOVA 2 material stays out of the workspace, in the private `nova2` repo (`~/nova2`): `SOW_NOVA2.md`,
  `nova1/` (a copy), and `transfer_register.md`. **`nova2` is private and its future is undecided.**
  `.github/snapshot_profiles/UNCOMPOSED_PLATFORM_PROFILE_V0.md`, added by `9db39f7`, is NOVA-2-era
  but **stays where it is** — it is a snapshot profile, and that is where snapshot profiles live.

### Build and test status

**PASSING.** No code changed this session. `python .github/process/pgc_env_check.py` →
`PGC ENVIRONMENT CHECK PASSED — no RI-0 dependency reachable`. Both repos clean:
`.github` on `dev/14`, `omnibachi-site` on `release/4`.

Paper audit: citations `[1]`–`[18]` map 1:1 both directions, first-appearance order monotonic, no
orphans, no bracketed non-numeric references. Cross-references resolve. Word count 5,160 text +
900 (Fig. 1 + two tables at 300 each) = **6,060**, roughly 5,935 in Word.

### Parking lot — two open paper items

Both are deliberate decisions with in-text cover, not gaps. Do not "fix" them without deciding to
change the paper's genre.

1. **End-to-end worked example.** Both mock reviews call for a 2–3 page walkthrough (genesis →
   transformation → execution) on a realistic domain. Declined: it turns an architecture-and-evidence
   paper into a tutorial and roughly doubles the length. Covered in §III-E — *"The standard [10]
   provides the detailed construction specification; this paper abstracts that machinery to expose
   the architectural argument."* Verified the standard contains no worked example, so that wording
   is the only defensible one.

2. **Comparative depth.** The one item flagged in *both* rounds, and the only one scored CONCERN.
   Table I answered round 1; round 2 wants 8–10 dimensions or a concrete failure scenario. If a real
   reviewer presses, the cheap answer is ~80 words in §I-C showing SLSA + OPA + admission control all
   passing while nothing carries the authorization determination — not the wider table. Budget exists
   for it.

Also declined, with cover: adoption guidance ("When PGC Is Appropriate"), covered by §VI's
*"Adoption conditions are not evaluated here"*; and a mutation score, which §IV-C declares absent
by design rather than omits.

### Architectural concerns

Two rulings the NOVA-2 SOW needs before it can run, both recorded in the SOW:

- **Transformation self-reference.** The uncomposed PNP contains `transformation` — the machinery by
  which the platform changes itself. A profile governing a platform that contains its own
  transformation pipeline brushes against the standard's own bar that a profile may not be authored
  by the system it governs. Settle before building.
- **Profile handover.** Give the worker the reference platform profile (making comparative
  conformance possible by construction, which closes a §VI limitation), or have them author one
  NOVA-style (which reintroduces the incomparability). Recommended: the former.

Also: the uncomposed PNP does not exist as a build. Both `snapshot/` (`72404ce4…`) and
`pgc_release/snapshot` (`4a1e8896…`) are the composed seven-domain build including the three
business domains.

### Next session should start with

If the paper: convert `gold_who_authorizes_software_behavior.md` to the IEEE Word template. Nothing
further is actionable in Markdown. Carry over — Index Terms becomes a run-in italic lead rather than
a heading; Tables I and II to IEEE typography (title above, no vertical rules, keep Table II's
right-aligned Demonstrations column, drop bold in cells); references to the template's style; and a
DOI audit of `[11]`, `[13]`–`[16]` against live Zenodo, which could not be verified offline (`[10]`
and `[12]` were verified against `pgc_release/MANIFEST.md`).

If NOVA-2: settle the two rulings above, then build and seal the uncomposed PNP and record its
snapshot id before any handover — that id is the commitment the worker's result is compared against.

---

## Citation closure. **The composition now has its own DOI. `pgc_release` created, tagged `v2`, minted as `10.5281/zenodo.22184748`; references [11] and [12] filled in the IEEE draft.** The paper's citations are closed. Next: verify external references [1]-[9].

The nine component repos already had DOIs. What was missing was an artifact identifying the
*composition* — §4.1 claims seven governed domains over 410 artifacts under one governance surface,
and no component DOI names that. The previous session's plan was a hand-typed Zenodo web deposit.
That was replaced with a tenth repository so the same GitHub-Zenodo integration mints it
automatically, like the nine.

### `pgc_release` — the sealed composition, published

| | |
|---|---|
| Repo | `protocol-governed-computing/pgc_release`, public, `main`-only |
| Commit | `184d465`, tag `v2` |
| Version DOI | `10.5281/zenodo.22184748` |
| Concept DOI | `10.5281/zenodo.22184747` |
| Contents | `snapshot/` (597 files, expanded not archived), `MANIFEST.md`, `.zenodo.json`, LICENSE/NOTICE, VERSION=13 |
| Deposit | 10 related identifiers verified on the record: 1 `references` (standard) + 9 `hasPart` |

The snapshot is committed expanded rather than as a tarball, so artifacts are browsable on GitHub
and diffable between releases. `snapshot/manifest.json` carries the id.

### Commit provenance — resolved, not a defect

The snapshot's `provenance.source_commits` do not match the `v2` tag commits in any of the five
artifact-contributing repos. Cause: `v2` tags are squash-merge commits on `main`; the snapshot was
assembled from `dev/14`. Verified same content — commit trees are hash-identical and
`git diff <dev-commit> v2` is empty for all five. Recorded in `pgc_release/MANIFEST.md`.

### Zenodo integration — the trap

Enabling a new repo takes **two** UI steps: select it into the enabled list, *then* flip the switch.
Sync alone does nothing. A release published before the webhook exists is lost silently — Zenodo
never receives the event. Recovery is `gh release delete` + `gh release create` on the same tag; the
tag survives. Check from outside with:

```sh
gh api repos/protocol-governed-computing/<repo>/hooks --jq '.[].events'
```

A working repo shows one hook on `release`.

### Zenodo account split — two accounts, one author

Discovered while checking the composition deposit. Two separate Zenodo accounts exist because two
signups happened — one via ORCID sign-in, one via GitHub OAuth. Not caused by the username
mismatch (`bachi` vs `bachipeachy`); Zenodo does not match accounts by name.

| Zenodo user | Holds | Dates |
|---|---|---|
| `1552470` | 21 records — the PGS/PGC paper series | 2026-02-20 → 2026-08-12 |
| `1552563` | 11 records — the standard, nine components, the composition | 2026-08-28 → 2026-08-31 |

**Citations are unaffected.** Every DOI resolves, and the ORCID lives in record metadata rather
than in account ownership, so one ORCID search spans both accounts. What is split is the
management surface: two dashboards, and the ten GitHub repo integrations exist only on `1552563`.

Zenodo has no self-service account merge — it would be a support request. **Decided: not merging.**
The split is accepted as the standing arrangement — `1552470` is the papers account, `1552563` is
the repo/GitHub account. Nothing is broken by it: DOIs resolve, and one ORCID search spans both.
A drafted request survives in the scratchpad as `zenodo_merge_request.md` if this is ever
revisited. If it is: merge INTO `1552563` so the ten webhooks survive, and never by re-uploading,
which would mint duplicate DOIs and fork the citation record.

### The standards record is missing its ORCID

`10.5281/zenodo.22150616` — reference [11] in the paper — has creator metadata
`{"name": "Ganti, Bhash", "affiliation": null}` and no ORCID, so it is the one cited record absent
from an ORCID search (31 of 32 records carry it).

Cause: `standards/.zenodo.json` was **not present at tag `v0`** — it was added afterwards in commit
`62ab860`, so Zenodo minted from fallback metadata. The repo file itself is correct and will apply
at the next standards release; nothing needs changing there.

**Decided: left as is.** The fix would be a metadata edit on the published record (metadata stays
editable; only files freeze), but it changes nothing that resolves — [11] cites the DOI, and the
DOI works. The consequence to know: this one record does not appear in an ORCID search, so an
ORCID-driven listing shows 31 of 32 works. The record reads revision 3, updated 2026-08-28.
Editing it requires being signed into `1552563`, which owns it.

### Changes made

| File | Change |
|---|---|
| `pgc_release/` (new repo) | Created, populated, committed, tagged `v2`, released, DOI minted |
| `.github/process/release.sh` | Gained `--publish-composition`, a second phase for `pgc_release` (it cannot join `REPOS` — its `hasPart` DOIs do not exist until the components are minted). Checks the Zenodo webhook before pushing |
| `.github/process/compose_release.py` | New. Regenerates `pgc_release` from the sealed snapshot; discovers component DOIs from Zenodo rather than keeping a declared list; fails hard when a part is unminted |
| `CLAUDE.md` (workspace root) | `pgc_release` row added to repo table; "Two snapshots, do not confuse" clause added |
| `.github/process/zenodo_composition_deposit.json` | Deleted — superseded by `pgc_release/.zenodo.json`. Had an uncommitted staged edit (404 to 410); content preserved in history at `ba92191` |
| `~/omnibachi-site/doc/draft_1_who_authorizes_software_behavior.md` | **The live paper.** [12] filled with `10.5281/zenodo.22184748` — the composition DOI, the reader's only route to the software. [11] already carried the standard DOI |
| `~/omnibachi-site/parkinglot/ieee_computer_pgc_draft_7.md` | Superseded draft, edited by mistake before the live paper was identified. [11], [12] and the open-item note were filled there too; DOIs are accurate but the file is scratch. `parkinglot/` is the author's temp storage, gitignored and periodically cleaned |

### Build and test status

PASSING.

- `pgc_env_check.py` — PASSED, no RI-0 dependency reachable
- `implementation_closure.py` — PASSED, 28 transforms, every module named and present
- Composition conformance (read from the sealed snapshot) — PASSED, 410 artifacts, 5 rules

The release-process code added this session (`--publish-composition`, `compose_release.py`) is
unexercised end to end — it cannot be until the next release cycle mints its inputs. What was
checked: `bash -n`, `--help`, argument rejection, and that the untouched `--check` path still
runs. `--check` currently reports 2 pre-existing failures (no `release-14.md` notes file;
`.github` dirty), neither caused by this change.

### Open issues

- `.github` has an uncommitted working-tree deletion: `process/zenodo_composition_deposit.json`.
  Finish with `git rm --cached process/zenodo_composition_deposit.json`.
- Workspace-root `CLAUDE.md` is not under version control (the root is not a repo) and is not
  backed up. The live paper under `omnibachi-site/doc/` **is** tracked; only `parkinglot/` is
  gitignored, and that is the author's temp storage by design.

### Architectural concerns

`pgc_release` deviates from the workspace convention deliberately: `main`-only, no `dev` branch,
because it holds a sealed output with no development. If it is folded into `release.sh`, that
asymmetry has to be encoded rather than smoothed over — the repo must never be built from.

### Next session should start with

Verify references [1]-[9] in `~/omnibachi-site/doc/draft_1_who_authorizes_software_behavior.md`
(the live paper, not the `parkinglot/` drafts) against the
actual publications — author lists, venues, dates. It is the only remaining blocker on the
reference list, and the paper's own open-items list (item 2) names it. After that: Tables 1 and 2
from the cycle-1 ledger, the §2/§5 five-question wording sweep, and the Sigstore entry.


## Publication. **`standards` cut to a single-commit remote and given a DOI; the ten PGC repos cut the same way and tagged `v1`; ten working documents retired. Nothing is published that has a development history behind it any more.** Next: decide how development continues, because `release.sh` can no longer run.

The whole day's git work was one operation performed twice: build an orphan commit from the current
tree, force it onto `main`, and delete every other ref from the remote. Eleven repositories, all
history kept locally, nothing lost.

### `standards` — one commit on the remote, `v0`, and a DOI

| | |
|---|---|
| Remote | `main` + tag `v0`. `main` is `d55dc77`; **`v0` stays pinned to `dd8bb2c`**, the single publication commit |
| Zenodo | version **`10.5281/zenodo.22150616`** · concept **`10.5281/zenodo.22150615`** |
| Local | `draft/2`, `draft/3`, `draft/4`, six tags, complete history |
| Backup | `~/standards-full-history.bundle` — verified, *records a complete history* |

**The `v0` tag was on the wrong commit and nobody would have noticed.** It sat on `2fc8c36`, two
commits behind, so every `blob/v0` link in the call for review resolved against a tree whose
`call_for_review.md` was the *previous* version — a document pointing readers at a stale copy of
itself. Re-cut onto the publication commit.

**The DOI commit is deliberately the second commit on `main`.** Zenodo mints the DOI *from* the
release, so it cannot exist in the commit it describes. What that costs is nothing: Zenodo archived
the tag, and the tag still names the single-commit tree. The branch moved past the archive; the
archive did not move.

**Version DOI in `CITATION.cff`, concept DOI on the README badge.** Not the common default, which
makes the concept DOI primary so citations follow to the newest release. That default contradicts
the file's own `message:` — *cite the revision you read* — and a citation that silently follows to a
successor is what `4e` §9 and `0z` §5.1 rule out. A badge is a way in; a citation names a revision.
The two DOIs are interchangeable today and diverge at the next revision, which is exactly when
having them the wrong way round would start to matter.

### The ten PGC repositories — `v1`, and `VERSION` left alone

Same operation, ten times. Every remote now carries **four refs**: `HEAD`, `main`, `v1`, `v1^{}`.
Deleted: **105 branches** (`dev/2`–`dev/12`, three stray `v1.0.0` branches) and **186 tags**
(`release-2`…`release-11`, `history-2`…`history-11`).

**`v1` is a tag and nothing else.** The proposal was to write `v1` into `VERSION`. That would have
broken the release machinery on the same day it was repaired: `VERSION` carries the composition
ordinal, `release.sh` now derives the release number from `.github/VERSION` behind a guard that
refuses a non-integer, and `pyproject` derives from it too. The two questions — *which composition is
this* and *what is the public identity* — are different, and answering them with one field costs the
first. `VERSION` stays `12`.

**Orphaned from `dev/12`, not `main`.** For the nine code repositories the difference was one line;
for `.github` it was **61 files and 6,006 lines** — the entire NOVA cycle 1 record. Orphaning `main`
as it stood would have published a v1 with the validation programme missing.

**`protocol_runtime` had a `v1.0.0` branch *and* a `v1.0.0` tag.** A bare `--delete v1.0.0` there is
ambiguous. Every deletion was written `refs/heads/…` or `refs/tags/…` for that one repository's sake.

**The local repositories already held everything, under tag names rather than branch names.** Only
`main` and `dev/12` were ever checked out locally, so `dev/2` through `dev/11` looked like they
existed only on the remotes being cleared. They did not. `release.sh` tags `history-$RELEASE` at
`dev/$RELEASE` before deleting the branch, and those tags are local — `history-9`, `history-10` and
`history-11` were verified to pin exactly the `dev/N` tips the bundles carry. The old `main` squash
commits are likewise reachable through `release-2` … `release-11`.

**So the branch names are gone and nothing else is.** The commits they named are all present in the
live repositories. `~/pgc-backups/` is redundancy, not the sole copy — an earlier reading of this
session had it the other way round and treated the bundles as load-bearing. The branches were
deliberately not recreated: a `dev/9` branch invites the idea that it can be committed to, while
`history-9` says what it is, an archived cycle.

### Ten working documents retired, before the orphan rather than after

Cleaning after publication would have cost a second commit on `main` or a second rewrite; the orphan
takes whatever the tree holds, so cleaning first was free. Removed from `software_governance` (6),
`protocol_compiler`, `transformation`, `snapshot_inspector`, and `.github`.

**What was checked first was who cites what.** Six candidates were kept because something references
them — `THE_SHAPE_OF_A_CHANGE_V0.md` from `p7_design_intent/rules.py`, `rule_ownership.md` from
`SCHEMA_INVARIANT_V0.json`, and **`MACHINE_BLOCK_CLOSURE.md` and `parked_rulings.md` from
`standards/doc/realization_map.md`** — which by then was frozen at `v0` and could not be amended to
repair a dangling reference.

**`dossiers/` looked ephemeral and is not.** `RUNBOOK.md:166` has `construction_acceptance.py`
reproducing 99 artifacts *"from their delivered dossiers"*. Roughly 120 files that a check reads.

**`SOTU.md` was untracked with `--cached` and gitignored**, not deleted — the handoff survives
locally and is no longer published. This file is that arrangement.

### Consequences, in the order they will be met

**`release.sh` was left unable to run, and was rewritten the same session** — see below. It had
required `origin/dev/$RELEASE` to exist and be pushed, which no remote can now satisfy. It was not
broken so much as obsolete: it implemented the publication model that was replaced that morning.


**Offsite backup is the open exposure, not the bundles.** Everything deleted from the remotes is
still in the live local repositories via `history-N` and `release-N`, and `~/pgc-backups/` plus
`~/standards-full-history.bundle` are a second copy again. All of it is on one Mac. What no longer
exists anywhere off this machine is *work in progress* — `dev/12` and whatever follows.

**Nothing published has a development history behind it.** Deliberate, and it costs less here than
it would elsewhere: `revisions.md` carries the supersession relations in-tree, and the family holds
that supersession is declared rather than inferred — so the record of what superseded what never
depended on git.

**GitHub retains unreachable objects addressable by SHA**, and forks or caches may hold copies. What
was achieved is a clean presentation, not erasure. Fine for the goal; worth not overstating.

### The version scheme settled, and `release.sh` rewritten around it

**Two counters, neither derived from the other.** `VERSION` carries the composition ordinal — `12`,
per repository, monotonic, written by the release process. New `.github/PUBLIC_VERSION` carries the
public identity — `v1`, one declaration for the composition. New `.github/publications.md` carries
the relation between successive identities, the way `standards/revisions.md` does for the
specification.

| | `VERSION` | `PUBLIC_VERSION` |
|---|---|---|
| Carries | composition ordinal `12` | public identity `v1` |
| Scope | all ten repositories | one declaration, in `.github` |
| Advances | every cycle | only on publication |
| Derived from | nothing | nothing |

**Deriving the identity from the ordinal was the tempting mistake.** `v = VERSION - 11` would have
worked today and been an *inferred* relation — which `4e` §9 refuses for exactly this reason, and an
arbitrary offset between two counters is the undeclared relation this family objects to everywhere
else. They advance on different occasions: the ordinal every cycle, the identity only when someone
publishes. **Release 12 is the proof** — cut, and deliberately not published.

**Counting integers, not semantic versions.** Same sentence the standard uses about itself: the
number counts publications and asserts nothing else. Nobody has to adjudicate whether a change is
breaking.

**Why it starts at one, written down while it is still obvious.** `v0` is reserved and will never be
issued from these repositories — it names **RI-0**, a different system under different governance.
`publications.md` also records that this `v1` and the standard's `v0` are unrelated subjects, since
two adjacent repositories both carrying a bare `v<n>` is a collision waiting to confuse someone.

### `release.sh` — cutting and publishing separated

| Invocation | Does |
|---|---|
| `release.sh` | cuts a cycle: `history-N` tag, `dev/N+1` from `dev/N`, `VERSION` bump. **No remote touched.** |
| `release.sh --publish` | that, plus orphan → force `main` → tag `$PUBLIC` → push `main` and the tag |
| `release.sh --check` | preflight only |

**What came out.** The `origin/dev/$RELEASE` requirement, the unpushed-work check, the `main`
fast-forward check, and the remote tag-collision checks. All four assumed a remote that mirrors
development. Preflight got shorter, not longer.

**Orphan, not squash.** A squash leaves the previous `main` commits reachable, which is the shape
that was just removed; only an orphan yields one commit and nothing else.

**`dev/N+1` now branches from `dev/N`, not from `main`** — the one place the rewrite changes meaning
rather than mechanism. `main` is an orphan with no ancestry, so branching from it would restart
development on a single commit and sever every cycle from the one before it.

**The orphan tree is verified against `dev/N` before any push.** An orphan takes whatever the index
holds, and a stray file would be published permanently under a declared identity.

**`--publish` refuses an identity `publications.md` does not name**, applying to the platform the
rule the standard applies to itself: an identity that appears in a version file and not in the
record has not been declared. The tag-collision check catches the likeliest error by far — running
`--publish` without having declared the next identity first.

**Not pushed by either mode: `history-N`, `dev/N`, `dev/N+1`, `VERSION`.** Step 4 carries the
warning in the script itself: this is where the absence of an offsite copy of work in progress
becomes real, and it must not be solved by pushing dev branches, which would undo the publication
surface.

### A loose end the rewrite surfaced

**All ten repositories were left checked out on `main`** by the publication, and `main` is now an
artifact pinned by a tag — a commit there diverges silently from what `v1` names. Preflight caught
it as ten failures. Fixed by checking out `dev/12`; worth knowing that the publication sequence
leaves you on the published branch, which is not where work belongs.

### Next session should start with

**Publish the call for review.** The URLs resolve correctly, the DOI exists, `doc/call_for_review.md`
asks for twenty minutes and one paragraph, and its closing section carries the standing need for an
external profile authority. Nothing further is waiting to be specified.

### The work itself, when there is some

**Mutation-test the reference realization.** C-1 is what release 12 is named for, and nothing has
ever removed a guard from this system to see whether a test notices. NOVA had that blind spot in two
places and neither was visible to a passing suite, its author, or a reading of its evidence.

---

## `standards` `draft/4` — **`v0` carried into the repository: the requirement projection joins the terminology projection, `0d` gains a drawn form, a profile template derived from `6a`, `CITATION.cff`, and the call for review rewritten as an invitation to disagree.** Release 12 notes written and the release ordinal derived rather than declared; the cut deferred, since the composition it would seal is the one release 11 already sealed. Next: publish, and wait for a reader who was not part of this.

The previous entry declared `v0` in `.github`. This session carried it into `standards` itself:
`VERSION` is `v0`, `revisions.md` holds the `draft-3` → `v0` supersession and the five findings
published with it, and the public-facing surface — the call for review, the citation record — now
says the same thing the record does.

### Changes made — `standards`, branch `draft/4`, three commits, working tree clean, pushed

| Commit | Files | What |
|---|---|---|
| `35065ce` | 11 files, +1238/−220 | **The requirement projection.** New `tools/requirement_index.py` derives `projections/requirement_index.md` — **356 requirements across 26 documents**. New `doc/profile_template.md`, derived from `6a` and adding nothing to it. `spec/0d` rewritten and given `0d_…​.svg` — the family's first drawn form. |
| `2fc8c36` | 8 files, +228/−42 | **`v0` in the repository.** `VERSION` → `v0`; `revisions.md` +134 lines carrying the supersession declaration, the five findings **B, C, C-1, C-2, C-3**, and the statement that Change 1 invalidates nothing. New `CITATION.cff` — *cite the revision you read*. Both projection contracts and the `projections/README` brought into line. |
| `870d7e5` | 1 file, +37/−41 | **`doc/call_for_review.md`.** Retitled *Call for Review* → **"an invitation to read, and to disagree"**. Body reflowed. The document ends on **a standing need, separate from review**: `6a` §6 requires that a profile not be authored by the system claiming it, no external profile authority exists, and a separation declared inside this project was **considered and refused as appearance without substance**. |

**The count guard shares no code with the extractor, on purpose.** `tools/check_requirement_count.py`
counts by a second route — `0z` §2 declares each document's invariant range, and the sum of those
ranges is what the family says it carries; the index is what the documents actually yield. It
reports **350 declared across 26 documents, plus 6 suffixed identifiers a range cannot express**
(`1b` SM-5a/7a/7b, `4d` TR-3a/5a/15a) = **356**, agreeing with the index. The first requirement
projection derived its guard the same way it derived the index, so a convention the extractor
stopped recognizing produced a smaller count every other check accepted. A guard that fails the same
way as the thing it guards is not a guard.

**`profile_template.md` carries its own prohibition.** `6a` §11 declines to specify the form a
profile takes, so the template *"is not part of the family and carries no authority"* — and it says
**do not give this to an authoring trial**, because the point of such a trial is to find what the
standard alone leads an author to produce. Three independently authored profiles organising the same
content three ways is the evidence that the structure was not determined; supplying the structure
answers that in advance and destroys the result.

### Changes made — `.github`, branch `dev/12`, uncommitted

| File | What |
|---|---|
| `process/notes/release-12.md` | **new, 153 lines.** *A passing suite is not evidence a demonstration could fail.* The release note for NOVA cycle 1: the SHA-256→MD5 substitution that passed all six demonstrations and the disabled baseline guard that passed all fifteen; execution asked for twice; the three times the instrument measured itself; three authors closing three different kind sets from byte-identical text; why G3 is blocked; what went untested. Continues release 10's line — `declared ≠ implemented ≠ enforced ≠ demonstrated` ends at *demonstrated*, and this cycle finds that *demonstrated* has an inside. |
| `process/release.sh` | **The release ordinal is derived from `.github/VERSION` rather than declared.** Was `RELEASE=11 / NEXT=12`, hand-set, and never bumped after release 11 was cut — so preflight expected every repo on `dev/11` and reported **eighty failures describing a release that had already shipped**. Now read from VERSION with a guard refusing empty, missing or non-integer, and `NEXT=$((RELEASE + 1))`. |

**The script had been keeping a second copy of the one thing it says must never be copied.** Its own
header holds that `VERSION` is the single declaration of which composition a repo belongs to and that
a version must never be hand-edited anywhere else — while `RELEASE` was exactly that, a hand-edited
second declaration with nothing to catch it going stale. The bump is now the write the script already
performs at step 4, so the step that can be missed no longer exists. What is no longer checkable is
whether the reference copy itself is wrong; there was never anything to check it against, the other
nine repos are still compared to it, and a VERSION bumped without a cycle behind it still fails the
branch and tag preconditions.

### Release 12 is written and deliberately not cut

Preflight passes but for the two uncommitted files above. **The cut was declined on the ground that
the composition has not moved.** Nine of the ten repositories carry one commit since `release-11` —
the version bump itself. The whole content of release 12 is in `.github`: NOVA cycle 1 end to end,
three G0 runs, G1, G2, G4, the instruments and the dispositions. None of it enters the snapshot.

**The manifest states the case exactly.** `compiler_version` is stamped into every domain projection;
it read `11` in the pre-session snapshot and reads `12` now. The `snapshot_id` therefore moved since
release 11 — **only because the version number is recorded inside the thing the version names.** The
governed content is identical. Cutting would mint a second composition identity over one composition,
which is the inverse of the defect the family polices everywhere else, where an identity must stand
in a declared relation to what actually changed.

So `dev/12` stays open and the note accumulates. Its opening was rewritten for that: the first draft
asserted *"nine of the ten repositories changed nothing this release"*, true only if the cut happened
that day and falsified by the next commit to land. The NOVA substance is untouched and holds whatever
lands next.

### Build and test status

**Standards projections — PASSING**, and both regenerate byte-identical (`git status` clean after
running them).

| Check | Result |
|---|---|
| `tools/check_requirement_count.py` | exit 0 — 356 expected, 356 carried, every mapped range plus its suffixed identifiers agrees |
| `tools/requirement_index.py --check` | exit 0 — 356 requirements, 26 documents, all contract checks passed |
| `tools/vocab_index.py --check` | exit 0 — 167 terms, 32 documents, **0 defects, 44 warnings** |

**Workspace — PARTIAL.** Environment clean; seven of eight conformance checks pass; one fails.

| Check | Result |
|---|---|
| `pgc_env_check.py` | PASSED — no RI-0 dependency reachable |
| `governance_closure` · `governance_chain_closure` | PASSED |
| `implementation_closure` | PASSED — 28 transforms, every module named and present |
| `frontmatter_fidelity` · `human_block_fidelity` | PASSED — 404 artifacts, prose declares nothing |
| `supersession_agreement` | PASSED — 7 relations, both sides agree |
| `evidence_determinism` | PASSED — `3e` EV-6, EV-7 |
| `admission_contract_fidelity` | **FAILED — 31 findings over 31 gates** |

All nine platform repositories are clean at `dev/12`; `.github` is clean at `dev/12`. **No platform
code was touched this session**, so the admission failure is not a regression from it — it stands
against the snapshot built the previous session (`snapshot/`, 2026-08-26).

### Open issues

**`admission_contract_fidelity` is red on 31 findings, and that is the documented expected state** —
`RUNBOOK.md:157` records them as *"all deliberate"*: other domains' business, plus
`IN_REGISTER_BOOK_V0`'s `subject`, deferred with its ground in `cr_04_catalog` P3 Q1, because
correcting it moves every caller and that change's seed forbids it. **Not an open issue.** A first
pass through this session's check run read the red as new and as the leading next action; it is
neither.

**Five findings carried into `v0` and published with it** — `revisions.md`: **B** (no demonstration
for the specification subject class), **C** (`0z` states MUSTs and carries no invariants), **C-1** (a
demonstration must be capable of failing; nothing requires showing which one does), **C-2** (`3a`
does not name the case distinguishing read routing from hard-coded routing that matches), **C-3** (a
profile exclusion bars comparability and `7a` §10 does not say so). **C-1 and C-2 would change what
conformance costs** if carried — said in the record rather than left to be discovered.

**The workspace-root `CLAUDE.md` repository table is stale.** It describes `business_domains` as
"business domains (ai_governance — untested)". Three domains are on disk and in the snapshot —
`ai_governance`, `blockchain`, `book_library_mgmt` — and 30 of the 31 admission findings are in the
two the table does not mention.

### Architectural concerns

**The 31 gates are in scope, and the profile settles it rather than raising it.** A first reading
took the failure for a scoping question — `blockchain` is named by no profile, so perhaps the check
should not be looking at it. It should. `REFERENCE_PLATFORM_PROFILE_V1` §6: *"A profile states
requirements, never an inventory. A snapshot may contain more than the profile requires and still
conform."* The same rule is in the superseded `NORMATIVE_PLATFORM_PROFILE_BASELINE_V0` §6, so it
predates both the current profile and this session. A profile pins governance identities, the closed
kind vocabulary, entry workflows and claims; **it selects no domains and is not meant to.** Domain
composition by discovery is not in tension with it, and there is no domain selection for a check to
narrow against. The findings are defects against `3a` EX-7 in content the sealed snapshot properly
carries.

**A declared snapshot composition was built, tried, and reverted — considered and declined.** The
observation was that membership in a composition is a fact about the filesystem: `core.py:51` takes
whatever sits under `tokenized/`, `assemble.sh:47` and `release.sh:157` glob `business_domains/*`.
Set against `6c` §10 — adding a domain is a governed transformation (TR-1) and a domain MUST NOT
claim genesis — that reads like a gap, since adding a domain today is `mkdir` plus a build config.

**It was declined because nothing requires it and nothing was failing.** `6c` §11 explicitly does not
specify *"what domains a system has, or how many"* or *"how domains are arranged — in repositories,
packages, or deployments"*, so the family asks for no composition artifact. `6c` §10 requires domain
addition to be a transformation; discovery does not make that false, it only declines to enforce it.
No check was red on it. The gap is between doctrine and mechanism, not a demonstrated defect, and it
was an architectural reading rather than a measured finding.

**Two things the attempt established, worth keeping.** A `STRUCTURE_SNAPSHOT_COMPOSITION_V0` pairing
each domain with its build STRUCTURE **was refused by the compiler** — `ASSERT_PROTOCOL_SURFACE_CLOSED_V0`,
six violations, one per non-platform pairing. The governance surface compiles before domains, so a
platform artifact naming a domain's artifact cannot resolve. **The platform cannot bind domain
identities**, and any future attempt at this must bind them at assembly, the only point where every
compiled domain is in hand. Second, deleting the artifact and rebuilding without cleaning surfaced
`E402_UNDECLARED_OUTPUT` on the orphaned JSON — compiled output with no source declaring it is
already refused, which is the property a composition declaration would have been partly duplicating.

**Including every domain is not a defect and should not be undone.** `release.sh:148` gives the
reason: an omitted domain is assembled from whatever stale output is on disk, and its compile against
the current governance closure is never proven. Seven domains exercise closure over 404 artifacts
rather than one, which is the only available evidence that platform governance is domain-neutral
(`6c` §3 — the platform governs the *form* of governance, the domain governs its own *subjects*).

**`v0` is declared and nothing external has read it.** The programme produced four gates of
independent authoring, realization, execution and transformation, and every instrument that examines
the text runs clean. What none of it manufactures is a reader who was not part of it. The call for
review and the standing need for an external profile authority are the two instruments aimed at
that, and neither is under this project's control once issued.

### Next session should start with

**Publish, and stop specifying.** `v0` is declared, carried into `standards` and pushed; the call for
review is written; every instrument that examines the family runs clean; the workspace is at its
documented state. The one red check is deliberate and recorded in `RUNBOOK.md:157`. There is no
repair queued and no gap the project can close for itself.

What it cannot manufacture is a reader who was not part of it, and the two instruments aimed at that
are already written and merely unissued: `standards/doc/call_for_review.md`, and its closing section
asking for **a party willing to author and own a conformance profile this project cannot change**.
Issue them.

**Then work that would actually move the composition, on `dev/12`.** The release cuts when there is
something to seal, not on a schedule. In descending order of what it would establish:

1. **Mutation-test the reference realization.** C-1 is the finding release 12 is named for, and
   nothing has ever removed a guard from the reference to see whether a test notices. NOVA had that
   blind spot in two places and neither was visible to a passing suite, its author, or a reading of
   its evidence. There is no reason to assume the reference is different, and this is the one piece
   of work pointed at this system rather than at more text.
2. **Unblock G3** — a third profile both NOVA and the reference can claim, narrow enough for the one
   and permissive enough for the other. The cycle summary calls it a design question, not a run.
3. **The effecting path** — no capability with an external effect has ever been exercised, the
   largest untested surface the cycle names.
4. **Transport** — Phase 1 frozen in `protocol_transport/TRANSPORT_STANDARD_V0.md`; constitutions
   and adapters await authorization.

**Resist the pull to build instead of publishing.** This session three times mistook a settled matter
for an open one — the 31 admission findings, dispositioned in the runbook; domain composition, which
`6c` §11 declines to specify; and the release cut itself, which the user stopped. Each was reverted
or declined at no cost, but the pattern is the risk: with nothing left to specify, an idle instrument
finds work that is not there. The standard is not waiting on another change. It is waiting on someone
outside it.

---

## dev/12. **`v0` declared, superseding `draft-3` · NOVA cycle 1 closed and seven findings dispositioned · the standard leaves draft and goes public · next: publish, and wait for a reader who was not part of this.**

The whole cycle came from one instrument: **a terminology index derived over the family and checked
against `1a` §12** — the first instrument pointed at the family's own vocabulary rather than at a
realization. Twenty-four documents declare the terms they introduce; twelve of those declarations
were untrue.

### Changes made — `standards`, branch `draft/4`, one commit, working tree clean

| Commit | Files | What |
|---|---|---|
| `dae8476` | 27 files, +2061/−37 | **`draft-4` Change 1.** Seven terms gained a definition where their document already declared them; four struck; `step` moved to `1a` §8. **Five refinements declared — the first in the family**, CM-2 having required the mechanism since `draft-1` with nothing exercising it. **CM-8 added** (`1a` §1, §12, §13, §14; `0z` §2 row now `CM-1 … CM-8`). Finding **E** recorded, not carried. New `tools/vocab_index.py`; new `projections/` at root; `revisions.md` moved to root beside `VERSION`. |

**Terms struck rather than defined — 4.** `3c` `execution agent` (`1a` §8 already defines
**Runtime**
as "the agent that performs execution"; a second name for one concept is what CM-3 forbids); `4a`
`admissibility determination` (a compound of **Admissibility** `1a` §7 and **determination** `1b`
§4); `6c` `platform-owned governance` and `domain-owned governance` (§3 names the distinction in its
table and never uses either phrase). The `6c` pair was **defined first and struck after** — see
Architectural concerns.

**CM-8 — ownership by semantic primacy.** A term belongs to the document whose subject matter
principally establishes it, never to `1a` by order of appearance. The rule had to be applied four
times in this change and was stated nowhere. It is the one part of Change 1 that adds a requirement
rather than repairing a declaration; it invalidates no existing definition.

**`candidate` was the case that tested it.** Wording could not settle it — `4a` §2 duplicated `1a`
§10 near-verbatim, which is evidence of an accident, not of ownership. Usage breadth settled it:
`candidate` appears in ten documents, and `1b` §4 defines **proposal** as "a candidate change
presented to a governed state". A Part I document using the term to define one of its own means the
concept is family-wide. Had construction owned it, `1b` would rest on a Part IV term — the same
defect this change repaired for `step`.

### Changes made — `.github`

| File | What |
|---|---|
| `external_validation_nova/NOVA.md` | **new.** The NOVA programme: a second PGC realization built from the standard alone by a cold worker, to test specification sufficiency and governed self-evolution at once. Five gates — **G0** profile authoring, **G1** experiment protocol, **G2** the realization, **G3** comparative conformance, **G4** governed transformation — and no gate starts until the prior one has *both* its artifact and its findings. Six finding classes, with **class 6, reference-shaped assumption**, as the result the programme exists to produce. |
| `external_validation_nova/instruments/task_author_a_profile.md` | revised for **G0**. Frozen candidate revision; existing profile candidates prohibited *including their shape and field names*; any concern or prefix taxonomy from a realization prohibited *including how many there are*; three finding classes become six; a sixth deliverable — close the kind vocabulary from the family alone; new sections on not inventing a conformance oracle, and on success and failure. |
| `external_validation_nova/instruments/task_author_a_profile_operator.md` | brought into line. Sandbox now built from a named revision via `git worktree`, with an exclusion table — `projections/` and `revisions.md` moved to the `standards` root this session and a whole-directory copy would leak both. New closing procedure: capture outputs, disposition findings, *then* freeze. **Fixed a broken path** — the setup script copied the worker document from `.github/doc/`, where it does not live. |
| `doc/SOTU.md`, `doc/` | nine resolved `draft-3` working files removed; the `draft-2`-era entry trimmed. `parked_rulings.md` kept — deferred, not resolved, and cited three times from `standards/doc/realization_map.md`. |
| `external_validation_nova/NOVA.md`, `external_validation_nova/instruments/task_author_a_profile_operator.md` | **the G1 network regime, settled per gate.** Not one policy: **G0** removes the network-capable surface outright — no `Bash`, no web tools, no subagents, because reading `spec/` and writing documents needs none of them, leaving no residual. **G2** cannot be bound that way, since a worker that executes can reach the network; it needs an offline container, with dependencies staged in advance from a fixed manifest and recorded. **G3/G4** need nothing. The trap named explicitly: G0's guarantee does not cover G2, and G2 is the gate that most needs isolation. |
| `external_validation_nova/instruments/task_author_a_profile_operator.md` | **the sandbox moves out of the workspace tree.** It was specified at `standards/sandbox/`; an agent session inherits the `CLAUDE.md` files above its working directory, and the workspace root's names every repository, the build lifecycle and the platform composition. A sandbox inside the tree hands over the whole reference architecture before the worker reads one document — contaminated by its own location. Now `~/g0-run`, with a check that nothing above it carries context and that the worker's agent-configuration directory has been archived. |
| `external_validation_nova/instruments/g1_realization_protocol.md` | **new.** G1 — what a realization worker may see, must produce, and is judged by. Its hard exit criterion is discharged: **disposition C**, a conformance suite is deliberately outside the family, so G2's claim discharges by demonstration with declared fixtures — including negative ones — obtainable by a party that did not build the system. `7b` §6's obtainability rule is the operative constraint, not a schema. |
| `external_validation_nova/instruments/task_build_a_realization.md` | **new.** The G2 worker commission, derived from G1. Its §6 carries the finding G2 exists to produce: an author can leave a question open on the page and a builder cannot, so every gap is filled with something, that something works, and a working system feels like evidence the choice was right. It is not evidence the standard determined it. |
| `external_validation_nova/NOVA.md`, `external_validation_nova/instruments/g1_realization_protocol.md` | **independence scoped to the boundaries that carry it.** Two only: `NPP-E`'s author must not build NOVA (`6a` §6), and NOVA's builder must not have had access to G0's findings. **A single worker may perform G2 and G4** — no fresh-worker rule between them, since G4 transforms the system G2 built. **G3 is a commissioning-side comparative evaluation**, not a worker task. Mirrors the real separation: standard author ≠ profile author ≠ implementer ≠ certifier. |
| `external_validation_nova/instruments/g1_realization_protocol.md` | **the claim types are bridged to the classes.** The worker-facing documents carry no class reference at all — five claim types for the worker, classes for the evaluator — and nothing said how one became the other. G1 §7 now maps *claim type × source basis* to class, and states what the record alone cannot settle: class 5 and class 6 differ by whether the worker chose freely among workable options or had to arrive at a shape for anything to fit. Class 6 is never named to a worker, because naming it says a realization exists. |
| `external_validation_nova/NOVA.md` | **G4's stronger follow-on, recorded and not required.** A transformation by an operator who did not build NOVA would test the premise harder: if evolution needs the builder's memory, the governed state did not carry what it required. Not a condition of the current claim. |
| `projections/`, `tools/` *(in `standards`)* | **the `1c` omission closed** — see below. |
| `external_validation_nova/` | **new tree, SoC.** The whole programme out of `doc/` and `process/`: `NOVA.md`, `instruments/` (7 commissions and protocols), `runs/` (11 — three G0 trials, G2, G4, with evaluations and dispositions), plus `README.md` and `CYCLE-1.md`. Twenty stale cross-references rewritten and verified to resolve. `doc/` keeps SOTU, `parked_rulings.md`, `e0_ruling_3_brief.md`; `process/` keeps the runbook, release script, checks, and the `6b` environment-profile trial — which is *not* NOVA and stays put. |
| `process/notes/release-11.md` | **new.** *A declaration is not a definition* — the release note for this cycle. Deliberately echoes release 10's *declared ≠ implemented ≠ enforced ≠ demonstrated*: the same shape of finding one level up, an instrument turned on the standard instead of on the realization. Carries the extractor's own failure as a full section, because a note reporting 124 defects without saying 111 were its own blindness reads as self-serving. Documents are named by role, not file identifier, matching release 10's register. |

### Changes made — `snapshot_assembler` and `protocol_runtime`, uncommitted

`SNAPSHOT_ASSEMBLY_CONTRACT.md` moved from `.github/doc/` to `snapshot_assembler/doc/`. Four modules
cite it — `assembler/{__init__,core}.py`, `runtime/{boot,loader}.py` — and an implementation
contract
belongs with the component it governs, not in org config. Its header carried two dead references:
`NAMESPACE_MODEL.md`, which exists nowhere in the workspace or in RI-0 and has no successor, and
`spec/01_machine_block.md`, an RI-0 path. **Neither was used by the body** — both words appeared
only
in that line — so they were replaced with what actually governs assembly, `3b` and `4b`, rather than
translated. The `Status:`/authoring-note bullet was dropped.

### NOVA G0 — three runs, three instrument repairs

The profile-authoring trial ran three times against byte-identical `spec/`. **Two of the three
failed as experiments, and each failure was the instrument rather than the author.**

| Run | Condition | What it established |
|---|---|---|
| `NPP-C` | commission supplied a six-class taxonomy | nothing about **A** — the taxonomy named the very distinction A says the family lacks. Ledger inflated: 7 of 12 class-2 entries cited the commission as authority |
| `NPP-D` | repaired commission, **same worker, same context** | nothing about **A** — carried the withdrawn phrase *reference-shaped assumption* forward, a term absent from its own commission and present in the previous one |
| `NPP-E` | repaired commission, **fresh session, zero carry-over** | **A answered.** Eleven determinations *expressly permitted by source*, eight *unresolved by family* — the distinction drawn from the text alone |

**Finding A — ANSWERED.** What rules out recall is that `NPP-E` extended the claim-type vocabulary
as `NPP-D` had, but with *different constructions for the same distinction*. Recall reproduces
phrasing; derivation reproduces structure.

**Finding F — SETTLED, and not as expected.** Three closures from one text under one scope: `NPP-C`
and `NPP-D` closed four kinds each and match one another — which is the carry-over, not agreement.
`NPP-E`, the run that could not remember, closed **five** and diverged from both, reaching
**workflow** and **capability contract**. The result is not *four rather than nine*: **the standard
determines no vocabulary at all**, and `2d` §1 says it must not. A set the family deliberately
declines to determine cannot be a canonical axis of its ontology. **Not carried into `2b`.**

**Two repairs to the commission, both held.** Class 0 for commissioner-supplied scope, and the
taxonomy withdrawn from the worker in favour of a provenance record — *source basis*, *claim type* —
with all interpretive labelling done by the evaluator after the run. A third rule was added when the
carry-over was found, scoped to authoring runs: **use a worker that has not performed a previous
authoring run, in a context that holds none of one.** The existing prohibition covered what is
handed over, not what is remembered. It does not reach forward to G2 and G4, where the boundaries
are `NPP-E`'s authorship and access to G0's findings, and nothing more.

**The rule that outlives G0:** an experiment may constrain the task, but it must not supply the
distinction whose derivability it is measuring.

### G0 is closed

All conditions met: three profiles, their registers, every entry classified, every finding
dispositioned. **No freeze** — that moved behind G2 (below).

**Seventeen candidate findings across three runs. Zero undeclared gaps.**

| Run | Candidates | Carried |
|---|---|---|
| `NPP-C` | 9, reclassified to 7 | 0 |
| `NPP-D` | 3 checked | 0 |
| `NPP-E` | 8 | 0 |

Every one landed on something the family had already marked — `6a` §7 and §11, `4c` §8, `2d` §1,
`2b` §10, `3e` §12, `3d` §7, `7b` §6, `2c`. Three authoring passes probing for the standard's edges
found only edges it had already drawn. **That the exercise changed no specification text is the
result, not a shortfall**: the *does-not-specify* apparatus held under three attempts to find its
seams.

**The seventeen are one position held consistently: the family specifies meaning and declines
form.** Encoding, syntax, canonicalization, schema, signature mechanism, publication, fixtures —
each named somewhere as a realization's or a profile's to choose. The consequence the authors kept
reaching is real and is the design: **a profile claim cannot be checked mechanically from the
family alone.**

**That settles G1's hard exit criterion in advance.** Of the three permitted dispositions for the
missing conformance suite, the answer is **C — a suite is deliberately outside the family.** G1 must
define G2's discharge in those terms. `7b` §6's obtainability rule is the operative constraint on
G2, not a schema: *"a demonstration against material an evaluator cannot obtain is not a
demonstration to that evaluator."*

**A third instrument repair**, from `NPP-E`: the commission asks for *"matters left unresolved"* and
never says **unresolved by whom**. That author read it as *unresolved by the family* — which is what
delegation is — and filed eight family delegations as findings. Run `NPP-C` inflated in the opposite
direction, filing commissioner scope as family delegation. Registers must be named by who is left
holding the question, not by where the silence originated.

### The `1c` omission — closed

Carried since dev/11 and blocking the freeze. The requirement projection reported **317 requirements
across 24 documents**; the family carries **356 across 26**.

**It was short by two whole documents, not one.** The extractor knew only the bullet form
`- **GS-1.** …`, so `1c` — which states AI-1 … AI-17 as `### AI-1 — …` headings and uses no bullets
— read as carrying nothing. `1a` was the second, and had nothing to find until Change 1 gave it
CM-1 … CM-8.

`tools/requirement_index.py` is new and harvests both forms. `projections/requirement_index.md` is
published, and the contract that declared it since `draft-3` finally has a projection behind it.

**The guard is the part that matters.** dev/11 recorded that the old count check *"did not fire,
because the independent count was derived the same way"*. `tools/check_requirement_count.py` shares
no code with the extractor and counts against a **different artifact** — `0z` §2's declared ranges.

**It fired twice before it agreed**, and both were real defects in the guard, found by running it
rather than reasoning about it:

1. `1b` and `4d` each over by three. A range like `SM-1 … SM-12` names twelve positions, and those
   documents carry `SM-5a, SM-7a, SM-7b` and `TR-3a, TR-5a, TR-15a`. **Range notation cannot express
   a suffixed identifier.**
2. The suffix scan then counted `SM-7a` in `6b` and `TR-15a` in `6c` and `7b` — cross-references,
   not owned invariants. Restricted to each document's own prefix, which `0z` already names.

```
356 requirements · 26 documents · 339 bullet · 17 heading
0z §2 declares 350, plus 6 suffixed identifiers = 356 · agreed
re-derivation byte-identical (PJ-2, PJ-9)
```

**One thing surfaced and left open:** `0z` §2's ranges understate the family by six, because range
notation cannot carry a suffix. The guard reports the six explicitly rather than absorbing them.
Whether `0z` should state counts rather than ranges is a question for the freeze, not for tooling.

### NOVA — cycle 1 complete except G3

Full account in `external_validation_nova/CYCLE-1.md`, written for the expert loop. In brief:

| Gate | | |
|---|---|---|
| **G0** profile authoring | run ×3 | `NPP-C`, `NPP-D`, `NPP-E` |
| **G1** protocol | written | governs G2 |
| **G2** realization | run | claims `NPP-E`, discharges 1 of its 8 claims |
| **G3** comparative conformance | **blocked** | `NPP-E` §12 excludes the reference by construction; `7a` §10 makes systems under different profiles incomparable. Needs a third profile both can claim — a design question, not a run |
| **G4** transformation | run | a lending domain added to G2's own baseline, grounded by identity |

**No repair to the standard follows from any gate.** Seventeen G0 candidates, nine G2
determinations with **none** carrying source basis `none`, and a G4 transformation that grounds by
querying the baseline rather than assuming it. **No class 6 anywhere.**

**Two evidence gaps, identical in shape, both found only by mutation testing.** `NPP-E` mandates a
SHA-256 digest and substituting MD5 passed all six G2 demonstrations; the G4 baseline-grounding
guard was correct and disabling it passed all fifteen. Both times a property the profile requires
was implemented, asserted *about*, and never demonstrated by anything that could fail. **A passing
suite is not evidence a demonstration could fail.** Both closed on the first pass after being named.

**The instrument failed three times and each repair is now in the commissions**: the taxonomy
answered the question it measured, commissioner scope was counted as family delegation, and a
worker's memory is not covered by a rule about handed-over material. The rule that outlives the
programme: *an experiment may constrain the task, but it must not supply the distinction whose
derivability it is measuring.*

**`3a` has since been built against.** The transformation's first delivery declared a workflow
carrying an outcome vocabulary that **nothing read** — the rule lived in a method, and deleting the
workflow artifact left behaviour unchanged. Asked to discharge the Runtime and execution claim, the
builder drove traversal from the sealed declarations. The decisive mutation — replacing
`step["routes"][outcome]` with the behaviourally equivalent hard-coded branch — **now fails a
test**, which is the only check a well-formed fixture cannot make.

**Three of `NPP-E`'s eight claims are discharged**, not two. An earlier draft miscounted:
the transformation is a claimed and discharged claim, not evidence for another. The summary now
carries a claim ledger distinguishing **discharged** (2, 4, 5), **exercised but not claimed**
(3, 6, 7) and **not claimed** (1, 8). The correction came from the builder.

**Three candidate findings against the standard — the first the programme has produced.** None from
being blocked; all from the builder's reflection. Recorded, not carried:

- **C-1** — `7b` requires a demonstration *capable* of failing, not that you show *which one* fails.
  Two correctly implemented guards broke no test and were invisible to everything but mutation.
- **C-2** — `3a` does not distinguish a route followed, a route absent, a route retargeted, and
  **hard-coded routing ignoring a changed declaration.** The fourth is the decisive architectural
  test and is unnamed in the text.
- **C-3** — `7a` §10 says systems under different profiles are not comparable; it does not say a
  **profile exclusion** bars comparability, which is exactly why G3 is blocked.

**One implementation limitation recorded**, also from the builder: `3d` CP-9 requires a declared
binding, and the realization dispatches on the capability's `effect` value as an implicit one.

**A snapshot exists and verifies independently.** NOVA had produced three snapshot identities and
no snapshot — nothing wrote one to disk, and the sealed content lived only in memory for the length
of a process. Reproducible, but not obtainable in `7b` §6's sense. The builder emitted
`snapshot.json`, archived at `runs/g4_run/`.

**Verified without using any of the realization's code**: `whole_integrity` recomputed from the
fields it declares it covers matches; `id` is `snapshot:` + that digest; **all five artifact
identities verify as content-derived.** That is `3b`'s *"verifiable — its integrity and identity can
be checked by a party that did not build it"*, satisfied rather than asserted, and it is the
strongest artifact the programme has produced.

Three things that could have been wrong and were not: `whole_integrity_covers` lists itself while
excluding `id` and `whole_integrity`, so the self-reference is handled; `constituents` carries whole
artifact objects rather than identities, so the snapshot is self-contained; and `governance-element`
is admitted by the vocabulary and absent from the snapshot, which is correct — a closed vocabulary
states what may exist, not what must.

**Still untested:** `3d`'s effecting path — no capability with an external effect, and `NPP-E` §2
selects no interaction boundary, so it may not be reachable under this profile at all.

### Build & test status — **PASSING**

Run from `standards/`:

```
python tools/vocab_index.py --check     → exit 0
167 terms · 32 documents · 25 defining documents
0 declared without a definition site · 0 defects · 47 warnings
5 declared refinements
```

Two further checks from the projection's own contract, run separately:

- **re-derivation from unchanged `spec/` is byte-identical** (PJ-2, PJ-9);
- **independent term count matches** — 167 counted by a script sharing no code with the extractor.

Workspace checks after the file moves:

```
python .github/process/pgc_env_check.py          → PASSED, exit 0
python .github/process/implementation_closure.py → PASSED, 28 transforms
imports: assembler · assembler.core · runtime.boot · runtime.loader
         protocol_compiler · snapshot_inspector    → 6/6 ok
```

**None of those checks would have caught what actually changed.** All four edits were docstring path
strings, which no import or closure check reads. The real verification was confirming every `*.md`
reference in the contract resolves, and that nothing still points at the old location.

Invariant identifiers across `spec/`: **356**. Note `revisions.md` records `draft-3`'s predecessor
count as 338 and SOTU dev/11 recorded 342; neither was re-derived this session and the three figures
do not agree.

### Open issues

1. ~~The requirement projection omits `1c`.~~ **Closed this session** — published at 356
   requirements across 26 documents, with a count guard that reads `0z` §2 rather than re-deriving
   from the documents. What it surfaced and left open: **`0z` §2's ranges understate the family by
   six**, because a range cannot express `SM-7a`. Whether `0z` should state counts rather than
   ranges is a freeze question.
2. **Finding E — nothing says when a word must become a term.** Six are declared, defined, and used
   nowhere: `Promotion` (`1a`), `construction disposition` (`2c`), `projection source` (`4b`),
   `protocol adapter` (`5a`), `profile derivation` (`6a`), `demonstration coverage` (`7b`). Evidence
   in `projections/vocabulary_locality.md`. Not carried — a CM-9 would have to be discharged by
every
   document, and the obvious formulation is contradicted by the evidence.
3. **Finding D narrowed, not closed.** First measurement: `4d` owns 11 terms, 4 local, **all 4 cited
   by a `4d` invariant** — it did not invent idle vocabulary. What survives is whether its subject
   requires that much, which is the `8a` §4.7 re-review, still not undertaken. `5a` and `2c` each
   carry 5 local terms and were never the subject of a finding.
4. **The commit message on `dae8476` is malformed.** All 27 files landed in one commit and the
   subject line carries a pasted label plus the whole body on one line. Content is correct;
   `git commit --amend` fixes it if nothing is pushed.
5. Carried unchanged from dev/11: **`7b` has no specification-subject section** (Finding B);
   **`0z` states three MUSTs and carries no invariants** (Finding C); **`4d` TR-2/TR-4 presume
   per-phase register documents**; **`1a` has two sections named *Conformance***, §11 and §14.

### Architectural concerns

- **A definition does not create a use.** `6c`'s pair was reported as declared-and-unused; the
triage
  judged that §3 names the distinction and defined them rather than striking them. They were then
  declared, defined, and *still* unused, and were struck. Writing a definition is the tempting
remedy
  for an unused declaration and it is the wrong one. Recorded inside Finding E.
- **CM-8 cannot be checked by tooling and the contract says so.** Whether a term sits with the
  document whose subject matter establishes it is a semantic determination — settling it for
  `candidate` meant reading `1b` §4. The projection reports where terms are defined; it does not
  judge whether that is where they belong.
- **The instrument was wrong before the documents were.** First pass reported 124 defects, of which
  **111 were its own blindness** to conventions the family had used all along. The contract now
  states the four source conventions the derivation depends on, because that is the characteristic
  failure of a derived index.
- **`projections/` mixes generated and hand-authored files.** Two are generated
  (`terminology_index.md`, `vocabulary_violations.md`); five are written — the README, both PJ-3
  contracts, and the two readings. A contract cannot be generated by the tool it governs. Documented
  in `projections/README.md` after this caused a false alarm.
- **`spec/` was held clean.** Projections stay out of it: a file identifier confers family
membership
  (`0z` §2), and a regenerated file inside a family built on declared supersession contradicts
  `4e` §9. `doc/` was reduced to what has no more specific home.

### Release — `v0`

**`VERSION` is `v0`, declared as superseding `draft-3`.** The version is a single number starting at
zero — ground zero, the first identity anyone may build against or name in a claim. Not semantic:
no major, minor or patch, because `4e` §9 holds that a revision is *declared* rather than inferred
from a number.

**`draft-4` was the working name and is gone.** It was never frozen, never tagged, no claim was made
against it, and nothing outside the repository named it — checked before collapsing it, so the
rename rewrote no external reference. The single supersession is `draft-3` → `v0`, and Change 1 is
its content.

**Occasioned by exposure, not by a defect.** Four gates of independent authoring, realization,
execution and transformation produced no undeclared gap; the terminology and requirement projections
run clean. **What the programme cannot manufacture is a reader who has not been part of it**, and a
draft identity now costs more than it buys.

**It invalidates nothing.** Change 1 altered no obligation on a realization — CM-8 binds documents
of
the family, not systems. A realization conforming to `draft-3` conforms to `v0` unchanged.

**Five findings are carried into `v0` and published with it**, each with what would settle it:
**B**,
**C**, **C-1**, **C-2**, **C-3**. Two of them — C-1 and C-2 — **would change what conformance
costs**
if carried. Claims against `v0` survive under `0z` §5.1, but a successor may ask more. That is said
in the declaration rather than left to be discovered.

**Also this cycle:** `call_for_review.md` reframed from a tasking document to a review invitation —
*"read it and say where it is wrong"* — with Discussions, Issues and email as channels, all eight
links repointed to `blob/v0/`, and the profile-authority ask demoted to a standing need stated
separately from the review. `CITATION.cff` added, carrying `version: v0`.

**Release 11 remains this cycle's composition release** — `process/notes/release-11.md`. It is
independent of the standard's revision identity: release 9 removed the standard from the composition
so it could be versioned on its own.

### Next session should start with

**Run G2 — the independent realization.** G0 is closed, G1 is written
(`external_validation_nova/instruments/g1_realization_protocol.md`), and the worker commission
derived from it is written
(`external_validation_nova/instruments/task_build_a_realization.md`). Nothing remains to author;
what remains is setup.

G1 settled three things so they are not re-derived at G2:

1. **The conformance-discharge basis is disposition C** — a suite is deliberately outside the
   family. G1 states G2's discharge in terms of demonstrations and evidence an outside party can
   obtain and check, per `7b` §6. It must not invent a test oracle.
2. **The network regime is settled per gate.** G2 needs environment isolation, not tool restriction:
   a worker that can execute can reach the network. Dependencies staged in advance from a fixed
   manifest, and recorded.
3. **The revision target is a pinned commit, not a frozen revision.** The freeze is after G2.

**G2's remaining setup, all of it mechanical:**

- an **offline container or VM** — G0's tool restriction cannot bind a worker that executes;
- ~~`NPP-E`'s scope register renamed to `NPP-E-scope.md`~~ — **done.** It was returned as the
  extension-less `list_assumptions`; the commission tells the worker to read it *before* the
  profile, since without it a commissioning constraint reads as a family requirement. The
  deliverables' own text was left unedited and the rename is recorded in the run's README;
- the **staging manifest**, declared by the worker before isolation and closed once the run starts.
  A later request is granted if it must be, and recorded as a break in the isolation with its
  reason and moment;
- a **worker satisfying the two independence boundaries, and no more than those**: it must not be
  the author of `NPP-E` (`6a` §6), and must not have had access to G0's findings or other excluded
  material. **The same worker may then perform G4** — no fresh-worker requirement stands between
  the gates, and G4 transforms the system G2 built.

**The commission's §6 carries the finding G2 exists to produce.** An author can leave a question
open on the page; a builder cannot — code does not run with a hole in it. Every gap must be filled
with something to proceed, that something will work, and a working system feels like evidence the
choice was right. It is not evidence the standard determined it. The test given to the worker is one
question: *can I quote what determined this, by document and section?*

**Watch for class 6.** G0 produced none, and authoring a profile does not press on the standard the
way building does. Either outcome at G2 is informative; several would be the most valuable findings
the programme can generate.

**The profile G2 builds against is `NPP-E`** — the only run of the three that was uncontaminated..

**The standing technical item is closed.** The requirement projection is published at 356
requirements across 26 documents, with an independent count guard. What remains for the freeze is
whether `0z` §2 should state counts rather than ranges, since a range cannot express `SM-7a`.

---

## dev/11. **`draft-3` at Change 10 · independent-authoring trial run once · next: the requirement projection omits `1c`.**

The whole cycle came from one exercise: **an external AI worker was given the family and nothing
else and asked to author a Normative Platform Profile.** Seven of the family's changes this session
were occasioned by what it got wrong, and two by reading its output closely enough to find things it
did not.

### Changes made — `standards`, branch `draft/3`, all committed, working tree clean

| Commit | Files | What |
|---|---|---|
| `f2c2e00` | `6a`, `5b`, `7a`, `doc/revisions.md` | **Changes 4–6.** NP-12 (a profile MUST NOT decide a deferred item by deferring it to the system that claims it); `6a` §7's read-surface row split into openness / attribution; **caller** introduced and glossed in `5b`; `7a` §3.1 bounds a system instance by the snapshot it accepted (RT-3 → next acceptance or stop). |
| `0469548` | `6a`, `5b`, `7a`, `doc/revisions.md` | **Change 7.** Five of ten review observations carried, five declined. Reverted an over-reach in Change 5 — IN-12 had been amended to *"governance applicable to it and to its caller"*, which asserts a governance-to-actor relation the family does not have; `5b` §1 now says **a caller is identified, not governed**. Added `6a` §7's two-systems test, the no-undischargeable-claim rule, `6a` §5's *an additional obligation must add something*, and `7a` §3.1's *a profile's subject-class list is a floor*. |
| `fb18d89` | `4d`, `doc/revisions.md` | **Change 8.** Closes the `4d` re-review left outstanding against `draft-2`. **TR-23 had no document behind it** — the invariant cited §14 and §14 said nothing of the kind; the requirement appeared nowhere in the body, in any revision, and `realization_map.md` records it as *Demonstrated*. §14 now states it. Two linearity over-specifications relaxed: §4 (phases are a dependency order, not a line) and TR-20 (gapless + dependency-respecting, not *total*). |
| `d1ac616` | `0z`, `1a`, `doc/revisions.md` | **Changes 9–10.** `0z` §2 map corrected: `6a` was `NP-1 … NP-11` (my own Change 4 introduced that); **`4e` Supersession was listed as carrying no invariants and carries SU-1 … SU-10**, wrong for two revisions. `1a` gained **CM-1 … CM-7**, derived from §3 and §12 with no wording change — it had six MUSTs and a conformance clause that nothing could cite. Former §13 → §14. |

### Changes made — `.github`, committed

| Commit | What |
|---|---|
| `df47ac5`, `7787623`, `19d9c70` | `external_validation_nova/instruments/task_author_a_profile.md` — the trial instrument, salvaged out of the deleted sandbox and hardened: per-run identity (never reused, `6a` §9); **the standard is read, never written**; no previous run's outputs; **do not ask the commissioning party to decide anything**; everything cited must be quotable by document and section. Plus `external_validation_nova/instruments/task_author_a_profile_operator.md` — JIT sandbox setup, operator rules, how to read the log, and the Changes 4–7 pass criteria, **deliberately not in the worker's copy.** |

### Build & test status — **PASSING**

No test suite; the family's checks are structural. Run from `standards/spec`:

```
31 documents · 342 invariants · 0 duplicate identifiers · 0 unresolved cross-references
all 25 mapped invariant ranges agree with 0z §2
```

### Open issues

1. **`doc/requirement_projection_contract.md` records `317 requirements · 24 documents`. The
family has 25 invariant-bearing documents and the projection omits `1c` entirely.** `1c` states
AI-1 … AI-17 as `### AI-1 — …` section headings; every other document uses `- **XX-1.**` bullets,
and the extractor matches the bullet convention. The contract's *Verification* section names the
count check as *"the guard against silent convention drift"* — the guard did not fire, because the
independent count was derived the same way. `draft-3` Change 1 declared this rendering a
projection under `4b`, so this is a faithfulness question (PJ-4, PJ-9) about the family's
projection of itself. **Correct figures: 342 total; the projection covered 317 of the then-334.**
2. **`7b` has no specification-subject section.** `7a` §3 names **specification** as a conformance
subject class evaluated by `1a` and `1b`; both now carry invariants; `7b` does not mention the
class and specifies no demonstration for it. Recorded as outstanding in Change 10.
3. **`0z` states three MUSTs — including the derivation rule — and carries no invariants.** Same
shape as the `1a` gap just closed; weaker case, left open in Change 10.
4. **`4d` TR-2 / TR-4 presume per-phase register documents**, excluding a model that records each
decision as a separately identified declaration. `draft-2` Change 6 settled a finding's location
as register/entry/field one revision ago; not reopened on review alone. Recorded as outstanding
against `draft-3` in Change 8.
5. **`1a` has two sections named *Conformance*** — §11 (the concepts) and §14 (the document's own
clause). Predates this session. One-line fix if wanted.

### Architectural concerns

- **The trial has been run once and its fixes have never been tested.** Changes 4–7 exist because
one cold reader fell into holes the family did not catch. Whether NP-12, the two-systems test, and
the caller gloss actually catch it is unknown. Pass criteria are written; the run is not done.
- **The trial cannot be run by this assistant.** It authored Changes 4–10; a trial it also authors
establishes nothing. It has to be a separate worker, driven by the user, per the task's own §8 on
externality being a property of authorship.
- **The first run's artifacts are gone.** `standards/sandbox/` was untracked and deleted. The
profile, its questions log, and the evaluation exist only as prose in `revisions.md` Changes 4–8.
No artifact-to-artifact diff between runs is possible.
- **Two contamination routes are closed in the task doc but untested**: a commissioner's reply
being cited as normative text (it happened — a sentence from a chat reply appeared in the profile
attributed to `6a` §7), and the worker patching its own copy of the standard (it happened —
including a section insertion that renumbered everything after it).

### Release posture

**Not yet `1.0`.** `VERSION` is `draft-3`, ten changes declared, **no freeze section**.
`standards/CLAUDE.md` is explicit that `VERSION` is a revision identity, not a release version,
and that bumping it declares nothing. Order agreed: **re-trial → close open issue 1 → freeze
`draft-3` → declare `1.0 supersedes draft-3`** (identity only, occasioned by adoption,
invalidating nothing).

### Next session should start with

**Open issue 1 — the requirement projection omits `1c`.** Establish whether the extractor ever saw
`1c`'s 17 architectural invariants, fix the extraction or the convention, and correct
`doc/requirement_projection_contract.md`'s stated count from `317 · 24 documents` to the verified
`342 · 25 documents`. It is the one open item that makes a *declared projection of this family
unfaithful to its source*, and it blocks the freeze in a way the others do not.

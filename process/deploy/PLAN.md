# Federated Deployment on `shuttle` — Plan

Deploys the `FEDERATED_NODE` composition (`STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V2`) onto four
LXC nodes and an external evidence store, so that `SIGNED_FEDERATED_MULTINODE_PROFILE_V0` can be read
back against a deployment that can satisfy it. Targets OB-2, OB-3, EO-1, EO-2, EO-3, EO-4.

The nodes are configured by hand. `NODE_CONFIG.md` in this directory is the end configuration of
every machine and the recipe for reaching it.

## 1. Topology

| Host | Address | Kind | Role | Inbound allowed |
|---|---|---|---|---|
| Mac | LAN | workstation | Build machine and sole signer | — |
| `shuttle` | 192.168.1.201 | LXD host | Hypervisor only; not in the evidence path | SSH from Mac |
| UC220 | 192.168.1.220 | **VM** | Evidence store (NFSv4). Not a node | NFS from .221–.224 only |
| UC221 | 192.168.1.221 | container | Interaction boundary | HTTP :8000 from LAN |
| UC222 | 192.168.1.222 | container | Coordinator | :8100 from .221, .223, .224 |
| UC223 | 192.168.1.223 | container | Worker | none |
| UC224 | 192.168.1.224 | container | Worker | none |

All nodes: Ubuntu 24.04.5, Python 3.12.3. No OS upgrade in this effort.

Invariants the layout carries:

- The private signing key exists only on the Mac. Nodes receive the public key as `PGC_TRUST_ROOT_PUBKEY`.
- `PGC_DATA_ROOT` on every node is the store mount. Traces, capability state and claims are written
  there directly; nothing is staged on a node.
- Every node boots the same signed snapshot, identified by `snapshot_id`.

## 2. Phase A — Runtime and boundary (proved locally before any deployment)

The existing `runtime/coordinator.py` realizes `LOCAL_MULTI_WORKER` with a process pool and refuses
any other placement. It stays as it is. Federation is a separate realization, `runtime/federation/`.

**A1. Federated coordinator** — `runtime/federation/coordinator.py`

- Refuses to start unless the sealed placement mode is `FEDERATED_NODE`.
- Serves an internal HTTP endpoint: `POST /units` accepts a unit, `GET /units/<id>` returns its
  outcome, `GET /health` reports `snapshot_id`.
- Enqueues a unit by exclusive creation of `data_root/queue/<unit_id>.unit.json`. It never executes.
- Refuses a unit submitted against another snapshot, or naming a domain the snapshot does not carry.

**A2. Worker** — `runtime/federation/worker.py`

- Refuses to start unless the snapshot is `FEDERATED_NODE`, the store is writable, and the
  coordinator answers `/health` with the same `snapshot_id` (EO-2).
- Polls `queue/`, claims by exclusive creation (atomic on NFSv4), runs `run_workflow` against the
  shared `data_root`, writes `outcomes/<unit_id>.outcome.json`.
- A claimed unit is never re-taken. OB-4 carries over unchanged.

**A3. Boundary submits, does not execute**

- `runtime.api.invoke_workflow` reads the sealed placement mode. Under `FEDERATED_NODE` it submits
  the unit to `PGC_COORDINATOR_URL` and returns the worker's outcome; under every other mode it calls
  `run_workflow` in place. The transport resolver calls `invoke_workflow`, so the engine still has
  one runtime interface and no placement logic.
- The HTTP adapter gains `PGC_HTTP_BIND` (default `127.0.0.1`; UC221 sets `0.0.0.0`).

**A4. CLI** — `protocol_runtime coordinator` and `protocol_runtime worker`.

**A5. Local proof** — `testbed/pgc/test_federation.py`, run by `regression.sh`: one coordinator and
two workers as processes over a local directory standing in for the store.

- Determinations through the group equal those reached in place.
- Each unit executes exactly once across two workers.
- Claimed units are not re-dispatched; a concurrent claim has one winner.
- Every refusal: non-federated snapshot, unreachable store or coordinator, boundary without a
  coordinator, unit from another snapshot.

Node dependency closure. Capability implementations are imported only at execution, so only workers
use them:

| Role | Needs |
|---|---|
| every node | `protocol_runtime`, `snapshot_assembler` (acceptance + signature verification), `cryptography` |
| boundary | + `snapshot_inspector`, `protocol_transport` source, the workload's HTTP binding |
| coordinator | nothing further |
| worker | + capability implementations (`software_governance`, `conformance_workloads`) |

## 3. Phase B — Infrastructure (by hand, once)

Per `NODE_CONFIG.md` §2–§3.

**B1. UC220 as a VM.** `ubuntu:24.04 --vm`, bridged on `br0` with the pinned MAC `00:16:3e:00:02:20`
so the DHCP reservation keeps .220. `nfs-kernel-server`, NFSv4 only, exporting `/srv/pgc/data`
`rw,sync,root_squash` to .221–.224 individually.

**B2. Nodes mount the store themselves.** The nodes are privileged containers (the `bridged`
profile), so each mounts the export over NFSv4 through `srv-pgc-data.mount`. AppArmor still confines
a privileged container, so each node carries `raw.apparmor: mount fstype=nfs4, mount fstype=rpc_pipefs,`.
The host is not in the evidence path.

**B3. One owner.** `pgc` is uid/gid 2001 on UC220 and every node. The export directory is `pgc`-owned
and `0750`; with `root_squash`, root on a node cannot read the store — only the PGC services can.

**B4. Network policy.** nftables input chain, policy drop, in every instance, per §1.

**Checks.** Every node writes as `pgc` and reads every other node's write; root on a node is refused
the store; a restarted node comes back with the mount and the rules; from the LAN only UC221:8000
answers.

## 4. Phase C — Release (by hand, per snapshot)

Per `NODE_CONFIG.md` §1 and §4.

1. On the Mac: compile the federated build configuration, collatz and the inspection domain; assemble
   under `~/.pgc/federated/sign.pem`. The key never leaves the Mac.
2. Copy to each node: the signed snapshot, `trust.pub`, the snapshot profiles (acceptance reads the
   claimed profile from outside the snapshot), and the Python wheels; the boundary also gets the
   transport source and the collatz binding and web client.
3. Per node: `role.env` and `pgc-<role>.service`, each `User=pgc`, `RequiresMountsFor=/srv/pgc/data`,
   with a store reachability check before start.
4. Start in order: coordinator, workers, boundary.

## 5. Verification

| Obligation | Check |
|---|---|
| OB-1 | A node given a copy of the snapshot with its signature altered refuses at authentication |
| OB-2 | The signing key is on no node and not on the host |
| OB-3 / EO-3 | Traces for a run exist on UC220; after a worker node is stopped and removed, they are intact |
| OB-4 / EO-5 | With one worker stopped the other serves every unit; no claimed unit runs twice |
| EO-1 | Four nodes active in their roles; the coordinator's `/health` reports the one `snapshot_id` |
| EO-2 | Coordinator stopped → a restarted worker refuses. Store stopped → a restarted node refuses at its reachability check; running nodes wait on the `hard` mount and resume, and no result changes |
| EO-4 | From the Mac: UC221:8000 answers; UC222–224 and UC220 refuse every port |
| EO-6 | `declared_environment_facts` is empty; one payload gives one determination on both workers |

After the checks: read `doc/profile_readback_signed_federated.md` back against this deployment.

## 6. Risks

- **Privileged nodes.** Root in a node is root on `shuttle`. `root_squash` keeps node root out of the
  store, but a node's root could reach the host and, through it, other instances. Node isolation
  from the host is not claimed.
- **Removing a node with the store mounted.** `lxc delete --force` on a node whose `hard` NFS mount
  is live leaves its NFS client in the shared kernel retrying forever; the host needed a console
  reboot. Stop a node (`lxc stop`, which unmounts) before deleting it.
- **Store loss blocks.** A `hard` mount makes a lost store a wait, never a changed result. A `soft`
  mount would fail writes mid-step, which is the breach EO-2 names.
- **Stateful domains.** Shared `data_root` gives workers one state, but concurrent units against the
  same capability state are serialized only by what the capability does today. The first deployment
  runs `collatz`; stateful domains follow once concurrency on shared state is examined.

## 7. Order of work

1. Phase A on the Mac, regression green.
2. Phase B by hand.
3. Phase C by hand, then §5.
4. Read-back and SOTU.

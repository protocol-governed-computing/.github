# Federated Deployment on `shuttle`

The `FEDERATED_NODE` composition (`STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V0`) runs on four LXC
nodes and an external evidence store, so that `SIGNED_FEDERATED_MULTINODE_PROFILE_V0` can be read
back against a deployment that can satisfy it. The deployment serves OB-2, OB-3, EO-1, EO-2, EO-3
and EO-4.

The nodes are configured by hand. `NODE_CONFIG.md` in this directory is the end configuration of
every machine and the recipe for reaching it. This document says why each piece is there.

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

All nodes run Ubuntu 24.04.5 and Python 3.12.3.

The layout carries three invariants:

- The private signing key exists only on the Mac. Nodes receive the public key as `PGC_TRUST_ROOT_PUBKEY`.
- `PGC_DATA_ROOT` on every node is the store mount. Traces, capability state and claims are written
  there directly. Nothing is staged on a node.
- Every node boots the same signed snapshot, identified by `snapshot_id`.

## 2. How the runtime realizes federation

`runtime/coordinator.py` realizes `LOCAL_MULTI_WORKER` with a process pool and refuses any other
placement. Federation is a separate realization, `runtime/federation/`.

**The coordinator** (`runtime/federation/coordinator.py`):

- refuses to start unless the sealed placement mode is `FEDERATED_NODE`;
- serves an internal HTTP endpoint: `POST /units` accepts a unit, `GET /units/<id>` returns its
  outcome, and `GET /health` reports `snapshot_id`;
- enqueues a unit by exclusive creation of `data_root/queue/<unit_id>.unit.json`, and never executes;
- refuses a unit submitted against another snapshot, or naming a domain the snapshot does not carry.

**A worker** (`runtime/federation/worker.py`):

- refuses to start unless the snapshot is `FEDERATED_NODE`, the store is writable, and the
  coordinator answers `/health` with the same `snapshot_id` (EO-2);
- polls `queue/`, claims by exclusive creation (atomic on NFSv4), runs `run_workflow` against the
  shared `data_root`, and writes `outcomes/<unit_id>.outcome.json`;
- never re-takes a claimed unit (OB-4).

**The boundary submits and does not execute.** `runtime.api.invoke_workflow` reads the sealed
placement mode. Under `FEDERATED_NODE` it submits the unit to `PGC_COORDINATOR_URL` and returns the
worker's outcome. Under every other mode it calls `run_workflow` in place. The transport resolver
calls `invoke_workflow`, so the engine has one runtime interface and no placement logic. The HTTP
adapter listens on `PGC_HTTP_BIND`: `127.0.0.1` by default, `0.0.0.0` on UC221.

**The commands** are `protocol_runtime coordinator` and `protocol_runtime worker`.

**The local proof** is `testbed/pgc/test_federation.py`, run by `regression.sh`. It runs one
coordinator and two workers as processes over a local directory that stands in for the store. It
checks that:

- determinations through the group equal those reached in place;
- each unit executes exactly once across two workers;
- claimed units are not re-dispatched, and a concurrent claim has one winner;
- every refusal holds: a non-federated snapshot, an unreachable store or coordinator, a boundary
  without a coordinator, and a unit from another snapshot.

**What each node needs.** Capability implementations are imported only at execution, so only
workers need them.

| Role | Needs |
|---|---|
| every node | `protocol_runtime`, `snapshot_assembler` (acceptance + signature verification), `cryptography` |
| boundary | + `snapshot_inspector`, `protocol_transport` source, the workload's HTTP binding |
| coordinator | nothing further |
| worker | + capability implementations (`software_governance`, `conformance_workloads`) |

## 3. Infrastructure

`NODE_CONFIG.md` §2–§3 gives the commands.

- **UC220 is a VM.** It runs `ubuntu:24.04 --vm`, bridged on `br0` with the pinned MAC
  `00:16:3e:00:02:20`, so the DHCP reservation keeps .220. It runs `nfs-kernel-server`, NFSv4 only,
  and exports `/srv/pgc/data` `rw,sync,root_squash` to .221–.224 individually.
- **Nodes mount the store themselves.** The nodes are privileged containers (the `bridged` profile),
  so each mounts the export over NFSv4 through `srv-pgc-data.mount`. AppArmor still confines a
  privileged container, so each node carries `raw.apparmor: mount fstype=nfs4, mount fstype=rpc_pipefs,`.
  The host is not in the evidence path.
- **One owner.** `pgc` is uid/gid 2001 on UC220 and every node. The export directory is `pgc`-owned
  and `0750`. With `root_squash`, root on a node cannot read the store; only the PGC services can.
- **Network policy.** Every instance runs an nftables input chain with policy drop, per §1.

These hold when every node writes as `pgc` and reads every other node's write, root on a node is
refused the store, a restarted node comes back with the mount and the rules, and only UC221:8000
answers from the LAN.

## 4. Releasing a snapshot to the nodes

`NODE_CONFIG.md` §1 and §4 give the commands.

1. On the Mac, compile the federated build configuration, collatz and the inspection domain. Assemble
   under `~/.pgc/federated/sign.pem`. The key never leaves the Mac.
2. Copy to each node: the signed snapshot, `trust.pub`, the snapshot profiles (acceptance reads the
   claimed profile from outside the snapshot), and the Python wheels. The boundary also gets the
   transport source, the collatz binding and the web client.
3. On each node, install `role.env` and `pgc-<role>.service`, each with `User=pgc`,
   `RequiresMountsFor=/srv/pgc/data`, and a store reachability check before start.
4. Start the coordinator, then the workers, then the boundary.

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

## 6. Limits

- **Privileged nodes.** Root in a node is root on `shuttle`. `root_squash` keeps node root out of the
  store, but a node's root could reach the host and, through it, other instances. The deployment
  does not claim node isolation from the host.
- **Removing a node with the store mounted.** `lxc delete --force` on a node whose `hard` NFS mount
  is live leaves its NFS client in the shared kernel retrying forever, and the host needs a console
  reboot. Stop a node (`lxc stop`, which unmounts) before deleting it.
- **Store loss blocks.** A `hard` mount makes a lost store a wait, never a changed result. A `soft`
  mount would fail writes mid-step, which is the breach EO-2 names.
- **Stateful domains.** A shared `data_root` gives workers one state. Concurrent units against the
  same capability state are serialized only by what the capability does. The deployment runs
  `collatz`. A stateful domain needs concurrency on shared state examined first.

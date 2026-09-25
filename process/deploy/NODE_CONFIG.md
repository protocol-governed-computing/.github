# Federated Node Group — End Configuration

What each machine holds when the `FEDERATED_NODE` composition is running, and how to set it by hand.
`PLAN.md` in this directory says why each piece is there.

| Host | Address | Role | Inbound allowed |
|---|---|---|---|
| Mac | LAN | build and sign | — |
| UC220 (VM) | 192.168.1.220 | evidence store | tcp 2049 from .221–.224 |
| UC221 | 192.168.1.221 | boundary | tcp 8000 from anywhere |
| UC222 | 192.168.1.222 | coordinator | tcp 8100 from .221, .223, .224 |
| UC223 | 192.168.1.223 | worker | none |
| UC224 | 192.168.1.224 | worker | none |

All: Ubuntu 24.04, Python 3.12. User `pgc`, uid/gid 2001, on every host.

```sh
groupadd -g 2001 pgc && useradd -r -u 2001 -g pgc -d /opt/pgc -s /usr/sbin/nologin pgc
```

---

## 1. Mac — build and sign (per release)

```sh
cd ~/protocol-governed-computing
PGC_SNAPSHOT_ROOT=$PWD/software_governance/snapshot_fed \
  protocol_compiler/compile.sh STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V1
protocol_compiler/compile_domain.sh conformance_workloads/workloads/collatz
protocol_compiler/compile_domain.sh snapshot_inspector
python -m assembler.cli assemble --profile SIGNED_FEDERATED_MULTINODE_PROFILE_V0 \
  --signing-key ~/.pgc/federated/sign.pem --out /tmp/pgc/snapshot \
  --source software_governance/snapshot_fed/compiled \
  --source conformance_workloads/workloads/collatz/snapshot/compiled \
  --source snapshot_inspector/snapshot/compiled
```

Copy to each node's `/opt/pgc/`: the `snapshot/` directory, `~/.pgc/federated/trust.pub` (never
`sign.pem`), and `.github/snapshot_profiles/*.md` into `profiles/`. The boundary also gets
`protocol_transport/{adapters,resolver,run_http.sh}` into `transport/` and
`conformance_workloads/workloads/collatz/client/{bindings,web}` into `client/`.

Python packages for every node, as wheels: `pip wheel --no-deps` of `protocol_runtime`,
`snapshot_assembler`, `snapshot_inspector`, `software_governance`, `conformance_workloads`, plus
`cryptography` and `pyyaml` (or let the node fetch those two from PyPI).

---

## 2. UC220 — evidence store

```sh
apt install nfs-kernel-server nftables
mkdir -p /srv/pgc/data && chown pgc:pgc /srv/pgc/data && chmod 0750 /srv/pgc/data
```

`/etc/exports.d/pgc.exports`
```
/srv/pgc/data 192.168.1.221(rw,sync,root_squash,no_subtree_check)
/srv/pgc/data 192.168.1.222(rw,sync,root_squash,no_subtree_check)
/srv/pgc/data 192.168.1.223(rw,sync,root_squash,no_subtree_check)
/srv/pgc/data 192.168.1.224(rw,sync,root_squash,no_subtree_check)
```

`/etc/nfs.conf.d/pgc.conf`
```
[nfsd]
vers3=n
```

`/etc/nftables.conf`
```
flush ruleset
table inet pgc {
  chain input {
    type filter hook input priority 0; policy drop;
    iif lo accept
    ct state established,related accept
    ip saddr { 192.168.1.221, 192.168.1.222, 192.168.1.223, 192.168.1.224 } tcp dport 2049 accept
  }
}
```

```sh
systemctl enable --now nfs-kernel-server nftables && exportfs -ra
```

---

## 3. Every node (UC221–UC224) — common

On `shuttle`, once per node (privileged containers are still AppArmor-confined):
```sh
lxc config set UC22x raw.apparmor 'mount fstype=nfs4, mount fstype=rpc_pipefs,' && lxc restart UC22x
```

In the node:
```sh
apt install nfs-common python3.12-venv nftables
mkdir -p /opt/pgc /srv/pgc/data
python3 -m venv /opt/pgc/venv
/opt/pgc/venv/bin/pip install <wheels> 'pgc-assembler[signing]'
```

`/etc/systemd/system/srv-pgc-data.mount`
```
[Unit]
Wants=network-online.target
After=network-online.target

[Mount]
What=192.168.1.220:/srv/pgc/data
Where=/srv/pgc/data
Type=nfs4
Options=hard,_netdev

[Install]
WantedBy=multi-user.target
```

`/opt/pgc/role.env` — common lines
```
PGC_SNAPSHOT_ROOT=/opt/pgc/snapshot
PGC_DATA_ROOT=/srv/pgc/data
PGC_TRUST_ROOT_PUBKEY=/opt/pgc/trust.pub
PGC_SNAPSHOT_PROFILES=/opt/pgc/profiles
PATH=/opt/pgc/venv/bin:/usr/bin:/bin
```

`/etc/systemd/system/pgc-<role>.service`
```
[Unit]
RequiresMountsFor=/srv/pgc/data
After=network-online.target srv-pgc-data.mount

[Service]
User=pgc
EnvironmentFile=/opt/pgc/role.env
ExecStartPre=/usr/bin/nc -z -w3 192.168.1.220 2049
ExecStart=<per role, below>
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

`/etc/nftables.conf` — as UC220's, with the node's own accept line (or none).

```sh
systemctl enable --now srv-pgc-data.mount nftables pgc-<role>
```

---

## 4. Per role

| Node | `role.env` additions | `ExecStart` | nftables accept line |
|---|---|---|---|
| UC222 coordinator | `PGC_COORDINATOR_BIND=0.0.0.0` · `PGC_COORDINATOR_PORT=8100` | `/opt/pgc/venv/bin/protocol_runtime coordinator` | `ip saddr { 192.168.1.221, 192.168.1.223, 192.168.1.224 } tcp dport 8100 accept` |
| UC223, UC224 worker | `PGC_COORDINATOR_URL=http://192.168.1.222:8100` | `/opt/pgc/venv/bin/protocol_runtime worker --id %H` | none |
| UC221 boundary | `PGC_COORDINATOR_URL=http://192.168.1.222:8100` · `PGC_HTTP_BIND=0.0.0.0` · `PGC_HTTP_PORT=8000` · `PYTHON=/opt/pgc/venv/bin/python` · `PGC_HTTP_BINDINGS=/opt/pgc/client/bindings/http.json` · `PGC_STATIC_MOUNTS=/=/opt/pgc/client/web;/traces=/srv/pgc/data/traces;/snapshot=/opt/pgc/snapshot` | `/opt/pgc/transport/run_http.sh` | `tcp dport 8000 accept` |

Start order: coordinator, then workers (they refuse until the coordinator answers), then boundary.

---

## 5. Check it works

From the Mac:
```sh
curl -s -X POST http://192.168.1.221:8000/collatz -H 'Content-Type: application/json' -d '{"number": 27}'
```

A `"result_class": "SUCCESS"` response with a `trace:` reference means the request crossed
boundary → coordinator → worker → store. On UC220, `ls /srv/pgc/data/outcomes` shows the record,
naming the worker that ran it.

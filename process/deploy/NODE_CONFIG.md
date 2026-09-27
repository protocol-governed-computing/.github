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

All: Ubuntu 24.04, Python 3.12. Commands below run as root (`sudo -i`). User `pgc`, uid/gid 2001,
on every host.

```sh
groupadd -g 2001 pgc && useradd -r -u 2001 -g pgc -d /opt/pgc -s /usr/sbin/nologin pgc
```

**Already in place:** UC220 (§2) is configured and its store is empty; the AppArmor allowance (§3,
first step) is set on UC221–UC224; every host has user `bp` with SSH keys, and `bp` has passwordless
sudo on UC221–UC224. UC221 additionally has `nfs-common` and a temporary manual mount of the store —
`umount /srv/pgc/data` before enabling the mount unit, or leave it and the unit adopts it.

---

## 1. Mac — build and sign (per release)

```sh
cd ~/protocol-governed-computing
PGC_SNAPSHOT_ROOT=$PWD/software_governance/snapshot_fed \
  protocol_compiler/compile.sh STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V2
protocol_compiler/compile_domain.sh conformance_workloads/workloads/collatz
protocol_compiler/compile_domain.sh snapshot_inspector
python -m assembler.cli assemble --profile SIGNED_FEDERATED_MULTINODE_PROFILE_V0 \
  --signing-key ~/.pgc/federated/sign.pem --out /tmp/pgc/snapshot \
  --source software_governance/snapshot_fed/compiled \
  --source conformance_workloads/workloads/collatz/snapshot/compiled \
  --source snapshot_inspector/snapshot/compiled
```

Stage everything a node receives under `/tmp/pgc`, then copy it to each node:

```sh
find /tmp/pgc/snapshot -name .DS_Store -delete          # acceptance refuses undeclared content
mkdir -p /tmp/pgc/profiles /tmp/pgc/wheels /tmp/pgc/transport /tmp/pgc/client
cp .github/snapshot_profiles/*.md /tmp/pgc/profiles/
cp ~/.pgc/federated/trust.pub /tmp/pgc/                 # the public half only — never sign.pem
python -m pip wheel -q --no-deps -w /tmp/pgc/wheels \
  ./protocol_runtime ./snapshot_assembler ./snapshot_inspector ./software_governance ./conformance_workloads
rsync -a --exclude __pycache__ protocol_transport/adapters protocol_transport/resolver \
  protocol_transport/run_http.sh /tmp/pgc/transport/
rsync -a conformance_workloads/workloads/collatz/client/bindings \
  conformance_workloads/workloads/collatz/client/web /tmp/pgc/client/
for n in 221 222 223 224; do rsync -a /tmp/pgc/ bp@192.168.1.$n:pgc/; done
```

`transport/` and `client/` are used only by the boundary; the other nodes may ignore them. Copy with
`rsync` or `scp`, not Finder: the Mac adds `.DS_Store` files, and acceptance refuses a snapshot
carrying them.

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
    ip saddr { 192.168.1.75, 192.168.1.201 } tcp dport 22 accept
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

In the node, after the Mac's copy has landed in `~bp/pgc`:
```sh
groupadd -g 2001 pgc && useradd -r -u 2001 -g pgc -d /opt/pgc -s /usr/sbin/nologin pgc
apt install -y nfs-common python3.12-venv nftables
mkdir -p /opt/pgc /srv/pgc/data
cp -r ~bp/pgc/. /opt/pgc/
python3 -m venv /opt/pgc/venv
/opt/pgc/venv/bin/pip install /opt/pgc/wheels/*.whl 'cryptography>=42'
```

`cryptography` and `pyyaml` come from PyPI here; everything PGC comes from the wheels.

`/etc/systemd/system/srv-pgc-data.mount`
```
[Unit]
Wants=network-online.target
After=network-online.target

[Mount]
What=192.168.1.220:/srv/pgc/data
Where=/srv/pgc/data
Type=nfs4
Options=hard,_netdev,lookupcache=none,actimeo=0

[Install]
WantedBy=multi-user.target
```

`hard` makes a lost store a wait, never a failed write. `lookupcache=none,actimeo=0` makes every node
see another node's writes at once: the capabilities save by writing a new file and renaming it over
the old one, and a client caching names or attributes can read the replaced file for seconds after
the rename — a worker would then decide from state another worker has already changed.

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

`/etc/nftables.conf` — as UC220's, with the node's own accept line from §4 in place of the 2049 line.

**Keep the SSH line in every node's rules** — `ip saddr { 192.168.1.75, 192.168.1.201 } tcp dport 22 accept`
(the Mac and `shuttle`) — or enabling nftables ends your SSH access (the session in progress
survives; the next login does not). SSH is admitted from those two admin addresses only, so EO-4
holds except for them; the read-back records the exception. `bp`'s `authorized_keys` holds the Mac's
keys and `shuttle`'s.

Enable the mount and the firewall first, then the service, in the start order of §4:

```sh
systemctl daemon-reload
systemctl enable --now srv-pgc-data.mount nftables
findmnt /srv/pgc/data                                   # must show 192.168.1.220:/srv/pgc/data
systemctl enable --now pgc-<role>
journalctl -u pgc-<role> -n 20                          # expect "Authenticated under trust root …"
```

---

## 4. Per role

| Node | `role.env` additions | `ExecStart` | nftables accept line |
|---|---|---|---|
| UC222 coordinator | `PGC_COORDINATOR_BIND=0.0.0.0` · `PGC_COORDINATOR_PORT=8100` | `/opt/pgc/venv/bin/protocol_runtime coordinator` | `ip saddr { 192.168.1.221, 192.168.1.223, 192.168.1.224 } tcp dport 8100 accept` |
| UC223, UC224 worker | `PGC_COORDINATOR_URL=http://192.168.1.222:8100` | `/opt/pgc/venv/bin/protocol_runtime worker --id %H` | none |
| UC221 boundary | `PGC_COORDINATOR_URL=http://192.168.1.222:8100` · `PGC_HTTP_BIND=0.0.0.0` · `PGC_HTTP_PORT=8000` · `PYTHON=/opt/pgc/venv/bin/python` · `PGC_HTTP_BINDINGS=/opt/pgc/client/bindings/http.json` · `PGC_STATIC_MOUNTS=/=/opt/pgc/client/web;/traces=/srv/pgc/data/traces;/snapshot=/opt/pgc/snapshot` | `/opt/pgc/transport/run_http.sh` | `tcp dport 8000 accept` |

Start order: coordinator, then workers (they refuse until the coordinator answers), then boundary.

`run_http.sh` must stay executable after copying (`chmod +x /opt/pgc/transport/run_http.sh`).

---

## 5. Check it works

From the Mac:
```sh
curl -s -X POST http://192.168.1.221:8000/collatz -H 'Content-Type: application/json' -d '{"number": 27}'
```

A `"result_class": "SUCCESS"` response with a `trace:` reference means the request crossed
boundary → coordinator → worker → store. On UC220, `ls /srv/pgc/data/outcomes` shows the record,
naming the worker that ran it.

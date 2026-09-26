# Reading a snapshot back against the profile it claims

The work no tool performs. The assembler checks a floor — required kinds, required domains, entry
points — and passes. Everything else a profile says is checked by a person reading it against a
composition and the deployment running it, and this is that reading.

## Subject

| | |
|---|---|
| **snapshot** | `347be1741d7a1191bf7863462d4ec41340a33e2de7375c8c51145a59a3b201d4` |
| **profile** | `SIGNED_FEDERATED_MULTINODE_PROFILE_V0` |
| **composition** | 3 domains — platform, workload, inspection — 212 artifacts |
| **placement** | `FEDERATED_NODE`, built from `STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V1` |
| **signed under** | `e5f15d7a0173e70a`; the private half is held by the build machine alone |
| **deployment** | four LXC nodes on one LXD host, an evidence store in a separate VM, a build machine outside the group; every node configured by hand per `process/deploy/NODE_CONFIG.md` |

| Node | Address | Role |
|---|---|---|
| UC221 | 192.168.1.221 | interaction boundary |
| UC222 | 192.168.1.222 | coordinator |
| UC223, UC224 | 192.168.1.223, .224 | workers |
| UC220 | 192.168.1.220 | evidence store (NFSv4), not a node |
| build machine | 192.168.1.75 | compiles, assembles, signs; never executes |

The nodes meet only at the store. The coordinator queues a unit; a worker claims it by exclusive
creation, executes it, and writes its outcome and trace; the boundary reads the outcome back through
the coordinator. Every demonstration below was run against this deployment.

## How to read a verdict

| | |
|---|---|
| **Holds** | checked against this composition and deployment, and the check could have failed |
| **Partial** | some clause holds and some does not; the entry says which |
| **Not satisfied** | the obligation is in force and this deployment does not meet it |
| **Not testable here** | the deployment cannot exhibit the condition either way — recorded, never counted as met |

---

## §1 — what the platform means

The assembler's composition check passed: five composition-scoped rules over 212 artifacts. The
selections below are properties of the governance surface, which this composition shares with the
multi-worker composition read earlier; the one added artifact is the `FEDERATED_NODE` placement
structure.

| Selection | Verdict |
|---|---|
| 16 admissible kinds, `ASSERT` admitted and not required | **Holds** |
| 15 required kinds | **Holds** — none missing |
| required domains `platform`, `inspection` | **Holds** — both carried, plus `workload` |
| four outcomes; no fifth | **Holds** — no liveness signal entered the vocabulary, though a node can now be lost |
| four result classes at the boundary | **Holds** |
| 29 namespaces, closed | **Holds** |
| retention window declared **in the snapshot** | **Holds** — `CS_EVIDENCE_EXPIRY_V0` carries `retention_window_days` |

## §2 — required governance artifacts

**Holds.** The eleven identities §2 names are present. The finding stands:
`required_governance.artifacts` is `[]`, so the machine-checked list requires none of them, and a
profile whose §2 emptied would still assemble.

## §3 — the five obligations

| | Verdict | Evidence |
|---|---|---|
| **OB-1** no node executes an unverified snapshot | **Holds** | on UC223, a copy of the deployed snapshot with one character of its signature changed was refused at authentication: `SignatureInvalid: signature over 347be174… does not verify under key e5f15d7a0173e70a`. The intact snapshot authenticated and booted. Only the signature was altered, so acceptance passed and the refusal is authentication's |
| **OB-2** no executing node can sign | **Holds** | the signing key's SHA-256 matches no private-key file on any node, on the store, or in the host's home and temporary directories; only its hash left the build machine. The nodes hold SSH host keys and nothing else. The signing *code* is installed on every node — the assembler package provides verification — so what is withheld is the key, not the capability |
| **OB-3** evidence is not held by the node that produced it | **Holds** | UC223's two traces were fingerprinted, then UC223 was stopped. Both were byte-identical on UC220 while it was down; UC224 served every request meanwhile; UC223 rejoined unaided when started |
| **OB-4** re-dispatch never resumes a begun step | **Holds** | a unit whose claim was written by a worker that never produced an outcome stayed `claimed` and was executed by no one — also after a worker restart — while a control unit written beside it was taken and executed within seconds |
| **OB-5** only the boundary node is externally reachable | **Holds, with a named exception** | from outside the group only UC221:8000 answers; every other port on every node and on the store is dropped silently. SSH is admitted from two administrative addresses, the build machine and the LXD host, on all five machines |

**All five hold.** OB-2, OB-3 and OB-5 were unmet or untestable on one host and are met by placing
the same composition on nodes.

## §4 — the claims, and demonstrations that could have failed

**`SNAPSHOT_IMMUTABILITY` — Holds.** On UC224, one byte appended to `tokenized/workload/dispatch.json`
in a copy of the deployed snapshot; boot refused at acceptance, naming the file and both hashes.

**`DETERMINISTIC_EXECUTION` — Holds.** One workflow and payload submitted eight times through the
boundary; both workers reached it, and every determination hashed alike on UC223 and UC224
(`21488c857a130358` over the canonical surface). The hash is the one an earlier installation of this
snapshot produced, so the determination held across workers and across installations. This is where
federation could have broken it: a worker executes a topology it did not receive from a caller, on a
host the caller never sees.

**`COMPILED_INVOCATION_RESOLUTION` — Holds.** A unit naming a workflow the snapshot does not seal was
admitted into a sealed domain and refused by the worker that took it:
`FQDN not in vocab: 'workload::WF_NOT_SEALED_V0'`. A unit naming an unsealed domain was refused by
the coordinator before any worker saw it.

**`SIGNED_SNAPSHOT_VERIFICATION` — Holds.** The OB-1 demonstration.

**`EVIDENCE_EXPIRY` — Holds, not re-run here.** Established against the multi-worker composition;
the capability and its window are unchanged in this one. Expiry over a store shared by four nodes
has not been exercised.

## §5 — derivation

**Holds.** The profile derives from `GOVERNANCE_SURFACE_PROFILE_V0` and widens nothing.

## §6 — externality

**Not satisfied.** The same party wrote this profile, the platform claiming it, the governance
surface it derives from, the deployment, and this reading. A second node group does not supply a
second reader.

## Environment profile — EO-1 … EO-6

| | Verdict |
|---|---|
| **EO-1** four separately addressable nodes, roles distinct | **Holds** — four hosts with their own names and addresses, one role service each and no other; the snapshot on disk, every service's log, and the coordinator's `/health` all name `347be174…` |
| **EO-2** prerequisites reachable or execution does not start | **Holds** — a worker refused to start while the coordinator was down and started once it returned; a worker refused to start while the store was down, at a reachability check before it touches the mount. A request made during a store outage waited, and returned `SUCCESS` when the store came back, with one unit executed |
| **EO-3** evidence store external to every node | **Holds** — the store is a separate VM that runs no PGC code; the OB-3 demonstration |
| **EO-4** only the boundary node externally reachable | **Holds, with a named exception** — the OB-5 demonstration |
| **EO-5** re-dispatch limited to un-started work | **Holds** — with UC223 stopped, UC224 took every new unit; a begun unit was never taken again |
| **EO-6** no declared environmental input | **Holds** — `declared_environment_facts` is `[]`, and one payload gave one determination on both worker nodes |

### EO-2: what the first reading found

The store-outage demonstration was run twice. The first time, the boundary gave up on the
coordinator after ten seconds and reported `EXECUTION_FAILURE`; when the store returned, the
coordinator's blocked write completed and the unit executed with `SUCCESS`. The caller had been
told the opposite of what the evidence then recorded. Unreachability had changed a result, which is
the breach EO-2 names.

The boundary now reports failure only while it is still true that nothing was admitted — the
coordinator could not be connected to, or it refused the unit. Once a unit is admitted its outcome
is waited for without limit. The second run is the one recorded above. One case remains ambiguous:
a connection lost after the unit was sent and before the coordinator answered, where admission is
unknown and the error says so.

The store is a `hard` NFS mount, and that choice is what EO-2 rests on. A lost store makes a node
wait; it never makes a write fail partway through a step. A `soft` mount would have turned an outage
into failed capability writes — a result changed by unreachability.

### What the environment does not claim

**The exception to EO-4.** SSH reaches every node and the store from the build machine and the LXD
host. That reachability was chosen for administration and is named here rather than argued away. A
non-administrative host on the LAN was not probed; the rules drop its traffic, but that was not
observed.

**The nodes share a kernel.** They are privileged containers on one LXD host. Root in a node is root
on the host, so isolation of a node from the host, and through it from its peers, is not claimed.
The store keeps node root out (`root_squash`; only the PGC service user reads it), which is the
property OB-3 needs and no more.

**Losing a node abruptly wedges the host.** An earlier installation of this deployment was tested by
destroying a node with `lxc delete --force`. Its evidence survived and the group kept serving, but
the host could not finish removing it: the node's NFS client lives in the shared kernel, its network
was gone, and a `hard` mount retries forever. The host needed a console restart. On separate
machines a lost node takes its client with it. Here a node is removed by stopping it first, and the
loss recorded under OB-3 is a stop.

---

## What this reading establishes

**The composition that satisfied what the profile means now satisfies where it runs.** All five
obligations and all six environment obligations hold on a deployment that could have failed each of
them, two with the administrative exception named above. Several were demonstrated by breaking
something: a signature, a constituent, a node, the store.

**One of them held only after the reading changed the platform.** EO-2 failed on the first store
outage because the boundary turned a delay into a failure; the fix was to stop it guessing. It is the
one defect this reading found, and finding it is what a read-back is for.

**The profile remains `usable_as_a_target: false`.** The precondition of use — a read-back against a
candidate — is met, and on a deployment. What keeps it from being handed to anyone as a target met is
the externality requirement, which only a second party can discharge.

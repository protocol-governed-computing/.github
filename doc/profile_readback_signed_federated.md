# Reading a snapshot back against the profile it claims

The work no tool performs. The assembler checks a floor — required kinds, required domains, entry
points — and passes. Everything else a profile says is checked by a person reading it against a
composition, and this is that reading.

## Subject

| | |
|---|---|
| **snapshot** | `f899c0d8ba6ff6e0b2fa76eb43cfb3010e2095ab44b696d0c37f456aacaa3466` |
| **profile** | `SIGNED_FEDERATED_MULTINODE_PROFILE_V0` |
| **composition** | 3 domains — platform, workload, inspection — 211 artifacts |
| **placement** | `LOCAL_MULTI_WORKER`, built from `STRUCTURE_BUILD_PLATFORM_MULTIWORKER_CONFIG_V1` |
| **deployment** | one host, worker processes; no separately addressable nodes |

The last row decides most of what follows.

## How to read a verdict

| | |
|---|---|
| **Holds** | checked against this composition, and the check could have failed |
| **Partial** | some clause holds and some does not; the entry says which |
| **Not satisfied** | the obligation is in force and this deployment does not meet it |
| **Not testable here** | the deployment cannot exhibit the condition either way — recorded, never counted as met |

**Not testable here is not a pass.** A profile obligation about four nodes, read against one host,
is unestablished rather than satisfied. Reporting it otherwise would make the read-back a formality.

---

## §1 — what the platform means

Machine-checked by the assembler, and re-checked here against the sealed composition.

| Selection | Verdict |
|---|---|
| 16 admissible kinds, `ASSERT` admitted and not required | **Holds** — the A1/A1b distinction is exercised, not theoretical |
| 15 required kinds | **Holds** — none missing |
| required domains `platform`, `inspection` | **Holds** — both carried, plus `workload` |
| four outcomes; no fifth | **Holds** — no liveness signal entered the vocabulary |
| four result classes at the boundary | **Holds** |
| 29 namespaces, closed | **Holds** |
| retention window declared **in the snapshot** | **Holds** — `CS_EVIDENCE_EXPIRY_V0` carries `retention_window_days`, so a party holding the snapshot reads the rule off the snapshot |

## §2 — required governance artifacts

`required_governance.artifacts` is `[]`, so the assembler checks nothing here. §2's prose names
eleven identities, and all eleven are present: the three governing constitutions, the six
constitutions this platform's own decisions rest on, and the expiry side effect.

**Holds**, and worth noting how nearly it did not. §2 was written naming an artifact nobody had
authored — an evidence-expiry capability — precisely so the profile could refuse the platform its
own author was building. It refused, and then the artifact was written.

**Finding.** The prose and the machine-checked list disagree in reach: eleven identities are
required by §2 and none by the field the assembler reads. A profile whose §2 emptied tomorrow would
still assemble.

## §3 — the five obligations

| | Verdict | Evidence |
|---|---|---|
| **OB-1** no node executes an unverified snapshot | **Holds** | an anchored node presented a snapshot whose signature does not verify refused at authentication, naming the identity and the key; an unanchored node booted the same snapshot, so the reference composition is unaffected |
| **OB-2** no executing node can sign | **Not satisfied** | the build machine and the executing node are the same host. The private half is on it. The runtime holds no signing path and imports only verification, which is a property of the code and not of the deployment the obligation is about |
| **OB-3** evidence is not held by the node that produced it | **Not satisfied** | claims and traces sit under one `data_root` on the executing host. Removing that host removes the evidence |
| **OB-4** re-dispatch never resumes a begun step | **Holds** | six units dispatched across three workers, all claimed; re-dispatching the same six executed nothing. Claims are taken by exclusive creation, so the filesystem decides once |
| **OB-5** only the boundary node is externally reachable | **Not testable here** | there is no node group. Worker processes are not addressable, so nothing can reach one and nothing is prevented from reaching one |

**Two of five hold, two are not satisfied, one cannot be exhibited.** The two failures share a
cause: one host. They are not defects in the platform and they are not met.

## §4 — the claims, and demonstrations that could have failed

Each was run against this composition.

**`SNAPSHOT_IMMUTABILITY` — Holds.** One constituent altered; boot refused at acceptance naming the
file and both hashes.

**`DETERMINISTIC_EXECUTION` — Holds.** The same workflow and payload executed by four workers in
four processes; all four determinations identical. This tests SM-10 across workers, which a
single-process platform cannot exercise at all.

**`COMPILED_INVOCATION_RESOLUTION` — Holds.** A workflow the dispatch table does not name refused:
`WF FQDN not in vocab`. Nothing resolved at run time that was not sealed.

**`SIGNED_SNAPSHOT_VERIFICATION` — Holds.** An anchored node refused a snapshot whose signature does
not verify: `SignatureInvalid: signature over f899c0d8… does not verify under key 70c5f1e7…`.

*The first attempt at this demonstration was invalid and is recorded because the failure is
instructive.* It corrupted a signature on an already-tampered snapshot, so acceptance refused before
authentication ran, and the result would have been reported as a signature refusal that never
happened. A demonstration that cannot isolate what it claims to test establishes nothing. It was
re-run on an intact snapshot.

**`EVIDENCE_EXPIRY` — Holds.** Evidence past a five-day window ended together with its attestation;
evidence within the window survived; the deletion was recorded to an append-only stream. Both halves
of the claim were checked — that the determination becomes unestablishable, **and** that a record of
the ending survives, without which deleted evidence cannot be told from evidence never written.

**All five discharged.** Every claim in §1 is supported by a demonstration that ran and could have
failed.

## §5 — derivation

**Holds.** The profile derives from `GOVERNANCE_SURFACE_PROFILE_V0` and widens nothing: every
selection the base makes is made here, and this profile only requires more — a trust root where the
base names none, a bounded window where the base leaves retention open, attributed reads, an
exercised boundary, five obligations.

Both profiles now sit in one directory and neither supersedes the other. A composition claims one.

## §6 — externality

**Not satisfied, and recorded as failing rather than argued around.** The same party wrote this
profile, the platform claiming it, and the governance surface it derives from. NP-7 is unmet and no
wording here can meet it.

The read-back does not improve this. **It was performed by the same party too.** A profile read
against a composition by its own author establishes that the author believes it holds, which is
weaker than what a read-back is for, and it is the honest description of this document.

## Environment profile — EO-1 … EO-6

| | Verdict |
|---|---|
| **EO-1** four separately addressable nodes, roles distinct | **Not satisfied** — four worker processes on one host, not addressable, no boundary or coordinator node |
| **EO-2** prerequisites reachable or execution does not start | **Partial** — boot refuses an unreadable or unverifiable snapshot; nothing checks reachability of an evidence store that is a local directory |
| **EO-3** evidence store external to every node | **Not satisfied** — same cause as OB-3 |
| **EO-4** only the boundary node externally reachable | **Not testable here** |
| **EO-5** re-dispatch limited to un-started work | **Holds** — the OB-4 demonstration |
| **EO-6** no declared environmental input | **Holds** — `declared_environment_facts` is `[]`, and no determination varied across four workers, which is the one way this deployment can test it |

**The environment profile is the part this deployment mostly cannot meet**, and it is the part whose
obligations are about placement. That is the expected shape: the composition satisfies what the
platform *means*; the deployment does not yet satisfy where it *runs*.

## Domain profiles

`platform` and `transformation` each claim authority, and each names a decision no other domain may
make — admission, and sufficiency. Both claims are stated in the profile and **neither is checked by
anything**: no mechanism establishes that no other domain admits an artifact, or that no other
domain decides when construction refuses. Recorded as asserted rather than established, which is
what the generated text already said before the tables were filled.

---

## What this reading establishes

**The profile is not decorative.** It refused a composition that lacked an artifact nobody had
written, and the artifact was written in response. Its five claims are discharged by demonstrations
that ran. Its §1 selections hold against the sealed composition.

**Five obligations are unmet, and all five have one cause.** OB-2, OB-3, EO-1, EO-3 and EO-4 are
about a deployment of several nodes. There is one host. Nothing about the platform prevents meeting
them; nothing about this deployment meets them.

**The profile remains `usable_as_a_target: false`**, and correctly. §7 makes being read against a
candidate snapshot the precondition of use. That reading has now happened, which satisfies the
precondition — and the reading found five unmet obligations and an unmet externality requirement, so
the profile is not yet something to hand anyone as a target met.

**What would change the verdict** is a deployment, not a change to the platform: nodes that are
separately addressable, an evidence store held by none of them, and a build machine that is not one
of them.

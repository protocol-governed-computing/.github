# Rulings

Each repository's `CLAUDE.md` holds the doctrine for that repository, and each is gitignored.
Rulings recorded only there are neither versioned nor backed up. This file is where a ruling
is kept. A `CLAUDE.md` may repeat a ruling so it is in front of whoever works in that repository,
but the ruling stands here.

A ruling is a decision about how something is to be read or done, made once so it is not re-argued
each time it comes up. Each entry says what was decided, why, and where it is applied. Only a later
ruling overturns an earlier one, and it names the ruling it replaces.

---

## Transformation

### A dossier is admitted on what it says, not on how it was written — C1, v5

**Ruling.** The phase checks admit a document; they do not see how it was produced. A generated
dossier is permitted, and this is a stated limit for v5.

**Conditions:**
- **Keep the generator as evidence,** exactly as it ran.
- **Say it was generated** in the dossier's `delivery.md`.
- **A generator is not a design authority.** Anything it infers that no register states is caught
  by construction completeness, which must still be 100%.

**Why.** CLM's P7, with 47 topology rows and 280 bindings, and its P8 were written by scripts from P5
and P6. Every rule admitted them as it would have admitted the same text typed by hand. Governing
generation, or making the design language small enough to write by hand, is larger than v5.

**Applied.** CLM's generators are in `notes/clm-generators/`, and its `delivery.md` states they were
used. Governed generation is v6 work.

### A change request pins the composition without its own output — lesson 4

**Ruling.** A CR's baseline is the composition the change is designed *against*. It is never one
that already holds what the change emits. For a domain's first CR, that means without the domain.

**Why.** Pinned against a build that contains it, every `NEW` row reads as `*_ALREADY_EXISTS`, and
P7 and P8 are refused. The default build includes every domain with source, so once a CR is emitted
the working `snapshot/` stops being a valid pin for it.

**Applied.** The pin comes from one side assembly, not from stashing and switching branches:

```
PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 \
PGC_SOURCE_ROOTS=<every */snapshot/compiled root but the CR's domain, ':'-separated> \
PGC_SNAPSHOT_OUT=<scratch dir> ./snapshot_assembler/assemble.sh
tc baseline show --snapshot <scratch dir> > <dossier>/baseline.json
```

Then run the phase checks with `--snapshot <scratch dir>`. The side assembly's id equals the pin
exactly when nothing outside the CR has changed, which makes it the test for whether a pin is
current.

**The exception** is a dossier re-authored against a composition holding its own earlier output.
Its rows move to `EXTEND`, deliberately.

### Validation criteria are designed from P0, not written after the build — lesson 2

**Ruling.** A domain's execution-validation criteria are drawn from the seed's acceptance criteria
and `operation_refusals`, in the seed's own words, while P7 is written.

When a criterion fails, first ask whether the criterion misread P0. Only then treat the failure as
a defect in the design or the platform. One workflow is dispatched as soon as artifacts are emitted.

**Why.** A criterion written after the build drifts toward what the system does. One of CLM's
expected a stopped response to keep its partial words; the seed says the model "gives no response".
And every phase check passed CLM's routing collision; the first dispatch found it.

**Applied.** This is doctrine: no register holds validation criteria yet, and no rule checks them
against P0.

---

## Runtime

### Deployment configuration is not branching — C2 and C3, v5

**Ruling.** The sealed snapshot decides behaviour: whether execution is federated, and how a unit
is admitted, executed and evidenced. These may come from the environment or the CLI:
- where a coordinator listens;
- the address a node reaches it at;
- how long a node waits to *connect*.

**Why.** Those are facts about a deployment. A snapshot is sealed once and run on many deployments,
so it cannot know them. `runtime.api` reading `PGC_COORDINATOR_URL` under a sealed `FEDERATED_NODE`
placement is conforming: the placement decides, and the environment supplies only the address.

**Applied.**
- The only defaults the runtime carries are in `protocol_runtime/runtime/federation/defaults.py`:
  bind, port, connect timeout and poll interval, each documented and overridable.
- The bind defaults to loopback, as a safety property.
- A new default goes there or nowhere. Anything that would change what a run determines belongs in
  the snapshot.

### An unknown admission after a dropped connection is a stated limit — C5, v5

**Ruling.** Suppose a connection drops after a unit is sent and before the coordinator answers.
Admission is then unknown, and the error says so. This is recorded as a known limit of v5.

**Why.** Resolving it needs a unit idempotency key and an admission-status query, so a retry can
ask whether the unit was admitted. That is design work, and it needs federated re-testing.

**Applied.** Recorded in the v5 release notes. The resolution is v6.

---

## Placement

### FEDERATED_NODE requires a store honouring POSIX record locks — C4, v5

**Ruling.** The constraint is declared in the `FEDERATED_NODE` placement, as a requirement on the
store workers share. It is not left to code alone.

**Why.** Capability correctness across workers depends on record locks. NFSv4 and local filesystems
honour them; an object store does not. A constraint held only in code is invisible to anyone
reading the profile.

**Applied.** It changes the placement artifact, so it belongs to v5's identity-changing batch
(v5 A batch, A8).

---

## Governance surface

### The transform constitutions are named for what they govern — v5

**Ruling.** `CONSTITUTION_CAPABILITY_TRANSFORMS_V0` is renamed `CONSTITUTION_DETERMINISTIC_ATOMS_V0`.
Each transform is governed by exactly one of three constitutions: deterministic atoms,
non-deterministic atoms, or molecules.

The three rules common to every transform stay where they were, option (a):
- surface closure;
- derived closure;
- implementation admissibility.

The constitution says so plainly.

**Why.** The old name claimed every transform, and it had governed one kind of three since
molecules and non-deterministic atoms were added.

**Applied.**
- Every current reference is renamed, and no alias is kept.
- Historical dossiers and `pgc_release` keep the old name, as they recorded it.
- A common home for the three rules is option (b), a separate change (v5 A batch, A6).

---

## Domains

### causal_language_model is a regression domain, frozen at CR-1 — v5

**Ruling.** CLM is part of the composition as a regression domain, delivered at CR-1 and frozen
there. CR-2 through CR-6 are parked. If the domain moves again, the next step is a real model as a
second realization of the declared step, not CR-2.

**Why.** CLM is the only domain exercising:
- molecules;
- recorded non-deterministic steps and replay;
- refusal moments;
- one contract at several places.

Its first run found a routing defect every phase check had passed. More business functions would
mostly repeat what CR-1 proved about the platform.

**Applied.** CLM is merged into dev/17, and `regression.sh` runs its suite. The reasoning is in
`notes/clm-process-check.md`.

---

### A profile's content is in the identity; profiles stay in `.github` — A1, v5

**Ruling.** The snapshot identity covers the content of the profile a snapshot claims, not only its
name. Profiles stay in `.github/snapshot_profiles/`, read through `PGC_SNAPSHOT_PROFILES` as today.
Moving them to a repository of their own is not part of v5.

**Why.** Today a profile can be weakened without changing the identity of any snapshot claiming it.
Hashing the content closes that, and it is the whole of the weakness. A repository of its own would
make profiles versioned and citable like the other components, which is worth having but is a
separate change with a larger reach: `release.sh`, `compose_release`, `pgc_install`.

**Applied.** Wave 4 of the A batch (v5 A batch, A1).

---

### A validator reports; the contract refuses — B8, v5

**Ruling.** `CT_PURE_VALIDATE_RECORD_STRUCTURE_V0` stays a reporter: it returns the violations it
finds and decides nothing. Each contract that validates a record refuses on what it finds, with a
following rule step requiring `violations == []`, as `causal_language_model::CC_CLAIM_MODEL_IDENTITY_V0`
already does.

**Why.** Four contracts — book's `CC_VALIDATE_BOOK_SUBMISSION_V0`, `CC_REGISTER_BOOK_V0` and
`CC_REGISTER_ADDITIONAL_EDITION_V0`, and blockchain's `CC_VALIDATE_REGISTRATION_V0` — validate and
never act on the result, so a malformed record is admitted. Making the transform refuse would fix
them in one place and leave no way to validate without deciding. Whether a violation refuses is the
business's rule, so it belongs in the business's contract.

**Applied.** Through a CR in each domain: book catalog, and blockchain identity with B9.

---

### Identity's admitted states are a literal — B9, v5

**Ruling.** `WF_ACCEPT_ACTOR_V0` and `WF_REJECT_ACTOR_V0` fix `states_admitting_a_decision` and
`admitted_outcomes` as literals, as wallet fixed its own. The fields leave the intents and the TIs.

**Why.** The TIs hold the sets as constants, so the transport boundary cannot widen them, but the
workflows admit them from the payload, so a caller invoking a workflow directly can. A business rule
the caller supplies is a business rule the caller can widen (`cr_04_wallet` delivery).

**Applied.** A blockchain identity CR, carrying B8's blockchain contract as well.

---

### ai_governance's three checks refuse — B10, v5

**Ruling.** `CT_PURE_CHECK_QUOTA_AVAILABLE_V0`, `CT_PURE_CHECK_TRAINING_STATUS_V0` and
`CT_PURE_EVALUATE_INACTIVITY_V0` keep PGC's behaviour: they refuse, as their `refusal: raises`
declares. The vectors inherited from RI-0, which expect a negative answer, are replaced by vectors
proving the refusal.

**Why.** The refusal was declared deliberately, and the vectors are what went stale.

**Applied.** An ai_governance CR.


---

### A contract redeclared whole requires only what it declares — cr_05_identity, v5

**Ruling.** `NODE_INPUT_UNBOUND` reads a contract's required inputs from the design where the design
composes that contract's steps. The pinned contract's inputs are joined only for a contract the
design calls without composing.

**Why.** The rule joined the pinned inputs to the design's so that a reused contract could not be
handed nothing. A design that redeclares a contract whole authors its interface again, and an input
it withdraws is no longer required. Joined, the only way to pass was to hand the contract a rule
none of its steps read — the constant the change exists to remove.

**Applied.** `transformation/design/checks.py` and the P7 rule set, re-sealed;
`keyed_node_design_test` proves both halves.

---

### An amendment declares what it withdraws — cr_05_identity, v5

**Ruling.** P7 gains `withdrawn_facts`: an artifact the design extends, a place in its machine
block, and the reason the fact goes. Construction subtracts declared withdrawals from what an
amendment loses; a fact omitted without one is still refused, and a withdrawal covering nothing
lost is refused as unfounded. `WITHDRAWAL_NOT_AN_AMENDMENT` holds a withdrawal to an `EXTEND`.
Separately, the narrowing guard now treats a value refined into a list as refined, as it already
treated one refined into an object.

**Why.** An `EXTEND` is rendered whole, so an omission and a decision read the same in the rendered
artifact, and the guard refused both. Trusting the redeclaration, as the P7 interface ruling does,
would have given up the guard's purpose. Stating the decision keeps it.

**Applied.** Template, P7 rule set (re-sealed, 241 rules), `completeness.py`, `cli.py`;
`withdrawal_design_test` (5/5). The register was added empty to every current-format P7 document.

---

### An entrance supplies what its gate requires — B25, v5

**Ruling.** P7 gains `ENTRANCE_UNDERSUPPLIES_GATE`: every field the gate of an entrance's workflow
requires is supplied by the entrance's payload. The gate is read from the design where the design
states it, and from the composition otherwise; `si.capability.surface` now publishes each intent's
workflow and inputs under `intents`, beside contracts.

**Why.** `cr_05_identity` stopped an entrance sending a field its workflow no longer read and reused
the gate that still required it. Every phase admitted the design, construction was complete, and
every registration through the entrance was refused at admission. The first request found it.

**Applied.** `snapshot_inspector` capability surface; `transformation` check, rule and observation,
P7 re-sealed at 242 rules; `entrance_gate_design_test` 4/4. No current P7 document trips it.

---

### An amendment is built as it was measured — B10, v5

**Ruling.** The domain build manifest is generated for a change that only amends, and it describes
the domain, naming every subdomain the domain holds, not only those the change declares. `construction
emit` carries forward the descriptions of the document it replaces, exactly as `construction check`
does when it measures the amendment.

**Why.** `cr_01_licensing` amends three transforms and creates nothing. The generator returned no
manifest, so the domain could not compile the cases, and it would have described ai_governance as
having one subdomain. `check` then measured the amendment as complete with its predecessor's
descriptions carried, and `emit` wrote it without them. The book and identity amendments had never
shown the gap, because their predecessors were themselves rendered and carried no descriptions.

**Applied.** `render.build_manifest` (amendments, held subdomains, declared root), `generators`
reads the held subdomains from the domain's registry, `cli.construction_emit` reads its
predecessors; `vector_design_test` 8/8.

---

### A process verifies once; a run writes evidence, not pictures — runtime performance, v5

**Ruling.** `runtime.api` keeps a booted snapshot resident per process, keyed by the manifest file
and by what acceptance was judged against (trust anchor, profile root). A rewritten manifest is
verified afresh; `boot()` itself is never cached. A run writes its `.jsonl` evidence only; the
path's picture is drawn on request (`run --behavior-logic`, `behavior-logic <trace>`). This reverses
"every execution trace has a picture".

**Why.** Measured, one governed run took ~330 ms: ~195 ms re-verifying the whole snapshot, ~128 ms
drawing the picture through a Graphviz subprocess, ~8 ms executing. The HTTP server, the federation
worker and coordinator, and every validation suite call `run_workflow` in a loop, so each paid both
on every request. Warm boot was always meant as load once, verify once; the package a boot produces
is frozen and nothing reads the snapshot after it. The picture is a view of the evidence, not
evidence.

**Applied.** `protocol_runtime/runtime/api.py`; `test_resident_boot.py` 4/4, in `regression.sh`.
A run now takes ~5 ms after the first in a process. No artifact and no snapshot identity changes, so
no dossier.


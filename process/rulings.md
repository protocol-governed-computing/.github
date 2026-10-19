# Rulings

A ruling decides how something is read or done, once, so it is not argued again each time it comes
up. Each entry gives the rule, the reason, and where it applies. Only a later ruling overturns an
earlier one, and it replaces the entry here.

Each repository's `CLAUDE.md` holds doctrine for that repository and is gitignored, so it is neither
versioned nor backed up. A `CLAUDE.md` may repeat a ruling to keep it in front of whoever works
there, but the ruling stands here.

---

## Transformation

### v6 is built as a baseline, outside the lifecycle, once

**Rule.** The v6 baseline is built directly, not through change requests. Its defects are fixed in
the artifacts and code that carry them, every identity is reset to `_V0`, and each domain's design
of record is generated from the result. After v6 is cut, every change goes through the lifecycle,
judged by the transformation module, and no later change may claim this ruling.

**Conditions:**
- The regression stays green at every step, and nothing red by design remains at the cut.
- Each domain's baseline design determines its whole registry: `construction_acceptance` rebuilds
  every artifact from it.
- The person cutting v6 approves the baseline before it is cut.

**Why.** A change request records an approval against a composition. Every composition before v6 is
discarded at the reset, so a dossier written now would describe identities that are about to stop
existing, and it would be deleted with them. The baseline design is the record v6 starts from.

### A dossier is admitted on what it says, not on how it was written

**Rule.** The phase checks admit a document; they do not see how it was produced. A generated
dossier is permitted, on three conditions:
- The generator is committed with the dossier it wrote, exactly as it ran. Once the dossier is
  delivered, git holds the generator, and the working tree does not.
- The dossier says it was generated.
- A generator is not a design authority. Construction completeness must still be 100%, so anything
  it infers that no register states is caught.

The design-of-record generator, `transformation.record`, stays in the working tree: each root's
design of record is regenerated from its registry, and `write_baseline_designs.py --check` refuses a
design its registry no longer generates.

**Why.** A large design is impractical to type by hand, and every rule admits a generated document
exactly as it would admit the same text typed. Governing generation itself is open work.

### A change request pins the composition without its own output

**Rule.** A change request's baseline is the composition the change is designed against. It never
holds what the change emits. For a domain's first change, that means a composition without the
domain.

```
PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 \
PGC_SOURCE_ROOTS=<every */snapshot/compiled root but the change's domain, ':'-separated> \
PGC_SNAPSHOT_OUT=<scratch dir> ./snapshot_assembler/assemble.sh
tc baseline show --snapshot <scratch dir> > <dossier>/baseline.json
```

Run the phase checks with `--snapshot <scratch dir>`. The side assembly's identity equals the pin
exactly when nothing outside the change has moved, which makes it the test of whether a pin is
current. A dossier re-authored against a composition that holds its own earlier output moves its
rows to `EXTEND`, deliberately.

**Why.** Pinned against a build that contains it, every `NEW` row reads as `*_ALREADY_EXISTS`, and
P7 and P8 are refused.

### Validation criteria come from P0

**Rule.** A domain's execution-validation criteria are drawn from the seed's acceptance criteria
and `operation_refusals`, in the seed's own words, while P7 is written. When a criterion fails,
first ask whether it misread P0, and only then treat the failure as a defect. Dispatch one workflow
as soon as artifacts are emitted.

**Why.** A criterion written after the build drifts toward what the system does, and some defects
pass every phase check and appear only on the first dispatch.

### A contract redeclared whole requires only what it declares

**Rule.** `NODE_INPUT_UNBOUND` reads a contract's required inputs from the design where the design
composes that contract's steps. The pinned contract's inputs are joined only for a contract the
design calls without composing.

**Why.** A design that redeclares a contract authors its interface again. An input it withdraws is
no longer required, and joining the pinned inputs would force the design to hand the contract a
value none of its steps read.

### An amendment declares what it withdraws

**Rule.** P7's `withdrawn_facts` names an artifact the design extends, a place in its Machine block,
and the reason the fact goes. Construction subtracts declared withdrawals from what an amendment
loses. A fact omitted without one is refused, a withdrawal covering nothing lost is refused as
unfounded, and `WITHDRAWAL_NOT_AN_AMENDMENT` holds a withdrawal to an `EXTEND`. A value refined
into a list or an object counts as refined, not narrowed.

**Why.** An `EXTEND` is rendered whole, so an omission and a decision look the same in the rendered
artifact. Stating the decision keeps the narrowing guard meaningful.

### An entrance supplies what its gate requires

**Rule.** `ENTRANCE_UNDERSUPPLIES_GATE` refuses an entrance whose payload omits a field the gate of
its workflow requires. The gate is read from the design where the design states it, and from the
composition otherwise, through `si.capability.surface`'s `intents`.

**Why.** Otherwise every phase can admit a design whose entrance is refused at admission on every
request.

### An amendment is built as it was measured

**Rule.** A change that only amends still gets a domain build manifest, and it describes the whole
domain, naming every subdomain the domain holds. `construction emit` carries forward the
descriptions of the document it replaces, exactly as `construction check` does when it measures
the amendment.

**Why.** What is emitted must be what was measured. A manifest describing only the change would
misdescribe the domain and fail to compile its cases.

---

## Runtime

### Deployment configuration is not branching

**Rule.** The sealed snapshot decides behaviour: whether execution is federated, and how a unit is
admitted, executed and evidenced. Only these may come from the environment or the command line:
where a coordinator listens, the address a node reaches it at, and how long a node waits to
connect. The runtime's only defaults are in `protocol_runtime/runtime/federation/defaults.py`:
bind (loopback, as a safety property), port, connect timeout and poll interval. A new default goes
there or nowhere. Anything that changes what a run determines belongs in the snapshot.

**Why.** Those are facts about a deployment. A snapshot is sealed once and runs on many
deployments, so it cannot know them.

### An unknown admission after a dropped connection is a stated limit

**Rule.** If a connection drops after a unit is sent and before the coordinator answers, admission
is unknown, and the error says so.

**Why.** Resolving it needs a unit idempotency key and an admission-status query, so a retry can ask
whether the unit was admitted. That is open design work, and it needs federated testing.

### A process verifies once; a run writes evidence, not pictures

**Rule.** `runtime.api` keeps a booted snapshot resident per process, keyed by the manifest file and
by what acceptance was judged against (trust anchor, profile root). A rewritten manifest is verified
afresh, and `boot()` itself is never cached. A run writes its `.jsonl` evidence only; a picture of
its path is drawn on request (`run --behavior-logic`, `behavior-logic <trace>`).

**Why.** Warm boot means load once and verify once: the booted package is frozen, and nothing reads
the snapshot after it. A picture is a view of the evidence, not evidence, and drawing one on every
run costs more than the run.

---

## Placement

### FEDERATED_NODE requires a store honouring POSIX record locks

**Rule.** The `FEDERATED_NODE` placement declares this as a requirement on the store its workers
share.

**Why.** Capability correctness across workers depends on record locks. NFSv4 and local filesystems
honour them; an object store does not. A constraint held only in code is invisible to anyone
reading the profile.

---

## Governance surface

### Each transform is governed by the constitution of its kind

**Rule.** A transform is governed by exactly one of three constitutions: deterministic atoms,
non-deterministic atoms, or molecules. The rules common to every transform (surface closure, derived
closure, implementation admissibility) are stated in each, and each constitution says so.

**Why.** A constitution's name says what it governs, and no constitution claims a kind it does not
govern.

### A profile's content is in the identity

**Rule.** The snapshot identity covers the content of the profile a snapshot claims, not only its
name. Profiles live in `.github/snapshot_profiles/` and are read through `PGC_SNAPSHOT_PROFILES`.

**Why.** Otherwise a profile could be weakened without changing the identity of any snapshot that
claims it.

### A validator reports; the contract refuses

**Rule.** `CT_PURE_VALIDATE_RECORD_STRUCTURE_V0` returns the violations it finds and decides nothing.
Each contract that validates a record refuses on what it finds, with a following rule step that
requires `violations == []`.

**Why.** Whether a violation refuses is the business's rule, so it belongs in the business's
contract, and a validator that decided would leave no way to validate without deciding.

### A business rule is fixed by the business, never supplied by the caller

**Rule.** A value only the business may decide — an admitted state, an admitted outcome, a limit —
is a literal in the workflow or contract that applies it. It is never read from the payload, and an
entrance does not pass it.

**Why.** A business rule the caller supplies is one the caller can widen, by invoking the workflow
directly.

### A transform's refusal is what it declares

**Rule.** A transform declared `refusal: raises` refuses, and its vectors prove the refusal. A
vector never expects a negative answer from a transform that is declared to refuse.

**Why.** The declaration is the authority. A vector that disagrees with it is the defect.

---

## Domains

### causal_language_model is a regression domain

**Rule.** causal_language_model is in the composition as a regression domain. Its business functions
are not extended. If it changes, the change is a real model as a second realization of its declared
step.

**Why.** It is the only domain that exercises molecules, recorded non-deterministic steps and
replay, refusal moments, and one contract at several places. More business functions would mostly
repeat what it already proves.

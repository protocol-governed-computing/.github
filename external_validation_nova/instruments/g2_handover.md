# G2 — handing the realization to a worker

**Operator-only.** The worker receives the archive built in §2 and the covering note in §3, and
nothing else from this document. It is governed by `g1_realization_protocol.md`.

## 1. Who may do this

Two boundaries, and no others:

- **The author of `NPP-E` must not build the system.** `6a` §6 — externality is a property of
  authorship, and a system claiming a profile it wrote is the collapse the standard forbids.
- **The builder must not have had access to G0's findings** or to any excluded material. G0's
  registers map the terrain this gate surveys; a builder told in advance where the standard's edges
  are will route around them rather than discover them.

**The same worker may go on to perform G4.** No fresh-worker requirement stands between the gates —
G4 transforms the system G2 built, and a worker who has never seen it tests nothing G4 is about.

**G3 is not a worker task.** It is a commissioning-side comparative evaluation.

## 2. The archive

```sh
SANDBOX=~/g2-nova
REV=$(git -C standards rev-parse HEAD)

mkdir -p "$SANDBOX"
git -C standards archive "$REV" spec | tar -x -C "$SANDBOX"
cp external_validation_nova/runs/g0_run_NPP-E/NPP-E.md        "$SANDBOX/"
cp external_validation_nova/runs/g0_run_NPP-E/NPP-E-scope.md  "$SANDBOX/"
cp external_validation_nova/instruments/task_build_a_realization.md "$SANDBOX/"
echo "$REV" > "$SANDBOX/REVISION"

find "$SANDBOX" -type f | wc -l          # 36 — 32 spec documents and 4 others
grep -rlE 'NPP-C|NPP-D|protocol_compiler|snapshot_assembler|protocol_runtime|software_governance|PNP' "$SANDBOX"

tar -czf g2-nova.tar.gz -C ~ g2-nova
```

The `grep` must print nothing. **Confirm `spec/` matches the revision `NPP-E` was authored
against** — if the standard has moved under the profile, the worker builds against two revisions.

**What must not enter.** G0's decision ledgers, findings registers, evaluations and dispositions;
`g1_realization_protocol.md`; the programme plan; any earlier profile; anything from the reference
realization. `NPP-E` and its scope register are the only G0 outputs the worker receives, and it
receives them because the profile is what the system claims.

**One thing the commission itself discloses**, left in deliberately: it names this as a gate of a
programme and cites a governing document the worker is not given. The profile's identity implies
predecessors anyway, and no finding or reference material is exposed by it.

## 3. Isolate first, then hand over

**The worker is offline before it reads a line.** It must read the standard and the profile to write
a sensible manifest — it cannot say what it needs to build with until it knows what it is building —
and that reading period is the longest stretch of the run and the one where curiosity is most likely
to reach for a search box.

An earlier draft of this packet staged dependencies *between* reading and building, which put the
whole reading period outside the firewall. It does not. Nothing in reading or in writing a manifest
needs a network.

```
isolate  →  worker reads  →  manifest handed back  →  stage into the running environment  →  build
```

Put the archive in the environment, cut the network, then send the note.

## 4. The covering note

Send this with the archive. Nothing else.

> You are asked to build a working system that claims the profile `NPP-E` and discharges at least
> one of the claims that profile supports.
>
> The full commission is `task_build_a_realization.md` in the attached archive. **Read it first.**
> It states what to produce, what you may not consult, how to record where every decision came
> from, and what counts as success. `REVISION` names the revision you are working against; cite it.
>
> Read `NPP-E-scope.md` **before** `NPP-E.md`. It records which of the profile's constraints came
> from the party that commissioned it rather than from the standard. Without it you will read a
> commissioning constraint as a family requirement.
>
> **You are already offline, and will stay offline.** Read the standard and the profile first — you
> cannot say what you need to build with until you know what you are building.
>
> **Then, before you write any code, produce `staging_manifest.md`** — the languages, runtimes,
> libraries and tools you want, each with a one-line reason. Nothing in the standard constrains the
> stack; the choice is yours. Hand me that file and pause. I will stage exactly what you asked for
> into the environment you are in, and the manifest then closes.
>
> Two constraints beyond what the commission says:
>
> - **Work only from the archive.** Do not search for the standard, its subject, or any existing
>   implementation of it — not in a search engine, a code host, or a package index. If you encounter
>   one, stop and record that you did. The prohibition is on the input, not on how it reached you.
> - **Do not ask me to decide anything.** Questions about what the standard or the profile requires
>   go in your registers, not to me. I will answer logistics only. A question you had to answer
>   yourself is the result this exercise is collecting.

## 5. Staging

Stage exactly what the manifest asked for **into the environment the worker is already in**, record
what was staged, and tell it to proceed.

**The manifest is then closed.** A later request is granted only if it must be, and **recorded as a
break in the isolation, with the reason and the moment.** Do not treat granting one as routine: the
record of when isolation held is part of what makes the result readable.

**If the environment cannot be isolated** — an external party's machine is not yours to control —
the firewall becomes attested rather than enforced. That is a defensible choice and must be
**recorded with the result**, as G0's honour-based runs were. It matters more here than it did at
G0: a builder searches for ordinary engineering answers all day.

## 6. While the run is open

- **Answer logistics only** — where a file is, how to request a dependency. Nothing about what the
  standard or the profile requires, and nothing that resolves a decision either delegates.
- **Assume anything you write will be quoted back with a document number attached.** In an earlier
  trial a sentence from a reply appeared in the deliverable attributed to a section of the standard.
- **Do not repair the standard or the profile underneath the run.** Both are pinned. A defect the
  worker finds in `NPP-E` is recorded, not fixed — repairing it mid-run would leave the system
  claiming something no longer identified by that name.

## 7. What comes back, and how to read it

The system, `staging_manifest.md`, `determinations.md`, `unresolved.md`, `fixed_scope.md`, and
`conformance_evidence.md`.

Classify every entry yourself, per `g1_realization_protocol.md` §7. The worker records provenance —
a source basis and a claim type — and no interpretive label; assigning classes is the
commissioning side's job, done after the run.

**Read for the entries with source basis *none* and claim type *chosen by author*.** That is where
class 6 lives — the worker could not proceed without reconstructing something knowable only from an
existing realization. It is never named to the worker, because naming it says a realization exists.

**Audit the entries you are about to record as *not* findings hardest.** A builder resolves a
genuine omission from engineering instinct and reports it as something the standard left open,
because the system works and the answer felt obvious. For each, read the cited text and check it
delegates or frees what is claimed.

**G0 produced no class 6 at all.** Authoring a profile does not press on the standard the way
building does. Either outcome here is informative; several would be the most valuable findings the
programme can generate.

## 8. Closing G2

G2 cannot close without: the realization; its three registers; the conformance evidence; the staging
manifest with a record of what was staged and whether isolation was ever broken; your classification
of every entry; and a **disposition** for each classified 3–6.

Only then are the defects repaired in `draft-4`, the revision frozen and tagged, and G3 permitted to
name it.

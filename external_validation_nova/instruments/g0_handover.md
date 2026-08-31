# G0 — handing the trial to an external worker

**Operator-only.** The worker receives the archive described in §2 and the covering note in §3, and
nothing else from this document.

## 1. What changes when the worker is external

The regime settled in `external_validation_nova/NOVA.md` assumed a locally run agent whose tools could be restricted. An
external party's tooling is outside your control, so **G0's firewall becomes honour-based.** That is
a trade, not a downgrade:

| | Local agent | External worker |
|---|---|---|
| **input control** | near-airtight — no execution, no web tools, no subagents | honour-based; the covering note is the only instrument |
| **externality (`6a` §6)** | weak — commissioned and run by the same party | **strong** — authorship genuinely sits elsewhere |

`6a` §6 is about authorship: *"what matters is that changing it is not within the authority of the
system that claims it."* An external author satisfies that in substance, not only in form. Take the
trade, and **record which regime was in force with the result** — a finding read as though inputs
were sealed, when they were not, is worse than one read honestly.

## 2. The archive

One self-contained archive. The worker never sees a repository, an organization, or a URL.

```sh
SANDBOX=~/g0-run
REV=e736800df3388dfb4ed403a494089e1320064017

mkdir -p "$SANDBOX"
git -C standards archive "$REV" spec | tar -x -C "$SANDBOX"
cp external_validation_nova/instruments/task_author_a_profile.md "$SANDBOX/"
echo "$REV" > "$SANDBOX/REVISION"

find "$SANDBOX" -type f | wc -l    # 34 — REVISION, the task, 32 documents
grep -rlE 'protocol_compiler|snapshot_assembler|protocol_runtime|software_governance|PNP' "$SANDBOX"

tar -czf g0-run.tar.gz -C ~ g0-run
```

The `grep` must print nothing. The count is the cheaper check: anything that raises it arrived by a
route nobody intended.

## 3. The covering note

Send this and no more. It names no project, no organization, and no prior run.

> You are asked to author one document: a Normative Platform Profile conforming to Part VI of the
> standard in the attached archive.
>
> The full commission is `task_author_a_profile.md` in the archive. Read it before the standard —
> it states what to produce, what you may not consult, how to classify every decision you make, and
> what counts as success. `REVISION` names the revision you are working against; cite it.
>
> Your profile identity for this run is **`NPP-C`**. Use it exactly.
>
> Two constraints beyond what the commission says, because your environment is your own:
>
> - **Work only from the archive.** Do not search for the standard, its subject, or any existing
>   implementation of it, in a search engine, a code host, or a package index. If you encounter one,
>   stop and record that you did. The prohibition is on the input, not on how it reached you.
> - **Do not ask us to decide anything.** Questions about what the standard requires go in your
>   registers, not to us. We will answer logistics only. A question you had to answer yourself is
>   the result this exercise is collecting.
>
> Return the four deliverables the commission names. A blocked task with a precise account of the
> blockage is a successful outcome; a complete profile with an empty findings register is the
> outcome we would trust least.

## 4. While the run is open

- **Answer logistics only** — where a file is, what the identity is. Nothing about what the standard
  requires, and nothing that resolves a decision the standard delegates.
- **Assume anything you write will be quoted back with a document number attached.** In an earlier
  run a sentence from a reply appeared in the profile attributed to a section of the standard.
- **Do not send a previous run's deliverables, log, or evaluation.**
- **Do not repair the standard underneath the run.** If a repair becomes necessary, stop the run.
  The revision is pinned; a finding against a moving target names nothing.

## 5. What comes back

Four things, per the commission: the profile, the decision ledger, the findings register, and the
list of assumptions not traceable to a permitted input.

Read them against `task_author_a_profile_operator.md` §4 — including its instruction to **audit the
class 1 and 2 entries hardest**, since a capable author files a genuine omission as realization
freedom without noticing.

The gate does not close on receipt. It closes after every class 3–6 finding has a disposition, the
defects are repaired, and the target revision is frozen and tagged.

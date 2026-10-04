# Running the profile-authoring trial — operator notes

**This run is NOVA gate G0.** Its output is not a document review: it is the profile every later
gate depends on, and the findings that decide whether the target revision can be frozen.

**Not for the worker.** Everything here would tell an author what is being looked for, which is the
one thing that makes the result worthless. Keep it out of whatever folder the worker can read.

The worker-facing document is `task_author_a_profile.md`, beside this one in `process/`.

## 1. What the trial establishes

Whether a competent reader can decide the family's delegated questions from the standard alone. It
costs a document review rather than an implementation, and it is the cheapest evidence of independent
usability the family can obtain.

It does **not** establish that the resulting profile is external to anything that later claims it
(`6a` §6) — that is a question about authority, decided separately.

**As G0 it also carries the programme's gate obligations.** It cannot close without the profile,
its three registers, your classification of every entry in them, and a **disposition** for each you
classify 3–6. G1 may then name the pinned candidate revision; the freeze comes later, after G2.

## 2. Setting up a run

The sandbox is built when needed and deleted after. Nothing in it is version-controlled, so nothing
in it survives by accident — **which is how trial 1's artifacts were lost.** Capture the outputs
before teardown (§6).

**The sandbox lives outside the workspace tree.** Not under `standards/`, not anywhere below the
workspace root. An agent session inherits the `CLAUDE.md` files above its working directory, and the
workspace root's names every repository, the build lifecycle, and the platform composition — the
whole reference architecture, handed over before the worker reads a single document. A sandbox
inside the tree is contaminated by its own location.

Build it from the **named candidate revision**, not from the working tree:

```sh
SANDBOX=~/g0-run            # outside the workspace; no CLAUDE.md above it
REV=<candidate-revision>    # a tag or commit, never a branch

mkdir -p "$SANDBOX"
git -C standards archive "$REV" spec | tar -x -C "$SANDBOX"
cp external_validation_nova/instruments/task_author_a_profile.md "$SANDBOX/"
git -C standards rev-parse "$REV" > "$SANDBOX/REVISION"
chmod -R a-w "$SANDBOX/spec"       # the family is read, never written
```

`git archive` rather than a worktree: it is read-only, registers nothing in the source repository,
and leaves no second checkout to clean up. It also carries only what the revision tracked under
`spec/`, so an untracked file sitting in the working tree cannot ride along.

Then confirm the sandbox is what it should be, and that nothing around it is not:

```sh
find "$SANDBOX" -type f | wc -l          # 34: REVISION, the task, 32 spec documents
grep -rlE 'protocol_compiler|snapshot_assembler|protocol_runtime|software_governance|PNP' "$SANDBOX"
ls ~/CLAUDE.md                           # must not exist
ls -d ~/.claude                          # must be archived, or the run inherits a memory of this work
```

The second command must print nothing. The count is the cheaper check of the two: anything that
raises it arrived by a route nobody intended.

`$SANDBOX/REVISION` is what the profile and every finding cite. A branch name is not a revision: it
moves, and a finding against a moving target names nothing (`7a` CF-1).

**What must not enter the sandbox.** `spec/*.md` and the task document, and nothing else. In
particular:

| Excluded | Why |
|---|---|
| `.github/snapshot_profiles/` | existing profile candidates — the exact prohibited input |
| `standards/projections/` | the terminology index hands over vocabulary the author must derive |
| `standards/revisions.md` | findings and dispositions from prior work, including this trial's own |
| `standards/doc/realization_map.md` | evidence about the reference realization |
| any `CLAUDE.md`, agent memory, or paper | implementation context by another route |

A whole-directory copy leaks every one of these. Copy the files named above, individually.

A run does not outlive a spec edit. If the standard is repaired, the candidate revision has changed:
tear the sandbox down and rebuild it from the new commit rather than refreshing in place.

**The lock is not paranoia.** In the first run the worker patched its own copy of the standard in
response to a review — including inserting a section and renumbering everything after it, which
breaks every cross-reference in the family. A worker reading a copy it has amended is being tested
against its own text.

## 3. Rules for the operator

- **Give the worker a fresh profile identity each run.** Never one a previous run used (`6a` §9).
- **Give the worker the candidate revision, and do not move it mid-run.** If a repair to the
  standard becomes necessary during the run, stop the run rather than amending underneath it.
- **Answer logistics only** — where the documents are, what identity to use. Nothing about what the
  standard requires, and nothing that resolves a delegated decision.
- **Whatever you do say is not the standard, and will be cited as though it were.** In the first run
  a sentence from a reply to the worker's pre-questions appeared in the profile attributed to `6a`
  §7. Assume anything you write will be quoted back with a document number attached.
- **Do not show the worker a previous run's deliverables, log, or evaluation.**
- **Use a worker that has not performed a previous run, in a context that holds none of one.** The
  rule above covers what you hand over; it does not cover what the worker already remembers. Runs
  `NPP-C` and `NPP-D` were performed by one worker in one context, and the second reproduced the
  first's answers and carried a phrase from the first's commission into its own findings. A worker
  restating itself establishes nothing about what the standard leads a reader to, and a distinction
  it was given in an earlier run is not one it derived in this one.
- **Run the worker without `Bash`, without web tools, and without subagents.** The reference
  realization is discoverable by name from the standard alone, and the prohibitions in the task
  cover what is offered to a worker rather than what it goes looking for. This task is reading
  `spec/` and writing documents; nothing in it needs a network-capable tool, so the surface is
  removed rather than policed. Confirm the restriction is in force **before** handing over the
  sandbox, and record that it was.
- **A blocked run with a precise account of the blockage is a successful outcome.** Do not unblock it.

## 4. Reading the result

Two documents come back: the profile and the questions log. **The log is the instrument** — the
profile is the occasion for producing it.

**You classify; the worker does not.** The worker returns three registers — determinations, matters
left unresolved, and scope this commission fixed — each entry carrying a source basis, a claim type,
reasoning and a confidence. That is provenance, not interpretation. Assigning classes is your job,
done after the run.

Read claim type against source basis first. *Expressly required* with a citation that does not
require it, or *inferred* where the text is plain, are the entries that move classes.

This is deliberate. Finding **A** records that `6a` gives an author no way to tell a deliberate
silence from an omission. A commission that hands over that distinction answers the finding in
advance: the log then shows that the *commission* works, and says nothing about whether `6a` does.
**Nothing is prompted for, not even class 6.** Asking a worker to mark what it *"could not decide
without knowing how an existing system does it"* tells the worker such a system exists. The provenance
record reaches the same place without saying so: an entry whose source basis is *none* and whose claim
type is *chosen by author* is a class 6 candidate, and you decide whether it is one.

| Class | The entry shows | Finding? |
|---|---|---|
| **0 — commissioner scope** | the commission's §2 fixed it, not the family | **No**, and not evidence either way about the family |
| **1 — realization freedom** | the standard deliberately leaves it open | **No.** Check the cited text actually leaves it open |
| **2 — profile decision, specified** | the family delegated it and supplied enough to decide | **No.** That is the task working |
| **3 — profile decision, underspecified** | the family delegated without supplying enough | **Yes.** Usually a `6a` §7 gap |
| **4 — ambiguity** | two readings, incompatible results | **Yes.** Check both readings are actually named |
| **5 — omission** | no normative source at all | **Yes.** The strongest ordinary finding |
| **6 — reference-shaped assumption** | could not proceed without reconstructing something knowable only from a realization | **Yes — the result this trial exists to produce** |

**Class 0 exists because run `NPP-C` did not have it.** Seven of that run's twelve class 2 entries
cited the commission as their authority — identity, scope, one tenant, no replication, no external
boundary. Those are the commission's decisions, recorded as though the family had delegated them
well. Without a class of their own they inflate the evidence that the standard is independently
usable, and the commission ends up measuring itself.

**Audit the class 0, 1 and 2 entries hardest** — the ones you are about to record as *not* findings.
A capable author resolves a genuine omission from engineering instinct and reports it as something
the standard left open, because the answer felt obvious. For each, read the cited text and check it
delegates or frees what is claimed. An entry whose only authority is the commission is class 0, not
class 2, however the worker framed it.

**Two failure modes in reading the log:**

- A log that walks `6a` §7 row by row and contains nothing else has recorded the questions the task
  named, not the questions the author had. Look for what is missing: terms the author needed and did
  not find, boundaries the family did not draw, periods it did not bound.
- A worker that accepts every finding in an evaluation without contesting any has done the same thing
  a profile written by consulting a realization does — deferred to the commissioning party. Some
  findings are wrong. Say so if none are contested.

## 5. What the current run is testing

Carried from trial 2 — whether `draft-3` Changes 4–7 do what they were written to do:

| Change | Passes if the new profile |
|---|---|
| **4** — NP-12, a decision must be the profile's own | decides artifact kinds, outcomes, and namespaces with actual content, rather than requiring the system to declare them |
| **5** — `caller` glossed in `5b` | needs no invented term for who reads; uses `caller`, or logs a finding if it still does not fit |
| **6** — instance bounded by the snapshot it accepted (`7a` §3.1) | anchors any retention decision to a period with a stated end |
| **7** — the two-systems test, §5 obligations, §3.1 floor | decides read attribution; declares no obligation that restates a selection; treats its subject-class list as a floor |

A pass on all four is weak positive evidence — one author, one scope. A failure on any is strong
negative evidence and reopens that change.

New for G0, three open findings this run is the instrument for:

| Finding | Passes if |
|---|---|
| **A** — `6a` gives an author the list of what to decide and no way to distinguish a deliberate silence from an omission | the log distinguishes them, without the task document having told the author how |
| **B** — `7b` specifies demonstrations but may not let one be constructed for a subject class | the author reaches the boundary and **records it rather than inventing an oracle** (worker §7) |
| **F** — whether the domain-neutral semantic spaces a runtime recognizes are canonical or artifacts of one realization | a kind vocabulary is closed from the family alone |

**Finding F is the one to handle carefully.** Compare the author's closed vocabulary against the
reference realization's set **only after the run is complete and the log is read**. Convergence is
evidence the spaces are canonical; divergence is evidence they were one realization's artifacts.
Either way the comparison is worthless if it happens first, and **nothing about that set — including
how many there are — may reach the worker at any point.**

**`draft-3` Change 8 (`4d`) is not under test here.** A profile author reaches transformation only by
claiming a transformation item; validating it needs a different exercise.

## 6. Capturing the run, and closing the gate

Trial 1's deliverables no longer exist because the sandbox was untracked and deleted. Before
teardown:

1. Copy the profile and its three registers out of the sandbox.
2. Commit the profile as an independent artifact, carrying its identity (`6a` §9) and the revision
   from `$SANDBOX/REVISION`. **Not into `spec/`** — a profile is not a document of the family.
3. Classify every entry, then record each 3–6 against the target revision in `revisions.md`, with a
   disposition: a normative defect to repair, or a matter that occasions no repair, with the reason.
4. Repair the defects, and repeat whatever G0 work they invalidate.

**G0 closes at step 4, not at step 1.** A profile in hand with findings undisposed is an open gate,
and starting G1 against it is how a finding becomes a design decision nobody declared. **The freeze
is not part of closing G0** — the candidate revision stays open through G2, so that what a
realization finds can still be repaired in it.

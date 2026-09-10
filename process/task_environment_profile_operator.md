# Running the environment-profile trial — operator notes

**Not for the worker.** Everything here would tell an author what is being looked for, which is the
one thing that makes the result worthless. Keep it out of whatever folder the worker can read.

The worker-facing document is `task_environment_profile.md`, beside this one in `process/`.

## 1. How this differs from the platform-profile trial

Same instrument, different subject. `task_author_a_profile.md` tests `6a`; this tests `6b`. Do not
run them against one worker, and do not show either author the other's output — `6a` §7's deferral
list would tell a `6b` author what a profile is expected to decide, which is one of the things this
trial is measuring.

**The material difference is that `6b` has no deferral list.** `6a` §7 hands a profile author a
fourteen-row table of what to decide. `6b` §9 gives four bullets of what to declare and no equivalent
enumeration. An author must work out what an environment profile decides largely from the document's
prose.

That makes this trial the direct test of the finding carried into `draft-4` as **A** — whether `6a`
should tell a profile author what to notice is missing. Do not fix A before running this. If `6b`
produces a rich log without a list, the under-reporting seen in the `6a` trials is a property of that
list, not of the family. If `6b` produces a thin log too, A is general and worth a normative section.

## 2. Setting up a run

The sandbox is built when needed and deleted after. Nothing in it is version-controlled.

```sh
cd standards
mkdir -p sandbox/spec
cp spec/*.md sandbox/spec/
cp ../.github/process/task_environment_profile.md sandbox/
chmod -R a-w sandbox/spec          # the family is read, never written
```

To refresh after a spec edit: `chmod -R u+w sandbox/spec`, re-copy, re-lock, and `diff -rq spec
sandbox/spec` to confirm.

**The lock is not paranoia.** In the first platform-profile run the worker patched its own copy of
the standard in response to a review, including inserting a section and renumbering everything after
it. A worker reading a copy it has amended is being tested against its own text.

## 3. Rules for the operator

Unchanged from the platform trial, and they matter more here because the environment scope invites
questions:

- **Give the worker a fresh profile identity each run.** Never one a previous run used (`6a` §9).
- **Answer logistics only.** Nothing about what the standard requires, and nothing that resolves a
  delegated decision.
- **Whatever you do say is not the standard, and will be cited as though it were.** In the first
  platform run a sentence from a reply to the worker's pre-questions appeared in the profile
  attributed to `6a` §7. Assume anything you write comes back with a document number attached.
- **Expect to be asked whether the environment "really" has to tolerate partitions, or whether the
  clock assumption can be relaxed.** It cannot, and saying so is a decision the author must reach
  from `6b` §4 rather than from you. Point at the task and stop.
- **Do not show the worker a previous run's deliverables, log, or evaluation.**
- **A blocked run with a precise account of the blockage is a successful outcome.** Do not unblock
  it.

## 4. Why the scope is what it is

The environment in §2 of the worker task is deliberately hostile, and each property is there to
create a specific pressure. **Do not describe any of this to the author.**

| Property of the scope | What it puts pressure on |
|---|---|
| partitions are expected, not exceptional | EE-7 — whether inability to determine produces refusal, or whether the author invents a degraded mode |
| no synchronized clock, no skew bound | whether a timing constraint becomes a governed input by the back door (EE-4) |
| no instant when all nodes hold the same snapshot | `7a` §3.1 — whether an instance is bounded by the snapshot it accepted, and what that means when acceptance is not simultaneous |
| attestation device on some nodes and not others | **EE-5** — the most likely single failure: requiring the substrate provide it, then letting behavior depend on it. Requiring presence is a precondition; only the *system* may declare a governed input |
| deadlines with operational consequences | `6b` §4's exemption pressure, and `3c` §12 — whether performance is traded against an invariant |
| one tenant, many replicas | EE-8, and GC-12/SN-3 on copies of one identity that differ |

## 5. What to watch for in the result

**The exemption is the headline test.** `6b` §4: *"An environment profile is the natural place to ask
for an exception — the substrate is awkward, the guarantee is expensive, the alternative is not
shipping. A profile cannot grant it (NP-4), and the honest outcome is that some systems do not run in
some environments."* A profile that finds a way to keep everything running has almost certainly
relaxed something. **A profile whose exclusions section is substantial is the expected shape of a
correct answer**, and one with a thin exclusions section deserves reading twice.

**Then, in descending order of what they would settle:**

- **EE-5, presence into authority.** Does any obligation on the environment become something a
  determination depends on? The attestation device is the bait.
- **Discharge by substitution.** `6b` §12 establishes conformance by executing the same snapshot in a
  *second* conforming environment. Does the profile bound its environment so tightly that no second
  one could exist? That supports a claim nobody can discharge (`6a` §7).
- **NP-12.** Does the profile decide its constraints, or require the system to declare them? A
  constraint stated as "whatever availability the system requires" has decided nothing.
- **Ordering.** `6b` §8.2 says distribution reveals under-specified ordering rather than introducing
  it. Does the author reach for an environment constraint to hide the ambiguity, or note that the
  remedy is in the declarations?
- **Did the author know `6a` applied?** `6b` §1 says so in one sentence. If the profile satisfies
  EE-1 … EE-8 and never mentions NP-*, that one sentence is not carrying what it needs to — and that
  is a finding against `6b`, not against the author.

## 6. Reading the log

As in the platform trial: classify each entry as an implementation choice, a profile choice, or a
missing semantic decision. Only the third is a finding against the family.

**Two failure modes in reading it:**

- A worker that accepts every finding in an evaluation without contesting any has deferred to the
  commissioning party, which is the same defect as consulting a realization. Some findings are wrong.
  Say so if none are contested.
- A thin log is not evidence of a complete standard. Both `6a` authors produced profiles that would
  survive review and logs that under-reported; six of `draft-3`'s changes came from silences the
  second author decided over without recognising them. **What finds those is reading the profile
  against the documents, not reading the log.**

## 7. Afterwards

- Findings become candidate changes in `draft-4`, declared against `draft-3` as predecessor
  (`doc/revisions.md`).
- A finding declined is recorded with the reason.
- Resolve finding **A** only after this run, and using it. That is the whole reason for the ordering
  in §1.
- `6c` is the remaining untested document. Its trial is a third task, not this one with the nouns
  changed — a domain profile's pressures are not an environment profile's.

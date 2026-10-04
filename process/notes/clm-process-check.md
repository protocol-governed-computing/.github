process check — what causal_language_model taught, and what becomes of it

`causal_language_model` CR-1, `model_response`, went through P0–P8, was emitted and implemented, and
holds 27/27 criteria by running. It lives on `work/clm`. Every platform fix it needed went to
`dev/17` first, with a test, and was merged across. This note records what the exercise was, what it
cost, what it taught about the process, and what happens to it next. It is written before any merge,
on purpose.

## What the exercise was

It was a stress test more than a business domain. CLM is the first domain to put these into one
composition:

- a step not determined by its inputs;
- molecules;
- one contract run at several places in a workflow;
- endings that refuse and still announce.

Each of those met a gap in the design language or the platform, seven in all, and each was fixed:

| Gap | Where it was fixed |
|---|---|
| A node was named by the contract it runs, so a contract could run at only one place | P7 §5 `Runs` column; key-uniqueness and route-resolution rules |
| Acyclicity was checked over contracts, so two places in sequence read as a cycle | compiler S4, per node key |
| Routing, endings and announcements were indexed by contract; the last place sealed stood for all | compiler dispatch and runtime scheduler, keyed by node |
| A refusing ending could not announce | P7 refusal moments |
| A molecule's atoms were refused as unreached | `INVARIANT_CT_SURFACE_DERIVED_CLOSED_V1` |
| The executor dropped an atom argument named like a step key | runtime `ct_executor` |
| Conformance crashed on a missing implementation | runtime conformance runner |

What it proves is the useful part. **Governance can sit around a step nobody governs.** The model
offers words, and the rules decide each word that is written. Every offer is recorded, and a replay
reproduces the response without consulting the model. The test model tries to break the rules on
every word. A response equal to the supporting material, with another customer's account number
offered on every word and written on none, is evidence of who decided.

## The sobering finding

**Every phase passed while execution was wrong.**
- P2–P8 were admissible and construction completeness was 100%.
- Yet the submission ended every record node where the last one did, announced nothing, and would
  have recorded a rule stop as the longest response being reached.
- `ai_governance` carried the same collision in two workflows (`WF_GOVERN_AGENT_ACTION_V0`,
  `WF_PROVISION_AI_LICENSING_V0`), undetected, for as long as those workflows have existed.

Running the workflows found it, and nothing else did. That is the same lesson `blockchain` cr_04
taught: the pipeline traces artifacts, not behaviour. **A design that determines its artifacts is not
yet a design that does what was asked**, and only execution tells the two apart.

## Lessons for the process

**1. Run something the moment artifacts exist.**
- A single happy-path dispatch right after emit would have surfaced the routing defect days before
  the validation suite did.
- The compiler should also refuse the defect class outright. The assertion would be: every keyed
  node that declares a continuation has its own routing entry in the sealed dispatch, and no two
  nodes share one.

**2. Write the validation criteria at design time, from P0.**
- The suite's criteria were written after the build, from the seed's acceptance criteria. One was
  wrong: it expected a stopped response to keep its partial words, and the seed says the model
  "gives no response".
- The system was right and the check was not. Criteria derived at P7 or P8, and checked against P0
  like everything else in the dossier, would not drift that way.

**3. P7 is beyond hand authoring, and that raises an authority question.**
- CLM's P7 has 47 topology rows and 280 bindings. A generator script wrote it from P5 and P6, and P8
  likewise. Both scripts are kept, as they ran, in `clm-generators/` next to this note.
- The phase checks admit the document, not the way it was produced. So the design's author is, in
  fact, a script outside governance.
- Either generation from P5/P6 becomes a governed step with its own evidence, or the design language
  must become small enough to write by hand. Leaving it implicit is a second, ungoverned design
  authority, which is what construction completeness exists to prevent.

**4. Pinning a change's baseline is tribal knowledge.**
- A change request's baseline must be the composition *without* its own domain. Pinned against a
  build that already holds it, every NEW row reads as `*_ALREADY_EXISTS`.
- CLM's pin was taken by stashing, switching branches, building, pinning and switching back.
- That was unnecessary. `assemble.sh` already builds a deliberately narrower composition when
  `PGC_SOURCE_ROOTS` names its roots, and writes it wherever `PGC_SNAPSHOT_OUT` says. A pin without
  the change's own domain is one assembly into a side directory, followed by `tc baseline show` on it.
- What is missing is the rule, not the tool. It belongs in `transformation/CLAUDE.md`.

**5. Isolating an exploratory domain on its own branch works, and costs.**
- Keeping CLM on `work/clm`, with platform fixes on `dev/17`, kept the release line clean. It took
  about eight merge round-trips, and once a platform change was made on the wrong branch.
- It is the right shape for an exploratory domain and the wrong one for routine work.

## What the exercise left open

**Replay agrees on every determinative event but one field.**
- An append-only store gives each record an identity read from the clock, and that identity reaches
  the trace inside `detail`. `VOCAB_EVIDENCE_CONTENT_CLASSIFICATION_V0` declares `detail`
  determinative, while stating it does not claim a caller-filled `detail` is purely so.
- The suite names the one field and fails on any other difference. Separating store-assigned content
  in the classification is a platform decision.

**A rule stop names the rule that stopped the most likely word.** With the test model that is always
the account-number rule. It is correct by the design, and it hides which rule the material's own word
broke.

**Smaller items:**
- `moment: refusal` is checked at P7 but not carried into the event artifact.
- P7 does not check that vector cases parse.
- `tc construction emit --help` is out of date on manifests.
- Two failures in `test_workflow_execution.py` predate this work.

## Disposition

**CLM stays on `work/clm`, frozen at CR-1, until two things are done:**

1. the compile-time routing assertion in lesson 1, so the defect class is refused without needing a
   domain to run into it. This is now done: S8 reads the sealed dispatch against every declared
   transition and refuses the build where they differ;
2. a decision on the replay classification, so the regression does not carry a named exception
   indefinitely.

**After that, merge CLM into `dev/17` as a regression domain.** It is the only domain exercising
molecules, non-deterministic atoms, refusal moments and one contract at several places. Without it,
those paths are covered by unit tests alone, and unit tests did not catch the routing collision.

**CR-2 through CR-6 are parked.** More business functions would mostly repeat what CR-1 proved about
the platform. That is consistent with the standing position of validation over more specification.

**The next CLM step worth taking is a real model, not CR-2.** It would join as a second realization
of the declared step, with genuine non-determinism, capacity in tokens rather than words, and the
optional dependencies that brings. It tests the thesis where the test model only simulates it.

**Before any new domain starts,** lessons 1, 2 and 4 are folded into the transformation process.
Lesson 3 needs its own decision first.

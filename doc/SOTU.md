# SOTU Handoff

## dev/12. **`draft-4` Change 1 declared · NOVA opened and G0 run three times · Findings A and F answered · next: close G0.**

The whole cycle came from one instrument: **a terminology index derived over the family and checked
against `1a` §12** — the first instrument pointed at the family's own vocabulary rather than at a
realization. Twenty-four documents declare the terms they introduce; twelve of those declarations
were untrue.

### Changes made — `standards`, branch `draft/4`, one commit, working tree clean

| Commit | Files | What |
|---|---|---|
| `dae8476` | 27 files, +2061/−37 | **`draft-4` Change 1.** Seven terms gained a definition where their document already declared them; four struck; `step` moved to `1a` §8. **Five refinements declared — the first in the family**, CM-2 having required the mechanism since `draft-1` with nothing exercising it. **CM-8 added** (`1a` §1, §12, §13, §14; `0z` §2 row now `CM-1 … CM-8`). Finding **E** recorded, not carried. New `tools/vocab_index.py`; new `projections/` at root; `revisions.md` moved to root beside `VERSION`. |

**Terms struck rather than defined — 4.** `3c` `execution agent` (`1a` §8 already defines **Runtime**
as "the agent that performs execution"; a second name for one concept is what CM-3 forbids); `4a`
`admissibility determination` (a compound of **Admissibility** `1a` §7 and **determination** `1b`
§4); `6c` `platform-owned governance` and `domain-owned governance` (§3 names the distinction in its
table and never uses either phrase). The `6c` pair was **defined first and struck after** — see
Architectural concerns.

**CM-8 — ownership by semantic primacy.** A term belongs to the document whose subject matter
principally establishes it, never to `1a` by order of appearance. The rule had to be applied four
times in this change and was stated nowhere. It is the one part of Change 1 that adds a requirement
rather than repairing a declaration; it invalidates no existing definition.

**`candidate` was the case that tested it.** Wording could not settle it — `4a` §2 duplicated `1a`
§10 near-verbatim, which is evidence of an accident, not of ownership. Usage breadth settled it:
`candidate` appears in ten documents, and `1b` §4 defines **proposal** as "a candidate change
presented to a governed state". A Part I document using the term to define one of its own means the
concept is family-wide. Had construction owned it, `1b` would rest on a Part IV term — the same
defect this change repaired for `step`.

### Changes made — `.github`, uncommitted

| File | What |
|---|---|
| `doc/NOVA.md` | **new.** The NOVA programme: a second PGC realization built from the standard alone by a cold worker, to test specification sufficiency and governed self-evolution at once. Five gates — **G0** profile authoring, **G1** experiment protocol, **G2** the realization, **G3** comparative conformance, **G4** governed transformation — and no gate starts until the prior one has *both* its artifact and its findings. Six finding classes, with **class 6, reference-shaped assumption**, as the result the programme exists to produce. |
| `process/task_author_a_profile.md` | revised for **G0**. Frozen candidate revision; existing profile candidates prohibited *including their shape and field names*; any concern or prefix taxonomy from a realization prohibited *including how many there are*; three finding classes become six; a sixth deliverable — close the kind vocabulary from the family alone; new sections on not inventing a conformance oracle, and on success and failure. |
| `process/task_author_a_profile_operator.md` | brought into line. Sandbox now built from a named revision via `git worktree`, with an exclusion table — `projections/` and `revisions.md` moved to the `standards` root this session and a whole-directory copy would leak both. New closing procedure: capture outputs, disposition findings, *then* freeze. **Fixed a broken path** — the setup script copied the worker document from `.github/doc/`, where it does not live. |
| `doc/SOTU.md`, `doc/` | nine resolved `draft-3` working files removed; the `draft-2`-era entry trimmed. `parked_rulings.md` kept — deferred, not resolved, and cited three times from `standards/doc/realization_map.md`. |
| `doc/NOVA.md`, `process/task_author_a_profile_operator.md` | **the G1 network regime, settled per gate.** Not one policy: **G0** removes the network-capable surface outright — no `Bash`, no web tools, no subagents, because reading `spec/` and writing documents needs none of them, leaving no residual. **G2** cannot be bound that way, since a worker that executes can reach the network; it needs an offline container, with dependencies staged in advance from a fixed manifest and recorded. **G3/G4** need nothing. The trap named explicitly: G0's guarantee does not cover G2, and G2 is the gate that most needs isolation. |
| `process/task_author_a_profile_operator.md` | **the sandbox moves out of the workspace tree.** It was specified at `standards/sandbox/`; an agent session inherits the `CLAUDE.md` files above its working directory, and the workspace root's names every repository, the build lifecycle and the platform composition. A sandbox inside the tree hands over the whole reference architecture before the worker reads one document — contaminated by its own location. Now `~/g0-run`, with a check that nothing above it carries context and that the worker's agent-configuration directory has been archived. |
| `process/notes/release-11.md` | **new.** *A declaration is not a definition* — the release note for this cycle. Deliberately echoes release 10's *declared ≠ implemented ≠ enforced ≠ demonstrated*: the same shape of finding one level up, an instrument turned on the standard instead of on the realization. Carries the extractor's own failure as a full section, because a note reporting 124 defects without saying 111 were its own blindness reads as self-serving. Documents are named by role, not file identifier, matching release 10's register. |

### Changes made — `snapshot_assembler` and `protocol_runtime`, uncommitted

`SNAPSHOT_ASSEMBLY_CONTRACT.md` moved from `.github/doc/` to `snapshot_assembler/doc/`. Four modules
cite it — `assembler/{__init__,core}.py`, `runtime/{boot,loader}.py` — and an implementation contract
belongs with the component it governs, not in org config. Its header carried two dead references:
`NAMESPACE_MODEL.md`, which exists nowhere in the workspace or in RI-0 and has no successor, and
`spec/01_machine_block.md`, an RI-0 path. **Neither was used by the body** — both words appeared only
in that line — so they were replaced with what actually governs assembly, `3b` and `4b`, rather than
translated. The `Status:`/authoring-note bullet was dropped.

### NOVA G0 — three runs, two instrument repairs

The profile-authoring trial ran three times against byte-identical `spec/`. **Two of the three
failed as experiments, and each failure was the instrument rather than the author.**

| Run | Condition | What it established |
|---|---|---|
| `NPP-C` | commission supplied a six-class taxonomy | nothing about **A** — the taxonomy named the very distinction A says the family lacks. Ledger inflated: 7 of 12 class-2 entries cited the commission as authority |
| `NPP-D` | repaired commission, **same worker, same context** | nothing about **A** — carried the withdrawn phrase *reference-shaped assumption* forward, a term absent from its own commission and present in the previous one |
| `NPP-E` | repaired commission, **fresh session, zero carry-over** | **A answered.** Eleven determinations *expressly permitted by source*, eight *unresolved by family* — the distinction drawn from the text alone |

**Finding A — ANSWERED.** What rules out recall is that `NPP-E` extended the claim-type vocabulary
as `NPP-D` had, but with *different constructions for the same distinction*. Recall reproduces
phrasing; derivation reproduces structure.

**Finding F — SETTLED, and not as expected.** Three closures from one text under one scope: `NPP-C`
and `NPP-D` closed four kinds each and match one another — which is the carry-over, not agreement.
`NPP-E`, the run that could not remember, closed **five** and diverged from both, reaching
**workflow** and **capability contract**. The result is not *four rather than nine*: **the standard
determines no vocabulary at all**, and `2d` §1 says it must not. A set the family deliberately
declines to determine cannot be a canonical axis of its ontology. **Not carried into `2b`.**

**Two repairs to the commission, both held.** Class 0 for commissioner-supplied scope, and the
taxonomy withdrawn from the worker in favour of a provenance record — *source basis*, *claim type* —
with all interpretive labelling done by the evaluator after the run. A third rule was added when the
carry-over was found: **use a worker that has not performed a previous run, in a context that holds
none of one.** The existing prohibition covered what is handed over, not what is remembered.

**The rule that outlives G0:** an experiment may constrain the task, but it must not supply the
distinction whose derivability it is measuring.

### Build & test status — **PASSING**

Run from `standards/`:

```
python tools/vocab_index.py --check     → exit 0
167 terms · 32 documents · 25 defining documents
0 declared without a definition site · 0 defects · 47 warnings
5 declared refinements
```

Two further checks from the projection's own contract, run separately:

- **re-derivation from unchanged `spec/` is byte-identical** (PJ-2, PJ-9);
- **independent term count matches** — 167 counted by a script sharing no code with the extractor.

Workspace checks after the file moves:

```
python .github/process/pgc_env_check.py          → PASSED, exit 0
python .github/process/implementation_closure.py → PASSED, 28 transforms
imports: assembler · assembler.core · runtime.boot · runtime.loader
         protocol_compiler · snapshot_inspector    → 6/6 ok
```

**None of those checks would have caught what actually changed.** All four edits were docstring path
strings, which no import or closure check reads. The real verification was confirming every `*.md`
reference in the contract resolves, and that nothing still points at the old location.

Invariant identifiers across `spec/`: **356**. Note `revisions.md` records `draft-3`'s predecessor
count as 338 and SOTU dev/11 recorded 342; neither was re-derived this session and the three figures
do not agree.

### Open issues

1. **`projections/requirement_projection_contract.md:80` still records `317 requirements · 24
   documents` and still omits `1c`.** Carried unchanged from dev/11. This session built the fix
   pattern but did not apply it: the terminology projection's guard was run as a **separate script
   sharing no code with the extractor**, which is what dev/11 identified as missing — there, the
   independent count was derived the same way as the extractor, so the guard could not fire.
2. **Finding E — nothing says when a word must become a term.** Six are declared, defined, and used
   nowhere: `Promotion` (`1a`), `construction disposition` (`2c`), `projection source` (`4b`),
   `protocol adapter` (`5a`), `profile derivation` (`6a`), `demonstration coverage` (`7b`). Evidence
   in `projections/vocabulary_locality.md`. Not carried — a CM-9 would have to be discharged by every
   document, and the obvious formulation is contradicted by the evidence.
3. **Finding D narrowed, not closed.** First measurement: `4d` owns 11 terms, 4 local, **all 4 cited
   by a `4d` invariant** — it did not invent idle vocabulary. What survives is whether its subject
   requires that much, which is the `8a` §4.7 re-review, still not undertaken. `5a` and `2c` each
   carry 5 local terms and were never the subject of a finding.
4. **The commit message on `dae8476` is malformed.** All 27 files landed in one commit and the
   subject line carries a pasted label plus the whole body on one line. Content is correct;
   `git commit --amend` fixes it if nothing is pushed.
5. Carried unchanged from dev/11: **`7b` has no specification-subject section** (Finding B);
   **`0z` states three MUSTs and carries no invariants** (Finding C); **`4d` TR-2/TR-4 presume
   per-phase register documents**; **`1a` has two sections named *Conformance***, §11 and §14.

### Architectural concerns

- **A definition does not create a use.** `6c`'s pair was reported as declared-and-unused; the triage
  judged that §3 names the distinction and defined them rather than striking them. They were then
  declared, defined, and *still* unused, and were struck. Writing a definition is the tempting remedy
  for an unused declaration and it is the wrong one. Recorded inside Finding E.
- **CM-8 cannot be checked by tooling and the contract says so.** Whether a term sits with the
  document whose subject matter establishes it is a semantic determination — settling it for
  `candidate` meant reading `1b` §4. The projection reports where terms are defined; it does not
  judge whether that is where they belong.
- **The instrument was wrong before the documents were.** First pass reported 124 defects, of which
  **111 were its own blindness** to conventions the family had used all along. The contract now
  states the four source conventions the derivation depends on, because that is the characteristic
  failure of a derived index.
- **`projections/` mixes generated and hand-authored files.** Two are generated
  (`terminology_index.md`, `vocabulary_violations.md`); five are written — the README, both PJ-3
  contracts, and the two readings. A contract cannot be generated by the tool it governs. Documented
  in `projections/README.md` after this caused a false alarm.
- **`spec/` was held clean.** Projections stay out of it: a file identifier confers family membership
  (`0z` §2), and a regenerated file inside a family built on declared supersession contradicts
  `4e` §9. `doc/` was reduced to what has no more specific home.

### Release posture

**Not yet `1.0`.** `VERSION` is `draft-4`, **one change declared**. The draft-4 block header now reads
"One change is declared" rather than "No change is declared yet". Nothing this session altered a
conformance obligation, so a realization conforming to `draft-3` conforms to `draft-4` unchanged.

**Release 11 is cut from this cycle** — `process/notes/release-11.md`. The order from dev/11 is
superseded in one respect: *re-trial* is no longer a loose next step but **NOVA G0**, a gate that
cannot close without a profile, a decision ledger, findings, and a disposition for each. The freeze
moves behind it deliberately — `draft-4` is G0's **candidate** input, fixed for the trial and not
sealed before it, because G0 may expose a defect that must be repaired first. Revised order:
**G0 → disposition → freeze and tag → close the `1c` omission → G1 → G2**, with `1.0` no earlier
than a realization that can discharge a claim against the frozen revision.

### Next session should start with

**Close G0 — it is not closed.** Three runs produced artefacts; the gate's own conditions are not
met. Outstanding, in order:

1. **Classify and disposition `NPP-E`'s eight findings.** Untouched. They include *no artifact-kind
   taxonomy supplied*, *identity syntax and canonicalization unspecified*, *no family-defined outcome
   names*, and *demonstration fixtures not supplied* — the last being Finding **B** reached from the
   author's side.
2. **Disposition `NPP-D`'s F-1, F-2, F-3** — no canonical profile representation, no trust-root
   verification mechanism, no payload grammar for profile-defined kinds. Identified, carryable,
   undispositioned. All three are one absence in different places: **the family specifies meaning
   and specifies no form**, and every mechanical check needs a form.
3. **Repair whatever those dispositions prove to be normative defects**, and repeat any G0 work they
   invalidate.
4. **Freeze and tag `draft-4`.** Only then may G1 name it.

**Superseded:** the original instruction to run the commission. It has run three times. The standing
technical item below is unchanged.

**NOVA G0 — run the profile-authoring commission.** Everything it needs is written; two things must
be supplied at commission time: a run identity never used before (`6a` §9), and the candidate
revision. `draft-4` is the candidate — fixed for the trial, **not frozen before it**, because G0 may
expose a defect that has to be repaired before the freeze.

G0 is the instrument for three open findings at once: **A** (whether `6a` lets an author tell a
deliberate silence from an omission), **B** (whether a demonstration can be constructed at all), and
**F** (whether the domain-neutral spaces are canonical or one realization's artifacts). For **F**,
compare the author's closed vocabulary against the reference set *only after* the run.

The standing technical item behind it is unchanged: **the requirement projection omits `1c`**, which
states AI-1 … AI-17 as `### AI-1 — …` headings while every other document uses `- **XX-1.**`
bullets. Apply the pattern this session proved — re-harvest, then verify with a counting script that
shares no code with the extractor.

## dev/11. **`draft-3` at Change 10 · independent-authoring trial run once · next: the requirement projection omits `1c`.**

The whole cycle came from one exercise: **an external AI worker was given the family and nothing
else and asked to author a Normative Platform Profile.** Seven of the family's changes this session
were occasioned by what it got wrong, and two by reading its output closely enough to find things it
did not.

### Changes made — `standards`, branch `draft/3`, all committed, working tree clean

| Commit | Files | What |
|---|---|---|
| `f2c2e00` | `6a`, `5b`, `7a`, `doc/revisions.md` | **Changes 4–6.** NP-12 (a profile MUST NOT decide a deferred item by deferring it to the system that claims it); `6a` §7's read-surface row split into openness / attribution; **caller** introduced and glossed in `5b`; `7a` §3.1 bounds a system instance by the snapshot it accepted (RT-3 → next acceptance or stop). |
| `0469548` | `6a`, `5b`, `7a`, `doc/revisions.md` | **Change 7.** Five of ten review observations carried, five declined. Reverted an over-reach in Change 5 — IN-12 had been amended to *"governance applicable to it and to its caller"*, which asserts a governance-to-actor relation the family does not have; `5b` §1 now says **a caller is identified, not governed**. Added `6a` §7's two-systems test, the no-undischargeable-claim rule, `6a` §5's *an additional obligation must add something*, and `7a` §3.1's *a profile's subject-class list is a floor*. |
| `fb18d89` | `4d`, `doc/revisions.md` | **Change 8.** Closes the `4d` re-review left outstanding against `draft-2`. **TR-23 had no document behind it** — the invariant cited §14 and §14 said nothing of the kind; the requirement appeared nowhere in the body, in any revision, and `realization_map.md` records it as *Demonstrated*. §14 now states it. Two linearity over-specifications relaxed: §4 (phases are a dependency order, not a line) and TR-20 (gapless + dependency-respecting, not *total*). |
| `d1ac616` | `0z`, `1a`, `doc/revisions.md` | **Changes 9–10.** `0z` §2 map corrected: `6a` was `NP-1 … NP-11` (my own Change 4 introduced that); **`4e` Supersession was listed as carrying no invariants and carries SU-1 … SU-10**, wrong for two revisions. `1a` gained **CM-1 … CM-7**, derived from §3 and §12 with no wording change — it had six MUSTs and a conformance clause that nothing could cite. Former §13 → §14. |

### Changes made — `.github`, committed

| Commit | What |
|---|---|
| `df47ac5`, `7787623`, `19d9c70` | `process/task_author_a_profile.md` — the trial instrument, salvaged out of the deleted sandbox and hardened: per-run identity (never reused, `6a` §9); **the standard is read, never written**; no previous run's outputs; **do not ask the commissioning party to decide anything**; everything cited must be quotable by document and section. Plus `process/task_author_a_profile_operator.md` — JIT sandbox setup, operator rules, how to read the log, and the Changes 4–7 pass criteria, **deliberately not in the worker's copy.** |

### Build & test status — **PASSING**

No test suite; the family's checks are structural. Run from `standards/spec`:

```
31 documents · 342 invariants · 0 duplicate identifiers · 0 unresolved cross-references
all 25 mapped invariant ranges agree with 0z §2
```

### Open issues

1. **`doc/requirement_projection_contract.md` records `317 requirements · 24 documents`. The family has 25 invariant-bearing documents and the projection omits `1c` entirely.** `1c` states AI-1 … AI-17 as `### AI-1 — …` section headings; every other document uses `- **XX-1.**` bullets, and the extractor matches the bullet convention. The contract's *Verification* section names the count check as *"the guard against silent convention drift"* — the guard did not fire, because the independent count was derived the same way. `draft-3` Change 1 declared this rendering a projection under `4b`, so this is a faithfulness question (PJ-4, PJ-9) about the family's projection of itself. **Correct figures: 342 total; the projection covered 317 of the then-334.**
2. **`7b` has no specification-subject section.** `7a` §3 names **specification** as a conformance subject class evaluated by `1a` and `1b`; both now carry invariants; `7b` does not mention the class and specifies no demonstration for it. Recorded as outstanding in Change 10.
3. **`0z` states three MUSTs — including the derivation rule — and carries no invariants.** Same shape as the `1a` gap just closed; weaker case, left open in Change 10.
4. **`4d` TR-2 / TR-4 presume per-phase register documents**, excluding a model that records each decision as a separately identified declaration. `draft-2` Change 6 settled a finding's location as register/entry/field one revision ago; not reopened on review alone. Recorded as outstanding against `draft-3` in Change 8.
5. **`1a` has two sections named *Conformance*** — §11 (the concepts) and §14 (the document's own clause). Predates this session. One-line fix if wanted.

### Architectural concerns

- **The trial has been run once and its fixes have never been tested.** Changes 4–7 exist because one cold reader fell into holes the family did not catch. Whether NP-12, the two-systems test, and the caller gloss actually catch it is unknown. Pass criteria are written; the run is not done.
- **The trial cannot be run by this assistant.** It authored Changes 4–10; a trial it also authors establishes nothing. It has to be a separate worker, driven by the user, per the task's own §8 on externality being a property of authorship.
- **The first run's artifacts are gone.** `standards/sandbox/` was untracked and deleted. The profile, its questions log, and the evaluation exist only as prose in `revisions.md` Changes 4–8. No artifact-to-artifact diff between runs is possible.
- **Two contamination routes are closed in the task doc but untested**: a commissioner's reply being cited as normative text (it happened — a sentence from a chat reply appeared in the profile attributed to `6a` §7), and the worker patching its own copy of the standard (it happened — including a section insertion that renumbered everything after it).

### Release posture

**Not yet `1.0`.** `VERSION` is `draft-3`, ten changes declared, **no freeze section**. `standards/CLAUDE.md` is explicit that `VERSION` is a revision identity, not a release version, and that bumping it declares nothing. Order agreed: **re-trial → close open issue 1 → freeze `draft-3` → declare `1.0 supersedes draft-3`** (identity only, occasioned by adoption, invalidating nothing).

### Next session should start with

**Open issue 1 — the requirement projection omits `1c`.** Establish whether the extractor ever saw
`1c`'s 17 architectural invariants, fix the extraction or the convention, and correct
`doc/requirement_projection_contract.md`'s stated count from `317 · 24 documents` to the verified
`342 · 25 documents`. It is the one open item that makes a *declared projection of this family
unfaithful to its source*, and it blocks the freeze in a way the others do not.

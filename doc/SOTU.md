# SOTU Handoff

## `standards` `draft/4` — **`v0` carried into the repository: the requirement projection joins the terminology projection, `0d` gains a drawn form, a profile template derived from `6a`, `CITATION.cff`, and the call for review rewritten as an invitation to disagree.** Next: nothing further to specify — publish, and wait for a reader who was not part of this.

The previous entry declared `v0` in `.github`. This session carried it into `standards` itself:
`VERSION` is `v0`, `revisions.md` holds the `draft-3` → `v0` supersession and the five findings
published with it, and the public-facing surface — the call for review, the citation record — now
says the same thing the record does.

### Changes made — `standards`, branch `draft/4`, three commits, working tree clean, pushed

| Commit | Files | What |
|---|---|---|
| `35065ce` | 11 files, +1238/−220 | **The requirement projection.** New `tools/requirement_index.py` derives `projections/requirement_index.md` — **356 requirements across 26 documents**. New `doc/profile_template.md`, derived from `6a` and adding nothing to it. `spec/0d` rewritten and given `0d_…​.svg` — the family's first drawn form. |
| `2fc8c36` | 8 files, +228/−42 | **`v0` in the repository.** `VERSION` → `v0`; `revisions.md` +134 lines carrying the supersession declaration, the five findings **B, C, C-1, C-2, C-3**, and the statement that Change 1 invalidates nothing. New `CITATION.cff` — *cite the revision you read*. Both projection contracts and the `projections/README` brought into line. |
| `870d7e5` | 1 file, +37/−41 | **`doc/call_for_review.md`.** Retitled *Call for Review* → **"an invitation to read, and to disagree"**. Body reflowed. The document ends on **a standing need, separate from review**: `6a` §6 requires that a profile not be authored by the system claiming it, no external profile authority exists, and a separation declared inside this project was **considered and refused as appearance without substance**. |

**The count guard shares no code with the extractor, on purpose.** `tools/check_requirement_count.py`
counts by a second route — `0z` §2 declares each document's invariant range, and the sum of those
ranges is what the family says it carries; the index is what the documents actually yield. It
reports **350 declared across 26 documents, plus 6 suffixed identifiers a range cannot express**
(`1b` SM-5a/7a/7b, `4d` TR-3a/5a/15a) = **356**, agreeing with the index. The first requirement
projection derived its guard the same way it derived the index, so a convention the extractor
stopped recognizing produced a smaller count every other check accepted. A guard that fails the same
way as the thing it guards is not a guard.

**`profile_template.md` carries its own prohibition.** `6a` §11 declines to specify the form a
profile takes, so the template *"is not part of the family and carries no authority"* — and it says
**do not give this to an authoring trial**, because the point of such a trial is to find what the
standard alone leads an author to produce. Three independently authored profiles organising the same
content three ways is the evidence that the structure was not determined; supplying the structure
answers that in advance and destroys the result.

### Build and test status

**Standards projections — PASSING**, and both regenerate byte-identical (`git status` clean after
running them).

| Check | Result |
|---|---|
| `tools/check_requirement_count.py` | exit 0 — 356 expected, 356 carried, every mapped range plus its suffixed identifiers agrees |
| `tools/requirement_index.py --check` | exit 0 — 356 requirements, 26 documents, all contract checks passed |
| `tools/vocab_index.py --check` | exit 0 — 167 terms, 32 documents, **0 defects, 44 warnings** |

**Workspace — PARTIAL.** Environment clean; seven of eight conformance checks pass; one fails.

| Check | Result |
|---|---|
| `pgc_env_check.py` | PASSED — no RI-0 dependency reachable |
| `governance_closure` · `governance_chain_closure` | PASSED |
| `implementation_closure` | PASSED — 28 transforms, every module named and present |
| `frontmatter_fidelity` · `human_block_fidelity` | PASSED — 404 artifacts, prose declares nothing |
| `supersession_agreement` | PASSED — 7 relations, both sides agree |
| `evidence_determinism` | PASSED — `3e` EV-6, EV-7 |
| `admission_contract_fidelity` | **FAILED — 31 findings over 31 gates** |

All nine platform repositories are clean at `dev/12`; `.github` is clean at `dev/12`. **No platform
code was touched this session**, so the admission failure is not a regression from it — it stands
against the snapshot built the previous session (`snapshot/`, 2026-08-26).

### Open issues

**`admission_contract_fidelity` is red on 31 findings, and that is the documented expected state** —
`RUNBOOK.md:157` records them as *"all deliberate"*: other domains' business, plus
`IN_REGISTER_BOOK_V0`'s `subject`, deferred with its ground in `cr_04_catalog` P3 Q1, because
correcting it moves every caller and that change's seed forbids it. **Not an open issue.** A first
pass through this session's check run read the red as new and as the leading next action; it is
neither.

**Five findings carried into `v0` and published with it** — `revisions.md`: **B** (no demonstration
for the specification subject class), **C** (`0z` states MUSTs and carries no invariants), **C-1** (a
demonstration must be capable of failing; nothing requires showing which one does), **C-2** (`3a`
does not name the case distinguishing read routing from hard-coded routing that matches), **C-3** (a
profile exclusion bars comparability and `7a` §10 does not say so). **C-1 and C-2 would change what
conformance costs** if carried — said in the record rather than left to be discovered.

**The workspace-root `CLAUDE.md` repository table is stale.** It describes `business_domains` as
"business domains (ai_governance — untested)". Three domains are on disk and in the snapshot —
`ai_governance`, `blockchain`, `book_library_mgmt` — and 30 of the 31 admission findings are in the
two the table does not mention.

### Architectural concerns

**The 31 gates are in scope, and the profile settles it rather than raising it.** A first reading
took the failure for a scoping question — `blockchain` is named by no profile, so perhaps the check
should not be looking at it. It should. `REFERENCE_PLATFORM_PROFILE_V1` §6: *"A profile states
requirements, never an inventory. A snapshot may contain more than the profile requires and still
conform."* The same rule is in the superseded `NORMATIVE_PLATFORM_PROFILE_BASELINE_V0` §6, so it
predates both the current profile and this session. A profile pins governance identities, the closed
kind vocabulary, entry workflows and claims; **it selects no domains and is not meant to.** Domain
composition by discovery is not in tension with it, and there is no domain selection for a check to
narrow against. The findings are defects against `3a` EX-7 in content the sealed snapshot properly
carries.

**A declared snapshot composition was built, tried, and reverted — considered and declined.** The
observation was that membership in a composition is a fact about the filesystem: `core.py:51` takes
whatever sits under `tokenized/`, `assemble.sh:47` and `release.sh:157` glob `business_domains/*`.
Set against `6c` §10 — adding a domain is a governed transformation (TR-1) and a domain MUST NOT
claim genesis — that reads like a gap, since adding a domain today is `mkdir` plus a build config.

**It was declined because nothing requires it and nothing was failing.** `6c` §11 explicitly does not
specify *"what domains a system has, or how many"* or *"how domains are arranged — in repositories,
packages, or deployments"*, so the family asks for no composition artifact. `6c` §10 requires domain
addition to be a transformation; discovery does not make that false, it only declines to enforce it.
No check was red on it. The gap is between doctrine and mechanism, not a demonstrated defect, and it
was an architectural reading rather than a measured finding.

**Two things the attempt established, worth keeping.** A `STRUCTURE_SNAPSHOT_COMPOSITION_V0` pairing
each domain with its build STRUCTURE **was refused by the compiler** — `ASSERT_PROTOCOL_SURFACE_CLOSED_V0`,
six violations, one per non-platform pairing. The governance surface compiles before domains, so a
platform artifact naming a domain's artifact cannot resolve. **The platform cannot bind domain
identities**, and any future attempt at this must bind them at assembly, the only point where every
compiled domain is in hand. Second, deleting the artifact and rebuilding without cleaning surfaced
`E402_UNDECLARED_OUTPUT` on the orphaned JSON — compiled output with no source declaring it is
already refused, which is the property a composition declaration would have been partly duplicating.

**Including every domain is not a defect and should not be undone.** `release.sh:148` gives the
reason: an omitted domain is assembled from whatever stale output is on disk, and its compile against
the current governance closure is never proven. Seven domains exercise closure over 404 artifacts
rather than one, which is the only available evidence that platform governance is domain-neutral
(`6c` §3 — the platform governs the *form* of governance, the domain governs its own *subjects*).

**`v0` is declared and nothing external has read it.** The programme produced four gates of
independent authoring, realization, execution and transformation, and every instrument that examines
the text runs clean. What none of it manufactures is a reader who was not part of it. The call for
review and the standing need for an external profile authority are the two instruments aimed at
that, and neither is under this project's control once issued.

### Next session should start with

**Publish, and stop specifying.** `v0` is declared, carried into `standards` and pushed; the call for
review is written; every instrument that examines the family runs clean; the workspace is at its
documented state with all nine repositories clean at `dev/12`. The one red check is deliberate and
recorded in `RUNBOOK.md:157`. There is no repair queued and no gap the project can close for itself.

What it cannot manufacture is a reader who was not part of it, and the two instruments aimed at that
are already written and merely unissued: `standards/doc/call_for_review.md`, and its closing section
asking for **a party willing to author and own a conformance profile this project cannot change**.
Issue them.

**Resist the pull to build instead.** This session twice mistook settled matters for open ones — the
31 admission findings, dispositioned in the runbook; and domain composition, which `6c` §11 declines
to specify — and each time the reflex was to start a repair. Both were reverted at no cost, but the
pattern is the risk: with nothing left to specify, an idle instrument finds work that is not there.
The standard is not waiting on another change. It is waiting on someone outside it.

---

## dev/12. **`v0` declared, superseding `draft-3` · NOVA cycle 1 closed and seven findings dispositioned · the standard leaves draft and goes public · next: publish, and wait for a reader who was not part of this.**

The whole cycle came from one instrument: **a terminology index derived over the family and checked
against `1a` §12** — the first instrument pointed at the family's own vocabulary rather than at a
realization. Twenty-four documents declare the terms they introduce; twelve of those declarations
were untrue.

### Changes made — `standards`, branch `draft/4`, one commit, working tree clean

| Commit | Files | What |
|---|---|---|
| `dae8476` | 27 files, +2061/−37 | **`draft-4` Change 1.** Seven terms gained a definition where their document already declared them; four struck; `step` moved to `1a` §8. **Five refinements declared — the first in the family**, CM-2 having required the mechanism since `draft-1` with nothing exercising it. **CM-8 added** (`1a` §1, §12, §13, §14; `0z` §2 row now `CM-1 … CM-8`). Finding **E** recorded, not carried. New `tools/vocab_index.py`; new `projections/` at root; `revisions.md` moved to root beside `VERSION`. |

**Terms struck rather than defined — 4.** `3c` `execution agent` (`1a` §8 already defines
**Runtime**
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

### Changes made — `.github`

| File | What |
|---|---|
| `external_validation_nova/NOVA.md` | **new.** The NOVA programme: a second PGC realization built from the standard alone by a cold worker, to test specification sufficiency and governed self-evolution at once. Five gates — **G0** profile authoring, **G1** experiment protocol, **G2** the realization, **G3** comparative conformance, **G4** governed transformation — and no gate starts until the prior one has *both* its artifact and its findings. Six finding classes, with **class 6, reference-shaped assumption**, as the result the programme exists to produce. |
| `external_validation_nova/instruments/task_author_a_profile.md` | revised for **G0**. Frozen candidate revision; existing profile candidates prohibited *including their shape and field names*; any concern or prefix taxonomy from a realization prohibited *including how many there are*; three finding classes become six; a sixth deliverable — close the kind vocabulary from the family alone; new sections on not inventing a conformance oracle, and on success and failure. |
| `external_validation_nova/instruments/task_author_a_profile_operator.md` | brought into line. Sandbox now built from a named revision via `git worktree`, with an exclusion table — `projections/` and `revisions.md` moved to the `standards` root this session and a whole-directory copy would leak both. New closing procedure: capture outputs, disposition findings, *then* freeze. **Fixed a broken path** — the setup script copied the worker document from `.github/doc/`, where it does not live. |
| `doc/SOTU.md`, `doc/` | nine resolved `draft-3` working files removed; the `draft-2`-era entry trimmed. `parked_rulings.md` kept — deferred, not resolved, and cited three times from `standards/doc/realization_map.md`. |
| `external_validation_nova/NOVA.md`, `external_validation_nova/instruments/task_author_a_profile_operator.md` | **the G1 network regime, settled per gate.** Not one policy: **G0** removes the network-capable surface outright — no `Bash`, no web tools, no subagents, because reading `spec/` and writing documents needs none of them, leaving no residual. **G2** cannot be bound that way, since a worker that executes can reach the network; it needs an offline container, with dependencies staged in advance from a fixed manifest and recorded. **G3/G4** need nothing. The trap named explicitly: G0's guarantee does not cover G2, and G2 is the gate that most needs isolation. |
| `external_validation_nova/instruments/task_author_a_profile_operator.md` | **the sandbox moves out of the workspace tree.** It was specified at `standards/sandbox/`; an agent session inherits the `CLAUDE.md` files above its working directory, and the workspace root's names every repository, the build lifecycle and the platform composition. A sandbox inside the tree hands over the whole reference architecture before the worker reads one document — contaminated by its own location. Now `~/g0-run`, with a check that nothing above it carries context and that the worker's agent-configuration directory has been archived. |
| `external_validation_nova/instruments/g1_realization_protocol.md` | **new.** G1 — what a realization worker may see, must produce, and is judged by. Its hard exit criterion is discharged: **disposition C**, a conformance suite is deliberately outside the family, so G2's claim discharges by demonstration with declared fixtures — including negative ones — obtainable by a party that did not build the system. `7b` §6's obtainability rule is the operative constraint, not a schema. |
| `external_validation_nova/instruments/task_build_a_realization.md` | **new.** The G2 worker commission, derived from G1. Its §6 carries the finding G2 exists to produce: an author can leave a question open on the page and a builder cannot, so every gap is filled with something, that something works, and a working system feels like evidence the choice was right. It is not evidence the standard determined it. |
| `external_validation_nova/NOVA.md`, `external_validation_nova/instruments/g1_realization_protocol.md` | **independence scoped to the boundaries that carry it.** Two only: `NPP-E`'s author must not build NOVA (`6a` §6), and NOVA's builder must not have had access to G0's findings. **A single worker may perform G2 and G4** — no fresh-worker rule between them, since G4 transforms the system G2 built. **G3 is a commissioning-side comparative evaluation**, not a worker task. Mirrors the real separation: standard author ≠ profile author ≠ implementer ≠ certifier. |
| `external_validation_nova/instruments/g1_realization_protocol.md` | **the claim types are bridged to the classes.** The worker-facing documents carry no class reference at all — five claim types for the worker, classes for the evaluator — and nothing said how one became the other. G1 §7 now maps *claim type × source basis* to class, and states what the record alone cannot settle: class 5 and class 6 differ by whether the worker chose freely among workable options or had to arrive at a shape for anything to fit. Class 6 is never named to a worker, because naming it says a realization exists. |
| `external_validation_nova/NOVA.md` | **G4's stronger follow-on, recorded and not required.** A transformation by an operator who did not build NOVA would test the premise harder: if evolution needs the builder's memory, the governed state did not carry what it required. Not a condition of the current claim. |
| `projections/`, `tools/` *(in `standards`)* | **the `1c` omission closed** — see below. |
| `external_validation_nova/` | **new tree, SoC.** The whole programme out of `doc/` and `process/`: `NOVA.md`, `instruments/` (7 commissions and protocols), `runs/` (11 — three G0 trials, G2, G4, with evaluations and dispositions), plus `README.md` and `CYCLE-1.md`. Twenty stale cross-references rewritten and verified to resolve. `doc/` keeps SOTU, `parked_rulings.md`, `e0_ruling_3_brief.md`; `process/` keeps the runbook, release script, checks, and the `6b` environment-profile trial — which is *not* NOVA and stays put. |
| `process/notes/release-11.md` | **new.** *A declaration is not a definition* — the release note for this cycle. Deliberately echoes release 10's *declared ≠ implemented ≠ enforced ≠ demonstrated*: the same shape of finding one level up, an instrument turned on the standard instead of on the realization. Carries the extractor's own failure as a full section, because a note reporting 124 defects without saying 111 were its own blindness reads as self-serving. Documents are named by role, not file identifier, matching release 10's register. |

### Changes made — `snapshot_assembler` and `protocol_runtime`, uncommitted

`SNAPSHOT_ASSEMBLY_CONTRACT.md` moved from `.github/doc/` to `snapshot_assembler/doc/`. Four modules
cite it — `assembler/{__init__,core}.py`, `runtime/{boot,loader}.py` — and an implementation
contract
belongs with the component it governs, not in org config. Its header carried two dead references:
`NAMESPACE_MODEL.md`, which exists nowhere in the workspace or in RI-0 and has no successor, and
`spec/01_machine_block.md`, an RI-0 path. **Neither was used by the body** — both words appeared
only
in that line — so they were replaced with what actually governs assembly, `3b` and `4b`, rather than
translated. The `Status:`/authoring-note bullet was dropped.

### NOVA G0 — three runs, three instrument repairs

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
carry-over was found, scoped to authoring runs: **use a worker that has not performed a previous
authoring run, in a context that holds none of one.** The existing prohibition covered what is
handed over, not what is remembered. It does not reach forward to G2 and G4, where the boundaries
are `NPP-E`'s authorship and access to G0's findings, and nothing more.

**The rule that outlives G0:** an experiment may constrain the task, but it must not supply the
distinction whose derivability it is measuring.

### G0 is closed

All conditions met: three profiles, their registers, every entry classified, every finding
dispositioned. **No freeze** — that moved behind G2 (below).

**Seventeen candidate findings across three runs. Zero undeclared gaps.**

| Run | Candidates | Carried |
|---|---|---|
| `NPP-C` | 9, reclassified to 7 | 0 |
| `NPP-D` | 3 checked | 0 |
| `NPP-E` | 8 | 0 |

Every one landed on something the family had already marked — `6a` §7 and §11, `4c` §8, `2d` §1,
`2b` §10, `3e` §12, `3d` §7, `7b` §6, `2c`. Three authoring passes probing for the standard's edges
found only edges it had already drawn. **That the exercise changed no specification text is the
result, not a shortfall**: the *does-not-specify* apparatus held under three attempts to find its
seams.

**The seventeen are one position held consistently: the family specifies meaning and declines
form.** Encoding, syntax, canonicalization, schema, signature mechanism, publication, fixtures —
each named somewhere as a realization's or a profile's to choose. The consequence the authors kept
reaching is real and is the design: **a profile claim cannot be checked mechanically from the
family alone.**

**That settles G1's hard exit criterion in advance.** Of the three permitted dispositions for the
missing conformance suite, the answer is **C — a suite is deliberately outside the family.** G1 must
define G2's discharge in those terms. `7b` §6's obtainability rule is the operative constraint on
G2, not a schema: *"a demonstration against material an evaluator cannot obtain is not a
demonstration to that evaluator."*

**A third instrument repair**, from `NPP-E`: the commission asks for *"matters left unresolved"* and
never says **unresolved by whom**. That author read it as *unresolved by the family* — which is what
delegation is — and filed eight family delegations as findings. Run `NPP-C` inflated in the opposite
direction, filing commissioner scope as family delegation. Registers must be named by who is left
holding the question, not by where the silence originated.

### The `1c` omission — closed

Carried since dev/11 and blocking the freeze. The requirement projection reported **317 requirements
across 24 documents**; the family carries **356 across 26**.

**It was short by two whole documents, not one.** The extractor knew only the bullet form
`- **GS-1.** …`, so `1c` — which states AI-1 … AI-17 as `### AI-1 — …` headings and uses no bullets
— read as carrying nothing. `1a` was the second, and had nothing to find until Change 1 gave it
CM-1 … CM-8.

`tools/requirement_index.py` is new and harvests both forms. `projections/requirement_index.md` is
published, and the contract that declared it since `draft-3` finally has a projection behind it.

**The guard is the part that matters.** dev/11 recorded that the old count check *"did not fire,
because the independent count was derived the same way"*. `tools/check_requirement_count.py` shares
no code with the extractor and counts against a **different artifact** — `0z` §2's declared ranges.

**It fired twice before it agreed**, and both were real defects in the guard, found by running it
rather than reasoning about it:

1. `1b` and `4d` each over by three. A range like `SM-1 … SM-12` names twelve positions, and those
   documents carry `SM-5a, SM-7a, SM-7b` and `TR-3a, TR-5a, TR-15a`. **Range notation cannot express
   a suffixed identifier.**
2. The suffix scan then counted `SM-7a` in `6b` and `TR-15a` in `6c` and `7b` — cross-references,
   not owned invariants. Restricted to each document's own prefix, which `0z` already names.

```
356 requirements · 26 documents · 339 bullet · 17 heading
0z §2 declares 350, plus 6 suffixed identifiers = 356 · agreed
re-derivation byte-identical (PJ-2, PJ-9)
```

**One thing surfaced and left open:** `0z` §2's ranges understate the family by six, because range
notation cannot carry a suffix. The guard reports the six explicitly rather than absorbing them.
Whether `0z` should state counts rather than ranges is a question for the freeze, not for tooling.

### NOVA — cycle 1 complete except G3

Full account in `external_validation_nova/CYCLE-1.md`, written for the expert loop. In brief:

| Gate | | |
|---|---|---|
| **G0** profile authoring | run ×3 | `NPP-C`, `NPP-D`, `NPP-E` |
| **G1** protocol | written | governs G2 |
| **G2** realization | run | claims `NPP-E`, discharges 1 of its 8 claims |
| **G3** comparative conformance | **blocked** | `NPP-E` §12 excludes the reference by construction; `7a` §10 makes systems under different profiles incomparable. Needs a third profile both can claim — a design question, not a run |
| **G4** transformation | run | a lending domain added to G2's own baseline, grounded by identity |

**No repair to the standard follows from any gate.** Seventeen G0 candidates, nine G2
determinations with **none** carrying source basis `none`, and a G4 transformation that grounds by
querying the baseline rather than assuming it. **No class 6 anywhere.**

**Two evidence gaps, identical in shape, both found only by mutation testing.** `NPP-E` mandates a
SHA-256 digest and substituting MD5 passed all six G2 demonstrations; the G4 baseline-grounding
guard was correct and disabling it passed all fifteen. Both times a property the profile requires
was implemented, asserted *about*, and never demonstrated by anything that could fail. **A passing
suite is not evidence a demonstration could fail.** Both closed on the first pass after being named.

**The instrument failed three times and each repair is now in the commissions**: the taxonomy
answered the question it measured, commissioner scope was counted as family delegation, and a
worker's memory is not covered by a rule about handed-over material. The rule that outlives the
programme: *an experiment may constrain the task, but it must not supply the distinction whose
derivability it is measuring.*

**`3a` has since been built against.** The transformation's first delivery declared a workflow
carrying an outcome vocabulary that **nothing read** — the rule lived in a method, and deleting the
workflow artifact left behaviour unchanged. Asked to discharge the Runtime and execution claim, the
builder drove traversal from the sealed declarations. The decisive mutation — replacing
`step["routes"][outcome]` with the behaviourally equivalent hard-coded branch — **now fails a
test**, which is the only check a well-formed fixture cannot make.

**Three of `NPP-E`'s eight claims are discharged**, not two. An earlier draft miscounted:
the transformation is a claimed and discharged claim, not evidence for another. The summary now
carries a claim ledger distinguishing **discharged** (2, 4, 5), **exercised but not claimed**
(3, 6, 7) and **not claimed** (1, 8). The correction came from the builder.

**Three candidate findings against the standard — the first the programme has produced.** None from
being blocked; all from the builder's reflection. Recorded, not carried:

- **C-1** — `7b` requires a demonstration *capable* of failing, not that you show *which one* fails.
  Two correctly implemented guards broke no test and were invisible to everything but mutation.
- **C-2** — `3a` does not distinguish a route followed, a route absent, a route retargeted, and
  **hard-coded routing ignoring a changed declaration.** The fourth is the decisive architectural
  test and is unnamed in the text.
- **C-3** — `7a` §10 says systems under different profiles are not comparable; it does not say a
  **profile exclusion** bars comparability, which is exactly why G3 is blocked.

**One implementation limitation recorded**, also from the builder: `3d` CP-9 requires a declared
binding, and the realization dispatches on the capability's `effect` value as an implicit one.

**A snapshot exists and verifies independently.** NOVA had produced three snapshot identities and
no snapshot — nothing wrote one to disk, and the sealed content lived only in memory for the length
of a process. Reproducible, but not obtainable in `7b` §6's sense. The builder emitted
`snapshot.json`, archived at `runs/g4_run/`.

**Verified without using any of the realization's code**: `whole_integrity` recomputed from the
fields it declares it covers matches; `id` is `snapshot:` + that digest; **all five artifact
identities verify as content-derived.** That is `3b`'s *"verifiable — its integrity and identity can
be checked by a party that did not build it"*, satisfied rather than asserted, and it is the
strongest artifact the programme has produced.

Three things that could have been wrong and were not: `whole_integrity_covers` lists itself while
excluding `id` and `whole_integrity`, so the self-reference is handled; `constituents` carries whole
artifact objects rather than identities, so the snapshot is self-contained; and `governance-element`
is admitted by the vocabulary and absent from the snapshot, which is correct — a closed vocabulary
states what may exist, not what must.

**Still untested:** `3d`'s effecting path — no capability with an external effect, and `NPP-E` §2
selects no interaction boundary, so it may not be reachable under this profile at all.

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

1. ~~The requirement projection omits `1c`.~~ **Closed this session** — published at 356
   requirements across 26 documents, with a count guard that reads `0z` §2 rather than re-deriving
   from the documents. What it surfaced and left open: **`0z` §2's ranges understate the family by
   six**, because a range cannot express `SM-7a`. Whether `0z` should state counts rather than
   ranges is a freeze question.
2. **Finding E — nothing says when a word must become a term.** Six are declared, defined, and used
   nowhere: `Promotion` (`1a`), `construction disposition` (`2c`), `projection source` (`4b`),
   `protocol adapter` (`5a`), `profile derivation` (`6a`), `demonstration coverage` (`7b`). Evidence
   in `projections/vocabulary_locality.md`. Not carried — a CM-9 would have to be discharged by
every
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

- **A definition does not create a use.** `6c`'s pair was reported as declared-and-unused; the
triage
  judged that §3 names the distinction and defined them rather than striking them. They were then
  declared, defined, and *still* unused, and were struck. Writing a definition is the tempting
remedy
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
- **`spec/` was held clean.** Projections stay out of it: a file identifier confers family
membership
  (`0z` §2), and a regenerated file inside a family built on declared supersession contradicts
  `4e` §9. `doc/` was reduced to what has no more specific home.

### Release — `v0`

**`VERSION` is `v0`, declared as superseding `draft-3`.** The version is a single number starting at
zero — ground zero, the first identity anyone may build against or name in a claim. Not semantic:
no major, minor or patch, because `4e` §9 holds that a revision is *declared* rather than inferred
from a number.

**`draft-4` was the working name and is gone.** It was never frozen, never tagged, no claim was made
against it, and nothing outside the repository named it — checked before collapsing it, so the
rename rewrote no external reference. The single supersession is `draft-3` → `v0`, and Change 1 is
its content.

**Occasioned by exposure, not by a defect.** Four gates of independent authoring, realization,
execution and transformation produced no undeclared gap; the terminology and requirement projections
run clean. **What the programme cannot manufacture is a reader who has not been part of it**, and a
draft identity now costs more than it buys.

**It invalidates nothing.** Change 1 altered no obligation on a realization — CM-8 binds documents
of
the family, not systems. A realization conforming to `draft-3` conforms to `v0` unchanged.

**Five findings are carried into `v0` and published with it**, each with what would settle it:
**B**,
**C**, **C-1**, **C-2**, **C-3**. Two of them — C-1 and C-2 — **would change what conformance
costs**
if carried. Claims against `v0` survive under `0z` §5.1, but a successor may ask more. That is said
in the declaration rather than left to be discovered.

**Also this cycle:** `call_for_review.md` reframed from a tasking document to a review invitation —
*"read it and say where it is wrong"* — with Discussions, Issues and email as channels, all eight
links repointed to `blob/v0/`, and the profile-authority ask demoted to a standing need stated
separately from the review. `CITATION.cff` added, carrying `version: v0`.

**Release 11 remains this cycle's composition release** — `process/notes/release-11.md`. It is
independent of the standard's revision identity: release 9 removed the standard from the composition
so it could be versioned on its own.

### Next session should start with

**Run G2 — the independent realization.** G0 is closed, G1 is written
(`external_validation_nova/instruments/g1_realization_protocol.md`), and the worker commission
derived from it is written
(`external_validation_nova/instruments/task_build_a_realization.md`). Nothing remains to author;
what remains is setup.

G1 settled three things so they are not re-derived at G2:

1. **The conformance-discharge basis is disposition C** — a suite is deliberately outside the
   family. G1 states G2's discharge in terms of demonstrations and evidence an outside party can
   obtain and check, per `7b` §6. It must not invent a test oracle.
2. **The network regime is settled per gate.** G2 needs environment isolation, not tool restriction:
   a worker that can execute can reach the network. Dependencies staged in advance from a fixed
   manifest, and recorded.
3. **The revision target is a pinned commit, not a frozen revision.** The freeze is after G2.

**G2's remaining setup, all of it mechanical:**

- an **offline container or VM** — G0's tool restriction cannot bind a worker that executes;
- ~~`NPP-E`'s scope register renamed to `NPP-E-scope.md`~~ — **done.** It was returned as the
  extension-less `list_assumptions`; the commission tells the worker to read it *before* the
  profile, since without it a commissioning constraint reads as a family requirement. The
  deliverables' own text was left unedited and the rename is recorded in the run's README;
- the **staging manifest**, declared by the worker before isolation and closed once the run starts.
  A later request is granted if it must be, and recorded as a break in the isolation with its
  reason and moment;
- a **worker satisfying the two independence boundaries, and no more than those**: it must not be
  the author of `NPP-E` (`6a` §6), and must not have had access to G0's findings or other excluded
  material. **The same worker may then perform G4** — no fresh-worker requirement stands between
  the gates, and G4 transforms the system G2 built.

**The commission's §6 carries the finding G2 exists to produce.** An author can leave a question
open on the page; a builder cannot — code does not run with a hole in it. Every gap must be filled
with something to proceed, that something will work, and a working system feels like evidence the
choice was right. It is not evidence the standard determined it. The test given to the worker is one
question: *can I quote what determined this, by document and section?*

**Watch for class 6.** G0 produced none, and authoring a profile does not press on the standard the
way building does. Either outcome at G2 is informative; several would be the most valuable findings
the programme can generate.

**The profile G2 builds against is `NPP-E`** — the only run of the three that was uncontaminated..

**The standing technical item is closed.** The requirement projection is published at 356
requirements across 26 documents, with an independent count guard. What remains for the freeze is
whether `0z` §2 should state counts rather than ranges, since a range cannot express `SM-7a`.

---

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
| `df47ac5`, `7787623`, `19d9c70` | `external_validation_nova/instruments/task_author_a_profile.md` — the trial instrument, salvaged out of the deleted sandbox and hardened: per-run identity (never reused, `6a` §9); **the standard is read, never written**; no previous run's outputs; **do not ask the commissioning party to decide anything**; everything cited must be quotable by document and section. Plus `external_validation_nova/instruments/task_author_a_profile_operator.md` — JIT sandbox setup, operator rules, how to read the log, and the Changes 4–7 pass criteria, **deliberately not in the worker's copy.** |

### Build & test status — **PASSING**

No test suite; the family's checks are structural. Run from `standards/spec`:

```
31 documents · 342 invariants · 0 duplicate identifiers · 0 unresolved cross-references
all 25 mapped invariant ranges agree with 0z §2
```

### Open issues

1. **`doc/requirement_projection_contract.md` records `317 requirements · 24 documents`. The
family has 25 invariant-bearing documents and the projection omits `1c` entirely.** `1c` states
AI-1 … AI-17 as `### AI-1 — …` section headings; every other document uses `- **XX-1.**` bullets,
and the extractor matches the bullet convention. The contract's *Verification* section names the
count check as *"the guard against silent convention drift"* — the guard did not fire, because the
independent count was derived the same way. `draft-3` Change 1 declared this rendering a
projection under `4b`, so this is a faithfulness question (PJ-4, PJ-9) about the family's
projection of itself. **Correct figures: 342 total; the projection covered 317 of the then-334.**
2. **`7b` has no specification-subject section.** `7a` §3 names **specification** as a conformance
subject class evaluated by `1a` and `1b`; both now carry invariants; `7b` does not mention the
class and specifies no demonstration for it. Recorded as outstanding in Change 10.
3. **`0z` states three MUSTs — including the derivation rule — and carries no invariants.** Same
shape as the `1a` gap just closed; weaker case, left open in Change 10.
4. **`4d` TR-2 / TR-4 presume per-phase register documents**, excluding a model that records each
decision as a separately identified declaration. `draft-2` Change 6 settled a finding's location
as register/entry/field one revision ago; not reopened on review alone. Recorded as outstanding
against `draft-3` in Change 8.
5. **`1a` has two sections named *Conformance*** — §11 (the concepts) and §14 (the document's own
clause). Predates this session. One-line fix if wanted.

### Architectural concerns

- **The trial has been run once and its fixes have never been tested.** Changes 4–7 exist because
one cold reader fell into holes the family did not catch. Whether NP-12, the two-systems test, and
the caller gloss actually catch it is unknown. Pass criteria are written; the run is not done.
- **The trial cannot be run by this assistant.** It authored Changes 4–10; a trial it also authors
establishes nothing. It has to be a separate worker, driven by the user, per the task's own §8 on
externality being a property of authorship.
- **The first run's artifacts are gone.** `standards/sandbox/` was untracked and deleted. The
profile, its questions log, and the evaluation exist only as prose in `revisions.md` Changes 4–8.
No artifact-to-artifact diff between runs is possible.
- **Two contamination routes are closed in the task doc but untested**: a commissioner's reply
being cited as normative text (it happened — a sentence from a chat reply appeared in the profile
attributed to `6a` §7), and the worker patching its own copy of the standard (it happened —
including a section insertion that renumbered everything after it).

### Release posture

**Not yet `1.0`.** `VERSION` is `draft-3`, ten changes declared, **no freeze section**.
`standards/CLAUDE.md` is explicit that `VERSION` is a revision identity, not a release version,
and that bumping it declares nothing. Order agreed: **re-trial → close open issue 1 → freeze
`draft-3` → declare `1.0 supersedes draft-3`** (identity only, occasioned by adoption,
invalidating nothing).

### Next session should start with

**Open issue 1 — the requirement projection omits `1c`.** Establish whether the extractor ever saw
`1c`'s 17 architectural invariants, fix the extraction or the convention, and correct
`doc/requirement_projection_contract.md`'s stated count from `317 · 24 documents` to the verified
`342 · 25 documents`. It is the one open item that makes a *declared projection of this family
unfaithful to its source*, and it blocks the freeze in a way the others do not.

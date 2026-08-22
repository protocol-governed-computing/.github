# SOTU Handoff

## dev/9 is closed. The standard is drafted and now lives in its own repository.

Read this cold: it is self-contained.

### Where things stand

**The Open PGC Standard is complete as `draft-1`** — 31 documents — and is no longer part of the
composition. `standards/` was re-initialized with clean history and pushed to a recreated remote.
Its `VERSION` is `draft-1`, deliberately not the composition integer.

**The composition is ten repos.** `standards` was removed from `REPOS` in `release.sh`.
`.github` absorbed the workspace process, the reference profile, and this handoff.

```
standards/          the standard, alone      spec/ (31 docs), README, LICENSE, NOTICE
.github/            org + workspace          process/ (release.sh, 5 checks, RUNBOOK, notes/)
                                             doc/ (SOTU, parked_rulings, assembly contract)
                                             snapshot_profiles/
software_governance/doc/namespace_map.md     the fb.* migration plan, beside its ruling
```

**Everything is committed and clean.** Checks pass from their new location:

```
python .github/process/pgc_env_check.py           PASSED — no RI-0 reachable
python .github/process/implementation_closure.py  PASSED — 27 transforms
.github/process/release.sh --check                build gate ok, snapshot 7b6f2699…
                                                  composition PASSED, 5 rules / 398 artifacts
                                                  fails only on missing release-9 notes
```

### The standard, in one screen

```
spec/0a-0c   Part 0    why this exists                       non-normative
spec/0z      Part 0    document set map, derivation rule, editorial rules, revision semantics
spec/1a-1c   I         Model              SM-1…12 · AI-1…17
spec/2a-2f   II        Governance         GS · GO · MB · KV · CA · EN
spec/3a-3e   III       Execution          EX · SN · RT · CP · EV
spec/4a-4e   IV        Construction       GC · PJ · ID · TR · SU
spec/5a-5b   V         Interchange        IB · IN
spec/6a-6c   VI        Profiles           NP · EE · DP
spec/7a-7b   VII       Conformance        CF · CD
spec/8a      Annex     Implementation Guidance               non-normative
```

A file identifier is an **address, not an identity**. Documents reference one another **by name**;
invariant prefixes never encode a file identifier. `spec/0z` is authoritative on structure — read it
before editing anything.

**Parts I–VII are drafted and reviewed. Revise only by explicit ruling** — and a revision is
supersession (`4e` §9): declared against a named predecessor, stating what it changes and what that
invalidates.

### dev/10 — agreed scope, in dependency order

1. **Repo split** — **done this session.**
2. **The realization map** (`8a` §6). Map each normative document to where the reference realization
   demonstrates it. This *is* the spec↔RI validation, and it tells you which requirements the RI
   cannot currently meet **before** anything is migrated.
3. **Namespace migration** — `fb.*` / `pgc::`. `AUTHORITY_VS_CONCERN_RULING` step 2 (canonical
   representation) is unblocked by `2b` §7.2. Plan is `software_governance/doc/namespace_map.md`.
   Scale: 1,407 occurrences, 532 files, 6 repos.
4. **Human-block template** — standardize the non-normative block across artifacts. Last, because
   the map tells you what artifacts need to say.

**Direction is not symmetric.** Validate the **RI against the spec**, never the reverse. `0z` §3: a
realization "informs this family by exposing concepts that were missing, distinctions that were
conflated, and requirements that could not be met; **it never supplies authority.** Where a document
and a realization disagree, the document governs and the disagreement is resolved by ruling."

**Constraint on item 4:** `MB-1` makes the machine block the *sole* normative declaration surface —
everything outside it "MUST NOT determine anything." A human-block template must carry nothing
load-bearing, or the thing meant to bring artifacts into conformance breaches MB-1.

### Open Issues

1. **Release 9 is uncut and now warranted.** Only the notes file is missing. It would mark the first
   composition without `standards` — `.github` absorbing the process, `software_governance` gaining
   the namespace map. No governed content changed; snapshot id is unchanged from release 8. Decide:
   cut it as the boundary marker, or roll into a later release once dev/10 work lands.
2. **`fb.*` / `pgc::` violation stands.** `2b` §7.2, GO-11, MB-7, ID-12 state the requirement; the
   implementation violates it. Ruled finding — the standard does not bend.
3. **Identity authority conflict.** `2c` MB-6 and `4c` ID-1/ID-9 require declared identity
   authoritative over position; discovery remains filename-driven. `4c` §10 gives the settling test:
   **relocation** — move a thing without changing declarations, and nothing about its identity,
   governance, or any composite identity may change.
4. **`blockchain` carries three references to a superseded workflow.** Under SU-5 it will not compile
   once referential closure is enforced. Detail in `.github/doc/parked_rulings.md`.
5. **Four architectural invariants have no counterpart** in the implementation's invariant list:
   AI-4 (determination precedes effect), AI-7 (refusal dominates), AI-14 (every determination
   evidenced, including refusals), AI-16 (evidence checkable without its producer). Unverified
   against code — the comparison to date is document-level only.
6. **Two Part-II questions deliberately open**: whether Evidential is a peer semantic category, and
   whether provenance remains an independent axis. **Federation** is treated as a relation among
   authorities with its ontological status open.

### Architectural Concerns

- **Item 2 will find defects in the spec, not only in the RI.** That is its purpose. Each is a
  finding resolved by ruling (`0z` §3), and a spec change is a revision superseding `draft-1` — so
  `draft-1` must stay marked and unedited as the predecessor.
- **`8a` §6 states the map's second purpose**: a normative document with no demonstration is either
  unimplemented or unimplementable, and the map makes which one visible. Expect it to expose both.
- **The map must not become a specification.** It is evidence about one realization; `8a` §2 governs
  what such evidence establishes — notably that resembling the reference realization establishes
  nothing.
- **`parked_rulings.md` is the ruling record.** It carries the charter contradictions, the kind
  enumeration ruling, the conformance-section ruling, the transformation comparison runs, and the
  specification-plan residue. Read it before reopening anything that looks unsettled.

### Next Session Should Start With

**Begin the realization map (`8a` §6)** — dev/10 item 2, and the prerequisite for items 3 and 4.

Work document by document through `standards/spec/`, and for each record: which declarations,
construction path, region of the sealed representation, or evidence demonstrates it — and where
nothing does, whether that is *unimplemented* or *unimplementable*. The second class is a finding
against the specification.

Start where the correspondence is densest and best understood: `3b` Snapshot against `snapshot/`,
`4a` Governed Construction against `protocol_compiler/compiler/stages/`, `5b` Governed Inspection
against the `si.*` operations. Those three will establish the map's shape before the harder ones.

Before touching anything: **decide Open Issue 1** — whether release 9 is cut now as the
composition boundary, or deferred.

---

# SOTU Handoff

## Release 8 is cut; cycle 9 is open

All 11 repos are on `dev/9`, tagged `release-8` and `history-8`. `.github` joined the composition
this release and carries its first tag. `VERSION` is 9 everywhere, the five editable packages are
reinstalled and report 9, and a clean rebuild passes: snapshot `7b6f2699…`, composition conformance
PASSED over 398 artifacts. `release.sh` is set to `RELEASE=9` / `NEXT=10`.

The snapshot id did not move across the release. That is the correct result — release 8 was
documentation, one specification fragment, two governance findings and five citation paths, and none
of it is governed content.

## Next session should start with

**`dev/9`'s main focus is standards development.** A proposal is coming from the author — wait for
it before opening work.

Two constraints on whatever it turns out to be:

- **The `fb.*`/`pgc::` thread stays parked.** Do not touch `pgc::`, `fb.*`, or the namespace
  representation. It is resumable from `software_governance/doc/AUTHORITY_VS_CONCERN_RULING.md`
  alone — finding, evidence, ruling, and the ordered follow-on plan with its blast radius, so
  nothing has to be re-derived. Note that it rode into `release-8` **unratified**: being tagged
  is not acceptance.
- The specification fragments live in `standards/doc/spec/` (`01_machine_block`, `02_kind_vocabulary`,
  `03_governance_ontology`, `04_transport`, `05_transformation`). `03` gained the
  Authority / Concern / Federation / Namespace distinction this release, with two open questions
  recorded at its foot.

## Where things stand

**The rule sets are no longer merely declared — 95.6% of them have been observed to refuse.**
`meta_test` proved every rule resolved to a mechanism; nothing proved a rule ever *fired*. Measured:
63 of 229 rule identifiers had ever been seen to fail. Thirty negative corpus documents later, 219
have. No rule was authored and no design construct added — the repair was documents.

```
                 before   after          P0 13/13   P3 21/21   P6 21/22   P8 19/19
observed to fire    63     222           P1 16/16   P4 18/18   P7 74/80
                  27.5%   96.9%          P2 16/16   P5 24/24
corpus documents    40      83
```

**Six defects that were invisible while the rules were only declared.**

1. **`DESIGN_LEAKED_INTO_BUSINESS_LANGUAGE` could not fire at P3, P5, P6 or P7.** The scoped flag
   `business_language=capability,notes` emitted a rule keyed on the template author's spelling, while
   parsed rows are held under the header `Capability`. Twenty-five column declarations, none able to
   match. **Fixed** in `template_reader.py`; a scoped name that resolves to no column now raises.
   Blast radius, measured: one existing fixture turned red on a genuine leak it had always carried.
2. **`TABLE_HAS_COLUMNS` matched a required column by prefix against any header**, so `Source
   Finding` satisfied a required `Source`. Nine registers across six phases could lose a column and
   report clean. **Fixed** — matches consumed once, exact before prefix, zero blast radius.
3. **`CITATION_ORDINAL_UNRESOLVED` is silent on every citation a real P5 document carries.** It
   resolves an ordinal inside the prior a citation names; P5 documents cite S1/S2/S4 and P5 receives
   only p0. Not fixed — the prior model is the question, and that is a ruling.
4. **`BINDING_SOURCE_UNREACHABLE` skips most of its own register.** It requires the binding's `Owner`
   to be a workflow; most step-binding owners are capability contracts and are passed over unread.
5. **Cross-subdomain reach looked like five rules needing a new dossier and was four needing the
   right kind of identifier.** `declared_reach.Consults` names a runtime **binding**, not a store;
   `.Act` names a **workflow**, not a contract; `cc_composition.Store` names a store by its **bare
   name**, not its key. One corpus document against cr_01's own priors now fires
   `DECLARED_REACH_UNUSED`, `CROSS_SUBDOMAIN_WRITE` and `NODE_INPUT_UNBOUND`. **Two rules genuinely
   need a dossier and its spec is recorded** — see issue 39.
6. **A correct check can make a fixture useless as evidence.** Dropping a vocabulary-bearing column
   at P1 fired `CELL_NOT_IN_VOCABULARY` thirty-nine times; dropping `field_declarations` at P8 fired
   `SCHEDULED_ARTIFACT_UNPLACED` forty-two. Both checks right, both fixtures unreadable, both recut.

**Are the rules domain-neutral? The rules yes, the corpus no.** Zero domain nouns across all nine
compiled rule sets. Three structural documents rewritten from library catalog into freight logistics
fired **identically** at P3; at P5 and P6 they fired a superset, and every extra was a prior-coupled
rule correctly reporting that the document had stopped answering for its own change request. The
boundary sits where it should. What is not neutral is the corpus: five of nine phases rest on one
subdomain of one domain.

**Where these rules live, since it is a fair thing to ask.** Declared in Python → generated into the
`WF_P*_ADMISSIBILITY_V0` artifacts → compiled → **sealed into the composition**; all 24 P5 rule ids
are in `snapshot/canonical/transformation/workflows/`. `tc phase check --snapshot` reads the sealed
set, not the working tree, because a dossier's pin already names the rule set. **The rules are live;
the corpus is the evidence that they fire.** `transformation/doc/FEATURE_LEVEL_CLOSEOUT.md` carries
the full account.

**`register_coverage` is closed unbuilt — and closing it found that two of its three instances had
been fixed months ago with nobody recording it against the fork.** That is why it read as "scope
collapsed" rather than as two-thirds delivered. The third instance is still true and is a different
question from the one the dossier asks. Issue 43; `transformation/doc/REGISTER_COVERAGE_VERIFICATION.md`
carries the evidence and `dossiers/register_coverage/closure.md` the ruling.

**dev/7 is closed. Invariant enforcement authority was measured, ruled on in four parts, and every
part proved by a probe built to fail.** The opening premise — *declared doctrine that no mechanism
reads* — did not survive measurement, and neither did its replacement. What was actually there:

- **`assert_projection.enforcement.phase` had no authority at all.** Declared on 14 of 88 invariants,
  canonicalized by `s1_extract`, copied into the derived ASSERT by `s4_govern`, and branched on by
  nothing. It disagreed with `core.enforcement_stage` on 7 — one of them a hard contradiction, where
  `composition_conformance` gates the invariant out of ASSERT derivation while the same machine block
  claims the assert phase. **Deleted**, from the 14 and from the schema. Because
  `enforcement.additionalProperties` is already `false`, the deletion is self-enforcing: a future
  `phase:` is a schema failure, not a review miss.

- **The dimension was already bounded.** The proposed repair was to add the enum
  `core.enforcement_stage` lacked. It lacked nothing — a closed six-value enum was already there, and
  the `compiler_typo` probe fails today and would have failed before. Coarse consequence is not the
  same defect as absent constraint. **No change**, and one believed constraint is now an observed one.

- **`assert_runtime_invariant_wired_v0` was not dormant — it was scoped away from its subjects.**
  It guards an empty set (no invariant declares `runtime_outcome`), which looked like waiting. The
  probe showed worse: the invariant declared `assert_projection.scope.applies_to: [PLATFORM]`, and
  `s1_extract.py:585` excludes scope-bearing invariants from a domain build's governance closure.
  Runtime business invariants are authored in **domains**. The check ran only where its subject could
  not exist and was absent from every build where one could.

- **And that scope declaration was a mislabel, not a boundary defect.** `scope.applies_to` is not an
  applicability axis — it is *the surface whose allowed-list the invariant carries*. Vocabulary
  `{PLATFORM, WORKLOAD}`; no `DOMAIN` value; 4 of 88 declare it, and **3 of those 4 carry an
  `allowed_*` list**. Excluding those from a domain build is correct — importing one asserts the
  platform's allow-list against domain artifacts. `INVARIANT_RUNTIME_INVARIANT_WIRED_V0` was the only
  scope-bearing invariant with no allow-list: it borrowed a surface-identity field to mean "platform
  concern". **One field deleted**, three lines. Imported closure 74 → 75.

**The probe that settles it is the same probe run twice.** An unwired `runtime_outcome` invariant
authored in a domain: before the fix the domain build fails on `ASSERT_PROTOCOL_SURFACE_CLOSED_V0`
only and `ASSERT_RUNTIME_INVARIANT_WIRED_V0` is silent; after, it fails on the wiring check. What
changed is not a check's strictness but whether it was there.

**The counterfactual was run too, and it is the reason closure admission was left alone.** The
general form of the fix — make scope select applicability rather than admission — applied to a
*genuine* surface-closure invariant produces `ASSERT_CT_SURFACE_CLOSED_V1`, 7 violations: the
platform's allow-list asserted against a domain that never declared it. The exclusion rule is
load-bearing. The defect was never in the rule.

The rulings, the measurement of record and all six probe transcripts are in
`software_governance/doc/ENFORCEMENT_AUTHORITY_RULING.md`; the read-only pass that preceded them is
`ENFORCEMENT_AUTHORITY_EVIDENCE.md`.

**`refusal_discharge` is implemented.** Twelve rules across P0 and P1 guarded the refusal register's
arrival and none guarded its consequence: a refusal was declared by the business, restated by the
change request, and carried unread through six phases into a composition where nothing performed it.
P7 now reads the seed, and five rules ask what carries each declared refusal out.

**All five rules are proved by a probe built to fail them.** No document in the corpus stated a
discharge, so each rule would have reported clean on its first run while checking nothing. Each probe
is CR-1's design with one row changed, and each fires exactly one rule. The last is the one worth
reading: `inadmissible_p7_discharge_completes.md` names an outcome the step really reports and routes
it to the ending that *completes* the act. Every cell of the row is accurate and the operation the
business refuses is performed anyway — the defect no rule reading the register alone can see.

**The event-emission guard is written, and it adds no register.** Nothing in the pipeline read an
`emit.` property: `multi_emission` gave an act the ability to announce several moments at one ending,
six acts then announced eight moments, and no rule looked at one. Two rules now do, joining
`artifact_properties` — which already states the site as `emit.<ending>` — to `execution_topology`,
which already types every node. An announcement must name an ending the act has, that ending must be
typed `EXIT_SUCCESS`, and the moment must be an identity the design declares. **Closes Open Issue
11b.**

**It does not close cr_03's half of Open Issue 21, and the reason is worth reading.** The guard
enforces cr_03's declared refusal in the strongest way available — no design can now express the
thing the business refuses — but cr_03's P7 still cannot *state* that discharge, because the refusal
is carried out by a rule of the design language rather than by a step of the catalog's own topology.
Confirmed: the fixture still reports `REFUSAL_UNACCOUNTED` on its one refusal. **That is a third
category neither register anticipated** — a refusal discharged by the governance surface — and it is
now the sharper form of the 21 ruling.

**CR-1's seven refusals are now stated, and they were always carried out.** The catalog discharges
every one of them in its topology and no document said so. The fixture's §18 states where, read from
the design's own rows. That is the register proving writable in practice, which was the open question
this change could not answer in advance.

**A design named one artifact of the seven it amended.** At `refusal_discharge`'s delivery,
`WF_P1`–`WF_P7` all changed — every phase workflow carries the full list of declared registers, so a
register added to the design language moves all of them — and only `WF_P7` was in the inventory. The
other two rows the design *did* name are a different fault: `CT_PURE_EVALUATE_RULES_V0` is produced
by no generator and has never changed, and `CC_JUDGE_AGAINST_SNAPSHOT_V0` was byte-identical then and
caught up later. **This is cr_03's failure class exactly** — nine admissible phases, and the design
does not determine its artifacts. Construction Completeness did not catch it either, because this
change renders nothing from a register and so gives it nothing to read. **The number is a moment**:
seven at delivery, eight in today's diff. Open Issue 22 carries the boundary and what each row is
worth.

**Two refusals in the corpus cannot be stated in either register.** cr_02's seed declares *"Retire a
work | Always."* — a refusal discharged by the act not existing, which has no act, step or outcome
and equally no owner and no "until". cr_03's is *"Announcing a moment | The act it names did not
complete"*, where an announcement attaches to an ending rather than to a step. Both fixtures were
left alone rather than filled with invented business facts. See Open Issue 21.

**The third refusal form is built: `refusal_governance_discharge`.** A declared refusal is carried
out in one of three places, and until now the design language knew only the first — a step of the
act. §20 states the third: the refusal is carried out by a rule of the pipeline, which makes the
declaration inadmissible before anything runs. **cr_03's fixture now accounts for its refusal** and
the whole refusal surface reads clean on it, which is the register proving writable.

**Two corrections to the ruling as first drafted, both checked rather than argued.** The cell holds a
**rule identifier, not a check kind** — a check kind is a mechanism bindable to any register with any
parameters, and `CT_PURE_EVALUATE_RULES_V0` says so itself: "it cannot tell you what is governed".
And the register carries a **Phase** column, because **15 rule identifiers are declared by more than
one phase** — every derived one, `REGISTER_MISSING` among them, is declared by all nine — so a rule
named without its phase names nine rules.

**The grounding rule is not built, and it cannot be built inside `transformation`.** The ruling
requires the cited rule to be *active in that phase's sealed rule set*, which means observing the
composition. Checks read observations gathered by fixed no-parameter operations, and **no existing
`si.` operation publishes the sealed rules** — I checked all five that answer without parameters
(`si.artifact.list`, `si.artifact.indexed`, `si.snapshot.topology`, `si.snapshot.summary`,
`si.capability.surface`). `transformation/design/sealed.py` already reads a rule set out of a
snapshot, but it does so with `si.artifact.show` and a per-workflow parameter, which the observation
pipeline cannot supply. **This needs a new `si.` operation in `snapshot_inspector`** — the path
`transformation/CLAUDE.md` names for exactly this case. Until it exists §20 is checked for form and
not for truth, which is the state the register was created to end. See Open Issue 25.

**§20 is grounded: `si.rule_set.list` publishes the sealed rules, and P7 resolves citations
against them.** The register no longer takes a citation on trust. `GOVERNING_RULE_NOT_IN_FORCE` looks
the cited rule up in the composition the design is **pinned** to — never a working tree — so the two
consequences the template warns about are now enforced rather than described: a design cannot
discharge a refusal by citing a rule its own change is adding, and a rule retired by a later change
stops discharging anything. **Closes Open Issue 25.**

**The inspector learned one fact and no vocabulary.** `si.rule_set.list` publishes which artifact
carries which rule identifiers. It says nothing about phases — which workflow is "phase 7" is the
design compiler's naming, and putting it in the inspection surface would move one repo's vocabulary
into another's. The phase mapping is declared with the P7 rule, read from `emit.SEALED_IN`, which
already owns it because it is the generator that writes those artifacts.

**A generated artifact had been edited by hand, and now a check catches the next one.**
`TI_SI_STORE_LIST_V0`'s catalog summary did not match what `author_transport_contracts.py` produces —
the newer wording had been written into the artifact and not into its generator, so regenerating
silently overwrote it. The doctrine says the generator wins and the artifact is stale; here the
artifact carried the better text, so the fix was to correct the **declaration**. `--check` now reports
agreement and writes nothing, naming a hand-edited contract `DRIFTED` and one declared by no operation
`ORPHANED`, and it is in the runbook beside `emit_rule_sets --check`.

**The check is proved by tampering, not by passing.** A test edits a real contract, asserts exit 1,
restores it; adds an orphan, asserts exit 1, removes it; and asserts the unknown-argument guard. A
check nobody has seen fail is a check nobody has seen — which is the standing architectural concern,
answered here for one generator.

**The differential's prior map is derived, and the last hand-kept copy in the harness is gone.**
It was a literal table — every corpus document, every prior it reads, by hand — and it was wrong
twice in one session. Two facts already existed and neither was read: **which phases** a document is
judged against is `PRIORS` in that phase's rule module, and **which dossier** supplies them is the
document's own `CR:` header. Adding a probe now needs nothing — cut it from a fixture and it is
judged against that fixture's priors because it says so in its own header. **Proved by the two new
deferral probes being picked up with no wiring at all**, 50 → 52 documents. The `"priors": True`
flag went with it, from all eight phase entries: a phase reads priors exactly when it declares some.

**Issue 23 is closed, both ways round.** No document in the corpus had ever populated the deferral
register, so a rule requiring its owner would have reported clean while checking nothing — and
nothing would have shown that a *correct* deferral is accepted either.
`admissible_p7_deferral_owned.md` moves CR-1's fourth refusal from discharged to deferred, with an
owner, and stays ADMISSIBLE; the negative blanks the owner. **A register whose only exercise is a
failure has been shown to refuse and not to work.**

**The governance surface was surveyed, and the survey drove a check rather than a cleanup.** All 58
`pgs_*` references in `software_governance/registry/` are classified in
`software_governance/doc/PGS_REFERENCE_SURVEY.md`. **Most are not broken**: 27 are live lookup keys
into `HANDLER_REGISTRY` — 85 handlers, all keyed by RI-0 module strings and implemented in PGC code —
so those invariants fire, and the name is the only legacy thing about them. Six were a field nothing
reads and were removed. Nine were a real contradiction and were ruled on.

**`standards/process/governance_closure.py` proves two relations and claims no more**: every compiler
handler is named by an invariant, and no layer is declared two ways. **It was written before the
defect was fixed**, reported the three conflicts on its first run, and went green only after the
ruling — which is the only reason it is known to detect anything.

**It corrected its own design and then my classification, in that order.** The first formulation asked
whether a layer *resolves*, and flagged six live, correct declarations: the compiler maps three
layers and everything else resolves to `None` by design. Absence is not the defect; **contradiction
is.** Then the remediation itself was wrong — deleting the three `STRUCTURE_REGISTRY_LOCATION_*`
artifacts compiled clean and turned three P3 cases red, because two of them carry
`reuse_visibility: substrate`, a live field `STRUCTURE_DISCOVERY_V0` does not carry. Only the
superseded fields were removed in the end. **An artifact is not a unit of liveness; a field is.**

**Construction acceptance covers two domains, and the second had never been checked.** It rendered
`book_library_mgmt` alone; `blockchain`'s 41 artifacts had no comparison against the designs that
determine them. Widening it cost one insight: **rendering reads registers and never judges
admissibility**, so a delivered dossier that would be refused at P7 today still determines exactly
what it determined when it was gated — no maintained fixtures required. **93/93 across two domains, 0
field differences.** The two supersession markers it first reported are written by standing an
artifact down rather than by rendering it, and are excluded with the reason stated.

**dev/6 closes here.** The release notes are `standards/process/notes/release-6.md`; `release.sh`
carries `RELEASE=6, NEXT=7`; every `VERSION` reads `6`. Preflight passes everything except the
commits themselves.

**dev/6's collateral is closed.** The branch's goal was migrating `blockchain/wallet` and that is
delivered. Five issues that accumulated around it were mechanical and are now resolved rather than
carried: the merit sentinel, the hand-kept dossier sequence, the dossier gitignore allowlist, the
`--root` flag that accepted a wrong root, and the wallet's 7/9. What remains open needs a ruling,
not an edit.

**Open Issue 8b is closed, and the missing record is recovered.** The wallet's 7/9 was a fixture
collision, not a product defect: the wallet suite registered `ada@example.test` and `bob@example.test`
— identity's own people — so when both suites ran into one data root, the criterion *"an unverified
person is refused a wallet"* tested someone identity's suite had already accepted, and no refusal
happened. `business_domains` commit `8f83aa4` gave the wallet suite its own `HOLDER`/`UNDECIDED`. It
was recorded as a data-root change, which is why the repair went unrecorded. **Confirmed by running
identity then wallet into one shared root: 15/15 then 9/9.** The `cr_06_wallet_acceptance` the last
handoff said to confirm against does not exist and never did.

## Changes Made

### The authority/concern finding — the session's substantive result

Documentation currency work surfaced a namespace mismatch that turned out to be an ontology defect.
`software_governance` documented itself as namespace `pgc::`; no artifact declares one. All declare
`fb.<concern>` — and `fb` is a **federation boundary**, defined by
`CONSTITUTION_FEDERATION_BOUNDARY_V0` as "a semantic sovereignty construct, not an implementation
packaging construct," carrying an anti-sprawl rule against speculative creation.

Applying that constitution's own test to all 26 declared boundaries, reading `applies_to_kinds` and
`enforcement.scope` as declared:

- **9 kind-mirrors** — `fb.actor`→`AC`, `fb.event`→`EV`, `fb.workflow`→`WF`. Boundary name *is* the
  artifact kind.
- **6 contest one jurisdiction** — `fb.authority`, `fb.capability_contracts` and `fb.execution`
  declare the *identical* `CC CS CT WF`; three more declare supersets.
- **4 contest the snapshot** — `cryptographic_trust`, `execution_placement`, `execution_scheduling`,
  `security_domain`, all `SNAPSHOT` + `ALL_ARTIFACTS`.
- **2 claim universal reach** — `fb.artifact` and `fb.vocabulary` enumerate all 16 kinds.
- **2 have no constituting act** — `fb.artifact`, `fb.surface_contract` declare no constitution.
- **3 exercise no jurisdiction** — `fb.federation`, `fb.lifecycle`, `fb.trace` declare no
  `applies_to_kinds` at all.

`fb.governance` initially looked like the one survivor. Applying an authority-independence test it
fails in the *opposite* direction: `CONSTITUTION_GOVERNANCE_V0` declares itself "the root authority
… supreme. All other constitutions derive authority from this document," with a tier table naming it
`Sovereign`. It is not a peer boundary — it is the platform authority, encoded as one boundary among
peers. **One modeling error explains all 26, with no exception.**

**PARKED.** The thread is written up and deliberately not scheduled. Two documents, both
**unratified**:

- `software_governance/doc/AUTHORITY_VS_CONCERN_RULING.md` — the single self-contained document:
  finding, the 26-row classification, the independence test, the ruling (five clauses), the
  enforcement obligation, and the ordered follow-on plan. Authority and concern are orthogonal; a
  boundary represents authority, never concern; a boundary must answer five questions from declared
  artifacts alone, plus authority independence. The two predicates are a *consequence* of the ruling,
  explicitly **not** a precondition for accepting it. Defers replacement encoding and migration.
- `software_governance/doc/GOVERNED_BY_AUTHORITY_CYCLE_FINDING.md` — kept **separate**, deliberately
  unruled. A literal two-node cycle exists:
  `fb.governance::CONSTITUTION_GOVERNANCE_V0 ⇄ fb.vocabulary::CONSTITUTION_VOCABULARY_V0`, both edges
  declared. Turns on whether `governed_by` means *authority derivation* (a defect) or *governed
  subject* (no contradiction). `governed_by` is pervasive — 46 artifacts name
  `CONSTITUTION_INVARIANTS_V0` — which argues for the narrower reading, but the surface does not say.

`standards/doc/spec/03_governance_ontology.md` updated — three surgical edits, no renumbering:
§2 gained a "Partitioning the universe" subsection defining **Authority / Concern / Federation /
Namespace** as four independent concepts; §6's existing rejection of "authority *level*" as an
ontology axis was **bounded, not reversed** (it governs element classification, which is a different
question from partitioning the universe); §11 gained two open questions.

**Nothing was migrated.** `pgc::`, `fb.*`, the `pgs_governance.registry.handlers.*` legacy handler
reference, and `software_governance/CLAUDE.md`'s `pgc::` assertions are all untouched by design —
they are downstream of a ruling that has not been accepted.

### Documentation currency pass — READMEs and ARCHITECTURE.md

- `protocol_compiler/README.md`, `protocol_runtime/README.md` — **rewritten.** Both were RI-0
  templates titled `pgs_compiler` / pointing at `bachipeachy/pgs_workspace`, with `pgs_*` layer
  tables and CLI examples using flags that no longer exist. Corrected against the code: real entry
  points, `TI_` added to the compiler's artifact kinds (it recognizes 10, the README listed 9), and
  the runtime's four subcommands (`run`, `boot`, `examine`, `behavior-logic` — `boot` was absent
  despite warm reboot being the repo's distinguishing act).
- `software_governance/README.md` — **rewritten** to peer shape: what it is → where it fits → what
  it holds → what binds a contributor → how completeness is verified. Written namespace-neutral so
  it does not front-run the ruling; glosses `fb` as federation boundary with a pointer to the
  constitution.
- `transformation/README.md` — CLI section covered 9 of 14 commands; `phase project/meta/emit`,
  `baseline show/approve` added. "Validation is pinned" showed only half of rebaselining. The
  runbook pointer (private `standards/`) was replaced by inlining the two loops.
- All 9 `ARCHITECTURE.md` — the `**Release 5.** … frozen for this release` banner removed
  (stale at VERSION 8, and status metadata in a deliverable doc). `protocol_compiler` gained
  `tokenized` in §6 (the runtime's actual input, omitted) and `governance/` in §7;
  `protocol_runtime` gained `runtime/cli.py`; `snapshot_inspector` gained `registry/`.
- `protocol_transport/README.md` — title `# transport` → `# protocol_transport`.

### `.github` promoted into the composition

`SNAPSHOT_ASSEMBLY_CONTRACT.md` and `requirements-domains.txt` moved from `standards/` (staying
private) to `.github/` (public), because five source-level citations in `snapshot_assembler`,
`protocol_runtime` and `business_domains` pointed at a repo public readers cannot open.
`release.sh` `REPOS` gained `.github` — its comment claiming `.github` "is deliberately absent: it
is the org profile page" was false once it carried composition surface. `.github/VERSION` created.
`RELEASE`/`NEXT` bumped 7/8 → 8/9.

### `software_governance` — enforcement authority (dev/7)

- `registry/schema/SCHEMA_INVARIANT_V0.json` — `assert_projection.enforcement.phase` property
  deleted. With `additionalProperties: false` already in place, re-declaring `phase` is now a schema
  failure rather than an unread duplicate.
- 14 invariants across `actor`, `artifact` (×2), `conformance` (×2), `cryptographic_trust`,
  `execution_placement`, `execution_scheduling`, `governance`, `security_domain`, `structure`,
  `surface_contract`, `transport`, `vocabulary` — the `phase:` line removed. Nothing else in the
  machine block touched, and key order preserved.
- `registry/execution/invariants/INVARIANT_RUNTIME_INVARIANT_WIRED_V0.md` — `scope.applies_to:
  [PLATFORM]` removed (3 lines). It carried no allow-list, so the field was a mislabel; removing it
  admits the invariant into every domain closure via `applies_to_kinds: [WF, CC]`.
- `doc/ENFORCEMENT_AUTHORITY_EVIDENCE.md` — new. The read-only measurement pass: which mechanisms
  read which fields, taken before anything changed.
- `doc/ENFORCEMENT_AUTHORITY_RULING.md` — new. Four rulings, the measurement of record, and the six
  probe transcripts (A/B schema, C platform wiring, D domain wiring before/after, E admission census,
  F the counterfactual).

No compiler, assembler or runtime code changed. Every domain was recompiled because the platform
governance closure digest moved — which the assembler's provenance check caught and refused before
the recompile, exactly as designed.

### `standards` + `conformance_workloads` — the governance chain, and the price of closing it

- `standards/process/governance_chain_closure.py` — new. Proves DECLARE, RESOLVE and PARITY by name,
  wherever an invariant may be authored: every invariant authored outside the platform is named by a
  constitution rule, and every build whose `artifact_types` admits `INVARIANT`/`CONSTITUTION` can
  reach the two chain invariants. Imports `_DOMAIN_INSTANTIATED` from `s1_extract` rather than
  restating it. **In the runbook.**
- `conformance_workloads/workloads/collatz/registry/structures/STRUCTURE_BUILD_WORKLOAD_CONFIG_V0.md`
  — `INVARIANT` removed from `artifact_types`.
- `…/registry/invariants/INVARIANT_CT_SURFACE_CLOSED_WORKLOAD_V0.md` — deleted. It was the only
  invariant authored outside the platform and the only one no constitution declared. Its enforcement
  is genuinely lost; see issue 38.

**The check was built before either was decided, and it was red on arrival.** That was the point: it
named the two ways to green and both were rulings. Probe H — withdrawing the authorship — is the one
that was taken.

### `transformation` — the corpus pass

- `scripts/testbed/corpus{,_p1..p8}/` — **31 new negative documents**, P0–P8, each grouped by a kind
  of authoring failure rather than one rule per file, and each naming in the suite the rules it must
  fire. Cut from the cr_01 fixtures except two: a P8 case from cr_02 (cr_01's P7 declares no EXTEND
  row, and `AMENDED_ARTIFACT_UNPLACED` is gated on one).
- `scripts/testbed/build_payloads.py`, `scripts/testbed/e2e_phases_test.py` — 31 payloads and 31
  cases. e2e 52 → 83, differential 52 → 83.
- `testbed/phases/test_payloads/` — regenerated, `--check` agrees.
- `transformation/design/template_reader.py` — `business_language_columns` resolves a scoped column
  name to the header it names, and raises on one that matches nothing. Twenty-five declarations
  across four phases had been emitting a rule that could not fire.
- `transformation/design/checks.py` — `TABLE_HAS_COLUMNS` consumes a match once, exact before prefix.
- `registry/design/workflows/WF_P{3,5,6,7}_*.md` — regenerated by `emit_rule_sets.py` after the
  template fix. Rule *declarations* unchanged; the emitted params now name real headers.
- `doc/FEATURE_LEVEL_CLOSEOUT.md` — updated: the coverage item is closed, and the ten remaining rules
  are listed with why each is not a document.

### `transformation` — the feature-level close-out

- `doc/FEATURE_LEVEL_CLOSEOUT.md` — new. What remains before the Design and Construction Compilers
  are done *at this feature level*, and the measurement behind it: 820 rules, 229 distinct ids, 63
  ever observed to fire, against 40 corpus documents of which 20 exercise P7 alone. The conclusion is
  that the open work is **corpus, not rules** — see the note in Architectural Concerns.

### `transformation` — the design language, the rules, and the probes

- `templates/p7_design_intent_template_v0.md` — §18 `refusal_discharge` (Operation, Refused When,
  Act, Step, Outcome, Source Finding) and §19 `refusal_deferrals` (Operation, Refused When, Deferred
  To, Until, Source Finding), both optional. Integer section numbers, per Open Issue 14.
- `transformation/design/checks.py` — two kinds, 53 → 55. `DISCHARGE_GROUNDED_IN_TOPOLOGY` resolves
  the act and step against `execution_topology` and requires the outcome to be one that step reports;
  `DISCHARGE_OUTCOME_REFUSES` reads the node the outcome routes to and requires it typed `EXIT`, not
  `EXIT_SUCCESS`. Both read the design alone; neither observes the composition.
  `PRIOR_ROWS_PRESENT_BY_KEY` gains an optional `registers` list defaulting to the single register it
  reads today. **Every existing rule using it is unchanged, and its finding text is unchanged too** —
  the default path still reports "restated nowhere here", because a widened kind must not reword a
  finding it did not change.
- `transformation/design/p7_design_intent/rules.py` — `PRIORS = ("p5", "p6", "p0")` and five rules:
  `REFUSAL_UNACCOUNTED` (coverage across both registers), `DISCHARGE_UNDECLARED_REFUSAL` and
  `DEFERRAL_UNDECLARED_REFUSAL` (confinement to the seed), `DISCHARGE_NOT_IN_TOPOLOGY` and
  `DISCHARGE_DOES_NOT_REFUSE` (grounding). P7 goes 152 → **167**.
- `scripts/testbed/corpus_p7/` — five new probes, one per rule.
- `scripts/testbed/fixture_dossiers/cr_01_catalog/p7_…_v0.md` and the five existing `corpus_p7`
  probes — §18 and §19 appended; §18 states CR-1's seven refusals across fifteen rows, because
  *"Any catalog operation | The staff member performing it is not authorized."* is discharged
  once per act and there are nine.
- `scripts/testbed/differential.py` — `p0` added to all six P7 prior mappings; the five probes
  registered. 37 → 42 documents.
- `scripts/testbed/e2e_phases_test.py` — five cases added, P7's asserted rule count 152 → 167.
  37 → 42 cases.
- `testbed/phases/test_payloads/` — five new payloads; the six existing P7 payloads re-cut from
  their source documents and given `p0`. **They carried `p5` and `p6` only, and a declared prior that
  is not supplied reports the handoff unchecked rather than passing quietly.**
- `registry/design/workflows/WF_P1…WF_P7` — re-emitted by `emit_rule_sets`. None written by hand.
- `dossiers/refusal_discharge/p7_…_v0.md`, `p8_…_v0.md` — **Gate 1 and Gate 2 closed** against
  `6e1e571dbbb8…`, the composition `baseline.json` pins.

### `transformation` — the event-emission guard

- `transformation/design/checks.py` — `EMISSION_GROUNDED_IN_ENDING`, 55 → 56 kinds. Site and type are
  one traversal of one topology row and are reported once: a property naming an ending the act does
  not have has no type to check, so splitting them would report one wrong row twice. The completing
  type is read from the topology, never from the ending's name.
  `CELL_RESOLVES_IN_REGISTER` gains `only_when_prefix`, because an emission is `emit.<ending>` — one
  property per ending, so there is no single value an equality gate could select.
- `transformation/design/p7_design_intent/rules.py` — `EMISSION_NOT_FROM_COMPLETING_ENDING` and
  `EMITTED_EVENT_UNDECLARED`. P7 goes 167 → **169**; the composition goes 808 → 810 rules.
- `scripts/testbed/corpus_p7/` — three probes: an ending the act does not declare, an ending typed
  `EXIT` rather than `EXIT_SUCCESS`, and a moment nothing declares. Three rather than two because the
  guard makes three claims.
- `scripts/testbed/differential.py`, `scripts/testbed/e2e_phases_test.py`,
  `testbed/phases/test_payloads/` — 42 → **45** documents and cases.
- **Verified clean on cr_03**, the only design in the corpus that announces anything.

### `transformation` — the governance-surface discharge

- `templates/p7_design_intent_template_v0.md` — §20 `refusal_governance_discharge`
  (Operation, Refused When, Phase, Governing Rule, Source Finding), optional. Its prose states the
  two things an author meets late otherwise: **a design cannot discharge a refusal by citing a rule
  its own change is adding**, and **resolution is not coverage** — that the cited rule exists is
  checkable, that it refuses the stated condition is what Gate 1 is reading for.
- `transformation/design/p7_design_intent/rules.py` — `REFUSAL_UNACCOUNTED` now spans all three
  registers, plus `GOVERNANCE_DISCHARGE_UNDECLARED_REFUSAL` (confinement to the seed),
  `GOVERNING_RULE_UNNAMED`, and `GOVERNING_RULE_PHASE_MALFORMED` (`^p[0-8]$` — the phase spelling,
  never a stage number). P7 goes 169 → **177**; the composition 810 → **818**.
- `scripts/testbed/fixture_dossiers/cr_03_catalog/p7_…_v0.md` — §18 and §19 declared empty, §20
  citing `p7 | EMISSION_NOT_FROM_COMPLETING_ENDING`. **Its refusal surface is clean.**
- `scripts/testbed/corpus_p7/`, `differential.py`, `e2e_phases_test.py`, `test_payloads/` — three
  more probes, built from cr_03 because it is the only design in the corpus that announces anything.
  45 → **48** documents and cases.

### `snapshot_inspector` — one new operation

- `inspector/reads/rule_set_list.py` — **NEW.** Publishes every artifact carrying a sealed rule set
  and the identifiers it declares. Identifiers rather than whole rules: what a rule *is* is already
  readable through `si.artifact.show`, and repeating it would be a second copy that can drift. The
  rule set is searched for rather than addressed by path, because which node carries it is the
  workflow's business.
- `scripts/author_transport_contracts.py` — the spec for `si.rule_set.list`, and a correction to
  `si.store.list`'s summary. **The TI/TE pair is generated, never hand-written** — the first draft of
  this change wrote them by hand and was discarded when the generator was found.
- `inspector/registry.py` — the implementation import. Metadata stays in the artifacts.
- `scripts/author_transport_contracts.py` — **`--check`**, mirroring `emit_rule_sets --check`:
  reports `DRIFTED` / `ORPHANED`, writes nothing, exits 1. An unrecognised argument exits 2 rather
  than falling through to the default, which writes.
- `scripts/testbed/test_inspector.py` — the fixture workflow gains a sealed rule set with a repeated
  identifier; six checks on `si.rule_set.list`, including that a carrier-less artifact is `NOT_FOUND`
  rather than an error. Plus five that prove `--check` by tampering. 108 → **121**.

### `transformation` — grounding the citation

- `transformation/design/checks.py` — `GOVERNING_RULE_IN_SEALED_SET`, 56 → **57** kinds. It resolves
  a phase and a rule identifier against the observation, and deliberately reports **only** that the
  rule is or is not in force: that the rule *covers* the stated refusal is not checkable and is
  Gate 1's to judge.
- `transformation/design/p7_design_intent/rules.py` — `si.rule_set.list` added to `OBSERVATIONS`,
  and `GOVERNING_RULE_NOT_IN_FORCE`. P7 goes 177 → **178**, and `CC_JUDGE_AGAINST_SNAPSHOT_V0` gains
  a seventh rule on its own: the contract's observation pipeline is derived, so a new observation
  arrives there without being declared twice.
- Two more probes — a rule nothing declares, and the right rule cited at the wrong phase. 48 → **50**
  documents and cases.

### `standards` — the runbook

- `process/RUNBOOK.md` — `author_transport_contracts.py --check` added to the Check block beside
  `emit_rule_sets --check`, with its expected result and the rule that matters: **a `DRIFTED` line
  means fix the declaration, never the artifact.**

### `transformation` — the derived prior map and the deferral owner

- `scripts/testbed/differential.py` — `PRIORS_BY_DOCUMENT` **deleted**. Priors are derived from the
  phase's `PRIORS` and the document's `CR:` header, with dossiers indexed by the `CR:` their own seed
  declares — not by directory name, because `dossiers/founding_design_bootstrap` declares
  `new_subdomain`. A document with no `CR:` header, or one no dossier claims, is a hard failure
  rather than an unchecked handoff. `"priors": True` removed from all eight entries.
- `transformation/design/p7_design_intent/rules.py` — `DEFERRAL_OWNER_UNNAMED`. P7 178 → **179**,
  the composition 819 → **820**.
- `scripts/testbed/corpus_p7/` — `admissible_p7_deferral_owned.md` and
  `inadmissible_p7_deferral_unowned.md`, plus their e2e cases. 50 → **52**.

### The dev/6 close-out

- `scripts/testbed/construction_acceptance.py` — generalised over **domains**: `book_library_mgmt`
  from maintained fixtures, `blockchain` from its delivered dossiers. `superseded_by` is excluded
  from comparison, because it is written when an artifact is stood down rather than rendered; the
  rest of the machine block is still compared, so a superseded artifact whose *content* drifted is
  still caught. 52 → **93 artifacts**.
- `standards/process/release.sh` — `RELEASE=6`, `NEXT=7`. Two lines, which is all the script's own
  rule permits. `REPOS` needed no change: all ten exist, and `.github` is deliberately absent.
- Ten `VERSION` files, `5` → `6`. `release.sh` only checks them; bumping is a prep step it names but
  does not perform.
- `standards/process/notes/release-6.md` — the release notes, read by convention at the cut.
- Five READMEs corrected — the transformation two-compiler split, `software_governance`'s retired
  `FB_*` layout and its false claim that the toolchain is RI-0, `blockchain`'s missing `wallet`
  subdomain, the inspector's 18th operation, and the assembler's one-domain framing.
- **A tenth paper was written, and it lives outside this workspace.**
  `~/omnibachi-site/content/papers/pgc_design_and_construction_compilers_v0.md` — *The Design and
  Construction Compilers*, 5.9k words, weight 75, between the closed-loop architecture paper it
  develops and the realization companion. Its thesis is this workspace's own result: **success at one
  semantic boundary does not imply success at the next**, evidenced by cr_03. It carries four
  sections that exist in no other paper — a rule that has never failed has been shown nothing; a
  design language invalidates its own corpus as it grows; three sites at which a refusal is
  discharged; and the architectural properties stated so they can be checked. **It is untracked in
  `omnibachi-site` and that repo is outside the ten this release covers**, so `release.sh` preflight
  will never mention it. Two of its references still lack DOIs, and it carries no `date:` field.
- Four spent documents removed: two delivered plans, the completed branch migration, and this
  session's own review once its findings were fixed or recorded here.

### `software_governance` + `standards` — the survey, the check, and the ruling

- `software_governance/doc/PGS_REFERENCE_SURVEY.md` — **NEW.** All 58 `pgs_*` references in five
  classes, machine field vs prose, with the disposition applied to each and one classification
  corrected in place.
- `INVARIANT_NO_UNDECLARED_BEHAVIOR_SURFACE_V0` — `extensions.enforcement_locations` **removed**.
  Nothing read it; it named six files that do not exist, inside a machine block, so it read as
  binding while enforcing nothing. Second declared-but-unread field in two sessions.
- `STRUCTURE_REGISTRY_LOCATION_{GOVERNANCE,REUSABLE_TRANSFORMS,REUSABLE_SIDE_EFFECTS}_V0` —
  `registry_module` and `module_path_pattern` removed; `layer_code`, `reuse_visibility`,
  `structure_scope` and `output_configuration` kept. `STRUCTURE_DISCOVERY_V0` says of itself that it
  replaces "fragmented registry location and layer authority discovery definitions"; the supersession
  was declared and the superseded fields were left in place, contradicting it.
- `standards/process/governance_closure.py` — **NEW.** Two relations, stdlib, reads artifacts as
  authored so it runs before a build. The third relation an earlier draft proposed —
  "every declared handler resolves" — was **dropped as vacuous**: it is already `E702_UNKNOWN_ASSERT`
  at every build, and measured beforehand, zero invariants sit in the gap.
- `standards/process/RUNBOOK.md` — `governance_closure.py` added to the Check block.

### `transformation` — the collateral, closed

- `transformation/design/merit.py:98` — `| NONE IDENTIFIED |` no longer counts as an open question.
  It reads `is_sentinel` from `checks.py` rather than carrying a second spelling of emptiness.
  **Six asserted figures moved** and were corrected in `e2e_phases_test.py`: P0 cases 01/02 and P1
  case 06 go 4/5 → 5/5, P0 cases 03/04 and P1 case 07 go 3/5 → 4/5. Every one was a document marked
  down for being complete. Closes Open Issue 2c.
- `transformation/cli.py:731` — `tc construction emit --root` refuses a root carrying no
  `registry/structures/STRUCTURE_BUILD_*_CONFIG_V*.md`, **except when this emission is the one
  founding it**, where its absence is the point. Verified: the repository root is now refused with
  the reason, the domain root proceeds. Closes Open Issue 18.
- `scripts/testbed/construction_acceptance.py:48` — the dossier sequence is derived from
  `cr_NN_<subject>` directory names, ordered by the number. The literal list is gone, and appending
  a delivered dossier is no longer a step anyone can miss. 52/52 unchanged. Closes Open Issue 19.
- `.gitignore` — the dossier exclusion is no longer an allowlist of names. Authored dossiers are
  `dossiers/<subject>/` and hold documents; generated ones are `dossiers/<domain>/<subdomain>/` and
  hold a directory, so `/dossiers/*/*/` ignores everything generated and nothing authored. Verified
  both ways with `git check-ignore`. **A new authored dossier is now tracked from the moment it
  exists.** Closes Open Issue 20.
- `scripts/emit_rule_sets.py:18` — an unrecognised argument prints the usage and exits 2 instead of
  falling through to the default, which writes. `--help` used to re-emit every workflow and report
  it as work done.

## Build & Test Status

**PASSING** — preflight passed at the release-8 cut, and again after the cycle-9 bump:

```
clean rebuild + assemble + composition conformance   ok
snapshot_id   7b6f26994f80b858d811e241ac0c80725d85de7b3e4e6936f37a9447ea9ba3f0
conformance   composition PASSED (5 rules over 398 artifacts)
```

Preflight for release 9 now reports only the two things a freshly-opened cycle should: no
`notes/release-9.md` yet, and the uncommitted `VERSION` bumps. `.github` passes its per-repo gates
alongside the other ten.

The suite below was run at the previous handoff and is unaffected by a documentation pass.

```
governance_closure          PASSED — 85 handlers declared, 11 layers each declared once
emit_rule_sets --check      agrees
author_transport_contracts  --check agrees — 36 contracts for 18 operations
meta_test                   PASSED — 820 rules across 9 phases / 57 check kinds
differential                PASSED — 52 documents, both paths agree
e2e_phases_test             PASSED — 52 cases
projection_test             PASSED
construction_acceptance     PASSED — 93/93 artifacts across 2 domains, 0 differences
implementation_closure      PASSED — 27 transforms
pgc_env_check               PASSED
inspector                   PASSED — 121/121
governance_chain_closure    PASSED — 0 invariants authored outside the platform, 6 domain build
                            configs, none authoring a chain kind
snapshot                    839efc635bef… · 7 domains · conformance PASSED (5 rules over 398)
                            round-trip verify OK after a clean rebuild of platform + 6 domains
                            398, not 399 — the workload's one invariant was withdrawn

collatz          SUCCESS       ai_governance   SUCCESS (both workflows)
catalog          23/23         cr02            21/21
identity         15/15 (2 not exercised)       wallet   9/9 (1 not exercised)
                 both run into ONE shared data root, identity first — the arrangement 8b turned on

probes           14 negative probes fire, one rule each; 1 admissible probe proves a correct
                 deferral is accepted — none fires on a document that should be clean
dev/7 probes     6 authored, built, observed to fail, reverted — A/B schema conformance,
                 C platform wiring, D domain wiring (silent before the fix, fires after),
                 E admission census 72 admitted / 15 excluded, F the counterfactual
rule coverage    222/229 rule ids observed to fire (96.9%), was 63/229 (27.5%)
                 P0–P5 and P8 complete · P6 21/22 · P7 74/80
```

**Every delivered dossier now reads INADMISSIBLE at P7** — catalog cr_01–03, identity cr_01–03,
wallet cr_04, `declared_reach` — for `REGISTER_MISSING` on the two new registers plus their own
unaccounted refusals. Per Open Issue 1 that red is correct and no original was edited.
`refusal_discharge`'s own dossier is red for the same reason, which its P7 predicted in writing.

## Open Forks — the single register

| fork | kind | blocks | state |
|---|---|---|---|
| `generated_artifacts` | authority | — | **DELIVERED**, and used |
| `register_coverage` | design language | — | **CLOSED UNBUILT** by ruling — two of three instances closed by work done since, the third is a different question |
| `rule_effectivity` | applicability | nothing; compounds | designed, P0–P6 admissible. P7 authorable |
| `multi_emission` | **platform** capability — 4 repos | — | **DELIVERED**, and used |
| `multi_structure_binding` | **platform** capability | — | **DELIVERED** |
| `declared_reach` | **transformation** — design + build | — | **DELIVERED** |
| `cr_04_wallet` | **blockchain** — the wallet function, entire | — | **DELIVERED** — wallet validation 9/9 |
| `cr_03_catalog` | **book_library_mgmt** — six acts announcing nothing | — | **DELIVERED** |
| `refusal_discharge` | **transformation** — design + build | — | **IMPLEMENTED**, uncommitted. Both gates closed. Four rulings open — Open Issues 21–24 |
| `select_operation` | **platform** — retrospective record | — | **COMPLETE at P6** |

## Open Issues

0. **PARKED — the authority/concern ruling is unratified and the thread is not scheduled.**
   `software_governance/doc/AUTHORITY_VS_CONCERN_RULING.md` is self-contained: finding, evidence,
   ruling, and ordered plan. When resumed, the sequence is
   ruling → canonical representation → enforcement predicates → migration. **Representation precedes
   predicates** — a predicate needs a declared field to test, and today every candidate reads the
   collapsed identifier. Blast radius is recorded in the ruling: 1,407 `fb.` references across 532
   files in six repos, `HANDLER_REGISTRY` constants in scope, 16 pinned baselines owing re-pin and
   re-approval. Do not touch `pgc::` or `fb.*`.

0b. **`governed_by` has two possible meanings and the surface declares neither.**
   `GOVERNED_BY_AUTHORITY_CYCLE_FINDING.md`. Rule this separately from the namespace question — it
   may be a different ontology problem.

0c. **`CLAUDE.md` is gitignored in every repo** (`.gitignore:13`). Every `CLAUDE.md` correction made
   this session — `protocol_compiler`'s stale "migration in progress" block, `transformation`'s
   P0–P7 phase span, `standards`' `.github` exclusion claim, the `pgc_env_check.py` and `pgc_compile`
   references — is **local-only and will not survive a clone.** Decide whether that is intended.

0d. **`software_governance/CLAUDE.md` still asserts `pgc::` in four places** while its README is now
   namespace-neutral. Deliberate: the docs should not lead the ruling. Revisit after ratification.

1. **A fixture is not evidence.** `book_library_mgmt` cr_01/cr_02 stay at their approved text and
   read INADMISSIBLE at P0; that red is correct. The testbed reads maintained copies at
   `transformation/scripts/testbed/fixture_dossiers/`. Never edit the originals.

2. **`blockchain` cr_01/02/03 are red and that is correct.** Findings from rules written after their
   approval. **Do not re-migrate them.** The approved originals were not given §17.

2b. **A business change request amended a platform capability, recorded rather than undone.**
   `select_operation` is the record; `AMENDED_ARTIFACT_NOT_AUTHORABLE` stops the next one.

2c. **RESOLVED — the figure of merit no longer counts a declared emptiness as an open question.**
   `merit.py` reads `is_sentinel` from `checks.py`. It moved six asserted figures in the e2e suite,
   which is why it had been deferred twice; all six were documents marked down for being complete,
   and all six were corrected upward.

6. **The composition is `d5d23ec9213e…`.** **Two counts exist and past handoffs have mixed them:**
   `tc baseline show --snapshot` counts the pin; the assembler's conformance line counts 398 over a
   wider set. Quote the pin. Left open deliberately — they count different things correctly, and
   collapsing them would lose one of the two. `refusal_discharge` is pinned to `6e1e571d…`, the composition it was
   designed against, which is correct: a dossier is judged against the composition it was designed
   against, never the one it produced.

7. **A design can add and cannot deliberately remove.** Every future replacement hits this.

8b. **RESOLVED — the wallet's 7/9 was a fixture collision and the repair is now on the record.**
   The wallet suite used identity's own people, so a shared data root left the unverified-person
   criterion testing someone already accepted. `business_domains` `8f83aa4` gave the suite its own
   `HOLDER`/`UNDECIDED`; its message describes the data-root change and not the criterion it fixed.
   **`cr_06_wallet_acceptance` does not exist** — the last handoff sent the next session to a
   dossier that was never written.

9. **`TOUCHED_SUBDOMAIN_AUTHORS_NOTHING` is gated to NEW_SUBDOMAIN and EXTEND_SUBDOMAIN only.**

10. **`ai_governance` has no dossier**, deliberately.

11e. **The dossier lifecycle vocabulary has no state for a governance change.** The three P6-terminal
   dossiers stay `DRAFT` forever. **It has no state for a closed gate either** — cr_03 and
   `refusal_discharge` both carry `**Status:** DRAFT` and `PENDING GATE N APPROVAL` in Pipeline
   Provenance with both gates closed. Following the precedent keeps the two comparable; a ruling
   would make either honest.

11d. **Identity assignment is ungoverned for a governance artifact.**

13. **The design language cannot state a dotted literal.** `BINDING_SOURCE_WELL_FORMED` admits
   `inputs.<field>`, `payload.<field>`, `results.<step>.<field>`, a bracketed literal, or a bare
   identifier. An operation identity is `si.store.list`, so a design cannot bind one. **The next
   design that must state an operation identity will stop here.**

14. **A P7 section number must be an integer.** `4b` is a hard parse failure in the document reader.
   §18 and §19 went at the end for that reason, which is right for them and will be wrong for
   something eventually.

15. **RESOLVED — the refusal register is discharged.** Twelve rules guarded its arrival and none its
   consequence; five rules now guard the consequence, and each is proved by a probe. What remains is
   Open Issue 21: two refusals in the corpus that neither register can express.

16. **Two in-flight dossiers can each own one artifact, and the guard cannot see it.**
   `tc construction check --snapshot` refuses an amendment that narrows what it replaces, but only
   against the dossier's own baseline. `THE_SHAPE_OF_A_CHANGE_V0` §8 rules when a dossier may be
   deleted rather than superseded.

17. **DEFERRED, as its own identity change — not unfinished wallet work.**
   `TI_ACCEPT_ACTOR_V0` and `TI_REJECT_ACTOR_V0` take `states_admitting_a_decision` and
   `admitted_outcomes` from the caller's payload, so a caller decides what the system admits. The
   wallet's equivalent was corrected to a design-fixed literal during the migration; identity's was
   not, so the migration closed with one half corrected.

   **It is a new CR against identity, and must not reopen `cr_04_wallet`.** `transformation/CLAUDE.md`
   is explicit: a subject touching an artifact a *delivered* dossier declares is a new CR, because
   "a delivered dossier is never edited". Those TIs belong to `cr_01`–`cr_03_identity`, all delivered.
   Framing this as wallet collateral would point at re-pinning a dossier and eroding its record.

18. **RESOLVED — `tc construction emit --root` refuses a root that is not a domain root.** It asks
   for the build config the compiler discovers a domain by, and exempts the emission that founds one,
   because there the config's absence is the point.

19. **RESOLVED — the dossier sequence is derived from the `cr_NN_` names, not restated beside
   them.** A business-domain dossier is numbered and the number *is* the sequence, so nothing has to
   be appended by hand. An unnumbered directory is not swept in.

20. **RESOLVED — the dossier gitignore is a structural rule, not an allowlist.** Authored and
   generated dossiers differ in shape — documents versus a nested directory — so `/dossiers/*/*/`
   separates them. A new authored dossier is tracked from the moment it exists, which is what
   `declared_reach` was not.

21. **RULED, and two of three forms are built.** A declared refusal is carried out in one of three
   places, and each is its own register rather than one stretched to mean three things:

   | form | carried out by | stated in | built |
   |---|---|---|---|
   | runtime discharge | a step of the act, routing to a refusing ending | §18 `refusal_discharge` | **yes** |
   | prohibition by absence | there being no such act at all | — | **no** |
   | governance-surface discharge | a rule of the pipeline refusing the declaration | §20 `refusal_governance_discharge` | **yes, ungrounded** — Open Issue 25 |

   **Prohibition by absence needs a stable declared operation identity, going forward only.** cr_02's
   *"Retire a work | Always."* supplies none — verified: it appears in its p0, p1 and p4 as business
   prose with no FQDN and nothing resolvable — so its fixture stays historical and unbackfilled.
   **It will read INADMISSIBLE at P7 permanently, and that red is expected rather than a defect.**
   Nothing asserts it today; it is not in the P7 corpus.

22. **A design named one artifact of the seven it amended.** **The count is a moment, not a
   standing fact, and the moment is `refusal_discharge`'s delivery** — measure it later and it moves,
   which is itself the point. Verified rather than asserted:

   - **At delivery, seven generated artifacts changed: `WF_P1`–`WF_P7`.** Those seven carry the full
     list of declared registers, so every register added to the design language moves all of them —
     six for no reason a reader of the design would predict. `WF_P0` and `WF_P8` do not carry the
     list and were untouched, which is why the number is seven and not nine. **Only `WF_P7` was in
     the inventory.**
   - **`CT_PURE_EVALUATE_RULES_V0` is declared EXTEND and did not change, then or since.** It
     enumerates no check kinds — four were added this session and it is untouched — and
     `emit_rule_sets` produces no CT artifact. **Its EXTEND row and its generation-provenance row are
     both wrong**, and the provenance row is the worse of the two: it names a generator that has
     never produced that artifact.
   - **`CC_JUDGE_AGAINST_SNAPSHOT_V0` is declared EXTEND, was byte-identical at delivery, and changed
     later** — this session, when a new observation added a step to its pipeline. `emit_rule_sets`
     does produce it and the callable reference is correct. That row was **premature, not wrong**.

   **The current uncommitted diff carries eight changed generated artifacts, not seven** — the same
   seven plus the CC, which caught up. A reader who counts today and a reader who counted at delivery
   get different numbers from the same defect, and neither is misreading.

   **Wants a ruling**: correct the record, or write a rule that refuses a design whose amendment set
   is incomplete. It is a delivered dossier, so it is not edited on a whim.

23. **RESOLVED — a deferral must name its owner.** `DEFERRAL_OWNER_UNNAMED`, the same
   `CELL_NOT_EMPTY` the governance discharge uses for its rule; the emptiness sentinel is excluded
   for free, because a declared `| NONE IDENTIFIED |` is an answer and not a row. **Proved both
   ways** — a correct deferral is accepted, a blank owner is refused. It sat outside the five rules
   Gate 2 froze for `refusal_discharge`, and once five more had been added beyond that mandate,
   leaving it was arbitrary rather than principled.

24. **A rule count in a mandate is a guess, because nothing computes it.** `refusal_discharge`
   projected ~157 rules for P7 and delivered 167; P7 now stands at **179**. The gap was derived
   rules — each register the template gains brings five with it — and no register author sees that
   number before emitting. The figure in a mandate should either be computed or not stated.

25. **RESOLVED — §20 is grounded.** `si.rule_set.list` publishes every artifact carrying a sealed
   rule set and the identifiers it declares; `GOVERNING_RULE_NOT_IN_FORCE` resolves a cited rule
   against it, in the composition the design is pinned to. The inspector learned a snapshot fact and
   no phase vocabulary; the phase→workflow mapping is declared with the P7 rule, read from
   `emit.SEALED_IN` rather than copied.

   **What it deliberately does not check.** That the cited rule *exists and is in force* is
   checkable. That it *refuses the condition stated beside it* is not, and no rule can check it —
   that judgment is Gate 1's, and the register's own prose says so. §20 is therefore the weakest of
   the three forms and is honest about it.

26. **RESOLVED — the transport contracts have an agreement check.**
   `author_transport_contracts.py --check` reports drift and orphans, writes nothing, and is in the
   runbook. **It is proved by tampering rather than by passing**, which is the only proof an
   invariant of this shape can have. The originating defect — a hand-improved
   `TI_SI_STORE_LIST_V0` summary that regenerating overwrote — is fixed in the declaration.

   **Two generators still have no check.** `author_transport_contracts.py` and `emit_rule_sets.py`
   now do; nothing equivalent exists for the domain artifacts `tc construction emit` renders, where
   `construction_acceptance` compares against designs rather than against the renderer.

27. **NEW — three classes of the `pgs_*` survey are deliberately unaddressed, and that is a decision
   rather than a backlog.** Full detail in `software_governance/doc/PGS_REFERENCE_SURVEY.md`.

   - **Class A — 27 live keys.** `HANDLER_REGISTRY` entries and schema `$id`s carrying RI-0 names.
     Nothing is broken. A rename must move the compiler, the registry and the artifacts together, and
     it changes identities and hashes. **Worth doing only as its own change with its own reason —
     never folded into a cleanup.**
   - **Class D — 5 historical citations.** `CONSTITUTION_CHANGE_MGMT_V0` and
     `CONSTITUTION_CONSTRUCTION_V0` naming RI-0 as history. **Keep the citation, fix the tense.** A
     sweep that rewrites them destroys the reasoning they exist to carry.
   - **Class E — 11 ungrounded prose claims.** Paths and tools stated as current that are not.
     Cheapest and safest; independent of everything else.

28. **NEW — the machine-block census already draws the line the survey blurred, and nothing reads
   it.** `compile_domain.sh --verbose` reports `○ preserved — declarative policy, no compiler
   consumer` separately from `⚠ candidate unconsumed`, and it correctly classified
   `reuse_visibility` as preserved. Had that been read first, the "inert" misclassification would not
   have happened. **The next survey of this kind starts at `--verbose`, not at grep.** The standing
   warning on `collatz`, `inspection` and `blockchain` is one key, `context_requirements`, declared
   `[]` on every TI and documented in the contracts as "inert in V0 (AC reserved)".

29. **NEW — a corpus filename asserts a verdict that is only true against one baseline.**
   `admissible_p7_deferral_owned.md` reports ADMISSIBLE in `e2e_phases_test` (CR-1's reproduced
   baseline) and INADMISSIBLE in `differential` (the current composition, where CR-1's artifacts
   already exist). Both are correct and the differential only claims the two paths agree — but the
   flagship fixture `p7_design_intent_book_library_mgmt_catalog_v0.md` has the same 12 findings, so
   this is a standing readability trap rather than a new one.

30. **NEW — most rules have never been shown to fire, and now there is a number.** Measured against
   the e2e expectations, which are the only place a rule is asserted to fire by name:

   ```
   P0 61.5%   P1 37.5%   P2 18.8%   P3  9.5%   P4 27.8%
   P5 25.0%   P6 18.2%   P7 31.2%   P8 21.1%
   229 distinct rule ids · 63 demonstrated · 27.5%
   ```

   **Roughly seven rule identifiers in ten have never been observed to fail.** P3 stands at two of
   twenty-one. The argument for why this matters is the workspace's own — five rules were found
   reporting clean while checking nothing — and it has only ever been applied to *new* rules. Two
   honest qualifications: a rule may fire on a differential document without an e2e case naming it,
   so the true figure is higher and cannot be read off; and full coverage is not obviously the goal
   for rules that are near-impossible to violate in a document that parses.

   **Corpus concentration is the cause.** Twenty of the forty corpus documents exercise P7; P5 has
   one, and its admissible case comes from a fixture rather than a corpus document of its own.

31. **NEW — a register costs five rules, and no author sees that number.** P7 declares 20 registers,
   16 of them optional, and every register brings five derived rules whether required or not. That
   is the arithmetic behind mandate rule-count projections coming out low (~157 projected, 179
   actual). It is computable at authoring time and nothing computes it.

32. **NEW — `core.enforcement_stage` is read by four mechanisms, and discriminates almost nothing.**
   An earlier draft of this entry, and `protocol_compiler/doc/MACHINE_BLOCK_CLOSURE.md` §4, both said
   it is read by one handler. **Both are wrong**, and the correction matters because it changes what
   the investigation is:

   ```
   s4_govern.py:136                              gates ASSERT derivation entirely
   assert_assert_parity_v0.py:61
   assert_governance_declaration_resolves_v0.py:90
   assert_runtime_invariant_wired_v0.py:53       the one the doc names
   ```

   The first decides whether an invariant is compiler-enforced **at all**. So this is not the
   declared-doctrine-nobody-reads class. What it is instead:

   ```
   88 invariants
     48  compiler_assertion      2  compiler_meta_validation
     37  compiler_validation     1  compiler_discovery
                                 1  composition_conformance
                                 0  runtime_outcome
   ```

   **87 of 88 declare a `compiler_*` stage.** Exactly one invariant is gated out of ASSERT
   derivation. A dimension with 88 authored values and one consequential distinction is not
   decoration and is not doing much either, and *that* is the question worth a dossier.

33. **NEW — a handler guards an empty set.** `assert_runtime_invariant_wired_v0` selects invariants
   whose `enforcement_stage` contains `runtime_outcome`. **No invariant declares it.** The handler
   runs on every build, matches nothing, and reports clean — the vacuity class, inside the
   enforcement machinery itself. Smaller and sharper than issue 32, and checkable today.

34. **NEW — `multi_structure_binding`'s P0 contradicts its own closure.** The dossier is
   **delivered**: P0–P6 all admissible, terminal at P6 by ruling, with `delivery.md` and
   `closure.md`. Its `p0_business_problem_statement.md` still opens *"This dossier is at P0 and its
   phase run has not begun."* That banner was true when written and is now false. **Recorded rather
   than edited** — a delivered dossier is not amended, and a status banner is not an exception worth
   making the first one.

35. **NEW — `MACHINE_BLOCK_CLOSURE.md` §4 is still wrong, and now wrong twice.** It says
   `core.enforcement_stage` is read by one handler; it is read by four. It is also the source the
   dev/7 opening premise was taken from, which is how a measured investigation started from a false
   claim. **Nothing in it is enforced by anything** — it is prose about machine consumption with no
   check that it still describes the machine. Fixing the one sentence is a ten-minute job and misses
   the point: the document is a second, unenforced spelling of what the code does, which is the exact
   defect dev/7 just deleted from 14 invariants.

36. **NEW — a domain invariant is authored outside the governance chain, and RULED.** The symptom is
   that only `conformance_workloads/workloads/collatz` lists `INVARIANT` in its `artifact_types`, so
   dev/7's wiring check can find a subject only in the workload and probe D had to be authored there.
   The defect underneath is larger: **a domain cannot express a *governed* constraint over subjects it
   owns.**

   ```
   workload::INVARIANT_CT_SURFACE_CLOSED_WORKLOAD_V0   named by no constitution, anywhere
   INVARIANT_GOVERNANCE_DECLARATION_RESOLVES_V0        applies_to_kinds [CONSTITUTION, INVARIANT]
   INVARIANT_ASSERT_PARITY_V0                          applies_to_kinds [INVARIANT]
   _DOMAIN_INSTANTIATED                                {WF,CC,CS,CT,RB,AC,IN,EV,TI,TE}
   ```

   Neither kind is domain-instantiated, so neither check is ever imported into a domain build. The
   rule that refuses an invariant no constitution declares cannot run where domain invariants live.
   The one that exists is an orphan and nothing can say so.

   **Ruled yes, with a precondition** — `software_governance/doc/DOMAIN_INVARIANT_AUTHORITY_RULING.md`.
   Authorship is granted only together with (1) a domain-authorable constitution to declare the
   invariant and (2) the two chain checks reaching domain builds. Granting `INVARIANT` in three
   `artifact_types` lists first is one line per domain and yields three more ungoverned invariants —
   the defect dev/7 spent itself deleting.

   **And the precondition cannot be enforced as a coverage count.** Measured: every domain build
   config reports **zero** ungoverned kinds, `INVARIANT` included — 8 admitted invariants name it.
   All 8 are universal well-formedness checks (FQDN shape, uniqueness, schema conformance,
   superseded references). A domain invariant is checked for *shape* and not at all for *authority*.
   A census by kind reports a complete surface over an absent chain.

   **The check is built and it is red.** `standards/process/governance_chain_closure.py` names the
   three relations instead of counting coverage, and imports `_DOMAIN_INSTANTIATED` from
   `s1_extract` rather than restating it:

   ```
   ORPHAN     workload::INVARIANT_CT_SURFACE_CLOSED_WORKLOAD_V0 — named by no constitution rule
   UNCHAINED  STRUCTURE_BUILD_WORKLOAD_CONFIG_V0 may author INVARIANT
                unreachable: DECLARE / RESOLVE / PARITY
   ```

   Probe G grants `INVARIANT` to `book_library_mgmt` and the check names the config that changed.
   Probe H withdraws the workload's authorship and its one invariant and the check **passes** —
   without H, a gate red on real state is indistinguishable from a gate red on everything.

   **Ruled: the workload's authorship is withdrawn.** `INVARIANT` removed from
   `STRUCTURE_BUILD_WORKLOAD_CONFIG_V0` and `INVARIANT_CT_SURFACE_CLOSED_WORKLOAD_V0` deleted. The
   chain check now passes and is in the runbook. **The cost is real and is issue 38.** S8_VERIFY
   caught the stale compiled artifact on the first rebuild, which is the build gate working.

38. **NEW — the workload's CT surface is no longer closed.** Withdrawing the workload's one invariant
   removed the only enforcement of its capability-transform allow-list, which named exactly the two
   CTs it has: a third could now be added and nothing would refuse it.
   `INVARIANT_CT_SURFACE_CLOSED_V1` cannot substitute — it carries the *platform's* allow-list, and
   importing it into a domain is the 7-violation counterfactual dev/7 measured. **This is the price of
   issue 36's ordering, paid deliberately and recorded rather than absorbed:** the workload traded a
   live-but-ungoverned check for no check, and gets it back when a domain can author a governed one.

43. **RESOLVED — `register_coverage` is closed unbuilt, and two of its instances had been fixed
   without anyone recording it.** The fork asked whether a design can state, for an artifact it
   amends, every fact that artifact carries. Its three named instances, checked against the design
   language as it stands:

   - **an amended artifact cannot state its subdomain** — no longer true. `p8.field_declarations`
     carries it, `render.py:304` reads it from there, and `AMENDED_ARTIFACT_UNPLACED` refuses an
     `EXTEND` artifact missing from it — a rule first demonstrated this session, from cr_02;
   - **a vocabulary that extends nothing cannot say so** — no longer true. `render.py:657` treats a
     sentinel in `Extends` as *declared* emptiness and says so in the P0's own words;
   - **a build configuration cannot be amended** — still true and deliberately so. No register holds
     its 56 leaf facts, but `build_manifest` derives the artifact whole and acceptance compares it
     every run with no differences. **The P0's own example no longer holds:** subdomain plurality is
     derived from the distinct `Subdomain Field` values a mandate declares.

   **The P0 says four instances and names three.** No fourth paragraph exists; whether one was
   dropped or the count was never right cannot be established. Fitting for a session that ruled a
   count is a moment and the things counted are the property.

   The residue is not the change this dossier describes. It is whether an artifact every field of
   which is **compiler configuration** belongs in the design language at all, or to the generator
   that derives it — `generated_artifacts`' question, asked of configuration rather than behaviour.
   **Raised when a change forces it; no change has yet amended a build configuration.**

42. **RESOLVED — the acceptance corpus can no longer go stale silently.** `tc construction emit` was
   recorded as the last generator without an agreement check. **It was not.**
   `construction_acceptance.py` already compares everything it writes — rendered artifacts and the
   generated build manifest both, semantically and Machine-block scoped, 93/93 over two domains.

   What was unchecked is `DOMAINS`, a **hand-kept pair** — the shape `SEQUENCED` was introduced to
   remove one level down, where a missed entry cost cr_03 twelve differences read as construction
   defects. Two ways it goes stale: a third domain reproduced by nothing, and `sequence()` matching
   only `cr_NN_` so a base-code domain's deliberately unnumbered `dossiers/<subject>/` can never
   enter the corpus whatever it declares.

   The harness now asks that question of the workspace rather than of a second list, and names the
   catalog's fixture substitution so a deliberate override is not read as an omission. Two probes,
   authored and observed to fail: dropping blockchain from `DOMAINS`, and giving
   `transformation/dossiers/declared_reach` one new artifact — the unnumbered form, the hazard that
   could not have been found by reading the list.

39. **NEW — two rules need a dossier, and the spec is written.** Not five: three of the reach rules
   turned out to be document-local once the right identifier kind was used, and are now demonstrated.
   What remains needs authoring, and the reasons are specific rather than "no subject exists":

   - **`UNDECLARED_REACH_READ` skips any act whose own binding the composition does not publish** —
     deliberately, since what an act owns being undecided makes what it reaches indistinguishable
     from it. **Every change that authors its own runtime binding is invisible to it.** cr_01
     authors `RB_CATALOG_BINDINGS_V0`; cr_03 extends a published one but composes nothing, so a row
     added to give it a read trips `COMPOSITION_CC_UNDECLARED` first.
   - **`BORROWED_CAPABILITY_NOT_DECLARED_CROSSING`** reconciles P6 against P5, and **all eight P5
     documents in the workspace declare `cross_subdomain_refs` empty** — three fixture CRs and five
     dossiers. The register has never carried a row.

   The dossier: extends an existing subdomain (so its RB is published), P5 names one borrowed CC,
   P6 carries it SATISFIED with the artifact named, P7 declares and composes a contract that reads
   the other subdomain's store by bare name, and leaves `declared_reach` empty in the probe cut from
   it. Full form in `transformation/doc/FEATURE_LEVEL_CLOSEOUT.md`. **Worth authoring for its own
   sake:** `declared_reach` was designed, delivered, and never once filled by any document.

40. **NEW — a correct check can make a fixture useless as evidence.** Dropping a vocabulary-bearing
   column at P1 fires `CELL_NOT_IN_VOCABULARY` thirty-nine times; dropping `field_declarations` at P8
   fires `SCHEDULED_ARTIFACT_UNPLACED` forty-two. Both are the check working. Five P7 rules remain
   undemonstrated for exactly this reason and want a recut, not a new rule.

41. **NEW — judging a delivered CR's P7 or P8 against the current snapshot is meaningless.** The
   admissible cr_01 fixtures fire `NEW_CODE_ALREADY_EXISTS` 42× and two spurious `NODE_INPUT_UNBOUND`
   under `tc phase check --snapshot ../snapshot`, because cr_01 shipped and cr_02 amended its
   contracts. The e2e harness carries the pin and is clean. **A CLI run of these documents is not
   evidence** — `design/sealed.py` exists to make the pin name the rule set, and the same discipline
   applies to the baseline.

12. **`standards` stays private.** `doc/github-recovery-codes.txt` is a standing violation awaiting
    `git filter-repo`.

## Architectural Concerns

- **A change that renders nothing has no Construction Completeness, and that is where the artifact
  set goes unchecked.** cr_03 was caught at 98.2% by the only thing that renders. This change renders
  nothing — every amended artifact is re-emitted by a generator — so the same class of omission
  (Open Issue 22) passed 808 rules and was found by reading `git status`. **Construction Completeness
  is not a check on generated artifacts; nothing is.**

- **Adding a register to the design language invalidates every document written before it.**
  `REGISTER_MISSING` fires on an absent optional register, so every delivered dossier goes red the
  moment the template grows. The established practice is to backfill the maintained fixtures and let
  the originals stay red. That practice is undocumented, was inferred from `declared_reach` having
  been handled the same way, and is the reason a green suite says nothing about the delivered corpus.

- **A refusal the business states in one sentence may need several rows, or none that fit.** "Any
  catalog operation" became nine rows keyed to one seed pair, which the coverage rule handles
  correctly and no rule requires. "Retire a work | Always." fits nothing at all. **The register was
  designed from four refusals in one seed and met seven and six in the next two.**

- **Nine admissible phases do not make a buildable design, and only construction knows.** Unchanged,
  and now with a second instance where construction could not know either.

- **The last hand-kept copy is the one that fails — all three are derived now, and a fourth is
  open.** `DOSSIERS` reads the `cr_NN_` names, the `--root` flag is checked, and the differential's
  prior map is read from `PRIORS` and the `CR:` header. The pattern held every time: the fact was
  already declared somewhere and the harness restated it. **The one left is `tc construction emit`**
  — the artifacts it renders have no agreement check, and that is the layer where business artifacts
  live. Ask of anything generated: what does a person still have to keep in step by hand?

- **An artifact is not a unit of liveness; a field is.** The `pgs_*` survey inferred "consulted by
  nothing" from one field resolving to nothing and generalised it to the whole artifact. Deleting
  three artifacts on that reading compiled clean and turned three P3 cases red, because a different
  field in the same artifacts was live. The compiler's own machine-block census had already made the
  distinction and nobody had read it. **Ask of any artifact proposed for removal: which of its fields
  is dead, and which is merely unread by the thing you happened to look at?**

- **The rules were coordinated; the evidence was not — and now it is.** 229 distinct rule ids, 63 ever
  observed to fire, against 40 corpus documents of which 20 exercised P7 alone. `meta_test` proved
  every rule resolved to a mechanism, which is not the same as proving one ever fired. Thirty
  documents later: 219 of 229. **The repair was documents, not rules**, and it found two rules that
  could not fire, one silent at a whole phase, one skipping most of its register, five with no subject
  anywhere, and a real leak in an existing fixture. `transformation/doc/FEATURE_LEVEL_CLOSEOUT.md`.

- **A doctrine nothing can fail is not enforced, however plainly it is written.** Unchanged, and now
  with a second instance: the sequencing rule *"never widen an authoring surface before its governance
  machinery is complete"* was proposed as doctrine, and the obvious encoding — coverage by kind —
  reports **zero** gaps for every domain while the authority chain is entirely absent. A check has to
  name the relation it wants or it measures nothing.

- **A declared invariant that passes is not an enforced invariant, and the only proof is tampering.**
  Unchanged.

## Next Session Should Start With

**dev/7 is closed. Issues 32 and 33 are discharged; issues 35 and 36 are what it left behind.**
Read `software_governance/doc/ENFORCEMENT_AUTHORITY_RULING.md` before reopening any of it — it
carries the four rulings, the measurement they rest on, and six probe transcripts. Nothing in dev/7
is open. What follows is the queue it did not touch.

**The one thing to carry forward, because it cost two wrong premises to learn.** dev/7 was framed
three times and was wrong twice — first from `MACHINE_BLOCK_CLOSURE.md` (a doc), then from an
expert reading of `scope.applies_to` as an applicability axis (a plausible name). Both were corrected
by reading what the code does with the field, not what the field is called. Issue 35 is the residue:
the doc that supplied the first false premise is still unenforced and still wrong. **Before ruling on
any field, ask what reads it and what happens when you remove it — a name is a hypothesis.**

**That pass is done — 27.5% → 96.9%, and it is what makes everything below cheaper.** What it left
is one dossier, not thirty documents: **two rules across P6 and P7 cannot be reached from any
existing fixture**, and the dossier that closes them also fills `declared_reach`, a register designed,
delivered and never once carried by a document. Issue 39 has the spec. Take that first.

Then, in order:

| # | What | Where |
|---|---|---|
| 1 | Rule on Open Issue 22 — the design named three artifacts and seven changed | `refusal_discharge` P7 §2, and a new rule |
| 2 | Open Issue 17 as its own identity CR — a caller supplies `admitted_outcomes`, so a caller decides what the system admits. **Not** a wallet reopening | new CR against `blockchain::identity` |
| 3 | Amendment-set completeness for generated changes — the general form of issue 22 | `design/` |
| 4 | Prohibition by absence — the one unbuilt refusal form. cr_02 cannot be its subject; its material supplies no identity to prohibit | new dossier |
| 5 | `pgs_*` classes D and E — tense and prose only, per the survey's classification. **Never a blind sweep** | `software_governance` |
| 6 | Issue 36 — **ruled yes, unbuilt.** Build the precondition before the permission: a domain-authorable constitution, then `GOVERNANCE_DECLARATION_RESOLVES` + `ASSERT_PARITY` reaching domain builds, then `INVARIANT` in business-domain `artifact_types` — in that order | `software_governance` + `protocol_compiler` |
| 7 | Issue 35 — `MACHINE_BLOCK_CLOSURE.md` §4 is wrong and unenforced. The one-line correction is not the fix; an unchecked description of machine consumption is the defect dev/7 just deleted from 14 invariants | `protocol_compiler/doc` |
| 8 | Issue 39 — a dossier that extends a subdomain, borrows a capability across the boundary and declares its reach. Closes the last two rules and fills a register no document has ever filled. Spec recorded | new dossier |

**Class A stays untouched:** 27 live lookup keys carrying RI-0 names, nothing broken, and a rename
that must move the compiler, the registry and the artifacts together.

**Guardrails that cost something to learn.** A delivered dossier is never reopened — raise a new CR.
A survey classifies *fields*, not artifacts. A check that has never been observed to fail is evidence
of nothing. **And a standing open item is a claim, not a fact** — `tc construction emit` was carried
for several sessions as the last generator without an agreement check, and measuring showed
everything it writes is already compared. What was unchecked was one level up; see issue 42. And from dev/7: **a field's name is a
hypothesis about what it does; the deletion probe is the test.** `scope.applies_to` reads as
"where this applies" and means "the surface whose allow-list I carry" — the difference between a
three-line fix and a rebuild of closure admission that would have broken surface closure in every
domain.

### Pins, before running anything

```
book_library_mgmt cr_01–03, rule_expressiveness   completed — never re-pin forward
register_coverage                                 closed unbuilt — never re-pin
rule_effectivity                                  in flight — legitimately re-pinned
multi_structure_binding, select_operation,
multi_emission                                    approved at P6 · pinned dd8da7a0…
declared_reach                                    delivered · pinned 2e7815fe…
cr_04_wallet                                      delivered · pinned 381ba055…
cr_03_catalog                                     delivered · pinned 9c2c693d…
refusal_discharge                                 implemented · pinned 6e1e571d…
```

### The runbook, in order

```bash
python standards/process/governance_closure.py               # two relations nothing else checks
python standards/process/governance_chain_closure.py         # declare/resolve/parity, wherever an invariant may be authored
python transformation/scripts/emit_rule_sets.py --check      # first — it sees param drift the others cannot
PYTHONPATH=snapshot_inspector \
  python snapshot_inspector/scripts/author_transport_contracts.py --check
python transformation/scripts/testbed/meta_test.py
python transformation/scripts/testbed/differential.py
python transformation/scripts/testbed/e2e_phases_test.py
python transformation/scripts/testbed/projection_test.py
python transformation/scripts/testbed/construction_acceptance.py
python standards/process/implementation_closure.py
PYTHONPATH=snapshot_inspector python snapshot_inspector/scripts/testbed/test_inspector.py
protocol_runtime/run.sh run --wf workload::WF_COLLATZ_CONJECTURE_V0 --payload <file> --data-root <abs path>
protocol_runtime/run.sh run --wf ai_governance::WF_GOVERN_AGENT_ACTION_V0   --payload <file> --data-root <abs path>
protocol_runtime/run.sh run --wf ai_governance::WF_PROVISION_AI_LICENSING_V0 --payload <file> --data-root <abs path>
python business_domains/book_library_mgmt/testbed/catalog/execution_validation.py
python business_domains/book_library_mgmt/testbed/catalog/execution_validation_cr02.py
python business_domains/blockchain/testbed/identity/execution_validation.py
python business_domains/blockchain/testbed/wallet/execution_validation.py
python standards/process/pgc_env_check.py
```

The full runbook is `standards/process/RUNBOOK.md`, which carries the payload paths and the seed step
`ai_governance` needs before its first run. **Run identity's validation before the wallet's and into
the same data root** — one domain has one place its records live, and the wallet suite refuses only
its own stores being non-empty.

A clean rebuild is `protocol_compiler/compile.sh`, then `compile_domain.sh` for every domain root
carrying a `STRUCTURE_BUILD_*_CONFIG_V*.md`, then `snapshot_assembler/assemble.sh` — the build gate
inside `standards/process/release.sh`, without the release.

### Judging a dossier

Each phase reads only its **declared** priors, and passing an undeclared one is a hard error:

```
p1←p0   p2←p1   p3←p2   p4←p3   p5←p0   p6←p0,p5   p7←p5,p6,p0   p8←p7
```

P7's third prior is this session's change. P0's document is the **seed**, not
`p0_business_problem_statement.md`. A phase run without a prior it declares does not quietly pass —
it reports that the handoff was unchecked.

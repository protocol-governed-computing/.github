# SOTU Handoff

## dev/10 is open. The realization map has begun.

Read this cold: it is self-contained. Prior cycles are **not** restated —
`.github/process/notes/release-3…9.md` carry what each release did, and `.github/doc/parked_rulings.md`
is the ruling record. Read the latter before reopening anything that looks unsettled. Only what bears
on future work survives here; resolved issues have been dropped.

### Where things stand

All ten composition repos are on `dev/10`, clean, with `release-9` cut. `standards` is on branch
`draft/2`, its `VERSION` still reading `draft-1`.

**Branch and revision are separate names and the slash is what keeps them apart.** The branch is
`draft/2`; the revision it will carry is `draft-2`, the value in `VERSION`. `draft-1` is a tag, so a
branch spelled `draft-2` would collide with the next one.

```
standards/          the standard, alone      spec/ (31 docs), doc/, README, LICENSE, NOTICE
.github/            org + workspace          process/ (release.sh, 5 checks, RUNBOOK, notes/)
                                             doc/ (SOTU, parked_rulings, dev_10_task_plan,
                                                   assembly contract)
                                             snapshot_profiles/
software_governance/doc/namespace_map.md     the fb.* migration plan, beside its ruling
```

**The dev/10 plan is `.github/doc/dev_10_task_plan.md`** — three tasks, ordered by dependency:
A realization map → B namespace representation (`fb.*` / `pgc::`) → C human text alignment. It is
live and is not restated here.

**Convention:** git-tracked working documents go in `doc/`; anything gitignored goes in
`doc/parkinglot/`, already covered by each repo's `.gitignore`.

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

**Revise only by explicit ruling**, and a revision is supersession (`4e` §9): declared against a
named predecessor, stating what it changes and what that invalidates. `draft-1` stays marked and
unedited; `draft-2` is the revision that supersedes it, authored on branch `draft/2`.

**Direction is not symmetric.** Validate the **RI against the spec**, never the reverse (`0z` §3).
A realization "informs this family by exposing concepts that were missing, distinctions that were
conflated, and requirements that could not be met; **it never supplies authority.**"

---

## Task A — the realization map, complete; rulings passed

**`standards/doc/realization_map.md` is complete over every normative document of the family** —
twenty-five documents, roughly 280 invariants, 43 findings. `1c` is partial by design: ten of its
seventeen invariants are restated by documents mapped elsewhere.

**dev/10 item 2 is delivered.** The map is what Tasks B and C were waiting on.

**The three findings against the documents are ruled and closed.** Rulings in
`.github/doc/parked_rulings.md`; **one reversed against the map, one upheld, one narrowed.** Both
surviving document findings are **applied** — `standards/VERSION` is now `draft-2`, declared in
`standards/doc/revisions.md`. **The map's remaining findings are all realization-side.**

**It is deliberately not in `spec/`.** A map inside the revision unit would let a change in a
codebase move the standard's revision identity — the inverse of the direction of authority the
family exists to protect. It declares no part, satisfies no membership condition of `0z` §5, carries
no file identifier, appears in no document map, and does not participate in revision or supersession.
`8a` §6 was rewritten to say so; `0z` §2 gained no row.

**It is stated against a named subject** — snapshot `7b6f2699…`, 7 domains, 398 artifacts,
`draft-1`. It does not age into being wrong; it stays about an older snapshot, and rechecking means
restating the subject and rewalking the entries.

### Forty-three findings. Forty-one against the realization, two against a document.

Full statements in the map's §9; grouped here by what would close them.

**The identity story is half-built — one defect, five entries.**

| # | Finding |
|---|---|
| 1 | The snapshot identity does not cover every constituent — `artifact_index`, `kind_index`, `store_index`, `behavior_logic/`, `conformance/`, `evidence/` sit outside `_identity_view` |
| 2 | Integrity at acceptance compares recorded values and never recomputes from content |
| 3 | The self-description is not covered by the identity it carries |
| 4 | No snapshot claims a profile, so acceptance cannot evaluate one; SN-7 has no subject |
| 5 | Nothing prevents or detects a sealed projection edited in place |

**Declaration surfaces that stop short of the mechanism.**

| # | Finding |
|---|---|
| 6 | No projection contract exists — six lossy projections declare no selection, so omission is uncheckable and PJ-6 is vacuous |
| 7 | `dispatch`, `handlers` and the vocabulary lookup tables have no structural verification, and `dispatch`/`handlers` are what the runtime routes on |
| 8 | The read/query classification IN-4 requires is undeclared — `catalog.category` is presentation |
| 9 | Reads are permitted by reachability; `context_requirements` is declared and inert |

**Evidence records the path and not the determination.**

| # | Finding |
|---|---|
| 10 | A trace establishes the path taken and none of `3e` §3.1's five points — no closure, no rules supplied, no predicate results |
| 11 | Construction refuses without evidence: a `CompilerError` produces a stderr diagnostic and exit 1, and no record of the determination |
| 12 | Evidence does not distinguish determinative from observational content, and the distinction is undeclared — so EV-6 cannot be checked even in principle |
| 13 | The attestation names no attesting party (`public_key_ref: "STUB"`), so no chain terminates in a nameable trust root |

**Resolution and admission — the only outright violations.**

| # | Finding |
|---|---|
| 14 | Imported-capability resolution **searches** (`rglob`), **selects** (`matches[0]`), **falls back** (`continue`), and never compares the found artifact's declared identity against the one sought — ID-14, ID-11, ID-7 |
| 15 | A pure relocation changes the composite snapshot identity — the canonical artifact carries a `module_path` derived from its source directory, and `_identity_view` covers the canonical projection hash. `4c` §10's relocation test fails. **Proved by probe** |
| 16 | A namespace of the form `fb.<concern>` encodes concern alongside identity — ID-12, already ruled |
| 19 | **`owner_subdomain` — a governed ownership fact a governance assertion refuses on — is derived from the source directory** via `module_path`, and no artifact declares it. PJ-4 and `4c` §4.1. **Proved by probe** |

**Enforcement — an obligation that cannot refuse.**

| # | Finding |
|---|---|
| 20 | **`INVARIANT_CC_NO_UNUSED_OUTPUTS_V0` is declared as governance and cannot refuse.** Its handler returns `"violations": []` / `"status": "PASSED"`; its only violation path is a missing-context guard. EN-5, EN-11 — and its declared subject is "code smell" and "optimization opportunities", which is **adequacy**, breaching GC-1 |
| 21 | Coverage is proved one way only: nothing proves an *obligation* has an assertion capable of refusing it. EN-1 |
| 22 | Nothing compares what an assertion does against what its invariant says, so a drifted handler is indistinguishable from a faithful one. EN-4 |

**Part II — declaration, classification, and authority.**

| # | Finding |
|---|---|
| 23 | **Integrity is computed over the serialization, not a canonical form of the semantic object.** Swapping two sibling YAML keys leaves the parsed object identical and moves `content_hash`, `graph_topology_hash` and `canonical_projection_hash` — the composite snapshot identity moves. MB-3, ID-3, KV-8. **Proved by probe** |
| 24 | **Five schemas do not close their surface** — STRUCTURE (the build-configuration authority), the three AUTHORITY kinds, TRACE_EVENT — and **`TRANSPORT_INGRESS`/`TRANSPORT_EGRESS` have no schema at all**, so 36 contracts carrying the read surface are validated by no closed surface. MB-11 |
| 25 | Semantic category and provenance are declared **per kind, in code**, where GO-1/GO-3 ask a kind to declare and GO-2/MB-12/MB-13 quantify over **elements** |
| 26 | Nothing evaluates an artifact against its category's contract; GO-6…GO-9 hold by pipeline arrangement rather than by a check. GO-5 |
| 27 | No kind states whether a governance assertion is required for its ordinary use, so omission is indistinguishable from a kind requiring none. MB-10 |

**Execution and vocabulary.**

| # | Finding |
|---|---|
| 28 | **An outcome with no declared routing ends the run instead of refusing.** A non-exit node with an unrouted outcome is indistinguishable from an exit, and the workflow reports the last contract's status as its own. EX-5, EX-14, RT-9 |
| 29 | **The `IN_` admission gate admits unconditionally** — `result_status = "ACK"`, with "admission_snapshot not yet integrated" stated in the code. A declared admission point determining nothing. AI-6, EX-14, RT-9 |
| 30 | **The kind registry constitutes the vocabulary.** KV-3 forbids a registry, contract or mechanism from constituting a kind; `artifact_kinds.py` is what makes a kind real, and nothing checks it against the declared vocabulary authority |
| 31 | Outcome resolution falls back from `transition::` to `outcome::` — two declared namespaces in fixed order, but resolution proceeding to a second source. AI-6, RT-6 |
| 32 | GS-2 requires refusing where subject-side and governing-side assertions disagree; `governance_chain_closure.py` detects it in a runbook script, not at build |

**Profiles — the instrument that was never attached.**

| # | Finding |
|---|---|
| 33 | **The baseline profile has rotted and nothing noticed.** 23 of its 35 required artifact FQDNs do not resolve — `fb.constitution::` and `fb.topology::` no longer exist. `REFERENCE_PLATFORM_PROFILE_V1` resolves 35/35. **Nothing distinguishes them, because nothing reads either.** NP-6. **Measured** |
| 34 | **NP-7 breached in substance, and no code change closes it.** Externality is *authorship*, not storage: changing `.github/snapshot_profiles/` is the same act, by the same authority, through the same release, as changing the platform it constrains |
| 35 | No execution environment profile exists; EE-2/EE-3/EE-8 have no subject, and what EE-4/EE-5 protect is held by doctrine in a `CLAUDE.md` rather than a declared boundary |
| 36 | No domain profile exists for any of six domains, so DP-4 — state whether the domain claims to be an authority or is a concern — is undeclared everywhere. Finding 16 at domain scale |

**Transformation, supersession, capability.**

| # | Finding |
|---|---|
| 37 | **RULED, narrowed.** The vocabulary concern fails `8a` §4.7 — every term names a real distinction an alternative may rename. **One clause survives**: TR-17's proportion-and-threshold, where §13 states the meaning one line later. **Against the document** |
| 38 | **RULED, upheld.** SU-5's subject is *dependency*, not mention. The realization's own handler already exempts `{supersedes, superseded_by}` — an implementer enforcing SU-5 as written hits the contradiction immediately. **Against the document** |
| 39 | Supersession is declared **twice** — `supersedes` on the successor and `superseded_by` on the predecessor — where SU-3 requires it once with the other side derived |
| 40 | TR-3a admits no threshold; **7 of 229 design rules have never been observed to refuse** (96.9%) |
| 41 | TR-11 requires preservation checked both ways; the realization checks **loss** and not **fabrication** — the exact failure `4d` §18 says reports success |
| 42 | **No census exists of which of the 85 compiler assertion handlers have ever refused.** CD-3 binds them as it binds the design rules, which were measured |
| 43 | The workload's CT surface closure invariant was withdrawn, so **CP-7 holds as a fact and nothing would refuse a third CT** in that domain |

**Refusal, and the one finding against a document.**

| # | Finding |
|---|---|
| 17 | Refusal leaving no residue holds by pipeline shape, not by mechanism. `1c` AI-8 carves out "except for the evidence that it was refused" — the realization holds the rule and drops the exception |
| 18 | **RULED, reversed.** `5b` §2 forecloses the tooling exemption by name; §12 closes the observability route; IN-14 bounds scope at the seal. **Violated by the realization** — `protocol_runtime examine` and `.github/process/frontmatter_fidelity.py` read the sealed snapshot outside the `si.` surface |

### The ruling pass — one reversal, one upheld, one narrowed

Full text in `.github/doc/parked_rulings.md`. Each states what changes and what it invalidates. **No
`spec/` file was edited** — that waits on Open Issue 1.

**Finding 18 — reversed against the map.** IN-13's scope was recorded as unsettled. It is not: the
map read IN-13 in isolation. `5b` §2 forecloses the tooling exemption *by name* — inspection "is not
a debugging affordance, a developer convenience, an administrative back door, or **a tool that
happens to read files**" — and §12 calls a side channel opened for observation an ungoverned read
path. **IN-14 supplies the boundary**: inspection cannot be performed against an unsealed
representation, so construction reading its own in-flight state is outside `5b` without needing an
exemption, and anything reading a *sealed* representation is inspection whoever performs it.

So the scope is broad, and **the finding converts into two violations by the realization**:
`protocol_runtime examine` (its own locator/parser/reporter over a sealed snapshot, answering to a
person) and `.github/process/frontmatter_fidelity.py`. `runtime examine` is the larger — a whole read
surface that should be `si.` operations. **The realization already shows the right pattern**:
`transformation/design/sealed.py` went through `si.artifact.show` rather than opening the file, and
`si.rule_set.list` was authored when a check needed a sealed fact.

*Worth saying plainly: the reading that exonerated the realization was the one the map reached first,
and it was wrong.*

**Finding 38 — upheld; SU-5 is narrowed to dependency rather than mention.** SU-5's subject is a
dependency on the predecessor, not any mention of it; §4's strictness clause overshot into forbidding
the declaration SU-3 mandates. **The decisive evidence is not textual** — the realization enforces
SU-5 with a handler that walks the entire machine block, deliberately total, and carries
`DECLARATION_KEYS = {"supersedes", "superseded_by"}` with a `continue`. An implementer enforcing SU-5
as written hit the contradiction and carved out exactly this exception, because without it nothing
can ever be superseded. Proposed: SU-5 gains "other than the supersession declaration SU-3 requires",
and §4 distinguishes a dependency from the record of a retirement. **The realization needs no change.**

**Finding 37 — narrowed. The vocabulary concern fails its own test; one clause survives.** Applying
`8a` §4.7: a **register** is any bounded declared surface carrying governed content rather than prose;
a **rung** is any level in a ladder from business language to bound identity; a one-phase system makes
TR-14 vacuous, not violated. Each names a real distinction and an alternative may rename it.

**TR-17 does not survive.** §13 requires sufficiency "measured … as the **proportion** of required
facts the design states" and refusal "below the declared **threshold**" — a computation and a scalar —
where §13 states the meaning one line later: *"A generator that supplies a fact the design omits is a
second, ungoverned design authority."* A realization checking **per-artifact determinability** meets
that more directly and does not conform to `4d` as written. **The realization is the evidence**:
`--require` defaults to `100.0`, the point at which a proportion carries no information.

**What stays open:** finding one over-specified clause does not settle whether `4d` was *derived* from
the realization, and derivation is not itself a defect (`0z` §5.1). **`4d` carries the highest
inverse-derivation risk in the family and should be re-reviewed clause-by-clause against §4.7.**

### What Part IV, V and VII settled

**The map's second and third findings against a document both came from Part IV**, and neither could
have been found by reading a document against code.

- **Finding 37 required noticing the correspondence was *too* good.** `4d` introduces eleven terms —
  dossier, phase, register, check kind, verdict, gate, worker, rung, grounding, sufficiency,
  realization — **none defined in Part I, all the vocabulary of `transformation/`**, carrying the
  largest invariant set in the family, several matching specific lessons this workspace learned and
  wrote down. `0z` §5 permits a document to define its own terms, so membership holds. `0z` §3
  forbids "describing what an implementation does and declaring the description to be the standard."
  **The map cannot settle which this is and should not try.** The test is `8a` §4.7, and it is
  concrete: *can a transformation system with no "registers" and no "rungs" be shown to satisfy
  `4d`?* If not, `4d` names a mechanism while believing it names a meaning.
- **Finding 38 required reading two invariants of one document against each other.** SU-3 requires
  the successor to declare `supersedes: <predecessor identity>`. SU-5 forbids anything referencing
  the predecessor and `4e` §4 insists the requirement is *strict* — *"no reference, not no executable
  reference. A system that mentions a retired identity has not finished retiring it."* **A conforming
  supersession is impossible on a literal reading.** Cheap to fix: SU-5 needs the exception SU-3
  creates.

**A standing open issue is corrected by measurement.** The record says `blockchain` "carries three
references to a superseded workflow" which "under SU-5 will not compile." Measured: **two** superseded
artifacts; the machine-block references to them are **exactly the SU-3 supersession declarations**; no
artifact carries a live dependency; and **SU-7 is already satisfied** — both are absent from the
vocabulary projection execution consumes and retained in the canonical record. The composition is not
carrying stale dependencies. It is carrying its supersession declarations twice (finding 39).

**Finding 42 is the actionable one, and it has a precedent.** The design compiler measured its own
rule system and found seven rules that could not fire and two silent at a whole phase. **The
governance surface has had no such measurement** — finding 20, an obligation declared as governance
that cannot refuse, was found by *reading*, which is exactly how the silent design rules were found
before the corpus pass. The same census over 85 assertion handlers is the next measurement worth
running.

**`5a` is the best-corresponded document in the map after `6c`, for an identifiable reason:**
transport is the one subject the realization **stopped and specified before building**. Phase 1 was
frozen as a standard, with constitutions, compiler kinds and adapters explicitly deferred until it
was accepted. IB-1 through IB-11 are satisfied by construction. That is the map's clearest evidence
that specifying first works, and it cost one repo's worth of discipline.

**Part VII describes this document.** CF-7 (an obligation with no derivable evaluation is a finding
against the document stating it) and CD-12 (every obligation without a demonstration must be
reported) together are exactly what the map produces. **The map is not a conformance claim** — no
claimant, no profile, discharges nothing — it is the CD-12 report, produced before any claim rather
than as part of one. And CD-4, *every demonstration must be shown capable of failing*, is the
realization's own doctrine in the family's words.

**Three convergences, recorded as the one kind of evidence a single-realization map can offer about
the documents rather than the code:**

| The realization built | The family requires |
|---|---|
| reach is read-only; a write to a consulted entity refused before the capability runs | **DP-7** — a cross-boundary write MUST NOT be authorized by reach |
| "a rule set is not evidence that its rules can fail" — then measured 63/229 → 222/229 | **TR-3a** — every declared rule demonstrated capable of refusing |
| "a check nobody has seen fail is a check nobody has seen" — proved by tampering | **CD-4** — every demonstration shown capable of failing |

Each was reached under pressure from a defect, written down as doctrine, and only later found to
match a normative requirement. Weak evidence — one group, one set of habits — but not nothing.

### What Part VI settled — and how finding 5b must now be closed

**Finding 33 is finding 5b's consequence, measured.** An unclaimed profile is an unverified profile,
and an unverified conformance contract decays silently. The platform's namespaces were reorganized —
`fb.constitution::` → `fb.governance::`/`fb.structure::`, `fb.topology::` → `fb.workflow::`/
`fb.execution::` — and the baseline profile went on looking authoritative while requiring
twenty-three artifacts that are not there. `2a` §6 anticipated a system relaxing its own profile;
this is the same outcome reached by not looking at it.

**Two immediate consequences for Task B.** The migration moves 1,407 `fb.*` occurrences, and
`REFERENCE_PLATFORM_PROFILE_V1` — currently sound — names thirty-five of them. **Add the profiles to
the migration's blast radius**, and **add an FQDN-resolution check on `.github/snapshot_profiles/` to
the runbook**. That check is three lines and would have caught finding 33 long ago.

**Finding 34 changes how 5b gets closed, and this is the important part.** The obvious fix — have the
assembler claim `REFERENCE_PLATFORM_PROFILE_V1` — satisfies SN-5's enumeration and **does not supply
the reflexivity term**, because the profile claimed would still be one the claiming system can
change. `6a` §6 is explicit that externality is a property of *authorship*, not storage, and warns
against exactly this: *"a system declaring the standard it will be judged against — and it will
pass."*

**Closing 5b properly is two acts, not one:** claim a profile, **and** place its amendment under an
authority the composition does not hold. The second is a question about who may amend a document —
a property of the project, not of the build — and no code change closes it.

**`6c` is the best-satisfied document in the map** — nine of eleven demonstrated, including DP-7,
where the realization independently built the exact prohibition the family states: a cross-boundary
write must never be authorized by *reach*. The reach mechanism refuses a write to a consulted entity
before the capability runs, on two declared facts, inferring nothing. **Record this as a win** — the
map's preponderance of findings does not establish that the realization is mostly wrong, and `8a` §2
cuts both ways.

**The map's own method took a correction.** The standing prediction was that documents specifying
subjects the realization approached *without* a specification would start yielding findings against
the documents. It was wrong twice in opposite directions: `3e` did not invert, and Part VI produced
both the best-satisfied document (`6c`) and the two most consequential findings (`6a`) in the same
part. **"Approached without a specification" does not predict where a realization will be found
wanting.** One finding against a document in thirty-six is weak evidence the documents are sound and
strong evidence this map examines the realization rather than the family — which is its stated
direction and also its limit. A second realization is what would test the documents.

### What Part III and the rest of Part II settled

**Open Issue 3 is settled and is not a defect — close it.** `2a` GS-6: every governing element is a
governed subject, and *"there is no privileged element that governs without being governed."* The
`CONSTITUTION_GOVERNANCE_V0 ⇄ CONSTITUTION_VOCABULARY_V0` cycle **is that requirement working**.
`governed_by` denotes the governed-subject relation; a vocabulary constitution governing the
governance constitution without being governed by it would be the privileged element GS-6 forbids.
The narrower reading was already better supported — 46 artifacts naming `CONSTITUTION_INVARIANTS_V0`
is incoherent as authority derivation — and GS-6 now supplies the reason.

**Finding 4 is escalated, and it is now the most consequential item in the map.** `2a` §6.1 says
where reflexivity's regress stops: the genesis closure includes *"an externally claimed profile the
proposal does not author,"* and **"the claimed profile is what prevents reflexivity from becoming
circularity — without it, a system could declare governance that approves of itself and be, by its
own account, perfectly governed."**

No snapshot claims a profile. **The realization is reflexive exactly as GS-6 requires and lacks the
only external term.** This was recorded as an acceptance check with no subject; it is structural.
Two profile documents sit in `.github/snapshot_profiles/` and nothing claims either — closing it is
plausibly a small change with a large consequence, and it is the one finding that changes what the
system *is* rather than what it checks.

**Finding 29 is the third declared-and-inert mechanism**, after `context_requirements` (9) and
`INVARIANT_CC_NO_UNUSED_OUTPUTS_V0` (20). They differ in how plainly the code admits it and not at
all in effect. **Worth a standing rule**: a declared governance point that determines nothing
produces the same outcome as one that permits, which is AI-6's least visible form. Three instances is
a pattern, not three bugs.

**Two things the runtime does better than the standard asks.** RT-11 — no extension point — is proved
by a closed statically imported registry *plus* `implementation_closure.py` proving the naming is
total in both directions, which is a positive demonstration of a property `5b` §16 says is normally
establishable only negatively. And EX-15 is satisfied outright: the trace carries every address in
order, so a party holding the snapshot can replay the traversal. **The trace is sufficient for the
path and insufficient for the determination** — EX-15 asks only for the former, EV-1 asks for both.

**A citation withdrawn.** Finding 23 cited KV-8 with MB-3 and ID-3. KV-8 governs the *declared
version*, not identity, and nothing computes a version — KV-8 is satisfied. `2d` §8 says integrity
values *must* move when the representation changes, **when they follow a canonical form**; the
realization has none, hashing raw bytes in `s1_extract` one stage before the stage named
`s2_canonicalize`. Finding 23 stands on MB-3 and ID-3.

### What Part II settled

**MB-1 adjudicated four open findings and split them two ways.** *"An artifact MUST have exactly one
bounded declaration surface, and nothing outside it MUST determine anything about the artifact."*

- **Finding 19 is a breach.** A directory determines `owner_subdomain` and a governance assertion
  refuses on it — something outside the declaration surface determining something about the artifact.
  `2e` **CA-8** names it a third way: *"containment MUST NOT carry governance of itself."*
- **Findings 6, 8 and 12 are gaps, not breaches.** A projection contract, a read/query class and a
  determinative/observational split are absent from the surface, but nothing outside it determines
  them either. **MB-1 prohibits a second surface, not an empty one.** That changes the cost: three
  are additions, one is the removal of an undeclared second surface — and the realization's stated
  position has to be overturned first.

**Finding 23 is finding 15's twin, and the pair is one defect.** Both move the composite identity
while governed content is unchanged — one on the *location* axis, one on the *representation* axis —
and both have the same cause: **a value that is a property of a file rather than of a semantic object
riding into a projection the identity covers.** `module_path` and `content_hash` are the two values.
Closing either alone leaves the test failing.

**CA-10 is the map's strongest demonstration — record it as a win.** The governance closure is
assembled, enumerated, counted, hashed, carried in the attestation, and re-verified at assembly by
`_verify_governance_provenance`, which refuses a domain compiled against a different closure. It
exceeds what the invariant asks.

**`2e` supplies the vocabulary the authority/concern ruling reached without it.** The realization's
audit of all 26 boundaries maps onto CA-2 (no constituting act), CA-3 (five questions unanswerable),
CA-4 (root authority among peers), CA-6 (a classification constituting a jurisdiction) and CA-7
(scope as the absence of a boundary). **CA-1 is what Task B step 2 must satisfy** — authority,
ownership, scope, concern, admission, inheritance and import each separately determinable. The
current identifier carries at least three of the seven.

**One place the realization decided a question the standard parked.** `2b` §11 leaves open whether
**Evidential** is a peer semantic category; the kind registry already carries it as one. Harmless
today, and exactly the material `0z` §5.1 says may occasion a revision.

### The four that matter most

**Finding 2 is invisible from a snapshot that verified.** Integrity *is* computed from content at
construction — `compute_projection_hash`, then `s8_verify`'s round-trip — and written into each
projection's `metadata.json`. At acceptance nothing recomputes it: `verify_snapshot` and
`loader.py`'s manifest anchor both compare the **recorded** `projection_hash` against the manifest's.
**Edit a file inside a projection, touch nothing else, and acceptance passes.** Closing it closes
finding 5 as a side effect.

**Finding 12 has the widest reach in the map.** EV-6, EV-16 and SN-11 all rest on the determinative /
observational distinction, and none can be demonstrated until it exists. A trace event is flat —
`ts_ns` beside `result_status` beside a caller-filled `detail` — and `3e` §5.2 describes exactly the
three ways a checker then fails. `make_trace_id` is documented as "not purely deterministic."

**Finding 14 is the map's only outright violation** — a mechanism demonstrably doing what an
invariant forbids, rather than failing to demonstrate that it does not. Four lines in
`s1_extract.py` breach three invariants.

**Finding 19 is the one that needs a ruling rather than a work item.** It is the only finding where
the realization holds a *stated, deliberate* position contrary to a normative document — subdomain
ownership declared by module organization, re-homing treated as a versioning obligation — rather than
an obligation it has not yet met. See Open Issue 4.

**Finding 15 is its symptom, and settles Open Issue 4 by probe rather than by argument.** Moving
`WF_COLLATZ_CONJECTURE_V0.md` from `registry/workflows/` to `registry/intents/` — filename and
declaration untouched — leaves `fqdn_id`, `content_hash`, graph address, graph topology, tokenized
projection and attestation **byte-identical**, and moves `canonical_projection_hash`. The cause is one
field: the canonical artifact carries `module_path`, derived from the source directory
(`workload.registry.workflows` → `workload.registry.intents`), and `_identity_view` covers the
canonical projection. **A pure relocation changes the composite identity of the snapshot.** The
semantic layer is sound; the defect is one location-derived field riding into a projection that
identity covers.

**Finding 18 is the class `8a` §6 predicted** and the only one that cannot be closed by building
anything. It needs a ruling: does a governed system's read surface govern reads by *parties*, or by
*any process* including the system's own compiler, assembler and checks? IN-14 inherits the answer.

### On the plan's four known gaps

`dev_10_task_plan.md` asks that AI-4, AI-7, AI-14 and AI-16 be confirmed or refuted first.
**All four are now settled**, and two of them are refuted:

- **AI-4 — refuted as a gap; the invariant holds.** At construction `s4_govern` completes before
  `s7_materialize` writes. At runtime there is exactly one live determination — the reach read-only
  check in `dispatcher._execute_cs_step` — and it returns `VIOLATION` before the capability runs,
  for the reason the invariant gives: *"a write that has happened cannot be unhappened."*
  **Worth knowing why it holds**: the realization moved nearly all determination to construction, so
  AI-4's failure mode is barely reachable. It is held by architecture, not by ordering discipline.
- **AI-7 — refuted as a gap, and held trivially.** Every handler returns `violations`; none returns
  a permission, so combining consequences permissively has no mechanism through which to occur.
  Recorded so that **admitting a permitting rule is recognized as requiring the combination
  semantics along with it.**
- **AI-14 — confirmed, and narrowed.** The runtime evidences its path faithfully and evidences no
  determination (finding 10); construction evidences nothing at all on refusal (finding 11).
- **AI-16 — confirmed as partial.** A party with no access to the producer can recompute the
  composite hash and the governance closure. They cannot establish who vouched for anything
  (finding 13), and cannot compare determinative content (finding 12). **Independently checkable for
  integrity, not for determination.**

**AI-6 was checked while there and is clean** — `E702_UNKNOWN_ASSERT` on an obligation that resolves
to no handler, `E701` on a handler that raises; both fail the build, so an unresolvable governing
element is never an empty one.

**Three absences are deliberately not findings.** SN-11 needs a second conforming agent. IN-2's and
IN-13's negative properties are established by the absence of a path rather than by observation,
which `5b` §16 states plainly. And PJ-12 holds by construction — all six projections derive from one
Graph in one pass — which is stronger than the invariant asks and still not a check on what was
carried.

**A naming collision the map had to state before anything else.** `snapshot/evidence/` declares
`projection_class: evidence_substrate` and carries `nodes`, `edges`, `event_catalog`. It is an
evidence *view* under `4b` §10 and contains **no evidence** under `3e` §3 — it records no
determination. This is the "distinctions that were conflated" case `0z` §3 describes, and it is
resolved in the realization's vocabulary rather than the standard's.

**One entry is a hazard rather than a finding.** The compiler's nine stages `s1_extract`…`s9_attest`
correspond one-to-one with `4a` §5's nine obligations. §5 says obligations, explicitly not stages.
The map states what the correspondence licenses (that they are discharged, in one satisfiable order)
and what it does not, because a conformance regime reading the stage list as the requirement would
reject a realization discharging several in one operation.

---

## Open Issues

### Specification and governance surface

1. **RESOLVED — `standards/VERSION` is `draft-2`, and the revision is declared.** `4e` §9 requires
   the relation be "declared rather than inferred from a number or a date," so bumping `VERSION` is
   not the declaration. **`standards/doc/revisions.md` is new** and carries it: `draft-2` supersedes
   `draft-1`, what each change alters, and what it invalidates. `draft-1` stays marked and unedited
   as the predecessor. **A revision in `VERSION` and not in `revisions.md` has not been declared** —
   that rule is now in `standards/CLAUDE.md`.

2. **Task B steps 2 and 3 are DELIVERED and green** — `software_governance/doc/CANONICAL_REPRESENTATION.md`
   §8–§10. Two declared carriers (`authority`, `concern`) — not three; measurement showed `owner`
   would hold the same string as `concern` everywhere. All 391 artifacts carry them, three generators
   emit them, the three `module_path` derivation sites now read the declaration, and **map finding 19
   is closed**. Both ruling-obligated predicates exist and were **observed to refuse**. Snapshot
   `7557b3a8…`, composition PASSED over 400 artifacts, full suite green including
   `construction_acceptance` 93/93 and all four domain execution suites.
   **Step 4 is delivered too**: 1,402 occurrences across 490 files, zero `fb.*` left, 34 → 32
   namespaces as the two split concerns merged (`capability_transforms` 12+6=18,
   `capability_side_effects` 6+5=11). Snapshot `884ffd0b…`, composition PASSED over 400 artifacts,
   full suite green including all six execution suites against real state.
   **The plan's baseline expectation was wrong and is corrected in §11 of that document**: all 16
   pins are stale and almost none owes a re-pin — a delivered dossier is judged against the
   composition it was designed against, and re-pinning it forward destroys its record (TR-15).
   **Only `rule_effectivity` is in flight and legitimately re-pinnable, and that is a gate, not an
   edit.** Original note:

2b. **Task B step 2 background** — `software_governance/doc/CANONICAL_REPRESENTATION.md`.
   Three declared carriers (`authority`, `concern`, `owner`) replace what the namespace and
   `module_path` currently carry; four of CA-1's seven dimensions already have carriers and need
   nothing. **Two of the plan's preconditions are now discharged**: `STRUCTURE_IDENTITY_V0`'s
   `method: module_path` is read by nothing, so migration edits declarations only and moves no
   directories; and the `blockchain` supersession references are the SU-3 declarations `draft-2`
   explicitly permits, so nothing blocks compilation. **Awaiting a decision before any artifact
   changes.** The original finding, unchanged:

2b. **`fb.*` / `pgc::` violation stands.** `2b` §7.2, GO-11, MB-7, ID-12 state the requirement; the
   implementation violates it. Ruled finding — the standard does not bend. Task B; plan in
   `software_governance/doc/namespace_map.md`, ruling in `AUTHORITY_VS_CONCERN_RULING.md`
   (**unratified**). Sequence is ruling → canonical representation → enforcement predicates →
   migration; **representation precedes predicates**, since a predicate needs a declared field to
   test. Blast radius: 1,407 `fb.` references, 532 files, 6 repos, plus `HANDLER_REGISTRY` constants
   and 16 pinned baselines owing re-pin and re-approval.
3. **RESOLVED by the map — `governed_by` means governed subject, and the cycle is correct.**
   `2a` GS-6 requires every governing element to be a governed subject and forbids "a privileged
   element that governs without being governed," so the
   `CONSTITUTION_GOVERNANCE_V0 ⇄ CONSTITUTION_VOCABULARY_V0` cycle is the invariant working rather
   than a defect. `GOVERNED_BY_AUTHORITY_CYCLE_FINDING.md` can be closed with that ruling recorded in
   `parked_rulings.md`. **It was correctly kept separate from the namespace question** — it turned
   out to be a different problem with a different answer.
4. **Identity authority conflict — measured, and it is governance following directory location.**
   `2c` MB-6 and `4c` ID-1/ID-9 are **satisfied**: `_resolve_identity` reads the declared `fqdn` and
   "path derivation is fully retired," and the relocation probe confirms the semantic layer is wholly
   location-insensitive. What fails is `module_path`, and it is not diagnostic — **two consumers
   derive a governed ownership fact from it**: `artifact_index._owner_subdomain` publishes
   `owner_subdomain` to the read surface, and `assert_rb_storage_subdomain_owned_v0` **refuses** a
   runtime binding that describes another subdomain's storage. Both split the source directory path
   and take the third segment. No artifact declares a subdomain.
   **The realization has already ruled the other way, in a code comment** —
   `artifact_index.py:217`: `owner_subdomain` is "IMMUTABLE once emitted … re-homing to another
   subdomain changes `module_path` and therefore requires a NEW version." `4c` §4.1 says the inverse:
   "A change of identity requires a governed determination, never a change of location." That is a
   genuine disagreement on a settled question, and `0z` §3 gives the resolution: the document governs
   and it is settled by ruling.
   **Do not "fix" this by deleting `module_path`** — an earlier draft of this handoff proposed
   exactly that and it is wrong; it would break both consumers. The question is whether subdomain
   ownership should be **declared in the machine block**, which is MB-1's subject and is flagged for
   `2c`.
5. **RESOLVED by the map — all four architectural invariants are settled.** AI-4 and AI-7 hold
   (and *why* they hold matters — see the map's §9); AI-14 is confirmed and narrowed to findings 10
   and 11; AI-16 is partial — independently checkable for integrity, not for determination.
   AI-6 was checked while there and is clean at construction, **but finding 29 breaches it at
   runtime**: the `IN_` admission gate admits unconditionally, which is inability to determine
   producing the same outcome as governance that permits.

5b. **The profile is the reflexivity term, and closing it takes two acts.** `2a` §6.1: without an
   externally claimed profile "a system could declare governance that approves of itself and be, by
   its own account, perfectly governed." **This is the highest-consequence finding in the map.**
   - **Act one — claim one.** Decide whether the profile is claimed by the assembler, by the build
     configuration, or by a selection step that does not exist. Claim
     `REFERENCE_PLATFORM_PROFILE_V1`, not the baseline: **the baseline is rotted, 23 of 35 FQDNs
     dead** (finding 33), and nothing distinguishes them today because nothing reads either.
   - **Act two — put its amendment outside the composition's authority.** NP-7's externality is
     authorship, not storage (finding 34). Claiming a profile the claiming system can change is the
     failure `6a` §6 names — the system declaring the standard it will be judged against.
   - **Cheap and immediate, regardless:** an FQDN-resolution check over
     `.github/snapshot_profiles/`, in the runbook. Three lines, and it would have caught 33.
6. **Two Part-II questions deliberately open**: whether Evidential is a peer semantic category, and
   whether provenance remains an independent axis. **Federation** is a relation among authorities
   with its ontological status open.
7. **Domain invariant authority — ruled yes, unbuilt.**
   `software_governance/doc/DOMAIN_INVARIANT_AUTHORITY_RULING.md`. A domain cannot express a
   *governed* constraint over subjects it owns. Authorship is granted only with (1) a
   domain-authorable constitution and (2) `GOVERNANCE_DECLARATION_RESOLVES` + `ASSERT_PARITY`
   reaching domain builds. **Build the precondition before the permission** — granting `INVARIANT` in
   `artifact_types` first yields more ungoverned invariants. Cost already paid: the workload's CT
   surface is no longer closed (its one invariant was withdrawn), so a third CT could be added and
   nothing would refuse it. `INVARIANT_CT_SURFACE_CLOSED_V1` cannot substitute — it carries the
   *platform's* allow-list.
8. **`pgs_*` survey — three classes deliberately unaddressed.**
   `software_governance/doc/PGS_REFERENCE_SURVEY.md`. **Class A (27 live keys)** stays untouched: a
   rename must move the compiler, the registry and the artifacts together and changes identities and
   hashes — its own change with its own reason, never a cleanup. **Class D (5 historical citations)**
   — keep the citation, fix the tense. **Class E (11 ungrounded prose claims)** — cheapest, safest,
   independent. **Never a blind sweep.**
9. **`MACHINE_BLOCK_CLOSURE.md` §4 is wrong and unenforced** — it says `core.enforcement_stage` is
   read by one handler; it is read by four. The one-line correction is not the fix: an unchecked
   prose description of machine consumption is the same defect dev/7 deleted from 14 invariants.
10. **`CLAUDE.md` is gitignored in every repo.** Every correction made to one is local-only and will
    not survive a clone. Decide whether that is intended. Related: `software_governance/CLAUDE.md`
    still asserts `pgc::` in four places, deliberately, pending issue 2's ratification.
11. **`standards` privacy residue.** A recovery-codes file is a standing violation awaiting
    `git filter-repo`.

### Transformation — design language and corpus

12. **A design can add and cannot deliberately remove.** Every future replacement hits this.
13. **The design language cannot state a dotted literal.** `BINDING_SOURCE_WELL_FORMED` admits
    `inputs.<field>`, `payload.<field>`, `results.<step>.<field>`, a bracketed literal, or a bare
    identifier. An operation identity is `si.store.list`, so a design cannot bind one. **The next
    design that must state an operation identity stops here.**
14. **A P7 section number must be an integer** — `4b` is a hard parse failure in the document reader.
    §18–§20 went at the end for that reason, right for them and eventually wrong for something.
15. **The dossier lifecycle vocabulary has no state for a governance change, and none for a closed
    gate.** Three P6-terminal dossiers stay `DRAFT` forever; cr_03 and `refusal_discharge` carry
    `DRAFT` / `PENDING GATE N APPROVAL` with both gates closed. Following the precedent keeps them
    comparable; a ruling would make either honest. Identity assignment is likewise ungoverned for a
    governance artifact.
16. **Two in-flight dossiers can each own one artifact, and the guard cannot see it.**
    `tc construction check --snapshot` refuses a narrowing amendment only against the dossier's own
    baseline. `THE_SHAPE_OF_A_CHANGE_V0` §8 rules when a dossier may be deleted rather than superseded.
17. **`TI_ACCEPT_ACTOR_V0` / `TI_REJECT_ACTOR_V0` let a caller decide what the system admits** —
    `states_admitting_a_decision` and `admitted_outcomes` come from the payload. The wallet's
    equivalent was corrected to a design-fixed literal; identity's was not. **It is a new CR against
    `blockchain::identity` and must not reopen `cr_04_wallet`** — a delivered dossier is never edited.
18. **Prohibition by absence is the one unbuilt refusal form.** Of the three sites a declared refusal
    is carried out — runtime discharge (§18), prohibition by absence, governance-surface discharge
    (§20) — the middle has no register. It needs a stable declared operation identity, going forward
    only. cr_02's *"Retire a work | Always."* supplies none, so its fixture stays historical and
    reads INADMISSIBLE at P7 permanently; that red is expected.
19. **A design named one artifact of the seven it amended** (`refusal_discharge`; eight by the next
    measurement). `WF_P1`–`WF_P7` all carry the register list, so a new register moves all of them.
    `CT_PURE_EVALUATE_RULES_V0`'s EXTEND row **and its generation-provenance row are both wrong** —
    it is produced by no generator and has never changed. **Wants a ruling**: correct the record, or
    write a rule refusing a design whose amendment set is incomplete. It is delivered, so not edited
    on a whim. General form is the next item.
20. **Amendment-set completeness for generated changes has no check.** A change that renders nothing
    has no Construction Completeness, so the omission in issue 19 passed 808 rules and was found by
    reading `git status`.
21. **A register costs five derived rules and no author sees that number.** P7 declares 20 registers,
    16 optional; each brings five rules. That is why mandate rule-count projections come out low
    (~157 projected, 179 actual). Computable at authoring time; nothing computes it. **A rule count
    in a mandate should either be computed or not stated.**
22. **Two rules still need a dossier, and its spec is written** —
    `transformation/doc/FEATURE_LEVEL_CLOSEOUT.md`. `UNDECLARED_REACH_READ` skips any act whose own
    binding the composition does not publish; `BORROWED_CAPABILITY_NOT_DECLARED_CROSSING` reconciles
    P6 against P5, and all eight P5 documents declare `cross_subdomain_refs` empty. The dossier
    extends a subdomain, names one borrowed CC at P5, carries it SATISFIED at P6, composes a contract
    reading another subdomain's store by bare name at P7, and leaves `declared_reach` empty in the
    probe cut from it. **Worth authoring for its own sake:** `declared_reach` was designed, delivered
    and never once filled.
23. **Five P7 rules remain undemonstrated because a correct check made a fixture useless as
    evidence.** Dropping a vocabulary-bearing column at P1 fires `CELL_NOT_IN_VOCABULARY` 39×;
    dropping `field_declarations` at P8 fires `SCHEDULED_ARTIFACT_UNPLACED` 42×. Both checks are
    working. These want a recut, not a new rule.
24. **Two counts of the composition exist and past handoffs have mixed them.** `tc baseline show
    --snapshot` counts the pin; the assembler's conformance line counts 398 over a wider set. **Quote
    the pin.** Left open deliberately — they count different things correctly.
25. **Judging a delivered CR's P7 or P8 against the current snapshot is meaningless.** The admissible
    cr_01 fixtures fire `NEW_CODE_ALREADY_EXISTS` 42× under a live `--snapshot` because cr_01 shipped
    and cr_02 amended its contracts. **A CLI run of these documents is not evidence** —
    `design/sealed.py` exists so the pin names the rule set.
26. **A corpus filename asserts a verdict true against only one baseline.**
    `admissible_p7_deferral_owned.md` is ADMISSIBLE in `e2e_phases_test` (CR-1's reproduced baseline)
    and INADMISSIBLE in `differential` (the current composition). Both correct; a standing readability
    trap.
27. **`tc construction emit` renders domain artifacts with no agreement check against the renderer.**
    `emit_rule_sets` and `author_transport_contracts` both have `--check`; nothing equivalent exists
    here. `construction_acceptance` compares against designs, which is a different question.
28. **Fixtures and delivered dossiers that read red, correctly.** `book_library_mgmt` cr_01/cr_02 at
    P0 and `blockchain` cr_01/02/03 are red from rules written after their approval. **Never edit the
    originals; do not re-migrate.** The testbed reads maintained copies at
    `transformation/scripts/testbed/fixture_dossiers/`. `ai_governance` has no dossier, deliberately.
    `TOUCHED_SUBDOMAIN_AUTHORS_NOTHING` is gated to NEW_SUBDOMAIN and EXTEND_SUBDOMAIN only.

---

## Architectural Concerns

- **The map is finding defects in the realization faster than in the spec, and that will invert.**
  Seven of eight findings are against the RI because `3b`, `4a` and `5b` specify subjects the
  realization built deliberately. Documents specifying subjects it approached without a specification
  — Part VI profiles, `3e` evidence, `4d` transformation — should yield the opposite ratio. If they
  do not, the map is being written to agree with the code.
- **Findings 1–5 are one defect seen five times.** The realization built its manifest as a
  *provenance record* — a chain establishing that the compiler, the assembler and the attestation
  agree about what was built — where `3b` and `4c` both require a *self-description whose identity is
  total over what it carries*. Closing any one in isolation produces a snapshot whose identity story
  is half-migrated.
- **The realization declares less than it enforces, in a specific direction.** Findings 6, 8 and 12
  are the same shape: a mechanism exists and works, and what it does is stated in Python rather than
  in a governed artifact. The fix has been demonstrated once already — `TI_SI_*` moved the inspection
  surface's metadata out of code so that re-pointing an operation "cannot happen silently in code."
  Projection contracts, read classes and the determinative/observational split are that same move,
  unmade.
- **The map must not become a specification.** It is evidence about one realization; `8a` §2 governs
  what such evidence establishes — notably that resembling the reference realization establishes
  nothing.
- **`parked_rulings.md` is the ruling record.** Findings resolved *against the specification* go
  there too. A ruling that exists only in a commit message will be re-litigated.
- **A declared invariant that passes is not an enforced invariant, and the only proof is tampering.**
  A check nobody has seen fail is a check nobody has seen.
- **A doctrine nothing can fail is not enforced, however plainly it is written.** The obvious
  encoding is usually a coverage count, and a coverage count reports zero gaps while the relation it
  was meant to guard is entirely absent. **A check has to name the relation it wants or it measures
  nothing.**
- **A field's name is a hypothesis about what it does; the deletion probe is the test.**
  `scope.applies_to` reads as "where this applies" and means "the surface whose allow-list I carry" —
  the difference between a three-line fix and a rebuild of closure admission.
- **An artifact is not a unit of liveness; a field is.** Ask of anything proposed for removal: which
  of its fields is dead, and which is merely unread by the thing you happened to look at? The
  compiler's own machine-block census (`compile_domain.sh --verbose`) already draws this line and
  distinguishes `○ preserved — declarative policy` from `⚠ candidate unconsumed`. **The next survey
  of this kind starts at `--verbose`, not at grep.**
- **A standing open item is a claim, not a fact.** `tc construction emit` was carried for several
  sessions as the last generator without an agreement check; measuring showed everything it writes is
  already compared, and what was unchecked was one level up.
- **The last hand-kept copy is the one that fails.** Ask of anything generated: what does a person
  still have to keep in step by hand?
- **Adding a register to the design language invalidates every document written before it.**
  `REGISTER_MISSING` fires on an absent optional register. Established practice is to backfill the
  maintained fixtures and let the originals stay red — undocumented, inferred, and the reason a green
  suite says nothing about the delivered corpus.
- **Nine admissible phases do not make a buildable design, and only construction knows.**

---

## Build & Test Status

**PASSING.** Run this session:

```
pgc_env_check            PASSED — no RI-0 dependency reachable
implementation_closure   PASSED — 27 transforms, every module named and present
snapshot                 7b6f2699…ea9ba3f0 · 7 domains · conformance PASSED (5 rules / 398 artifacts)
```

The full suite was last run at the release-9 cut and is unaffected by a documentation session; see
`.github/process/notes/release-9.md`. All ten composition repos are clean. `standards` carries two
uncommitted changes: `spec/8a_implementation_guidance.md` (§6 rewritten) and the new `doc/`.

### The runbook, in order

```bash
python .github/process/governance_closure.py                 # two relations nothing else checks
python .github/process/governance_chain_closure.py           # declare/resolve/parity, wherever an invariant may be authored
python transformation/scripts/emit_rule_sets.py --check      # first — it sees param drift the others cannot
PYTHONPATH=snapshot_inspector \
  python snapshot_inspector/scripts/author_transport_contracts.py --check
python transformation/scripts/testbed/meta_test.py
python transformation/scripts/testbed/differential.py
python transformation/scripts/testbed/e2e_phases_test.py
python transformation/scripts/testbed/projection_test.py
python transformation/scripts/testbed/construction_acceptance.py
python .github/process/implementation_closure.py
PYTHONPATH=snapshot_inspector python snapshot_inspector/scripts/testbed/test_inspector.py
protocol_runtime/run.sh run --wf workload::WF_COLLATZ_CONJECTURE_V0 --payload <file> --data-root <abs path>
protocol_runtime/run.sh run --wf ai_governance::WF_GOVERN_AGENT_ACTION_V0    --payload <file> --data-root <abs path>
protocol_runtime/run.sh run --wf ai_governance::WF_PROVISION_AI_LICENSING_V0 --payload <file> --data-root <abs path>
python business_domains/book_library_mgmt/testbed/catalog/execution_validation.py
python business_domains/book_library_mgmt/testbed/catalog/execution_validation_cr02.py
python business_domains/blockchain/testbed/identity/execution_validation.py
python business_domains/blockchain/testbed/wallet/execution_validation.py
python .github/process/pgc_env_check.py
```

Full runbook is `.github/process/RUNBOOK.md`, which carries the payload paths and the seed step
`ai_governance` needs before its first run. **Run identity's validation before the wallet's and into
the same data root** — one domain has one place its records live, and the wallet suite refuses only
its own stores being non-empty.

A clean rebuild is `protocol_compiler/compile.sh`, then `compile_domain.sh` for every domain root
carrying a `STRUCTURE_BUILD_*_CONFIG_V*.md`, then `snapshot_assembler/assemble.sh` — the build gate
inside `.github/process/release.sh`, without the release.

### Judging a dossier

Each phase reads only its **declared** priors, and passing an undeclared one is a hard error:

```
p1←p0   p2←p1   p3←p2   p4←p3   p5←p0   p6←p0,p5   p7←p5,p6,p0   p8←p7
```

P0's document is the **seed**, not `p0_business_problem_statement.md`. A phase run without a prior it
declares does not quietly pass — it reports that the handoff was unchecked.

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

**Guardrails that cost something to learn.** A delivered dossier is never reopened — raise a new CR.
A survey classifies *fields*, not artifacts. A check that has never been observed to fail is evidence
of nothing.

---

## Next Session Should Start With

**Decide Open Issue 1** — whether `standards/VERSION` becomes `draft-2`. It is two minutes and it
gates every further spec edit, including the `8a` §6 change already made.

**Task A, the ruling pass, and `draft-2` are done. Every remaining finding is realization-side.**

**Task C is delivered.** `software_governance/doc/HUMAN_BLOCK_TEMPLATE.md` states the three-layer
split — normative standard (what PGC requires) → human realization document (how this artifact
realizes it) → machine block (what the implementation consumes) — and the three rules that keep the
middle layer from becoming a second specification: **cite never restate**, **never restate a
machine-block value**, **say what is not claimed**.

Applied: **216 `## Header` blocks removed** (~1,265 duplicated lines), 44 prose `Version History`
sections dropped, 224 normative-sounding sections renamed. `.github/process/human_block_fidelity.py`
enforces what is checkable and is in the runbook; it was **red on arrival at 1,761 findings across
340 of 393 artifacts** and both its rules are proved by probe. §3.1 — whether a sentence cites or
restates — is a reading, not a pattern, and is stated as a review obligation rather than claimed.

**One recorded exception to "nothing outside a machine block is read by any mechanism":** TEST_DATA
declares its cases in per-case fenced yaml blocks that `assert_ct_test_data_outcome_declared_v0`
parses out of the body. That is a governance determination reading a second surface (MB-1). Not
fixed here — moving those cases is a change to governed content, not to prose.

**Start with Task B**, which the map now equips. GO-11, MB-7, ID-12 and **CA-1** are all recorded with what
the realization does instead; CA-1 is the operative constraint — seven things separately determinable,
and the current identifier carries at least three. Add the profiles to the migration's blast radius
(finding 33).

**Two cheap measurements worth running before either**, both with precedent in this workspace:

- **The assertion-handler census** (finding 42) — how many of 85 have ever been observed to refuse?
  The design compiler ran exactly this on its own rules and it found real defects.
- **An FQDN-resolution check over `.github/snapshot_profiles/`** (finding 33) — three lines, and it
  would have caught a conformance contract that stopped naming the system years ago.

**Task B is now unblocked on the map's side.** `2b`, `2c`, `2e` and `4c` are all mapped, so GO-11,
MB-7, ID-12 and CA-1 — the four requirements step 2 must satisfy — are each recorded with what the
realization does instead. **CA-1 is the operative one**: seven things separately determinable, and
the current identifier carries at least three. That is the design constraint for the canonical
representation, and it is now written down rather than inferred.

**Both probes are run and recorded in the map's §11.** No repository and no sealed snapshot was
modified; the composition verified unchanged afterwards at `7b6f2699…`. One probe sharpened a finding
and one withdrew a claim, which is the argument for running them rather than reasoning about them.

**Do not open Task B yet.** `4c` is now mapped and confirms ID-12, but the map has not reached `2b`,
and B's step 2 is a canonical representation for a requirement stated across GO-11, MB-7 and ID-12.
Two of the three are mapped; the third is one document away.

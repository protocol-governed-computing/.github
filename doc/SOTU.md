# SOTU Handoff

## dev/11. **Task E — Draft-2 closure and independent-implementability audit.**

Read this cold: it is self-contained and forward-facing. Nothing about how dev/10 got here is
restated — `.github/process/notes/release-3…10.md` carry what each release did, and
`.github/doc/parked_rulings.md` is the ruling record. Read the latter before reopening anything that
looks unsettled.

---

## Where things stand

```
composition   snapshot_id 39d6f73e9b3a9a530b4622c5c11a3bff1d4a4618c3b745247ba87f5f134741c7
              PASSED — 5 rules over 410 artifacts · identity stable across rebuilds
standard      standards on draft/2 · VERSION draft-2 · 2 changes declared in doc/revisions.md
domains       ai_governance, blockchain, book_library_mgmt, inspection,
              platform, transformation, workload
```

Release 10 is cut, or is one commit from it. `release.sh` now writes `VERSION` on every repo as its
last step, so `dev/11` opens already declaring `11` — do not hand-edit a version anywhere.

**A rebuild reproduces its identity.** That was false for the whole of dev/10 and is the property
everything else now rests on: a pin taken from here survives a rebuild.

---

## Build & Test Status — PASSING

```
composition            PASSED (5 rules over 410 artifacts)
clean rebuild+assemble ok — reproduces 39d6f73e…
workspace checks       8/9 — env · implementation · governance · chain · frontmatter ·
                       human block · supersession · evidence determinism
transformation suites  meta · projection · e2e (83) · differential · acceptance   5/5 PASS
domain execution       catalog 23/23 · catalog cr02 21/21 · identity 15/15 · wallet 9/9
```

**One check is red by design:** `admission_contract_fidelity` — 31 findings over 31 gates, all in
other domains' business surface plus `IN_REGISTER_BOOK_V0`'s `subject`. Deferred with ground
recorded; see Open Issues 6.

---

## Task E — what it is

The question has changed. Through dev/10 it was *what is wrong?* It is now:

> **Is the standard semantically closed enough that an implementation team would not have to invent
> anything important?**

Task E establishes that Draft-2 is a coherent, implementation-independent specification. It is not a
prose pass. Six passes, in order — E0 gates the rest, and E2 and E4 are the load-bearing ones.

### E0 — Resolve the standing rulings

**The four open rulings are not cleanup. Two of them can invalidate the E4 audit if left open**, and
a ruling is the maintainer's act — nothing below can be done on the maintainer's behalf. Full
statements in Open Issues; what each needs:

- **Ruling 3 (build manifest) first.** It is not *where the manifest lives*. It is **does the
  governed design schedule the manifest's production, or is production construction machinery
  outside the governed design?** That decides how a new domain becomes discoverable. Defer it and
  E5's implementer asks *"how does my constructed domain join the executable system?"* and we invent
  an answer at the worst possible moment — which is the exact failure E4 exists to prevent.
- **Ruling 2 (attestation) is already answered better than the question was asked.** See below; it
  needs ratification, not deliberation.
- **Ruling 1 (expired-pin approvals) is a history question, not a staleness question.** An approval
  made against an identity that was later found unstable is not thereby invalid: if what was
  approved has not changed, the approval anchors to the identity *at the time of approval*.
  Invalidating them would destroy historical governance records because a later identity
  representation changed. Rule it deliberately; it reaches every completed change in the workspace.
- **Ruling 4 (defaults) is effectively settled** — `construction_determinacy` ruled that
  overridability is a difference in remedy, not in what happened. Record it as settled and do not
  reopen it absent a contradiction elsewhere.

### E1 — Reconcile the change register

Two registers already exist and neither is the whole picture: `standards/doc/revisions.md` declares
what changed in the *document* (two changes), and `realization_map.md` §28 disposes of all 44
findings (17 closed, 3 revised, 5 in CR, 2 deferred, **17 open**).

What is missing is small and specific: the seventeen OPEN rows have no standard-side column, so
nothing says whether each is an RI absence, a profile absence, or a document defect. **Do not build a
third register.** Add the disposition to §28's open rows and close the loop there.

**Finding 44 is the pending third document change** — `4e` §22.3, a supersession is complete inside
the composition and silent outside it. It is ruled and unwritten. Write it as Change 3 in
`revisions.md`.

### E2 — Cross-document semantic closure

Nothing in the repository does this, and it is where the dangerous defects are. Documents have been
reviewed individually and against their immediate neighbours. Never end to end.

Trace each major concept from its introduction through every document that relies on it, and ask
whether it survives without a semantic break:

```
authority → governance relation → closure → obligation → assertion → rule → refusal
         → execution → snapshot → evidence → inspection → conformance
```

Produce a **semantic dependency matrix** — concept · defined in · constrained in · consumed by ·
disposition. `0z` §3 (the derivation rule) already governs how a requirement may derive across
documents; the matrix is that rule made checkable rather than a new frame.

**The defect this finds:** a concept exists, and the standard never says what happens when it is
absent, ambiguous, invalid, contradictory, or changed.

### E3 — Fold into E1, do not revive the map

**The realization map is retired and records its own retirement.** Its stated ground: the mechanism
that found all three specification defects was *implementation under literal reading*, and that
mechanism needs no map. Re-running it as verification is a new hypothesis and would have to overturn
that ruling on the record first.

The verification it wants is cheaper as E1 — a status pass over §28's seventeen open rows. The
discovery it wants is E4, which is what the retirement note actually asked for.

### E4 — Independent-implementability audit

**The strongest single item in Task E, and the one that answers "how do we know we are done."**

An adversarial reading of Draft-2 alone, with the RI treated as nonexistent: *what would I have to
invent?* For each normative requirement — what is the input, what determination is required, what
constitutes satisfaction, what constitutes refusal, what state is authoritative, what happens when
information is absent, when two declarations conflict, what persists, what is observable, what is
evidence, and what is merely an implementation choice.

Classify every answer:

| | |
|---|---|
| **A** | specified — the standard tells the implementer what they need |
| **B** | deliberately implementation-defined — semantic boundary stated, mechanism open |
| **C** | profile-defined — the universal standard does not decide it; a profile does |
| **D** | **missing semantic decision — the implementer must invent something** |

**Zero D's is the done criterion.**

**Prerequisite nobody has named:** C has no instances to point at. Map findings 35 and 36 are open
because **no execution environment profile exists and no domain profile exists for any of the six
domains** — `6b` and `6c` have no realization. An audit will push every intentional gap into a
profile that does not exist, so the profiles have to be written or C collapses into D.

### E5 — A small independent implementation challenge

Not another full implementation. Give a competent implementer Draft-2, the applicable profile, one
small governed workload and its conformance requirements — and **not** the RI, its architecture, or
its artifact inventory. Can they build the minimum conforming system without asking a semantic
question?

**Record every question.** *"What encoding should I use?"* is fine. *"What happens when X and Y
conflict?"* is a Draft-2 defect. That distinction is the instrument.

This one depends on a person who is neither the maintainer nor an agent that has read this
workspace. Treat it as a dependency to arrange, not a task to schedule.

---

## The process question, and what the standard says about it

`0z` §5.1 is explicit: **"Who proposes, reviews, and admits a revision is a property of whoever
maintains this family, not of the family itself."** The standard deliberately declines to define its
own amendment process. So the process is the maintainer's to declare, and it cannot live in `spec/`.

What already holds and needs no invention:

- **A change to `spec/` is a declared revision** against a named predecessor, stating what it changes
  and what that invalidates — `4e` §9, recorded in `doc/revisions.md`. `VERSION` alone declares
  nothing.
- **A realization may occasion a revision and may not decide one** — `0z` §5.1. Editing a normative
  document to match what was built is forbidden by `0z` §3, *except* where the finding is against the
  document.
- **A finding is resolved by ruling, by a change, or by deferral with its ground stated** — §28's
  own rule.

What is undeclared and should be written down this cycle, in `standards/CLAUDE.md` or a maintainer
doc beside it: **what occasions a change now that the map is retired.** With the draft public, the
second legitimate occasion under `0z` §5.1 becomes real — a reader who could not derive the
semantics. Nothing in the repository receives external critique today.

**Recommendation:** declare it as one paragraph — a finding register for the standard, an occasion
(realization refusal, or a reader who had to invent), a ruling, a declared change, and a draft cut
when a coherent batch lands. Then Draft-3 supersedes Draft-2 the way Draft-2 superseded Draft-1.

---

## The exit gate — Draft-2 is complete when

1. **Normative closure.** Every concept is defined, constrained, and states its refusal semantics.
2. **Cross-document closure.** No document depends on an unstated assumption supplied by another.
3. **Realization closure.** No open finding without a disposition. *(Stated against §28, not against
   a revived map.)*
4. **Implementation neutrality.** No requirement depends on Python, repository layout, component
   names, compiler stages, the current artifact inventory, or the current encoding.
5. **Profile closure.** Anything intentionally outside the universal standard has an explicit home in
   a profile rather than being silently invented.
6. **Machine-processability.** Requirements are identifiable, traceable and testable. *(Closest to
   met — every invariant already carries a document-prefixed identifier.)*
7. **Independent-implementability audit** produces zero D's.
8. **The implementation challenge** raises no question that is not an implementation choice, a
   profile choice, or an explicitly permitted degree of freedom.

**Two stopping points, not one.** Gates 1–7 earn *Draft-2 semantically closed and ready for
independent implementation challenge*. Only gate 8 earns *implementation-independent readiness
demonstrated*. Do not collapse them: passing the document gates is the maintainer marking their own
work, and E5 is the only evidence produced by someone with nothing invested in the answer.

**Then freeze.** Stop revising the normative standard in response to this RI. The RI becomes *one
conforming implementation of the standard* rather than *the thing the standard is inferred from*.
That transition is the point of the whole exercise — and the stopping rule does not require building
a second RI, only an independent implementer failing to find anything important left to invent.

### Not this cycle

No second large implementation. No paragraph polishing. No expanding the standard because the RI has
another mechanism. No chasing textual correspondence. **Never use the RI as the oracle for an
unresolved semantic question** — that is the failure `0z` §3 exists to prevent.

---

## Open Issues

### Rulings waiting on you

1. **Do approvals recorded against expired pins still stand?** They failed because the identity was
   unstable, not because anything they name changed. Reaches every completed change in the workspace.
2. **Does an attestation belong to the composition it attests, or accompany it?** **`composition_identity`
   P3 Q1 answers that the question is malformed at file grain: "an attestation both constitutes and
   accompanies, and the file is the wrong unit to decide about."** Two of its fields bind what was
   built — the projection and a value over it — and the runtime refuses a composition whose
   projection does not match them, so those *constitute*. One field records when signing happened,
   is read by nothing, and changes every build; that *accompanies*. Hence the exclusion is of a
   **field, not a file** — excluding the file would drop a binding the runtime enforces.
   **No circularity arises today** because the signature, algorithm and key reference are
   placeholders; §28 finding 13 defers making the signature real as its own change, and that is
   where circularity would actually have to be resolved. Ratify, do not re-litigate.
3. **Does the governed design schedule the manifest's production, or is production construction
   machinery outside the governed design?** **Load-bearing: a genuinely new domain has no way to
   become discoverable until this is answered.** Construction stopped founding a manifest because it
   took its domain from the namespace of the first scheduled artifact — invisible for a business
   domain where the two are one word, wrong for the platform, where one domain carries a namespace
   per concern. Whichever way it is ruled, the standard then owes a semantic relationship
   `design → construction → manifest → discoverability` **without making the manifest business
   governance.** Existing domains are unaffected; E5 would found a domain, so this is E0's first act.
4. **Does a default count as a fact the design determined?** `construction_determinacy` rules that it
   does not; overridability is a difference in remedy, not in what happened.

### Named for another subdomain, not deferred

5. **`schema_governance`'s five descriptions.** Three drifted, owned by `actor`, `event` and
   `intent`; two absent, owned by `transport`.
6. **`IN_REGISTER_BOOK_V0` under-declares `subject`.** Requiring it breaks every present caller,
   which the seed forbids. Its own CR, where the boundary and its callers move together. This was
   ruled the other way first, emitted, and overturned by execution.
7. **The seventeen enforcement obligations** across six subdomains. They are what arms
   `INVARIANT_ASSERT_CAPABLE_OF_REFUSING_V0`, which sits at `declared_not_enforced` until they are
   restated.

### Standing limits of the design language

8. **A design can add and cannot deliberately remove.** Every replacement hits this; versioning is
   the pattern.
9. **A leaf-walking measure cannot see a fact that is a path.** A vocabulary's group is a key, not a
   value. A group undesigned where the casing is stated would pass.
10. **The design language cannot state a dotted literal.** An operation identity is `si.store.list`,
    so a design cannot bind one. The next design that must stops here.
11. **A P7 section number must be an integer.** `4b` is a hard parse failure in the document reader.
12. **The dossier lifecycle vocabulary has no state for a closed gate**, so closed dossiers stay
    `DRAFT`.
13. **Two in-flight dossiers can each own one artifact and the guard cannot see it.**
    `THE_SHAPE_OF_A_CHANGE_V0` §8 carries the doctrine; nothing enforces it.

---

## Architectural Concerns

- **The realization declares less than it enforces.** A mechanism exists and works, and what it does
  lives in Python rather than in a governed artifact. The construction origins are declared *in the
  renderer* and the artifact declaring them is still unwritten. **This is gate 4's shape, inside the
  RI.**
- **Every one of the 87 handler registry keys is a `pgs_governance.*` path.** They resolve because
  the binding is by string against a registry, not by import — but the identity every obligation
  gives its check names a namespace that was severed.
- **`CONSTITUTION_ASSERT_V0` names carriers that do not traverse.** A constitution can name a carrier
  that does not exist and nothing objects.
- **Seven of 229 design rules have never been observed to refuse anything** (finding 40). The
  standard-side counterpart is E4's question, asked from the other end.

---

## Next Session Should Start With

**E0, ruling 3 first** — does the governed design schedule the manifest's production, or is that
construction machinery outside the design? Nothing else in Task E can be finished around it: it is
the one open ruling that leaves a real question with no answer in the document, which is precisely
the class of defect E4 is built to count.

Then ratify 2, rule 1, record 4 as settled. Only then E1, whose first writing act is **Change 3** —
`4e` §22.3, a supersession is complete inside the composition and silent outside it, ruled and
unwritten — declared in `standards/doc/revisions.md`, before E2 traces `supersession` through the
matrix and traces the uncorrected text.

```
standards/spec/           31 documents, 0z is authoritative on structure — read it before editing
standards/doc/            revisions.md (declared changes) · realization_map.md (retired, §28 register)
.github/doc/              parked_rulings.md (the ruling record) · this file
.github/process/notes/    release-3…10.md — what each composition was
~/omnibachi-site/         papers, Field Manual v1, blog #22, the LinkedIn open-standards series
                          — its own repo, outside this workspace and outside release.sh
```

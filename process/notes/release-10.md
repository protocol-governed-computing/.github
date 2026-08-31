release 10 — declared ≠ implemented ≠ enforced ≠ demonstrated

Release 9 removed the standard from the composition so it could be versioned independently. This
release is what that made possible: the first cycle spent measuring the realization against the
standard rather than extending either one. The snapshot moves from `7b6f2699…` to `39d6f73e…`, and
composition conformance passes over 410 artifacts rather than 398.

Every finding below is one sentence in five forms. A rule can be **declared**, and code can be
**implemented** to carry it, and that code can be **enforced** — able to refuse something — and the
refusal can be **demonstrated**. Those are four states, not four words for one state, and a system
sitting in any of them presents from outside as though it were in the last.

## A rebuild reproduces its identity

This is the most consequential change in the release, and it was true of nothing before it.

A composition's identity is computed over the bytes of everything it carries, so that tampering and
relocation are detectable. Two compiles of unchanged source wrote ninety-one files each; ninety were
byte-identical. The ninety-first differed in one field — `signed_at`, a microsecond timestamp
recording when the build ran, read by nothing.

The consequence was total. **Twenty of twenty-two pins in the workspace could not be verified**, every
baseline expired on the next rebuild, and a genuine alteration was indistinguishable from a no-op
recompile — precisely what an identity over bytes exists to prevent.

The exclusion is at the grain of a field, not the file: the attestation's projection binding is
enforced by the runtime and has to stay a constituent. A pin taken from here survives a rebuild.

## The checks that could not refuse

Of eighty-seven compile-time assertion handlers, **fourteen have no path that produces a violation**,
for any input. Ten say so in their own prose — *"Phase 1 stub — full enforcement in Phase 3"*. All
fourteen declare `violation_response: FAIL_IMMEDIATELY`, all fourteen run on every build, and all
fourteen report passed, indistinguishable in the record from the seventy-three that can refuse.

The obligation guaranteeing parity between declaration and check, `INVARIANT_ASSERT_PARITY_V0`, sits
in `_OBSOLETE_DERIVED_ASSERTS`: published, declaring `FAIL_IMMEDIATELY`, evaluated by nothing, with
zero consumers. The guarantee that every obligation has a check was satisfied by a check that carries
nothing.

`VOCAB_ENFORCEMENT_STATUS_V0` and its mechanism are delivered, and the obligation schema now admits
the stages it declares — the capability had authored a vocabulary that nothing could use, and that
was found only by authoring the governance rather than designing it. The seventeen restatements
belong to six other subdomains and are named, not scheduled.

## The profile nobody read

A snapshot claimed a conformance profile and nothing read it. `REFERENCE_PLATFORM_PROFILE_V1` and the
rotted baseline it superseded were indistinguishable from inside the build, though twenty-three of the
baseline's thirty-five required artifacts no longer resolved.

The claimed profile is now read by identity and evaluated at assembly. The reference profile passes
with nothing unmet; the baseline is refused with twenty-one.

## Coverage is not governance

A third of the composition was described by no schema. Three descriptions had drifted, unread. And one
artifact kind *was* dispatched to a schema — one requiring no field and closing no surface, which
thirty-three declarations passed because everything passes it. On any count of dispatched kinds, that
kind read as governed.

`schema_governance` delivers the disposition vocabulary and a drift report. The five descriptions
themselves are named for the subdomains that own their kinds — `actor`, `event`, `intent` and
`transport` — because what a declaration admits is each owner's to state.

## Construction counted presence, not provenance

Construction Completeness tested whether a leaf was non-empty, so a value the renderer supplied from a
literal passed as a value the design stated. Three origins are now declared beside the renderer that
reports them, a fourth (`carried_from_predecessor`) lets an amendment preserve prose the design has no
way to speak about, and `requirements()` tests provenance rather than presence.

The fix refused itself on first run: `INVARIANT_CT_SURFACE_DERIVED_CLOSED_V0`, written hours earlier,
caught the new provenance transform declared and invoked by nothing. Two other rules written the same
day caught two more — an artifact naming a module that did not exist, and a stage list stated twice
that disagreed the moment the first copy was extended. That is the best evidence this cycle produced
that the rules work.

## The federation-boundary prefix is retired

Governance namespaces carried an `fb.` prefix denoting a *federation boundary* — a claim of distinct
sovereignty. Measured against the composition, all twenty-six were one authority's concerns, and the
six candidates for genuinely distinct authorities carried no prefix at all: the marker for "separate
sovereign" sat on everything that was not one.

What it was carrying is now declared as two fields in every machine block — `authority`, from whom
jurisdiction derives, and `concern`, the semantic subject, which confers nothing. An authority must be
constituted by a declared constituting act, and no value may be both. Neither could be checked while
one identifier carried both: a check could refuse an *unlisted* namespace but never an *illegitimate*
one, because the two were the same string. The migration moved 1,407 occurrences.

Human blocks were realigned in the same pass. About 1,265 lines restating machine-block fields in
prose — kind, governing constitution, version, status, supersession — are gone, along with prose
version histories. A supersession is a declared relation; a paragraph claiming one is a second place
for it to be wrong.

## The standard was wrong three times

The realization map covers twenty-five normative documents. Its purpose was to find where the
implementation fell short of the standard, and its most valuable findings ran the other way.

- **SU-5 and SU-3.** SU-5 requires that a superseded identity be referenced by nothing — *"no
  reference, not no executable reference."* SU-3 requires the supersession relation to be declared on
  the successor as `supersedes: <predecessor identity>`. Read literally, a conforming supersession is
  impossible: one rule mandates the single reference the other forbids. The closure check had carried
  a two-line exception and a comment explaining why for months.
- **TR-17.** Ruled and the document corrected.
- **SU-9.** The catalog harness invoked a workflow that had been superseded and was refused by it, for
  as long as the supersession existed — correct behaviour by an artifact nobody had told it was
  retired. **A supersession is complete inside the composition and silent outside it.** Superseding
  does not redirect a caller; the caller moves.

Each was found by trying to conform and failing. In all three the realization needed no change and the
document did.

## The map is retired, and records its own retirement

Its value was the attempt, not the document. The mechanism that found the three specification defects
was implementation under literal reading, and that mechanism needs no map. The seventeen findings it
leaves open are absences with recorded ground, each a change request when somebody wants one. It
should not be extended.

The question it never asked of the standard is the one worth asking next: how many of the standard's
invariants could be violated by a realization that looks conformant? Seven of two hundred twenty-nine
design rules have never been observed to refuse anything.

## What this release does not settle

Four rulings are open and recorded, and one of them is load-bearing: **construction no longer founds a
build manifest, so a genuinely new domain has no way to become discoverable** until it is ruled
whether a build manifest is something a design schedules at all. Existing domains are unaffected.

`admission_contract_fidelity` remains red by design with thirty-one findings, all in other domains'
business surface. The seventeen enforcement restatements and `schema_governance`'s five descriptions
are named for their owners. Historical pins still mismatch — legitimately, because the composition
genuinely changed rather than because the identity moved on its own.

# NPP-E Findings Register

Family revision: `14d54013494da27e43362d29ce15059c6fce5f21`

These matters are not silently treated as family requirements. NPP-E avoids claims that require an
unresolved matter unless this register states the author selection used.

## F-01 - Exact artifact-kind taxonomy is not supplied

**Matter:** complete set of artifact kinds for a concrete platform.

**Source basis:** `2d` §§1, 9, 10; `6a` §7.

**Claim type:** unresolved.

**Reasoning:** `2d` defines the vocabulary mechanism and delegates enumeration to a profile. The
family supplies artifact-bearing examples but no canonical complete kind list. This prevented
treating any larger taxonomy as family-required.

**Confidence:** high.

**Disposition:** NPP-E makes an author selection and closes its own five-kind vocabulary; the choice
is not reported as a family determination.

## F-02 - Identity syntax and canonicalization are not specified

**Matter:** concrete syntax and canonicalization algorithm for identity.

**Source basis:** `4c` §§2.2, 8; `2c` §3; `3b` §4.

**Claim type:** unresolved.

**Reasoning:** The documents require identity over the semantic object and require a canonical form,
but do not name a syntax or scheme. This prevented citing a family-defined identity format.

**Confidence:** high.

**Disposition:** NPP-E selects one system namespace and canonical semantic-object normalization,
without claiming the family selected either.

## F-03 - Trust-root content is not supplied

**Matter:** external thing a checking party accepts axiomatically.

**Source basis:** `3e` §§6.2, 12; `6a` §7.

**Claim type:** unresolved by family, decided by author for NPP-E.

**Reasoning:** The family expressly supplies no trust root. Without a profile selection, attestation
chains would terminate differently for different checkers and the supported evidence claim would
not be fixed.

**Confidence:** high.

**Disposition:** NPP-E names its externally published profile artifact at the supplied revision as
the sole trust root.

## F-04 - Evidence retention period is not supplied

**Matter:** duration for which past determinations remain checkable.

**Source basis:** `3e` §11; `6a` §7.

**Claim type:** unresolved by family, decided by author for NPP-E.

**Reasoning:** The family states the consequence of retention and delegates the period to profiles;
it does not provide a duration. This prevented treating indefinite or finite retention as universal.

**Confidence:** high.

**Disposition:** NPP-E selects lifetime plus ten years.

## F-05 - Ontology questions explicitly remain open

**Matter:** whether Evidential is a peer category, provenance remains an independent axis,
Participatory is primary, and federation is only a relation or also a subject.

**Source basis:** `2b` §10.

**Claim type:** unresolved.

**Reasoning:** The ontology records these questions as unresolved and requires later demonstration.
This prevented claiming that NPP-E resolves them merely by naming categories.

**Confidence:** high.

**Disposition:** NPP-E uses existing category names, supports no federation or multi-authority claim,
and does not decide the ontology questions.

## F-06 - Capability realization correctness remains outside the contract

**Matter:** whether a realization computes what business intent requires while satisfying its
contract.

**Source basis:** `3d` §7; `4a` §4.1; `7a` §11.

**Claim type:** unresolved for this profile claim.

**Reasoning:** The family expressly leaves this residue to validation against declared intent. This
prevented NPP-E from claiming business correctness from capability or execution conformance.

**Confidence:** high.

**Disposition:** NPP-E excludes a business-adequacy claim and requires separate real-state proof for
transformation claims.

## F-07 - Demonstration fixtures are not supplied

**Matter:** concrete proposals, authorship records, malformed snapshots, and other fixtures used to
discharge claims.

**Source basis:** `7b` §§6, 8-9, 11; `6a` §7.

**Claim type:** unresolved by family, selected by author for supported claims.

**Reasoning:** `7b` requires fixtures to be declared and identified but does not supply their
identities. This prevented asserting that a demonstration is discharged without named material.

**Confidence:** high.

**Disposition:** Genesis fixtures are named in NPP-E §9; other claim attempts must supply identified
fixtures and report any unrun or failing demonstration.

## F-08 - No family-defined outcome names exist

**Matter:** names of capability outcomes in a concrete profile.

**Source basis:** `3a` §14; `3d` §§3.2, 11; `6a` §7.

**Claim type:** unresolved by family, decided by author for NPP-E.

**Reasoning:** The family requires a closed enumerated vocabulary and declared failure routing but
does not reserve or enumerate names. This prevented treating `completed` or `failed` as universal
family vocabulary.

**Confidence:** high.

**Disposition:** NPP-E selects the two names and keeps them distinct from governance refusal.

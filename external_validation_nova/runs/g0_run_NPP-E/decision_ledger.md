# NPP-E Decision Ledger

Family revision: `14d54013494da27e43362d29ce15059c6fce5f21`

Each entry records one author determination in the commission's required shape. Commission-fixed
scope is recorded separately in `list_assumptions`.

## Determinations

### D-01 - Profile identity

**Matter:** identity of the profile.

**Source basis:** `task_author_a_profile.md` §2; `6a` §9.

**Claim type:** expressly required by source.

**Reasoning:** The commission assigns `NPP-E`; a profile must have an identity and an obligation
change requires a new identity.

**Decision:** identity is `NPP-E`; family revision is the supplied revision.

**Confidence:** high.

### D-02 - Admitted artifact kinds

**Matter:** which artifact kinds are admissible.

**Source basis:** `6a` §7; `2d` §§2, 9, 10; `1a` §§3.1, 6; `2c` §7.1; `5b` §4.

**Claim type:** expressly permitted by source, with author selection.

**Reasoning:** The family delegates enumeration to the profile. The selected kinds correspond to
artifact-bearing subjects named by the family; declaration elements remain inside their owning
artifact.

**Decision:** close `NPP-E.artifacts` with `constitution`, `governance-element`, `workflow`,
`capability-contract`, and `read-operation`.

**Confidence:** medium.

### D-03 - Governance assertion per kind

**Matter:** whether each admitted kind requires a governance assertion.

**Source basis:** `2c` §8; `2d` §5.1; `6a` §7.

**Claim type:** expressly required by source, parameterized by author.

**Reasoning:** A vocabulary must state the disposition for every kind. Root governance may omit the
assertion only at genesis; all ordinary kinds require it.

**Decision:** `constitution` omits only at genesis; every other admitted kind requires it.

**Confidence:** high.

### D-04 - Capability outcomes

**Matter:** the closed outcomes contracts may declare.

**Source basis:** `3a` §§4, 4.2, 4.4; `3d` §§3.2, 4; `6a` §7.

**Claim type:** expressly permitted by source; chosen by author.

**Reasoning:** The family requires enumerated outcomes and declared failure routing but leaves the
vocabulary to a profile. `completed` and `failed` cover the selected narrow capability surface;
governance refusal remains distinct.

**Decision:** admit only `completed` and `failed` as capability outcomes.

**Confidence:** medium.

### D-05 - Projection selection

**Matter:** which projections the system carries.

**Source basis:** `4b` §10; `4b` §12; `6a` §7; `3b` §§5-6.

**Claim type:** expressly permitted by source; chosen by author.

**Reasoning:** The selected canonical form, identity index, address-resolved form, structural
rendering, vocabulary view, and evidence view are named projection realizations and support the
profile's execution and inspection claims.

**Decision:** require all six listed projections with individual contracts and provenance.

**Confidence:** medium.

### D-06 - Namespace arrangement

**Matter:** namespaces and their arrangement.

**Source basis:** `4c` §§5-6; `6a` §7; `GO-11`.

**Claim type:** expressly permitted by source; chosen by author.

**Reasoning:** The profile may narrow the open namespace arrangement. One system-wide namespace is
sufficient for the one-system scope and keeps identity, authority, and concern separate.

**Decision:** use one namespace, `NPP-E.system`, with identity-only addressing and no aliases.

**Confidence:** medium.

### D-07 - Integrity mechanism

**Matter:** integrity mechanism for canonical content.

**Source basis:** `2c` §3; `3b` §§6, 13-14; `3e` §12.

**Claim type:** expressly permitted by source; chosen by author.

**Reasoning:** The family requires a canonical-form integrity value but leaves the mechanism open.
The profile selects SHA-256 to make checking determinate without making the mechanism authority.

**Decision:** SHA-256 over the canonical semantic object; whole-integrity coverage excludes the
whole-integrity value itself.

**Confidence:** medium.

### D-08 - Trust root

**Matter:** what a checking party accepts as a trust root.

**Source basis:** `3e` §§6.2, 12; `6a` §7; `EV-10`.

**Claim type:** expressly permitted by source; chosen by author.

**Reasoning:** The family supplies no trust root and requires the profile to decide one. The exact
external NPP-E profile artifact is the only root; unsupported attestations cannot discharge a claim.

**Decision:** the externally published `NPP-E` artifact at the named family revision is the sole
profile trust root.

**Confidence:** medium.

### D-09 - Evidence retention

**Matter:** how long evidence is retained.

**Source basis:** `3e` §11; `6a` §7; `SU-7`.

**Claim type:** expressly permitted by source; chosen by author.

**Reasoning:** Retention is delegated and must be decided for historical claims. Ten years after
retirement or final-snapshot supersession makes the supported historical claim bounded and evaluable.

**Decision:** retain evidence and canonical history for system lifetime plus ten years.

**Confidence:** medium.

### D-10 - Read openness and attribution

**Matter:** openness of the read surface and whether reads are attributed.

**Source basis:** `5b` §§2.1, 10-11, 14; `6a` §7.

**Claim type:** expressly permitted by source; chosen by author.

**Reasoning:** The one-tenant scope permits an open read policy. Attribution supports evidence and
is observational; it must not become authority or change answers.

**Decision:** every caller may use every declared read operation, subject to per-read determination;
all reads are attributed to the identified caller.

**Confidence:** high.

### D-11 - Read-surface reachability

**Matter:** how inspection is reached when no interaction boundary is selected.

**Source basis:** `5b` §2.1; `5b` §§7, 10, 14; `6a` §7.

**Claim type:** expressly required by source; chosen by author.

**Reasoning:** Selecting no interaction boundary does not remove inspection and requires a declared
means of reach. The profile selects direct in-process access to sealed representation and evidence.

**Decision:** use a declared independent in-process inspection interface, not an interaction or
capability path.

**Confidence:** high.

### D-12 - Interaction-form artifact status

**Matter:** whether an interaction-form element is a governed artifact.

**Source basis:** `5a` §§8, 14; `6a` §7.

**Claim type:** expressly permitted by source; selected as not applicable.

**Reasoning:** NPP-E selects no interaction boundary, so it has no interaction-form element in
scope.

**Decision:** no interaction-form artifact is admitted or claimed.

**Confidence:** high.

### D-13 - External protocol binding artifact status

**Matter:** whether an external protocol binding is a governed artifact.

**Source basis:** `5a` §§10, 14; `6a` §7.

**Claim type:** expressly permitted by source; selected as not applicable.

**Reasoning:** NPP-E selects no external protocol boundary and therefore has no such binding in
scope.

**Decision:** no external protocol binding is admitted or claimed.

**Confidence:** high.

### D-14 - Transformation sufficiency

**Matter:** sufficiency criterion below which realization refuses.

**Source basis:** `4d` §§5-9, 11-15; `4d` §16; `6a` §7.

**Claim type:** expressly required by source, parameterized by author.

**Reasoning:** The family requires sufficiency before realization and leaves the criterion open. A
binary all-required-facts criterion is enforceable and preserves the distinction from quality.

**Decision:** every listed required fact, blocking-question resolution, grounding, bidirectional
preservation, exact realization coverage, dependency order, and amendment condition must hold; any
failure refuses before usable output.

**Confidence:** high.

### D-15 - Genesis discharge fixtures

**Matter:** what discharges a genesis claim.

**Source basis:** `1b` §11; `4d` §12; `7b` §9; `6a` §7.

**Claim type:** expressly required by source, with fixtures chosen by author.

**Reasoning:** Genesis is in scope because the profile constitutes a first snapshot. `7b` assigns
the profile the fixture decision while `7a` and `7b` retain the discharge-class rules.

**Decision:** use the identified genesis proposal, NPP-E profile artifact, independent authorship/
control record, first snapshot, and acceptance evidence as named fixtures.

**Confidence:** medium.

### D-16 - Additional obligations

**Matter:** additional profile obligations.

**Source basis:** `6a` §§3-5; `NP-6`.

**Claim type:** expressly permitted by source; chosen by author.

**Reasoning:** The selected facilities and parameters already narrow the family. Adding a duplicate
obligation would violate the profile's distinction between selection and additional obligation.

**Decision:** add none.

**Confidence:** high.

## Author choices not determined by the family

The exact kind names, outcome names, namespace label, SHA-256, ten-year retention period, open and
attributed read policy, and fixture details are author choices. Their source basis is permission or
delegation, not a family mandate.

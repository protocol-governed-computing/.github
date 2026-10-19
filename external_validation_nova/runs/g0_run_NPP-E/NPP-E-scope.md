# NPP-E Scope Register and Assumptions

Family revision: `14d54013494da27e43362d29ce15059c6fce5f21`

## Commission-fixed scope

These conditions come from `task_author_a_profile.md` §2. They are recorded separately from profile
determinations because they are supplied by the commission, not decided by NPP-E.

| Scope matter | Commission-fixed condition | Source |
| --- | --- | --- |
| System count | one governed system | commission §2 |
| Snapshot and execution | sealed and executed; one snapshot accepted whole and executed against governed state | commission §2 |
| Inspection | required | commission §2 |
| External protocol | none during this profile's scope | commission §2 |
| Attestation | no attestation beyond what the standard requires | commission §2 |
| Tenancy | one tenant | commission §2 |
| Replication | none | commission §2 |
| Profile identity | `NPP-E` | commission §§2, 5 |
| Authorized inputs | only the named commission, 32 `spec` documents, and `REVISION` may be consulted | commission §§3, 4 |

## Working assumptions

These are operational assumptions used to make the profile reviewable. They are not claimed as
requirements of the family.

1. The supplied revision string identifies the frozen family revision for this run.
2. The profile artifact can be obtained by a checking party independently of the system that later
   claims it, satisfying the authorship/externality condition in `6a` §6 and `SN-7`.
3. The phrase "no external protocol boundary" does not remove the possibility of a direct,
   in-process inspection interface; `5b` §2.1 requires the profile to state how inspection is
   reached when interaction is not selected.
4. A profile may choose canonical kind names for an open artifact-kind language and close those
   names for its own system, provided the choice does not claim that the family enumerated them.
5. SHA-256 is treated here as a profile-selected integrity mechanism, not as a semantic term or
   authority supplied by the family.
6. A ten-year post-retirement retention period is treated as a profile parameter, not as a family
   retention rule.

## Matters deliberately not assumed

- No existing implementation, reference realization, prior profile, prior deliverable, session
  transcript, architecture paper, repository layout, or naming taxonomy was consulted.
- No claim is made that the selected five kinds are the only kinds a conforming PGC platform could
  ever use; they are only the closed vocabulary of NPP-E.
- No claim is made that contract conformance proves business correctness.
- No unresolved ontology question in `findings_register.md` is silently answered by this register.

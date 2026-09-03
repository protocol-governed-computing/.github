# NOVA — external validation of the PGC Standard

A programme to test whether the Open PGC Standard is sufficient to build from, by having parties
with no access to the reference realization author a profile against it, build a system claiming
that profile, and evolve that system through its own transformation semantics.

**Nothing here is part of the standard.** These are instruments and evidence about it.

| | |
|---|---|
| `NOVA.md` | the programme: five gates, the finding classes, the firewall, who must be independent of whom |
| `instruments/` | the commissions and protocols each gate is run under |
| `runs/` | what each run produced, and the commissioning side's reading of it |
| `runs/run_conditions.md` | which model performed which role, and what the separation does and does not establish |

## Instruments

Two documents per gate that involves a worker: one the worker receives, one it never sees.

| Gate | Worker receives | Operator only |
|---|---|---|
| **G0** profile authoring | `task_author_a_profile.md` | `task_author_a_profile_operator.md`, `g0_handover.md` |
| **G1** protocol | — | `g1_realization_protocol.md` |
| **G2** realization | `task_build_a_realization.md` | `g2_handover.md` |
| **G4** transformation | `task_transform_a_realization.md` | — no firewall on this gate |

**The split is the point.** A worker handed the classification taxonomy answers the question the
taxonomy exists to measure — which is what happened at G0 and is why the two layers are separate.

## Runs

| | |
|---|---|
| `g0_run_NPP-C`, `NPP-D`, `NPP-E` | three profile-authoring trials, with their evaluations, reclassification and dispositions |
| `g2_run` | the realization claiming `NPP-E`, its registers, evidence, baseline and staging record |
| `g4_run` | the governed transformation adding a lending domain to that baseline |

`NPP-E` is the only uncontaminated authoring run and is the profile G2 built against. `NPP-C` was
handed the taxonomy; `NPP-D` shared a context with `NPP-C` and inherited its vocabulary.

## What it has established

- **Finding A answered** — `6a` supports telling a deliberate silence from an omission; an author
  with no prior context drew the distinction from the text and coined its own name for the
  delegated case.
- **Finding F settled** — three authors closed three different vocabularies from identical text.
  The standard determines no vocabulary, and `2d` §1 says it must not. **Not carried into `2b`.**
- **Seventeen candidate findings across G0, none an undeclared gap.** Every one landed on something
  the family had already marked as delegated or out of scope.
- **No repair to the standard follows from any gate so far.**

## What it has not tested

`3a` execution and `3d` capability have been read and never built against. G2 discharged one of
`NPP-E`'s eight claims; G4 exercised `4d`. **G3 is blocked** — `NPP-E` §12 excludes the reference
realization by construction, and `7a` §10 makes systems under different profiles incomparable.

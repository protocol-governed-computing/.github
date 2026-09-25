# A superseded artifact stays in force

Held in `doc/` because it is a defect in the family's model rather than in any one boundary, and
because nothing in the workspace triggers it today. It cost an afternoon to find and would cost the
same again.

## What is missing

Supersession is declared, checked for referential hygiene, and **not honoured in effect**. A
superseded artifact stays compiled, and anything that reaches it by being present rather than by
being named goes on reaching it.

The standard already requires otherwise:

> **SU-7.** A superseded thing MUST be excluded from **every projection execution consumes**, and
> MUST be retained in the canonical record and reachable by inspection.

Both halves matter and the realization satisfies only the second.

## How the existing mitigation misses it

`assert_superseded_not_referenced_v0` is correct and its docstring states the reasoning plainly:

> without it a superseded artifact **stays compiled, stays dispatchable**, and everything that
> referenced it goes on reaching it — so a change could stand a workflow down, report success, and
> leave the composition executing what it retired.

The authors knew the artifact stays live. Their mitigation was to forbid *references* to it, so that
nothing reaches it.

**That assumes an artifact acquires effect by being referenced. Some acquire it by being present.**
An `INVARIANT` is referenced by nothing: every invariant in the composition derives an assertion and
runs. The hygiene check cannot cover that and was never meant to.

So the population splits, and only one half is protected:

| Reached by | Examples | Covered |
|---|---|---|
| reference — named by another artifact, or by exact identity in code | `WORKFLOW`, `INTENT`, a policy `STRUCTURE` read by FQDN | yes |
| presence — found by scanning for a kind or a prefix | `INVARIANT`, a `STRUCTURE` selected by prefix | **no** |

## Observed, not theorised

Both halves of the gap were seen while making execution placement composable.

A superseded `INVARIANT_EXECUTION_PLACEMENT_DECLARED_V0` went on being enforced, failing the build
with `No active placement contract found` — a message naming neither supersession nor the
predecessor, so the cause was not visible in the symptom.

A superseded placement `STRUCTURE` was offered as a selection candidate beside its successor, and
the two agreed, so a mode named once resolved to two declaring artifacts.

## The exposure today is nil, and that is luck

Five superseded artifacts exist in the workspace:

```
WORKFLOW  × 2    reference-reached
INTENT    × 2    reference-reached
STRUCTURE × 1    read by exact FQDN in merit.py — reference-reached
```

**No superseded invariant exists anywhere.** Every one of the five is reached by name, which is the
half the hygiene check covers. Nothing to repair — but nothing prevents the sixth.

Selection was narrowed while placement was being fixed: `_declared_mode` in the compiler's extract
stage returns nothing for a superseded structure, so the four prefix-selected boundaries no longer
offer one. **Enforcement was not narrowed.** A superseded invariant still derives and runs.

## The undeclared restriction

Stated nowhere, and true now:

> Supersession is only safe for artifacts reached by name. For an artifact reached by presence,
> superseding it leaves both versions in force, and the surface must **delete** it instead.

That is what was done to the V0 placement artifacts, and
`CONSTITUTION_EXECUTION_PLACEMENT_V1` §8 argues it at length rather than asserting it. Deletion was
available only because supersession was never declared — `SU-8` forbids deleting a superseded thing,
and `SU-2` forbids treating deletion as supersession. The two acts are exclusive, and choosing
between them is currently forced by a property of the artifact's kind that nothing documents.

## The strategic fix

One distinction, declared once: **presence is not force.**

A superseded artifact remains **compiled** — present, readable, part of the canonical record, so
`SU-7`'s second half holds and the relation it declares can be read. It is not **in force**: not
enforced, not dispatchable, not a selection candidate.

Three parts, and the third is the one that matters:

1. **One predicate**, `in_force(a) = not a.superseded_by`, declared in the governance surface rather
   than spelled inline. A predicate copied to five call sites is five places to forget it.
2. **Applied wherever presence confers effect.** Enumerating those paths is the deliverable; the
   filters are trivial once the enumeration exists. Two are known — assertion derivation, and
   selection, already closed.
3. **Made checkable.** An invariant failing when a new effect-conferring path does not consult the
   predicate. Without it the next such path reintroduces the gap silently, which is exactly what
   happened here: a correct hygiene check existed and did not cover a path nobody had enumerated.

## What this means for the realization map

`SU-7` is currently mapped **Demonstrated**, on the evidence that superseded artifacts are absent
from the vocabulary projection. That evidence is sound and its scope is narrower than the invariant:
`SU-7` says *every* projection execution consumes, and the assertion path consumes the canonical
projection, where a superseded invariant would still be present and still run.

The entry should be re-read against the clause rather than against one projection. It is a `Partial`
at least, and a `Violated` the moment a superseded invariant exists.

`SU-3` is already a finding — the relation is declared twice, `supersedes` on the successor and
`superseded_by` on the predecessor, where the standard requires once, on the successor. Worth noting
that the fix above keys on `superseded_by`, the predecessor-side declaration the standard does not
ask for. A model that declared the relation only on the successor would have to derive the
predecessor's status by lookup, which is a different implementation and the same rule.

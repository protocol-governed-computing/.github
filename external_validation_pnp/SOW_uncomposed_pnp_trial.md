# Independent realization from the uncomposed platform PNP — input slice

Successor trial to NOVA. NOVA asked whether a *minimal* profile could be authored and realized from
the spec alone. This asks a different question on the same axis: given the platform's own governed
artifacts, can a second party build a PGC implementation that reads them and produces the same
governed behavior?

## 1. The result this is built to produce

One binary outcome, decided before anything is judged by hand:

> Does the worker's implementation, given identical declarative inputs, produce a snapshot whose
> content-derived identity equals the reference snapshot's?

Equal — the spec pins canonical form well enough that two independent implementations converge.
Unequal — the spec underdetermines canonicalization, ordering, or projection, and the divergence
localizes the defect. Either way the trial yields a fact, not an opinion. Everything else in this
document exists to make that comparison legitimate.

## 2. Operator prerequisites (before any handover)

1. **Build the uncomposed PNP.** It does not exist yet. The current working `snapshot/` and
   `pgc_release/snapshot` are both the *composed* 7-domain build (`REFERENCE_PLATFORM_PROFILE_V1`,
   snapshot id `72404ce4…` / release `4a1e8896…`), including the three business domains.
   The trial target is governance + collatz only — `platform`, `workload`, `inspection`,
   `transformation` — with `ai_governance`, `blockchain`, `book_library_mgmt` excluded.
2. **Record its snapshot id and per-domain graph addresses**, sealed and dated, before handover.
   This is the commitment the worker's result is compared against. Do not share it.
3. **Freeze the spec revision** and record the rev, as `g0_handover.md` does for NOVA.
4. **Decide the profile question** (§5 below).
5. **Rule on the transformation self-reference** (§7).

## 3. Package A — what the worker receives

### A1. Standard
- `standards/spec/` at the frozen revision — 33 documents, `0a` through `8a`.
- `REVISION` file naming the rev.

### A2. Profile
- `.github/snapshot_profiles/REFERENCE_PLATFORM_PROFILE_V1.md` (252 lines), amended to the
  uncomposed selection, or the successor profile that supersedes it by declared identity (`4e §2`).

### A3. Governance surface — declarations only
- `software_governance/registry/` — 27 categories, 157 artifacts.
- `software_governance/capability_transforms/registry/`
- `software_governance/capability_side_effects/` (registry side)
- `software_governance/ARCHITECTURE.md`, `README.md`, `VERSION`

### A4. Conformance workload — declarations only
- `conformance_workloads/workloads/collatz/registry/` — 12 artifacts
- `conformance_workloads/workloads/collatz/snapshot/determinations/`
- `conformance_workloads/workloads/collatz/test_payloads/`
- `conformance_workloads/ARCHITECTURE.md`, `README.md`, `VERSION`

### A5. Task instruments
Modelled on `external_validation_nova/instruments/`:
- `task_build_an_implementation.md` — the worker's charter
- `run_conditions.md` — regime in force, tooling, honour-based firewall (per `g0_handover.md` §1)
- the findings taxonomy from §6 below, handed over *before* the run

## 4. Package B — withheld, and why

| Withheld | Why |
|---|---|
| `protocol_compiler/`, `snapshot_assembler/`, `protocol_runtime/`, `snapshot_inspector/` | The toolchain is what the worker must independently produce. |
| `software_governance/capability_transforms/implementation/` | Behavior must be derived from declarations, not copied. |
| `conformance_workloads/workloads/collatz/implementation/` (5 modules) | Same. Collatz is trivially specified; if the declarations do not suffice to reproduce it, that is a finding. |
| `snapshot/`, `pgc_release/snapshot/`, all manifests and hashes | Sharing the target contaminates the only binary test. |
| `.github/process/*.py` closure checks | These encode conformance judgments the spec should already carry. Withholding tests whether it does. |
| `business_domains/`, `protocol_transport/` | Out of profile scope. |
| Papers, NOVA materials, this document | Not spec; would leak intent and prior findings. |

## 5. The profile decision

Two options, materially different in what they buy:

**(a) Hand the worker the platform profile.** Both implementations then claim the *same* profile, so
direct conformance comparison is possible by construction. This closes the limitation the paper
currently records — that comparative conformance did not run because the authored profile excluded
the reference implementation. Recommended.

**(b) Have the worker author their own profile first**, NOVA-style. Tests profile authoring again,
but reintroduces the incomparability that made NOVA's conformance comparison impossible.

(a) tests more of what remains untested. NOVA already exercised (b) across three runs.

## 6. Pre-registration — write before the run, not after

NOVA raised seventeen candidate findings and classified none as an undeclared gap. On a surface this
much wider that classification will be contested unless the rule is fixed in advance. Publish, before
handover, the test that separates:

- **spec defect** — the worker could not proceed, or proceeded differently, because the standard
  does not determine the answer;
- **deliberately open** — the standard names the decision as left to the implementer;
- **worker error** — the standard determines it and the worker read it wrong.

Also pre-register what counts as behavioral equivalence for collatz: identical emitted evidence and
declared outcomes over `test_payloads/`, compared as traces.

## 7. Ruling required before handover

The uncomposed PNP contains `transformation` as a governed domain — the machinery by which the
platform changes itself. A profile governing a platform that includes its own transformation
pipeline sits close to the self-reference bar: a profile may not be authored by the system it
governs. Decide explicitly whether the platform profile is authored outside that surface, and record
the reasoning. This is cheaper to settle now than to defend afterward.

## 8. Worker deliverables

1. A working implementation: compile, assemble, seal, execute, inspect.
2. The snapshot it produces, with its content-derived identity.
3. An evidence document naming each claim it discharges, with demonstrations that fail when the
   behavior is removed.
4. A findings log, each entry classified against the §6 taxonomy.
5. A statement of what it did not claim and why.

## 9. Evaluation

1. **Identity comparison** — worker snapshot id against the sealed commitment. The headline result.
2. **Trace equivalence** — collatz outcomes and evidence over the shared payloads.
3. **Findings adjudication** — against the pre-registered taxonomy, by someone who did not author
   the standard, if that can be arranged.
4. **Mutation check on the worker's own suite** — remove a required guard from *their*
   implementation and see whether *their* demonstrations fail. This is the test that caught two
   non-discriminating suites in the reference implementation; it should be applied symmetrically.

## 10. Known limits of this trial

- Still a single worker. Use a different model than NOVA's, or the single-worker limitation is
  unchanged and no comparison across workers is available.
- Honour-based input firewall for an external party. Record which regime was actually in force.
- No external effect is exercised; the profile selects no interaction boundary.
- A matching snapshot id proves convergence on canonical form. It does not prove the spec is
  sufficient for surfaces this profile excludes.

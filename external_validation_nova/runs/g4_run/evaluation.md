# G4 — evaluation

A governed transformation of the `NPP-E` realization, adding a lending domain to its own baseline.
Performed by the G2 builder, with no firewall — correct for this gate, which asks whether the
**governed state** carries what evolution requires rather than what the standard alone supports.

## Verified independently

15 tests pass under an independent run. The transformation grounds against the pinned baseline
`snapshot:70dd9dea…` at family revision `f476ea5c`, and that identity appears in the code, the
transformation evidence, and — now corrected — the conformance evidence.

**Mutation-tested, as at G2.** The third row is the finding below, and its closure:

| Guard disabled | First delivery | After the finding |
|---|---|---|
| `unknown_check_kind` refusal | fails — demonstrated | fails |
| `copy_already_on_loan` refusal | fails — demonstrated | fails |
| **`baseline_identity_mismatch` refusal** | **passes — undetected** | **fails — demonstrated** |

16 demonstrations now, from 15.

## The finding: grounding is asserted, not demonstrated

`evaluate_design` refuses when the baseline's identity or family revision does not match. The guard
is present and correct. **No demonstration exercises it.** The test asserts that the baseline's id
*equals* the expected constant; it never supplies a wrong baseline and requires a refusal. Disabling
the guard entirely leaves all 15 tests green.

**This is the SHA-256 gap again, in a second place.** Both times a property the profile requires
was implemented, asserted *about*, and never demonstrated by something that could fail. `7b` is
explicit: a fixture set containing only well-formed material cannot exhibit a refusal.

It matters more here than it did there. `NPP-E` §9 requires claims about the existing system to be
**grounded against the named frozen baseline**, and the commission named grounding as the thing that
separates a real transformation from one performed against remembered state. The system does ground
correctly; the evidence does not establish that it must.

**The worker knows how to do this** — two other refusals in the same file have negative
demonstrations that bite. This one was missed, not misunderstood.

**Closed on the first pass after it was named.** A sixteenth demonstration supplies a mismatched
baseline and requires the refusal; disabling the guard now fails it. Verified by re-running the
mutation, not by reading the report. Both times a gap of this shape was named, it was closed
without argument and without the fix being specified.

## The gate's own question came out well

The commission asked the worker to notice every point it reached for something it knew because it
built the system. The transformation:

- **grounds by querying the baseline's read surface** — `inspection.get_artifact`,
  `inspection.enumerate_artifacts` — rather than assuming what the baseline contains;
- **uses only kinds `NPP-E` admits** — `workflow`, `capability-contract`, `read-operation`. No kind
  was invented for the domain;
- **derives every identity through the system's own functions**, supplying none from memory.

Its coupling to `npp_e` is to *mechanism* — `make_artifact`, `build_snapshot`, `Inspection`,
`Refusal` — not to remembered governance content. A transformation runs inside the realization; it
is not a separate program obliged to rediscover it. **That distinction is the one G4 was testing,
and the transformation falls on the right side of it.**

## `unresolved.md`, three gates running

The register again holds scope statements — governance closure, capability conformance, genesis,
retention — rather than matters the author could not resolve. The commission was rewritten before
this gate to say so explicitly, and it was still read the other way.

Three readings across three gates, each by a competent author, is not an author problem. **The word
"unresolved" invites the question "by whom", and no amount of clarifying prose in the commission
overrides what the filename says.** Rename it.

## Disposition

- **The transformation stands.** A lending domain added to a named baseline, with refusals for
  unknown check kinds and duplicate active loans, both demonstrated by tests that fail when the
  guard is removed.
- **One finding against the evidence**, raised and closed: baseline grounding now has a negative
  demonstration that fails when the guard is removed.
- **No repair to `draft-4` follows from G4.**
- **`4d` has now been exercised**, and produced no finding against the standard. Of the three
  documents G2 never reached, execution and capability remain untouched at any depth.

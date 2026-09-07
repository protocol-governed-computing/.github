# G2 — evaluation

An offline realization claiming `NPP-E` at revision `f476ea5c`, built by a worker meeting both
independence boundaries: not the author of `NPP-E`, and with no access to G0's findings.

## Integrity

All 32 spec documents byte-identical to the pinned commit. `staging_manifest.md` restored to its
handed-back form after the role-inversion episode. No prohibited input recorded, and the worker
volunteered that `8a` §2 discloses a reference realization exists and that it consulted nothing
from it.

## The demonstrations were run by a party that did not build the system

Six tests, all passing under an independent `python3 -m unittest`. That satisfies `7b` §6's
obtainability rule directly rather than by assertion.

**They were then mutation-tested**, because `7b` requires a demonstration capable of failing if the
system were non-conforming, and a passing suite is not evidence of that on its own:

| Mutation | Result |
|---|---|
| disable one kind-closure guard | **passes** — a second guard covers it |
| disable both kind-closure guards | **fails** — closure is genuinely demonstrated |
| `sorted(` → `list(`, breaking canonicalization | **fails** |
| `!=` → `==` in a verification path | **fails** |
| **`sha256` → `md5`** | **passes — nothing detects it** |

**The last one is a real gap in the evidence.** `NPP-E` states: *"For this profile, the integrity
value over canonical semantic content is a SHA-256 digest."* A system substituting MD5 would not
conform to the profile, and **every one of the six demonstrations still passes.** The suite
demonstrates the *property* — content-derived, verifiable, re-derivable — and never binds the
algorithm the profile selects.

This is a finding against the realization's evidence, not against the standard. It does not
invalidate the discharged claim, and it is exactly what a demonstration-based conformance regime is
supposed to surface when someone checks rather than reads.

## No findings against the standard

**Nine determinations**: seven *chosen by author*, two *inferred from source*. **Zero carry source
basis `none`** — every free choice cites text that permits it. By `g1_realization_protocol.md` §7
that is class 1, realization freedom, throughout.

**Five unresolved matters**, and none is a class 3–6 finding. Each records something the narrow
slice does not implement — governance closure, capability effect paths, transformation, genesis,
ten-year retention — and states that no claim is made for it. That is the discipline the commission
asks for. It is not a defect in the family.

**Class 6: none.** Nothing shows the worker unable to proceed without reconstructing a convention
knowable only from an existing realization.

**Across G0 and G2 the count is now seventeen candidates and one build, with no undeclared gap.**
The standard held under building as it held under reading.

## What G2 did not test, which bounds that result

The realization discharges **one of `NPP-E`'s eight claims** — vocabulary and declaration surface,
with the sealed snapshot and in-process read surface. It implements **no execution, no capability
effect path, and no transformation.**

So the parts of the family most likely to carry gaps — `3a` execution, `3d` capability, `4d`
transformation — **were never exercised.** G2 tested construction, identity, canonicalization,
refusal, inspection and evidence, and found the standard sufficient there.

**That is a narrower result than "the standard supports building a conforming system."** It is
"the standard supports building the construction-and-inspection surface of one, and the builder
declined to claim the rest rather than assert it." The second half is worth as much as the first.

## The register naming is still ambiguous, in a third way

`unresolved.md` was to hold *matters the worker could not resolve*. G0's `NPP-E` author read it as
*matters the family declined to determine*. This builder read it as *matters this slice does not
cover*. Neither is what it asks for, and the repair made after G0 did not prevent the second
misreading.

Three readings of one register name across two gates is the instrument's problem, not the workers'.
**A register should be named for what goes in it, not for the state of the question** — *"what I
could not decide"* rather than *"unresolved"*.

## Disposition

- **The claim stands.** One claim of eight, discharged with demonstrations that run independently
  and, with one exception, fail when the system is broken.
- **The SHA-256 gap is recorded against the realization**, not the standard. It would need closing
  before this claim is compared at G3.
- **No repair to `draft-4` follows from G2.**
- **One instrument repair**, for any later gate: rename the third register.

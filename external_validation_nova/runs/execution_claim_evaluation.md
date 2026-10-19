# Runtime and execution claim — evaluation

A second claim of `NPP-E`'s eight, discharged after the observation that the transformation declared
a workflow whose outcome vocabulary nothing read.

## What was wrong before

The workflow artifact carried `"outcomes": ["completed", "failed"]` and the lending rule lived in
the
body of `lend()`, which raised a refusal directly. **Deleting the workflow artifact left behaviour
unchanged.** `3a` §3.2 is the rule that forbids it: *"Execution performs no routing logic of its
own.
It does not decide where to go; it reads where to go."*

## Verified independently

22 tests pass. **Mutation-tested, including the one named in the commission before the work began:**

| Mutation | Result |
|---|---|
| **hard-code the routing the declaration supplies** | **fails** |
| empty the declared `routes` map | **fails** (4 errors) |
| remove the `unrouted_outcome` refusal | **fails** |
| remove the `unresolved_route_target` refusal | **fails** |

**The first row is the whole claim.** A traversal that reads declared routing and one that ignores
it
produce identical results on well-formed input; only a demonstration built to separate them can
tell.
`current = step["routes"][outcome]` replaced with the equivalent hard-coded branch now fails a test,
so the routing is demonstrably read rather than assumed.

## The pattern that had held twice did not hold a third time

SHA-256 at G2 and baseline grounding at G4 were both properties implemented correctly, asserted
*about*, and demonstrated by nothing that could fail — found only by mutation after delivery.

**Here the commission named the risk in advance** — *"if routing were hard-coded rather than read,
would anything fail?"* — and the demonstration set closed it before evaluation.

That is worth recording precisely, because it narrows what the earlier gaps were. They were not
carelessness and not a capability gap: **the author demonstrates what it is asked to think about
demonstrating.** Told that a passing suite is not evidence a demonstration could fail, and given the
specific question, it built the discriminating fixture first time. Left to infer it from `7b`, it
did not — twice.

## Disposition

- **The claim stands.** `3a`'s central rule is now demonstrated, not asserted: behaviour is carried
  by the sealed representation, and removing the workflow artifact refuses execution.
- **`3a` has been built against**, and produced no finding against the standard.
- **`3d` is reached but shallow.** A capability contract exists, declares an outcome vocabulary, and
  its outcomes are routed on. What is not exercised is a capability with an external effect —
  `3d`'s effecting path — and `NPP-E` §2 selects no interaction boundary, so it may not be reachable
  under this profile at all.
- **No repair to `draft-4` follows.**

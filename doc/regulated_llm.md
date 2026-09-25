# rLLM — a regulated language model as a governed domain

Nothing here is decided, and no work on the platform should be sequenced around it. Held in `doc/`
because the idea outlives the session that had it, not because it is scheduled.

---

## The idea

A domain, `regulated_llm`, in which a language model is a declared capability behind a governed
contract: its configuration declared as artifacts, its invocation admitted or refused at a governed
boundary, and every determination about it evidenced.

Two phases were proposed. Phase 1 declares a transformer's configuration — the parameters of Vaswani
et al. (2017) — as artifacts and inspects the result without running anything, to find out whether
the declaration vocabulary can express a model at all. Phase 2 adds governance to the model's
behavior.

## What the first phase would actually test

Whether a model's *configuration* is expressible as governed artifacts, and whether a model's
identity can therefore be content-derived and sealed rather than being a filename and a version
string. That is worth knowing and cheap to find out.

Expect it to reach a limit. `behavior_logic` here means declared steps, declared outcomes, and the
routing between them. A forward pass has none of those: it reports no outcome and nothing routes on
one. The vocabulary may reach a model's configuration and its invocation and stop there, which is a
finding rather than a failure.

## Why the second phase, as proposed, does not hold

The stated goal was to prevent jailbreaking and to prevent a model learning rogue behavior. This
architecture governs declarations and determinations. A model's behavior is determined by weights
and by sampling, and neither is a declaration.

- Jailbreaking attacks the model's own behavior, inside the weights. A boundary contract can refuse a
  request matching a declared condition and refuse a response matching one. That is a guardrail, it
  is well understood, and it needs none of this architecture.
- Learning cannot be governed here at all. It happens in training, and training is not a governed
  transition in this lifecycle.

Claiming otherwise would be the error this project names as its central discipline: letting the
presence of a governance mechanism stand in for evidence that the mechanism secures the property it
was built for.

## What would hold

Not governed behavior. Governed authority, and a record.

- nothing reaches the model except through declared ingress;
- every invocation is evidenced — which snapshot, which contract, which actor, what was admitted,
  what was refused;
- refusal is a governed determination carrying evidence, not a filtered string;
- the model's configuration and identity are sealed and content-derived.

This is the narrower claim and also the one regulation asks for. A regulator cannot verify a model's
internals either, which is why the obligations written around these systems are about traceability
and record-keeping rather than about behavior. *Here is a checkable record of what was authorized,
what ran, and what was refused* is answerable. *This model is safe* is not answerable by any
architecture.

## The result worth having

This platform's execution is deterministic: the same state, proposal and closure yield the same
determination. A language model is not deterministic, by construction.

Admitting one therefore places it outside that claim, and **declaring where the determinism ends is
the interesting part** — a capability whose non-determinism is a declared property of a declared
surface, rather than a property discovered later by whoever depended on it. Few systems carrying a
model can say precisely where their determinism stops.

## Sequencing

After the platform, not alongside it. What would make this domain worth a regulator's attention is
the signed, evidenced, verifiable part, and that part is unfinished: signing is a stub, no node
dispatches to another, and nothing has been read back against the profile by hand.

The domain does not add platform requirements. It raises what is already owed.

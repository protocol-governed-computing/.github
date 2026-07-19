# Protocol-Governed Computing (PGC)

> 🚧 **Under construction.** PGC is in early bootstrapping. The working
> repositories are private while the founding documents settle. This page will
> grow as the standard takes shape.

**Protocol-Governed Computing is a standard, not a program.** It defines a model of
computation in which *all behavior originates from a compiled, governed protocol
snapshot*, and a generic runtime executes that snapshot with zero domain knowledge.
Behavior is determined and validated at compile time; execution is a deterministic
traversal that produces an observable trace.

PGC exists to **preserve human authority over business behavior while allowing
implementation technologies to evolve independently** — the governed protocol, not
any compiler or runtime, is the seat of authority. PGC is deliberately independent
of any one compiler, runtime, or language, in the same way SQL is independent of
any one database and JVM bytecode is independent of any one JVM.

## Five authorities

PGC separates five things that are usually blended. Authority flows **downward**;
each authority is bound by the ones above it.

| Authority | Responsibility |
|-----------|----------------|
| Architecture | *explains* |
| Standard | *specifies* |
| Conformance | *verifies* |
| Reference Implementation | *demonstrates* |
| Independent Implementations | *validate* |

The center of gravity is not prose: **the Genesis Snapshot plus the conformance
definition *is* the standard.** The prose RFCs explain it; they are not its ground
truth.

## PGC and PGS

- **PGC** — this ecosystem: the architecture papers, the standards, the conformance
  suite, and the governance process.
- **PGS** (Protocol-Governed Systems) — **Reference Implementation 0**, the
  implementation in which the architecture was developed and validated. It
  demonstrates *one conforming realization* of the standard; it does not define it.

## Status

Bootstrapping. Founding documents (the charter and organization topology) are being
finalized in `pgc-charter`. Public participation details will follow once the
first RFCs open.

---

*Nothing here is final until it is ratified through the standard's own amendment
process.*

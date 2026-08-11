# Protocol-Governed Computing (PGC)

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

## The model, in three functions

A governed system's life is three governed compilations over one architecture:

```
   (Bₙ, P) ──𝒯──▶ Bₙ₊₁ ──𝒞──▶ Sₙ₊₁ ──Φ──▶ (R, T)

   𝒯  transformation   changes the system      a baseline becomes its successor
   𝒞  compilation      seals it                the successor becomes a snapshot
   Φ  execution        realizes it             the snapshot produces result + evidence
```

Transformation is **partial** — not every problem yields a next baseline — while the
transformation *process* is **total**: every failure is reported at a named stage rather
than left undefined. That is what makes governed evolution auditable rather than merely
careful.

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
definition *is* the standard.** The prose papers explain it; they are not its ground
truth.

---

# Documentation

*Papers predating the PGC name describe the same substrate as **Protocol-Governed
Systems (PGS)**. The name changed; the architecture did not.*

## Current — Protocol-Governed Computing

The three papers that state the architecture and its realization. Read in any order;
each stands alone.

| | paper | what it answers |
|---|---|---|
| **1** | [An Architecture for Deterministic Declarative Execution](https://omnibachi.org/papers/architecture-deterministic-declarative-execution/) | **What execution must be.** Execution as traversal of a compiled protocol by an interpreter that decides nothing. [DOI](https://doi.org/10.5281/zenodo.21879516) |
| **2** | [An Architecture for Closed-Loop Governed Transformation](https://omnibachi.org/papers/architecture-closed-loop-governed-transformation/) | **What evolution must be.** Software evolution as the governed transformation of an executable baseline into the next, rather than as specification authoring. [DOI](https://doi.org/10.5281/zenodo.21879948) |
| **3** | [Realizing the Normative Platform and Its Governed Transformation](https://omnibachi.org/papers/realizing-the-normative-platform/) | **What it takes to make both real.** The Profiled Normative Platform, the formal treatment of transformation, and what realization surfaces that architecture cannot. |
| **·** | [Field Manual](https://omnibachi.org/papers/field-manual/) | **How the reference implementation is operated.** Doctrine, the artifact ontology, the build lifecycle, and the invariants — the working companion to the three papers above. |

## Foundations — published, still current

Earlier work under the PGS name that the papers above assume rather than restate.
Listed in reading order.

| paper | what it covers |
|---|---|
| [Architecture Inversion Concepts](https://omnibachi.org/papers/architecture-inversion-concepts-v1/) | **Start here if you are new.** Fifteen inversions in four propagating groups — governance, orchestration, engineering, scale — and why each follows from the one above it. The shortest route to why this differs from what you already know. |
| [A Conceptual Model](https://omnibachi.org/papers/conceptual-model/) | The protocol snapshot, the unit of admissibility, the constitutional invariants, the implementation boundary, and the evidence model. The foundation the later papers cite. |
| [A Constitutionally Constrained Architecture](https://omnibachi.org/papers/pgs-constitutionally-constrained-architecture/) | The formal treatment: the dual-space model, the protocol-governed abstract machine, the threat model and the classes of vulnerability it makes unrepresentable, and the derivation of O(N + M) governance complexity. The only place the Governance Dividend is derived rather than asserted. |
| [Compiler Conceptual Model](https://omnibachi.org/papers/compiler-conceptual-model/) | What the compiler produces, why the runtime is simple, the admissibility boundary contract, and protocol inspection. The dedicated treatment of 𝒞. |
| [Runtime Conceptual Model](https://omnibachi.org/papers/runtime-conceptual-model/) | What the runtime does with a sealed snapshot, and the multi-runtime certification method Paper 1 cites as the route to demonstrated runtime independence. The dedicated treatment of Φ. |

## Historic

Every paper a later paper has replaced. DOI-published and permanently citable, kept for
lineage rather than for reference: <https://omnibachi.org/papers/working_papers/>.

- **Closed-Loop Governed Evolution** — superseded by Paper 2. Note that it describes the
  transformation pipeline in *stage* vocabulary, which the implementation has since
  renamed to *phases* (P0–P8) to avoid collision with the compiler's own stages.
- **Architecture Inversion Concepts v0** — superseded by the v1 listed above.
- The earlier **PGS working paper series** — governance and authoring, protocol as law,
  deterministic enforcement, pure computation and governed mutation, the inversion of
  trust, and the three dividends.

---

# Repositories

The composition is built from repositories that each own one concern. **A platform is a
composition under a conformance profile, never a repository** — the repository boundary
and the platform boundary are orthogonal, and conflating them is a category error the
architecture is explicit about.

| repository | role |
|---|---|
| `software_governance` | The governance surface: capability transforms and side effects |
| `conformance_workloads` | Workloads that prove conformance |
| `business_domains` | Business domains built on the platform |
| `protocol_compiler` | Compiles and validates protocol source into domain projections |
| `snapshot_assembler` | Assembles validated projections into an immutable snapshot |
| `protocol_runtime` | Reads the sealed snapshot and executes workflows |
| `protocol_transport` | The transport boundary — protocol-neutral ingress and egress |
| `snapshot_inspector` | Read-only snapshot inspection |
| `transformation` | The transformation lifecycle: design compiler and construction compiler |

```
   protocol artifacts ──▶ protocol_compiler ──▶ domain projections
        ──▶ snapshot_assembler ──▶ immutable snapshot
        ──▶ protocol_runtime ──▶ execution ──▶ trace / evidence
```

The snapshot is sealed at build time and the runtime consumes it unchanged. **No behavior
enters at execution time that was not present in the snapshot.**

## PGC and PGS

- **PGC** — this ecosystem: the architecture papers, the standards, the conformance
  suite, and the governance process.
- **PGS** (Protocol-Governed Systems) — the implementation in which the architecture was
  first developed and validated, now **frozen**. It is retained for lineage and is not
  where work continues.

The repositories in this organization are **the reference implementation of PGC**. They
demonstrate one conforming realization; they do not define the standard — that distinction
is the whole point of the table above, and it is why the implementation is a role rather
than a name.

---

*Nothing here is final until it is ratified through the standard's own amendment
process.*

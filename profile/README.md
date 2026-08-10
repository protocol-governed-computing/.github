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
| **1** | [An Architecture for Closed-Loop Governed Transformation](../doc/pgc_architecture_closed-loop_governed_transformation_v0.md) | **What evolution must be.** Software evolution as the governed transformation of an executable baseline into the next, rather than as specification authoring. |
| **2** | [An Architecture for Deterministic Declarative Execution](../doc/pgc_architecture_deterministic_declarative_execution_v0.md) | **What execution must be.** Execution as traversal of a compiled protocol by an interpreter that decides nothing. |
| **3** | [Realizing the Normative Platform and Its Governed Transformation](../doc/pgc_realizing_the_normative_platform_and_its_governed_transformation_v0.md) | **What it takes to make both real.** The Profiled Normative Platform, the formal treatment of transformation, and what realization surfaces that architecture cannot. |

## Foundations — published, still current

Earlier work under the PGS name that the three papers above assume rather than restate.

| paper | what it covers |
|---|---|
| [Architecture Inversion Concepts](../doc/pgs_architecture_inversion_concepts_v1.md) | **Start here if you are new.** Fifteen inversions in four propagating groups — governance, orchestration, engineering, scale — and why each follows from the one above it. The shortest route to why this differs from what you already know. |
| [A Conceptual Model](../doc/pgs_conceptual_model_v0.md) | The protocol snapshot, the unit of admissibility, the constitutional invariants, the implementation boundary, and the evidence model. The foundation the later papers cite. |
| [Compiler Conceptual Model](../doc/pgs_compiler_conceptual_model_v1.md) | What the compiler produces, why the runtime is simple, the admissibility boundary contract, and protocol inspection. The dedicated treatment of 𝒞. |

## Historic

Superseded work, retained for lineage rather than for reference. Kept in
[`bachipeachy/pgs_workspace`](https://github.com/bachipeachy/pgs_workspace/tree/main/doc).

- **Closed-Loop Governed Evolution** — superseded by Paper 1. Note that it describes the
  transformation pipeline in *stage* vocabulary, which the implementation has since
  renamed to *phases* (P0–P8) to avoid collision with the compiler's own stages.
- **Protocol-Governed Systems technical paper**, v1 and v2 — a correct account of
  construction and execution, frozen. Nothing in the current papers retracts it; a
  realization layer now sits above the model it formalizes.
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
| `standards` | Standards documents, specification fragments, the governance charter |
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

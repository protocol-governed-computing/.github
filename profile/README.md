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

**If you read no further:**

1. **Behaviour is declared and governed before it runs.** A change is admitted or refused as a
   governed act; nothing reaches execution by being written.
2. **The implementation realizes that behaviour; it does not define its authority.** The standard
   specifies, a realization demonstrates, and where they disagree the standard governs.
3. **One governance model spans the whole life of a system** — construction, execution, and
   evolution into the next version — rather than stopping at deployment.

What that buys, in practice, is a lifecycle a machine can carry end to end: **a stated business
problem becomes analysis, design, constructed artifacts, a sealed snapshot and a running system
without a human writing the intervening code** — while scope, the governing profile and promotion
stay outside the automated span. [From a stated problem to running
software](#from-a-stated-problem-to-running-software) sets out how, and what is deliberately left
out.

## The standard

The normative specification lives in **[`standards`](https://github.com/protocol-governed-computing/standards)** — thirty-two documents in seven parts, at revision `draft-3`, frozen. It states what a
governed system must mean and do, independently of anything built here.

**It is seeking critical review, not adoption.** What is claimed, what would falsify it, and what has
not yet been established are stated in the
[call for review](https://github.com/protocol-governed-computing/standards/blob/main/doc/call_for_review.md).
[`0d`](https://github.com/protocol-governed-computing/standards/blob/v0/spec/0d_visual_representation_of_the_standard.md)
draws the model in seven figures and is the shortest way in.

**The specification governs; the realization demonstrates.** Where a document of the family and any
implementation disagree, the document governs — including every implementation in this organization.

## The model, in three functions

A governed system's life is three governed compilations over one architecture. In plain terms: a
proposed change becomes a new baseline, the baseline is sealed into a snapshot, and the snapshot is
executed.

```
   (Bₙ, P) ──𝒯──▶ Bₙ₊₁ ──𝒞──▶ Sₙ₊₁ ──Φ──▶ (R, T)

   𝒯  transformation   changes the system      a baseline becomes its successor
   𝒞  compilation      seals it                the successor becomes a snapshot
   Φ  execution        realizes it             the snapshot produces result + evidence
```

Not every proposed change has a legitimate successor. When one doesn't, the pipeline stops
and says which phase refused it and under which rule — it does not produce a weaker baseline
instead. A refusal is an artifact of the process, not an absence of one, and because a
baseline only becomes a snapshot at 𝒞, a change that is refused never reaches the running
system. That is what makes governed evolution auditable rather than merely careful.

## From a stated problem to running software

The three functions above begin at `(Bₙ, P)` — a baseline and a proposal. The proposal does not
arrive from nowhere. `𝒯` is itself a governed lifecycle of nine declared phases, and it starts at a
business problem stated in plain language.

```
   P0  Change Seed              the stated problem, as given
   P1  Change Request           what is being asked of the system
   P2  Domain Model Verification   beliefs confronted with what the baseline actually contains
   P3  Analysis Loop            what the change touches, and on what evidence
   P4  Business Model           what exists, modelled
        │
   P5  Business Intent          what the business seeks          ─┐
   P6  Governance Intent        what is permitted                 │  each cites P0 directly,
   P7  Design Intent            how permitted behaviour is built  │  not the analysis
   P8  Authoring Mandate        what may be constructed, in order ─┘
        │
        ▼  construction → admission → sealing → a runtime that traverses the result
```

A phase that cannot be satisfied refuses rather than producing a weaker artifact. The intent phases
cite the original seed rather than the analysis performed on it, so what the business asked for
cannot be quietly redefined by the work of finding out what exists.

**Every step in that span is machine-performable** — problem statement through construction, sealing,
and then transformation of that sealed state into its successor rather than a rebuild from nothing.
This is not a design notation that stops at the diagram, nor a policy engine that starts at the
deployment boundary: it is one toolchain across the whole lifecycle, and the reference implementation
carries a governed change through it end to end.

**Three things are deliberately outside that span**, and they are the reason the automation is worth
having rather than worth fearing:

| outside the span | why |
|---|---|
| **Scope** | what is governed is decided before the lifecycle opens |
| **The normative profile** | a system may not author the rules it is then judged against |
| **Promotion** | producing a candidate is not the same act as authorizing it to become the next baseline |

An agent can perform the engineering work of the entire lifecycle without acquiring authority over
what the resulting software is permitted to do, because that authority never sat in any of the steps
it performed. **Autonomy over the work; no authority over the software.** That separation is the
claim the architecture exists to make good on, and it is what the conformance suite and the external
validation runs are for.

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

The center of gravity is the normative family, not the papers and not any artifact a build
produces: **the standard is the specification, and a realization demonstrates that it is
satisfiable rather than defining what conformance requires.** The prose papers argue for it; they
are not its ground truth, and neither is anything in this organization's code.

---

## Documentation

*Papers predating the PGC name describe the same substrate as **Protocol-Governed
Systems (PGS)**. The name changed; the architecture did not.*

### Current — Protocol-Governed Computing

The three papers that state the architecture and its realization. Read in any order;
each stands alone.

| | paper | what it answers |
|---|---|---|
| **1** | [An Architecture for Deterministic Declarative Execution](https://omnibachi.org/papers/architecture-deterministic-declarative-execution/) | **What execution must be.** Execution as traversal of a compiled protocol by an interpreter that decides nothing. [DOI](https://doi.org/10.5281/zenodo.21879516) |
| **2** | [An Architecture for Closed-Loop Governed Transformation](https://omnibachi.org/papers/architecture-closed-loop-governed-transformation/) | **What evolution must be.** Software evolution as the governed transformation of an executable baseline into the next, rather than as specification authoring. [DOI](https://doi.org/10.5281/zenodo.21879948) |
| **3** | [Realizing the Normative Platform and Its Governed Transformation](https://omnibachi.org/papers/realizing-the-normative-platform/) | **What it takes to make both real.** The Profiled Normative Platform, the formal treatment of transformation, and what realization surfaces that architecture cannot. |
| **·** | [Field Manual](https://omnibachi.org/papers/field-manual/) | **How the reference implementation is operated.** Doctrine, the artifact ontology, the build lifecycle, and the invariants — the working companion to the three papers above. |

### Foundations — published, still current

Earlier work under the PGS name that the papers above assume rather than restate.

**[Architecture Inversion Concepts](https://omnibachi.org/papers/architecture-inversion-concepts-v1/)
— start here if you are new.** Fifteen inversions in four propagating groups, and why each follows
from the one above it. The shortest route to why this differs from what you already know.

| paper | what it covers |
|---|---|
| [A Conceptual Model](https://omnibachi.org/papers/conceptual-model/) | The protocol snapshot, the unit of admissibility, the constitutional invariants, the implementation boundary, and the evidence model |
| [A Constitutionally Constrained Architecture](https://omnibachi.org/papers/pgs-constitutionally-constrained-architecture/) | The formal treatment: the dual-space model, the abstract machine, the threat model, and the derivation of O(N + M) governance complexity — the only place the Governance Dividend is derived rather than asserted |
| [Compiler Conceptual Model](https://omnibachi.org/papers/compiler-conceptual-model/) | What the compiler produces and why the runtime is simple. The dedicated treatment of 𝒞 |
| [Runtime Conceptual Model](https://omnibachi.org/papers/runtime-conceptual-model/) | What the runtime does with a sealed snapshot, and the multi-runtime certification method. The dedicated treatment of Φ |

### Historic

Every paper a later paper has replaced, DOI-published and permanently citable, kept for lineage
rather than for reference: <https://omnibachi.org/papers/working_papers/>. One naming note if you
read them: the transformation pipeline appears there in *stage* vocabulary, which the implementation
has since renamed to *phases* (P0–P8) to avoid collision with the compiler's own stages.

---

## Repositories

**These are the reference implementation.** The standard itself is not among them — it is
[`standards`](https://github.com/protocol-governed-computing/standards), and it is authored against
no implementation. The composition below is built from repositories that each own one concern. **A PGC platform is
assembled from these components under a conformance profile; no single repository is the platform.**

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
   transformation ──▶ protocol artifacts ──▶ protocol_compiler ──▶ domain projections
        ──▶ snapshot_assembler ──▶ immutable snapshot
        ──▶ protocol_runtime ──▶ execution ──▶ trace / evidence
```

Two repositories deliberately sit off this line. `protocol_transport` is the boundary at
either end of execution — governed ingress and egress contracts, protocol-neutral and not
stages in the lifecycle. `snapshot_inspector` reads the sealed snapshot and takes no part in
producing it.

The snapshot is sealed at build time and the runtime consumes it unchanged. **No behavior
enters at execution time that was not present in the snapshot.**

### PGC and PGS

- **PGC** — this ecosystem: the architecture papers, the standards, the conformance
  suite, and the governance process.
- **PGS** (Protocol-Governed Systems) — the implementation in which the architecture was
  first developed and validated, now **frozen**. It is retained for lineage and is not
  where work continues.

These repositories are **one reference realization of PGC**. The standards define PGC; the
implementation demonstrates it.

---

*A revision of the standard is **declared, not inferred** — proposed against a named predecessor,
stating what it changes and what that invalidates. Every declared change is recorded in
[`doc/revisions.md`](https://github.com/protocol-governed-computing/standards/blob/main/doc/revisions.md),
including the findings considered and declined.*

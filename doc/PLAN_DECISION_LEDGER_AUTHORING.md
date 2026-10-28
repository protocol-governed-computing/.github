# Plan — Authoring Behavior as a Decision Ledger

## Question

Can a person specify a PGC domain by answering decisions, without writing PGC artifacts, and still
get the same sealed snapshot?

Today a human author works in PGC's own vocabulary. `book_library_mgmt` is a small catalog domain.
Its P7 design intent runs to 4,595 lines of registers, artifact families and codes (`AC_`, `CC_`,
`RB_`). The governance does not create that load. The authoring surface does.

## Hypothesis

Most P7 content is a mechanical consequence of a small number of human decisions. If so, a person
can author the decisions, and a front end can derive the rest of P7. The kernel stays unchanged.

- **Ledger entry.** A question, its answer, and the authority who answered it.
- **Case.** A concrete input with its expected outcome and a reason. Cases are both specification
  and conformance tests.
- **Open question.** A ledger entry with no answer. Any behavior that depends on it is refused at
  admission.

The front end never fills a gap with a default. When it cannot derive a P7 cell, it emits an open
question.

## Scope

In scope:

- One domain: `book_library_mgmt`, baseline.
- A ledger format, the smallest that works.
- A deterministic front end that turns the ledger into a P7 design intent.
- The existing pipeline, unchanged, from P7 through Design Compiler, Construction Compiler,
  protocol compiler, snapshot assembler and runtime.

Out of scope:

- The fact-based data model and just-in-time federation. Test them only if this plan succeeds.
- LLM generalization from cases to rules. The prototype derives deterministically. An LLM can
  propose ledger entries later, but it never answers them.
- Any change to the kernel, the compiler or the assembler.

The prototype lives outside `release.sh` until it passes.

## Steps

### 1. Census the baseline

Classify every cell in the `book_library_mgmt` P7 registers into one of four classes:

| Class | Meaning |
|---|---|
| Decision | Encodes a choice only a human can make (a refusal, an authority, an identity rule) |
| Case | Encodes an expected outcome for a concrete input (`test_cases`, `test_case_values`) |
| Mechanical | Follows from decisions and cases plus PGC doctrine (codes, bindings, topology) |
| Unaccounted | Fits none of the above |

The census is the go/no-go gate. It costs the least and decides whether the rest is worth doing.

- **Go:** the decisions and cases come to a small fraction of all cells. "Small" means the ledger
  fits on a few pages.
- **No-go:** most cells are decisions. Then P7 is already close to minimal, and the load is
  inherent.

### 2. Define the ledger format

- One file per domain. Plain YAML with three entry kinds: decision, case, open question.
- No PGC vocabulary. An entry never names a family, a code or a register.
- Each decision names its authority, for example `librarian` or `catalog owner`.

### 3. Author the ledger without reading P7

The author works only from the domain's plain-language purpose. Ideally the author is someone
outside the project. The census in step 1 is the answer key. The author does not see it.

### 4. Build the front end

- Input: the ledger. Output: a P7 design intent that validates against
  `REGISTER_SCHEMA_P7_V0`.
- Every emitted cell carries the ledger entry it derives from, or the doctrine rule that makes it
  mechanical.
- A cell the front end cannot derive becomes an open question. It never becomes a default.

### 5. Run the pipeline and compare

Run the generated P7 through the unchanged pipeline. Compare the resulting snapshot with the
current sealed `book_library_mgmt` snapshot.

- Every difference must trace to a ledger entry or an open question.
- A difference with no trace is a hidden assumption, and the prototype fails.

### 6. Test refusal

- Delete one decision. Admission must refuse the dependent behavior.
- Plant an implementation that violates one case. Construction must refuse it.
- Answer an open question two different ways. The two snapshots must differ only in the behavior
  that depends on that question.

### 7. Test a change as a delta

Author one change request in two ways: as a conventional change dossier, and as a ledger delta
against the baseline ("like the baseline, except…"). Compare effort and the resulting snapshots.

## Measures

| Measure | Target |
|---|---|
| Human entries (decisions + cases) vs P7 lines | At least an order of magnitude fewer |
| Unaccounted cells after the census | Zero, or each explained |
| Snapshot differences with no trace | Zero |
| Rules introduced with no authorizing decision | Zero |
| Refusal tests passed (step 6) | All |
| Delta size vs dossier size for one change | Delta clearly smaller |
| PGC terms the author needed to know | Zero |

## Kill criteria

Stop and record the finding if any of these holds:

- The census shows that most P7 cells are decisions.
- The front end needs PGC vocabulary in the ledger to derive P7.
- Snapshot differences cannot be traced to ledger entries.

A stop still yields a result. It states which part of P7 no human decision accounts for, and
that informs the decision accounting design.

## Next if it succeeds

- Run the same ledger on a second domain with real side effects (`ai_governance`).
- Then test the fact-based data model. A new concept enters as a new fact type, and its promotion
  is a sealed mapping that a ledger entry decides.

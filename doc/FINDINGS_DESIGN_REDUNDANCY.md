# Findings — how much of a design restates other facts

## Question

Can construction derive a large share of what a design states, so a human writes about half as
much? The idea came from a proposal to put a smaller human vocabulary over the ten artifact kinds.

## Answer

No. Measured in P7 register cells, the cells a person actually writes, the redundancy is 13–20%. It
is not half. Most of it sits where a domain contract meets a platform capability, and removing it
would change construction's architecture.

## Two measurements, and why they differ

**Rendered artifact facts.** Candidate rules were applied to the leaves of each rendered Machine
block (`construction check` counts these). The rules derived 35–40% of the facts, and the result
held on held-out domains.

**P7 register cells.** The renderer already derives many artifact facts from a single register cell
or from row order. That is one fact stated once and rendered into several leaves. So counting
artifact leaves overstates what a human writes. These facts are already derived, with no register cell:

- WF node `code` (stated only when it differs, as `runs`)
- `start_node` (from row order)
- WF `structure`
- IN `workflow` and the ACK/NACK text
- CC `allowed`, `on_input_failure` and step `result_surface`
- EV timestamp and description
- `subdomain`
- TEST_DATA `target`

| Domain | Register cells | Removable by the rules | Plus redundancy inside the registers |
|---|---:|---:|---:|
| collatz | 543 | 16.9% | 20.3% |
| book_library_mgmt | 4042 | 13.9% | 20.1% |
| ai_governance | 2711 | 11.5% | 15.5% |
| blockchain | 2420 | 13.3% | 18.7% |
| causal_language_model | 7786 | 10.0% | 13.3% |

## Where the redundancy is, and what removing it costs

| Source | Share of cells | Cost |
|---|---:|---|
| CC interface rows that restate the field of the capability they bind | 6–10% | 70–100% of these bind platform transforms and side effects, whose specs are not in P7. Deriving them means construction reads the sealed composition while rendering. Today it renders from P7/P8 alone. |
| CC step routing, node types, CT implementation fields, EV `required`, STRUCTURE constants, test `expected_outcome` | 3–6% | Declared defaults in eight constitutions. |
| Identity `interface` maps in `cc_composition` | 2–4% | `STEP_BINDINGS_MATCH_INTERFACE` and `STEP_INTERFACE_CONFORMS` must read an absent map as identity. Today they skip it. |
| `semantic_status` / `interpreted_by` written as `—` | 1–2% | Reverses the P7 template's ruling that `—` is a declaration, not a blank. |

Every option changes `REGISTER_SCHEMA_P7_V0` and the rule set sealed in
`WF_P7_DESIGN_INTENT_ADMISSIBILITY_V0`, or the constitutions. All of them were published in v6, so
`published_identity_check` flags them. Each option therefore also needs either new identities with
`supersedes`, or a ruling that the next cut is a genesis.

## What holds

- Construction does not invent design. Every rule that matched by name (bindings, payload reads,
  event field types) broke on a real domain, because business names differ from the names generic
  platform capabilities use. `CC_NO_IMPLICIT_CHAINING` already forbids implicit dataflow.
- The renderer derives a fact from a register only where a register states it. That is why the
  register count is so much lower than the artifact count.
- Two designs are below 100% construction completeness:
  - `ai_governance`, at 1218/1221: three node inputs in `WF_PROVISION_AI_LICENSING_V0`.
  - `transformation`, at 1282/1288: six `core.phases[].gate` facts.

## If this is revisited

Start from the interface rows. They are the one large source. The question to settle first is
architectural: may construction read platform capability specs from the sealed composition while
rendering, as the phase checks already do through `si.capability.surface`? If not, the remaining
redundancy is too small to justify new identities.

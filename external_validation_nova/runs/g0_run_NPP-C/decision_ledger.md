# Decision Ledger

This ledger records the decisions that are class 1 and class 2 under the task's classification scheme. It does not include unresolved or underspecified questions; those are in the findings register.

## Class 1 — realization freedom

| Question | Where looked | Decision made | Why this is class 1 |
|---|---|---|---|
| What file format or encoding shall represent a machine block? | Machine Block §3; 1a §2 | Encoding is left open. Any encoding that losslessly carries the semantic object is admissible. | The family states that representation is not normative and explicitly makes encoding neutral. |
| How the system is internally decomposed into files, services, slots, or processes | Conceptual Model §3.1, §3.3; Machine Block §2; 0z §4 | No implementation structure is required. Internal structure is not a profile decision. | The standard forbids architecture in normative text and defines semantics independent of representation. |
| Whether runtime execution is implemented as a single process or many | Runtime and Architectural Invariants; 1a §8 | It is left open. The runtime is a role, not a component. | The family defines runtime as a role and does not require any implementation topology. |
| Whether the read surface is exposed through a service, API, or direct in-process query | Governed Inspection; 5b §2.1 | The means of access is left open, provided the read surface is declared and governed. | The family distinguishes the boundary from its implementation form. |
| Whether evidence is emitted as logs, records, or signed objects | Evidence and Attestation; 3e; 1a §9 | Evidence is required, but its representation is left open. | The standard defines evidence semantically; encoding is a realization choice. |

## Class 2 — profile decision, specified

| Question | Where looked | Decision made | Why this is class 2 |
|---|---|---|---|
| What is the profile identity? | 6a §9; Identity & Addressing; task commission | The profile identity is NPP-C. | The family requires a profile to have identity and the commission specifies the correct identity for this work. |
| What does the profile profile? | 6a §1; 1a §6 | It profiles a single governed system, sealed, inspected, without external protocol boundary, one tenant, no replication. | This is exactly the scope delegated by the commission under 6a §1 and §7. |
| Whether inspection is required | 5b; 6a §7; task commission | Inspection is required. | The task scope and the family treat inspection as a declared boundary rather than an optional facility. |
| Whether there may be an external protocol boundary | 5a; 6a §1; task commission | No external protocol boundary is admitted under this profile. | The task explicitly narrows the platform to a system without an external wire boundary. |
| Whether attestation beyond the family is accepted | 3e; 6a §7; task commission | No additional attestation regime is accepted. | The profile restricts trust and attestation to the family-defined semantics. |
| Whether the profile permits replication | 3b; 3c; 6a §7; task commission | No replication is permitted. | The profile's scope and the family's semantics distinguish one baseline and one governed state. |
| Whether the profile permits multiple tenants | 1a §6; 2e; 6a §7; task commission | No multiple tenants are permitted. | The profile's authority and scope are intentionally singular. |
| Which kinds are admissible under the profile | 2d; 2c; 6a §7 | The profile closes a vocabulary of four kinds: platform-root, snapshot, inspection-surface, and evidence-record. | 2d requires a closed vocabulary and 6a requires profile closure where the profile supports a claim. |
| Whether the profile may impose additional enforceable requirements | 6a §5; EN-1; NP-6 | The profile adds narrowing obligations that are enforceable and measurable. | The family explicitly permits profile-level additional obligations if they are enforceable and narrow. |
| What claims the profile supports | 6a §5; 7a §3; 7b §3 | The profile supports only the six supported claims listed in NPP-C.md. | The family requires a profile to say which claims it supports and how they are discharged. |
| What the profile excludes | 6a §5; 7a; task commission | It excludes multi-tenant, replicated, externally reached, and any wider platform. | The family requires a profile to state what it excludes. |
| Whether a profile may be derived or narrowed from another | 6a §10 | This profile is not derived from another; it is a direct profile authored for the task's scope. | The family authorizes derived profiles but does not require one here. |

## Decision summary

The profile makes all required selections under Part VI, and it does so within the family's delegated scope. Every selected item is either an explicit profile decision or a realization fact left open by the family itself.

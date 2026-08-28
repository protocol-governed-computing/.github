# Findings Register

This register records every question that had to be answered by the author and that the standard did not answer for us. Each item is classified into exactly one of the classes defined by the task.

## Class 3 — profile decision, underspecified

| Question | Where looked | What I did | Why it counts as class 3 |
|---|---|---|---|
| What counts as an acceptable trust root for a checking party under this profile? | 3e; 6a §7; 7a §4; 7b §3 | I narrowed the profile to accept only family-defined evidence and attestation semantics and refused any non-standard trust root. | The family requires a profile to decide what a checking party accepts, but it does not define a general trust-root policy or a concrete root-of-trust authorization model. |
| What exactly constitutes a “tenant” in a governed system? | 1a §5; 1a §6; 2e; 6a §7 | I treated tenant as a single-authority, single-closure profile decision and excluded multi-tenant arrangements. | The family defines authority and domain but not a normative tenant concept. A profile may define it, but the family does not supply the metric. |
| What determines whether a given system is still one system versus a component composition? | 1a §6; 2e; 6a §7; 4a | I treated the system as one governed subject with one accepted baseline and a single closure. | The family distinguishes a governed system from a composition, but it does not define the concrete boundary test for a single-system claim in a general platform. |

## Class 4 — ambiguity

| Question | Where looked | What I did | Why it counts as class 4 |
|---|---|---|---|
| Does a profile's “no external protocol boundary” mean no externally reachable wire protocol anywhere, or only no protocol boundary in the claimed execution surface? | 5a; 6a §1; 6a §7 | I chose the stronger reading for this profile: no external protocol boundary within the profile's supported scope. | The family distinguishes interaction boundaries and inspection boundaries and permits both, but it does not say whether a profile may define a platform with no external boundary but still support internal protocol surfaces. The texts support more than one defensible reading. |
| Is a domain or tenant a governance concern, an authority, or both? | 1a §5; 2a §8; 2b §7.2; 6c §4 | I treated a tenant as a profile-level scope condition rather than a family-defined authority. | The family separates concern from authority but does not provide a universal rule that converts a domain or tenant into an authority. Two readings are plausible. |

## Class 5 — omission

| Question | Where looked | What I did | Why it counts as class 5 |
|---|---|---|---|
| What is the canonical profile representation or profile grammar by which a system names and claims the profile? | 6a; 7a; 7b; 0z | I recorded NPP-C as a named profile and described its obligations in prose, without claiming a machine-readable or standardized profile syntax. | The family requires a profile identity and claims, but it provides no normative syntax, format, or schema for a profile artifact. The omission is serious because profile claims cannot be mechanically checked without it. |
| What determines a profile's claim vocabulary or claim names? | 6a §5; 7a §2; 7b §12 | I wrote a small, explicit claim set for the profile, but did not assume a family-wide registry of claim identifiers. | The family states that profiles support claims, but it does not supply a normative vocabulary or registry that would make claim names interoperable. |

## Class 6 — reference-shaped assumption

| Question | Where looked | What I did | Why it counts as class 6 |
|---|---|---|---|
| What is the concrete trust-root structure that a checking party is meant to accept when attestation is required? | 3e; EV-9, EV-16; 6a §7; 7a §4 | I refused any non-standard trust root and limited the profile to family-defined evidence and attestation semantics only. | The family names evidence and attestation but does not specify the concrete structure or trust-root regime by which a real checking party settles trust. That missing structure is only knowable from a concrete realization, which this task forbids consulting. |
| How does a real system identify the authority that may change a profile under a claimed identity? | 6a §6; 6a §9; 4e; 2e | I treated the profile as externally authored and not authored by the claiming system, but I did not invent a concrete mechanism for profile authority change. | The family requires externality of authorship but not a concrete authority mechanism for profile change; the mechanism is only knowable from an existing realization, which would be a reference-shaped assumption. |

## Summary

The profile is still useful as a constrained, reviewable statement under the profile's own scope, but the standard leaves a number of profile-level operational details unresolved. Those gaps are recorded here as findings rather than silently filled by authorial assumption.

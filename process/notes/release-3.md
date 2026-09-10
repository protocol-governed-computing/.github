release 3 — snapshot_inspector CLI and web UI

Added the snapshot_inspector CLI and web UI, and the governed boundary that serves them.

- snapshot_inspector answers 16 si.* operations behind inspector.api.query; the si CLI and the
  Inspection Surface (the second out-of-box reference implementation) are both clients of it.
- New composition unit: the inspection:: TOOL DOMAIN — 32 TI/TE boundary contracts, and the first
  PGC domain with no WF/CC/RB. A tool domain declares capabilities about a snapshot rather than
  within one, consumes the assembled snapshot as the runtime does, and composes like any other.
- The protocol declares the operation set: a TI declares an operation's identity, handler kind,
  input contract, presentation, and the {module, callable} that answers it. inspector.registry
  holds implementations and no metadata at all.
- Transport implements all three handler kinds — WF_INVOCATION, SNAPSHOT_READ, SNAPSHOT_QUERY —
  and operation_in_body bindings, where a namespace is an admission constraint the adapter checks,
  never a dispatcher it branches on.
- The assembler now produces an INSPECTABLE snapshot, not merely an executable one: store_index
  joins storage ownership to its binding surface, and kind_index cross-references were vacuous
  because they read the compile trace instead of the semantic graph.
- compiler/inspection retired — 3,215 lines, superseded by snapshot_inspector.
- Console scripts dropped the pgc_ prefix: protocol_compiler, snapshot_assembler,
  protocol_runtime, si.

Governance surface changed. Result Class NOT_FOUND admitted, distinct from OPERATION_NOT_FOUND;
INVARIANT_TRANSPORT_TARGET_EXISTS_V0 is now handler-kind aware; CANONICAL_NORMALIZATION accepts an
empty input_contract as a declaration rather than an absence; new
INVARIANT_INSPECTION_BOUNDARY_COMPOSED_V0, introducing the composition_conformance enforcement
stage and the at_least_one cardinality rule.

Operational: the governance closure hash MOVED this cycle — 47d603fb25977a05, 69 members. Every
domain MUST be recompiled; stale domains are rejected at assembly by design. Assemble with no
arguments: any argument bypasses auto-discovery, and an explicit --source list silently omits
domains added later.

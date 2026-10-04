release 17 — the identity covers what it claims, and a run explains itself

This cycle is published as `v5`. It changes what a sealed composition admits and what a run can
answer about itself. The snapshot identity now covers the profile's content. A superseded artifact
no longer confers effect. A trace now records enough for the inspector to attribute each decision to
the sealed model. Eight domains, 500 protocol artifacts, composition conformance PASSED over five
rules. The sealed snapshot is `f8356d9c8938aea16ab7850d7bda964d8d16c42c64e5db9056d5fe58040ec1d0`.
A clean `regression.sh --all` runs 59 of 59 steps as expected.

## What was actually done

**The identity covers the profile's content (A1).** The manifest carries `profile_sha256` and names
it in `identity_covers`. Acceptance recomputes it from the profile as it reads now. A profile changed
after sealing is refused, and so is a manifest that does not cover its profile.

**Presence is not force (A11).** `INVARIANT_SUPERSEDED_NOT_IN_FORCE_V0` declares one predicate. The
compiler realizes it once and asks it at selection, assertion derivation, dispatch entry and
admission. Two superseded workflows had been dispatchable, and the catalog's CR-01 validation ran
one. It now runs the act in force.

**Evidence says where and why.**
- A trace names the node, not only the contract (A9). One contract at two places is now two places.
- The trace schema describes the trace PGC writes (A5). A regression step checks every trace line
  against it.
- What a replay ignores is declared in the evidence vocabulary and carried in the trace header
  (A3, A4).
- The runtime records every admission check it evaluated, held or not.
- `si.execution.explain` reads a trace against the snapshot it names. It reports the path, the
  outcome that chose each route, where the run was decided, and which capability decided it. It
  refuses a trace that names another snapshot. The run's picture is drawn from its answer.

**The governance surface.** Handler keys say `pgc_governance.handlers.*` (A2). The transform-wide
rules moved to `CONSTITUTION_CAPABILITY_TRANSFORMS_V1` (A6). `cryptographic_trust` is V1, and the
federated build declares `SIGNED_SNAPSHOT` (A7). A federated node declares its record-lock
requirement (A8). Each build configuration declares its output root, and the compiler no longer reads
`PGC_SNAPSHOT_ROOT` (A10).

**Domains changed what they decide, each through its own change request.**
- Blockchain `cr_05_identity`: identity's rules are literals, an incomplete registration is refused,
  and self-decision is refused.
- Book `cr_05_catalog`: the catalog holds its authorization rules. Before, an unauthorized caller
  registered a book by sending no rules.
- ai_governance `cr_01_licensing`: its three checks are proven by seven declared cases.
- Language model `cr_02_hosted_model`: the domain governs a hosted model, and can require every number
  in a response to be one the model read.

**The runtime is fast enough to stop noticing.** A booted snapshot stays resident per process. A
governed run takes about 5 ms after the first. A run writes its trace only, and draws its picture on
demand.

**Defects fixed.** `examine` reads PGC traces (B21). Events are schema-checked (B22). The blockchain
web page names the acts in force (B23). The dead platform build configuration is deleted, and
`compile` requires `--structure` (B24). P7 holds an entrance to the gate it reaches (B25). The
regression has a verdict and fails on any unexpected count (B13, B20).

## Stated limits

- **C1.** A generated dossier is admitted on what it says. Its generator is kept as evidence in its
  `delivery.md`. Governed generation is v6 work.
- **C5.** After a dropped connection, a caller cannot tell whether it was admitted. An idempotency key
  with an admission-status query is v6 design work.
- **An unrouted act outcome is refused late.** Construction admits a workflow that leaves an outcome
  an act can surface without a route. Execution refuses it with no declared answer, and adds no
  behaviour. The sealed composition holds 11 such outcomes, all storage failures in blockchain.
- **The runtime continues past an outcome a step omits.** Construction does not check that a step
  lists every outcome its operation declares, and 14 of 73 such steps list fewer. When an operation
  reports an unlisted outcome, the runtime continues to the next step, and the trace does not record
  the step's outcome. With a corrupted contact-address registry, a failed lookup let a person be
  accepted. This breaks non-addition. The fix is a construction check, a runtime that refuses, and a
  trace that records each step's outcome.
- **A pre-`v5` snapshot is refused.** It carries no `profile_sha256`. That includes the `v4` snapshot
  in `pgc_release`, which `v4`'s tooling still verifies.
- **Deployment.** The SSH exception to EO-4 stands. `EVIDENCE_EXPIRY` is not exercised over the shared
  store, and cross-node concurrency only lightly. The evidence store is not external to every node.
- **Only someone else can close.** A second reader, and a read-back of the signed federated profile
  by someone other than the author.
- **Deferred.** B17, the signed federated profile existing twice, waits for the next standards
  revision. B18, 13 domain transforms unproven and implementation source not sealed by hash, is
  recorded, not fixed.

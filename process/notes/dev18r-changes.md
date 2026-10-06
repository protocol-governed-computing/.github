# dev/18r — platform change notes

One entry per platform change, in step order. Domain changes have their own dossiers.

## Step 2 — The rebuild keeps the previous build until the new one is assembled

**Problem.** `regression.sh --build` and `--all` deleted every snapshot, `data/` and `traces/` before
they compiled anything. If the build then failed, there was no snapshot left, and every later check
failed because of that rather than for its own reason. In dev/18 this happened four times, and each
time the snapshot was restored by hand.

**Change** (`process/regression.sh`):
- The previous build output is moved to a temporary directory, not deleted. That covers each
  `snapshot/`, `software_governance/snapshot_fed` and `snapshot_mw`, `data/` and `traces/`.
- If any compile or assembly step fails, the partial output is removed and the previous output is
  moved back. The script then exits 1.
- After a successful assembly, the backup is deleted.
- `pgc_release/snapshot` is still excluded, and the check that it survived still runs.

**Verified.**

| Case | Command | Result |
|---|---|---|
| Failed build | `PGC_SNAPSHOT_PROFILE=NO_SUCH_PROFILE_V0 regression.sh --build` | The assembler refuses and the script exits 1. All 1,270 build-output files come back, and the checksums of `snapshot/`, `snapshot_mw/` and the blockchain snapshot match. No backup is left behind. |
| Successful build | `regression.sh --all` | 59/59 as expected. No backup is left behind. |

## Step 3 — The platform declares what a reference is

**Problem.** The platform decided what a reference is in three places, and they disagreed:
- S1's record of references read a fixed list of nine keys;
- the superseded check walked every value shaped like a full name;
- construction had no notion of a reference at all.

So a reference could be missed by one place and seen by another.

**Change.**
- **`software_governance`.** New `artifact::VOCAB_DECLARATION_REPRESENTATION_V0` declares the parts
  that only explain, the unordered lists, the reference parts (`code` included), the keyed reference
  part (`bindings`), the parts that require a full name, the supersession parts and the two sameness
  rules. It is new, so no published identity changes.
- **`protocol_compiler`.**
  - New `compiler/atoms/representation.py` reads the declaration by its exact identity.
  - S1 records references from the declaration and refuses a full name in an undeclared part
    (`E105_UNDECLARED_REFERENCE`).
  - The FQDN-only and superseded handlers read the declaration. The superseded handler reads a
    workflow's own place labels as labels.
  - S4 passes the declaration to every handler.
  - New test: `test_reference_semantics`. `test_vector_build` expects the refusal of a dangling
    target.
- **`snapshot_inspector`.** `si.artifact.refs` reads the composition's record of references.
- **`transformation`.** New `build/sameness.py` compares two declarations by the platform's
  declaration. Only the published-identity check uses it so far; construction uses it from step 4.
- **`.github`.** New `published_identity_check.py`. It compares every identity published in v5 with
  the working composition and fails on a change of meaning or a missing identity. It is added to the
  regression, the RUNBOOK and the README.

**Verified.** `regression.sh --all`: 61/61 as expected.
- 505 artifacts, 7 supersession relations.
- Construction acceptance 167/167.
- `test_reference_semantics` 15/15; `test_vector_build` 4/4; `test_inspector` 152/152.
- Published identity: 500 identities published in v5, none changed meaning.
- **Probe.** On `blockchain::CC_RESOLVE_ACTOR_V0`, the comparison reports an added outcome
  (`core.result_surface`) and ignores a reworded `summary`.

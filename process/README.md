# `.github/process`

**Workspace process: how a composition is checked, cut, and recorded.**

This directory is the only place in the workspace where cross-repository process lives. Nothing here
is a governed artifact, nothing here is compiled, and nothing here ships in a wheel. It is the
machinery that operates on the ten repositories rather than anything belonging to one of them.

## What is here

**Two entry points.** Everything else is called by one of them or run by hand.

| | |
|---|---|
| `regression.sh` | build, check, execute. `--all` is the full pass; `RUNBOOK.md` states what each step should print |
| `release.sh` | preflight, cut a cycle, publish it. `--check` changes nothing and is safe to run any time |

**Checks.** Each answers one question about the composition and exits non-zero when the answer is
wrong. All are called by `regression.sh --all`, and each is runnable alone.

| | |
|---|---|
| `governance_closure.py` | every compiler handler is named by an invariant; no layer is declared two ways |
| `governance_chain_closure.py` | every authored invariant is named by a constitution rule |
| `supersession_agreement.py` | a supersession is stated on both sides and the two agree |
| `human_block_fidelity.py` | prose beside a machine block declares nothing |
| `frontmatter_fidelity.py` | every authored machine-block value survived compilation |
| `evidence_determinism.py` | determinative evidence content is identical across runs; observational content differs |
| `admission_contract_fidelity.py` | an IN gate's declared contract matches what its workflow binds |
| `implementation_closure.py` | every capability transform names a module and every named module exists |
| `domain_authoring.py` | the domain-authoring path `pgc_install/README.md` documents, executed |
| `pgc_env_check.py` | the active interpreter is the workspace venv and no RI-0 package is reachable |

**Release machinery.**

| | |
|---|---|
| `compose_release.py` | regenerates `pgc_release` from the sealed snapshot. Called only by `release.sh --publish-composition` |
| `notes/release-<N>.md` | one file per cycle, written before the cut. The durable record of what a composition was |

**Reference.**

| | |
|---|---|
| `RUNBOOK.md` | the end-to-end sequence by hand, and the expected result of every check |
| `requirements-domains.txt` | optional domain dependencies, never needed by the core compile path |
| `task_environment_profile*.md` | an authoring task given to an external party, kept with its operator brief |

## What belongs here, and what does not

A thing belongs here if it **operates on the composition as a whole** and has no single owning
repository. A check that reads across repositories, a script that cuts a release, the record of what
a cycle contained.

A thing does **not** belong here if:

- **it belongs to one repository.** A test of the assembler's indexes belongs in
  `snapshot_assembler/scripts/testbed/`, not here — its failure is that repository's failure.
  `regression.sh` calls such tests where they live rather than hosting them.
- **it is a governed artifact.** Constitutions, invariants, schemas and structures live in
  `software_governance/registry/`, are compiled, and are subject to the machinery here. Nothing in
  this directory is admitted, determined, or sealed.
- **it is a document about the platform rather than about operating it.** `doc/` holds the session
  handoff and analyses awaiting a decision. A design ruling or a finding goes there or into the
  owning repository, not beside the scripts.
- **it is a conformance contract.** Snapshot profiles are `../snapshot_profiles/`. They are read by
  the assembler and the runtime, so they are inputs to a build rather than process.

## Adding a check

A check earns its place by failing when something is wrong and by being run. Two rules, both learned
the hard way in this workspace:

**Wire it into `regression.sh` in the same change.** Five test files once sat here and in the
component repositories unrun; two of them had been failing for months and nobody knew, because
nothing invoked them. An unrun check is worse than no check — it reads as coverage.

**State its expected output in `RUNBOOK.md`.** Including when the expected output is a failure. Two
things are red by design, and a run that is entirely green means something stopped reporting.

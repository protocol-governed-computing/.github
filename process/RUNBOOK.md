# End-to-End Runbook

A clean-slate build of the composition, then one check per domain.

The transformation phases are checked by a single script rather than one runbook line per phase.
The phase count grows; the runbook does not.

---

## Run it all: `regression.sh`

Everything below, scripted.

```bash
bash ~/protocol-governed-computing/.github/process/regression.sh --all
```

| Invocation | Runs |
|---|---|
| `regression.sh` | the execution block only — fastest, and assumes a built snapshot |
| `regression.sh --build` | clean rebuild, then the execution block |
| `regression.sh --all` | clean rebuild, then every check, then execution |

**The run ends with a verdict, and exits with it.** Every check and execution step runs through
`step`, which keeps the step's output and exit code in `traces/regression/` (or
`$PGC_REGRESSION_OUT`). `regression_verdict.py` then compares each step against
`expectations.yaml`, the table under "## Expected" as data. The run fails on:
- a step that fails, or prints a different count;
- a step red by design that comes back green (an **unexpected pass**);
- a step expected and not run, or run with no expectation.

`REGRESSION PASSED — every step as expected` is the only green. When a result changes on purpose,
change `expectations.yaml` in the same commit, and this file when what a step proves changes.

**`--build` and `--all` delete every generated snapshot**, not only the assembled one — each
domain's `snapshot/` as well, so a clean rebuild is a fact rather than a claim. A retired artifact
left in a domain's `compiled/` is caught by S8 as an undeclared output, which reads as a compiler
defect rather than as stale state.

**`.DS_Store` is swept workspace-wide, `pgc_release` included.** macOS writes one into any directory
Finder opens; acceptance then refuses the snapshot as carrying undeclared content (3b §6). That is
correct behaviour, but it makes a DOI-cited release look corrupt when nothing about it changed, and
because these files are gitignored `git status` stays clean and nothing warns you. Removing them
cannot destroy anything — a `.DS_Store` is never a constituent, and none is tracked in any repo.

**`pgc_release/snapshot` is excluded, and the script aborts if it ever isn't.** That directory is the
sealed composition a paper cites by DOI — written once by `release.sh --publish-composition`,
reproduced by nothing, recoverable only from git. Do not simplify the cleanup to `rm -rf */snapshot`:
it misses the nested ones under `business_domains/*` and `conformance_workloads/workloads/*`, and it
does not protect the one that matters.

**One run checks one profile.** A snapshot claims exactly one profile identity, and the run claims
`GOVERNANCE_SURFACE_PROFILE_V0` — the profile in force, which supersedes
`REFERENCE_PLATFORM_PROFILE_V1`. `PGC_SNAPSHOT_PROFILE` overrides it, which is how a candidate
profile is read against the composition before it is put in force.

`SIGNED_FEDERATED_MULTINODE_PROFILE_V0` is such a candidate and coexists rather than competing: it
supersedes nothing, because it invalidates nothing about the composition claiming the profile in
force. Running it needs no change to this script —

```bash
PGC_SNAPSHOT_PROFILE=SIGNED_FEDERATED_MULTINODE_PROFILE_V0 bash regression.sh --all
```

— and answers a different question, since it requires fifteen kinds where the profile in force
requires seven, and obliges a signed snapshot that a default run neither produces nor checks.

**One surface, three compositions.** Placement is selected by a build configuration rather than marked
on an artifact, so the surface declares what is available and a build declares what is active:

| Build configuration | Placement | Output root |
|---|---|---|
| `STRUCTURE_BUILD_PLATFORM_CONFIG_V0` | `LOCAL_SINGLE_NODE` | `software_governance/snapshot` |
| `STRUCTURE_BUILD_PLATFORM_MULTIWORKER_CONFIG_V0` | `LOCAL_MULTI_WORKER` | `software_governance/snapshot_mw` |
| `STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V0` | `FEDERATED_NODE` | `software_governance/snapshot_fed` |

A default run builds the first. The others are built by naming them:

```bash
protocol_compiler/compile.sh STRUCTURE_BUILD_PLATFORM_MULTIWORKER_CONFIG_V0
```

**Each configuration declares its own root** in `output_configuration.root`, and the table's last
column is that declaration. Nothing on the command line overrides it, and two in-force configurations
of one repository naming the same root are refused, so the compositions cannot overwrite each other.
`python -m compiler.cli output-root --structure <code>` prints where a configuration writes.

The federated composition runs on a node group, not in place. Its nodes are configured by hand per
`process/deploy/NODE_CONFIG.md`; `process/deploy/DEPLOYMENT.md` gives the topology and the checks.
`protocol_runtime/testbed/pgc/test_federation.py` exercises the same arrangement as processes on one
machine.

**Signing is optional and off by default.** `assemble --signing-key` writes a signature beside the
manifest; a node holding `PGC_TRUST_ROOT_PUBKEY` requires and checks one, and a node holding no
anchor boots an unsigned snapshot exactly as before. A default run neither signs nor checks, which
is why the profile's OB-1 is not exercised by it.

**What a regression run does not establish about the signed profile.** It composes and it satisfies
the machine-checked floor. The obligations about placement — several addressable nodes, an evidence
store held by none of them, a build machine that is not one of them — are not exercised by any run
on one host. Only a deployment on a node group, read back against the profile, can show them.

A default run answers whether the profile is *satisfiable* over the reference composition: seven
domains, one of them a workload. It does not establish the narrower claim the profile is written for
— a profile requiring no workload is not tested by a snapshot containing one. For that, restrict the
sources and send the result elsewhere, so the composition the rest of this runbook assumes is left
intact:

```bash
PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 \
PGC_SOURCE_ROOTS="$PWD/software_governance/snapshot/compiled:$PWD/snapshot_inspector/snapshot/compiled" \
PGC_SNAPSHOT_OUT="$PWD/snapshot_skinny" \
  ./snapshot_assembler/assemble.sh
```

`assemble.sh` refuses by default when a domain declares source but has no compiled output, precisely
so a skipped compile cannot silently narrow a composition. `PGC_SOURCE_ROOTS` is the deliberate way
to narrow one, and bypasses that guard — which is the point, and the reason to be explicit about it.

**Prefer it to pasting.** The commands below are long and single-line by necessity, and a terminal
that wraps one splits an argument from its flag: `--payload` loses its value, the shell tries to
execute a JSON path, and the result reads like a test failure rather than the shell error it is.
That has cost two clean runs.

**It is not a substitute for reading `## Expected`.** The script reports what each step printed; it
does not judge. One thing is red by design, the advisory half of `si snapshot validate`, so a run
in which it reports nothing means something stopped reporting.

**Prerequisite for a rebuild.** `--build` and `--all` assume the workspace venv has every package
editable-installed under its current distribution name. After a rename or a fresh clone:

```bash
cd ~/protocol-governed-computing
find . -maxdepth 2 \( -name build -o -name '*.egg-info' \) -not -path './.venv/*' -exec rm -rf {} +
for r in protocol_compiler snapshot_assembler protocol_runtime snapshot_inspector \
         transformation software_governance conformance_workloads; do .venv/bin/pip install -e "$r"; done
python .github/process/pgc_env_check.py
```

Stale `.egg-info` under a superseded name is the failure mode here: setuptools may read it in
preference to the current metadata, and the run then exercises a package that no longer exists.

The sections below are the same sequence by hand, and remain the reference for what each step is for.

---

## Build

**Neither tool defaults.** `compile.sh` requires the STRUCTURE and `assemble.sh` requires the
profile, because a platform is whatever a build config declares and none is minimal by nature
(`6a` §8), and a snapshot must **name** the profile it claims (`1b` §11, SN-5) — a default would
have the assembler supply the one condition genesis takes from outside itself. Both refuse with the
clause they enforce.

```bash
cd ~/protocol-governed-computing
export PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0

~/protocol-governed-computing/protocol_compiler/compile.sh STRUCTURE_BUILD_PLATFORM_CONFIG_V0

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/conformance_workloads/workloads/collatz

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/transformation_compilers

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/snapshot_inspector

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/business_domains/ai_governance

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/business_domains/book_library_mgmt

~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/business_domains/blockchain

PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 ~/protocol-governed-computing/snapshot_assembler/assemble.sh
```

Every domain that declares source must be compiled — the assembler refuses otherwise rather than
silently producing a smaller composition. If a compile step is skipped it names the command to run.

A build list that omits a domain is indistinguishable from a domain that declares no source, which
is why the assembler names the command rather than proceeding: every runtime check afterwards would
fail on a snapshot that was never written.

**Every build proves the transforms it supplies.** `compile.sh` and `compile_domain.sh` run
`runtime conformance` once the compile succeeds, and exit non-zero when any case fails. Each build
prints one line, naming every transform it supplies as proven, unproven or refused, and counting the
platform transforms it carries. The platform supplies its own twelve transforms and proves them; each
of its three builds prints the same line:

```
[conformance] platform: 11 proven, 1 unproven, 0 refused, 0 carried from another surface (49 case(s))
[conformance] workload: 0 proven, 2 unproven, 0 refused, 0 carried from another surface (0 case(s))
[conformance] transformation: 0 proven, 6 unproven, 0 refused, 0 carried from another surface (0 case(s))
[conformance] inspection: 0 proven, 0 unproven, 0 refused, 0 carried from another surface (0 case(s))
[conformance] ai_governance: 0 proven, 3 unproven, 0 refused, 4 carried from another surface (0 case(s))
[conformance] book_library_mgmt: 0 proven, 4 unproven, 0 refused, 5 carried from another surface (0 case(s))
[conformance] blockchain: 0 proven, 1 unproven, 0 refused, 6 carried from another surface (0 case(s))
```

The platform's unproven transform is `CT_PURE_COMPARE_EQUAL_V0`, which no inherited vector tests. A
domain's transforms stay unproven until the domain's own change gives them vectors, and a count moves
only when that change lands. **Any refused transform, or any failed case, is a defect.** Unproven is
never reported as passing.

What a build supplies and what it carries is read from its attestation's `imported_capabilities`, never
from a name. The result is written to `<build>/snapshot/compiled/transform_conformance/result.json`, or
under the build's own root for a placement build. The assembler carries it to
`snapshot/transform_conformance/<build>/`, and it is part of the snapshot's identity. The platform's
vectors are declarations: `si artifact list --kind TEST_DATA` lists them.

**A rebuild reproduces its identity, and that is worth checking when anything near the assembler or
the attestation changes.** Recompile one domain and reassemble twice; the `snapshot_id` must not move.

```bash
for i in 1 2; do
  rm -rf transformation/snapshot/compiled
  protocol_compiler/compile_domain.sh transformation >/dev/null
  PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 snapshot_assembler/assemble.sh | grep snapshot_id
done
```

Two different identities means something the composition carries changed without the source changing.
An attestation records when it was signed; if the identity were taken over that, it would be a function
of *when* the composition was built, and a genuine alteration would be indistinguishable from a no-op
recompile. `cryptographic_trust::CONSTITUTION_CRYPTOGRAPHIC_TRUST_V0` declares which of an attestation's
fields constitute the composition and which merely accompany it, and the assembler reads that division
in both the enumerator and the verifier. Evidence paths are recorded relative to the declared output
root, so the build folder does not enter the identity either.

## Check

Paste the whole block. It runs from a clean state every time --- the domain validations accumulate
into their data roots and refuse a root that already has their stores, so the block clears them
first.

```bash
# generators agree with what they produce
python ~/protocol-governed-computing/.github/process/governance_closure.py
python ~/protocol-governed-computing/.github/process/governance_chain_closure.py
python ~/protocol-governed-computing/.github/process/supersession_agreement.py
python ~/protocol-governed-computing/.github/process/human_block_fidelity.py
python ~/protocol-governed-computing/.github/process/evidence_determinism.py
python ~/protocol-governed-computing/transformation_compilers/scripts/emit_rule_sets.py --check
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/build_payloads.py --check
PYTHONPATH=~/protocol-governed-computing/snapshot_inspector \
  python ~/protocol-governed-computing/snapshot_inspector/scripts/author_transport_contracts.py --check
python ~/protocol-governed-computing/.github/process/frontmatter_fidelity.py

# the phase testbeds
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/meta_test.py
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/closure_test.py
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/effectivity_test.py
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/render_vectors_test.py
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/construction_mapping_test.py
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/interface_structures_test.py
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/differential.py
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/e2e_phases_test.py
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/projection_test.py
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/construction_acceptance.py

# closure and environment
python ~/protocol-governed-computing/.github/process/implementation_closure.py
PYTHONPATH=~/protocol-governed-computing/snapshot_inspector \
  python ~/protocol-governed-computing/snapshot_inspector/scripts/testbed/test_inspector.py
python ~/protocol-governed-computing/.github/process/pgc_env_check.py

# execution — from empty data roots
rm -rf ~/protocol-governed-computing/data/collatz ~/protocol-governed-computing/data/ai_governance ~/protocol-governed-computing/data/book_library_mgmt \
       ~/protocol-governed-computing/data/book_library_mgmt_works ~/protocol-governed-computing/data/blockchain

~/protocol-governed-computing/protocol_runtime/run.sh run --wf workload::WF_COLLATZ_CONJECTURE_V0 --payload ~/protocol-governed-computing/conformance_workloads/workloads/collatz/test_payloads/01_happy_path.json --data-root ~/protocol-governed-computing/data/collatz

P=~/protocol-governed-computing/business_domains/ai_governance/testbed/ai_licensing/test_payloads
for step in SET_LICENSE_CAP:01_set_license_cap REGISTER_EMPLOYEE:02_register_employee_std \
            RECORD_TRAINING_COMPLETED:03_record_training_std PROVISION_LICENSE:04_provision_license_std; do
  ~/protocol-governed-computing/protocol_runtime/run.sh run --wf "ai_governance::WF_${step%%:*}_V0" --payload "$P/${step#*:}.json" --data-root ~/protocol-governed-computing/data/ai_governance
done

~/protocol-governed-computing/protocol_runtime/run.sh run --wf ai_governance::WF_GOVERN_AGENT_ACTION_V1 --payload ~/protocol-governed-computing/business_domains/ai_governance/testbed/agent_governance/test_payloads/01_valid_standard_action.json --data-root ~/protocol-governed-computing/data/ai_governance

python ~/protocol-governed-computing/business_domains/ai_governance/testbed/owner_decisions/execution_validation_owner_decisions.py

python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py --data-root ~/protocol-governed-computing/data/book_library_mgmt

python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation_works.py --data-root ~/protocol-governed-computing/data/book_library_mgmt_works

python ~/protocol-governed-computing/business_domains/blockchain/testbed/identity/execution_validation.py --data-root ~/protocol-governed-computing/data/blockchain

python ~/protocol-governed-computing/business_domains/blockchain/testbed/wallet/execution_validation.py --data-root ~/protocol-governed-computing/data/blockchain
```

**`frontmatter_fidelity` reads the assembled snapshot**, so it belongs after Build rather than before
it. Everything above it reads artifacts as authored and runs at any time.

**Both blockchain suites run into one root**, because a domain has one place its records live. Each
seeds people of its own so they never collide, and each refuses only its *own* stores being already
present rather than the whole root. Run identity first, then wallet; the result is
`<root>/blockchain/identity/` and `<root>/blockchain/wallet/` side by side, with one traces directory.

**The two catalog suites need separate roots.** Both write `book_library_mgmt/catalog`, so sharing one
would leave the second refusing a root the first had already filled.

**`implementation_closure`** checks both ends of the one pointer an artifact makes outside the
composition: a transform module nobody names, and an artifact naming a module that is not on disk.
Neither is visible to any phase rule, because neither has a design to judge.

**`construction_acceptance` covers every designed root.** Each carries one design of record in
`<root>/design/`, generated from its registry by `transformation.record`. Acceptance renders it and
compares the result with the registry. `baseline_designs` refuses a design its registry no longer
generates, so the two checks together say the design states the registry whole.

Every path is absolute; the `cd` is convenience only.

## Expected

Rows are in the order the block runs them. **`expectations.yaml` is what is checked**, counts
included; this table explains what each step proves and states no counts. The step ids there are the names below.

| Check | Result |
|---|---|
| `governance_closure.py` | `GOVERNANCE CLOSURE PASSED` — every compiler handler is named by an invariant, and no layer is declared two ways |
| `governance_chain_closure.py` | `GOVERNANCE CHAIN PASSED` — every authored invariant is named by a constitution rule, and every authoring build reaches the chain. An `orphan invariant` line means an obligation nobody's constitution names: author the rule, or the obligation is ungoverned rather than leniently governed |
| `supersession_agreement.py` | `SUPERSESSION AGREEMENT PASSED — N relation(s), M predecessor(s) present, K deleted by record` — the relation is declared once, on the successor, and the compiler derives which artifacts are superseded from it. A successor may name an absent predecessor only when `retired_identities.yaml` records its deletion |
| `published_identity_check.py` | `PUBLISHED IDENTITY FAILED — n of N identities published in v5`, exit 1, red by design while the v6 baseline is built: it compares the working composition with the last sealed release, and the baseline changes what v5 published, by ruling. From the cut it compares against v6, passes, and its entry in `expectations.yaml` returns to a plain pass |
| `human_block_fidelity.py` | `HUMAN BLOCK FIDELITY PASSED` — the prose beside a machine block declares nothing. A `RESTATED` line means delete the prose copy, never edit the machine block; a `SECTION` line means the section is named as if it states a rule. The policy is `vocabulary::VOCAB_HUMAN_BLOCK_CONSTRAINTS_V0`, read from the sealed composition — add a forbidden name there, never here. Reasoning: Field Manual, *The human block* |
| `evidence_determinism.py` | **Give `PGC_SNAPSHOT_ROOT` an absolute path or leave it unset** — this check shells out to `run.sh`, which resolves a relative one against its own directory and fails in a way that reads like a determinism defect. `EVIDENCE DETERMINISM PASSED` — one workflow run twice; determinative content identical, observational content differs. A `DETERMINATIVE CONTENT DIFFERS` line means something non-deterministic is classified determinative; a `vacuous` line means nothing observational varies, so the split is untested. Policy: `vocabulary::VOCAB_EVIDENCE_CONTENT_CLASSIFICATION_V0` |
| `test_admission_covers_bindings.py` | `4/4 passed` — a workflow binds only payload fields its IN gate declares. The rule is the compiler's (`INVARIANT_ADMISSION_COVERS_BINDINGS_V0`), so every build enforces it, not only this workspace's regression. |
| `emit_rule_sets.py --check` | Every phase `OK` — the sealed rule set matches the declared one |
| `build_payloads.py --check` | `OK` — every phase payload matches the corpus document it is cut from. A `DRIFTED` line is a hand-edited payload; fix the source document and regenerate |
| `author_transport_contracts.py --check` | `OK` — every `si.` boundary contract matches the declaration that generates it. A `DRIFTED` line is a hand-edited artifact; fix the declaration, never the artifact |
| `frontmatter_fidelity.py` | `FRONTMATTER FIDELITY PASSED` — every authored Machine Block value survived compilation. The compiler may add; it may never overwrite |
| `meta_test.py` | `META PASSED` — every declared rule resolves to a check kind, and every kind is declared |
| `closure_test.py` | `CLOSURE PASSED` — every `x-realises` resolves, every design invariant is realised, every template agrees with its schema |
| `effectivity_test.py` | `EFFECTIVITY PASSED` — every rule set is its schema's last revision; header, approval and rule-difference cases hold |
| `render_vectors_test.py` | `RENDER VECTORS PASSED` — every value form renders as DESIGN_LANGUAGE §1.2 specifies |
| `construction_mapping_test.py` | `CONSTRUCTION MAPPING PASSED` — CONSTRUCTION_MAPPING.md states every field construction writes, with its class |
| `interface_structures_test.py` | `INTERFACE STRUCTURES PASSED` — what the readers and the evaluator return conforms to the STRUCTURE each field names |
| `differential.py` | `DIFFERENTIAL PASSED` — the sealed rule set and the declared one agree on every corpus document |
| `e2e_phases_test.py` | `E2E PASSED` — every phase, both admissible and inadmissible, through the runtime |
| `projection_test.py` | `PROJECTION PASSED` — reproducible, general, and refusing an inadmissible prior |
| `construction_acceptance.py` | `n/N artifacts reproduced across 6 domain(s)` — every designed root's design of record rendered and compared with its registry: the four business domains, the Collatz workload and transformation. An artifact a generator produces is reported `GEN` and compared by that generator's own check. A build manifest is determined by no design. The platform and the inspection surface carry no design of record: the platform's governance kinds are ones the design language cannot state, and the inspection contracts are generated from their declaration |
| `molecule_design_test.py`, `vector_design_test.py` | The design language renders a molecule's steps, and a transform's cases as its vector, and each rule that holds them fires on the defect it names |
| `keyed_node_design_test.py`, `refusal_moment_design_test.py` | A node is a key and the contract it runs a column, and a route to a place the composition already has resolves; a refusing ending announces only a declared refusal moment |
| `semantic_change_design_test.py` | Construction compares every amendment with the composition by the platform's declaration and refuses a change of meaning under an old identity; an amendment built without `--snapshot` is refused; a design re-points a reference with `REPOINT`; a replacement whose live referrer the design does not account for is refused; P7 refuses a `withdrawn_facts` row |
| `implementation_closure.py` | `IMPLEMENTATION CLOSURE PASSED` — every transform module named by an artifact, every named module present |
| `test_inspector.py` | `PASSED` — every `si.*` operation against fixture snapshots, including `si.kind.map` counting pairs rather than edges, narrowing to one composed domain, and its exported page carrying no server reference |
| `si snapshot validate --strict` | Reads **the snapshot just assembled**, which `test_inspector.py` does not — that runs against fixtures. Every check holds at zero, advisory ones included: `--strict` fails the step on any finding. `republished_copies_agree` holds because a domain that runs a platform capability carries a copy recording exactly what the platform records; `bound_paths_declared_as_stores` holds because every path a runtime binding writes is a store its storage structure declares |
| `domain_authoring.py` | Authors the smallest domain from scratch in a temporary directory, compiles it against the platform, composes, boots and executes it. This is the path `pgc_install/README.md` documents for a domain developer, run rather than described. A failure means the README is wrong, not the platform. It pins four things that were each wrong when that guide was first written: all five projection paths are required and their absence fails at S7 rather than early; `structure_scope` names the composed domain, so a generic value assembles and conforms under the wrong name; a domain composes without violating the claimed profile; and an unimportable domain returns `VIOLATION` with null outputs rather than raising |
| `tc phase derive check`, `tc phase derive meta`, `tc phase derive selftest` | The Design Compiler's derive route admits each domain's ledger; its doctrine, ledger schema and catalog are each their last sealed revision, and every doctrine rule cites an invariant the composition holds or says why none states it; and each answer the self-test puts outside its shape is refused |
| `route_seal_test.py` | `5/5 passed` — the route as it stands is one a dossier sealed; a changed or added building block refuses every derivation, and a seal whose dossier has no `change.md` is refused |
| `repoint_callers_test.py` | `6/6 passed` — a caller outside the domain follows each successor; history, the domain itself and a short name in a file that does not name the domain are left alone; a caller of a retired artifact, or another domain's declaration, refuses the delivery |
| `criteria_before.sh <domain> 36bc62a <suite>` | Each delivered domain's owner-decision criteria against the domain before the derive route designed it: book `0/8`, blockchain `2/9`, ai_governance `4/21`. Each criterion that holds there is behavior the owner kept |
| `derive_build.sh <domain>` | One ledger derived; its identities decided by meaning against the working snapshot; its phase documents P0 to P6 projected and judged by the sealed rules, `phase documents: 7/7 admissible (p0 to p6)`; and the design built in scratch: construction at 100%, emit compared by construction, compile, assembly, and the domain's suites run against the successors the design declares. What the ledger no longer derives is retired (`RETIRE`): construction accounts its references and never deletes it, and the build deletes it and writes the retirement record, as delivery would. The suites dispatch a workflow by the name they were written against; the build follows the successors this design, its lineage and the retirement ledger declare |
| `test_indexes.py` | Assembler index construction, including that a republished identity resolves to its authoring copy and that resolution does not track domain-name order |
| `test_transform_conformance_evidence.py` | Every build's conformance result, the platform's included, is carried, names each transform the build supplies with none refused, names as carried exactly what its attestation records, and is a manifest constituent; the platform proves every transform it has a vector for; `conformance/` holds only `composition.json` |
| `test_transform_conformance.py`, `test_vector_build.py` | The compiler refuses a malformed vector before conformance runs, and a wrong expectation fails the build at conformance |
| `test_reference_semantics.py` | Every place that finds a reference reads it from `artifact::VOCAB_DECLARATION_REPRESENTATION_V0`, and a full name in an undeclared part is refused (E105) |
| `test_routing_closure.py`, `test_routing_lookup.py` | A workflow routes every outcome its contracts can end with, and a step answers every outcome its capability declares; routing is a lookup of `continue` or `exit`, a contract declares no `evaluation` block, and a stood-down contract is checked by neither |
| `test_platform_vectors.py` | The platform materializes its vectors and writes their cases; each defect in a platform vector stops the platform build on its own rule; a build records what it carried in, and the platform carries nothing |
| `test_transform_conformance_runner.py` | `OK` — a molecule is proven from recorded results without running its non-deterministic step; a missing or unused record refuses; what a build supplies is read from its attestation, never a name; a failed case for a carried transform refuses the build |
| `test_compiler_atoms.py` | `PASSED` — the compiler's atoms |
| `test_molecule_composition.py` | Molecules compose, each transform is placed under the constitution its kind and purity name, and an atom run directly is sealed with its purity |
| `test_keyed_chain_and_molecule_surface.py`, `test_dispatch_routing_fidelity.py` | Two places running one contract are not a cycle; the sealed dispatch realizes every declared transition at its own node, and S8 refuses one that does not |
| `test_force_and_output_root.py` | A superseded workflow, intent or invariant that still confers effect fails S8 (`INVARIANT_SUPERSEDED_NOT_IN_FORCE_V0`); a build writes to the root its configuration declares, and two in-force configurations of one repository naming one root are refused |
| `test_governance_provenance.py` | Every case `PASS`, and `provenance restored: yes` on the last line — the script mutates governance to make its point and must put it back. `DETERMINISM` same governance → identical closure hash; `ISOLATION` a platform-only change leaves it unchanged; `SENSITIVITY` an imported change moves it; `ENFORCEMENT` a stale domain against changed governance is blocked at assembly. If any of the four goes red, read `provenance restored` before rerunning — a run that died mid-mutation leaves governance edited |
| `test_reference_collatz.py` | `OK` — the Collatz workload runs as declared, and a run whose check reports a sequence that did not end at 1 ends violated, stores nothing and announces the numbers |
| `test_warm_boot.py` | The identity covers the claimed profile's content: a profile changed after sealing, and a manifest carrying no `profile_sha256`, are refused at boot. `boot()` delegates acceptance to `assembler.core.verify_snapshot`, which recomputes every constituent from its bytes and evaluates all four clauses of `3b` §7; `boot` raises `RuntimeError` on any of them. Recomputing over the manifest's *recorded* hashes would catch a tampered manifest but not a tampered constituent. `test_manifest_states_one_identity` asserts the manifest's two statements of its own identity agree. **These tests skip when no assembled snapshot is present** — a bare workspace reports them skipped, not passed |
| `test_federation.py`, `test_capability_concurrency.py`, `test_molecule_execution.py` | `OK` — federated roles; capabilities under concurrent writers; molecules run, recorded and replayed |
| `test_node_keyed_routing.py`, `test_trace_path.py` | `OK` — routing, endings and announcements by node, and the trace naming each place; the path drawn over a workflow's graph is the one the trace records |
| `test_examine.py` | `OK` — `runtime examine` reads `SCHEMA_TRACE_EVENT_V0`, refuses any other format (a v5 trace, written to V1, included), tells a completed run (refusals included) from a structural failure, and reads every trace under `data/` |
| `test_step_outcome.py` | A step outcome its contract declares no continuation for refuses, writes an ERROR and runs nothing after it (`3a` EX-18); every step record carries its outcome and the continuation it selected, an admission's being `route` (`3e` EV-19). A fault refuses the run with an ERROR and is never routed: a transform that will not load, an atom that breaks, a side effect that raises or states no outcome (`3a` §4.1, `3c` §7). An atom's own refusal still routes as VIOLATION. Runs the Collatz workload, so no business domain's delivery reaches it. Needs an assembled snapshot |
| `test_no_default.py`, `test_unknown_continuation.py` | No resolver supplies a default (`3c` RT-6): a transform path that reaches nothing refuses, a result maps only on SUCCESS and must carry each field it maps, an absent source is left out and never set to null; execution refuses a routing answer other than `continue` or `exit` |
| `pgc_env_check.py` | `PGC ENVIRONMENT CHECK PASSED` — no legacy dependency reachable |
| `test_regression_verdict.py` | The verdict fails a run for every way it can differ from this table, including an unexpected pass and a suite that skipped everything |
| collatz | `SUCCESS`, `all_terminate: true` |
| govern agent action | `SUCCESS` |
| provision licensing | `SUCCESS` — the block clears `data/` first, so this is always a first run |
| `execution_validation.py` (catalog) | Every criterion holds — the catalog's nine workflows against its registration criteria |
| `execution_validation_works.py` (catalog) | Every criterion holds — the works criteria, including a record written before works existed |
| `execution_validation.py` (identity) | Every criterion holds — those not exercised are a timed test and the transaction half of the wallet claim, which no function realizes |
| `execution_validation.py` (wallet) | Every criterion holds — the one not exercised is a write through a consulted binding, which no act is authored to attempt |
| `execution_validation.py` (model_response) | Every criterion holds — CLM CR-1: a model answers only in service, only on what it may read, only in words the rules permit; refusals recorded and announced; a replay agrees on every determinative event |
| `blockchain/testbed/routing_closure/execution_validation.py` | Every criterion holds — a failed record ends every identity and wallet act at `EXIT_REJECTED`, at the step that failed |
| `ai_governance/testbed/routing_closure/execution_validation.py` | 4/4 — a reclaim the registry refuses ends at `EXIT_REJECTED` with the license still assigned and active and no revocation announced; nothing after `CC_RELEASE_LICENSE_IDENTITY_V0` runs |
| `ai_governance/testbed/owner_decisions/execution_validation_owner_decisions.py` | 21/21 — the business holds its own facts (cr_04): licensing's acts, the cap, training, usage, reclaim after 30 days, and agent governance reading licensing's license |
| `transformation_compilers/testbed/routing_closure/execution_validation.py` | Every criterion holds — a phase whose observation reports NOT_FOUND ends at `EXIT_REJECTED` and judges nothing; every way the observing capability answers is answered by every observing step and routed by every phase, read from the contract each node runs (`code`); an outcome the capability gains is answered at the next emission |
| `transport_cli_check.sh` | `TRANSPORT CLI PASSED — 8/8 cases` — `pgc_transport call`, run from the repository root as `run_http.sh` provisions it: 27 admitted with exit 0 and a named trace, -5 and text refused with exit 1, an unknown operation exit 5, an `si.` operation through the same command, and exit 2 for an invocation that never reaches the boundary |
| `demo_script_check.sh` | `DEMO SCRIPT PASSED — 12/12 cases` — `pgc_install/demo/pgc-demo.sh` in workspace mode through every terminal step `README_DEMO.md` walks: play, refusals, `set-limit` admitting 1,000,000, a second build of one limit reproducing its identity, `tamper` refused at acceptance, `reset`, `inspect show` and `inspect code`. It takes about ten seconds; the web pages are not served |
| `trace_schema_conformance.py` | `TRACE SCHEMA CONFORMANCE PASSED` — every line of every trace the execution block wrote conforms to `SCHEMA_TRACE_EVENT_V0` |

### Choosing a store operation

`CS_MUTABLE_JSON_V0` publishes three ways to change a record, and the wrong one destroys data
silently:

| | replace whole value | merge named fields |
|---|---|---|
| **by key** | `WRITE` | `UPDATE` |
| **by filter** | — | `UPDATE_WHERE` |

**Write what does not exist; update what does.** A step creating a record uses `WRITE`; a step
changing a record it did not create uses `UPDATE`, which sets the fields it is given and leaves the
rest alone. `WRITE` on an existing record destroys every field the caller did not supply, and it
succeeds — there is no error to notice.

`UPDATE` reports `VIOLATION` where the key is not held, so a step that changes a record can never
create one. `UPDATE_WHERE` addresses a *set*; reach for it only when you mean every record matching
a filter, never as a stand-in for a keyed update — that substitution is correct only while some
domain invariant guarantees the filter matches exactly one record, and it carries that invariant
wherever it is copied.

### A property no step consults

Identity accepts and rejects an actor in two workflows, `WF_ACCEPT_ACTOR_V0` and
`WF_REJECT_ACTOR_V0`, and the reject path validates grounds unconditionally. One workflow carrying
both decisions could not check grounds: its steps are unconditional, so the check would refuse
acceptances that correctly omit them. Two workflows match the business's own distinction, two events
rather than one carrying an outcome field.

A rule declared at P5 (*A rejection states grounds*) and recorded at P7
(`EV_ACTOR_REJECTED_V0 | grounds_required | YES`) can still be realised nowhere, and every document
passes. A property is a true statement about an artifact no step consults: no phase rule sees it,
and only an execution validation catches it.

Both transformation verdicts complete with `Status: SUCCESS`. An inadmissible document is a correct
judgement, not a failed execution — `VIOLATION` there would mean the phase itself is broken.

`differential.py` must be run from the `transformation` directory: it imports `design_baseline` from
`e2e_phases_test`, which sits beside it. `--check` on the emitter is the cheap half of what the
differential proves — it compares counts without booting a snapshot, so it catches a rule added and
never re-emitted in a second rather than a minute.

## The catalog subdomain

`book_library_mgmt/catalog` is constructed and runs. Its nine workflows are exercised by one script,
which is the **only check in this runbook that proves the catalog does anything**:

```bash
python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py 
```

It dispatches real workflows through `protocol_runtime` against a fresh temp data root and asserts the
CR's §15 acceptance criteria — 23 of them — reading the stores it wrote rather than the status it was
handed. State accumulates deliberately across scenarios, so the order is part of the evidence and the
run is not idempotent; that is why it starts from an empty data root every time.

It takes an optional snapshot path, defaulting to `~/protocol-governed-computing/snapshot`.

**To inspect the catalog it built**, give it somewhere to keep the stores:

```bash
python ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py --data-root ~/protocol-governed-computing/data/catalog_inspect
```

```
  23/23 criteria hold

  stores kept at .../data/catalog_inspect/book_library_mgmt/catalog
    book_identity_registry.jsonl 2 entries (json lines)
    books.json                   2 record(s)
    catalog_operations.jsonl     15 entries (json lines)
    copy_barcode_registry.jsonl  4 entries (json lines)
    physical_copies.json         4 record(s)
```

The path must be empty or absent — the run accumulates state across scenarios, so starting it over a
previous run's stores proves nothing. It refuses rather than emptying a directory you named.

**Two file formats, and the extension tells you which.** `CS_MUTABLE_JSON_V0` writes one JSON
object keyed by store key (`.json`); `CS_REGISTRY_V0` and `CS_APPENDONLY_JSONL_V0` write JSON Lines
(`.jsonl`). Use `jq` on the former, `jq -s` on the latter.

`CS_REGISTRY_V0` §12 declares its path a **JSONL registry file (append-only)**, and its runtime
writes one — the catalog had named those two stores `.json`, so the extension advertised a document
that could never be parsed as one. P7's `STORE_PATH_FORMAT_MISMATCH` now refuses it: a store's path
must carry the extension its storage capability writes. The correspondence is declared in
`STORE_FORMATS` in the phase's rules, because a CS states its format only in the prose of its
configuration schema and nothing machine-readable carries it.

**Why it exists, and why the other checks do not replace it.** Every document check can pass —
P0–P8 ADMISSIBLE, `tc construction check` 100%, construction acceptance with no field difference,
conformance PASSED, `e2e_phases_test.py` green — against a composition whose stores hold binding
expressions instead of records: a cross-step source authored without its `results.` root is read by
the runtime as a literal string. Document checks prove a design determines its artifacts. Only
execution proves the artifacts do anything.

Individual workflows can be dispatched directly. The payloads live in the testbed and are **derived**
from the validation suite's own helpers — regenerate rather than hand-edit them:

```bash
cd ~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog
python emit_payloads.py          # -> test_payloads/01..09

P=~/protocol-governed-computing/business_domains/book_library_mgmt/testbed/catalog/test_payloads

~/protocol-governed-computing/protocol_runtime/run.sh run \
  --wf book_library_mgmt::WF_REGISTER_BOOK_V0 \
  --payload $P/01_register_book.json \
  --data-root ~/protocol-governed-computing/data/book_library_mgmt
```

They are a **sequence against one data root**, not nine independent cases — `01` registers the book
the rest operate on, and the numbering is the order to run them in. All nine return `SUCCESS` in
order from an empty data root. Run out of order a payload is still well-formed and its workflow
refuses it, which is the catalog behaving correctly rather than a broken payload.

| Payload | Workflow |
|---|---|
| `01_register_book` | `WF_REGISTER_BOOK_V0` |
| `02_register_physical_copy` | `WF_REGISTER_PHYSICAL_COPY_V0` |
| `03_update_bibliographic_information` | `WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0` |
| `04_search_catalog` | `WF_SEARCH_CATALOG_V0` |
| `05_retrieve_book_details` | `WF_RETRIEVE_BOOK_DETAILS_V0` |
| `06_retire_physical_copy` | `WF_RETIRE_PHYSICAL_COPY_V0` |
| `07_reinstate_physical_copy` | `WF_REINSTATE_PHYSICAL_COPY_V0` |
| `08_retire_book_record` | `WF_RETIRE_BOOK_RECORD_V0` |
| `09_reinstate_book_record` | `WF_REINSTATE_BOOK_RECORD_V0` |

The five stores land under `<data-root>/book_library_mgmt/catalog/`: `books.json`,
`physical_copies.json`, `catalog_operations.jsonl`, `book_identity_registry.jsonl`,
`copy_barcode_registry.jsonl`. Inspect those to see what a workflow actually did — the status alone
does not tell you.

The nine are `WF_REGISTER_BOOK_V0` · `WF_REGISTER_PHYSICAL_COPY_V0` ·
`WF_UPDATE_BIBLIOGRAPHIC_INFORMATION_V0` · `WF_RETIRE_BOOK_RECORD_V0` · `WF_RETIRE_PHYSICAL_COPY_V0` ·
`WF_REINSTATE_BOOK_RECORD_V0` · `WF_REINSTATE_PHYSICAL_COPY_V0` · `WF_SEARCH_CATALOG_V0` ·
`WF_RETRIEVE_BOOK_DETAILS_V0`. Every one takes `staff_credentials`, `authorization_rules` and
`staff_id`: authorization is read, never granted, so the caller supplies both the credentials and the
rules they are checked against. `execution_validation.py`'s `book_payload()` is the worked example.

### A change request that amends rather than authors

A defect correction creates nothing: it re-renders an artifact the composition already holds. The
registers that name what a change *creates* are therefore empty — `provisional_codes` at P5,
`new_artifacts` at P7, `build_order` and `critical_path` at P8 — and all four are optional so that
an amend-only change is expressible. Emptiness there is not an omission; it is the shape.

What carries the change instead:

- **P7 `existing_inventory`** — the artifact with Action `EXTEND`. This is what construction reads:
  `render_all` renders what the mandate schedules **and what the design amends**, because an
  extended artifact is never a build step (`BUILD_CODE_ALREADY_EXISTS` refuses to schedule an
  identity the composition already holds).
- **P7 `cc_composition` / `step_bindings`** — the artifact's full composition, not the delta. An
  amended artifact is rendered *whole*, so every step it keeps must be restated exactly. Anything
  the design does not state is dropped.
- **The `Summary` cell of the inventory row** becomes the emitted artifact's summary. Write what the
  artifact *is*, carried over unchanged — a summary describing the change silently rewrites it.

```bash
tc construction check --snapshot ~/protocol-governed-computing/snapshot $D
#   AMENDMENT NARROWS lists facts that exist now and the design does not state. For an amendment
#   some narrowing is the point — a replaced input is a lost fact — so read the list rather than the
#   count. It cannot tell a renamed step from a deleted one: renaming one step reported 13 facts
#   lost where 1 had changed. Prefer the smallest diff.
```

Verify by diffing the emitted artifact, not by trusting the measurement. CR-3's correction is two
lines; anything larger meant the design restated something imperfectly.

### After editing a governance artifact, recompile every domain

A platform artifact is copied into **every** domain's compiled output — the governance surface is
compiled per domain and the assembler collects them all. `compile.sh` alone updates only `platform`,
and the artifact index may resolve the identity to any copy.

**The copies can disagree and nothing checks.** After adding an operation to `CS_MUTABLE_JSON_V0`,
five copies existed with two different operation sets; the assembler reported
`conformance PASSED (5 rules over 376 artifacts)` and `round-trip verify: OK`. The published
capability surface kept reporting the old set while the edited artifact sat correctly compiled under
`platform`.

Run the full Build list at the top of this file after any governance edit. A single domain compile is
never enough — but the assembler now checks: `verify_snapshot` compares every copy of an artifact
identity by `content_hash` and refuses the composition when they disagree, naming the identity and
the copies. A partial recompile fails the build instead of sealing a snapshot that answers from
whichever copy the index happened to resolve.

## Designs of record

Every designed root carries its design of record in `<root>/design/`: one P7 and one P8, generated
from the registry. After any change to a registry, regenerate them and check them:

```bash
cd ~/protocol-governed-computing/transformation_compilers
python scripts/write_baseline_designs.py            # write every root's design/
python scripts/write_baseline_designs.py --check    # exit 1 if a design is not the one its registry generates
python scripts/testbed/construction_acceptance.py   # render each design and compare it with its registry
```

A difference acceptance reports is a generator bug when the design states the fact, and a design
insufficiency when it does not. A design of record is read by construction. It is not a phase
document a rule set judges, because it has no P0 to P6 to cite.

## Constructing a change into artifacts

A change after the baseline is a dossier, `<domain>/cr_dossiers/cr_NN_<subject>/`, designed against
the composition. The loop to run after **any** edit to its P7 or P8:

```bash
W=~/protocol-governed-computing
D=$W/business_domains/<domain>/cr_dossiers/cr_NN_<subject>

tc construction check $D --snapshot $W/snapshot
#   100% or the design does not determine its artifacts, AND no amendment narrows what it replaces.
#   `--snapshot` is what checks the second: an artifact inventoried EXTEND is rendered whole and
#   replaces its predecessor, so a design stating only the delta deletes the rest — at 100%
#   completeness, because completeness never looks at what already exists. Without the flag that
#   check does not run and says so.

tc construction emit $D --root $W/business_domains/<domain> --snapshot $W/snapshot

# A new CT is a protocol artifact AND a Python implementation. Construction renders the first; the
# second is hand-authored at
# business_domains/<domain>/implementation/capability_transforms/atoms/<code_lower>.py
# with a callable `execute(inputs, context)` raising CTExecutionError. A CT whose module is missing
# returns nothing, its contract yields VIOLATION, and every check above this line still passes.

$W/protocol_compiler/compile_domain.sh $W/business_domains/<domain>
PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 $W/snapshot_assembler/assemble.sh

(cd $W/transformation_compilers && python scripts/write_baseline_designs.py)   # the design of record follows the registry
```

The governed construction workflow, `transformation::WF_CONSTRUCT_ARTIFACTS_V0`, writes into
`data/transformation/construction/registry/` through `CS_TEXT_ARTIFACT_V0 WRITE_ALL`. **Promotion into
the domain is a separate act**, and no CLI performs it: one would duplicate a governed path with an
ungoverned one.

Each change carries its own execution validation in the domain's `testbed/`, one criterion per
acceptance criterion, and every earlier one is run with it: a later change's suite proves it did
something, and the earlier suites prove it broke nothing.

### A change the derive route designs

A change whose decision is a ledger is delivered by one script, which runs every step above:

```bash
D=$W/business_domains/<domain>/cr_dossiers/cr_NN_<subject>   # holds ledger.yaml and criteria.yaml
bash $W/transformation_compilers/scripts/derive_deliver.sh <domain> $D
```

`criteria.yaml` names the suites, under the domain, that hold the change's acceptance criteria:
`suites: [testbed/<part>/execution_validation_<subject>.py]`. Write them first, from P0.

It pins `baseline.json`. It runs the criteria against that composition and stops unless one fails
(`criteria_before.txt`). It writes P0 to P8, stops unless P0 to P6 are admissible and construction is
complete, emits, deletes what the design superseded or retired with a record in
`retired_identities.yaml`, repoints the testbed and client and every caller outside the domain,
compiles, assembles and regenerates the
design of record. Last, it requires every criterion to hold (`criteria_after.txt`). Write
`delivery.md` beside it, then run the regression. See DESIGN_LANGUAGE §9.7.

### A change to the derive route

A change to a module of `transformation/design/derive/`, or to its doctrine, ledger schema or
catalog, runs as its own dossier. Until a seal records it, every derivation is refused:

```bash
mkdir $W/transformation_compilers/dossiers/<subject>            # write change.md: what and why
tc phase derive revise <document> --change "…"                  # only if a sealed document changed
tc phase derive seal $W/transformation_compilers/dossiers/<subject> --snapshot $W/snapshot --change "…"
```

The seal re-derives every ledger and records each outcome. A design of record that changes is
delivered as a change request. See DESIGN_LANGUAGE §9.5.

## Serving a domain over HTTP

A domain that declares `TI_`/`TE_` artifacts is reachable from outside. The transport adapter is
domain-neutral and is **pointed** at everything; a client is a launcher, a binding table and static
files, and it lives with the domain it serves.

```bash
# blockchain/identity — three operations, one route
~/protocol-governed-computing/business_domains/blockchain/client/serve.sh
#   -> http://127.0.0.1:8000        PGC_HTTP_PORT overrides

# collatz — one operation, one route per operation
~/protocol-governed-computing/conformance_workloads/workloads/collatz/client/serve.sh

# snapshot inspection — twenty-one operations sharing one route
~/protocol-governed-computing/snapshot_inspector/client/serve.sh
#   -> http://127.0.0.1:8001/kinds/     the kind map: every kind, and how kinds refer to kinds
#   -> http://127.0.0.1:8001/kinds/?domain=blockchain   the same, for one composed domain
#   -> http://127.0.0.1:8001/workflow/  one workflow drawn from its compiled graph
#   -> http://127.0.0.1:8001/workflow/?trace=<ref>  a run's path marked on its workflow
#      (serve with PGC_DATA_ROOT set to the data root the run wrote under)
```

The kind map is also a file you can open without a server, for any snapshot that declares
`si.kind.map`. A snapshot sealed before the operation existed, such as v6, refuses with one line:

```bash
cd ~/protocol-governed-computing/snapshot_inspector
PYTHONPATH=. python scripts/export_kind_map.py --snapshot ../snapshot --out ~/kind_map.html
si --snapshot ../snapshot kind map                       # the same answer as JSON
si --snapshot ../snapshot kind map --domain blockchain   # one composed domain
si --snapshot ../snapshot compile trace --artifact blockchain::WF_REGISTER_ACTOR_V0   # how a build produced it
```

The page's Domain selector narrows the map to one composed domain: the artifacts addressed in it,
including the platform capabilities it reaches, and the links between them. The whole snapshot is
the default. The exported file embeds every domain's answer, so the selector works offline too.

A number on a kind-map arrow counts distinct artifact pairs, not edges. One workflow names a
contract as a node, a routing target and a full name, and that is one link.

Read the startup banner before believing anything. It prints the `snapshot_id` the process booted
against and the operations that snapshot declares — **the boundary is read once, at startup**, so a
snapshot rebuilt afterwards is invisible until the process restarts. A stale server is then a
one-line comparison rather than an inference.

### The data root is an instance, not an interface

`PGC_DATA_ROOT` names *which business instance* is being driven. Nothing in the runtime or the
transport engine ties it to a user interface, and the layout is identical whatever drove it —
the domain is namespaced inside the root, not by it:

```
<data_root>/blockchain/identity/{actors.json,contact_address_registry.jsonl,actor_occurrences.jsonl}
<data_root>/traces/blockchain/<WF>/<trace_id>/<trace_id>.jsonl
```

**Point the client and the CLI at the same root.** `blockchain/client/serve.sh` defaults to
`data/blockchain`, which is what the CLI runner at the foot of this file uses, so a person registered
from a web form is the person a CLI decision is about. A root per client is two disjoint worlds that
happen to share a snapshot — you cannot then verify what you registered, and the composition's claim
that a boundary reaches the same acts the CLI does goes untested.

```bash
# register over HTTP, then decide from the CLI against the same instance
curl -s -X POST http://127.0.0.1:8000/blockchain -H 'Content-Type: application/json' \
  -d '{"operation":"blockchain.register_actor","params":{"name":"Ada","contact_address":"ada@example.test"}}'
cat ~/protocol-governed-computing/data/blockchain/blockchain/identity/actors.json
```

**Concurrency, stated so it is not discovered.** A mutable store is written atomically per file
(temp → `fsync` → `os.replace`), so a torn or half-written store is impossible, and every operation
takes a per-file lock around load → modify → save. **That lock is a `threading.Lock` in a
process-local registry** (`CS_MUTABLE_JSON_V0/impl/executor.py:20-28`), so it serializes concurrent
requests *inside one server* and does nothing at all *between processes*. A CLI run and a running
web server writing one store in the same instant can therefore still lose an update — which is
precisely the pairing a shared data root invites. Drive one at a time, or accept the race
knowingly.

### The two binding shapes

`bindings/http.json` is adapter-owned data, not an artifact. Either form is governed — an operation
resolves only if the snapshot holds a matching TI/TE pair.

```jsonc
{ "method": "POST", "path": "/collatz", "operation": "collatz.compute" }              // one act, one place
{ "method": "POST", "path": "/blockchain", "operation_in_body": true,                 // a family, one place
  "namespace": "blockchain." }
```

The namespace on the second is an **admission constraint the adapter checks textually**, never a
dispatcher it branches on. Each identity still resolves against its own TI/TE pair. Use it when a
domain expects to add acts: a new function then adds a name, not a place, and no caller learns a new
address. `si.catalog` submitted to `/blockchain` is refused `OPERATION_NOT_ADMITTED`.

### Exercising it

```bash
B=http://127.0.0.1:8000
curl -s -X POST $B/blockchain -H 'Content-Type: application/json' \
  -d '{"operation":"blockchain.register_actor","params":{"name":"Ada","contact_address":"ada@example.test"}}'
```

Expected, for blockchain/identity against a fresh `PGC_DATA_ROOT`:

| call | HTTP | Result Class |
|---|---|---|
| `register_actor` | 200 | `SUCCESS` — `sequence_number: 1`, evidence `trace:…` |
| the same registration again | 200 | `SUCCESS` — `sequence_number: 2`, one actor, no failure |
| `register_actor` with no `contact_address` | 400 | `VIOLATION` — `INPUT_MISSING`, names the field |
| `accept_actor` | 200 | `SUCCESS` — `ACTOR_ACCEPTED`, `grounds: null` |
| `accept_actor` again | 400 | `VIOLATION` — the act ran and refused |
| `reject_actor` with no `grounds` | 400 | `VIOLATION` — `INPUT_MISSING`, names `grounds` |
| `reject_actor` on an unregistered address | 404 | `NOT_FOUND` |
| an act the domain does not offer | 404 | `OPERATION_NOT_FOUND` |
| an identity outside the route's namespace | 400 | `OPERATION_NOT_ADMITTED` |

**Rows 3 and 5 are both `VIOLATION` and mean different things** — the boundary could not read the
request, versus the act ran and refused. The governed Result Class set has no kind for the second,
so they are told apart by `errors[]`: `INPUT_MISSING` naming a field, against `handler status
VIOLATION`. A client that switches on Result Class alone will conflate them.

The `evidence` reference resolves under the `/traces` mount, so the record of what happened is one
request away from the answer reporting it. `/snapshot` mounts the sealed composition read-only.

### Serving the compiled workflow beside the form

Because `/snapshot` is mounted, a screen can draw the graph the runtime actually traverses, live
from the sealed composition. It mounts the inspector's workflow diagram as `/diagram` and draws the
workflow's compiled `graph.json` with it:

```html
<svg class="workflow" data-graph="/snapshot/behavior_logic/<domain>/<WF_CODE>/<WF_CODE>.graph.json"
     data-entrance="<TI_CODE>"></svg>
<script src="/diagram/workflow_diagram.js"></script>
```

The screen's script fetches each `data-graph` and calls `WorkflowDiagram.draw(svg, graph, {entrance})`.
Live means never stale: rebuild the snapshot and the drawing changes with it. Both identity screens
draw their workflows this way, and so does collatz, which also marks the routes a run took. The
snapshot carries no picture of a workflow. A rendered image would make the sealed snapshot depend on
the renderer of the machine that built it.

### What a client may not do

The page collects, sends, and renders. It holds no rule, validates nothing, and keeps no copy of
what the business holds. Concretely, in `blockchain/client/web/`: **no `required` attribute and no
`type="email"`** — those are client-side judgement, and the platform's refusal naming the field is
what the caller should see instead. A control may carry an *operation identity* (accept and reject
are two acts, so each is an `<option>` value); it may not carry a mapping, a schema, or a default.
The one thing a page may keep is what the person just typed, to save retyping it — nothing the
business does may depend on it being there.

A client that POSTs a workflow identity violates `OPERATION_IDENTITY_INDEPENDENCE`: it names an
operation identity and reads the Canonical Transport Response, nothing else.

## Adding a new domain

There are two paths, and the difference is not the build — it is whether the artifacts already
exist. Once a domain has a `registry/`, adding it to the composition is the ordinary loop at the
top of this file: `compile_domain.sh`, then `assemble.sh`. Nothing below changes that.

### The simple path — artifacts you already have

Correct whenever the artifacts are authored rather than derived:

```bash
W=~/protocol-governed-computing
# 1. Hand-author registry/<subdomain>/{actors,intents,workflows,capability_contracts,...}
# 2. Hand-author registry/structures/STRUCTURE_BUILD_<DOMAIN>_CONFIG_V0.md — without it the
#    compiler cannot discover the domain at all.
$W/protocol_compiler/compile_domain.sh $W/business_domains/<domain>
PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 $W/snapshot_assembler/assemble.sh
```

Then give the domain its design of record: add its root to `ROOTS` in
`transformation_compilers/scripts/write_baseline_designs.py` and to `DOMAINS` in
`construction_acceptance.py`, and write it. Acceptance then reports every fact of the hand-authored
registry the design language cannot state.

**What it costs.** A design of record is read by construction, not judged by a phase's rules, so
none of the composition-integrity rules judges a hand-authored domain — not
`STEP_INTERFACE_CONFORMS`, not `STEP_INPUT_UNBOUND`, none of them. A literal no binding resolves sits
in every record it writes, and nothing looks. Only a change request's P7 is judged in full.

**The build manifest is hand-authored, and no rule governs it.** Copied from a sibling, it keeps the
sibling's domain name and subdomains until someone corrects them.

### The governed path — a domain the pipeline produces

Everything below is about *producing* the artifacts. A domain established by a change request has
no baseline to extend and no registry to write into, and the order matters: a deviation fails at a
step that looks unrelated. Steps 1 and 5 exist only because a dossier is involved — they say nothing
about the build.

```bash
W=~/protocol-governed-computing
DOM=<domain>                                     # the namespace; artifacts are <DOM>::
SUB=<subdomain>
CR=$W/business_domains/$DOM/cr_dossiers/cr_01_$SUB

# 1. Pin the baseline the CR is validated against — the composition BEFORE this domain exists.
mkdir -p $CR && tc baseline show --snapshot $W/snapshot > $CR/baseline.json

# 2. Author P0 (problem statement + seed), project P1, author P2..P8.
tc phase project --phase p1 --out $CR/p1_change_request_${DOM}_${SUB}_v0.md $CR/p0_seed_${DOM}_${SUB}_v0.md
tc phase check --phase p7 --snapshot $W/snapshot \
   --prior p5=$CR/p5_*.md --prior p6=$CR/p6_*.md $CR/p7_*.md

# 3. Emit. Writes the artifacts the mandate schedules — and NOT the build manifest. Every field of
#    a manifest is compiler configuration no register states, and a manifest appearing where a glob
#    finds it confers no authority to introduce a domain (`2e` §6). Adding a domain is a governed
#    transformation against an existing baseline (`6c` §10); a domain MUST NOT claim genesis (DP-11).
#    So --root must already carry a STRUCTURE_BUILD_*_CONFIG, hand-authored as in the simple path
#    above. `construction emit` refuses otherwise rather than founding one by inference.
tc construction emit $CR --root $W/business_domains/$DOM

# 4. Compile the domain against the compiled platform surface, then assemble.
$W/protocol_compiler/compile_domain.sh $W/business_domains/$DOM
PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 $W/snapshot_assembler/assemble.sh

# 5. Re-pin and re-approve — the composition now contains the domain, so the old pin is stale.
tc baseline show --snapshot $W/snapshot > $CR/baseline.json
for p in p2 p3 p4 p5 p6 p7 p8; do tc baseline approve --phase $p --by "$USER" $CR/baseline.json; done

# 6. Give the domain its design of record, as in the simple path: add its root to ROOTS and DOMAINS.
(cd $W/transformation_compilers && python scripts/write_baseline_designs.py)
```

**Re-validating the CR after step 4 will fail**, with `NEW_CODE_ALREADY_EXISTS` on every artifact.
That is correct: a change request that says *create these* cannot be judged against a composition
that already holds them. To re-check or amend it, roll the composition back first:

```bash
rm -rf $W/business_domains/$DOM/{registry,snapshot} && PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 $W/snapshot_assembler/assemble.sh
```

Editing an artifact already sealed into a released composition is a `REPLACE` in a governed change
request, not an edit. Rolling back is legitimate only while the domain is unreleased.

**The assembler refuses a domain that declares source with no compiled output**, so compile the
domain before assembling: a manifest with no compiled artifacts is a domain the assembler cannot
account for.

### What a new domain needs beyond its artifacts

- **A capability the substrate does not offer** is a platform change, not a domain one. Declare the
  CS in `software_governance/capability_side_effects/registry/`, implement it under
  `implementation/<CODE>/runtime.py` with `execute(*, op, payload)`, and add it to
  `allowed_capability_side_effects` in `INVARIANT_CS_SURFACE_CLOSED_V0` — the platform surface is
  closed and the compiler refuses an undeclared capability. `core.category` must be one of
  `storage · external · ephemeral · execution_gateway · inspection`.
- **A capability the workflow reaches must be bound for it** in the domain's `RB_`. A capability
  composed into a contract and bound for nobody produces no handler, no trace entry and no error —
  the step is simply never reached.
- **A new CT is two things**: the artifact construction renders, and a Python implementation at
  `business_domains/<domain>/implementation/capability_transforms/atoms/<code_lower>.py`. Either half
  can go missing without anything failing until the step runs, which is what
  `.github/process/implementation_closure.py` exists to catch — run it after adding or retiring a transform.

## Running a domain's workflows from the CLI

`run.sh` boots the snapshot but needs `PGC_IMPL_ROOTS` for domain implementations. Driving the
runtime directly is what the testbeds do:

```bash
python - <<'EOF'
import json, sys, pathlib
W = "/Users/bp/protocol-governed-computing"
sys.path[:0] = [f"{W}/software_governance", f"{W}/business_domains"]
from runtime import api
P = pathlib.Path(f"{W}/business_domains/blockchain/testbed/identity/test_payloads")
WF = {"04": "blockchain::WF_ACCEPT_ACTOR_V0", "08": "blockchain::WF_REJECT_ACTOR_V0"}
for f in sorted(P.glob("*.json")):
    r = api.run_workflow(wf_fqdn=WF.get(f.name[:2], "blockchain::WF_REGISTER_ACTOR_V0"),
                         payload=json.loads(f.read_text()),
                         snapshot_root=f"{W}/snapshot", data_root=f"{W}/data/blockchain")
    print(f"{f.name:<36} {r.status}")
EOF
```

Stores land under `data/<domain>/<domain>/<subdomain>/`, traces under
`data/<domain>/traces/<domain>/<WF>/<trace_id>/*.jsonl`.

**Read the trace before theorising.** A `CC_START` event carries the contract's *resolved* inputs,
which is the only place a binding that resolved to `None` is visible — the artifact, the workflow
and the contract all look correct. `CC_STEP` names each capability as it runs; a step missing from
the trace entirely was never bound.

## Clean rebuild from source

The strongest check there is. Every other suite judges the composition; this judges whether the
composition can be *rebuilt* — and a `snapshot_id` that comes back unchanged proves the whole thing
derives from committed source with nothing on disk carrying state nobody can regenerate.

Safe only when every repo is clean. Every registry and every design of record is **tracked**, so the
wipe below removes nothing that is not derivable.

```bash
W=~/protocol-governed-computing

# 0. Refuse to start if anything is uncommitted. What is not in git is about to be lost.
for r in transformation_compilers business_domains standards software_governance snapshot_inspector \
         protocol_runtime protocol_compiler snapshot_assembler conformance_workloads; do
  printf "%-24s %s\n" $r "$(git -C $W/$r status --short | wc -l | tr -d ' ')"
done

# 1. Wipe every build output: the assembled snapshot, each domain's compiled projections, runtime data.
rm -rf $W/snapshot $W/data \
       $W/software_governance/snapshot $W/snapshot_inspector/snapshot $W/transformation_compilers/snapshot \
       $W/business_domains/*/snapshot $W/conformance_workloads/workloads/*/snapshot

# 2. Platform first — a domain resolves its references against the compiled governance surface.
$W/protocol_compiler/compile.sh STRUCTURE_BUILD_PLATFORM_CONFIG_V0

# 3. Every domain in the composition. Omitting one assembles it from stale output that no longer exists.
for d in $W/transformation_compilers $W/snapshot_inspector $W/conformance_workloads/workloads/collatz \
         $W/business_domains/ai_governance $W/business_domains/book_library_mgmt \
         $W/business_domains/blockchain $W/business_domains/causal_language_model; do
  $W/protocol_compiler/compile_domain.sh $d
done

PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 $W/snapshot_assembler/assemble.sh
```

**The snapshot_id must be the one you started with.** It is content-derived over each domain's
projection hashes with provenance, timestamps and paths excluded, so a rebuild of unchanged sources
reproduces it exactly. A different id means either a source changed or something in the build is
not deterministic — and the second is the one worth chasing.

Then the full surface:

```bash
cd $W/transformation_compilers
for s in meta_test e2e_phases_test differential projection_test construction_acceptance; do
  python scripts/testbed/$s.py
done
python scripts/emit_rule_sets.py --check          # sealed rule sets match their declaration
python scripts/write_baseline_designs.py --check  # every design of record is the one its registry generates
tc phase meta                                     # rule/mechanism parity
```

and execute two domains against the snapshot just built, which is the only evidence that a
composition assembled from nothing still runs:

```bash
python - <<'EOF'
import json, sys, pathlib
W = "/Users/bp/protocol-governed-computing"
sys.path[:0] = [f"{W}/software_governance", f"{W}/business_domains", f"{W}/conformance_workloads"]
from runtime import api
P = pathlib.Path(f"{W}/business_domains/blockchain/testbed/identity/test_payloads")
WF = {"04": "blockchain::WF_ACCEPT_ACTOR_V0", "08": "blockchain::WF_REJECT_ACTOR_V0"}
for f in sorted(P.glob("*.json")):
    wf = WF.get(f.name[:2], "blockchain::WF_REGISTER_ACTOR_V0")
    r = api.run_workflow(wf_fqdn=wf, payload=json.loads(f.read_text()),
                         snapshot_root=f"{W}/snapshot", data_root=f"{W}/data/blockchain")
    print(f"{f.name:<36} {r.status}")
print(api.run_workflow(wf_fqdn="workload::WF_COLLATZ_CONJECTURE_V0", payload={"numbers": [27]},
                       snapshot_root=f"{W}/snapshot", data_root=f"{W}/data/workload").status)
EOF
```

Run this before a release, after any change to the compiler or assembler, and whenever a build
starts behaving differently on two machines.

## After changing a phase's rules

The rule set is declared in `transformation/design/<phase>/rules.py` and **sealed** into that phase's
workflow artifact. Editing the declaration alone leaves `tc phase check` and the governed workflow
evaluating different rule sets:

```bash
python ~/protocol-governed-computing/transformation_compilers/scripts/emit_rule_sets.py           # re-seal
~/protocol-governed-computing/protocol_compiler/compile_domain.sh ~/protocol-governed-computing/transformation_compilers
PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 ~/protocol-governed-computing/snapshot_assembler/assemble.sh
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/build_fixtures.py   # derive
python ~/protocol-governed-computing/transformation_compilers/scripts/testbed/build_payloads.py
```

`--check` first will name the drifted phase. Fixtures and payloads are **derived from the fixture
dossiers** in `scripts/testbed/fixtures/` — never hand-edit one; change the fixture or the mutator in
`build_fixtures.py`. A derived
fixture cannot go stale silently: the derivation raises rather than producing a wrong fixture.

A new rule needs four things, or it is untested: its declaration in the phase's register schema
(`transformation_compilers/registry/schema/REGISTER_SCHEMA_P<n>_V0.json`), recorded as a revision with
`tc phase revise`, plus a procedure module under `design/evaluate/procedures/` only if no keyword or
annotation can state it; a mutator plus `FIXTURES` row in `build_fixtures.py`; and entries in
`build_payloads.py` (source, priors, register key), `e2e_phases_test.py` (`CASES`) and
`differential.py` (`PRIORS_BY_DOCUMENT`).

## Why the phase check is a script

`e2e_phases_test.py` executes each compiled workflow through `protocol_runtime` and asserts the verdict,
finding count and rules evaluated. It is not the same evidence as the differential:

- `differential.py` drives the capability transforms directly — it proves the rule sets and the
  check logic, and nothing about workflow wiring.
- `e2e_phases_test.py` boots the assembled snapshot and dispatches workflows — it proves the IN/WF/CC
  wiring, node bindings and routing.

A workflow that bound `$.capability_result.header` across nodes passed the differential and failed
immediately under the runtime, because workflow nodes read the intent payload rather than a previous
node's result. Both checks are needed; neither substitutes for the other.

## Faster loops

```bash
tc phase list
tc phase check --phase p0 <seed.md>
tc phase check --phase p1 <register.md>
tc phase check --phase p2 <register.md> --snapshot ~/protocol-governed-computing/snapshot

cd ~/protocol-governed-computing/transformation_compilers && python scripts/testbed/differential.py
```

From P2 a phase also needs its **priors**, or the handoff between phases goes unchecked:
P1←p0 · P2←p1 · P3←p2 · P4←p3 · **P5←p0** · P6←p5 · P7←p5+p6 · P8←p7.

**P5 reads the seed, not P4.** It transforms P4's consolidation rather than restating it, so there
is no row-level obligation to check against P4 — but the subdomain purpose is authored once at P0,
has no register to travel in through P1–P4, and reappears at P5. Without the seed, P5 cannot tell an
inherited purpose from a second author's paragraph.

A phase that is *projected* rather than authored is written by the compiler, and the prior is judged
before it is projected:

```bash
D=~/protocol-governed-computing/transformation_compilers/scripts/testbed/fixtures/catalog/cr_02_catalog
tc phase project --phase p1 $D/p0_seed_book_library_mgmt_catalog_v0.md \
   --out $D/p1_change_request_book_library_mgmt_catalog_v0.md --force
```

A seed carrying an open blocking clarification is refused rather than projected. A question found
while restating the seed amends the seed and is projected again — it never enters at P1.

```bash
D=~/protocol-governed-computing/transformation_compilers/scripts/testbed/fixtures/catalog/cr_01_catalog
tc phase check --phase p7 $D/p7_design_intent_book_library_mgmt_catalog_v0.md \
   --prior p5=$D/p5_business_intent_book_library_mgmt_catalog_v0.md \
   --prior p6=$D/p6_governance_intent_book_library_mgmt_catalog_v0.md \
   --snapshot <the composition without book_library_mgmt>
```

A CR is judged against the composition it was **designed** against, never one that already contains
its own output — every identity it assigns would collide. Once a CR is promoted, checking its P7
against the live snapshot reports its own codes as already existing; that is the rule working, not a
defect.

`e2e_phases_test.py` reproduces the composition a catalog fixture is designed against with
`design_baseline()`, side-assembled from:
- the platform, the Collatz workload, inspection and transformation, as compiled;
- `ai_governance`, the neighbour the catalog cites, frozen at `business_domains` `36bc62a` and built
  from git into `traces/design_baseline_sources/`.

Nothing a domain delivers reaches the corpus. The baseline is rebuilt whenever a source root has
been recompiled since.

`tc phase check` is the right loop while authoring a document. Phases through P1 judge a document
alone and need no snapshot; from P2 a phase grounds claims against the composition, so `--snapshot`
is required for its grounding rules to be checked at all — without it they report that they could
not run rather than quietly passing. The differential
needs an assembled snapshot and compares the sealed rule set against the declared one.

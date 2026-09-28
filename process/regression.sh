#!/usr/bin/env bash
# Full regression, as the RUNBOOK specifies it. Long one-line commands are hostile
# to terminal paste; this removes that failure mode and makes the run repeatable.
#
#   regression.sh            execution block only (default — fastest, needs a built snapshot)
#   regression.sh --build    clean rebuild first, then execution
#   regression.sh --all      clean rebuild, then every check, then execution
#
# Expected results are data: `expectations.yaml`, compared by `regression_verdict.py` after the
# run, and the script exits with the verdict. RUNBOOK.md "## Expected" explains each row. Two things
# are red by design: admission_contract_fidelity (31 findings, all deliberate), and the advisory
# half of `si snapshot validate`, which reports known divergences without failing. Each step's output
# and exit code are kept in `traces/regression/` (or $PGC_REGRESSION_OUT).
set -u
cd ~/protocol-governed-computing || exit 1
W=~/protocol-governed-computing
# Overridable so a second profile can be read against the same compiled domains without editing
# this file:  PGC_SNAPSHOT_PROFILE=<IDENTITY> regression.sh --build
export PGC_SNAPSHOT_PROFILE="${PGC_SNAPSHOT_PROFILE:-GOVERNANCE_SURFACE_PROFILE_V0}"

MODE="${1:-exec}"

if [[ "$MODE" == "--build" || "$MODE" == "--all" ]]; then
  echo "=== BUILD: clean rebuild ==="

  # Every generated snapshot, not just the assembled one. Leaving a domain's compiled/ in place
  # makes "clean rebuild" a claim rather than a fact: a retired artifact surviving there is caught
  # by S8 as an undeclared output, which reads as a compiler defect rather than as stale state.
  #
  # `pgc_release/snapshot` is EXCLUDED and must stay excluded. It is not build output — it is the
  # sealed composition a paper cites by DOI, written once by `release.sh --publish-composition`
  # and reproducible by nothing. Its only copy is git. The exclusion is asserted below rather than
  # trusted, because a deletion here is silent and the loss is discovered much later.
  find "$W" -type d -name snapshot \
       -not -path "$W/.venv/*" -not -path "$W/pgc_release/*" \
       -prune -exec rm -rf {} +
  rm -rf "$W/data" "$W/traces"

  # macOS writes .DS_Store into any directory Finder opens, including a sealed snapshot. Acceptance
  # then refuses the snapshot as carrying undeclared content (3b §6) — correct, but it makes a
  # DOI-cited release look corrupt when nothing about it changed. They are gitignored, so nothing
  # warns you and the failure surfaces only at boot. Removing them cannot destroy anything: a
  # .DS_Store is never a constituent. This sweeps the workspace, `pgc_release` included, because
  # that is the one snapshot no rebuild would otherwise clean.
  find "$W" -name .DS_Store -not -path "$W/.venv/*" -delete

  if [[ ! -f "$W/pgc_release/snapshot/manifest.json" ]]; then
    echo "ABORT: the cleanup removed pgc_release/snapshot — sealed evidence, not build output." >&2
    echo "  Recover it before doing anything else:  git -C pgc_release restore snapshot/" >&2
    exit 1
  fi
  "$W/protocol_compiler/compile.sh" STRUCTURE_BUILD_PLATFORM_CONFIG_V2 || exit 1
  # The platform's other two placements, each into its own root. They are compiled against the
  # same governance surface as the default build, so a governance change leaves them stale until they
  # are rebuilt — and the assembler then refuses to compose them with freshly compiled domains, which
  # surfaced as a red test_federation after a change that touched no federation code.
  rm -rf "$W/software_governance/snapshot_fed" "$W/software_governance/snapshot_mw"
  PGC_SNAPSHOT_ROOT="$W/software_governance/snapshot_fed" \
    "$W/protocol_compiler/compile.sh" STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V2 || exit 1
  PGC_SNAPSHOT_ROOT="$W/software_governance/snapshot_mw" \
    "$W/protocol_compiler/compile.sh" STRUCTURE_BUILD_PLATFORM_MULTIWORKER_CONFIG_V2 || exit 1
  for d in conformance_workloads/workloads/collatz transformation snapshot_inspector \
           business_domains/ai_governance business_domains/book_library_mgmt \
           business_domains/blockchain business_domains/causal_language_model; do
    "$W/protocol_compiler/compile_domain.sh" "$W/$d" || exit 1
  done
  "$W/snapshot_assembler/assemble.sh" || exit 1
fi

# Every check and execution step runs through `step`, which keeps its output and exit code. The
# verdict then compares the run against `expectations.yaml` — the RUNBOOK's "## Expected" table as
# data. A step that fails, prints other than what is expected, is missing, or passes where it is red
# by design fails the run. Before this, a failing test script left the run at exit 0, and the
# expected-results table was a rule set in prose that nothing evaluated.
RUN="${PGC_REGRESSION_OUT:-$W/traces/regression}"
rm -rf "$RUN" && mkdir -p "$RUN"
step() {
  local id="$1"; shift
  echo "--- $id"
  "$@" 2>&1 | tee "$RUN/$id.log"
  echo "${PIPESTATUS[0]}" > "$RUN/$id.exit"
}

if [[ "$MODE" == "--all" ]]; then
  echo "checks" >> "$RUN/sections"
  echo; echo "=== CHECKS ==="
  for c in governance_closure governance_chain_closure supersession_agreement \
           human_block_fidelity evidence_determinism admission_contract_fidelity; do
    step "$c" python "$W/.github/process/$c.py"
  done
  step emit_rule_sets python "$W/transformation/scripts/emit_rule_sets.py" --check
  step build_payloads python "$W/transformation/scripts/testbed/build_payloads.py" --check
  step author_transport_contracts env PYTHONPATH="$W/snapshot_inspector" \
    python "$W/snapshot_inspector/scripts/author_transport_contracts.py" --check
  step frontmatter_fidelity python "$W/.github/process/frontmatter_fidelity.py"
  for t in meta_test differential e2e_phases_test projection_test construction_acceptance \
           molecule_design_test vector_design_test keyed_node_design_test \
           refusal_moment_design_test vector_value_design_test; do
    step "$t" python "$W/transformation/scripts/testbed/$t.py"
  done
  step implementation_closure python "$W/.github/process/implementation_closure.py"
  step test_inspector env PYTHONPATH="$W/snapshot_inspector" \
    python "$W/snapshot_inspector/scripts/testbed/test_inspector.py"

  # The domain-authoring path pgc_install/README.md documents, executed. Prose about a build path
  # rots the moment the build changes, and nothing notices.
  step domain_authoring python "$W/.github/process/domain_authoring.py"

  # Suites that existed but were never run here. Two of them were red, and were red unnoticed for
  # exactly that reason — see RUNBOOK "## Expected".
  for t in "$W/snapshot_assembler/scripts/testbed/test_indexes.py" \
           "$W/snapshot_assembler/scripts/testbed/test_transform_conformance_evidence.py" \
           "$W/protocol_compiler/scripts/testbed/test_compiler_atoms.py" \
           "$W/protocol_compiler/scripts/testbed/test_molecule_composition.py" \
           "$W/protocol_compiler/scripts/testbed/test_transform_conformance.py" \
           "$W/protocol_compiler/scripts/testbed/test_vector_build.py" \
           "$W/protocol_compiler/scripts/testbed/test_platform_vectors.py" \
           "$W/protocol_compiler/scripts/testbed/test_keyed_chain_and_molecule_surface.py" \
           "$W/protocol_compiler/scripts/testbed/test_dispatch_routing_fidelity.py" \
           "$W/protocol_compiler/scripts/test_governance_provenance.py" \
           "$W/protocol_runtime/testbed/pgc/test_reference_collatz.py" \
           "$W/protocol_runtime/testbed/pgc/test_warm_boot.py" \
           "$W/protocol_runtime/testbed/pgc/test_federation.py" \
           "$W/protocol_runtime/testbed/pgc/test_capability_concurrency.py" \
           "$W/protocol_runtime/testbed/pgc/test_molecule_execution.py" \
           "$W/protocol_runtime/testbed/pgc/test_node_keyed_routing.py" \
           "$W/protocol_runtime/testbed/pgc/test_trace_path.py" \
           "$W/protocol_runtime/testbed/pgc/test_transform_conformance_runner.py"; do
    step "$(basename "$t" .py)" python "$t"
  done

  # The assembled snapshot read by the inspector that was just composed. test_inspector.py runs
  # against fixtures and says nothing about THIS snapshot; without this line a fully green run can
  # sit on top of a composition carrying advisory failures, which is how fifteen divergent copies
  # went unreported. Advisory failures exit 0 by design — `--strict` is what turns them red.
  step si_snapshot_validate si --snapshot "$W/snapshot" snapshot validate

  step pgc_env_check python "$W/.github/process/pgc_env_check.py"
  step test_regression_verdict python "$W/.github/process/test_regression_verdict.py"
fi

echo "execution" >> "$RUN/sections"
echo; echo "=== EXECUTION ==="
echo "=== clearing data roots ==="
rm -rf "$W/data/collatz" "$W/data/ai_governance" "$W/data/book_library_mgmt" \
       "$W/data/book_library_mgmt_cr02" "$W/data/blockchain" "$W/data/causal_language_model"

echo; echo "=== collatz ==="
step collatz "$W/protocol_runtime/run.sh" run \
  --wf workload::WF_COLLATZ_CONJECTURE_V0 \
  --payload "$W/conformance_workloads/workloads/collatz/test_payloads/01_happy_path.json" \
  --data-root "$W/data/collatz"

echo; echo "=== ai_governance: seed ==="
mkdir -p "$W/data/ai_governance/ai_governance/ai_licensing"
cp "$W/business_domains/ai_governance/testbed/agent_governance/seed_data/license_facts.json" \
   "$W/data/ai_governance/ai_governance/ai_licensing/"

echo; echo "=== ai_governance: govern agent action ==="
step govern_agent_action "$W/protocol_runtime/run.sh" run \
  --wf ai_governance::WF_GOVERN_AGENT_ACTION_V0 \
  --payload "$W/business_domains/ai_governance/testbed/agent_governance/test_payloads/01_valid_standard_action.json" \
  --data-root "$W/data/ai_governance"

echo; echo "=== ai_governance: provision licensing ==="
step provision_licensing "$W/protocol_runtime/run.sh" run \
  --wf ai_governance::WF_PROVISION_AI_LICENSING_V0 \
  --payload "$W/business_domains/ai_governance/testbed/ai_licensing/test_payloads/provision_ai_licensing_payload.json" \
  --data-root "$W/data/ai_governance"

echo; echo "=== book_library_mgmt: catalog (CR-1) ==="
step catalog_cr01 python "$W/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py" \
  --data-root "$W/data/book_library_mgmt"

echo; echo "=== book_library_mgmt: catalog (CR-2) ==="
step catalog_cr02 python "$W/business_domains/book_library_mgmt/testbed/catalog/execution_validation_cr02.py" \
  --data-root "$W/data/book_library_mgmt_cr02"

echo; echo "=== blockchain: identity (must precede wallet) ==="
step blockchain_identity python "$W/business_domains/blockchain/testbed/identity/execution_validation.py" \
  --data-root "$W/data/blockchain"

echo; echo "=== blockchain: wallet ==="
step blockchain_wallet python "$W/business_domains/blockchain/testbed/wallet/execution_validation.py" \
  --data-root "$W/data/blockchain"

echo; echo "=== causal_language_model: model_response ==="
step clm_model_response python "$W/business_domains/causal_language_model/testbed/model_response/execution_validation.py" \
  --data-root "$W/data/causal_language_model"

echo; echo "=== VERDICT ==="
python "$W/.github/process/regression_verdict.py" "$RUN"
exit $?

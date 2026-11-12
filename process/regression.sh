#!/usr/bin/env bash
# Full regression, as the RUNBOOK specifies it. Long one-line commands are hostile
# to terminal paste; this removes that failure mode and makes the run repeatable.
#
#   regression.sh            execution block only (default — fastest, needs a built snapshot)
#   regression.sh --build    clean rebuild first, then execution
#   regression.sh --all      clean rebuild, then every check, then execution
#
# Expected results are data: `expectations.yaml`, compared by `regression_verdict.py` after the
# run, and the script exits with the verdict. RUNBOOK.md "## Expected" explains each row. One thing
# is red by design: the advisory half of `si snapshot validate`, which reports known divergences
# without failing. Each step's output
# and exit code are kept in `traces/regression/` (or $PGC_REGRESSION_OUT).
set -u
cd ~/protocol-governed-computing || exit 1
W=~/protocol-governed-computing
# Every step writes its temporary files into one directory owned by this run. It must be empty when
# the run ends, so a step that leaves anything behind fails the run and names what it left. The
# build's own backup and kept evidence go to the real temporary directory, outside that check.
REAL_TMP="${TMPDIR:-/tmp}"; REAL_TMP="${REAL_TMP%/}"
TEST_TMP="$(mktemp -d "$REAL_TMP/pgc_regression_tmp.XXXXXX")" || exit 1
export TMPDIR="$TEST_TMP"
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
  #
  # The previous build output is moved aside, not deleted, and comes back if the rebuild fails, so
  # a failed build never leaves the later checks without a snapshot to fail on for their own
  # reasons. It is deleted only once the new build has been assembled.
  BACKUP="$(mktemp -d "$REAL_TMP/pgc_rebuild.XXXXXX")" || exit 1
  build_output() {
    find "$W" -type d \( -name snapshot -o -name snapshot_fed -o -name snapshot_mw \) \
         -not -path "$W/.venv/*" -not -path "$W/pgc_release/*" -prune -print
    for d in "$W/data" "$W/traces"; do [[ -d "$d" ]] && echo "$d"; done
  }
  build_output | while IFS= read -r d; do
    rel="${d#"$W"/}"
    mkdir -p "$BACKUP/$(dirname "$rel")" && mv "$d" "$BACKUP/$rel" && echo "$rel" >> "$BACKUP/.moved"
  done
  rebuild_failed() {
    # Keep the failing output before the restore replaces it: a failure that passes on rerun is
    # otherwise undiagnosable, because the restore is what erases its evidence.
    KEPT="$(mktemp -d "$REAL_TMP/pgc_failed_build.XXXXXX")"
    build_output | while IFS= read -r d; do
      rel="${d#"$W"/}"; mkdir -p "$KEPT/$(dirname "$rel")" && cp -R "$d" "$KEPT/$rel"
    done
    echo "BUILD FAILED — the failing output is kept in $KEPT" >&2
    echo "BUILD FAILED — restoring the previous build output from $BACKUP" >&2
    build_output | while IFS= read -r d; do rm -rf "$d"; done
    if [[ -f "$BACKUP/.moved" ]]; then
      while IFS= read -r rel; do
        mkdir -p "$W/$(dirname "$rel")" && mv "$BACKUP/$rel" "$W/$rel"
      done < "$BACKUP/.moved"
    fi
    rm -rf "$BACKUP" "$TEST_TMP"
    exit 1
  }

  # macOS writes .DS_Store into any directory Finder opens, including a sealed snapshot. Acceptance
  # then refuses the snapshot as carrying undeclared content (3b §6) — correct, but it makes a
  # DOI-cited release look corrupt when nothing about it changed. They are gitignored, so nothing
  # warns you and the failure surfaces only at boot. Removing them cannot destroy anything: a
  # .DS_Store is never a constituent. This sweeps the workspace, `pgc_release` included, because
  # that is the one snapshot no rebuild would otherwise clean.
  find "$W" -name .DS_Store -not -path "$W/.venv/*" -delete
  # Bytecode is build output too. A clean rebuild compiles every module from its source.
  find "$W" -name __pycache__ -type d -not -path "$W/.venv/*" -prune -exec rm -rf {} +

  if [[ ! -f "$W/pgc_release/snapshot/manifest.json" ]]; then
    echo "ABORT: the cleanup removed pgc_release/snapshot — sealed evidence, not build output." >&2
    echo "  Recover it before doing anything else:  git -C pgc_release restore snapshot/" >&2
    rebuild_failed
  fi
  "$W/protocol_compiler/compile.sh" STRUCTURE_BUILD_PLATFORM_CONFIG_V0 || rebuild_failed
  # Every domain compiles against this surface, so nothing after this point may change it. Its
  # fingerprint is taken once and re-read after each later compile; a step that alters it is named.
  surface() { (cd "$W/software_governance/snapshot" && find . -type f -print0 | sort -z |
               xargs -0 shasum | shasum | cut -d' ' -f1); }
  SURFACE="$(surface)"
  surface_unchanged() {
    [[ "$(surface)" == "$SURFACE" ]] && return 0
    echo "BUILD FAILED — the platform surface changed during: $1" >&2
    rebuild_failed
  }
  # The platform's other two placements, each into its own root. They are compiled against the
  # same governance surface as the default build, so a governance change leaves them stale until they
  # are rebuilt — and the assembler then refuses to compose them with freshly compiled domains, which
  # surfaced as a red test_federation after a change that touched no federation code.
  # Each configuration declares its own root (output_configuration.root), so none is passed here.
  "$W/protocol_compiler/compile.sh" STRUCTURE_BUILD_PLATFORM_FEDERATED_CONFIG_V0 || rebuild_failed
  surface_unchanged "the federated platform compile"
  "$W/protocol_compiler/compile.sh" STRUCTURE_BUILD_PLATFORM_MULTIWORKER_CONFIG_V0 || rebuild_failed
  surface_unchanged "the multiworker platform compile"
  for d in conformance_workloads/workloads/collatz transformation_compilers snapshot_inspector \
           business_domains/ai_governance business_domains/book_library_mgmt \
           business_domains/blockchain business_domains/causal_language_model; do
    "$W/protocol_compiler/compile_domain.sh" "$W/$d" || rebuild_failed
    surface_unchanged "the $d compile"
  done
  "$W/snapshot_assembler/assemble.sh" || rebuild_failed
  rm -rf "$BACKUP"
fi

# Every check and execution step runs through `step`, which keeps its output and exit code. The
# verdict then compares the run against `expectations.yaml` — the RUNBOOK's "## Expected" table as
# data. A step that fails, prints other than what is expected, is missing, or passes where it is red
# by design fails the run, so the expected-results table is a rule set that is evaluated, not prose.
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
           human_block_fidelity evidence_determinism; do
    step "$c" python "$W/.github/process/$c.py"
  done
  step emit_rule_sets python "$W/transformation_compilers/scripts/emit_rule_sets.py" --snapshot "$W/snapshot" --check
  step build_payloads python "$W/transformation_compilers/scripts/testbed/build_payloads.py" --check
  step baseline_designs python "$W/transformation_compilers/scripts/write_baseline_designs.py" --check
  step author_transport_contracts env PYTHONPATH="$W/snapshot_inspector" \
    python "$W/snapshot_inspector/scripts/author_transport_contracts.py" --check
  step frontmatter_fidelity python "$W/.github/process/frontmatter_fidelity.py"
  for t in meta_test closure_test effectivity_test render_vectors_test construction_mapping_test interface_structures_test differential e2e_phases_test projection_test construction_acceptance \
           molecule_design_test vector_design_test keyed_node_design_test \
           refusal_moment_design_test semantic_change_design_test \
           entrance_gate_design_test binding_literal_design_test route_seal_test reuse_own_domain_test delivery_declared_test; do
    step "$t" python "$W/transformation_compilers/scripts/testbed/$t.py"
  done
  step implementation_closure python "$W/.github/process/implementation_closure.py"
  step test_inspector env PYTHONPATH="$W/snapshot_inspector" \
    python "$W/snapshot_inspector/scripts/testbed/test_inspector.py"

  # The domain-authoring path pgc_install/README.md documents, executed. Prose about a build path
  # rots the moment the build changes, and nothing notices.
  step domain_authoring python "$W/.github/process/domain_authoring.py"

  # The derive route: each ledger admitted, answers outside their shapes refused, and each derived
  # domain's phase documents judged, then built in scratch through construction, compile, assembly
  # and its suites.
  L="$W/transformation_compilers/testbed/ledgers"
  step derive_ledgers tc phase derive check "$L/book_library_mgmt/ledger.yaml" "$L/blockchain/ledger.yaml" \
    "$L/ai_governance/ledger.yaml"
  step derive_meta tc phase derive meta --snapshot "$W/snapshot"
  step derive_selftest tc phase derive selftest "$L/book_library_mgmt/ledger.yaml" "$L/ai_governance/ledger.yaml"
  # Each delivered domain's owner-decision criteria, against the domain before the derive route
  # designed it (business_domains 36bc62a): a criterion the delivery made true fails there.
  CB="$W/transformation_compilers/scripts/criteria_before.sh"
  step criteria_before_book_library_mgmt bash "$CB" book_library_mgmt 36bc62a \
    testbed/catalog/execution_validation_owner_decisions.py
  step criteria_before_blockchain bash "$CB" blockchain 36bc62a testbed/identity/execution_validation_owner_decisions.py
  step criteria_before_ai_governance bash "$CB" ai_governance 36bc62a \
    testbed/owner_decisions/execution_validation_owner_decisions.py
  for d in book_library_mgmt blockchain ai_governance; do
    step "derive_$d" bash -c 'out="$(mktemp -d)"; bash "$1/transformation_compilers/scripts/derive_build.sh" "$2" "$out"
      rc=$?; rm -rf "$out"; exit $rc' _ "$W" "$d"
  done

  # Suites that existed but were never run here. Two of them were red, and were red unnoticed for
  # exactly that reason — see RUNBOOK "## Expected".
  for t in "$W/snapshot_assembler/scripts/testbed/test_indexes.py" \
           "$W/snapshot_assembler/scripts/testbed/test_transform_conformance_evidence.py" \
           "$W/protocol_compiler/scripts/testbed/test_compiler_atoms.py" \
           "$W/protocol_compiler/scripts/testbed/test_molecule_composition.py" \
           "$W/protocol_compiler/scripts/testbed/test_transform_conformance.py" \
           "$W/protocol_compiler/scripts/testbed/test_vector_build.py" \
           "$W/protocol_compiler/scripts/testbed/test_reference_semantics.py" \
           "$W/protocol_compiler/scripts/testbed/test_routing_closure.py" \
           "$W/protocol_compiler/scripts/testbed/test_routing_lookup.py" \
           "$W/protocol_compiler/scripts/testbed/test_input_typed.py" \
           "$W/protocol_compiler/scripts/testbed/test_governance_ontology.py" \
           "$W/protocol_compiler/scripts/testbed/test_admission_covers_bindings.py" \
           "$W/protocol_compiler/scripts/testbed/test_platform_vectors.py" \
           "$W/protocol_compiler/scripts/testbed/test_keyed_chain_and_molecule_surface.py" \
           "$W/protocol_compiler/scripts/testbed/test_dispatch_routing_fidelity.py" \
           "$W/protocol_compiler/scripts/testbed/test_force_and_output_root.py" \
           "$W/protocol_compiler/scripts/test_governance_provenance.py" \
           "$W/protocol_runtime/testbed/pgc/test_reference_collatz.py" \
           "$W/protocol_runtime/testbed/pgc/test_step_outcome.py" \
           "$W/protocol_runtime/testbed/pgc/test_no_default.py" \
           "$W/protocol_runtime/testbed/pgc/test_unknown_continuation.py" \
           "$W/protocol_runtime/testbed/pgc/test_no_smart_execution.py" \
           "$W/protocol_runtime/testbed/pgc/test_warm_boot.py" \
           "$W/protocol_runtime/testbed/pgc/test_resident_boot.py" \
           "$W/protocol_runtime/testbed/pgc/test_federation.py" \
           "$W/protocol_runtime/testbed/pgc/test_capability_concurrency.py" \
           "$W/protocol_runtime/testbed/pgc/test_molecule_execution.py" \
           "$W/protocol_runtime/testbed/pgc/test_node_keyed_routing.py" \
           "$W/protocol_runtime/testbed/pgc/test_examine.py" \
           "$W/protocol_runtime/testbed/pgc/test_transform_conformance_runner.py"; do
    step "$(basename "$t" .py)" python "$t"
  done

  # The assembled snapshot read by the inspector that was just composed. test_inspector.py runs
  # against fixtures and says nothing about THIS snapshot; without this line a fully green run can
  # sit on top of a composition carrying advisory failures, which is how fifteen divergent copies
  # went unreported. Advisory failures exit 0 by design — `--strict` is what turns them red.
  step si_snapshot_validate si --snapshot "$W/snapshot" snapshot validate --strict

  # What the sealed composition published still means what it meant (`4e` SU-11).
  step published_identity python "$W/.github/process/published_identity_check.py"
  step single_instance python "$W/.github/process/single_instance_check.py" \
    --namespace transformation --namespace artifact --namespace lifecycle

  step pgc_env_check python "$W/.github/process/pgc_env_check.py"
  step test_regression_verdict python "$W/.github/process/test_regression_verdict.py"
fi

echo "execution" >> "$RUN/sections"
echo; echo "=== EXECUTION ==="
echo "=== clearing data roots ==="
rm -rf "$W/data/collatz" "$W/data/ai_governance" "$W/data/book_library_mgmt" \
       "$W/data/book_library_mgmt_works" "$W/data/blockchain" "$W/data/causal_language_model" \
  "$W/data/causal_language_model_hosted"

echo; echo "=== collatz ==="
step collatz "$W/protocol_runtime/run.sh" run \
  --wf workload::WF_COLLATZ_CONJECTURE_V0 \
  --payload "$W/conformance_workloads/workloads/collatz/test_payloads/01_happy_path.json" \
  --data-root "$W/data/collatz"

echo; echo "=== ai_governance: license the seed users through ai_licensing's own acts ==="
P="$W/business_domains/ai_governance/testbed/ai_licensing/test_payloads"
step set_license_cap "$W/protocol_runtime/run.sh" run --wf ai_governance::WF_SET_LICENSE_CAP_V0 \
  --payload "$P/01_set_license_cap.json" --data-root "$W/data/ai_governance"
step register_employee "$W/protocol_runtime/run.sh" run --wf ai_governance::WF_REGISTER_EMPLOYEE_V0 \
  --payload "$P/02_register_employee_std.json" --data-root "$W/data/ai_governance"
step record_training_completed "$W/protocol_runtime/run.sh" run --wf ai_governance::WF_RECORD_TRAINING_COMPLETED_V0 \
  --payload "$P/03_record_training_std.json" --data-root "$W/data/ai_governance"
step provision_licensing "$W/protocol_runtime/run.sh" run --wf ai_governance::WF_PROVISION_LICENSE_V0 \
  --payload "$P/04_provision_license_std.json" --data-root "$W/data/ai_governance"

echo; echo "=== ai_governance: govern agent action ==="
step govern_agent_action "$W/protocol_runtime/run.sh" run \
  --wf ai_governance::WF_GOVERN_AGENT_ACTION_V1 \
  --payload "$W/business_domains/ai_governance/testbed/agent_governance/test_payloads/01_valid_standard_action.json" \
  --data-root "$W/data/ai_governance"

echo; echo "=== ai_governance: the owner's decisions (cr_04) ==="
step ai_governance_owner_decisions python "$W/business_domains/ai_governance/testbed/owner_decisions/execution_validation_owner_decisions.py"

echo; echo "=== book_library_mgmt: catalog (CR-1) ==="
step catalog_registration python "$W/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py" \
  --data-root "$W/data/book_library_mgmt"

echo; echo "=== book_library_mgmt: catalog (CR-2) ==="
step catalog_works python "$W/business_domains/book_library_mgmt/testbed/catalog/execution_validation_works.py" \
  --data-root "$W/data/book_library_mgmt_works"

echo; echo "=== book_library_mgmt: catalog (cr_06 to cr_09, the owner's decisions) ==="
step catalog_owner_decisions python "$W/business_domains/book_library_mgmt/testbed/catalog/execution_validation_owner_decisions.py"

echo; echo "=== blockchain: identity (must precede wallet) ==="
step blockchain_identity python "$W/business_domains/blockchain/testbed/identity/execution_validation.py" \
  --data-root "$W/data/blockchain"

echo; echo "=== blockchain: wallet ==="
step blockchain_wallet python "$W/business_domains/blockchain/testbed/wallet/execution_validation.py" \
  --data-root "$W/data/blockchain"

echo; echo "=== causal_language_model: model_response ==="
step clm_model_response python "$W/business_domains/causal_language_model/testbed/model_response/execution_validation.py" \
  --data-root "$W/data/causal_language_model"

echo; echo "=== causal_language_model: hosted model ==="
step clm_hosted_model python "$W/business_domains/causal_language_model/testbed/hosted_model/execution_validation.py" \
  --data-root "$W/data/causal_language_model_hosted"

# Every trace this block wrote, against the schema its constitution names. Scoped to the data roots
# cleared above, so a stale trace from an earlier run is never what is judged.
echo; echo "=== trace schema ==="
echo; echo "=== blockchain: routing closure (each case on its own scratch root) ==="
step blockchain_routing_closure python "$W/business_domains/blockchain/testbed/routing_closure/execution_validation.py"

echo; echo "=== blockchain: the owner's decisions (cr_08 to cr_11) ==="
step blockchain_owner_decisions python "$W/business_domains/blockchain/testbed/identity/execution_validation_owner_decisions.py"

echo; echo "=== transformation: routing closure (a phase whose observation finds nothing rejects) ==="
step transformation_routing_closure python "$W/transformation_compilers/testbed/routing_closure/execution_validation.py"

echo; echo "=== ai_governance: reclaim closure (a reclaim the registry refuses stays active) ==="
step ai_governance_reclaim_closure python "$W/business_domains/ai_governance/testbed/routing_closure/execution_validation.py"

echo; echo "=== transport: the pgc_transport command (exit status and response, per Result Class) ==="
step transport_cli bash "$W/.github/process/transport_cli_check.sh"

echo; echo "=== demo: pgc-demo.sh in workspace mode, every terminal step README_DEMO.md walks ==="
step demo_script bash "$W/.github/process/demo_script_check.sh"

step trace_schema_conformance python "$W/.github/process/trace_schema_conformance.py" \
  "$W/data/collatz" "$W/data/ai_governance" "$W/data/book_library_mgmt" \
  "$W/data/book_library_mgmt_works" "$W/data/blockchain" "$W/data/causal_language_model" \
  "$W/data/causal_language_model_hosted"

step temp_hygiene bash -c 'left="$(ls -A "$1")"
  if [[ -n "$left" ]]; then echo "TEMP HYGIENE FAILED — steps left these in their TMPDIR:"; echo "$left"; exit 1; fi
  echo "TEMP HYGIENE PASSED — no step left anything in its TMPDIR"' _ "$TEST_TMP"
rm -rf "$TEST_TMP"

echo; echo "=== VERDICT ==="
python "$W/.github/process/regression_verdict.py" "$RUN"
exit $?

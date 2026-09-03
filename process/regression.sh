#!/usr/bin/env bash
# Full regression, as the RUNBOOK specifies it. Long one-line commands are hostile
# to terminal paste; this removes that failure mode and makes the run repeatable.
#
#   regression.sh            execution block only (default — fastest, needs a built snapshot)
#   regression.sh --build    clean rebuild first, then checks, then execution
#   regression.sh --all      build + checks + execution
#
# Expected results are the table in RUNBOOK.md "## Expected". One check is red by
# design: admission_contract_fidelity, 31 findings, all deliberate.
set -u
cd ~/protocol-governed-computing || exit 1
W=~/protocol-governed-computing
export PGC_SNAPSHOT_PROFILE=REFERENCE_PLATFORM_PROFILE_V1

MODE="${1:-exec}"

if [[ "$MODE" == "--build" || "$MODE" == "--all" ]]; then
  echo "=== BUILD: clean rebuild ==="
  rm -rf "$W/snapshot" "$W/data" "$W/traces"
  "$W/protocol_compiler/compile.sh" STRUCTURE_BUILD_PLATFORM_CONFIG_V1 || exit 1
  for d in conformance_workloads/workloads/collatz transformation snapshot_inspector \
           business_domains/ai_governance business_domains/book_library_mgmt \
           business_domains/blockchain; do
    "$W/protocol_compiler/compile_domain.sh" "$W/$d" || exit 1
  done
  "$W/snapshot_assembler/assemble.sh" || exit 1
fi

if [[ "$MODE" == "--all" ]]; then
  echo; echo "=== CHECKS ==="
  for c in governance_closure governance_chain_closure supersession_agreement \
           human_block_fidelity evidence_determinism admission_contract_fidelity; do
    echo "--- $c"; python "$W/.github/process/$c.py"
  done
  python "$W/transformation/scripts/emit_rule_sets.py" --check
  python "$W/transformation/scripts/testbed/build_payloads.py" --check
  PYTHONPATH="$W/snapshot_inspector" python "$W/snapshot_inspector/scripts/author_transport_contracts.py" --check
  python "$W/.github/process/frontmatter_fidelity.py"
  for t in meta_test differential e2e_phases_test projection_test construction_acceptance; do
    echo "--- $t"; python "$W/transformation/scripts/testbed/$t.py"
  done
  python "$W/.github/process/implementation_closure.py"
  PYTHONPATH="$W/snapshot_inspector" python "$W/snapshot_inspector/scripts/testbed/test_inspector.py"
  python "$W/.github/process/pgc_env_check.py"
fi

echo; echo "=== EXECUTION ==="
echo "=== clearing data roots ==="
rm -rf "$W/data/collatz" "$W/data/ai_governance" "$W/data/book_library_mgmt" \
       "$W/data/book_library_mgmt_cr02" "$W/data/blockchain"

echo; echo "=== collatz ==="
"$W/protocol_runtime/run.sh" run \
  --wf workload::WF_COLLATZ_CONJECTURE_V0 \
  --payload "$W/conformance_workloads/workloads/collatz/test_payloads/01_happy_path.json" \
  --data-root "$W/data/collatz"

echo; echo "=== ai_governance: seed ==="
mkdir -p "$W/data/ai_governance/ai_governance/ai_licensing"
cp "$W/business_domains/ai_governance/testbed/agent_governance/seed_data/license_facts.json" \
   "$W/data/ai_governance/ai_governance/ai_licensing/"

echo; echo "=== ai_governance: govern agent action ==="
"$W/protocol_runtime/run.sh" run \
  --wf ai_governance::WF_GOVERN_AGENT_ACTION_V0 \
  --payload "$W/business_domains/ai_governance/testbed/agent_governance/test_payloads/01_valid_standard_action.json" \
  --data-root "$W/data/ai_governance"

echo; echo "=== ai_governance: provision licensing ==="
"$W/protocol_runtime/run.sh" run \
  --wf ai_governance::WF_PROVISION_AI_LICENSING_V0 \
  --payload "$W/business_domains/ai_governance/testbed/ai_licensing/test_payloads/provision_ai_licensing_payload.json" \
  --data-root "$W/data/ai_governance"

echo; echo "=== book_library_mgmt: catalog (CR-1) ==="
python "$W/business_domains/book_library_mgmt/testbed/catalog/execution_validation.py" \
  --data-root "$W/data/book_library_mgmt"

echo; echo "=== book_library_mgmt: catalog (CR-2) ==="
python "$W/business_domains/book_library_mgmt/testbed/catalog/execution_validation_cr02.py" \
  --data-root "$W/data/book_library_mgmt_cr02"

echo; echo "=== blockchain: identity (must precede wallet) ==="
python "$W/business_domains/blockchain/testbed/identity/execution_validation.py" \
  --data-root "$W/data/blockchain"

echo; echo "=== blockchain: wallet ==="
python "$W/business_domains/blockchain/testbed/wallet/execution_validation.py" \
  --data-root "$W/data/blockchain"

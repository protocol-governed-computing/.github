#!/usr/bin/env bash
#
# The `pgc_transport` command, as an installed user runs it, against the working snapshot.
#
# `pgc_transport call` is the command-line Protocol Adapter: it prints the Canonical Transport
# Response and projects the Result Class onto its exit status. Each case below checks both — the
# status the adapter owns, and the response the boundary owns. Transport is not installed in the
# workspace, so the command runs from the repository root, exactly as `run_http.sh` provisions it.
#
#   transport_cli_check.sh        prints TRANSPORT CLI PASSED — n/n cases, or FAILED with the cases
set -uo pipefail

W="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/transport_cli.XXXXXX")"
trap 'rm -rf "$SCRATCH"' EXIT

export PYTHONPATH="$W/protocol_transport${PYTHONPATH:+:$PYTHONPATH}"
export PGC_SNAPSHOT_ROOT="$W/snapshot" PGC_DATA_ROOT="$SCRATCH"
export PGC_SNAPSHOT_PROFILES="$W/.github/snapshot_profiles"
pgc_transport() { python -m pgc_transport.adapters.cli.main "$@"; }

total=0; failed=()
# case NAME EXIT PATTERN COMMAND... — the command exits EXIT and its output matches PATTERN.
case_() {
  local name=$1 want=$2 pattern=$3 out got; shift 3
  total=$((total + 1))
  out="$("$@" 2>&1)"; got=$?
  if [ "$got" = "$want" ] && grep -qE -- "$pattern" <<< "$out"; then
    echo "  ok    $name"
  else
    echo "  FAIL  $name (exit $got, wanted $want; pattern '$pattern')"
    sed 's/^/        /' <<< "$out" | head -8
    failed+=("$name")
  fi
}

case_ "admits 27: SUCCESS, exit 0"             0 '"steps": 111' \
  pgc_transport call collatz.compute '{"number": 27}'
case_ "names the run's trace"                  0 '"trace:traces/workload/' \
  pgc_transport call collatz.compute '{"number": 6}'
case_ "refuses -5: VIOLATION, exit 1"          1 'INPUT_OUT_OF_RANGE' \
  pgc_transport call collatz.compute '{"number": -5}'
case_ "refuses text: VIOLATION, exit 1"        1 'INPUT_TYPE' \
  pgc_transport call collatz.compute '{"number": "abc"}'
case_ "unknown operation: exit 5"              5 'OPERATION_NOT_FOUND' \
  pgc_transport call no.such.operation
case_ "inspection through the same command"    0 '"max": 999999' \
  pgc_transport call si.artifact.show '{"artifact": "workload::TI_COLLATZ_COMPUTE_V0"}'
case_ "input that is not JSON: usage, exit 2"  2 'not JSON' \
  pgc_transport call collatz.compute 'x'
case_ "no data root: usage, exit 2"            2 'PGC_DATA_ROOT is not set' \
  env -u PGC_DATA_ROOT python -m pgc_transport.adapters.cli.main call collatz.compute '{"number": 27}'

passed=$((total - ${#failed[@]}))
if [ ${#failed[@]} -eq 0 ]; then
  echo "TRANSPORT CLI PASSED — $passed/$total cases"
else
  echo "TRANSPORT CLI FAILED — $passed/$total cases; failing: ${failed[*]}"
  exit 1
fi

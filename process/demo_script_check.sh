#!/usr/bin/env bash
#
# pgc_install/demo/pgc-demo.sh, in workspace mode, through every terminal step README_DEMO.md walks.
#
# The demo adds no behavior: each step runs a PGC command. This checks that the script and the
# commands it runs still agree with what the demo tells a reader — the limit, the refusals, a
# rebuilt snapshot that admits more, a rebuild that reproduces its identity, the refusal of an
# edited snapshot, and the way back. The web pages are not served here.
#
#   demo_script_check.sh          prints DEMO SCRIPT PASSED — n/n cases, or FAILED with the cases
set -uo pipefail

W="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/demo_script.XXXXXX")"
trap 'rm -rf "$SCRATCH"' EXIT

# The command a user installs as `pgc_transport`, provided from the repository root.
PY="$(python -c 'import sys; print(sys.executable)')"
mkdir -p "$SCRATCH/bin"
printf '#!/usr/bin/env bash\nPYTHONPATH="%s${PYTHONPATH:+:$PYTHONPATH}" exec "%s" -m pgc_transport.adapters.cli.main "$@"\n' \
  "$W/protocol_transport" "$PY" > "$SCRATCH/bin/pgc_transport"
chmod +x "$SCRATCH/bin/pgc_transport"

export PATH="$SCRATCH/bin:$PATH"
export PGC_DEMO_HOME="$SCRATCH/home" PGC_DEMO_WORKSPACE="$W" PGC_DEMO_REF=regression
export PGC_DEMO_PYTHON="$PY" PGC_DEMO_NO_BROWSER=1
demo() { bash "$W/pgc_install/demo/pgc-demo.sh" "$@"; }

total=0; failed=(); OUT=""
case_() {
  local name=$1 want=$2 pattern=$3 got; shift 3
  total=$((total + 1))
  OUT="$("$@" 2>&1)"; got=$?
  if [ "$got" = "$want" ] && grep -qE -- "$pattern" <<< "$OUT"; then
    echo "  ok    $name"
  else
    echo "  FAIL  $name (exit $got, wanted $want; pattern '$pattern')"
    sed 's/^/        /' <<< "$OUT" | tail -8
    failed+=("$name")
  fi
}
built_id() { sed -nE 's/^New snapshot +([0-9a-f]{64}).*/\1/p' <<< "$OUT"; }

case_ "plays 27"                                0 '"steps": 111'               demo collatz 27
case_ "refuses 1000000 at the entrance"         1 'above maximum 999999'       demo collatz 1000000
case_ "refuses text at the entrance"            1 'INPUT_TYPE'                 demo collatz abc
case_ "set-limit rebuilds and seals"            0 'New snapshot +[0-9a-f]{64}' demo collatz set-limit 9999999
first="$(built_id)"
case_ "the rebuilt snapshot admits 1000000"     0 '"steps": 152'               demo collatz 1000000
case_ "show reads the raised limit"             0 'max: 9999999'               demo inspect show workload::TI_COLLATZ_COMPUTE_V0
case_ "a second build of one limit"             0 'New snapshot +[0-9a-f]{64}' demo collatz set-limit 9999999
second="$(built_id)"
total=$((total + 1))
if [ -n "$first" ] && [ "$first" = "$second" ]; then echo "  ok    reproduces its identity"
else echo "  FAIL  reproduces its identity ('$first' then '$second')"; failed+=("identity"); fi
case_ "tamper is refused at acceptance"         0 'refused at acceptance'      demo collatz tamper
case_ "reset restores the published snapshot"   0 'published snapshot is active' demo collatz reset
case_ "which refuses 1000000 again"             1 'above maximum 999999'       demo collatz 1000000
case_ "code prints the transform's module"      0 'CT_PURE_COLLATZ_STEP_V0' \
  demo inspect code workloads.collatz.implementation.capability_transforms.atoms.ct_pure_collatz_step_v0

passed=$((total - ${#failed[@]}))
if [ ${#failed[@]} -eq 0 ]; then
  echo "DEMO SCRIPT PASSED — $passed/$total cases"
else
  echo "DEMO SCRIPT FAILED — $passed/$total cases; failing: ${failed[*]}"
  exit 1
fi

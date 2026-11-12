"""The verdict fails a run for each way a run can differ from what is expected.

Before the verdict, `regression.sh` exited 0 whatever its steps did, and the RUNBOOK's expected results
were prose nothing compared. Each case here is one way a run can go wrong unnoticed, shown to fail:
a step failing, a step printing a different count, a failure red by design coming back green, a step
not run, a step run that nobody declared, and a unittest suite that skipped everything.

Run:  python .github/process/test_regression_verdict.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from regression_verdict import judge

EXPECTED = [
    {"id": "closure", "section": "checks", "expect": ["CLOSURE PASSED — 34"]},
    {"id": "fidelity", "section": "checks", "exit": 1, "expect": ["FAILED — 31 finding"],
     "red_by_design": "deliberate findings"},
    {"id": "suite", "section": "checks", "expect": ["Ran 6 tests", "(?m)^OK$"]},
    {"id": "wallet", "section": "execution", "expect": ["9/9 criteria hold"]},
]
GOOD = {"closure": (0, "CLOSURE PASSED — 34 transform(s)"),
        "fidelity": (1, "FAILED — 31 finding(s)"),
        "suite": (0, "Ran 6 tests in 0.9s\n\nOK"),
        "wallet": (0, "9/9 criteria hold")}


def verdicts(steps: dict, sections=("checks", "execution")) -> dict[str, str]:
    with tempfile.TemporaryDirectory() as tmp:
        run = Path(tmp)
        (run / "sections").write_text("\n".join(sections))
        for sid, (code, text) in steps.items():
            (run / f"{sid}.exit").write_text(str(code))
            (run / f"{sid}.log").write_text(text)
        return {sid: v for sid, v, _ in judge(run, EXPECTED)}


def test_a_run_as_expected_holds():
    assert verdicts(GOOD) == {"closure": "OK", "fidelity": "RED BY DESIGN", "suite": "OK", "wallet": "OK"}


def test_a_failing_step_fails_the_run():
    assert verdicts({**GOOD, "wallet": (1, "8/9 criteria hold")})["wallet"] == "MISMATCH"


def test_a_count_that_moves_fails_the_run_even_at_exit_0():
    assert verdicts({**GOOD, "closure": (0, "CLOSURE PASSED — 35 transform(s)")})["closure"] == "MISMATCH"


def test_a_failure_red_by_design_that_passes_is_an_unexpected_pass():
    assert verdicts({**GOOD, "fidelity": (0, "PASSED")})["fidelity"] == "UNEXPECTED PASS"


def test_a_step_not_run_is_missing():
    steps = {k: v for k, v in GOOD.items() if k != "suite"}
    assert verdicts(steps)["suite"] == "MISSING"


def test_a_step_nobody_declared_is_unexpected():
    assert verdicts({**GOOD, "stray": (0, "fine")})["stray"] == "UNEXPECTED STEP"


def test_a_suite_that_skipped_everything_is_not_a_pass():
    assert verdicts({**GOOD, "suite": (0, "Ran 6 tests in 0.0s\n\nOK (skipped=6)")})["suite"] == "MISMATCH"


def test_a_section_not_run_is_not_judged():
    execution_only = {"wallet": GOOD["wallet"]}
    assert verdicts(execution_only, sections=("execution",)) == {"wallet": "OK"}


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except Exception as exc:  # report every test, then fail the run
            failed += 1
            print(f"  FAIL  {name}: {exc!r}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)

"""The regression's verdict: the run compared against `expectations.yaml`.

`regression.sh` runs each check and execution step through `step`, which keeps the step's output as
`<id>.log` and its exit code as `<id>.exit` in the run directory, and records which sections ran in
`sections`. This compares every step against its expectation.

A step holds when its exit code is the one expected and every expected line appears in its output.
The run fails on:

- **a mismatch** — a step failing, or printing other than what is expected;
- **an unexpected pass** — a step red by design coming back green. A known failure that silently
  stops failing means something changed that nobody decided, and the expectation is now wrong;
- **a missing step** — expected in a section that ran, and not run;
- **an unexpected step** — run, with no expectation. A step nobody states the result of is a step
  whose result nobody checks.

Expected lines are regular expressions, and counts are stated exactly. A count that grows is a change
too, and changing the expectation is how it is accepted.

Run:  python .github/process/regression_verdict.py <run dir> [--expectations <path>]
Exit: 0 if every step holds, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DEFAULT_EXPECTATIONS = HERE / "expectations.yaml"


def load(path: Path) -> list[dict]:
    steps = yaml.safe_load(path.read_text(encoding="utf-8"))["steps"]
    seen: set[str] = set()
    for s in steps:
        if s["id"] in seen:
            raise SystemExit(f"{path}: step {s['id']!r} is declared twice")
        seen.add(s["id"])
        if s.get("section") not in ("checks", "execution"):
            raise SystemExit(f"{path}: step {s['id']!r} names no section (checks | execution)")
    return steps


def judge(run: Path, expected: list[dict]) -> list[tuple[str, str, str]]:
    """(step, verdict, detail) for every step expected or run."""
    sections = set((run / "sections").read_text().split()) if (run / "sections").is_file() else set()
    ran = {p.stem for p in run.glob("*.exit")}
    out: list[tuple[str, str, str]] = []

    for s in expected:
        sid, want_exit = s["id"], int(s.get("exit", 0))
        if s["section"] not in sections:
            continue
        if sid not in ran:
            out.append((sid, "MISSING", "expected in this run and not run"))
            continue
        got_exit = int((run / f"{sid}.exit").read_text().strip() or -1)
        text = (run / f"{sid}.log").read_text(encoding="utf-8", errors="replace")
        absent = [p for p in s.get("expect", []) if not re.search(p, text)]
        if got_exit == want_exit and not absent:
            out.append((sid, "RED BY DESIGN" if s.get("red_by_design") else "OK", ""))
        elif s.get("red_by_design") and got_exit == 0 and want_exit != 0:
            out.append((sid, "UNEXPECTED PASS",
                        f"red by design ({s['red_by_design']}) and now exits 0 — decide, then update "
                        f"the expectation"))
        else:
            detail = []
            if got_exit != want_exit:
                detail.append(f"exit {got_exit}, expected {want_exit}")
            if absent:
                detail.append("missing: " + "; ".join(absent))
            out.append((sid, "MISMATCH", " — ".join(detail)))

    declared = {s["id"] for s in expected}
    for sid in sorted(ran - declared):
        out.append((sid, "UNEXPECTED STEP", "ran with no expectation in expectations.yaml"))
    return out


def main() -> int:
    args = sys.argv[1:]
    expectations = DEFAULT_EXPECTATIONS
    if "--expectations" in args:
        i = args.index("--expectations")
        expectations = Path(args[i + 1])
        del args[i:i + 2]
    if len(args) != 1:
        print(__doc__.strip().splitlines()[-2])
        return 1
    run = Path(args[0])

    results = judge(run, load(expectations))
    width = max((len(sid) for sid, _, _ in results), default=0)
    for sid, verdict, detail in results:
        print(f"  {verdict:<16} {sid:<{width}}  {detail}".rstrip())
    bad = [r for r in results if r[1] not in ("OK", "RED BY DESIGN")]
    held = len(results) - len(bad)
    print(f"\n  {held}/{len(results)} steps as expected")
    if bad:
        print(f"  REGRESSION FAILED — {len(bad)} step(s) not as expected ({run})")
        return 1
    print("  REGRESSION PASSED — every step as expected")
    return 0


if __name__ == "__main__":
    sys.exit(main())

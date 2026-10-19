#!/usr/bin/env python3
"""Every transform implementation is named by an artifact, and every artifact's module exists.

A capability transform is the one family whose artifact points outside the composition, and the
module path is the whole of that pointer. Both ends of that pointer can be wrong, and neither is
visible to anything else we run:

  - **A module nobody names.** `book_library_mgmt` carried `ct_pure_require_condition_v0.py` for two
    releases after its artifact was deleted. Nothing loads it, no rule reads it, and it looks exactly
    like code the composition depends on. A design rule cannot catch it — there is no design.
  - **An artifact naming a module that is not there.** `IMPLEMENTATION_MODULE_MISPLACED` holds a
    *design* to the convention, so a hand-authored artifact, or one whose module was later moved,
    fails at execution and nowhere earlier.

Reads the artifacts as authored rather than a compiled snapshot, so it runs before a build.

Usage:  python .github/process/implementation_closure.py
Exit:   0 if both directions close, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]

# Where a domain keeps its transform implementations. The platform predates the convention and keeps
# them one level up; every other domain follows `<domain>.implementation.capability_transforms.atoms`.
IMPLEMENTATION_DIRS = ("implementation/capability_transforms/atoms",
                       "capability_transforms/implementation")

MODULE = re.compile(r"^\s*module:\s*(\S+)\s*$", re.M)

# Shared machinery that sits alongside the atoms and is imported by them rather than declared.
NOT_A_TRANSFORM = {"__init__", "ct_executor"}


def _skip(path: Path) -> bool:
    return ".git" in path.parts or "snapshot" in path.parts or ".venv" in path.parts


def declared_modules() -> dict[str, Path]:
    """Every module path a CT artifact points at, by its trailing module name."""
    out: dict[str, Path] = {}
    for artifact in WORKSPACE.rglob("CT_*.md"):
        if _skip(artifact):
            continue
        for module in MODULE.findall(artifact.read_text()):
            out[module.rsplit(".", 1)[-1]] = artifact
    return out


def implementation_files() -> dict[str, Path]:
    """Every module sitting in a transform implementation directory, by module name."""
    out: dict[str, Path] = {}
    for parent in IMPLEMENTATION_DIRS:
        for path in WORKSPACE.glob(f"*/{parent}/*.py"):
            out.setdefault(path.stem, path)
        for path in WORKSPACE.glob(f"*/*/{parent}/*.py"):
            out.setdefault(path.stem, path)
        for path in WORKSPACE.glob(f"*/*/*/{parent}/*.py"):
            out.setdefault(path.stem, path)
    return {name: path for name, path in out.items()
            if name not in NOT_A_TRANSFORM and not _skip(path)}


def main() -> int:
    declared, present = declared_modules(), implementation_files()

    ungoverned = sorted(set(present) - set(declared))
    missing = sorted(set(declared) - set(present))

    for name in sorted(declared):
        if name in present:
            print(f"ok      {name}")

    for name in ungoverned:
        print(f"ORPHAN  {name} — {present[name].relative_to(WORKSPACE)}: no CT artifact names it",
              file=sys.stderr)
    for name in missing:
        print(f"ABSENT  {name} — {declared[name].relative_to(WORKSPACE)} points at a module that "
              f"is not on disk", file=sys.stderr)

    if ungoverned or missing:
        print(f"\nIMPLEMENTATION CLOSURE FAILED — {len(ungoverned)} ungoverned, "
              f"{len(missing)} absent", file=sys.stderr)
        return 1

    print(f"\nIMPLEMENTATION CLOSURE PASSED — {len(declared)} transform(s), "
          f"every module named and present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

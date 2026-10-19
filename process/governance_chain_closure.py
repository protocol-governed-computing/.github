#!/usr/bin/env python3
"""The governance chain, wherever an invariant may be authored.

An invariant is authoritative because three relations hold, not because it exists:

  DECLARE   a constitution rule names it. An invariant no constitution declares enforces a rule
            that was never constitutionally established.
  RESOLVE   that rule's `enforced_by` resolves to the invariant, and the invariant's derived
            ASSERT has a registered handler.
  PARITY    invariant and ASSERT are paired — neither exists without the other.

The platform surface proves all three at every build. **A domain build proves none of them**, and
this is not a gap somebody left open — it is structural. Both chain invariants govern the kinds
`CONSTITUTION` and `INVARIANT`, neither of which is domain-instantiated, so the import filter that
admits platform governance into a domain closure never admits either of them:

    INVARIANT_GOVERNANCE_DECLARATION_RESOLVES_V0   applies_to_kinds [CONSTITUTION, INVARIANT]
    INVARIANT_ASSERT_PARITY_V0                     applies_to_kinds [INVARIANT]

So a domain that may author an INVARIANT authors it outside the chain. It is still checked for
shape — FQDN valid, id unique, schema conformant, by eight universal well-formedness invariants
that do reach domain builds — and not at all for authority.

**Why this is not a coverage census.** The obvious encoding of the same idea — every kind a build
may author is covered by at least one governing invariant admitted to it — was measured first and
reports **zero** gaps for every domain, `INVARIANT` included, because those eight shape checks
enumerate every kind. Full coverage, no consequential distinction. A check has to name the relation
it wants or it measures nothing, so this one names three.

Two relations are proved here:

  1. **Every invariant authored outside the platform is named by a constitution rule.**
     Checked across the workspace rather than within a build, because the build cannot: a domain
     build carries no constitutions at all, so there is nothing there for a domain invariant to be
     declared by.

  2. **Any build whose `artifact_types` admits a chain kind can reach the chain checks.**
     Permission to author an INVARIANT without the checks that make one authoritative is how a
     second, unchecked governance surface appears — one line in a build config.

Reads artifacts as authored and imports the compiler's own admission inputs rather than restating
them. A second spelling of `_DOMAIN_INSTANTIATED` here would be the defect this repository has
spent a release deleting.

Usage:  python .github/process/governance_chain_closure.py
Exit:   0 if both relations close, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# The compiler's own admission input, imported rather than copied. If this import fails the check
# must fail with it: a chain check that guesses at the admission rule proves nothing about the
# builds that actually run.
from compiler.stages.s1_extract import _DOMAIN_INSTANTIATED

WORKSPACE = Path(__file__).resolve().parents[2]
PLATFORM = WORKSPACE / "software_governance"

# The three relations, by the artifact that enforces each. Named, not counted.
CHAIN = {
    "DECLARE": "INVARIANT_GOVERNANCE_DECLARATION_RESOLVES_V0",
    "RESOLVE": "INVARIANT_GOVERNANCE_DECLARATION_RESOLVES_V0",
    "PARITY": "INVARIANT_ASSERT_PARITY_V0",
}

# Kinds whose authorship puts an artifact inside the enforcement machinery rather than under it.
CHAIN_KINDS = ("INVARIANT", "CONSTITUTION")

MACHINE_BLOCK = re.compile(r"```yaml\n(.*?)\n```", re.S)


def machine(path: Path) -> dict:
    """The artifact's machine block, or an empty dict if it has none."""
    found = MACHINE_BLOCK.search(path.read_text(encoding="utf-8"))
    if not found:
        return {}
    block = yaml.safe_load(found.group(1))
    return block if isinstance(block, dict) else {}


def repos() -> list[Path]:
    """Every directory in the workspace that carries a registry, at any depth.

    Depth varies by three: `software_governance/registry`, `business_domains/<d>/registry`,
    `conformance_workloads/workloads/<w>/registry`. A fixed set of globs silently skipped the
    business domains — which is the failure mode this whole check exists to catch, so it is
    searched rather than enumerated.
    """
    found = []
    for registry in WORKSPACE.glob("*/**/registry"):
        if registry.is_dir() and not any(
            part in (".venv", "snapshot", "data", ".git") for part in registry.parts
        ):
            found.append(registry.parent)
    return sorted(set(found))


def invariants() -> list[tuple[Path, dict]]:
    """Every authored INVARIANT in the workspace, platform and domain alike."""
    out = []
    for repo in repos():
        for md in sorted((repo / "registry").rglob("INVARIANT_*.md")):
            block = machine(md)
            if block.get("artifact_kind") == "INVARIANT":
                out.append((md, block))
    return out


def declared_by_constitutions() -> set[str]:
    """Every FQDN named by some constitution rule's `enforced_by`, anywhere in the workspace."""
    named: set[str] = set()
    for repo in repos():
        for md in sorted((repo / "registry").rglob("CONSTITUTION_*.md")):
            block = machine(md)
            for rule in block.get("rules") or []:
                target = (rule or {}).get("enforced_by")
                if isinstance(target, str) and "::" in target:
                    named.add(target)
    return named


def admitted_to_domain_builds() -> set[str]:
    """Platform invariants the import filter admits into a domain's governance closure.

    Mirrors `s1_extract._admits_invariant`: a domain-instantiated subject kind, and no declared
    surface — an invariant carrying a specific surface's allow-list is that surface's, and
    importing it would assert the platform's allow-list against a domain that never declared it.
    """
    admitted: set[str] = set()
    for path, block in invariants():
        if PLATFORM not in path.parents:
            continue
        proj = block.get("assert_projection") or {}
        kinds = set(proj.get("applies_to_kinds") or [])
        if kinds & _DOMAIN_INSTANTIATED and not (proj.get("scope") or {}).get("applies_to"):
            admitted.add(path.stem)
    return admitted


def build_configs() -> list[tuple[Path, dict]]:
    """Every build config that compiles against an imported platform surface."""
    out = []
    for repo in repos():
        for md in sorted((repo / "registry").rglob("STRUCTURE_BUILD_*.md")):
            block = machine(md)
            discovery = block.get("artifact_discovery") or {}
            if (discovery.get("import_surface") or {}).get("domain"):
                out.append((md, discovery))
    return out


def main() -> int:
    failures: list[str] = []

    # --- Relation 1: every non-platform invariant is declared by a constitution ------------------
    named = declared_by_constitutions()
    authored = [(p, b) for p, b in invariants() if PLATFORM not in p.parents]
    print(f"  declared   {len(authored)} invariant(s) authored outside the platform surface")
    for path, block in authored:
        fqdn = block.get("fqdn", path.stem)
        if fqdn not in named:
            failures.append(f"{fqdn} is named by no constitution rule")
            print(f"    ORPHAN     {fqdn}")
            print(f"               {path.relative_to(WORKSPACE)}")

    # --- Relation 2: a build that may author a chain kind can reach the chain -------------------
    admitted = admitted_to_domain_builds()
    configs = build_configs()
    print(f"  reachable  {len(configs)} domain build config(s) against {len(admitted)} admitted invariant(s)")
    for path, discovery in configs:
        kinds = [k for k in CHAIN_KINDS if k in (discovery.get("artifact_types") or [])]
        if not kinds:
            continue
        missing = sorted({
            f"{relation} ({artifact})"
            for relation, artifact in CHAIN.items()
            if artifact not in admitted
        })
        if missing:
            failures.append(f"{path.stem} may author {'/'.join(kinds)} with {len(missing)} relation(s) unreachable")
            print(f"    UNCHAINED  {path.stem} may author {'/'.join(kinds)}")
            for relation in missing:
                print(f"               unreachable: {relation}")

    if failures:
        print(f"\nGOVERNANCE CHAIN FAILED — {len(failures)} relation(s) do not close")
        for failure in failures:
            print(f"  · {failure}")
        return 1
    print("\nGOVERNANCE CHAIN PASSED — every authored invariant is declared, every authoring build reaches the chain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

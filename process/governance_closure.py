#!/usr/bin/env python3
"""Two closure relations in the governance surface that nothing else checks.

**This does not prove "governance closure".** It proves exactly the two relations below. Naming it
for the general property would be the same overclaim it exists to catch — an artifact that reads as
authority over more than it governs.

  1. registry handler  ──→ declaring artifact
     Every handler the compiler can run is named by some INVARIANT. A handler nobody declares is
     code that looks like enforcement and enforces nothing; the compiler cannot see it, because it
     iterates invariants and never asks the reverse question. This is the mirror of
     `implementation_closure`'s "a module nobody names".

  2. layer declaration ──→ one declaration per layer
     No layer is declared by two artifacts that disagree about where it lives. The first draft of
     this check asked whether a layer *resolves*, and that was wrong: the compiler's module map
     covers three layers and everything else resolves to None **by design**, so the check reported
     six live, correct declarations as defects. Absence is not the defect — **contradiction is.**

The direction *not* checked here is deliberate. "Every declared handler resolves" is already a hard
build error — `E702_UNKNOWN_ASSERT` in `S4_GOVERN` — for every invariant, because the compiler
derives an ASSERT per invariant and binds its handler by convention. Measured before writing this:
88 invariants, 6 declaring an explicit handler, and **zero** that both declare a handler and are
enforced outside the compiler. So a check here could never fail, and a check that cannot fail is
what this repository keeps finding at the bottom of its worst defects.

What relation 2 catches, and why it is here: three `STRUCTURE_REGISTRY_LOCATION_*_V0` artifacts
declare `registry_module: pgs_governance.registry` and its siblings for GOVERNANCE,
REUSABLE_TRANSFORMS and REUSABLE_SIDE_EFFECTS. `STRUCTURE_DISCOVERY_V0` declares the same three
layers as `software_governance.registry`, `capability_transforms.registry` and
`capability_side_effects.registry` — and says of itself that it is the "single source of truth for
artifact discovery, replacing fragmented registry location and layer authority discovery
definitions". So the supersession was declared and the superseded artifacts were left in place,
still reading as authority. Nothing detected it; a person reading 58 references did.

Reads artifacts as authored rather than a compiled snapshot, so it runs before a build.

Usage:  python .github/process/governance_closure.py
Exit:   0 if both relations close, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
PLATFORM = WORKSPACE / "software_governance"
REGISTRY = PLATFORM / "registry"

# The compiler binds a derived ASSERT's handler by this convention unless the invariant overrides it.
HANDLER_PREFIX = "pgs_governance.registry.handlers"

# How a layer declaration says where its root is, in order of the compiler's own preference.
# `registry_module` is last because it is RI-0 harvest naming kept for backward compatibility, and
# it resolves only through a fixed map — which is exactly how three artifacts came to resolve to
# nothing while looking authoritative.
LAYER_SUBPATH_KEYS = ("domain_subpath", "platform_subpath")
MODULE_MAP = {
    "software_governance.registry": ("registry",),
    "capability_transforms.registry": ("capability_transforms", "registry"),
    "capability_side_effects.registry": ("capability_side_effects", "registry"),
}


def yaml_block(text: str) -> dict:
    import yaml

    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def invariant_handlers() -> set[str]:
    """Every handler key the governance surface names, explicitly or by the compiler's convention."""
    named: set[str] = set()
    for md in sorted(REGISTRY.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        if "artifact_kind: INVARIANT" not in text:
            continue
        code = re.search(r"^\s*invariant_code:\s*(\S+)", text, re.M)
        code = code.group(1) if code else md.stem
        override = re.search(r"^\s*handler:\s*(\S+)", text, re.M)
        if override:
            named.add(override.group(1))
        # The convention applies whether or not an override exists: an invariant with an override
        # still derives its assert code, and both spellings are keys a registry entry may answer to.
        named.add(f"{HANDLER_PREFIX}.{('ASSERT_' + code[len('INVARIANT_'):]).lower()}"
                  if code.startswith("INVARIANT_") else f"{HANDLER_PREFIX}.{code.lower()}")
    return named


def registry_handlers() -> set[str]:
    sys.path.insert(0, str(WORKSPACE / "protocol_compiler"))
    from compiler.governance_engine.assertions.handlers import HANDLER_REGISTRY

    return set(HANDLER_REGISTRY)


def layer_declarations() -> list[tuple[str, str, str]]:
    """(artifact, layer, where-it-says-the-layer-lives) for every declaration in the surface.

    Two shapes are in the surface and both are read, because reading only one is how the older shape
    went unexamined. `STRUCTURE_DISCOVERY_V0` declares `discovery.layers.<LAYER>`; the older
    `STRUCTURE_REGISTRY_LOCATION_*` artifacts declare `core.layer_code` with the root beside it.
    """
    out: list[tuple[str, str, str]] = []
    for md in sorted(REGISTRY.rglob("*.md")):
        block = yaml_block(md.read_text(encoding="utf-8"))
        if not isinstance(block, dict):
            continue
        for name, decl in ((block.get("discovery") or {}).get("layers") or {}).items():
            if isinstance(decl, dict):
                out.append((md.name, name, stated_root(decl)))
        core = block.get("core") or {}
        if isinstance(core, dict) and core.get("layer_code"):
            out.append((md.name, str(core["layer_code"]), stated_root(core)))
    return out


def stated_root(decl: dict) -> str:
    """Where a declaration says a layer lives, as one comparable string.

    Whether it resolves is not asked. The compiler maps three layers into the platform root and
    leaves the rest to resolve to None by design, so an unresolvable root is a normal answer for a
    layer that lives in another repo. What no layer may have is two answers.
    """
    for key in (*LAYER_SUBPATH_KEYS, "registry_module"):
        if decl.get(key):
            return f"{key}={decl[key]}"
    return "unstated"


def main() -> int:
    failures: list[str] = []

    named, live = invariant_handlers(), registry_handlers()
    orphans = sorted(live - named)
    print(f"  handlers   {len(live)} in the registry, {len(named)} named by an invariant")
    for handler in orphans:
        failures.append(f"handler named by no invariant: {handler}")
        print(f"    ORPHAN   {handler}")

    declarations = layer_declarations()
    by_layer: dict[str, set[tuple[str, str]]] = {}
    for artifact, layer, root in declarations:
        by_layer.setdefault(layer, set()).add((artifact, root))
    print(f"  layers     {len(declarations)} declaration(s) over {len(by_layer)} layer(s)")
    for layer in sorted(by_layer):
        # An artifact that declares a layer without saying where it lives is not a second answer.
        # `STRUCTURE_REGISTRY_LOCATION_*` still declare `reuse_visibility` for their layer and no
        # longer declare its root; that is one answer plus a different fact, not a contradiction.
        stated = {(a, r) for a, r in by_layer[layer] if r != "unstated"}
        if len({root for _, root in stated}) > 1:
            failures.append(f"{layer} is declared {len(stated)} ways")
            print(f"    CONFLICT   {layer}")
            for artifact, root in sorted(stated):
                print(f"               {root:<52} {artifact}")

    if failures:
        print(f"\nGOVERNANCE CLOSURE FAILED — {len(failures)} relation(s) do not close")
        return 1
    print("\nGOVERNANCE CLOSURE PASSED — every handler is declared, every layer declared once")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
